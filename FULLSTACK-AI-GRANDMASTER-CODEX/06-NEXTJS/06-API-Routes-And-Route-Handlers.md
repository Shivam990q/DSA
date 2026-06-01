# ▲ 06 — API Routes & Route Handlers

> *"Server Actions cover writes from your own UI. Route Handlers cover everything else — webhooks, third-party clients, mobile apps, public APIs. They are your project's front door for HTTP."*

**Prev:** [`05-Data-Fetching-And-Mutations.md`](./05-Data-Fetching-And-Mutations.md) · **Next:** [`07-Auth-And-Full-Stack-Nextjs.md`](./07-Auth-And-Full-Stack-Nextjs.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT A ROUTE HANDLER IS

A **Route Handler** is an HTTP endpoint that lives inside the App Router. Instead of a `page.tsx` (which renders UI), you create a **`route.ts`** that exports functions named after HTTP methods. The folder path becomes the URL, exactly like pages.

```
app/api/hello/route.ts        →  GET/POST/... /api/hello
app/api/users/route.ts        →  /api/users
app/api/users/[id]/route.ts   →  /api/users/:id
```

```ts
// app/api/hello/route.ts — the simplest possible endpoint.
export async function GET() {
  return Response.json({ message: "Hello from a Route Handler" });
}
```

Visit `http://localhost:3000/api/hello` and you get JSON. No Express, no separate server — it deploys with the rest of your app.

> **Gotcha — `route.ts` and `page.tsx` cannot coexist in the same folder.** A segment is *either* a page *or* an endpoint, not both. `app/users/page.tsx` and `app/users/route.ts` in the same directory is an error. Keep APIs under `app/api/...` by convention to avoid clashes with UI routes.

### When to use Route Handlers vs Server Actions

| Use a **Server Action** when… | Use a **Route Handler** when… |
|-------------------------------|-------------------------------|
| The caller is your own form/UI | The caller is external (webhook, mobile app, cron) |
| It's a mutation tied to a page | You need a stable public URL / REST shape |
| You want progressive enhancement | You need full control of status codes/headers |
| — | You're streaming files, proxying, or handling uploads |

---

## II. HTTP METHODS — ONE EXPORT PER VERB

Export an async function per method you support. Unhandled methods automatically return **405 Method Not Allowed**.

```ts
// app/api/posts/route.ts
import { prisma } from "@/lib/db";

// GET /api/posts — list
export async function GET() {
  const posts = await prisma.post.findMany();
  return Response.json(posts);
}

// POST /api/posts — create
export async function POST(request: Request) {
  const body = await request.json();                 // parse JSON body
  const post = await prisma.post.create({ data: body });
  return Response.json(post, { status: 201 });       // 201 Created
}
```

The supported exports: **`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`**. Each receives the incoming `Request` (and, for dynamic routes, a context object with `params`).

```ts
export async function GET()    { /* read */ }
export async function POST()   { /* create */ }
export async function PUT()    { /* full update */ }
export async function PATCH()  { /* partial update */ }
export async function DELETE() { /* remove */ }
```

---

## III. REQUEST & RESPONSE — WEB STANDARDS

Route Handlers use the **Web Platform** `Request` and `Response` objects (the same APIs as `fetch` and service workers), so what you learn here is transferable beyond Next.js. Next.js also provides `NextRequest`/`NextResponse` subclasses with extra conveniences (cookies, geo, easy redirects/rewrites).

### Reading the request

```ts
// app/api/demo/route.ts
import { NextRequest } from "next/server";

export async function POST(request: NextRequest) {
  // 1) JSON body
  const json = await request.json();

  // 2) Form body (multipart or urlencoded)
  // const form = await request.formData();

  // 3) Query string  →  /api/demo?q=shoes&page=2
  const q = request.nextUrl.searchParams.get("q");
  const page = request.nextUrl.searchParams.get("page");

  // 4) Headers
  const auth = request.headers.get("authorization");

  // 5) Cookies (NextRequest convenience)
  const token = request.cookies.get("token")?.value;

  return Response.json({ json, q, page, hasAuth: Boolean(auth), token });
}
```

### Building the response

```ts
import { NextResponse } from "next/server";

// JSON with a status code
return Response.json({ ok: true }, { status: 200 });

// Plain text / custom headers
return new Response("Not found", {
  status: 404,
  headers: { "Content-Type": "text/plain" },
});

// NextResponse helpers
return NextResponse.json({ data }, { status: 201 });
return NextResponse.redirect(new URL("/login", request.url));

// Set a cookie on the way out
const res = NextResponse.json({ ok: true });
res.cookies.set("session", "abc123", { httpOnly: true, secure: true, path: "/" });
return res;
```

> **Gotcha — `request.json()` throws on an empty or non-JSON body.** A `GET` has no body; calling `.json()` on a malformed `POST` rejects. Wrap parsing in `try/catch` and return a 400 on bad input rather than letting the handler 500.

---

## IV. DYNAMIC ROUTE HANDLERS — READING `params`

Dynamic segments work just like pages. The second argument is a context object whose `params` is a **Promise** in Next 15.

```ts
// app/api/users/[id]/route.ts
import { prisma } from "@/lib/db";

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> },   // Promise in Next 15
) {
  const { id } = await params;
  const user = await prisma.user.findUnique({ where: { id } });

  if (!user) {
    return Response.json({ error: "Not found" }, { status: 404 });
  }
  return Response.json(user);
}

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id } = await params;
  await prisma.user.delete({ where: { id } });
  return new Response(null, { status: 204 });        // 204 No Content
}
```

A full REST resource is just two files:

```
app/api/posts/route.ts         → GET (list), POST (create)
app/api/posts/[id]/route.ts    → GET (one), PUT/PATCH (update), DELETE (remove)
```

---

## V. CACHING & DYNAMIC BEHAVIOR

By default in modern Next.js, Route Handlers are **dynamic** (not cached) — they run on every request, which is usually what an API wants. A `GET` with no dynamic inputs *can* be cached, and you control it with the same segment config as pages.

```ts
// app/api/config/route.ts
export const dynamic = "force-dynamic";   // always run (default for most handlers)
// export const revalidate = 60;          // or cache the GET response for 60s

export async function GET() {
  return Response.json({ time: Date.now() });   // force-dynamic → changes every call
}
```

> **Gotcha — using `request` makes a handler dynamic automatically.** If you read the `Request` (query params, headers, body), the handler can't be statically cached — it depends on per-request input. That's correct behavior; just don't expect a handler that inspects `request` to be cached.

---

## VI. MIDDLEWARE — CODE THAT RUNS BEFORE EVERY REQUEST

**Middleware** runs *before* a request reaches a route, on the Edge by default. Use it for cross-cutting concerns: auth gating, redirects, rewrites, header/cookie manipulation, A/B testing, locale detection. It lives in a single **`middleware.ts`** at the project root (next to `app/`).

```ts
// middleware.ts
import { NextRequest, NextResponse } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Example: gate /dashboard behind a session cookie
  const token = request.cookies.get("session")?.value;
  if (pathname.startsWith("/dashboard") && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", pathname);     // remember where they were going
    return NextResponse.redirect(loginUrl);
  }

  // Otherwise continue, optionally adding a header
  const res = NextResponse.next();
  res.headers.set("x-pathname", pathname);
  return res;
}

// Limit which paths run middleware (perf + clarity).
export const config = {
  matcher: ["/dashboard/:path*", "/api/:path*"],
};
```

What middleware can return:

| Return | Effect |
|--------|--------|
| `NextResponse.next()` | Continue to the route (optionally with modified headers/cookies) |
| `NextResponse.redirect(url)` | Send a 3xx to a different URL |
| `NextResponse.rewrite(url)` | Serve a different URL's content while keeping the address bar URL |
| `NextResponse.json(...)` | Respond immediately (e.g. block with 401) |

> **Gotcha — middleware runs on the Edge runtime by default.** That means **no Node.js APIs** (no `fs`, no native DB drivers) and a limited set of globals. Keep middleware lightweight: check a cookie/JWT, redirect, set headers. Do heavy work (DB lookups, bcrypt) inside the route or a Server Action, not middleware.

> **Gotcha — the `matcher` is your friend.** Without it, middleware runs on *every* request including static assets, which is wasteful and can break things. Scope it with `matcher` to only the paths that need it.

---

## VII. CORS — ALLOWING CROSS-ORIGIN CALLERS

Browsers block cross-origin requests unless the server opts in with CORS headers. For a *public* API consumed by other domains, set them on the response and handle the preflight `OPTIONS` request.

```ts
// app/api/public/route.ts
import { NextResponse } from "next/server";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",                       // or a specific origin
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

// Preflight — browsers send OPTIONS before the real cross-origin request.
export async function OPTIONS() {
  return new Response(null, { status: 204, headers: corsHeaders });
}

export async function GET() {
  return NextResponse.json({ data: "public" }, { headers: corsHeaders });
}
```

You can also set CORS centrally in `middleware.ts` or `next.config.ts` `headers()` if many routes share the policy.

> **Gotcha — `Access-Control-Allow-Origin: *` is fine for truly public, unauthenticated data only.** If your API uses cookies/credentials, you cannot use `*` — you must echo a specific allowed origin and set `Access-Control-Allow-Credentials: true`. Wildcard + credentials is rejected by browsers.

---

## VIII. DATABASE CONNECTIONS IN HANDLERS

Route Handlers (and Server Actions, and Server Components) all need a DB connection. The danger in serverless/dev environments is **connection exhaustion** — creating a new client on every request or every hot-reload. The fix is a **singleton**.

```ts
// lib/db.ts — one Prisma client, reused (survives hot reloads in dev).
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({ log: ["error"] });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

```ts
// app/api/posts/route.ts — import the singleton, don't `new` a client per request.
import { prisma } from "@/lib/db";

export async function GET() {
  const posts = await prisma.post.findMany();
  return Response.json(posts);
}
```

> **Gotcha — serverless + traditional pooled DBs = trouble.** On serverless platforms each invocation may open its own connection, quickly exhausting a Postgres/MySQL connection limit. Use a **pooler** (PgBouncer, Prisma Accelerate, Neon/PlanetScale serverless drivers) or set the route to the Node runtime with a managed pool. This is an infrastructure decision — flag it before going to production.

---

## IX. EDGE vs NODE.JS RUNTIME

Route Handlers and middleware can run in two runtimes:

| | **Node.js** (default for handlers) | **Edge** (default for middleware) |
|---|-----------------------------------|-----------------------------------|
| APIs | Full Node.js (`fs`, native drivers) | Web APIs only (`fetch`, `crypto.subtle`) |
| Cold start | Slower | Near-instant |
| Location | Regional | Globally distributed |
| Good for | DB access, heavy libs, file I/O | Auth checks, redirects, geolocation, lightweight JSON |

```ts
// Opt a handler into the Edge runtime explicitly:
export const runtime = "edge";       // or "nodejs" (default)

export async function GET() {
  return Response.json({ region: process.env.VERCEL_REGION ?? "local" });
}
```

> **Gotcha — most ORMs/DB drivers don't run on the Edge.** Prisma (classic), `pg`, and other Node-native libraries need the Node.js runtime. Only move a handler to the Edge if its dependencies are Edge-compatible (or you use an Edge-ready data client). When in doubt, stay on `nodejs`.

---

## X. A COMPLETE REST RESOURCE

Putting methods, dynamic params, validation, and status codes together:

```ts
// app/api/posts/route.ts
import { prisma } from "@/lib/db";
import { z } from "zod";

const CreatePost = z.object({ title: z.string().min(1), body: z.string().min(1) });

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const take = Number(searchParams.get("limit") ?? 20);
  const posts = await prisma.post.findMany({ take, orderBy: { createdAt: "desc" } });
  return Response.json(posts);
}

export async function POST(request: Request) {
  let data: unknown;
  try {
    data = await request.json();
  } catch {
    return Response.json({ error: "Invalid JSON" }, { status: 400 });
  }

  const parsed = CreatePost.safeParse(data);
  if (!parsed.success) {
    return Response.json({ error: parsed.error.issues }, { status: 422 });
  }

  const post = await prisma.post.create({ data: parsed.data });
  return Response.json(post, { status: 201 });
}
```

```ts
// app/api/posts/[id]/route.ts
import { prisma } from "@/lib/db";

export async function GET(_: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const post = await prisma.post.findUnique({ where: { id } });
  return post
    ? Response.json(post)
    : Response.json({ error: "Not found" }, { status: 404 });
}

export async function DELETE(_: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  await prisma.post.delete({ where: { id } });
  return new Response(null, { status: 204 });
}
```

---

## XI. PAGES ROUTER CONTRAST

The Pages Router put APIs in `pages/api/` with a single `(req, res)` handler (Express-style), not per-method exports:

```ts
// pages/api/posts.ts — LEGACY. For recognition only.
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "GET") return res.status(200).json({ posts: [] });
  if (req.method === "POST") return res.status(201).json(req.body);
  res.setHeader("Allow", ["GET", "POST"]).status(405).end();
}
```

| App Router (`route.ts`) | Pages Router (`pages/api`) |
|-------------------------|----------------------------|
| One export per HTTP method | One handler, branch on `req.method` |
| Web `Request`/`Response` | Node `req`/`res` (Express-like) |
| `Response.json(...)` | `res.status().json()` |
| Edge or Node runtime | Node only |

---

## XII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `page.tsx` + `route.ts` in one folder | Build error | One segment is a page OR an endpoint, not both |
| Calling `request.json()` on empty/bad body | 500 error | `try/catch` parsing, return 400 |
| Reading `params` synchronously in Next 15 | Type/runtime error | `await params` (it's a Promise) |
| Heavy work or DB calls in middleware | Edge runtime errors / slow | Keep middleware light; do DB work in the route |
| No `matcher` on middleware | Runs on every asset, breaks/slows | Scope with `config.matcher` |
| `new PrismaClient()` per request | Connection exhaustion | Use a singleton in `lib/db.ts` |
| Edge runtime + Node-only driver | "module not found" / runtime crash | Use `runtime = "nodejs"` or an Edge-ready client |
| `Allow-Origin: *` with credentials | Browser blocks the response | Echo a specific origin + `Allow-Credentials: true` |
| Forgetting the `OPTIONS` handler | CORS preflight fails | Export `OPTIONS` returning the CORS headers |

---

## 🧠 KEY TAKEAWAYS

- A **Route Handler** is `app/.../route.ts` exporting one async function per HTTP method (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, ...). The folder path is the URL.
- Use **Server Actions** for writes from your own UI; use **Route Handlers** for external callers, public APIs, webhooks, and full control of status/headers.
- Handlers use the Web **`Request`/`Response`** standard, plus Next's `NextRequest`/`NextResponse` for cookies, redirects, and rewrites. Dynamic `params` is a Promise in Next 15.
- **Middleware** (`middleware.ts`) runs before requests on the Edge — ideal for auth gating, redirects, and headers; keep it light and scope it with `matcher`.
- Handle **CORS** by setting `Access-Control-*` headers and an `OPTIONS` preflight; never combine `*` with credentials.
- Reuse a **singleton DB client** to avoid connection exhaustion; choose the **Node.js runtime** for Node-native ORMs and the **Edge** only for lightweight, Web-API-only work.

---

**Prev:** [`05-Data-Fetching-And-Mutations.md`](./05-Data-Fetching-And-Mutations.md) · **Next:** [`07-Auth-And-Full-Stack-Nextjs.md`](./07-Auth-And-Full-Stack-Nextjs.md) · **Index:** [`00-Index.md`](./00-Index.md)
