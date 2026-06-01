# 🔄 05 — State, File Uploads, And Real-Time

> *"A good app feels instant and alive. Instant comes from optimistic updates that don't wait for the server. Alive comes from sockets that tell you what changed before you ask. Both are illusions you engineer on purpose."*

**Prev:** [`04-Authentication-Across-The-Stack.md`](./04-Authentication-Across-The-Stack.md) · **Next:** [`06-Testing-Building-And-Deploying-MERN.md`](./06-Testing-Building-And-Deploying-MERN.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT WE ARE BUILDING

TaskFlow works and is authenticated. Now we make it feel like a real product:

- A clear model of **client state vs server state**, and which tool owns each
- **TanStack Query as the server-state cache** (recap + the deeper why)
- **File/image uploads** — multer (disk vs memory), limits, file filters, `FormData` on the frontend, and serving uploads vs cloud storage
- **Socket.IO real-time** — server setup alongside Express, authenticated sockets, per-user rooms, the client reacting to events
- **Optimistic updates** — UI that responds before the server does, with rollback on failure

---

## II. CLIENT STATE vs SERVER STATE (THE DEEPER CUT)

File 03 introduced this; here is the rule that resolves 90% of "where does this state go?" questions.

```text
Ask: "If I closed this tab and reopened it, should this value still exist
      because it lives on the server?"

  YES → SERVER STATE  → TanStack Query (it's a cache of remote data)
  NO  → CLIENT STATE  → useState / useReducer / Context / Zustand
```

| State | Kind | Tool |
|-------|------|------|
| The task list, current user, notifications | Server | **TanStack Query** |
| Is the "new task" modal open? | Client (UI) | `useState` |
| Dark mode, sidebar collapsed | Client (UI, maybe persisted) | Context / `localStorage` |
| The logged-in user object | Server-derived, app-wide | Auth Context (file 04) |
| Current filter/sort selection | Client (drives a server query) | `useState` in the page |

### When do you need Redux / Zustand?

Most MERN apps **don't**, once Query owns server state. Reach for a client-state store only when you have **complex, app-wide *client* state** that many distant components read and write (e.g. a multi-step wizard, a complex editor, cross-cutting UI selection).

| Tool | Use when |
|------|----------|
| `useState` / `useReducer` | Local component state |
| Context | A handful of app-wide values (auth, theme), low update frequency |
| **Zustand** | App-wide client state, simple API, no boilerplate |
| **Redux Toolkit** | Large team, complex client state, time-travel debugging, strict conventions |
| **TanStack Query** | *Anything from the server* (the common case) |

> **Gotcha — the "everything in global state" anti-pattern.** Beginners dump server data into Redux, then hand-write loading flags, refetch logic, and cache invalidation — re-implementing TanStack Query badly. Server data is **not** global client state; it is a *cache of remote truth*. Keep it in Query. Reserve a global store for genuine client state.

---

## III. FILE UPLOADS — THE BACKEND WITH MULTER

JSON can't carry binary files, so uploads use **`multipart/form-data`**. On Express, **multer** parses that.

```bash
cd server
npm install multer
```

### Disk vs memory storage

```js
// server/src/middleware/upload.js
import multer from 'multer';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { AppError } from '../utils/AppError.js';

// __dirname doesn't exist in ES modules — reconstruct it (noted in file 02).
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const UPLOAD_DIR = path.join(__dirname, '../../uploads');

// DISK storage: stream the file straight to disk. Good for large files / local dev.
const diskStorage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, UPLOAD_DIR),
  filename: (req, file, cb) => {
    // Never trust the original filename — generate a random, safe one.
    const ext = path.extname(file.originalname).toLowerCase();
    const name = `${Date.now()}-${crypto.randomBytes(8).toString('hex')}${ext}`;
    cb(null, name);
  },
});

// MEMORY storage: keep the file as a Buffer in RAM. Good when you immediately
// forward to cloud storage (S3/Cloudinary) and never touch local disk.
// const memoryStorage = multer.memoryStorage();

// Only allow images, and cap the size.
function fileFilter(req, file, cb) {
  const allowed = ['image/png', 'image/jpeg', 'image/webp', 'image/gif'];
  if (!allowed.includes(file.mimetype)) {
    return cb(new AppError('Only image files are allowed', 400, 'BAD_FILE_TYPE'), false);
  }
  cb(null, true);   // accept
}

export const uploadImage = multer({
  storage: diskStorage,
  fileFilter,
  limits: {
    fileSize: 2 * 1024 * 1024,   // 2 MB max — reject larger BEFORE buffering it all
    files: 1,
  },
});
```

| | Disk storage | Memory storage |
|---|--------------|----------------|
| Where the file lands | server filesystem | a `Buffer` in RAM (`file.buffer`) |
| Big files | fine (streamed) | risky (RAM spikes) |
| Best paired with | serving from a static dir | forwarding to S3/Cloudinary |
| Survives a restart/redeploy | only if disk is persistent | n/a |

### The upload route

```js
// server/src/routes/upload.routes.js
import { Router } from 'express';
import { protect } from '../middleware/auth.js';
import { uploadImage } from '../middleware/upload.js';
import { asyncHandler } from '../utils/asyncHandler.js';
import { ok } from '../utils/respond.js';
import { User } from '../models/User.js';

const router = Router();

// upload.single('avatar') parses ONE file from the "avatar" form field.
// multer puts file metadata on req.file and any text fields on req.body.
router.post(
  '/avatar',
  protect,
  uploadImage.single('avatar'),
  asyncHandler(async (req, res) => {
    if (!req.file) throw new Error('No file uploaded');
    // Public URL the frontend can render (served statically below).
    const url = `/uploads/${req.file.filename}`;
    await User.findByIdAndUpdate(req.user.id, { avatarUrl: url });
    return ok(res, { avatarUrl: url }, 201);
  })
);

export default router;
```

### Serving uploaded files (local) vs cloud storage

```js
// server/src/app.js  (addition)
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Serve the uploads folder as static files at /uploads/*
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));
app.use('/api/uploads', uploadRoutes);   // the upload endpoints
```

> 🔒 **Gotcha — never trust the uploaded filename or MIME alone.** Attackers send `evil.png` that's actually a script, or path-traversal names like `../../etc/passwd`. We (1) **generate** a random filename, (2) check the MIME via `fileFilter`, and (3) cap size with `limits`. For real security also verify the file's *magic bytes* (actual content), and never serve user uploads from the same origin as sensitive HTML without thought. Better yet, offload to **cloud storage**.

> **Gotcha — local disk is ephemeral on most hosts.** Platforms like Render/Railway/Heroku wipe the filesystem on every deploy/restart. Files saved to local disk *vanish*. For production, use **memory storage + upload to S3/Cloudinary** (or a persistent volume). Local disk is fine for dev and learning. We flag this again in file 06.

### The frontend upload — FormData

```jsx
// client/src/features/profile/AvatarUpload.jsx
import { useState } from 'react';
import { api } from '../../api/client';

export default function AvatarUpload({ onUploaded }) {
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const onChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Client-side guardrails (UX) — server still enforces the real limits.
    if (file.size > 2 * 1024 * 1024) return setError('Max 2 MB');
    if (!file.type.startsWith('image/')) return setError('Images only');

    setError(null);
    setPreview(URL.createObjectURL(file));   // instant local preview, no upload yet

    // FormData → axios sends multipart/form-data. Do NOT set Content-Type manually;
    // the browser sets it WITH the required multipart boundary.
    const fd = new FormData();
    fd.append('avatar', file);               // field name must match upload.single('avatar')

    setUploading(true);
    try {
      const { data } = await api.post('/uploads/avatar', fd);
      onUploaded?.(data.data.avatarUrl);
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="avatar-upload">
      {preview && <img src={preview} alt="preview" className="avatar-preview" />}
      <input type="file" accept="image/*" onChange={onChange} disabled={uploading} />
      {uploading && <span>Uploading…</span>}
      {error && <p className="form-error">{error}</p>}
    </div>
  );
}
```

> **Gotcha — don't hand-set `Content-Type` for FormData.** If you set `Content-Type: multipart/form-data` yourself, you omit the **boundary** the server needs to parse parts, and multer fails. Let axios/the browser set it automatically when you pass a `FormData` body.

---

## IV. REAL-TIME WITH SOCKET.IO — WHY AND WHEN

REST is request/response: the client must *ask*. For "task updated by a teammate" you'd have to **poll** (ask repeatedly), which is wasteful and laggy. **WebSockets** keep a persistent connection so the server can **push** the moment something changes. Socket.IO is a battle-tested wrapper over WebSockets with reconnection and room support.

| | Polling | WebSockets (Socket.IO) |
|---|---------|------------------------|
| Direction | client pulls | server pushes |
| Latency | up to the poll interval | near-instant |
| Server load | many redundant requests | one persistent connection |
| Best for | infrequent changes | live updates, chat, notifications |

```bash
cd server && npm install socket.io
cd ../client && npm install socket.io-client
```

### Server: attach Socket.IO to the same HTTP server

```js
// server/src/realtime/io.js
import { Server } from 'socket.io';
import jwt from 'jsonwebtoken';
import { authConfig } from '../config/auth.config.js';

let io;   // module-level so services can emit from anywhere

export function initSocket(httpServer, clientOrigin) {
  io = new Server(httpServer, {
    cors: { origin: clientOrigin, credentials: true },   // same CORS care as REST
  });

  // AUTH MIDDLEWARE for sockets — runs once per connection.
  io.use((socket, next) => {
    // Client passes the access token in the handshake auth payload.
    const token = socket.handshake.auth?.token;
    if (!token) return next(new Error('Unauthorized'));
    try {
      const payload = jwt.verify(token, authConfig.accessSecret);
      socket.userId = payload.sub;          // remember who this socket belongs to
      next();
    } catch {
      next(new Error('Unauthorized'));
    }
  });

  io.on('connection', (socket) => {
    // Put every user in a private ROOM named by their id.
    // Now we can target notifications to exactly one user, across all their tabs/devices.
    socket.join(`user:${socket.userId}`);
    console.log(`🔌 socket connected: user ${socket.userId}`);

    socket.on('disconnect', () => {
      console.log(`socket disconnected: user ${socket.userId}`);
    });
  });

  return io;
}

// Helpers services call to push events to a specific user's room.
export function emitToUser(userId, event, payload) {
  if (io) io.to(`user:${userId}`).emit(event, payload);
}
```

### Wire it into the server entry point

```js
// server/src/server.js  (updated from file 02)
import http from 'node:http';
import { createApp } from './app.js';
import { connectDB, disconnectDB } from './config/db.js';
import { env } from './config/env.js';
import { initSocket } from './realtime/io.js';

async function start() {
  await connectDB();
  const app = createApp();
  const httpServer = http.createServer(app);   // wrap Express so Socket.IO can share the port
  initSocket(httpServer, env.CLIENT_ORIGIN);    // Socket.IO + Express, ONE server, ONE port

  httpServer.listen(env.PORT, () => console.log(`🚀 API + WS on :${env.PORT}`));

  const shutdown = async () => {
    httpServer.close(async () => { await disconnectDB(); process.exit(0); });
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}
start();
```

### Emit from the task service when data changes

```js
// server/src/services/task.service.js  (emit on mutations)
import { emitToUser } from '../realtime/io.js';

// inside create():
async create(ownerId, data) {
  const task = await Task.create({ ...data, owner: ownerId });
  emitToUser(ownerId, 'task:created', task);   // push to all the user's open tabs
  return task;
},

// inside update():
async update(ownerId, taskId, data) {
  const task = await Task.findOneAndUpdate(
    { _id: taskId, owner: ownerId }, data, { new: true, runValidators: true }
  );
  if (!task) throw AppError.notFound('Task not found');
  emitToUser(ownerId, 'task:updated', task);
  return task;
},
```

> **Gotcha — Socket.IO and Express must share ONE HTTP server.** A common mistake is `app.listen()` *and* `new Server(somePort)` separately — now you have two servers and the proxy/CORS only covers one. Create one `http.Server` from the Express app and hand it to Socket.IO. (The Vite proxy entry for `/socket.io` with `ws:true` from file 01 makes this work in dev.)

> 🔒 **Gotcha — authenticate sockets, don't trust them.** A WebSocket connection is just as forgeable as an HTTP request. Verify the JWT in `io.use(...)` before joining rooms, and scope rooms by the *verified* `userId` — never by an id the client sends in an event payload, or user A can subscribe to user B's notifications.

### Client: connect and react to events

```js
// client/src/realtime/socket.js
import { io } from 'socket.io-client';
import { getAccessToken } from '../api/client';

let socket = null;

export function connectSocket() {
  if (socket) return socket;
  socket = io({                              // same origin → Vite proxies /socket.io in dev
    autoConnect: true,
    auth: { token: getAccessToken() },       // send the access token in the handshake
  });
  return socket;
}

export function disconnectSocket() {
  socket?.disconnect();
  socket = null;
}
```

```jsx
// client/src/realtime/useTaskEvents.js — sync sockets INTO the Query cache
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { connectSocket, disconnectSocket } from './socket';
import { useAuth } from '../context/AuthContext';

export function useTaskEvents() {
  const qc = useQueryClient();
  const { user } = useAuth();

  useEffect(() => {
    if (!user) return;
    const socket = connectSocket();

    // When the server says data changed, invalidate the cache → Query refetches.
    const onChange = () => qc.invalidateQueries({ queryKey: ['tasks'] });
    socket.on('task:created', onChange);
    socket.on('task:updated', onChange);

    return () => {
      socket.off('task:created', onChange);
      socket.off('task:updated', onChange);
      disconnectSocket();
    };
  }, [user, qc]);
}
```

Call `useTaskEvents()` once near the top of the authenticated app (e.g. in `RootLayout` behind the auth check) and every open tab updates live.

> **Gotcha — bridge sockets to your cache, don't fork state.** The temptation is to keep a *separate* socket-driven list in `useState`. Then you have two sources of truth (Query cache + socket state) that drift. Instead, let socket events **invalidate** Query (or `setQueryData`) so there's still one source of truth. Real-time becomes "a smarter trigger for the cache you already have."

---

## V. OPTIMISTIC UPDATES — UI THAT DOESN'T WAIT

Invalidation refetches *after* the server confirms — correct, but the user waits a round trip. **Optimistic updates** apply the change to the cache *immediately*, then reconcile (and roll back on failure). This is what makes toggling a task feel instant.

```js
// client/src/features/tasks/useTasks.js  (optimistic update variant)
export function useToggleTaskOptimistic() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }) => tasksApi.update(id, { status }),

    // 1) BEFORE the request — update the cache optimistically.
    onMutate: async ({ id, status }) => {
      await qc.cancelQueries({ queryKey: ['tasks'] });   // stop in-flight refetches racing us
      const previous = qc.getQueriesData({ queryKey: ['tasks'] });  // snapshot for rollback

      // Patch every cached task list to reflect the new status now.
      qc.setQueriesData({ queryKey: ['tasks'] }, (old) => {
        if (!old?.data) return old;
        return { ...old, data: old.data.map((t) => (t._id === id ? { ...t, status } : t)) };
      });

      return { previous };   // becomes `context` in onError
    },

    // 2) ON FAILURE — roll back to the snapshot.
    onError: (_err, _vars, context) => {
      context?.previous?.forEach(([key, data]) => qc.setQueryData(key, data));
    },

    // 3) ALWAYS — refetch to converge with the server's truth.
    onSettled: () => qc.invalidateQueries({ queryKey: ['tasks'] }),
  });
}
```

```text
optimistic update lifecycle
  onMutate  → snapshot + patch cache   (UI updates INSTANTLY)
      │
   request fires
      ├── success → onSettled refetch confirms (no visible change)
      └── failure → onError rolls back to snapshot (UI reverts) → onSettled refetch
```

> **Gotcha — always snapshot and always roll back.** The danger of optimistic UI is showing a change that the server then *rejects* (validation, permission, network). Without the `onMutate` snapshot + `onError` rollback, the user sees a lie that never corrects. `cancelQueries` matters too: an in-flight refetch could overwrite your optimistic patch with stale data mid-flight.

> **Optimistic + real-time together.** With both: `onMutate` updates the actor's UI instantly; the server emits `task:updated`; *other* tabs/devices get the change via socket invalidation; `onSettled` reconciles the actor with server truth. Snappy for the actor, live for everyone else.

---

## VI. PUTTING IT TOGETHER — THE FULL EXPERIENCE

A user toggles a task to "done":

```text
1. Click → useToggleTaskOptimistic.mutate()
2. onMutate patches the Query cache → checkbox flips INSTANTLY (no wait)
3. axios PATCH /api/tasks/:id  → controller → service.update()
4. service emits 'task:updated' to user:<id> room
5. the user's OTHER tabs receive it → invalidate → refetch → stay in sync
6. response resolves → onSettled invalidates → this tab reconciles with server truth
7. if the PATCH had failed → onError rolls the checkbox back
```

Instant (optimistic) + alive (sockets) + correct (reconcile/rollback). That trio is what separates a toy from a product.

---

## VII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Server data in a global store | Re-implementing caching badly | Keep server state in TanStack Query |
| Setting `Content-Type` for FormData | multer can't parse; upload fails | Let the browser set it (with boundary) |
| Trusting uploaded filename/MIME | Path traversal, disguised files | Random filename, MIME filter, size limit, magic-byte check |
| Saving uploads to local disk in prod | Files vanish on redeploy | Cloud storage (S3/Cloudinary) or persistent volume |
| Two separate HTTP servers | Sockets/CORS/proxy half-work | One `http.Server` shared by Express + Socket.IO |
| Unauthenticated sockets | Users subscribe to others' events | Verify JWT in `io.use`; rooms by verified id |
| Rooms keyed by client-sent id | Cross-user eavesdropping | Key rooms by the server-verified `userId` |
| Separate socket state + Query | Two sources of truth, drift | Socket events invalidate/patch the Query cache |
| Optimistic update without rollback | UI shows a change the server rejected | Snapshot in `onMutate`, restore in `onError` |
| No `cancelQueries` in `onMutate` | In-flight refetch clobbers optimistic patch | `await cancelQueries` first |

---

## 🧠 KEY TAKEAWAYS

- Decide state placement with one question: *would this survive a tab reload because it lives on the server?* If yes → **server state (TanStack Query)**; if no → **client state**. Most apps need no Redux/Zustand once Query owns server state.
- Uploads use **`multipart/form-data`** + **multer**. Choose **disk** storage for local/large files, **memory** when forwarding to cloud. Always set **size limits** and a **file filter**, and generate safe filenames.
- **Never trust uploaded files**; local disk is **ephemeral** on most hosts — use **cloud storage** in production. On the frontend, pass `FormData` and let the browser set `Content-Type`.
- **Socket.IO shares ONE HTTP server** with Express. **Authenticate every socket** via JWT in `io.use`, and scope **per-user rooms** by the *verified* id.
- **Bridge real-time into the Query cache** (invalidate/`setQueryData`) instead of forking a second source of truth.
- **Optimistic updates** make the UI instant: patch the cache in `onMutate` (after `cancelQueries`), **roll back in `onError`** from a snapshot, and **reconcile in `onSettled`**.
- Combine optimistic UI (instant for the actor) with sockets (live for everyone else) and reconciliation (correct for all) to make TaskFlow feel like a product.

---

**Prev:** [`04-Authentication-Across-The-Stack.md`](./04-Authentication-Across-The-Stack.md) · **Next:** [`06-Testing-Building-And-Deploying-MERN.md`](./06-Testing-Building-And-Deploying-MERN.md) · **Index:** [`00-Index.md`](./00-Index.md)
