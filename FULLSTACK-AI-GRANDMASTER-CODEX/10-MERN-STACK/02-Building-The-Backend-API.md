# 🛠️ 02 — Building The Backend API

> *"The backend is the part of your app no user ever sees and every user depends on. Build it in layers, validate at the door, and fail loudly in one place — and it will carry weight you never imagined."*

**Prev:** [`01-The-MERN-Architecture.md`](./01-The-MERN-Architecture.md) · **Next:** [`03-Building-The-React-Frontend.md`](./03-Building-The-React-Frontend.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT WE ARE BUILDING

In this file we build the entire **TaskFlow server** — the Express + Mongoose API that file 03's React app will consume. By the end you will have:

- A scaffolded Express app with a clean entry point and a testable `app.js`
- A **validated environment config** module (dotenv + zod)
- A **MongoDB connection** with lifecycle events and graceful shutdown
- Two Mongoose models — **`User`** and **`Task`** — with schemas, validation, refs, and timestamps
- A **layered architecture**: `routes → controllers → services → models`
- Full **CRUD REST endpoints** for tasks with pagination, filtering, and sorting
- **zod validation** at the boundary
- A **centralized error handler**, a custom `AppError`, and an `asyncHandler` wrapper
- **CORS** configured for the React client and a consistent **JSON response envelope**

> This file integrates Express and Mongoose; their deep dives live in [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/00-Index.md) and [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/00-Index.md). Here we wire them into a real API.

---

## II. SCAFFOLD THE SERVER

From the monorepo root created in file 01:

```bash
mkdir server && cd server
npm init -y
```

Install runtime and dev dependencies:

```bash
# runtime
npm install express mongoose dotenv cors zod cookie-parser

# dev: nodemon restarts on file change
npm install --save-dev nodemon
```

We will use **ES modules** (`import`/`export`) to match the frontend. Enable them and add scripts:

```jsonc
// server/package.json
{
  "name": "taskflow-server",
  "version": "1.0.0",
  "type": "module",                 // ← enables import/export syntax in .js files
  "scripts": {
    "dev": "nodemon src/server.js", // auto-restart on save
    "start": "node src/server.js"   // production
  }
}
```

Create the folder structure:

```bash
mkdir -p src/config src/models src/routes src/controllers src/services src/middleware src/utils
```

> **Gotcha — `"type": "module"` changes everything.** With it, `require`/`module.exports` no longer work; you must use `import`/`export`, and `__dirname` is gone (reconstruct it with `import.meta.url`). The payoff is one module system across your whole stack. We show the `__dirname` workaround when serving uploads in file 05.

---

## III. ENVIRONMENT CONFIG — LOAD ONCE, VALIDATE, EXPORT

Reading `process.env.X` scattered across the codebase is fragile — a typo or missing variable fails deep in a request instead of at boot. Centralize and **validate** config in one module so the app refuses to start if misconfigured.

```js
// server/src/config/env.js
import 'dotenv/config';   // loads server/.env into process.env (side-effect import)
import { z } from 'zod';

// Describe EXACTLY what env we require and its types/defaults.
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().default(5000),         // coerce: env vars are strings → number
  MONGODB_URI: z.string().min(1, 'MONGODB_URI is required'),
  JWT_SECRET: z.string().min(10, 'JWT_SECRET must be set (≥10 chars)'),
  JWT_REFRESH_SECRET: z.string().min(10),
  CLIENT_ORIGIN: z.string().url().default('http://localhost:5173'),
});

// Validate at import time. If it fails, crash NOW with a clear message.
const parsed = envSchema.safeParse(process.env);
if (!parsed.success) {
  console.error('❌ Invalid environment variables:');
  console.error(parsed.error.flatten().fieldErrors);
  process.exit(1);   // fail fast — do not boot a misconfigured server
}

export const env = parsed.data;   // typed, validated, the ONLY way to read config
```

```bash
# server/.env  (from file 01 — never committed)
NODE_ENV=development
PORT=5000
MONGODB_URI=mongodb://localhost:27017/taskflow
JWT_SECRET=dev-only-change-me-to-a-long-random-string
JWT_REFRESH_SECRET=dev-only-another-long-random-string
CLIENT_ORIGIN=http://localhost:5173
```

> **Gotcha — env vars are always strings.** `process.env.PORT` is `"5000"`, not `5000`. `z.coerce.number()` converts it. Comparing a string port to a number, or doing math on it, causes subtle bugs. Coerce at the boundary, once.

---

## IV. CONNECT TO MONGODB WITH LIFECYCLE EVENTS

```js
// server/src/config/db.js
import mongoose from 'mongoose';
import { env } from './env.js';

export async function connectDB() {
  // Strict query: Mongoose ignores fields not in the schema for queries (safer).
  mongoose.set('strictQuery', true);

  // Connection lifecycle events — log them so you SEE what the DB is doing.
  mongoose.connection.on('connected', () => console.log('✅ MongoDB connected'));
  mongoose.connection.on('error', (err) => console.error('❌ MongoDB error:', err.message));
  mongoose.connection.on('disconnected', () => console.warn('⚠️  MongoDB disconnected'));

  try {
    await mongoose.connect(env.MONGODB_URI, {
      serverSelectionTimeoutMS: 5000,  // fail fast if DB unreachable (don't hang forever)
    });
  } catch (err) {
    console.error('❌ Initial MongoDB connection failed:', err.message);
    process.exit(1);  // can't run without a DB — exit so the platform restarts us
  }
}

// Graceful shutdown: close the DB connection cleanly on Ctrl-C / container stop.
export async function disconnectDB() {
  await mongoose.connection.close();
  console.log('🔌 MongoDB connection closed');
}
```

> **Gotcha — `serverSelectionTimeoutMS`.** Without it, if the DB is unreachable Mongoose retries silently and your requests hang for ~30s before a confusing timeout. Setting it to 5s means you find out fast. In production a process manager (or Render/Railway) restarts the crashed process.

---

## V. THE RESPONSE ENVELOPE, AppError, AND asyncHandler

Three small utilities make the whole API consistent. Build them before the features.

### The success envelope

```js
// server/src/utils/respond.js
// Every successful response goes through here → the frontend can rely on ONE shape.
export function ok(res, data, status = 200, meta = undefined) {
  const body = { data };
  if (meta) body.meta = meta;       // pagination etc., only when present
  return res.status(status).json(body);
}
```

### A custom, operational error class

```js
// server/src/utils/AppError.js
// Distinguishes EXPECTED errors (bad input, not found) from bugs.
// `isOperational` errors are safe to show the client; everything else is a 500.
export class AppError extends Error {
  constructor(message, statusCode = 500, code = 'INTERNAL', details = null) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;          // machine-readable: 'NOT_FOUND', 'VALIDATION', ...
    this.details = details;    // optional structured info (e.g. field errors)
    this.isOperational = true; // we threw this on purpose, it's not a crash
    Error.captureStackTrace(this, this.constructor);
  }

  static notFound(msg = 'Resource not found') { return new AppError(msg, 404, 'NOT_FOUND'); }
  static badRequest(msg = 'Bad request', details) { return new AppError(msg, 400, 'BAD_REQUEST', details); }
  static unauthorized(msg = 'Not authenticated') { return new AppError(msg, 401, 'UNAUTHORIZED'); }
  static forbidden(msg = 'Not allowed') { return new AppError(msg, 403, 'FORBIDDEN'); }
}
```

### The async wrapper — no more try/catch in every handler

```js
// server/src/utils/asyncHandler.js
// Express (v4) does NOT catch rejected promises in async handlers — an unhandled
// rejection would hang the request. This wrapper forwards any error to next().
export const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
```

> **Gotcha — async errors in Express 4 vanish.** If an `async` route handler throws and you don't `.catch` it, Express never sees the error, the client waits forever, and your central handler never runs. `asyncHandler` is the standard fix. (Express 5 handles this natively, but most deployed code is still v4.)

---

## VI. THE MODELS — USER AND TASK

Mongoose schemas are where your data shape, validation, and relationships live.

### User model

```js
// server/src/models/User.js
import mongoose from 'mongoose';

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Name is required'],
      trim: true,
      maxlength: [80, 'Name too long'],
    },
    email: {
      type: String,
      required: [true, 'Email is required'],
      unique: true,                  // creates a unique index (no duplicate emails)
      lowercase: true,               // normalize before saving
      trim: true,
      match: [/^\S+@\S+\.\S+$/, 'Invalid email'],
    },
    // Stored as a bcrypt HASH (file 04), never plaintext.
    // select:false → never returned by queries unless explicitly asked for.
    passwordHash: {
      type: String,
      required: true,
      select: false,
    },
    // Refresh-token rotation store (file 04).
    refreshTokens: { type: [String], default: [], select: false },
    avatarUrl: { type: String, default: null },   // file 05
  },
  { timestamps: true }   // adds createdAt & updatedAt automatically
);

// Transform JSON output: never leak the hash or internal fields to the client.
userSchema.set('toJSON', {
  transform: (_doc, ret) => {
    delete ret.passwordHash;
    delete ret.refreshTokens;
    delete ret.__v;
    return ret;
  },
});

export const User = mongoose.model('User', userSchema);
```

### Task model — with a reference to its owner

```js
// server/src/models/Task.js
import mongoose from 'mongoose';

const taskSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Title is required'],
      trim: true,
      maxlength: [200, 'Title too long'],
    },
    description: { type: String, default: '', maxlength: 2000 },
    status: {
      type: String,
      enum: ['todo', 'in_progress', 'done'],  // only these values allowed
      default: 'todo',
    },
    priority: {
      type: String,
      enum: ['low', 'medium', 'high'],
      default: 'medium',
    },
    dueDate: { type: Date, default: null },
    // The OWNER — a reference (foreign key) to a User document.
    owner: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',                  // enables .populate('owner') to fetch the user
      required: true,
      index: true,                  // we query by owner constantly → index it
    },
    attachmentUrl: { type: String, default: null },  // file 05
  },
  { timestamps: true }
);

// Compound index: list a user's tasks newest-first efficiently.
taskSchema.index({ owner: 1, createdAt: -1 });

taskSchema.set('toJSON', {
  transform: (_doc, ret) => { delete ret.__v; return ret; },
});

export const Task = mongoose.model('Task', taskSchema);
```

> **Gotcha — `ref` does not enforce a foreign key.** MongoDB will happily store an `owner` ObjectId that points to a deleted/nonexistent user. `ref` only tells `.populate()` which collection to look in. *You* enforce integrity in code (e.g., delete a user's tasks when the user is deleted). This is the flexibility-vs-safety tradeoff from file 01, made concrete.

| Schema feature | What it does | Example above |
|----------------|--------------|---------------|
| `required` | Reject save if missing | `title`, `email` |
| `enum` | Restrict to a set of values | `status`, `priority` |
| `unique` | DB-level uniqueness index | `email` |
| `ref` + `ObjectId` | Relationship to another model | `owner → User` |
| `timestamps` | Auto `createdAt`/`updatedAt` | both models |
| `select: false` | Hide field from queries by default | `passwordHash` |
| `toJSON.transform` | Shape what serializes to the client | strip hash, `__v` |
| `index` | Speed up frequent queries | `owner` |

---

## VII. THE LAYERED ARCHITECTURE

Each request flows through clearly separated layers, each with one responsibility:

```text
HTTP request
   │
   ▼
routes/        → maps URL + verb to a controller; attaches middleware (auth, validate)
   │
   ▼
controllers/   → reads req (params/body/user), calls a service, sends the response
   │             (NO business logic, NO direct DB access)
   ▼
services/      → the business logic; orchestrates models; throws AppError on rule violations
   │             (NO knowledge of req/res — pure-ish, testable)
   ▼
models/        → Mongoose schemas; the only thing that touches MongoDB
```

Why bother? Each layer is independently testable and swappable. You can unit-test a **service** with no HTTP, reuse it from a Socket.IO handler (file 05), and keep controllers thin enough to read at a glance.

> **Gotcha — the classic anti-pattern is the "fat controller".** Beginners cram validation, DB queries, and business rules into the route handler. It works until the logic is needed elsewhere (a cron job, a socket event) and cannot be reused without copy-paste. Keep business logic in services from day one.

---

## VIII. THE TASK SERVICE — BUSINESS LOGIC

The service owns the rules: ownership scoping, "not found" handling, pagination math. It knows nothing about HTTP.

```js
// server/src/services/task.service.js
import { Task } from '../models/Task.js';
import { AppError } from '../utils/AppError.js';

export const taskService = {
  // List tasks for ONE user, with filtering/sorting/pagination.
  async list(ownerId, { status, priority, sort = '-createdAt', page = 1, limit = 20 }) {
    const filter = { owner: ownerId };           // ALWAYS scope to the owner
    if (status) filter.status = status;
    if (priority) filter.priority = priority;

    const skip = (page - 1) * limit;

    // Run the data query and the count in parallel (independent → Promise.all).
    const [items, total] = await Promise.all([
      Task.find(filter).sort(sort).skip(skip).limit(limit),
      Task.countDocuments(filter),
    ]);

    return {
      items,
      meta: { page, limit, total, pages: Math.ceil(total / limit) },
    };
  },

  async getById(ownerId, taskId) {
    const task = await Task.findOne({ _id: taskId, owner: ownerId });
    if (!task) throw AppError.notFound('Task not found');  // also covers "not yours"
    return task;
  },

  async create(ownerId, data) {
    return Task.create({ ...data, owner: ownerId });
  },

  async update(ownerId, taskId, data) {
    const task = await Task.findOneAndUpdate(
      { _id: taskId, owner: ownerId },  // scope: can only update YOUR task
      data,
      { new: true, runValidators: true } // return updated doc; re-run schema validation
    );
    if (!task) throw AppError.notFound('Task not found');
    return task;
  },

  async remove(ownerId, taskId) {
    const res = await Task.findOneAndDelete({ _id: taskId, owner: ownerId });
    if (!res) throw AppError.notFound('Task not found');
    return null;
  },
};
```

> **Gotcha — `findOneAndUpdate` skips validators by default.** Schema validators (`enum`, `maxlength`, etc.) do **not** run on updates unless you pass `{ runValidators: true }`. Forget it and a `PATCH` can write `status: "banana"` straight past your `enum`. Always set it on updates.

> **Gotcha — scope EVERY query by owner.** Note every method filters by `owner: ownerId`. Returning a task by `_id` alone would let user A read/edit user B's tasks just by guessing an id (an "IDOR" vulnerability). Authorization is enforced in the query itself, not bolted on after.

---

## IX. VALIDATION AT THE BOUNDARY WITH ZOD

Never trust the client. Validate the request body/query *before* it reaches a controller, using a reusable middleware.

```js
// server/src/middleware/validate.js
import { AppError } from '../utils/AppError.js';

// Returns middleware that validates a chosen part of the request against a zod schema,
// REPLACING it with the parsed (coerced, defaulted) value on success.
export const validate = (schema, source = 'body') => (req, res, next) => {
  const result = schema.safeParse(req[source]);
  if (!result.success) {
    // Flatten zod's error into a friendly field→messages map for the frontend.
    const details = result.error.flatten().fieldErrors;
    return next(AppError.badRequest('Validation failed', details));
  }
  req[source] = result.data;   // use the cleaned data downstream
  next();
};
```

```js
// server/src/validators/task.schema.js
import { z } from 'zod';

export const createTaskSchema = z.object({
  title: z.string().trim().min(1, 'Title is required').max(200),
  description: z.string().max(2000).optional(),
  status: z.enum(['todo', 'in_progress', 'done']).optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
  dueDate: z.coerce.date().optional(),
});

// Update = every field optional, but at least one must be present.
export const updateTaskSchema = createTaskSchema.partial().refine(
  (obj) => Object.keys(obj).length > 0,
  { message: 'Provide at least one field to update' }
);

// Query params arrive as strings → coerce numbers, constrain enums.
export const listTaskQuerySchema = z.object({
  status: z.enum(['todo', 'in_progress', 'done']).optional(),
  priority: z.enum(['low', 'medium', 'high']).optional(),
  sort: z.enum(['-createdAt', 'createdAt', '-dueDate', 'dueDate']).default('-createdAt'),
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});
```

> **Gotcha — two layers of validation, two jobs.** Mongoose schema validation is your *last* line of defense (protects the DB). zod at the boundary is your *first* — it rejects garbage early with friendly messages and coerces types (query strings → numbers/dates). You want both; they are not redundant.

---

## X. THE CONTROLLER AND ROUTES

Controllers are thin: read the request, call the service, send the envelope.

```js
// server/src/controllers/task.controller.js
import { asyncHandler } from '../utils/asyncHandler.js';
import { ok } from '../utils/respond.js';
import { taskService } from '../services/task.service.js';

export const taskController = {
  list: asyncHandler(async (req, res) => {
    // req.user is attached by the auth middleware (file 04).
    const { items, meta } = await taskService.list(req.user.id, req.query);
    return ok(res, items, 200, meta);
  }),

  get: asyncHandler(async (req, res) => {
    const task = await taskService.getById(req.user.id, req.params.id);
    return ok(res, task);
  }),

  create: asyncHandler(async (req, res) => {
    const task = await taskService.create(req.user.id, req.body);
    return ok(res, task, 201);              // 201 Created
  }),

  update: asyncHandler(async (req, res) => {
    const task = await taskService.update(req.user.id, req.params.id, req.body);
    return ok(res, task);
  }),

  remove: asyncHandler(async (req, res) => {
    await taskService.remove(req.user.id, req.params.id);
    return ok(res, null, 200);
  }),
};
```

```js
// server/src/routes/task.routes.js
import { Router } from 'express';
import { taskController } from '../controllers/task.controller.js';
import { validate } from '../middleware/validate.js';
import { protect } from '../middleware/auth.js';   // built in file 04
import {
  createTaskSchema, updateTaskSchema, listTaskQuerySchema,
} from '../validators/task.schema.js';

const router = Router();

// EVERY task route requires authentication.
router.use(protect);

router
  .route('/')
  .get(validate(listTaskQuerySchema, 'query'), taskController.list)
  .post(validate(createTaskSchema), taskController.create);

router
  .route('/:id')
  .get(taskController.get)
  .patch(validate(updateTaskSchema), taskController.update)
  .delete(taskController.remove);

export default router;
```

> **Gotcha — middleware order is execution order.** `router.use(protect)` must come *before* the routes it guards. Put `validate(...)` before the controller so invalid requests never reach your logic. Express runs middleware top-to-bottom; order is the program.

---

## XI. THE CENTRAL ERROR HANDLER

One place catches every error — operational (`AppError`), Mongoose validation, duplicate keys, bad ObjectIds — and returns the consistent error envelope.

```js
// server/src/middleware/errorHandler.js
import { env } from '../config/env.js';
import { AppError } from '../utils/AppError.js';

// A 404 for any route that didn't match.
export function notFoundHandler(req, res, next) {
  next(AppError.notFound(`Route not found: ${req.method} ${req.originalUrl}`));
}

// MUST have 4 args (err, req, res, next) for Express to recognize it as an error handler.
export function errorHandler(err, req, res, next) {
  let { statusCode = 500, code = 'INTERNAL', message, details = null } = err;

  // Translate common Mongoose errors into clean client responses.
  if (err.name === 'ValidationError') {          // schema validation failed
    statusCode = 400; code = 'VALIDATION';
    details = Object.fromEntries(
      Object.entries(err.errors).map(([k, v]) => [k, [v.message]])
    );
    message = 'Validation failed';
  } else if (err.name === 'CastError') {          // e.g. malformed ObjectId in :id
    statusCode = 400; code = 'BAD_REQUEST'; message = `Invalid ${err.path}`;
  } else if (err.code === 11000) {                // duplicate unique key (e.g. email)
    statusCode = 409; code = 'CONFLICT';
    const field = Object.keys(err.keyValue)[0];
    message = `${field} already in use`;
  }

  // Log server-side. Unexpected (non-operational) errors get a full stack trace.
  if (!err.isOperational) {
    console.error('💥 UNEXPECTED ERROR:', err);
  }

  // Never leak internals to the client in production.
  if (statusCode === 500 && env.NODE_ENV === 'production') {
    message = 'Something went wrong';
  }

  res.status(statusCode).json({
    error: {
      message,
      code,
      details,
      // Stack only in non-production, for your debugging.
      ...(env.NODE_ENV !== 'production' && { stack: err.stack }),
    },
  });
}
```

> **Gotcha — Express identifies error handlers by arity.** An error-handling middleware **must** declare all four parameters `(err, req, res, next)`, even if you don't use `next`. Drop the fourth and Express treats it as a normal middleware and your errors sail past it.

---

## XII. ASSEMBLING THE APP AND CORS

```js
// server/src/app.js
import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import { env } from './config/env.js';
import taskRoutes from './routes/task.routes.js';
import authRoutes from './routes/auth.routes.js';     // file 04
import { notFoundHandler, errorHandler } from './middleware/errorHandler.js';

export function createApp() {
  const app = express();

  // --- global middleware (order matters) ---
  app.use(cors({
    origin: env.CLIENT_ORIGIN,   // ONLY allow our React app's origin
    credentials: true,           // allow cookies (needed for auth in file 04)
  }));
  app.use(express.json());            // parse JSON request bodies
  app.use(express.urlencoded({ extended: true }));
  app.use(cookieParser());            // parse cookies into req.cookies

  // --- health check (from file 01) ---
  app.get('/api/health', (req, res) =>
    res.json({ data: { status: 'ok', time: new Date().toISOString() } })
  );

  // --- feature routes ---
  app.use('/api/auth', authRoutes);
  app.use('/api/tasks', taskRoutes);

  // --- error handling (LAST) ---
  app.use(notFoundHandler);   // anything unmatched → 404
  app.use(errorHandler);      // the single error funnel

  return app;
}
```

```js
// server/src/server.js  — the entry point
import { createApp } from './app.js';
import { connectDB, disconnectDB } from './config/db.js';
import { env } from './config/env.js';

async function start() {
  await connectDB();                 // 1. DB first — fail fast if unreachable
  const app = createApp();           // 2. build the Express app
  const server = app.listen(env.PORT, () =>
    console.log(`🚀 API on http://localhost:${env.PORT}`)
  );

  // graceful shutdown on Ctrl-C / platform stop signal
  const shutdown = async () => {
    server.close(async () => { await disconnectDB(); process.exit(0); });
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

start();
```

> **Gotcha — `credentials: true` requires a specific origin.** CORS does **not** allow `origin: '*'` together with `credentials: true` — the browser will block cookie-bearing requests. You must name the exact client origin (`http://localhost:5173` in dev; your deployed domain in prod). We revisit cross-origin cookies for production in file 06.

> **Why separate `app.js` from `server.js`?** `createApp()` returns an Express app *without* starting a listener or opening the real DB. That makes it trivial to import in tests and drive with Supertest against an in-memory database (file 06). Mixing `app.listen()` into the same module would force tests to bind a real port.

---

## XIII. TRYING IT OUT (BEFORE THE FRONTEND EXISTS)

You can exercise the whole API with `curl` (auth is added in file 04, so for now imagine a valid token). The shapes you see here are exactly what React will consume in file 03.

```bash
# create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Write file 02","priority":"high"}'
# → 201
# {"data":{"_id":"66..","title":"Write file 02","status":"todo","priority":"high",...}}

# list with filtering + pagination
curl "http://localhost:5000/api/tasks?status=todo&sort=-createdAt&page=1&limit=10" \
  -H "Authorization: Bearer <token>"
# → 200
# {"data":[...],"meta":{"page":1,"limit":10,"total":1,"pages":1}}

# validation error shape (empty title)
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" -H "Authorization: Bearer <token>" \
  -d '{"title":""}'
# → 400
# {"error":{"message":"Validation failed","code":"BAD_REQUEST","details":{"title":["Title is required"]}}}
```

---

## XIV. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `async` handler without `asyncHandler` | Request hangs on error; central handler skipped | Wrap every async handler |
| `findOneAndUpdate` without `runValidators` | Invalid data slips past schema | Pass `{ runValidators: true, new: true }` |
| Query not scoped to `owner` | Users read/edit each other's data (IDOR) | Filter by `owner` in every query |
| Error handler with 3 params | Errors bypass it | Declare all four `(err, req, res, next)` |
| CORS `origin:'*'` + `credentials:true` | Browser blocks authed requests | Name the exact client origin |
| Reading `process.env` everywhere | Late, confusing failures | Centralize + validate in `config/env.js` |
| Treating `PORT` as a number | `"5000"` string bugs | `z.coerce.number()` |
| Returning `passwordHash` | Leaked credentials | `select:false` + `toJSON` transform |
| Fat controllers | Logic can't be reused/tested | Push logic into services |
| Trusting `ref` for integrity | Orphaned references | Enforce relationships in code |

---

## 🧠 KEY TAKEAWAYS

- Build the backend in **layers** — `routes → controllers → services → models` — so each piece has one job and is independently testable.
- **Validate the environment once at boot** with dotenv + zod and fail fast; read config only through the validated `env` object.
- Connect to MongoDB with **lifecycle events**, a fast `serverSelectionTimeoutMS`, and **graceful shutdown**.
- Mongoose models carry **validation, refs, timestamps, and `toJSON` transforms**; remember `ref` does not enforce integrity and updates need `runValidators`.
- Validate requests at the boundary with **zod**, then let Mongoose schema validation be the last line of defense — two layers, two jobs.
- Funnel all errors through **one central handler** with a custom `AppError`, an `asyncHandler` wrapper, and a consistent **`{ data }` / `{ error }` envelope**.
- **Scope every query to the owner** to prevent IDOR, and configure **CORS** with a specific origin + `credentials:true` for the React client.

---

**Prev:** [`01-The-MERN-Architecture.md`](./01-The-MERN-Architecture.md) · **Next:** [`03-Building-The-React-Frontend.md`](./03-Building-The-React-Frontend.md) · **Index:** [`00-Index.md`](./00-Index.md)
