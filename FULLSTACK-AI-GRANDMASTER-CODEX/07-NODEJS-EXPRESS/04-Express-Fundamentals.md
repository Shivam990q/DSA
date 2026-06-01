# 🟢 04 — Express Fundamentals

> *"Express is a stack of functions, called in order, each free to talk to a request, write to a response, or pass the baton. The whole framework is the next() call. Master that and you can read any Node backend."*

**Prev:** [`03-Core-Modules-And-Async.md`](./03-Core-Modules-And-Async.md) · **Next:** [`05-Building-REST-APIs.md`](./05-Building-REST-APIs.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT EXPRESS IS — AND ISN'T

**Express** is a thin web framework on top of Node's `http` module. It gives you:

- **Routing** — match incoming requests to handler functions by method + path.
- **Middleware** — a pipeline of functions that runs before (or after) a handler.
- A nicer **`req` / `res` API** — `res.json()`, `req.params`, `req.query`, etc.
- A pluggable ecosystem (helmet, cors, morgan, multer...).

What it is **not**:

- A "batteries-included" framework like Spring Boot or Django. There is no built-in ORM, no built-in validation, no built-in auth, no opinions about folders.
- An async-by-default framework. Express **predates** `async/await`; some patterns (especially error handling) need explicit care, which we cover in file 06.

> **The mental model:** Express is a list of functions. A request walks the list. Any function can write the response or call `next()` to pass to the next function. That's it.

```
req ─► [logger] ─► [json parser] ─► [auth] ─► [route handler] ─► res
                                                    │
                                                    ▼ (on error)
                                              [error handler]
```

Express 5 is GA at the time of writing; the API in this file works on Express 4 and 5 except where noted.

---

## II. INSTALL & A 6-LINE SERVER

```bash
mkdir hello-express && cd hello-express
npm init -y
npm install express
```

```js
// index.js   (ESM — package.json has "type": "module")
import express from "express";          // pull in the framework

const app = express();                  // create an application

app.get("/", (req, res) => {            // GET / — match
  res.send("Hello, Express!");          // write a response
});

app.listen(3000, () => console.log("http://localhost:3000"));
```

```bash
node --watch index.js                   # auto-restart on file change (Node 20+)
```

That's a working web server. Hit `http://localhost:3000` in a browser.

---

## III. THE APP, THE ROUTES, AND `req` / `res`

```js
import express from "express";
const app = express();

// HTTP verbs map to methods on the app
app.get   ("/users",        (req, res) => res.json([]));
app.post  ("/users",        (req, res) => res.status(201).json({ id: 1 }));
app.put   ("/users/:id",    (req, res) => res.json({}));
app.patch ("/users/:id",    (req, res) => res.json({}));
app.delete("/users/:id",    (req, res) => res.status(204).end());

// Match ALL methods
app.all("/diagnostic", (req, res) => res.send("any method works here"));

app.listen(3000);
```

### Route parameters and query strings

```js
// /users/42/posts/9
app.get("/users/:userId/posts/:postId", (req, res) => {
  const { userId, postId } = req.params;       // strings
  res.json({ userId, postId });
});

// /search?q=node&page=2&tag=ts&tag=express   <-- repeated keys become arrays
app.get("/search", (req, res) => {
  const { q, page = "1", tag } = req.query;     // 'tag' is string OR string[]
  res.json({ q, page: Number(page), tag });
});

// Optional segment (Express 4 syntax):  /posts/:slug?
app.get("/posts/:slug?", (req, res) => res.json({ slug: req.params.slug ?? null }));

// Regex / wildcard
app.get(/\/admin\/.*/, (req, res) => res.send("admin area"));
```

### The `req` object — what you'll actually use

| Property / method | Meaning |
|-------------------|---------|
| `req.method`, `req.url`, `req.path` | Verb, URL, just the path part |
| `req.params` | Route params (`:id`) |
| `req.query` | Query string parsed into an object |
| `req.body` | Parsed body (only after a body parser middleware) |
| `req.headers` | Lowercased header object |
| `req.get('content-type')` / `req.is('json')` | Header lookup, content-type check |
| `req.ip`, `req.ips` | Client IP (when `trust proxy` is set) |
| `req.cookies` / `req.signedCookies` | After `cookie-parser` |
| `req.protocol`, `req.secure`, `req.hostname` | Connection info |
| `req.originalUrl` | URL before any router strip |

### The `res` object — every response shortcut

```js
res.status(201).json({ id: 1 });               // status + JSON body
res.status(204).end();                          // no content
res.sendStatus(404);                            // status + default text
res.set("X-Custom", "yes").send("ok");          // header + body
res.type("html").send("<p>hi</p>");             // sets content-type
res.redirect(302, "/login");
res.cookie("session", "abc", { httpOnly: true, secure: true });
res.download("/abs/path/to/file.pdf");          // sends with Content-Disposition
res.sendFile("/abs/path/to/asset.png");
res.location("/users/1");                       // sets Location header (handy for 201)
res.append("Set-Cookie", "tracker=1");          // additive
```

> **Gotcha — once you respond, you're done.** Calling `res.send` or `res.json` twice throws `Error [ERR_HTTP_HEADERS_SENT]`. Either return after sending, or check `res.headersSent`.

---

## IV. MIDDLEWARE — THE WHOLE FRAMEWORK IN ONE CONCEPT

A **middleware** is a function with this signature:

```js
function middleware(req, res, next) {
  // do something with req / res
  next();                  // pass control to the next middleware
  // or:
  // next(err);            // skip to error-handling middleware (file 06)
  // or:
  // res.send(...);        // end the chain right here
}
```

You register them with `app.use(...)`:

```js
import express from "express";
const app = express();

app.use((req, res, next) => {
  console.log(`${req.method} ${req.url} @ ${new Date().toISOString()}`);
  next();
});

app.use(express.json());                    // parses JSON bodies into req.body

app.use((req, res, next) => {
  req.startedAt = Date.now();               // attach data for downstream
  next();
});

app.get("/", (req, res) => {
  res.json({ hello: "world", elapsed: Date.now() - req.startedAt });
});

app.listen(3000);
```

### The two laws of middleware

1. **Order matters.** Middleware runs in the order it was registered. Auth must come *before* the route it protects.
2. **You must either respond or call `next()`.** Forgetting both leaves the request hanging until the client times out.

```js
app.use((req, res, next) => {
  if (!req.headers.authorization) {
    return res.status(401).json({ error: "missing auth" });   // RESPOND
  }
  next();                                                      // OR continue
});
```

### Mounting middleware on a path

```js
app.use(loggingMiddleware);                  // every request
app.use("/api", apiOnlyMiddleware);          // only paths starting with /api
app.use(["/admin", "/staff"], onlyStaffMw);  // multiple mount paths
```

### Chained route-level middleware

```js
app.get("/private", requireAuth, requireAdmin, (req, res) => {
  res.json({ secret: 42 });
});

// Or as an array
app.get("/private", [requireAuth, requireAdmin], handler);
```

### Built-in middleware

| Middleware | What it does |
|------------|--------------|
| `express.json([options])` | Parse JSON bodies into `req.body` |
| `express.urlencoded({ extended: true })` | Parse form bodies (`application/x-www-form-urlencoded`) |
| `express.static(rootDir)` | Serve static files |
| `express.text()` / `express.raw()` | Plain-text or `Buffer` bodies |
| `express.Router()` | Modular route group (see below) |

### Common third-party middleware

| Package | Purpose |
|---------|---------|
| `cors` | CORS headers (cross-origin) |
| `helmet` | Security headers (file 07) |
| `morgan` | HTTP request logging (file 06) |
| `cookie-parser` | Parse cookies into `req.cookies` |
| `compression` | gzip responses |
| `multer` | `multipart/form-data` & file uploads (file 07) |
| `express-rate-limit` | Basic rate limiting (file 07) |
| `express-session` | Session store (file 07) |

```js
import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import compression from "compression";

const app = express();
app.use(helmet());                       // security defaults
app.use(cors({ origin: "https://app.example.com", credentials: true }));
app.use(compression());                  // gzip
app.use(express.json({ limit: "1mb" })); // bound the body size!
app.use(morgan("dev"));                  // HTTP request log
```

> **Gotcha — body size.** `express.json()` defaults to `100kb`. If you accept larger bodies (file metadata, image uploads), set `{ limit: "1mb" }` (or use streams via `multer` for files). Otherwise you get `PayloadTooLargeError`.

---

## V. STATIC FILES

```js
app.use(express.static("public"));                                // serve from /public on URL /
app.use("/assets", express.static("public", { maxAge: "1d" }));   // mount under /assets, cache headers

// Common production setup:
app.use(express.static("public", {
  immutable: true,
  maxAge: "1y",
  fallthrough: true   // if not found, call next() to keep walking the stack
}));
```

For SPAs (single-page apps), serve `index.html` for any non-API path:

```js
import path from "node:path";
const PUBLIC = path.resolve("public");

app.use(express.static(PUBLIC));
app.get(/^\/(?!api).*/, (req, res) => res.sendFile(path.join(PUBLIC, "index.html")));
```

---

## VI. `express.Router` — MODULAR ROUTES

Putting every route on `app` is fine for tiny apps. For real ones, split by resource using `Router`:

```js
// routes/users.js
import { Router } from "express";
const router = Router();

router.get   ("/",      listUsers);
router.post  ("/",      createUser);
router.get   ("/:id",   getUser);
router.put   ("/:id",   updateUser);
router.delete("/:id",   deleteUser);

export default router;
```

```js
// app.js
import express from "express";
import users from "./routes/users.js";
import posts from "./routes/posts.js";

const app = express();
app.use(express.json());
app.use("/api/v1/users", users);              // mount path is prepended
app.use("/api/v1/posts", posts);
app.listen(3000);
```

### Router-level middleware

```js
router.use(requireAuth);                      // applies to every route in THIS router
router.param("id", (req, res, next, id) => {  // runs whenever ":id" is captured
  if (!/^\d+$/.test(id)) return res.status(400).json({ error: "bad id" });
  req.userId = Number(id);
  next();
});
```

### Chain handlers with `route()`

```js
router.route("/:id")
  .get(getUser)
  .put(updateUser)
  .delete(deleteUser);
```

### Mergeable routers

```js
// routes/posts.js — needs access to :userId from a parent router
const router = Router({ mergeParams: true });
router.get("/:postId", (req, res) => res.json(req.params));     // userId AND postId

// app.js
app.use("/users/:userId/posts", router);
```

---

## VII. PATH MATCHING — PATH-TO-REGEXP

Express uses [`path-to-regexp`](https://github.com/pillarjs/path-to-regexp) for paths. A few shapes you'll meet:

```js
app.get("/users/:id", h);                  // single param
app.get("/users/:id(\\d+)", h);            // typed param (numbers only) — Express 4
app.get("/files/:path*", h);               // greedy — captures everything after /files/
app.get("/api/:resource(.*)", h);          // catch-all
app.get("/(api|admin)/data", h);           // alternation
app.get(/^\/legacy\/.*\.html$/, h);        // raw regex
```

> **Heads-up — Express 5 changed path-to-regexp version.** Some patterns (like `*` and `(...)?`) behave differently. If you migrate, run your test suite. The simple `:id` and `/x/:y` cases work the same.

---

## VIII. APP SETTINGS THAT MATTER

```js
app.set("env", "production");                  // (auto-derived from NODE_ENV)
app.set("trust proxy", 1);                     // behind a single proxy/load balancer
app.set("x-powered-by", false);                // remove the "X-Powered-By: Express" header
app.disable("x-powered-by");                   // same as above
app.set("query parser", "extended");           // 'simple' | 'extended' | function | false
app.set("etag", "strong");                     // ETag generation
app.set("json spaces", 2);                     // pretty-print JSON in dev
```

> **Production checklist:**
> - `NODE_ENV=production` (not "production " with a space — yes that's a real bug)
> - `app.disable("x-powered-by")` to avoid leaking framework info
> - `app.set("trust proxy", 1)` if you're behind one — otherwise `req.ip` is wrong

---

## IX. TEMPLATE ENGINES (POINTER)

Express can render server-side HTML templates via view engines. Common ones: **EJS**, **Pug**, **Handlebars**.

```bash
npm install ejs
```

```js
import path from "node:path";
app.set("view engine", "ejs");
app.set("views", path.resolve("views"));

app.get("/hello/:name", (req, res) => {
  res.render("hello", { name: req.params.name });   // renders views/hello.ejs
});
```

```ejs
<!-- views/hello.ejs -->
<!doctype html>
<html><body><h1>Hello, <%= name %>!</h1></body></html>
```

In modern stacks, frontends usually live in **React/Next.js** (sections 05/06), and Express is a JSON API. Use views when you actually want server-rendered HTML — internal tools, transactional emails, simple pages.

---

## X. REQUEST LIFECYCLE — THE WHOLE PIPELINE

```
1. TCP connection accepted by Node's http server
2. HTTP message parsed → IncomingMessage (req) + ServerResponse (res)
3. Express router matches: app-level middleware first, then mounted routers, then route handlers
4. Each middleware can:
      - read/modify req
      - send a response (terminates the chain)
      - call next()        → next middleware
      - call next(err)     → jumps to ERROR-handling middleware (4 args)
5. After the response is sent:
      - 'finish' event on res
      - Logger middleware records duration
      - Connection kept alive or closed
```

A worked example with timing:

```js
app.use((req, res, next) => {
  req.t0 = process.hrtime.bigint();
  res.on("finish", () => {
    const ms = Number(process.hrtime.bigint() - req.t0) / 1e6;
    console.log(`${req.method} ${req.originalUrl} ${res.statusCode} ${ms.toFixed(1)}ms`);
  });
  next();
});
```

---

## XI. ASYNC HANDLERS — A PRELUDE TO FILE 06

Express 4 handlers are sync-by-default. Throw or reject inside one and Express won't catch it:

```js
// BUG (Express 4): unhandled rejection — request hangs
app.get("/users/:id", async (req, res) => {
  const user = await db.user.findUnique({ where: { id: req.params.id } });
  if (!user) throw new Error("Not found");
  res.json(user);
});
```

Two fixes:

```js
// 1) Manually try/catch and forward to next(err)
app.get("/users/:id", async (req, res, next) => {
  try {
    const user = await db.user.findUnique({ where: { id: req.params.id } });
    if (!user) return next(new Error("Not found"));
    res.json(user);
  } catch (err) {
    next(err);
  }
});

// 2) Use a wrapper helper (recommended)
const asyncHandler = fn => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);
app.get("/users/:id", asyncHandler(async (req, res) => {
  const user = await db.user.findUnique({ where: { id: req.params.id } });
  if (!user) throw Object.assign(new Error("Not found"), { status: 404 });
  res.json(user);
}));
```

> **Express 5** auto-catches rejections from async handlers. If you're on 4, use a wrapper or `express-async-errors`. File 06 has the full treatment.

---

## XII. A WORKED EXAMPLE — A TODO API SKELETON

```js
// app.js
import express from "express";
import morgan from "morgan";
import cors from "cors";
import { todos } from "./routes/todos.js";

const app = express();

// Plumbing
app.use(morgan("dev"));
app.use(cors());
app.use(express.json({ limit: "100kb" }));
app.disable("x-powered-by");

// Mount feature routers
app.use("/api/v1/todos", todos);

// 404 catch-all (must come AFTER routes)
app.use((req, res) => res.status(404).json({ error: "Not Found" }));

// Centralized error handler (4 args!)
app.use((err, req, res, _next) => {
  const status = err.status ?? 500;
  res.status(status).json({ error: err.message });
});

app.listen(3000, () => console.log("http://localhost:3000"));
```

```js
// routes/todos.js
import { Router } from "express";
const router = Router();
const store = new Map();
let next = 1;

router.get("/", (req, res) => res.json([...store.values()]));

router.post("/", (req, res) => {
  const { title } = req.body ?? {};
  if (!title || typeof title !== "string") {
    return res.status(400).json({ error: "title is required" });
  }
  const todo = { id: next++, title, done: false };
  store.set(todo.id, todo);
  res.status(201).location(`/api/v1/todos/${todo.id}`).json(todo);
});

router.get("/:id", (req, res) => {
  const t = store.get(Number(req.params.id));
  if (!t) return res.status(404).json({ error: "Not Found" });
  res.json(t);
});

router.put("/:id", (req, res) => {
  const t = store.get(Number(req.params.id));
  if (!t) return res.status(404).json({ error: "Not Found" });
  Object.assign(t, req.body);
  res.json(t);
});

router.delete("/:id", (req, res) => {
  store.delete(Number(req.params.id)) ? res.status(204).end()
                                      : res.status(404).json({ error: "Not Found" });
});

export { router as todos };
```

You now have a fully shaped REST API — file 05 turns this skeleton into a real service with validation, a database, and proper layering.

---

## XIII. EXPRESS vs ALTERNATIVES — A QUICK TOUR

| Framework | One-line take |
|-----------|---------------|
| **Express** | The default. Tiny, flexible, huge ecosystem, no opinions. |
| **Fastify** | Faster than Express, schema-first validation, plugin system, modern defaults. |
| **Koa** | By Express's creator. Generators/async-first. Smaller core, you BYO most things. |
| **Hapi** | Configuration-driven, batteries-included. |
| **NestJS** | Angular-style architecture (decorators, DI). Built on Express or Fastify. |
| **Hono / Elysia** | Edge-runtime first (Cloudflare Workers, Bun, Deno). |

**Why we pick Express here:** the largest set of jobs, libraries, and tutorials still target it. Once you understand Express middleware, every other Node framework reads like a dialect.

---

## XIV. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Forgetting `express.json()` | `req.body` is `undefined` | Mount the parser before routes |
| Sending two responses | `ERR_HTTP_HEADERS_SENT` | `return` after responding |
| Wrong middleware order | Auth bypassed; CORS not on errors | Order: logger → CORS/helmet → parsers → routers → 404 → error handler |
| Async handler throws (Express 4) | Request hangs | Use `asyncHandler` wrapper / Express 5 |
| Body too large | `PayloadTooLargeError` | `express.json({ limit: "1mb" })` |
| Wrong `req.ip` behind a proxy | All requests look like 127.0.0.1 | `app.set("trust proxy", 1)` |
| Catch-all 404 placed before routes | Every request 404s | 404 handler goes **after** routes |
| Error handler with 3 args | Errors leak as 500 with no body | Error handler must be `(err, req, res, next)` — exactly 4 args |
| Mutating `req.params`/`req.query` reuse pitfalls | Stale data across calls | Treat them as read-only |
| `app.use(handler)` for routes | Catches every method, every path | Use `app.get`/`post` etc. |
| Mounting `Router` without `mergeParams` | Parent params missing | `Router({ mergeParams: true })` |
| Not pinning Node version in deploy | Subtle behavior changes | `engines.node` + Docker base tag |

---

## 🧠 KEY TAKEAWAYS

- Express is `http` + a **middleware pipeline** + a friendlier `req`/`res`. The whole framework is `next()`.
- Order is destiny: **logger → security → parsers → routers → 404 → error handler.**
- Use `express.Router` once you have more than a handful of routes; group by resource.
- `req.params`, `req.query`, `req.body` (after a parser), `req.headers` — that's 90% of what you read.
- `res.status().json()` covers most responses; remember `204` for no-content and `Location` for `201`.
- Body parsing has size limits — set them deliberately. Static files belong on `express.static` with proper cache headers.
- Async handlers in Express 4 must be wrapped (`asyncHandler` or `express-async-errors`); Express 5 catches rejections natively.
- `trust proxy`, `disable('x-powered-by')`, and `NODE_ENV=production` are non-negotiable in real deployments.

---

**Prev:** [`03-Core-Modules-And-Async.md`](./03-Core-Modules-And-Async.md) · **Next:** [`05-Building-REST-APIs.md`](./05-Building-REST-APIs.md) · **Index:** [`00-Index.md`](./00-Index.md)
