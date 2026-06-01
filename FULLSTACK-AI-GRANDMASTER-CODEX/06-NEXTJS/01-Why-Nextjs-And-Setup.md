# ▲ 01 — Why Next.js & Setup

> *"A library hands you bricks. A framework hands you a blueprint, a foundation, and the plumbing already run. Next.js is the framework that lets React build whole buildings."*

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-App-Router-And-Routing.md`](./02-App-Router-And-Routing.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT NEXT.JS ACTUALLY IS

Next.js is a **React framework**. React itself is "just" a library for building user interfaces out of components — it renders UI and manages state, and that is *all* it promises. The moment you try to ship a real app, React leaves a long list of decisions to you:

- How does the URL `/blog/hello` map to a component? (React has no router.)
- How do you render pages on a server so search engines and slow phones see content fast? (React runs in the browser by default.)
- Where does data come from, and how is it cached?
- How do you build an API endpoint, bundle assets, optimize images, and split code?

**Next.js answers all of those with conventions and built-in machinery.** It is the most widely used production React framework, built and maintained by **Vercel**, with the React core team collaborating closely (Server Components were designed by React and shipped first in Next.js).

```
            ┌─────────────────────────────────────────┐
            │                 NEXT.JS                   │
            │  routing · rendering · data · bundling ·  │
            │  server · image opt · caching · API       │
            │   ┌─────────────────────────────────┐     │
            │   │             REACT               │     │
            │   │   components · state · hooks     │     │
            │   └─────────────────────────────────┘     │
            └─────────────────────────────────────────┘
```

You still write React. Next.js wraps it with everything a React app needs to become a product.

> **Mental model.** If React is an *engine*, Next.js is the *car* — chassis, wheels, steering, and dashboard built around the engine so you can actually drive somewhere.

---

## II. THE PROBLEMS NEXT.JS SOLVES

To appreciate the framework, look at what a plain React app (e.g. one made with Vite or Create React App) struggles with.

### Problem 1 — SEO and the "blank page" of client-side rendering

A vanilla React app ships an almost-empty HTML shell plus a big JavaScript bundle. The browser downloads the JS, runs it, *then* renders content:

```html
<!-- What a search-engine crawler or a slow phone first receives from a plain SPA -->
<!DOCTYPE html>
<html>
  <body>
    <div id="root"></div>          <!-- EMPTY. No content yet. -->
    <script src="/bundle.js"></script>
  </body>
</html>
```

The content does not exist until JavaScript runs. Crawlers that do not execute JS well, link-preview bots, and users on slow connections see nothing useful. This hurts **SEO** and **perceived performance**.

Next.js renders HTML **on the server** so the very first response already contains the content:

```html
<!-- What Next.js sends — content is THERE on first byte -->
<!DOCTYPE html>
<html>
  <body>
    <main>
      <h1>Welcome to my blog</h1>
      <article>The full post text, already rendered...</article>
    </main>
    <script src="/_next/static/chunks/main.js"></script> <!-- hydrates for interactivity -->
  </body>
</html>
```

### Problem 2 — Performance

Next.js does a pile of optimization work automatically: automatic **code splitting** (each route only ships the JS it needs), the `<Image>` component (automatic resizing, lazy loading, modern formats), font optimization, prefetching of linked routes, and aggressive caching. Most of this is opt-out, not opt-in.

### Problem 3 — Routing

React has no built-in router; you reach for a third-party library and configure routes by hand. Next.js makes the **file system the router**: a file at `app/blog/page.tsx` *is* the `/blog` route. No configuration.

### Problem 4 — Full-stack in one project

With plain React you build a frontend, then separately build a backend (Express, etc.) to serve data and handle writes. Next.js lets you write **server code and client code in the same project** — server components, server actions, and route handlers all live next to your UI and deploy together.

| Concern | Plain React (SPA) | Next.js |
|---------|-------------------|---------|
| Routing | Add a library, configure manually | File-based, zero config |
| Initial render | Blank shell, then JS renders | Server-rendered HTML on first byte |
| SEO | Poor by default | Strong by default |
| Data fetching | Client-side `useEffect` waterfalls | Fetch on the server, before render |
| API / backend | Separate project | Built in (route handlers, server actions) |
| Image / font optimization | Manual | Built in |
| Code splitting | Manual config | Automatic per route |

> **Gotcha — "Next.js is always faster" is wrong.** Next.js is not magic. A misconfigured Next.js app can be slower than a tuned SPA. What Next.js gives you is *better defaults and more rendering options*. You still have to use them correctly — which is the rest of this section.

---

## III. APP ROUTER vs PAGES ROUTER

Next.js has **two** routing systems. You must know which one a tutorial or codebase uses, because they are different enough to confuse you.

| | **App Router** (`app/`) | **Pages Router** (`pages/`) |
|---|---|---|
| Introduced | Next.js 13 (stable in 13.4) | Original (since 2016) |
| Status | **The future. Use this.** | Legacy, still supported |
| Components | Server Components by default | Client Components only |
| Data fetching | `async` components + `fetch` | `getServerSideProps`, `getStaticProps` |
| Layouts | Nested `layout.tsx`, persistent | Single `_app.tsx` / `_document.tsx` |
| Loading UI | `loading.tsx` + Suspense streaming | Manual |
| Mutations | Server Actions | API routes only |

```
app/                          pages/
├── layout.tsx                ├── _app.tsx
├── page.tsx        → /       ├── index.tsx        → /
├── about/                    ├── about.tsx        → /about
│   └── page.tsx    → /about  └── blog/
└── blog/                         └── [slug].tsx   → /blog/:slug
    └── [slug]/
        └── page.tsx → /blog/:slug
```

**This entire section teaches the App Router.** The Pages Router appears only in contrast tables. If you join a team with an existing `pages/` directory, the concepts transfer, but write all *new* features in `app/`.

> **Gotcha — they can coexist.** A single project can have both an `app/` and a `pages/` directory (this is how teams migrate incrementally). If a route exists in both, `app/` wins. Do not let a half-migrated repo confuse you about which file is serving a URL.

---

## IV. PROJECT STRUCTURE

After `npx create-next-app@latest my-app` with the recommended options, you get roughly this:

```
my-app/
├── src/
│   └── app/                  ← the App Router lives here
│       ├── layout.tsx        ← root layout (wraps EVERY page) — required
│       ├── page.tsx          ← the homepage, route "/"
│       ├── globals.css       ← global styles
│       └── favicon.ico
├── public/                   ← static assets served as-is (/logo.png → public/logo.png)
├── next.config.ts            ← Next.js configuration
├── tsconfig.json             ← TypeScript config (includes the @/* path alias)
├── package.json
├── eslint.config.mjs
└── tailwind.config.ts        ← (if you chose Tailwind)
```

Key points:

- **`src/app/`** is the heart. Every route is a folder here.
- **`public/`** holds files served at the root path. `public/robots.txt` is reachable at `/robots.txt`.
- The **`@/*` import alias** (configured in `tsconfig.json`) lets you write `import { Button } from "@/components/Button"` instead of `../../../components/Button`. Use it everywhere.

> **Gotcha — `src/` is optional.** If you did not choose the `src/` directory, your app folder is `app/` at the project root instead of `src/app/`. Both are valid; just know which one you have. This section writes `app/...` for brevity — prefix with `src/` if you chose it.

---

## V. FILE CONVENTIONS — THE SPECIAL FILENAMES

The App Router gives **specific filenames** special meaning inside any route folder. This is the vocabulary of the whole framework — learn it now, master it in file 02.

| File | Role | Runs on |
|------|------|---------|
| `page.tsx` | The unique UI for a route. **Makes the route publicly accessible.** | Server (default) |
| `layout.tsx` | Shared UI that *wraps* a page and its children; persists across navigation. | Server (default) |
| `loading.tsx` | Instant loading UI shown via Suspense while the page loads. | Server |
| `error.tsx` | Error boundary UI for the segment. **Must be a Client Component.** | Client |
| `not-found.tsx` | UI for `notFound()` calls and unmatched URLs. | Server |
| `template.tsx` | Like `layout`, but re-mounts on every navigation (rarely needed). | Server |
| `route.ts` | An API endpoint (Route Handler) instead of a page. | Server |

A single route folder can contain several of these working together:

```
app/dashboard/
├── layout.tsx     ← persistent shell (sidebar, nav) around everything below
├── page.tsx       ← the /dashboard content
├── loading.tsx    ← shown while page.tsx's data loads
└── error.tsx      ← catches errors thrown while rendering this segment
```

Here is the minimum viable App Router — a root layout plus a homepage. **The root `layout.tsx` is required** and must render `<html>` and `<body>`:

```tsx
// app/layout.tsx — wraps EVERY page in the app. Required at the root.
import type { Metadata } from "next";
import "./globals.css";

// Static metadata for SEO — Next.js turns this into <head> tags (more in file 07)
export const metadata: Metadata = {
  title: "My App",
  description: "Built with the Next.js App Router",
};

export default function RootLayout({
  children,                                   // the active page is injected here
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

```tsx
// app/page.tsx — the route "/". A Server Component by default.
export default function HomePage() {
  return (
    <main>
      <h1>Welcome to my app</h1>
      <p>This HTML was rendered on the server.</p>
    </main>
  );
}
```

> **Gotcha — a folder without `page.tsx` is not a route.** `app/settings/layout.tsx` alone does **not** create a `/settings` URL. The folder only becomes a navigable route when it contains a `page.tsx` (or `route.ts`). Folders without one are used purely for organization or to hold a shared layout.

---

## VI. RUNNING THE APP — DEV, BUILD, START

The `package.json` scripts wrap the Next.js CLI:

```json
{
  "scripts": {
    "dev": "next dev",       // development server, Fast Refresh
    "build": "next build",   // production build
    "start": "next start",   // serve the production build
    "lint": "next lint"      // ESLint
  }
}
```

### `next dev` — your daily driver

```bash
npm run dev
# ▲ Next.js 15.x
# - Local:   http://localhost:3000
# ✓ Ready in 1.2s
```

Fast Refresh re-renders on save while preserving component state where it can. The dev server renders dynamically and skips most caching — by design, so you see edits instantly.

### `next build` — the production build (and the route map)

```bash
npm run build
```

The build output is one of the most useful diagnostics in Next.js. It prints a table of every route and **how it is rendered**:

```
Route (app)                     Size     First Load JS
┌ ○ /                           1.2 kB         95 kB
├ ○ /about                      0.8 kB         94 kB
├ ƒ /dashboard                  2.1 kB         98 kB
└ ● /blog/[slug]                1.5 kB         96 kB
    ├ /blog/hello-world
    └ /blog/second-post

○  (Static)   prerendered as static HTML
●  (SSG)      prerendered with generateStaticParams
ƒ  (Dynamic)  server-rendered on demand
```

Read this every time you are unsure how a route renders. The legend (`○` static, `●` SSG, `ƒ` dynamic) tells you exactly what file 04 will teach you to control.

### `next start` — serve production locally

```bash
npm run build && npm run start   # serves the optimized build on :3000
```

> **Gotcha — never benchmark `next dev`.** The dev server is intentionally slow and uncached for a good developer experience. Caching, static generation, and true performance only exist in a production build. If you want to *see* how your app behaves in production, you must `build` then `start`.

---

## VII. A QUICK TWO-PAGE APP

Let's prove the file-based router works. Create two routes with a shared header.

```tsx
// app/layout.tsx — shared shell with navigation across all pages
import Link from "next/link";
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header>
          {/* <Link> does client-side navigation + prefetching — more in file 02 */}
          <nav>
            <Link href="/">Home</Link> | <Link href="/about">About</Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

```tsx
// app/page.tsx → "/"
export default function HomePage() {
  return <h1>Home</h1>;
}
```

```tsx
// app/about/page.tsx → "/about"  (just by creating the folder + file!)
export default function AboutPage() {
  return <h1>About us</h1>;
}
```

Run `npm run dev`, open `http://localhost:3000`, and click between Home and About. You created two routes and navigation with **zero router configuration** — the file system *is* the config.

---

## VIII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Folder without `page.tsx` | URL 404s even though the folder exists | Every route needs a `page.tsx` (or `route.ts`) |
| Editing root `layout.tsx` and removing `<html>`/`<body>` | App crashes / blank render | Root layout must render `<html>` and `<body>` |
| Benchmarking `next dev` | "Next.js is slow!" | Measure `next build` + `next start` instead |
| Mixing App and Pages router blindly | Confusing duplicate routes | Know which directory serves the URL; `app/` wins |
| Forgetting `src/` prefix | "File not found" / wrong paths | Check whether you chose the `src/` option |
| Importing with deep `../../..` paths | Brittle, hard to refactor | Use the `@/*` alias |
| Expecting `useState` in `page.tsx` to work | Error about hooks/`"use client"` | `page.tsx` is a Server Component — see file 03 |
| Putting secrets in client code | Secrets leak to the browser | Server-only code & non-`NEXT_PUBLIC_` env vars (file 07) |

---

## 🧠 KEY TAKEAWAYS

- Next.js is a **React framework**: it adds routing, server rendering, data fetching, an API layer, and optimization on top of React's component model.
- It solves four concrete problems plain React leaves open: **SEO/initial render**, **performance**, **routing**, and **full-stack glue**.
- There are two routers; you use the **App Router** (`app/`). The **Pages Router** (`pages/`) is legacy and shown only for contrast.
- The **file system is the router**. A `page.tsx` inside a folder creates that route — no config.
- Special filenames (`page`, `layout`, `loading`, `error`, `not-found`, `route`) are the framework's vocabulary; learn them now.
- Three commands run everything: `next dev` (daily), `next build` (production + the route map), `next start` (serve production).
- **Never judge performance from `next dev`** — caching and static generation only exist in a real build.

---

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-App-Router-And-Routing.md`](./02-App-Router-And-Routing.md) · **Index:** [`00-Index.md`](./00-Index.md)
