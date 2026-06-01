# 🟢 08 — Advanced Node & Deployment

> *"A backend isn't done when the tests are green. It's done when it survives a Friday-afternoon traffic spike, restarts gracefully when you push a fix, and tells you exactly what it's doing while it does it."*

**Prev:** [`07-Authentication-And-Security.md`](./07-Authentication-And-Security.md) · **Next:** [`../08-SQL-DATABASES/00-Index.md`](../08-SQL-DATABASES/00-Index.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. TESTING — THE FOUNDATION

A Node API that you'll trust at 3am has three layers of tests:

| Layer | What it checks | Tools |
|-------|----------------|-------|
| **Unit** | A pure function / service in isolation | Jest, Vitest, `node:test` |
| **Integration** | Service + DB / Redis / queue | Jest + Testcontainers |
| **API / e2e** | The HTTP surface end to end | Supertest |

### Set up Jest

```bash
npm install --save-dev jest supertest @types/jest cross-env
```

```json
// package.json
{
  "scripts": {
    "test":         "cross-env NODE_ENV=test jest",
    "test:watch":   "cross-env NODE_ENV=test jest --watch",
    "test:coverage":"cross-env NODE_ENV=test jest --coverage"
  },
  "jest": {
    "testEnvironment": "node",
    "testPathIgnorePatterns": ["/node_modules/", "/dist/"]
  }
}
```

For ESM projects, prefer **Vitest** (Jest-compatible API, native ESM):

```bash
npm install --save-dev vitest supertest
```

```json
"scripts": { "test": "vitest run", "test:watch": "vitest" }
```

### Unit test — a pure service

```js
// services/__tests__/cart.service.test.js
import { applyCoupon } from "../cart.service.js";

test("applies a 10% coupon", () => {
  expect(applyCoupon(100, "SAVE10")).toBe(90);
});

test("rejects unknown coupons", () => {
  expect(() => applyCoupon(100, "NOPE")).toThrow(/unknown/i);
});
```

### API test with Supertest

```js
// __tests__/todos.api.test.js
import request from "supertest";
import app from "../src/app.js";

describe("Todos API", () => {
  let token;
  beforeAll(async () => {
    const r = await request(app)
      .post("/api/v1/auth/login")
      .send({ email: "ada@example.com", password: "hunter2pass" });
    token = r.body.accessToken;
  });

  it("creates and lists a todo", async () => {
    const created = await request(app)
      .post("/api/v1/todos")
      .set("Authorization", `Bearer ${token}`)
      .send({ title: "Walk the dog" })
      .expect(201);

    expect(created.body.data).toMatchObject({ title: "Walk the dog", done: false });

    const list = await request(app).get("/api/v1/todos").set("Authorization", `Bearer ${token}`);
    expect(list.body.data.find(t => t.id === created.body.data.id)).toBeTruthy();
  });

  it("422 on missing title", async () => {
    await request(app)
      .post("/api/v1/todos")
      .set("Authorization", `Bearer ${token}`)
      .send({}).expect(422);
  });
});
```

> **Tip:** export the `app` (no `app.listen`) from `app.js`. Boot the server in `index.js`. Tests `import app` and never bind a port.

### Mocking — the pragmatic rules

- **Don't mock what you own** when you can use the real thing cheaply (in-memory DB / SQLite / Testcontainers).
- **Do mock external services**: payment processors, third-party HTTP, email senders.
- Use `jest.mock("../services/email.js")` to swap implementations; for HTTP, **`nock`** intercepts outgoing requests.

### Test database — Testcontainers

```bash
npm install --save-dev @testcontainers/postgresql
```

```js
import { PostgreSqlContainer } from "@testcontainers/postgresql";
let container;
beforeAll(async () => {
  container = await new PostgreSqlContainer().start();
  process.env.DATABASE_URL = container.getConnectionUri();
  // run migrations...
}, 60_000);
afterAll(async () => container && container.stop());
```

This spins up a real Postgres in Docker per test run — slower than mocks, far more truthful.

---

## II. WEBSOCKETS — REAL-TIME WITH SOCKET.IO

When you need push, presence, chat, live dashboards, multiplayer, switch from request/response to **WebSockets**. Raw `ws` is 60 lines; `socket.io` adds rooms, fallbacks, auth, and reconnects.

```bash
npm install socket.io
```

```js
// realtime.js
import { Server } from "socket.io";

export const attachRealtime = (httpServer) => {
  const io = new Server(httpServer, {
    cors: { origin: process.env.CORS_ORIGIN, credentials: true }
  });

  // Auth handshake using your JWT
  io.use((socket, next) => {
    try {
      const token = socket.handshake.auth?.token;
      const payload = jwt.verify(token, process.env.JWT_ACCESS_SECRET);
      socket.user = { id: payload.sub, role: payload.role };
      next();
    } catch (err) { next(new Error("unauthorized")); }
  });

  io.on("connection", (socket) => {
    console.log("connected", socket.id, socket.user.id);

    socket.join(`user:${socket.user.id}`);              // private room

    socket.on("chat:join", (room) => socket.join(`room:${room}`));
    socket.on("chat:msg",  ({ room, text }) => {
      io.to(`room:${room}`).emit("chat:msg", { from: socket.user.id, text, at: Date.now() });
    });

    socket.on("disconnect", () => console.log("gone", socket.id));
  });

  return io;
};
```

```js
// index.js — share the HTTP server
import http from "node:http";
import app  from "./app.js";
import { attachRealtime } from "./realtime.js";

const server = http.createServer(app);
const io = attachRealtime(server);
server.listen(3000);
```

Client (browser):

```js
import { io } from "socket.io-client";
const socket = io("https://api.example.com", { auth: { token } });
socket.emit("chat:join", "general");
socket.on("chat:msg", ({ from, text }) => console.log(from, text));
```

### Scaling Socket.IO across multiple Node processes

A single Node process holds connections. With **clustering**, sockets on process A can't broadcast to clients on process B unless you **adapter** them:

```bash
npm install @socket.io/redis-adapter
```

```js
import { createAdapter } from "@socket.io/redis-adapter";
import Redis from "ioredis";

const pub = new Redis(process.env.REDIS_URL);
const sub = pub.duplicate();
io.adapter(createAdapter(pub, sub));
```

Now `io.emit(...)` reaches clients on every process. Without an adapter, clustered Socket.IO is a footgun.

---

## III. CACHING WITH REDIS

Caching is not optional past a certain scale. Reach for Redis when:

- A handful of endpoints are read-heavy (top items, leaderboards, hot search results).
- You need shared state across processes (rate limits, session store, Socket.IO adapter).
- You need queues, pub/sub, or short-lived locks.

```bash
npm install ioredis
```

```js
// lib/redis.js
import Redis from "ioredis";
export const redis = new Redis(process.env.REDIS_URL, {
  // Recommended defaults
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
});
```

### Cache-aside pattern

```js
const KEY = (id) => `todo:${id}`;
const TTL = 60;                                 // seconds

export async function getTodoCached(id) {
  const cached = await redis.get(KEY(id));
  if (cached) return JSON.parse(cached);

  const todo = await db.todo.findUnique({ where: { id } });
  if (todo) await redis.set(KEY(id), JSON.stringify(todo), "EX", TTL);
  return todo;
}

export async function updateTodo(id, patch) {
  const todo = await db.todo.update({ where: { id }, data: patch });
  await redis.del(KEY(id));                      // invalidate
  return todo;
}
```

### Pitfalls of caching

- **Cache stampede** — many requests miss at once and all hammer the DB. Use a short randomized TTL or **single-flight** locks (`redlock`).
- **Stale data** — pick TTL to match how stale you can tolerate. For "must be fresh" data, invalidate on writes (cache-aside) or use **write-through**.
- **Forgetting to invalidate** — every write path that mutates `todo:42` must `DEL todo:42`.
- **Caching personalized data under a shared key** — disaster. Include user/tenant in the key.

### Redis as a rate limiter / session store

```bash
npm install rate-limit-redis express-rate-limit connect-redis
```

```js
import { rateLimit } from "express-rate-limit";
import RedisStore from "rate-limit-redis";
import { redis } from "./lib/redis.js";

app.use(rateLimit({
  windowMs: 60_000,
  max: 120,
  store: new RedisStore({ sendCommand: (...args) => redis.call(...args) })
}));
```

---

## IV. CLUSTERING — USING ALL YOUR CPU CORES

A single Node process pins to one core. For CPU-light, I/O-bound services (most APIs), one process is often enough — but `cluster` (or **pm2**) lets you fan out across cores with zero code changes:

```js
// cluster.js
import cluster from "node:cluster";
import os from "node:os";

if (cluster.isPrimary) {
  const cores = os.cpus().length;
  console.log(`primary ${process.pid} forking ${cores} workers`);
  for (let i = 0; i < cores; i++) cluster.fork();

  cluster.on("exit", (worker, code) => {
    console.log(`worker ${worker.process.pid} died (${code}) — restarting`);
    cluster.fork();
  });
} else {
  await import("./index.js");                    // each worker boots the app
}
```

**pm2** does this and a lot more (zero-downtime reload, log management, monitoring):

```bash
npm install -g pm2

pm2 start dist/index.js -i max --name api      # 1 worker per core
pm2 logs api                                    # tailing logs
pm2 reload api                                  # zero-downtime reload
pm2 monit                                        # interactive dashboard
pm2 startup && pm2 save                         # boot on system start
```

```json
// ecosystem.config.cjs
module.exports = {
  apps: [{
    name: "api",
    script: "dist/index.js",
    instances: "max",
    exec_mode: "cluster",
    env_production: { NODE_ENV: "production", PORT: 3000 }
  }]
};
```

> **In Kubernetes / Docker?** Run **one process per container** and let the orchestrator scale containers. Don't double-stack with `pm2 -i max` inside the container; you'll oversubscribe CPUs.

---

## V. WORKER THREADS — REAL CPU PARALLELISM

Cluster forks **separate processes** (heavy, isolated, expensive to share data). For *true* shared-memory parallelism inside one process, use **worker_threads**:

```js
// worker.js — runs in a separate thread
import { parentPort, workerData } from "node:worker_threads";

function fib(n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }

parentPort.postMessage(fib(workerData.n));
```

```js
// main.js
import { Worker } from "node:worker_threads";

function fibAsync(n) {
  return new Promise((resolve, reject) => {
    const w = new Worker("./worker.js", { workerData: { n } });
    w.on("message", resolve);
    w.on("error",   reject);
    w.on("exit",    code => code !== 0 && reject(new Error(`exit ${code}`)));
  });
}

console.log(await fibAsync(40));
```

Use a **pool** (e.g. `piscina`) so you don't pay startup cost on every call:

```bash
npm install piscina
```

```js
import Piscina from "piscina";
const pool = new Piscina({ filename: new URL("./worker.js", import.meta.url).pathname });
app.post("/render", async (req, res) => res.send(await pool.run(req.body)));
```

> **When to use which:**
> - **Worker threads:** CPU-heavy work in-process (image transforms, parsing big files, hashing, ML inference).
> - **Cluster / pm2:** scale a stateless HTTP API across cores.
> - **child_process:** invoke another program (`git`, `ffmpeg`).

---

## VI. STREAMS AT SCALE

You met streams in file 03. In production, the patterns to know:

### Backpressure for free with `pipeline`

```js
import { pipeline } from "node:stream/promises";

app.get("/export.csv", async (req, res) => {
  res.setHeader("content-type", "text/csv");
  res.setHeader("content-disposition", 'attachment; filename="export.csv"');

  const dbStream = db.todo.streamCsv();         // a Readable producing CSV rows
  await pipeline(dbStream, res);                // honors res.write backpressure
});
```

This streams arbitrarily large exports with bounded memory.

### Transform pipelines — gzip + line-counting + uppercase

```js
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";
import { Transform } from "node:stream";
import { pipeline } from "node:stream/promises";

const upper = new Transform({
  transform(chunk, _enc, cb) { cb(null, chunk.toString().toUpperCase()); }
});

await pipeline(
  createReadStream("input.txt", { encoding: "utf8" }),
  upper,
  createGzip(),
  createWriteStream("output.txt.gz")
);
```

### `Readable.from` — anything iterable becomes a stream

```js
import { Readable } from "node:stream";
async function* generate() {
  for (let i = 0; i < 1_000_000; i++) yield `row ${i}\n`;
}
Readable.from(generate()).pipe(res);
```

---

## VII. GRACEFUL SHUTDOWN

Containers receive `SIGTERM` (10–30 seconds before `SIGKILL`). You must:

1. Stop accepting new connections (`server.close()`).
2. Wait for in-flight requests to finish, with a hard cap.
3. Close DB pools, queues, Redis, sockets.
4. Exit.

```js
// shutdown.js
export function setupGracefulShutdown(server, deps) {
  let shuttingDown = false;
  const onSig = async (sig) => {
    if (shuttingDown) return;
    shuttingDown = true;
    console.log(`Got ${sig}. Draining...`);

    // Stop accepting new requests; existing ones can finish
    server.close(() => console.log("HTTP server closed"));

    // Hard cap so we don't wait forever
    const killer = setTimeout(() => {
      console.error("Force exit");
      process.exit(1);
    }, 25_000).unref();

    try {
      await Promise.allSettled([
        deps.prisma?.$disconnect(),
        deps.redis?.quit(),
        deps.io?.close()
      ]);
    } finally {
      clearTimeout(killer);
      process.exit(0);
    }
  };

  process.on("SIGTERM", onSig);
  process.on("SIGINT",  onSig);
}
```

```js
// index.js
import { setupGracefulShutdown } from "./shutdown.js";
const server = app.listen(PORT);
setupGracefulShutdown(server, { prisma, redis, io });
```

> **Tip:** if you're behind a load balancer, **fail readiness checks first**, then start draining. The LB stops sending you traffic; only then do you `server.close()`.

---

## VIII. HEALTH CHECKS

Two distinct checks for orchestrators (Kubernetes, ECS, Render, Fly):

| Endpoint | Purpose | Should it touch the DB? |
|----------|---------|--------------------------|
| **liveness** (`/healthz`) | "Is the process alive?" Restart if not | No — keep it cheap |
| **readiness** (`/readyz`) | "Can I serve traffic?" Pull out of LB if not | Yes — pings DB/Redis |

```js
app.get("/healthz", (req, res) => res.json({ ok: true, pid: process.pid, uptime: process.uptime() }));

app.get("/readyz", async (req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    await redis.ping();
    res.json({ ok: true });
  } catch (err) {
    res.status(503).json({ ok: false, error: err.message });
  }
});
```

> **Never block traffic on a flaky liveness check.** If liveness fails for any transient reason, Kubernetes will keep killing your pods.

---

## IX. ENVIRONMENT CONFIG — 12-FACTOR

Recap from file 07: **strict env at boot**.

```js
// config/env.js
import "dotenv/config";
import { z } from "zod";

export const env = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT:     z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL:    z.string().url().optional(),
  JWT_ACCESS_SECRET:  z.string().min(32),
  JWT_REFRESH_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace"]).default("info")
}).parse(process.env);
```

In containers, *do not* ship a `.env` file — inject env via the platform's secret system.

---

## X. DOCKER — SHIPPING NODE PROPERLY

### A correct, multi-stage Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.7

# ---- 1) Install deps in a builder stage with dev deps ----
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --ignore-scripts

# ---- 2) Build the app (TS compile, etc.) ----
FROM deps AS build
COPY . .
RUN npm run build         # produces /app/dist

# ---- 3) Production image with only runtime deps ----
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev --ignore-scripts && npm cache clean --force
COPY --from=build /app/dist ./dist

# Run as non-root
RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 3000

# Use 'node' directly so SIGTERM propagates (NOT 'npm start')
CMD ["node", "dist/index.js"]

# Optional health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD wget -qO- http://localhost:3000/healthz || exit 1
```

### `.dockerignore` — keep images lean and safe

```
node_modules
.git
.env
.env.*
coverage
*.log
Dockerfile*
docker-compose*
README.md
```

### `docker-compose.yml` for local dev

```yaml
services:
  api:
    build: .
    ports: ["3000:3000"]
    environment:
      DATABASE_URL: postgres://app:app@db:5432/app
      REDIS_URL:    redis://redis:6379
      JWT_ACCESS_SECRET: dev-access-secret-32-bytes-or-more-aaaaaa
      JWT_REFRESH_SECRET: dev-refresh-secret-32-bytes-or-more-bbb
    depends_on: [db, redis]
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    volumes: ["pgdata:/var/lib/postgresql/data"]
  redis:
    image: redis:7-alpine
volumes:
  pgdata:
```

> **Why `node` not `npm start`:** `npm` swallows signals and forks. With `CMD ["node", "dist/index.js"]`, `SIGTERM` reaches your app and graceful shutdown works.

---

## XI. WHERE TO DEPLOY NODE

| Target | Strengths | Watch out for |
|--------|-----------|---------------|
| **VPS** (Hetzner, DO) + nginx + pm2 | Cheapest, full control | You manage everything (TLS, OS updates) |
| **Render / Railway / Fly.io** | "git push, get URL", auto-TLS | Vendor pricing, cold starts on cheap tiers |
| **AWS ECS / EKS** | Mature, scalable, integrates with everything | Operational complexity |
| **Vercel / Netlify (functions)** | Zero-ops, perfect for SSR / edge | Timeouts, statelessness, cold starts |
| **Cloudflare Workers / Bun / Deno Deploy** | Fast edge, low latency | Smaller subset of Node API |

For a *typical* Express API: **Render or Fly.io for hobby/SMB**, **AWS ECS or EKS for serious production**, **a VPS** if you like operating servers.

### A Fly.io deploy in 4 commands

```bash
# 1. install flyctl, then
fly launch         # detects Node, generates fly.toml, builds Docker
fly secrets set JWT_ACCESS_SECRET=$(node -e "console.log(require('crypto').randomBytes(64).toString('hex'))")
fly deploy
fly logs
```

---

## XII. LOGGING & MONITORING IN PRODUCTION

### Structured logs out of the box

We chose **pino** in file 06. In prod:

```js
const logger = pino({
  level: env.LOG_LEVEL,
  redact: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token"],
  formatters: {
    level: (label) => ({ level: label })   // standardize for log aggregators
  },
  timestamp: pino.stdTimeFunctions.isoTime
});
```

Ship logs to **stdout/stderr** — let the platform collect them (Cloud Logging, CloudWatch, Datadog, Loki). Don't write log files inside containers.

### Metrics & traces — OpenTelemetry

```bash
npm install @opentelemetry/api @opentelemetry/sdk-node \
  @opentelemetry/instrumentation-http @opentelemetry/instrumentation-express \
  @opentelemetry/exporter-trace-otlp-http
```

```js
// otel.js — load this BEFORE express imports
import { NodeSDK } from "@opentelemetry/sdk-node";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";

new NodeSDK({
  serviceName: "todo-api",
  traceExporter: new OTLPTraceExporter({ url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT }),
  instrumentations: [getNodeAutoInstrumentations()]
}).start();
```

```bash
node --import ./otel.js dist/index.js
```

You get distributed traces (Express → Prisma → Redis), metrics, and logs correlated by trace ID. Forward to Honeycomb, Datadog, Grafana Tempo, etc.

### What to alert on

- **5xx rate** above a threshold for N minutes
- **p95 latency** above SLO
- **Error budget burn** (SLO-based alerting)
- **Memory / event-loop lag** for the process
- **Auth failures** spiking (credential stuffing)
- **Queue depth** for background jobs

---

## XIII. PERFORMANCE — KNOW THE BOTTLENECK

A short ranking of what usually slows Node services:

1. **Database** (slow queries, missing indexes, n+1).
2. **External HTTP calls** (no timeout, no retry budget, blocking serial).
3. **JSON / serialization** (huge payloads — paginate, compress, project columns).
4. **Sync work** in the request path (sync `fs`, regex on big inputs).
5. **Lack of caching** for read-heavy endpoints.
6. **Single-process bottleneck on multi-core machines** (cluster / pm2).

Tools:

```bash
# CPU profile — produces an isolate-*.log → V8 profiler format
node --prof dist/index.js
node --prof-process isolate-*.log > profile.txt

# Flamegraph
npx 0x dist/index.js

# Heap snapshot near limit
node --heapsnapshot-near-heap-limit=2 --max-old-space-size=512 dist/index.js

# Modern: built-in inspector — open chrome://inspect
node --inspect dist/index.js
```

### Event-loop lag — a critical health metric

```js
import { monitorEventLoopDelay } from "node:perf_hooks";
const h = monitorEventLoopDelay({ resolution: 20 });
h.enable();
setInterval(() => {
  const p99ms = h.percentile(99) / 1e6;
  if (p99ms > 100) logger.warn({ p99ms }, "event loop lag spike");
}, 5_000).unref();
```

---

## XIV. CI/CD — THE SHORT VERSION

A lean GitHub Actions pipeline:

```yaml
# .github/workflows/ci.yml
name: CI
on: { push: { branches: [main] }, pull_request: {} }

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: postgres }
        ports: [ "5432:5432" ]
        options: >-
          --health-cmd "pg_isready -U postgres"
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm test
        env:
          DATABASE_URL: postgres://postgres:postgres@localhost:5432/postgres
          JWT_ACCESS_SECRET:  ci-secret-32-bytes-or-more-xxxxxxxxxxxxx
          JWT_REFRESH_SECRET: ci-secret-32-bytes-or-more-yyyyyyyyyyyy

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env: { FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }} }
```

Required pieces in any CI: **install (npm ci) → lint → test → build → deploy**.

---

## XV. THE PRODUCTION CHECKLIST

A condensed pre-flight list. Tick them all before you call your service production-ready.

- [x] `NODE_ENV=production` set everywhere
- [x] env vars validated at boot (zod) — fail fast on missing config
- [x] HTTPS terminating somewhere (TLS via LB / Caddy / nginx)
- [x] `helmet`, `cors`, `rate-limit`, body size limit set
- [x] Auth uses bcrypt/argon2; access tokens short-lived; refresh tokens rotated; secrets ≥ 32 bytes
- [x] Centralized error handler with sanitized prod messages
- [x] Structured logs (pino) → stdout, secrets redacted
- [x] `/healthz` (cheap) and `/readyz` (DB/Redis) endpoints
- [x] Graceful shutdown on `SIGTERM`
- [x] Connection pooling for DB (Prisma sets sane defaults; check it)
- [x] DB migrations are reproducible and backward-compatible (deploy-then-migrate or migrate-then-deploy strategy chosen)
- [x] Backups: DB + secrets — and **tested restores**
- [x] Monitoring + alerting on 5xx, p95, memory, event-loop lag
- [x] CI runs lint + tests + build before deploy
- [x] Multi-stage Docker image, non-root user, `.dockerignore`
- [x] Dependency audit clean (`npm audit`); Dependabot/Renovate enabled
- [x] Pinned Node version (`engines.node`) + base image (`node:20-alpine` not `node:latest`)
- [x] Logging cardinality controlled (no logging per-byte of every request body)
- [x] Runbook: deploy, rollback, incident response, oncall rotation

---

## XVI. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `npm start` as Docker `CMD` | `SIGTERM` ignored, ungraceful kills | `CMD ["node", "dist/index.js"]` |
| pm2 cluster *inside* a container | Oversubscribed CPU | One process per container, scale pods |
| Liveness probe hits the DB | Service flaps under DB blips | Liveness cheap, readiness deep |
| No graceful shutdown | Truncated requests on deploy | Wire `SIGTERM` + drain |
| Unbounded JSON | OOM under attack | `express.json({ limit: "1mb" })` |
| Cache without invalidation | Stale data | Invalidate on writes; bound TTL |
| Cache stampede | DB tipped over | Jittered TTL or `redlock` single-flight |
| Socket.IO across processes without adapter | Broadcasts miss clients | `@socket.io/redis-adapter` |
| Worker threads created per request | Slow, memory churn | Pool with `piscina` |
| Missing event-loop monitoring | Mystery slowness | `monitorEventLoopDelay`, OTel |
| Logging secrets | Compliance + breach risk | pino `redact` |
| Logging too much | $$ on log ingestion | Filter at level + sample |
| Mixing dev secrets with prod | Compromise | Separate vaults, separate CI envs |
| Trusting `.env` in prod | Easy to leak | Inject from secret manager |
| Building tests but not running them in CI | Untrusted main branch | CI is mandatory |

---

## 🧠 KEY TAKEAWAYS

- **Test in three layers** (unit, integration, API) and run them in CI on every PR.
- **WebSockets** with Socket.IO are easy; **scale them** with the Redis adapter.
- **Cache with Redis** for read-heavy endpoints; invalidate on writes; beware stampedes and stale data.
- Use **cluster** or **pm2** to fan across cores; **worker_threads** (with `piscina`) for CPU-bound work in-process.
- Stream large payloads with `pipeline`; honor backpressure for free.
- Implement **graceful shutdown** (`SIGTERM` → stop accept → drain → close deps → exit).
- Expose **liveness vs readiness**; logs go to **stdout** as JSON; ship traces with **OpenTelemetry**.
- Ship as a **multi-stage, non-root Docker image** running `node` directly so signals propagate.
- Validate config on boot, run `npm audit`, automate deploys, and keep a written runbook.
- The codex continues with the database that powers it all → [`../08-SQL-DATABASES/00-Index.md`](../08-SQL-DATABASES/00-Index.md).

---

**Prev:** [`07-Authentication-And-Security.md`](./07-Authentication-And-Security.md) · **Next:** [`../08-SQL-DATABASES/00-Index.md`](../08-SQL-DATABASES/00-Index.md) · **Index:** [`00-Index.md`](./00-Index.md)
