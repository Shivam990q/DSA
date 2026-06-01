# 🟢 06 — Middleware & Error Handling

> *"In Express, the bug is almost never in your route. It's in the order of your middleware, the error you forgot to await, or the rejection that fell through the floor."*

**Prev:** [`05-Building-REST-APIs.md`](./05-Building-REST-APIs.md) · **Next:** [`07-Authentication-And-Security.md`](./07-Authentication-And-Security.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. MIDDLEWARE — A DEEPER LOOK

Recap: a middleware is a function `(req, res, next)`. The framework calls them **in registration order**, each gets a chance to do something with the request, and the first one to write a response stops the chain.

```js
function mw(req, res, next) {
  // before downstream (do stuff with req)
  next();
  // after downstream (rare in Express — most "after" work uses res events)
}
```

### The five flavors of middleware

| Flavor | Mounted with | Example |
|--------|--------------|---------|
| **Application-level** | `app.use(...)` | Logger, body parser |
| **Router-level** | `router.use(...)` | Auth on a feature router |
| **Route-level** | `app.get(path, mw, handler)` | Per-endpoint validation |
| **Built-in** | `express.json()`, `express.static()` | Plumbing |
| **Error-handling** | `app.use((err, req, res, next) => {})` (4 args!) | Central error handler |

---

## II. CUSTOM MIDDLEWARE — FACTORY PATTERN

A middleware that takes options is just a function that returns a function:

```js
// middleware/requireRole.js
export const requireRole = (...allowed) => (req, res, next) => {
  if (!req.user) return next({ status: 401, message: "Auth required" });
  if (!allowed.includes(req.user.role)) {
    return next({ status: 403, message: "Forbidden" });
  }
  next();
};

// usage
router.delete("/:id", requireRole("admin", "owner"), ctrl.remove);
```

A few useful, real custom middleware:

### Request ID — propagate a correlation ID through logs

```js
import { randomUUID } from "node:crypto";

export const requestId = (req, res, next) => {
  const id = req.headers["x-request-id"] ?? randomUUID();
  req.id = id;
  res.setHeader("X-Request-Id", id);
  next();
};
```

### Response timing

```js
export const responseTime = (req, res, next) => {
  const t0 = process.hrtime.bigint();
  res.on("finish", () => {
    const ms = Number(process.hrtime.bigint() - t0) / 1e6;
    res.setHeader("X-Response-Time-Ms", ms.toFixed(1)); // already sent — only useful in logs
    req.log?.info({ ms, status: res.statusCode }, "response");
  });
  next();
};
```

### Per-route timeout

```js
export const timeout = (ms) => (req, res, next) => {
  const t = setTimeout(() => {
    if (!res.headersSent) res.status(503).json({ error: "Timeout" });
  }, ms);
  res.on("finish", () => clearTimeout(t));
  res.on("close",  () => clearTimeout(t));
  next();
};

app.use("/api/heavy", timeout(10_000));
```

### Async middleware wrapper

```js
// utils/asyncHandler.js — turns async fns into Express-friendly middleware
export const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
```

---

## III. THE ORDER YOU REGISTER THINGS — A REFERENCE

This is the order that works in nearly every Express app:

```
1.  trust proxy / x-powered-by:false       (settings)
2.  request ID                              (req.id, X-Request-Id)
3.  HTTP logger                             (morgan / pino-http)
4.  helmet                                  (security headers)
5.  CORS                                    (browser-side)
6.  cookie-parser                           (req.cookies)
7.  body parsers (json, urlencoded)         (req.body)
8.  rate limiter                            (file 07)
9.  authentication                          (req.user)  — file 07
10. routes / routers
11. 404 catch-all
12. centralized error handler  (4-arg!)
```

> **Rule of thumb:** if a middleware needs `req.user`, register auth before it. If a middleware sets a header, register it before any route that responds.

---

## IV. ASYNC ERROR HANDLING — THE BIGGEST GOTCHA IN EXPRESS

In Express **4**, throwing inside an `async` handler does **not** trip the error pipeline. The promise rejects silently and the request hangs:

```js
// EXPRESS 4 — this hangs the request
app.get("/danger", async (req, res) => {
  throw new Error("oops");
});
```

Fixes (pick one per project):

### Fix A — wrap every async handler

```js
const asyncHandler = (fn) => (req, res, next) => Promise.resolve(fn(req, res, next)).catch(next);

app.get("/danger", asyncHandler(async (req, res) => {
  throw new Error("oops");                    // → next(err) → error handler
}));
```

### Fix B — `express-async-errors` (one-line monkeypatch)

```js
import "express-async-errors";    // must be imported BEFORE you define routes
import express from "express";
const app = express();
app.get("/danger", async (req, res) => { throw new Error("oops"); });
```

### Fix C — upgrade to **Express 5**

Express 5 catches rejections from async handlers natively. If you're on 5, throw freely.

> **Common bug:** mixing the two — using `express-async-errors` *and* manual `try/catch` everywhere gives you swallowed errors. Pick one.

---

## V. THE 4-ARGUMENT ERROR HANDLER

Express identifies error-handling middleware by **arity**: a function with **exactly four parameters**.

```js
app.use((err, req, res, next) => {
  // ...
});
```

If you write `(err, req, res)` (three args) Express thinks it's a normal middleware and **never calls it on errors**. Yes, this trips everyone.

A solid central error handler:

```js
// middleware/error.js
import { ZodError } from "zod";
import { Prisma } from "@prisma/client";       // optional examples

export function errorHandler(err, req, res, _next) {
  // 1) Map well-known errors to clean responses
  if (err instanceof ZodError) {
    return res.status(422).json({
      error: { code: "VALIDATION_ERROR", message: "Invalid input", details: err.flatten() }
    });
  }
  if (err instanceof Prisma?.PrismaClientKnownRequestError) {
    if (err.code === "P2002")  // unique constraint
      return res.status(409).json({ error: { code: "CONFLICT", message: "Already exists" } });
    if (err.code === "P2025")  // record not found
      return res.status(404).json({ error: { code: "NOT_FOUND", message: "Not Found" } });
  }
  if (err.type === "entity.parse.failed")            // bad JSON body
    return res.status(400).json({ error: { code: "BAD_JSON", message: "Invalid JSON" } });
  if (err.type === "entity.too.large")
    return res.status(413).json({ error: { code: "PAYLOAD_TOO_LARGE", message: "Body too big" } });

  // 2) Use status/code from a thrown AppError
  const status = Number.isInteger(err.status) ? err.status : 500;
  const code   = err.code   ?? (status === 500 ? "INTERNAL" : "ERROR");
  const message = status === 500 && process.env.NODE_ENV === "production"
    ? "Internal error"
    : err.message ?? "Unknown error";

  // 3) Log with request context, never log secrets
  req.log?.error({ err, status, requestId: req.id }, "request failed");
  if (status >= 500) console.error(err);                  // also goes to stderr/PM logs

  // 4) Respond
  res.status(status).json({
    error: { code, message, requestId: req.id }
  });
}
```

```js
// errors/AppError.js
export class AppError extends Error {
  constructor(message, status = 500, code = "INTERNAL") {
    super(message);
    this.status = status;
    this.code = code;
  }
}
```

```js
// app.js — wiring
import { errorHandler } from "./middleware/error.js";
app.use(errorHandler);    // MUST be the LAST app.use(...)
```

---

## VI. 404 CATCH-ALL — AFTER ROUTES, BEFORE THE ERROR HANDLER

```js
// after all routes, before the error handler
app.use((req, res, next) => {
  res.status(404).json({
    error: { code: "NOT_FOUND", message: `Cannot ${req.method} ${req.originalUrl}` }
  });
});
```

If you'd rather route 404s through the error pipeline (so logging is consistent):

```js
import { AppError } from "./errors/AppError.js";
app.use((req, _res, next) => next(new AppError("Not Found", 404, "NOT_FOUND")));
app.use(errorHandler);
```

> **Order matters:** 404 must come *after* all real routes. Otherwise it eats every request.

---

## VII. THROWING vs `next(err)`

Inside a synchronous handler, `throw` is fine — Express catches it.

```js
app.get("/sync", (req, res) => {
  if (!req.query.id) throw Object.assign(new Error("id required"), { status: 400 });
  res.send("ok");
});
```

Inside an async handler:
- with `express-async-errors` or Express 5: `throw` works.
- otherwise: `throw` rejects the promise — wrap with `asyncHandler` so it forwards to `next(err)`.

```js
// hand-rolled, no wrapper
app.get("/legacy", async (req, res, next) => {
  try {
    const data = await loadData();
    res.json(data);
  } catch (err) {
    next(err);              // forward to error handler
  }
});
```

---

## VIII. LOGGING — MORGAN, PINO, WINSTON

Logging answers two questions:

1. **HTTP-level**: what requests came in, with what status and timing?
2. **App-level**: what did the code do, and what went wrong?

### `morgan` — concise HTTP request logs

```bash
npm install morgan
```

```js
import morgan from "morgan";
app.use(morgan("dev"));            // human-friendly in dev
app.use(morgan("combined"));        // Apache combined log format in prod

// custom format with request id
morgan.token("rid", (req) => req.id);
app.use(morgan(":rid :method :url :status :res[content-length] - :response-time ms"));
```

### `pino` — fast structured JSON logs (recommended for prod)

```bash
npm install pino pino-http
npm install --save-dev pino-pretty   # human-readable dev formatter
```

```js
// lib/logger.js
import pino from "pino";
export const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  // Pretty in dev, JSON in prod
  transport: process.env.NODE_ENV !== "production"
    ? { target: "pino-pretty", options: { colorize: true } }
    : undefined,
  redact: ["req.headers.authorization", "*.password"]
});
```

```js
// app.js
import pinoHttp from "pino-http";
import { logger } from "./lib/logger.js";

app.use(pinoHttp({ logger, customProps: (req) => ({ requestId: req.id }) }));

app.get("/health", (req, res) => {
  req.log.info({ uptime: process.uptime() }, "health check");
  res.json({ ok: true });
});
```

### `winston` — flexible, transports galore

```bash
npm install winston
```

```js
import winston from "winston";

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL ?? "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: "error.log", level: "error" })
  ]
});
```

### Which to pick?

| Library | Best for |
|---------|----------|
| `morgan` | Pure HTTP request logs (combine with another for app logs) |
| `pino` + `pino-http` | High-performance production logging — JSON, fast, built for Node |
| `winston` | Flexibility (multiple transports — file/Cloud/Slack), older codebases |

Most modern services pick **pino**.

> **Logging discipline:**
> - **Levels:** `error`, `warn`, `info`, `debug`, `trace`. Most logs are `info`.
> - **Structured:** log objects, not strings. JSON is your friend in prod.
> - **Don't log secrets:** redact `Authorization`, passwords, tokens, PII.
> - **Correlation:** include `requestId` everywhere — searchable across services.
> - **Don't `console.log` in production hot paths** — pino is dramatically faster.

---

## IX. REQUEST CONTEXT — `AsyncLocalStorage`

To attach data (request id, current user) to every log without passing it down through every function:

```js
import { AsyncLocalStorage } from "node:async_hooks";
export const als = new AsyncLocalStorage();

// middleware
app.use((req, res, next) => {
  als.run({ requestId: req.id, userId: req.user?.id }, next);
});

// anywhere deep in your code
import { als } from "./lib/context.js";
const ctx = als.getStore();
console.log(ctx?.requestId, ctx?.userId);
```

This is how libraries like OpenTelemetry weave context through async calls without you wiring it explicitly.

---

## X. THE FULL REQUEST LIFECYCLE — ANNOTATED

```
[1] TCP connection / TLS handshake
[2] HTTP message parsed by Node:                IncomingMessage (req), ServerResponse (res)
[3] Express runs middleware in order:
       trust-proxy → x-request-id → morgan → helmet → cors →
       cookie-parser → body parsers → rate-limit → auth → routers
[4] Route handler executes (sync or async):
       - validates input (zod)
       - calls service
       - service calls repository (DB)
       - controller writes response
[5] If a middleware/handler calls next(err) or throws:
       Express SKIPS remaining normal middleware
       and jumps to the FIRST 4-arg error handler
[6] Error handler:
       maps known errors → clean responses
       logs with request id + stack
[7] res.end() → 'finish' event fires:
       morgan/pino-http log final status + duration
       cleanup hooks run (timeout clearTimeout, etc.)
[8] Connection kept-alive or closed
```

If you can narrate this for any Express app, you can debug any bug.

---

## XI. UNCAUGHT EXCEPTIONS & UNHANDLED REJECTIONS

Process-wide safety nets:

```js
process.on("uncaughtException", (err) => {
  logger.fatal({ err }, "uncaughtException");
  // Do not "recover" — process state is now suspect.
  process.exit(1);
});

process.on("unhandledRejection", (reason) => {
  logger.error({ reason }, "unhandledRejection");
  // Optional: exit. Many teams crash here too in production.
});
```

> **Rule:** these handlers exist to **log and exit**, not to keep the app running. The supervisor (pm2, systemd, Kubernetes) restarts the process on crash. That's the contract.

---

## XII. REQUEST VALIDATION ERRORS — A FULL FLOW

A clean shape from validation to response:

```js
// schemas/auth.schema.js
import { z } from "zod";
export const loginSchema = z.object({
  email:    z.string().email(),
  password: z.string().min(8)
});

// middleware/validate.js
export const validateBody = (schema) => (req, res, next) => {
  const result = schema.safeParse(req.body);
  if (!result.success) {
    return next(Object.assign(new Error("Validation failed"), {
      status: 422,
      code: "VALIDATION_ERROR",
      details: result.error.flatten()
    }));
  }
  req.body = result.data;     // typed, sanitized
  next();
};

// route
router.post("/login", validateBody(loginSchema), authCtrl.login);
```

```jsonc
// 422 response from the central error handler
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": {
      "fieldErrors": { "password": ["String must contain at least 8 character(s)"] },
      "formErrors":  []
    },
    "requestId": "0a8b...4f"
  }
}
```

Every error in your app — validation, auth, DB, business — funnels through one handler with one shape. Clients can rely on it.

---

## XIII. WORKED EXAMPLE — MIDDLEWARE STACK FOR A REAL API

```js
// app.js
import express from "express";
import "express-async-errors";
import helmet from "helmet";
import cors from "cors";
import morgan from "morgan";
import compression from "compression";
import cookieParser from "cookie-parser";
import { rateLimit } from "express-rate-limit";
import pinoHttp from "pino-http";

import { requestId }    from "./middleware/requestId.js";
import { responseTime } from "./middleware/responseTime.js";
import { logger }       from "./lib/logger.js";
import { errorHandler } from "./middleware/error.js";

import authRoutes from "./routes/auth.routes.js";
import todoRoutes from "./routes/todo.routes.js";

const app = express();

// ---- 0. App settings ----
app.disable("x-powered-by");
app.set("trust proxy", 1);

// ---- 1. Observability (first so EVERYTHING is logged) ----
app.use(requestId);
app.use(pinoHttp({ logger, customProps: (req) => ({ requestId: req.id }) }));
app.use(responseTime);

// ---- 2. Security ----
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN ?? "https://app.example.com", credentials: true }));
app.use(rateLimit({ windowMs: 60_000, max: 120, standardHeaders: true, legacyHeaders: false }));

// ---- 3. Body / cookies ----
app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: true, limit: "1mb" }));
app.use(cookieParser(process.env.COOKIE_SECRET));
app.use(compression());

// ---- 4. Routes ----
app.get("/health",   (req, res) => res.json({ ok: true }));
app.get("/healthz",  (req, res) => res.json({ ok: true })); // K8s liveness
app.get("/readyz",   (req, res) => res.json({ ok: true })); // K8s readiness — wire to DB later

app.use("/api/v1/auth",  authRoutes);
app.use("/api/v1/todos", todoRoutes);

// ---- 5. 404 ----
app.use((req, _res, next) => {
  next(Object.assign(new Error("Not Found"), { status: 404, code: "NOT_FOUND" }));
});

// ---- 6. Centralized error handler — LAST ----
app.use(errorHandler);

export default app;
```

Read this and you have the playbook for every Express app you'll ship.

---

## XIV. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Error handler with 3 args | Errors leak as 500 with empty body | Must be `(err, req, res, next)` (4 args) |
| Async handler that throws (Express 4) | Request hangs forever | `asyncHandler` wrapper or `express-async-errors` |
| Mixed `try/catch` and `express-async-errors` | Swallowed or duplicated errors | Pick one strategy |
| 404 handler placed before routes | Every request 404s | Place after all routes |
| Logger registered after routes | Some requests aren't logged | Register first |
| Body parser registered after routes | `req.body` is undefined | Parser first |
| Auth registered after the protected route | Endpoints public | Auth before routes |
| Logging secrets / tokens | Leak in logs | `redact` config |
| Returning stack traces in prod | Info disclosure | Hide stacks behind `NODE_ENV !== "production"` |
| Using `console.log` for high-throughput logs | Slow + unstructured | Use pino |
| Missing `next()` in middleware | Request hangs | Either respond or `next()` |
| Calling `next()` after responding | "Cannot set headers after sent" | Only one of: respond OR `next()` |
| Forgetting to clear timeouts on error | Memory leak | Use `res.on("close")` to clear |
| Throwing non-Error objects | Stack traces lost | Always throw `Error` instances |
| Catching `uncaughtException` to keep running | Memory + state corruption | Log and exit; let supervisor restart |

---

## 🧠 KEY TAKEAWAYS

- Middleware order is the framework. Nail it: **observability → security → parsers → auth → routes → 404 → error handler.**
- The error handler **must have 4 parameters**. If it has 3, it's silently a normal middleware.
- Async errors don't propagate in Express 4; use `asyncHandler` or `express-async-errors`. Express 5 fixes this natively.
- Centralize error mapping (Zod → 422, Prisma → 404/409, AppError → status). Clients rely on a stable error shape.
- Use **pino** for structured production logs; redact secrets; thread a **request ID** through everything.
- `process.on("uncaughtException")` is for logging and exit, not for control flow. Let the supervisor restart you.

---

**Prev:** [`05-Building-REST-APIs.md`](./05-Building-REST-APIs.md) · **Next:** [`07-Authentication-And-Security.md`](./07-Authentication-And-Security.md) · **Index:** [`00-Index.md`](./00-Index.md)
