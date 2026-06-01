# 🟢 Node.js & Express

> *"The browser was JavaScript's prison. Node opened the door, handed JS a server, a file system, and a network socket — and said: build the rest of the world."*

> **Section 07 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module takes you from `console.log("hello")` outside the browser to a production-grade, secured, tested, deployed Express REST API with auth, sockets, caching, and clustering.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- The **Node.js runtime**: V8, libuv, the **event loop**, microtasks, non-blocking I/O, and when Node is (and isn't) the right tool.
- **Modules**: CommonJS vs ESM, `require` vs `import`, module resolution, and **npm / package.json / semver** end to end.
- **Core modules**: `fs`, `path`, `os`, `http`, `events`, `stream`, `buffer`, `crypto`, `util` — and the full async story (callbacks → promises → `async/await`).
- **Express**: routing, middleware, request lifecycle, modular routers, error handling, validation, logging.
- **REST API design** the way senior engineers actually do it: resources, status codes, versioning, pagination, DTOs, controllers/services/repos.
- **Authentication & security**: bcrypt, JWT (access + refresh), sessions, OAuth2 outline, RBAC, helmet, CORS, rate limiting, OWASP top issues.
- **Production-grade Node**: testing (Jest + Supertest), WebSockets (Socket.IO), Redis caching, clustering, worker threads, pm2, Docker, graceful shutdown, health checks.

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file builds on the previous. ⭐ marks the highest-leverage files — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here · roadmap · setup | — |
| 01 | [`01-The-Nodejs-Runtime.md`](./01-The-Nodejs-Runtime.md) | What Node is, V8 + libuv, the event loop, microtasks, non-blocking I/O, single-threaded model, `process` / `global` | ⭐ |
| 02 | [`02-Modules-And-NPM.md`](./02-Modules-And-NPM.md) | CommonJS vs ESM, module resolution, `package.json`, npm/npx, semver, scripts, deps vs devDeps, monorepos, publishing | ⭐ |
| 03 | [`03-Core-Modules-And-Async.md`](./03-Core-Modules-And-Async.md) | `fs`, `path`, `os`, `http`, `events`/EventEmitter, streams (readable/writable/transform/pipe), `Buffer`, callbacks → promises → async/await, `util.promisify` | ⭐ |
| 04 | [`04-Express-Fundamentals.md`](./04-Express-Fundamentals.md) | Express setup, routing, route params/query, `req`/`res`, middleware concept & order, built-in/third-party middleware, static files, `Router`, template engines | ⭐ |
| 05 | [`05-Building-REST-APIs.md`](./05-Building-REST-APIs.md) | REST principles, resource design, status codes, full CRUD, validation (zod / express-validator), pagination/filtering/sorting, versioning, MVC, DTOs, DB integration | ⭐ |
| 06 | [`06-Middleware-And-Error-Handling.md`](./06-Middleware-And-Error-Handling.md) | Middleware deep dive, custom middleware, **error-handling middleware (4-arg)**, async error handling, central error handler, 404, logging (morgan / winston / pino), request lifecycle | ⭐ |
| 07 | [`07-Authentication-And-Security.md`](./07-Authentication-And-Security.md) | bcrypt, JWT (access + refresh), sessions & cookies, OAuth2 overview, RBAC, helmet, CORS, rate limiting, sanitization, OWASP top issues, secrets/env | ⭐ |
| 08 | [`08-Advanced-Node-And-Deployment.md`](./08-Advanced-Node-And-Deployment.md) | Jest + Supertest, Socket.IO, Redis caching, clustering, worker threads, pm2, streams at scale, graceful shutdown, Docker, deployment, health checks, monitoring | ⭐ |

---

## 🗺️ COMPLETE NODE.JS + EXPRESS ROADMAP (coverage checklist)

> Roadmap.sh-style exhaustive checklist. **Reading only this codex covers all of it.** Each topic links to the file where it lives.

### A. Node.js runtime fundamentals
- [x] What is Node.js, history, why it exists → [`01`](./01-The-Nodejs-Runtime.md)
- [x] **V8 engine** (JS → machine code, JIT, hidden classes) → [`01`](./01-The-Nodejs-Runtime.md)
- [x] **libuv** (the C library that powers async I/O) → [`01`](./01-The-Nodejs-Runtime.md)
- [x] **Event loop** — phases (timers, pending, idle/prepare, **poll**, check, close) → [`01`](./01-The-Nodejs-Runtime.md)
- [x] **Microtasks** (`process.nextTick`, Promise jobs) vs macrotasks → [`01`](./01-The-Nodejs-Runtime.md)
- [x] Non-blocking I/O & the single-threaded model → [`01`](./01-The-Nodejs-Runtime.md)
- [x] **Thread pool** (UV_THREADPOOL_SIZE) for fs / crypto / dns / zlib → [`01`](./01-The-Nodejs-Runtime.md), [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] `process`, `global`, `__dirname`, `__filename`, `globalThis` → [`01`](./01-The-Nodejs-Runtime.md)
- [x] CLI: `node`, REPL, `--inspect`, debugging, env vars → [`01`](./01-The-Nodejs-Runtime.md)
- [x] When Node is great vs when it isn't → [`01`](./01-The-Nodejs-Runtime.md)

### B. Modules, npm, ecosystem
- [x] **CommonJS** (`require`, `module.exports`) → [`02`](./02-Modules-And-NPM.md)
- [x] **ES Modules** (`import` / `export`, `"type": "module"`) → [`02`](./02-Modules-And-NPM.md)
- [x] CJS ↔ ESM interop, dual packages, `.cjs` / `.mjs` → [`02`](./02-Modules-And-NPM.md)
- [x] Module resolution algorithm (core, relative, `node_modules`, exports map) → [`02`](./02-Modules-And-NPM.md)
- [x] `package.json` fields (every important one) → [`02`](./02-Modules-And-NPM.md)
- [x] `npm`, `npx`, `npm init`, `install`, `ci`, `update`, `audit` → [`02`](./02-Modules-And-NPM.md)
- [x] **Semver** (`^`, `~`, exact), `package-lock.json` → [`02`](./02-Modules-And-NPM.md)
- [x] `dependencies` vs `devDependencies` vs `peerDependencies` → [`02`](./02-Modules-And-NPM.md)
- [x] npm scripts, lifecycle hooks, `npm run` → [`02`](./02-Modules-And-NPM.md)
- [x] Workspaces / monorepos (npm/pnpm/yarn) → [`02`](./02-Modules-And-NPM.md)
- [x] Publishing a package → [`02`](./02-Modules-And-NPM.md)
- [x] Alternatives: `pnpm`, `yarn`, `bun` → [`02`](./02-Modules-And-NPM.md)

### C. Core modules
- [x] `fs` (sync, async, promises, streams) → [`03`](./03-Core-Modules-And-Async.md)
- [x] `path` (cross-platform paths) → [`03`](./03-Core-Modules-And-Async.md)
- [x] `os` (system info) → [`03`](./03-Core-Modules-And-Async.md)
- [x] `http` / `https` (raw server & client) → [`03`](./03-Core-Modules-And-Async.md)
- [x] `events` / `EventEmitter` → [`03`](./03-Core-Modules-And-Async.md)
- [x] `stream` — readable, writable, duplex, **transform**, `pipe`, `pipeline` → [`03`](./03-Core-Modules-And-Async.md)
- [x] `Buffer` & binary data → [`03`](./03-Core-Modules-And-Async.md)
- [x] `crypto` (hash, hmac, randomBytes, ciphers) → [`03`](./03-Core-Modules-And-Async.md), [`07`](./07-Authentication-And-Security.md)
- [x] `util.promisify`, `util.inspect` → [`03`](./03-Core-Modules-And-Async.md)
- [x] `child_process`, `worker_threads`, `cluster` → [`08`](./08-Advanced-Node-And-Deployment.md)

### D. Async patterns
- [x] **Error-first callbacks** & callback hell → [`03`](./03-Core-Modules-And-Async.md)
- [x] Promises (states, chaining, error propagation, `Promise.all/allSettled/race/any`) → [`03`](./03-Core-Modules-And-Async.md)
- [x] **`async`/`await`**, error handling with `try/catch` → [`03`](./03-Core-Modules-And-Async.md)
- [x] Top-level await (ESM) → [`02`](./02-Modules-And-NPM.md), [`03`](./03-Core-Modules-And-Async.md)
- [x] Async iterators, `for await...of` → [`03`](./03-Core-Modules-And-Async.md)
- [x] Backpressure & streams → [`03`](./03-Core-Modules-And-Async.md), [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] `AbortController` / `AbortSignal` → [`03`](./03-Core-Modules-And-Async.md)

### E. Express fundamentals
- [x] What Express is, philosophy → [`04`](./04-Express-Fundamentals.md)
- [x] App, routes, route handlers → [`04`](./04-Express-Fundamentals.md)
- [x] HTTP verbs (GET / POST / PUT / PATCH / DELETE / OPTIONS / HEAD) → [`04`](./04-Express-Fundamentals.md), [`05`](./05-Building-REST-APIs.md)
- [x] Route parameters, query strings, body parsing → [`04`](./04-Express-Fundamentals.md)
- [x] `req` / `res` object — every important method → [`04`](./04-Express-Fundamentals.md)
- [x] **Middleware** concept, ordering, `next()` → [`04`](./04-Express-Fundamentals.md), [`06`](./06-Middleware-And-Error-Handling.md)
- [x] Built-in middleware (`express.json`, `express.urlencoded`, `express.static`) → [`04`](./04-Express-Fundamentals.md)
- [x] Third-party middleware (cors, helmet, morgan, cookie-parser) → [`04`](./04-Express-Fundamentals.md), [`07`](./07-Authentication-And-Security.md)
- [x] **`express.Router`** modularization → [`04`](./04-Express-Fundamentals.md)
- [x] Static files, view engines (EJS/Pug/Handlebars) — pointer → [`04`](./04-Express-Fundamentals.md)
- [x] Path-to-regexp patterns → [`04`](./04-Express-Fundamentals.md)

### F. REST API design
- [x] REST principles (resources, statelessness, uniform interface) → [`05`](./05-Building-REST-APIs.md)
- [x] Resource modeling, URI design → [`05`](./05-Building-REST-APIs.md)
- [x] **HTTP status codes** (the ones that matter) → [`05`](./05-Building-REST-APIs.md)
- [x] Full CRUD endpoint design → [`05`](./05-Building-REST-APIs.md)
- [x] **Validation** with `zod` and `express-validator` → [`05`](./05-Building-REST-APIs.md)
- [x] Pagination, filtering, sorting → [`05`](./05-Building-REST-APIs.md)
- [x] API versioning (URL, header) → [`05`](./05-Building-REST-APIs.md)
- [x] **MVC + Service layer** (controllers / services / repositories) → [`05`](./05-Building-REST-APIs.md)
- [x] DTOs, serialization → [`05`](./05-Building-REST-APIs.md)
- [x] **Database integration** (PostgreSQL via Prisma; ORM pointers for Sequelize/Mongoose) → [`05`](./05-Building-REST-APIs.md)
- [x] HATEOAS — what it is and when you'd care → [`05`](./05-Building-REST-APIs.md)

### G. Middleware & errors
- [x] Custom middleware patterns → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] **Error-handling middleware** (4-arg `(err, req, res, next)`) → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] Async error wrapper / `express-async-errors` → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] Centralized AppError class & error mapper → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] 404 catch-all → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] Logging with **morgan**, **winston**, **pino** → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] Request ID / correlation ID → [`06`](./06-Middleware-And-Error-Handling.md)
- [x] Full request lifecycle in Express → [`06`](./06-Middleware-And-Error-Handling.md)

### H. Authentication & security
- [x] **Password hashing** with bcrypt → [`07`](./07-Authentication-And-Security.md)
- [x] **JWT** (structure, sign, verify), access + refresh tokens → [`07`](./07-Authentication-And-Security.md)
- [x] Sessions & cookies (`express-session`, `cookie-parser`) → [`07`](./07-Authentication-And-Security.md)
- [x] **OAuth2** & OpenID Connect overview, Passport.js → [`07`](./07-Authentication-And-Security.md)
- [x] **Role-based authorization** middleware → [`07`](./07-Authentication-And-Security.md)
- [x] **helmet**, **cors**, **rate limiting**, **input sanitization**, **HPP** → [`07`](./07-Authentication-And-Security.md)
- [x] **OWASP top issues** for Node (SQLi, XSS, CSRF, IDOR, SSRF, deserialization) → [`07`](./07-Authentication-And-Security.md)
- [x] HTTPS, secure cookies, `SameSite` → [`07`](./07-Authentication-And-Security.md)
- [x] Secrets management & **dotenv**, 12-factor → [`07`](./07-Authentication-And-Security.md), [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **File uploads** with `multer` (typed, sized, validated) → [`07`](./07-Authentication-And-Security.md)

### I. Advanced Node & deployment
- [x] **Testing** with Jest + Supertest, fixtures, mocking → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **WebSockets** with Socket.IO → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **Caching** with Redis (`ioredis`) → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **Clustering** + **worker_threads** + **pm2** → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] Streams at scale, backpressure → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **Graceful shutdown** (SIGTERM, drain) → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **Docker** for Node, multi-stage builds → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] Environment config (NODE_ENV, dotenv, secrets) → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] Deployment targets (VPS, Render/Railway/Fly, AWS) → [`08`](./08-Advanced-Node-And-Deployment.md)
- [x] **Health checks**, readiness vs liveness, monitoring (OpenTelemetry pointer) → [`08`](./08-Advanced-Node-And-Deployment.md)

---

## 🛠️ SETUP — GET A WORKING NODE TOOLCHAIN

You write `.js` (or `.ts`) source files; Node executes them. You need **Node** itself, npm comes bundled, and a way to run multiple versions.

### Which version?

Use the **current Active LTS** of Node (even-numbered: 18, 20, 22...). LTS releases get bug fixes for ~30 months. As of writing the strong default is **Node 20 LTS** or **22 LTS**. Everything in this section runs on Node 18+.

### Install

| OS | Easiest path |
|----|--------------|
| Windows | [nodejs.org](https://nodejs.org) installer · or `winget install OpenJS.NodeJS.LTS` · or **fnm** for multi-version |
| macOS | `brew install node` · or **fnm** / **nvm** for multi-version |
| Linux | Use **nvm** or **fnm** (avoid the distro package — usually too old) |

A multi-version manager is strongly recommended. **fnm** (fast) and **nvm** (classic) both let you switch:

```bash
# After installing fnm:
fnm install 20         # install Node 20 LTS
fnm use 20             # switch to it
fnm default 20         # make it default
node -v && npm -v      # verify
```

### Your first script

```js
// hello.js
console.log("Welcome to Node.js & Express.");
console.log("Running Node version:", process.version);
console.log("On platform:", process.platform);
```

```bash
node hello.js
# Welcome to Node.js & Express.
# Running Node version: v20.x.x
# On platform: win32
```

### Your first project

```bash
mkdir my-api && cd my-api
npm init -y                     # creates package.json with sane defaults
npm install express             # adds Express to dependencies
echo "node_modules" > .gitignore
```

```js
// index.js  — three-line "hello server"
import express from "express";   // works only if package.json has "type": "module"
const app = express();
app.get("/", (_req, res) => res.json({ hello: "world" }));
app.listen(3000, () => console.log("http://localhost:3000"));
```

```bash
node index.js
# in another terminal:  curl http://localhost:3000
```

### The tools you will actually use

- **Editor:** VS Code with the **ESLint** + **Prettier** + **REST Client** extensions.
- **Runtime helpers:** `nodemon` (or `node --watch` on Node 20+) for auto-restart in dev.
- **Process manager (prod):** `pm2` for clustering and zero-downtime restarts.
- **API tester:** Postman, Insomnia, or `curl` / `httpie`.
- **Type-checker:** TypeScript — section [`03-TYPESCRIPT`](../03-TYPESCRIPT/) covers it; we keep examples here in plain JS for clarity but show TS where it matters.

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Type everything.** Type the snippets, run them, break them. Read the stack traces.
2. **Keep a `scratch/` folder** with throwaway scripts. Use it to test ideas the moment they appear.
3. **Build a real REST API alongside file 05.** Pick a domain (notes, todos, books) and grow it through every chapter — by file 08 it should be tested, secured, and Docker-deployable.
4. **Don't skip file 06.** Most production Express bugs live in middleware order and unhandled async errors.
5. **Read every "Common Pitfalls" table.** Those are the bugs you would otherwise hit in production.

### The Project (do this once, all the way through)

Pick a domain you actually care about (your reading list, gym log, recipe box) and grow it as you read:

| After file | Your project should... |
|------------|-------------------------|
| 01–02 | Have a working `package.json`, a `dev` script, and one route. |
| 03 | Read/write data from disk via `node:fs/promises` and stream a CSV. |
| 04 | Have modular routers, JSON body parsing, and 4–5 endpoints. |
| 05 | Be a real REST API: validation (zod), pagination, MVC layers, Postgres via Prisma. |
| 06 | Have a centralized error handler, structured logs (pino), and a 404. |
| 07 | Have signup/login (bcrypt + JWT or session), helmet, cors, rate limit, role-based authz. |
| 08 | Have unit + API tests, Redis cache, graceful shutdown, a Dockerfile, and a deployed URL. |

That single, long project is worth ten tutorials.

---

## 🧰 OPINIONATED STARTER STACK (used in this section)

When the codex shows code, this is the stack it leans on. Each is replaceable; the patterns transfer.

| Concern | Pick | Why |
|---------|------|-----|
| Module system | **ESM** (`"type": "module"`) | Standard, top-level await, modern |
| Web framework | **Express 4 / 5** | Largest ecosystem; concepts transfer to Fastify/Koa |
| Validation | **zod** | One schema, runtime check + TS type |
| ORM | **Prisma** (Postgres) | Type-safe, great DX, migration story |
| Auth | **bcrypt** + **JWT (access)** + **refresh-token cookie** | Standard for SPAs/mobile |
| Logging | **pino** + **pino-http** | Fast, structured, prod-ready |
| HTTP request log | **morgan** (dev) / pino-http (prod) | Light overhead |
| Security | **helmet**, **cors**, **express-rate-limit**, **hpp** | Default-on protections |
| File uploads | **multer** | Standard in Express |
| Realtime | **socket.io** + Redis adapter | Rooms, fallbacks, scale |
| Cache / queues | **ioredis** | Mature Node Redis client |
| Testing | **Jest** (or Vitest) + **Supertest** | Unit + API tests |
| Process | **pm2** (VPS) or one-process-per-container (Docker/K8s) | Choose by deploy target |
| Deploy | **Docker** image → **Fly.io / Render / ECS** | Portable + boring |

> **Core skill:** the goal is fluency with the *patterns*, not loyalty to a library. Once you know how middleware/error-handling/auth/streams work in Express, picking up Fastify or NestJS is a weekend.

---

## 📅 SUGGESTED CADENCE

If you can give it 1–2 hours a day, this section comfortably fits in **3 weeks**:

| Week | Focus | Files |
|------|-------|-------|
| 1 | Runtime, modules, async, core APIs | 01 → 03 |
| 2 | Express + REST + middleware/errors | 04 → 06 |
| 3 | Auth/security + production + deploy | 07 → 08 |

Spend the last weekend deploying your project somewhere public and writing a tiny README. That deploy is what you'll show in interviews.

---

## 🔗 RELATED SECTIONS

- Pairs with [`08-SQL-DATABASES`](../08-SQL-DATABASES/) (Postgres + Prisma) and [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/) (Mongoose).
- Frontend that consumes these APIs: [`05-REACT`](../05-REACT/) and [`06-NEXTJS`](../06-NEXTJS/).
- Combined into a full app in [`10-MERN-STACK`](../10-MERN-STACK/) and shipped in [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/).
- Language depth: [`02-JAVASCRIPT-MASTERY`](../02-JAVASCRIPT-MASTERY/) and [`03-TYPESCRIPT`](../03-TYPESCRIPT/).

---

## 📖 DEEP REFERENCES

- **Node.js docs** — <https://nodejs.org/en/docs> (the API is the source of truth)
- **Express docs** — <https://expressjs.com> (small surface, read it all)
- **MDN HTTP** — <https://developer.mozilla.org/en-US/docs/Web/HTTP>
- **OWASP Top 10** — <https://owasp.org/www-project-top-ten/>
- **The Twelve-Factor App** — <https://12factor.net> (config, processes, deploy)
- **Node.js Best Practices** (community) — <https://github.com/goldbergyoni/nodebestpractices>
- **JWT.io** — <https://jwt.io> (decode tokens, learn the structure)

---

**→ Begin:** [`01-The-Nodejs-Runtime.md`](./01-The-Nodejs-Runtime.md) | Back to [`../README.md`](../README.md)
