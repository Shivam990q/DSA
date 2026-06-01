# ▲ Next.js

> *"React gives you components. Next.js gives you an application — routing, rendering, data, and a server — all wired together with sane defaults. It is the framework that turns a UI library into a product."*

> **Section 06 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module takes you from `npx create-next-app` to a deployed, full-stack application with server components, server actions, authentication, a database, and a global CDN behind it.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- **Why Next.js exists** — the concrete problems (SEO, performance, routing, full-stack glue) it solves that plain React leaves to you
- The **App Router** — file-based routing, dynamic segments, route groups, **parallel & intercepting routes**, nested layouts, and the special files (`page`, `layout`, `loading`, `error`, `not-found`)
- The **React Server Components (RSC)** model — what runs on the server, what ships to the browser, and the `"use client"` / `"use server"` boundaries that separate them
- **Rendering strategies** — static (SSG), dynamic (SSR), incremental (ISR), streaming, and **Partial Prerendering (PPR)** — and exactly when each one fires
- The **four caching layers** — request memoization, the Data Cache, the Full Route Cache, and the client-side Router Cache — and how to invalidate each
- **Data fetching and mutations** — fetching in server components, the extended `fetch` cache, and **Server Actions** for writes without hand-rolling an API
- **Route Handlers** — building real HTTP API endpoints (`GET`/`POST`/...) inside the same project, plus **middleware**
- **Authentication** — Auth.js (NextAuth), sessions, and middleware-protected routes
- **Shipping it** — environment variables, the Metadata API for SEO, Image/Font optimization, and deploying to Vercel or self-hosting

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file assumes the ones before it. The ⭐ files are the highest-leverage — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here — overview, roadmap, setup | — |
| 01 | [`01-Why-Nextjs-And-Setup.md`](./01-Why-Nextjs-And-Setup.md) | What Next.js is, the problems it solves, App vs Pages Router, project structure, file conventions, dev/build/start | Core |
| 02 | [`02-App-Router-And-Routing.md`](./02-App-Router-And-Routing.md) | File-based routing, dynamic & catch-all segments, route groups, **parallel & intercepting routes**, nested layouts, `loading`/`error`/`not-found`, `<Link>`, `useRouter`/`usePathname`/`useParams` | ⭐ |
| 03 | [`03-Server-And-Client-Components.md`](./03-Server-And-Client-Components.md) | The RSC model, server vs client components, `"use client"`, composition rules, the serialization boundary, server-only code | ⭐ |
| 04 | [`04-Rendering-Strategies-SSR-SSG-ISR.md`](./04-Rendering-Strategies-SSR-SSG-ISR.md) | SSG, SSR, ISR, dynamic vs static rendering, the four caching layers, `revalidate`, `generateStaticParams`, streaming, Suspense & **PPR** | ⭐ |
| 05 | [`05-Data-Fetching-And-Mutations.md`](./05-Data-Fetching-And-Mutations.md) | Fetching in server components, `fetch` caching/revalidation, **Server Actions**, forms, `revalidatePath`/`revalidateTag`, `useFormStatus`/`useOptimistic`, loading/error UX | ⭐ |
| 06 | [`06-API-Routes-And-Route-Handlers.md`](./06-API-Routes-And-Route-Handlers.md) | Route Handlers (`app/api/.../route.ts`), HTTP methods, `Request`/`Response`, dynamic handlers, **middleware**, CORS, DB connections | Core |
| 07 | [`07-Auth-And-Full-Stack-Nextjs.md`](./07-Auth-And-Full-Stack-Nextjs.md) | Auth.js/NextAuth, sessions, middleware-protected routes, a full feature end-to-end (DB + actions + UI), environment variables | ⭐ |
| 08 | [`08-Optimization-And-Deployment.md`](./08-Optimization-And-Deployment.md) | Metadata API & SEO, `<Image>`/`next/font` optimization, performance, deploying to Vercel & self-hosting, monitoring | Core |

---

## 🗺️ COMPLETE NEXT.JS ROADMAP (coverage checklist)

> A roadmap.sh-style map of **everything** this section covers. Reading this codex front to back covers every item below. Each row points to the file where the concept is taught. Tick them off as you master them.

### 1 — Foundations

- [ ] What Next.js is & the problems it solves (SEO, perf, routing, full-stack) → **01**
- [ ] App Router vs Pages Router (and why App Router) → **01** (contrast), **all**
- [ ] Project structure & the `@/*` import alias → **01**
- [ ] File conventions: `page`, `layout`, `loading`, `error`, `not-found`, `template`, `route`, `default` → **01**, **02**
- [ ] CLI: `next dev` / `next build` / `next start` / `next lint` + reading the route table → **01**
- [ ] TypeScript throughout (`.tsx`/`.ts`, typed `params`/`searchParams`, `Metadata`) → **01–08**

### 2 — Routing (App Router)

- [ ] File-based routing — folders are routes, `page.tsx` makes them public → **02**
- [ ] Dynamic segments `[id]` and nested dynamic segments → **02**
- [ ] Catch-all `[...slug]` and optional catch-all `[[...slug]]` → **02**
- [ ] Query strings via `searchParams` → **02**
- [ ] Route groups `(group)` — organize without affecting the URL → **02**
- [ ] **Parallel routes** `@slot` (simultaneous independent panes) → **02**
- [ ] **Intercepting routes** `(.)`, `(..)`, `(...)` (modals over a route) → **02**
- [ ] Layouts & nested layouts (persistent UI) → **02**
- [ ] `template.tsx` (re-mounting layout) → **02**
- [ ] `loading.tsx` (Suspense loading UI) → **02**, **04**
- [ ] `error.tsx` + `global-error.tsx` (error boundaries) → **02**
- [ ] `not-found.tsx` + `notFound()` → **02**
- [ ] Navigation with `<Link>` (prefetch, client-side nav) → **02**
- [ ] Programmatic nav & hooks: `useRouter`, `usePathname`, `useSearchParams`, `useParams`, `redirect()` → **02**

### 3 — Server & Client Components

- [ ] The RSC model — server is the default → **03**
- [ ] Server Components (async, DB access, secrets, zero JS) → **03**
- [ ] Client Components & the `"use client"` directive → **03**
- [ ] Composition rules (server renders client; client receives server via `children`) → **03**
- [ ] The serialization boundary (what props can cross) → **03**
- [ ] `server-only` / `client-only` guards → **03**
- [ ] Hydration & avoiding hydration mismatches → **03**
- [ ] `"use server"` directive (Server Actions) → **05**

### 4 — Rendering & Caching

- [ ] Static rendering / SSG → **04**
- [ ] Dynamic rendering / SSR (and what triggers it) → **04**
- [ ] Incremental Static Regeneration (ISR) with `revalidate` → **04**
- [ ] `generateStaticParams` (pre-render dynamic routes) → **04**
- [ ] Route segment config (`dynamic`, `revalidate`, `fetchCache`, `runtime`) → **04**
- [ ] Streaming with Suspense → **04**
- [ ] **Partial Prerendering (PPR)** → **04**
- [ ] **Caching layer 1: Request Memoization** → **04**
- [ ] **Caching layer 2: Data Cache** → **04**
- [ ] **Caching layer 3: Full Route Cache** → **04**
- [ ] **Caching layer 4: Router Cache (client-side)** → **04**

### 5 — Data Fetching & Mutations

- [ ] Fetching in Server Components (`async`/`await`, no `useEffect`) → **05**
- [ ] `fetch` caching options (`force-cache`, `no-store`, `next.revalidate`, `next.tags`) → **05**
- [ ] Parallel vs sequential fetching (avoiding waterfalls) → **05**
- [ ] Fetching from an ORM/DB directly → **05**
- [ ] **Server Actions** (`"use server"`) for mutations → **05**
- [ ] Forms with the `action` prop & progressive enhancement → **05**
- [ ] `revalidatePath` / `revalidateTag` → **05**
- [ ] `redirect()` inside actions → **05**
- [ ] `useFormStatus`, `useActionState`, `useOptimistic` → **05**
- [ ] Loading & error UX for mutations → **05**

### 6 — API & Edge

- [ ] Route Handlers `app/api/.../route.ts` → **06**
- [ ] HTTP methods (`GET`/`POST`/`PUT`/`PATCH`/`DELETE`) → **06**
- [ ] Web `Request`/`Response` & `NextRequest`/`NextResponse` → **06**
- [ ] Dynamic handlers, reading params, query, body, headers, cookies → **06**
- [ ] **Middleware** (`middleware.ts`) — redirects, rewrites, headers → **06**
- [ ] CORS handling → **06**
- [ ] Edge vs Node.js runtime → **06**
- [ ] Database connection patterns (pooling, singletons) → **06**, **07**

### 7 — Auth & Full-Stack

- [ ] Authentication with Auth.js (NextAuth v5) → **07**
- [ ] Sessions (JWT vs database sessions) → **07**
- [ ] OAuth & credentials providers → **07**
- [ ] Protecting routes via middleware → **07**
- [ ] Reading the session in server components & actions → **07**
- [ ] Authorization (role checks) → **07**
- [ ] A full feature end-to-end (DB schema + Server Action + UI) → **07**
- [ ] Environment variables (`NEXT_PUBLIC_`, `.env.local`, server secrets) → **07**

### 8 — Optimization, SEO & Deployment

- [ ] Metadata API (static & `generateMetadata`) → **08**
- [ ] SEO: title templates, Open Graph, `sitemap.ts`, `robots.ts`, JSON-LD → **08**
- [ ] `<Image>` optimization → **08**
- [ ] `next/font` optimization → **08**
- [ ] `<Script>` and third-party scripts → **08**
- [ ] Bundle analysis & performance (Core Web Vitals) → **08**
- [ ] Deploying to Vercel → **08**
- [ ] Self-hosting (Node server, Docker, `output: "standalone"`) → **08**
- [ ] Monitoring & analytics → **08**

### 9 — Pages Router (contrast only)

- [ ] `pages/` directory & `_app`/`_document` → **01** (contrast), **08** (contrast)
- [ ] `getStaticProps` / `getServerSideProps` / `getStaticPaths` → **04** (contrast table)
- [ ] `pages/api` API routes → **06** (contrast table)

---

## 🛠️ SETUP — SCAFFOLD A PROJECT

Next.js is a Node.js framework. You need **Node.js 18.18+** (the App Router and modern features assume a recent LTS). Verify first:

```bash
node -v    # v18.18+ or v20+ recommended
npm -v
```

### Create the app

The official scaffolder wires up TypeScript, ESLint, Tailwind, and the App Router for you:

```bash
npx create-next-app@latest my-app
```

It asks a few questions. The grandmaster defaults for this section:

```
✔ Would you like to use TypeScript?            … Yes
✔ Would you like to use ESLint?                … Yes
✔ Would you like to use Tailwind CSS?          … Yes
✔ Would you like your code inside a `src/` directory? … Yes
✔ Would you like to use App Router? (recommended)     … Yes
✔ Would you like to customize the import alias (@/*)? … No (keep @/*)
```

Then run the dev server:

```bash
cd my-app
npm run dev          # starts on http://localhost:3000 with hot reload
```

Open `http://localhost:3000` and you have a live app. Edit `src/app/page.tsx`, save, and the browser updates instantly.

### The commands you will live in

| Command | What it does |
|---------|--------------|
| `npm run dev` | Development server with Fast Refresh (hot reload). Use this 99% of the time. |
| `npm run build` | Production build — compiles, bundles, and pre-renders static pages. |
| `npm run start` | Serves the production build locally (test before deploy). |
| `npm run lint` | Runs ESLint over the project. |

> **Gotcha — dev ≠ production.** The dev server renders everything dynamically and skips most caching so your edits show instantly. Caching, static generation, and real performance only appear after `npm run build && npm run start`. Always test rendering behavior against a production build.

---

## ✅ PREREQUISITES

Next.js is **React with a framework around it**. Do not start here cold.

- **[`05-REACT`](../05-REACT/)** — components, props, JSX, hooks (`useState`, `useEffect`, `useContext`), and lists/keys. This section assumes all of it. If `useState` and "lifting state up" are not second nature, finish React first.
- **[`03-TYPESCRIPT`](../03-TYPESCRIPT/)** — every example here is TypeScript (`.tsx`/`.ts`). You should be comfortable with types, interfaces, and generics.
- **[`02-JAVASCRIPT-MASTERY`](../02-JAVASCRIPT-MASTERY/)** — async/await, promises, modules, and the `fetch` API.
- **[`01-WEB-FOUNDATIONS`](../01-WEB-FOUNDATIONS/)** — HTTP methods, status codes, requests/responses, and what "the server" actually is.

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Build alongside.** Keep one `create-next-app` project open and recreate every example in it. Reading Next.js without running it teaches you almost nothing.
2. **Watch the boundary.** The single hardest idea is *server vs client components*. Every time you write a component, ask "where does this run?" File 03 is the hinge of the whole section.
3. **Verify against a build.** When a page behaves unexpectedly, run `npm run build` and read the route table it prints (`○ Static`, `ƒ Dynamic`). It tells you exactly how each route is rendered.
4. **Ship something small early.** Deploy a two-page app to Vercel after file 02. Deploying is a skill; practice it before the stakes are high.

---

## 🔗 RELATED SECTIONS

- Built directly on [`05-REACT`](../05-REACT/) — Next.js *is* React plus routing, rendering, and a server.
- Pairs with [`08-SQL-DATABASES`](../08-SQL-DATABASES/) and [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/) — server components and server actions talk to these directly.
- [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/) is the alternative/companion backend; Route Handlers (file 06) are Next.js's built-in answer to Express.
- [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/) goes deeper on auth, testing, CI/CD, and system design for what you build here.

---

## 📎 DEEP REFERENCES

- **Official docs (the source of truth):** [nextjs.org/docs](https://nextjs.org/docs) — the App Router docs are excellent and version-accurate.
- **Learn course:** [nextjs.org/learn](https://nextjs.org/learn) — the official hands-on dashboard tutorial.
- **React docs (Server Components):** [react.dev](https://react.dev) — the RSC model originates in React itself.
- **Caching deep dive:** [nextjs.org/docs/app/building-your-application/caching](https://nextjs.org/docs/app/building-your-application/caching) — the canonical reference for the four caching layers.
- **Auth.js (NextAuth):** [authjs.dev](https://authjs.dev) — the auth library used in file 07.
- **Deployment:** [vercel.com/docs](https://vercel.com/docs) — Vercel is built by the Next.js team; deploys are first-class.

> **Version note.** This section targets **Next.js 14 and 15** with the **App Router**. The older **Pages Router** (`pages/` directory, `getServerSideProps`, `getStaticProps`) is mentioned only for contrast — it still works and ships in millions of apps, but all new work should use the App Router.

---

**→ Begin:** [`01-Why-Nextjs-And-Setup.md`](./01-Why-Nextjs-And-Setup.md) | Back to [`../README.md`](../README.md)
