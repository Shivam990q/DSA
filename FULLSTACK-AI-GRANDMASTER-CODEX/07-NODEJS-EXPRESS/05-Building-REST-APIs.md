# 🟢 05 — Building REST APIs

> *"REST is not a framework, it's a discipline: name your nouns well, use HTTP verbs honestly, and let status codes carry meaning. Do that and your API documents itself."*

**Prev:** [`04-Express-Fundamentals.md`](./04-Express-Fundamentals.md) · **Next:** [`06-Middleware-And-Error-Handling.md`](./06-Middleware-And-Error-Handling.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT REST ACTUALLY MEANS

REST = **Representational State Transfer** (Roy Fielding, 2000). The constraints that matter in practice:

1. **Client-server** separation.
2. **Stateless** requests — every request carries everything the server needs (auth, params). No server-side session that the client implicitly relies on.
3. **Uniform interface** — everything is a **resource**, identified by a **URI**, manipulated via standard **HTTP verbs**, returning standard **representations** (JSON, usually).
4. **Layered** — caches, proxies, gateways are transparent.
5. **Cacheable** — responses are explicit about what's cacheable.
6. (Optional) **HATEOAS** — responses include links to related actions/resources.

Most "REST APIs" in the wild are really **HTTP APIs that lean on REST conventions**. That is fine. The discipline you keep is:

> **Resources are nouns. Verbs come from HTTP. State lives in representations. Errors come back as status codes + a body.**

---

## II. RESOURCE MODELING — NAME THE NOUNS WELL

Pick **plural nouns** for collections. Express identity in URLs, never in verbs.

```
GET    /users                  list users
POST   /users                  create a user
GET    /users/42               read user 42
PUT    /users/42               replace user 42 (full update)
PATCH  /users/42               partially update user 42
DELETE /users/42               delete user 42

GET    /users/42/posts         list posts for user 42 (sub-resource)
POST   /users/42/posts         create a post under user 42
GET    /posts/9                read post 9 (when posts are also a top-level resource)
```

### Bad URLs vs good URLs

| Don't | Do | Why |
|-------|-----|-----|
| `GET /getUser?id=42` | `GET /users/42` | Verb is in the method, identity in the path |
| `POST /deleteUser` | `DELETE /users/42` | Use the right HTTP verb |
| `/userList` | `/users` | Plural, lowercase, kebab-case if multi-word |
| `/users/42/delete` | `DELETE /users/42` | Don't put verbs in paths |
| `/api/Users` | `/api/users` | Lowercase URLs |
| `/api/orderItems` | `/api/order-items` | kebab-case for multi-word resources |

### Sub-resources vs flat URLs

Use sub-resources when the child only makes sense in the parent's scope:

```
GET /orders/42/items          ← items belong to order 42
```

If the child can stand alone (and you might query it across parents), keep it flat:

```
GET /comments?postId=9        ← comments live anywhere
```

### Actions that don't fit CRUD

Sometimes you genuinely need a verb (publish, archive, refund). Treat the action as a **sub-resource** or a transition:

```
POST /articles/42/publish              ← imperative endpoint
POST /payments/77/refund               ← creates a refund as a sub-resource
PATCH /articles/42  { "status":"published" }   ← state transition via PATCH
```

Pick one style per project and stay consistent.

---

## III. HTTP STATUS CODES — THE ONES THAT MATTER

Use standard codes. Clients (and your future self) know them.

### 2xx — success

| Code | Use |
|------|-----|
| `200 OK` | General success with a body |
| `201 Created` | Resource was created. Include `Location` header |
| `202 Accepted` | Request accepted, processing async (queues, jobs) |
| `204 No Content` | Success with no body (DELETE, PATCH that returns nothing) |

### 3xx — redirection

| Code | Use |
|------|-----|
| `301 Moved Permanently` | Resource moved permanently |
| `302 Found` | Temporary redirect |
| `304 Not Modified` | Conditional GET — client's cache is still fresh |

### 4xx — client error

| Code | Use |
|------|-----|
| `400 Bad Request` | Malformed request (bad JSON, missing fields) |
| `401 Unauthorized` | "You're not authenticated" (yes, the name is misleading) |
| `403 Forbidden` | Authenticated but **not allowed** |
| `404 Not Found` | Resource doesn't exist |
| `405 Method Not Allowed` | Path is real, method isn't supported here |
| `409 Conflict` | State conflict — e.g. unique-constraint violation, optimistic-lock fail |
| `410 Gone` | Resource intentionally removed |
| `415 Unsupported Media Type` | Body's content-type is wrong |
| `422 Unprocessable Entity` | JSON parsed fine, but validation failed |
| `429 Too Many Requests` | Rate limit exceeded |

### 5xx — server error

| Code | Use |
|------|-----|
| `500 Internal Server Error` | An unhandled bug |
| `502 Bad Gateway` | An upstream service failed |
| `503 Service Unavailable` | You're overloaded / maintenance |
| `504 Gateway Timeout` | Upstream timed out |

> **Gotcha — 401 vs 403.** `401` means "I don't know who you are; sign in." `403` means "I know exactly who you are, and you can't do that."

> **Gotcha — `200` with `{ error: "..." }`.** Don't. Use the right 4xx. Returning errors with 200 forces clients to parse bodies to detect failures.

---

## IV. JSON BODY CONVENTIONS

Pick a shape and never deviate.

```jsonc
// Success — single resource
{
  "data": { "id": 42, "name": "Ada" }
}

// Success — collection with pagination
{
  "data": [ /* ... */ ],
  "page":  { "page": 2, "perPage": 20, "total": 137 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "title is required",
    "details": [
      { "field": "title", "issue": "missing" }
    ]
  }
}
```

Use `camelCase` for JSON keys (matches JS). ISO-8601 strings for dates (`"2024-05-12T08:00:00Z"`). UUIDs for public IDs when sequential numbers leak business data ("we have 12 customers").

> **Tip — be conservative in what you send, liberal in what you accept.** Reject unknown fields on input (saves you from typos and security holes), but always include a small set of stable fields on output.

---

## V. PROJECT STRUCTURE — MVC + SERVICES

Tiny apps can live in `index.js`. Anything you'll maintain past a weekend deserves layers:

```
src/
├── index.js                # boot — only wires things up
├── app.js                  # express() + middleware + routes
├── config/
│   └── env.js              # validated env (zod-parsed process.env)
├── routes/
│   └── todo.routes.js      # express.Router for the resource
├── controllers/
│   └── todo.controller.js  # adapts HTTP to/from services
├── services/
│   └── todo.service.js     # business logic, transactions
├── repositories/
│   └── todo.repo.js        # database access (Prisma / Mongoose)
├── schemas/
│   └── todo.schema.js      # zod schemas for validation
├── middleware/
│   ├── error.js            # central error handler (file 06)
│   └── auth.js             # auth/authorization (file 07)
├── lib/
│   └── prisma.js           # singleton clients
├── errors/
│   └── AppError.js
└── utils/
```

The **rule of layers**:

- **Routes** describe HTTP endpoints. They wire URL+method → controller.
- **Controllers** translate HTTP to/from your domain. They read `req`, call services, write `res`.
- **Services** hold business logic. They don't know about HTTP.
- **Repositories** talk to the database. Services don't write SQL/Prisma queries directly (testable boundary).

This boundary makes testing trivial: you can call a service in a unit test without faking `req`/`res`.

---

## VI. VALIDATION — DO IT, ALWAYS

Validate **everything that comes from the client**: body, params, query, headers. Two excellent options:

### Option 1 — `zod` (preferred for TS-friendly schemas)

```bash
npm install zod
```

```js
// schemas/todo.schema.js
import { z } from "zod";

export const createTodoSchema = z.object({
  title: z.string().min(1).max(200),
  done:  z.boolean().optional().default(false),
  due:   z.coerce.date().optional()
});

export const idParamSchema = z.object({
  id: z.coerce.number().int().positive()
});

export const listQuerySchema = z.object({
  page:    z.coerce.number().int().positive().default(1),
  perPage: z.coerce.number().int().positive().max(100).default(20),
  q:       z.string().optional(),
  done:    z.enum(["true", "false"]).optional(),
  sort:    z.enum(["createdAt", "title"]).default("createdAt"),
  order:   z.enum(["asc", "desc"]).default("desc")
});
```

```js
// middleware/validate.js — generic validator factory
export const validate = (schemas) => (req, res, next) => {
  try {
    if (schemas.body)   req.body   = schemas.body.parse(req.body);
    if (schemas.params) req.params = schemas.params.parse(req.params);
    if (schemas.query)  req.query  = schemas.query.parse(req.query);
    next();
  } catch (err) {
    err.status = 422;
    next(err);
  }
};
```

```js
// routes/todo.routes.js
import { Router } from "express";
import { validate } from "../middleware/validate.js";
import { createTodoSchema, idParamSchema, listQuerySchema } from "../schemas/todo.schema.js";
import * as ctrl from "../controllers/todo.controller.js";

const router = Router();
router.get   ("/",     validate({ query: listQuerySchema }),                     ctrl.list);
router.get   ("/:id",  validate({ params: idParamSchema }),                       ctrl.get);
router.post  ("/",     validate({ body: createTodoSchema }),                      ctrl.create);
router.put   ("/:id",  validate({ params: idParamSchema, body: createTodoSchema }), ctrl.update);
router.delete("/:id",  validate({ params: idParamSchema }),                       ctrl.remove);
export default router;
```

### Option 2 — `express-validator`

```bash
npm install express-validator
```

```js
import { body, param, validationResult } from "express-validator";

router.post("/",
  body("title").isString().isLength({ min: 1, max: 200 }),
  body("done").optional().isBoolean(),
  (req, res, next) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) return res.status(422).json({ errors: errors.array() });
    next();
  },
  ctrl.create
);
```

Both work. **`zod`** wins when you want one schema for runtime validation **and** TypeScript types.

> **Rule:** never trust query/body/params. The browser is hostile until proven otherwise.

---

## VII. CONTROLLERS, SERVICES, REPOSITORIES — A WORKED EXAMPLE

```js
// controllers/todo.controller.js
import * as service from "../services/todo.service.js";

export const list = async (req, res) => {
  const result = await service.list(req.query);
  res.json(result);
};

export const get = async (req, res) => {
  const todo = await service.get(req.params.id);
  res.json({ data: todo });
};

export const create = async (req, res) => {
  const todo = await service.create(req.body);
  res.status(201).location(`/api/v1/todos/${todo.id}`).json({ data: todo });
};

export const update = async (req, res) => {
  const todo = await service.update(req.params.id, req.body);
  res.json({ data: todo });
};

export const remove = async (req, res) => {
  await service.remove(req.params.id);
  res.status(204).end();
};
```

```js
// services/todo.service.js — pure business logic, no HTTP
import * as repo from "../repositories/todo.repo.js";
import { AppError } from "../errors/AppError.js";

export async function list({ page, perPage, q, done, sort, order }) {
  const [items, total] = await Promise.all([
    repo.findMany({ page, perPage, q, done, sort, order }),
    repo.count({ q, done })
  ]);
  return { data: items, page: { page, perPage, total } };
}

export async function get(id) {
  const t = await repo.findById(id);
  if (!t) throw new AppError("Todo not found", 404, "TODO_NOT_FOUND");
  return t;
}

export async function create(input) {
  return repo.create(input);
}

export async function update(id, input) {
  const exists = await repo.exists(id);
  if (!exists) throw new AppError("Todo not found", 404, "TODO_NOT_FOUND");
  return repo.update(id, input);
}

export async function remove(id) {
  const ok = await repo.remove(id);
  if (!ok) throw new AppError("Todo not found", 404, "TODO_NOT_FOUND");
}
```

```js
// repositories/todo.repo.js — Prisma flavor (file 08-SQL-DATABASES covers Prisma)
import { prisma } from "../lib/prisma.js";

export const findById = (id) => prisma.todo.findUnique({ where: { id } });
export const exists   = (id) => prisma.todo.findUnique({ where: { id }, select: { id: true } });
export const findMany = ({ page, perPage, q, done, sort, order }) =>
  prisma.todo.findMany({
    where:   { ...(done && { done: done === "true" }), ...(q && { title: { contains: q, mode: "insensitive" } }) },
    skip:    (page - 1) * perPage,
    take:    perPage,
    orderBy: { [sort]: order }
  });
export const count    = ({ q, done }) =>
  prisma.todo.count({ where: { ...(done && { done: done === "true" }), ...(q && { title: { contains: q, mode: "insensitive" } }) } });
export const create   = (data)        => prisma.todo.create({ data });
export const update   = (id, data)    => prisma.todo.update({ where: { id }, data });
export const remove   = async (id)    => { try { await prisma.todo.delete({ where: { id } }); return true; } catch { return false; } };
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
// app.js — wiring it all together
import express from "express";
import morgan from "morgan";
import helmet from "helmet";
import cors from "cors";
import "express-async-errors";   // file 06 covers this
import todos from "./routes/todo.routes.js";

const app = express();
app.disable("x-powered-by");
app.use(helmet());
app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(morgan("dev"));

app.use("/api/v1/todos", todos);

// 404
app.use((req, res) => res.status(404).json({ error: { code: "NOT_FOUND", message: "Not Found" } }));

// Central error handler — file 06 fleshes this out
app.use((err, req, res, _next) => {
  const status = err.status ?? 500;
  res.status(status).json({
    error: { code: err.code ?? "INTERNAL", message: status === 500 ? "Internal error" : err.message }
  });
});

export default app;
```

```js
// index.js
import app from "./app.js";
const PORT = Number(process.env.PORT ?? 3000);
app.listen(PORT, () => console.log(`http://localhost:${PORT}`));
```

That is a production-shaped Express service.

---

## VIII. PAGINATION, FILTERING, SORTING

Two pagination styles dominate; pick the one that fits your data:

### Offset pagination (simple, drifts on inserts)

```
GET /todos?page=2&perPage=20
```

```jsonc
{
  "data": [ /* up to 20 items */ ],
  "page": { "page": 2, "perPage": 20, "total": 137, "totalPages": 7 }
}
```

Works for: admin tables, dashboards, anything with stable enough data.

### Cursor pagination (stable, scales)

```
GET /todos?after=eyJpZCI6MTAwMH0&limit=20
```

```jsonc
{
  "data": [ /* up to 20 items */ ],
  "page": { "nextCursor": "eyJpZCI6MTAyMH0", "hasMore": true }
}
```

Works for: feeds, infinite scroll, very large or write-heavy collections.

### Filtering and sorting

```
GET /todos?done=false&q=launch&sort=createdAt&order=desc
```

Validate the `sort` field against an allowlist:

```js
const SORTABLE = new Set(["createdAt", "title", "due"]);
if (!SORTABLE.has(sort)) throw new AppError("Bad sort field", 400);
```

> **Security note — never** pass `sort` straight into a SQL `ORDER BY` string from the client. That's a SQL-injection vector. Use ORM column names from an allowlist.

---

## IX. API VERSIONING

Three common styles:

| Style | Example | Notes |
|-------|---------|-------|
| **URL** | `/api/v1/todos` | Easiest to navigate; we use this. |
| **Header** | `Accept: application/vnd.myapp.v1+json` | Cleaner URLs, harder to test. |
| **Query** | `/api/todos?v=1` | Discouraged — caches and proxies don't love it. |

**Rule:** ship `v1` from day one. Never break it. Add `v2` for breaking changes; deprecate `v1` with a `Sunset` header and a long support window.

```
HTTP/1.1 200 OK
Sunset: Wed, 31 Dec 2025 23:59:59 GMT
Deprecation: true
Link: </api/v2/todos>; rel="successor-version"
```

---

## X. DTOs AND SERIALIZATION

Don't return your database rows raw. They might contain secrets (`passwordHash`), internal flags (`deletedAt`), or fields not yet meant to be public.

```js
// dto/todo.dto.js
export const toPublicTodo = (t) => ({
  id:        t.id,
  title:     t.title,
  done:      t.done,
  due:       t.due ? t.due.toISOString() : null,
  createdAt: t.createdAt.toISOString()
});
```

```js
// in the controller
res.json({ data: toPublicTodo(todo) });
```

For larger projects, use `class-transformer`, `superjson`, or zod's `.transform()` to serialize on the way out. The point is: **the wire format is a contract**, not a side-effect of your ORM.

---

## XI. CONNECTING A DATABASE — THE FOUR PATTERNS

Pointer to the database sections — full coverage in [`08-SQL-DATABASES`](../08-SQL-DATABASES/) and [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/). The shapes you'll meet:

### 1) Raw SQL with `pg` (Postgres) or `mysql2` (MySQL)

```js
import { Pool } from "pg";
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export const findById = async (id) => {
  // ALWAYS parameterize — never string-concat values
  const { rows } = await pool.query("SELECT * FROM todos WHERE id = $1", [id]);
  return rows[0];
};
```

> **Security:** use placeholder parameters. Concatenating user input into SQL = SQL injection.

### 2) **Prisma** (TS-first, schema-driven) — recommended in this codex

```bash
npm install prisma --save-dev
npx prisma init
npm install @prisma/client
```

```prisma
// prisma/schema.prisma
datasource db { provider = "postgresql"; url = env("DATABASE_URL") }
generator client { provider = "prisma-client-js" }

model Todo {
  id        Int      @id @default(autoincrement())
  title     String
  done      Boolean  @default(false)
  due       DateTime?
  createdAt DateTime @default(now())
}
```

```bash
npx prisma migrate dev --name init    # creates the table
npx prisma generate                   # regenerates the client
```

```js
// lib/prisma.js — single instance per process
import { PrismaClient } from "@prisma/client";
export const prisma = global.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== "production") global.prisma = prisma;
```

### 3) Sequelize (older, batteries-included ORM)

```js
import { Sequelize, DataTypes } from "sequelize";
const sequelize = new Sequelize(process.env.DATABASE_URL);
const Todo = sequelize.define("Todo", { title: DataTypes.STRING, done: DataTypes.BOOLEAN });
```

### 4) Mongoose (MongoDB)

```js
import mongoose from "mongoose";
await mongoose.connect(process.env.MONGO_URL);
const Todo = mongoose.model("Todo", new mongoose.Schema({ title: String, done: Boolean }));
```

> **Pick one per project.** Switching ORMs mid-flight is one of the most expensive refactors in software.

---

## XII. CONTENT NEGOTIATION & ETAGS (BRIEFLY)

Express handles ETags by default (`app.set("etag", "strong")`). Clients send `If-None-Match`; the server replies `304` if unchanged. Free bandwidth.

```js
res.set("Cache-Control", "private, max-age=60");
```

For most JSON APIs, `Cache-Control: no-store` (private user data) or short `max-age` is fine. Public, read-mostly endpoints can be aggressive cache hits — combine with **CDN** caching.

---

## XIII. HATEOAS AND HYPERMEDIA — WHEN TO CARE

Adding links to responses lets clients discover what they can do next:

```jsonc
{
  "data": { "id": 42, "title": "Buy milk", "done": false },
  "links": {
    "self":       { "href": "/api/v1/todos/42" },
    "complete":   { "href": "/api/v1/todos/42/complete", "method": "POST" }
  }
}
```

Useful for state-machine resources and machine-driven clients. Most JSON APIs skip it because client teams already know the routes. Don't force HATEOAS unless your domain benefits.

---

## XIV. DOCUMENTATION — OPENAPI / SWAGGER

Your API is a contract. Document it.

```bash
npm install swagger-ui-express
```

Hand-write or generate an `openapi.yaml`:

```yaml
openapi: 3.0.3
info: { title: Todo API, version: 1.0.0 }
paths:
  /api/v1/todos:
    get:
      summary: List todos
      responses:
        "200":
          description: OK
```

```js
import swaggerUi from "swagger-ui-express";
import openapi from "../openapi.json" with { type: "json" };
app.use("/docs", swaggerUi.serve, swaggerUi.setup(openapi));
```

Tools like `zod-to-openapi`, `express-zod-api`, `tsoa` can generate the OpenAPI doc from your code so they don't drift apart.

---

## XV. TESTING THE API (PREVIEW)

```bash
npm install --save-dev jest supertest
```

```js
// __tests__/todo.test.js
import request from "supertest";
import app from "../src/app.js";

describe("Todos API", () => {
  it("creates and reads a todo", async () => {
    const created = await request(app)
      .post("/api/v1/todos")
      .send({ title: "Buy milk" })
      .expect(201);

    const got = await request(app).get(`/api/v1/todos/${created.body.data.id}`).expect(200);
    expect(got.body.data.title).toBe("Buy milk");
  });

  it("422 on missing title", async () => {
    await request(app).post("/api/v1/todos").send({}).expect(422);
  });
});
```

Full testing strategy is in **file 08**.

---

## XVI. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Verbs in URLs (`/getUser`) | "REST"-shaped only on the surface | Nouns + HTTP verbs |
| Returning `200` for errors | Clients can't detect failures by status | Use the right 4xx/5xx |
| 200 with stack trace in dev shipped to prod | Info disclosure | Differentiate dev vs prod error responses |
| Trusting client input | Injection, garbage in DB | Validate every body/param/query (zod) |
| Concatenating SQL | SQL injection | Parameterized queries / ORM |
| Returning `passwordHash`, internal flags | Data leak | DTOs / serializers |
| Pagination on huge tables | Slow OFFSET scans | Cursor pagination |
| Allowing arbitrary `sort` values | SQL injection / errors | Allowlist sortable fields |
| No API version | First breaking change destroys clients | Ship `/v1` from day one |
| Lots of fat controllers | Untestable | Push logic into services |
| Calling DB from controller | Can't reuse logic | Repository layer |
| Same schema for create and update | Required fields wrong on PATCH | Separate schemas |
| CORS configured per route, inconsistently | Browser errors | Single CORS middleware up top |

---

## 🧠 KEY TAKEAWAYS

- **Resources are nouns; HTTP verbs are the actions; status codes are the result.** Stop inventing your own.
- Layer your code: **routes → controllers → services → repositories**. Services don't know about HTTP.
- Validate **everything** at the edge with `zod` (or `express-validator`). Use DTOs to control output.
- Pick a pagination style (offset for admin, cursor for feeds) and an explicit sort/filter allowlist.
- Version from `/v1` and deprecate, never break.
- Use Prisma (or your chosen ORM) consistently; never concatenate SQL with user input.
- Document with OpenAPI; test with Supertest; treat your API as a contract.

---

**Prev:** [`04-Express-Fundamentals.md`](./04-Express-Fundamentals.md) · **Next:** [`06-Middleware-And-Error-Handling.md`](./06-Middleware-And-Error-Handling.md) · **Index:** [`00-Index.md`](./00-Index.md)
