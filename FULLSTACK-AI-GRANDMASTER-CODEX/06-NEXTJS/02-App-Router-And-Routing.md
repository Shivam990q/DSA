# ▲ 02 — App Router & Routing

> *"The URL is the most important API your app has. Next.js makes your folder structure the URL — so the shape of your code becomes the shape of your product."*

**Prev:** [`01-Why-Nextjs-And-Setup.md`](./01-Why-Nextjs-And-Setup.md) · **Next:** [`03-Server-And-Client-Components.md`](./03-Server-And-Client-Components.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. FILE-BASED ROUTING — THE CORE IDEA

In the App Router, **folders define routes** and a special **`page.tsx`** file makes a route publicly accessible. The path of folders from `app/` to a `page.tsx` *is* the URL.

```
app/
├── page.tsx                    →  /
├── about/
│   └── page.tsx                →  /about
├── blog/
│   ├── page.tsx                →  /blog
│   └── archive/
│       └── page.tsx            →  /blog/archive
└── dashboard/
    └── settings/
        └── page.tsx            →  /dashboard/settings
```

Two rules cover 90% of routing:

1. **A folder = a URL segment.** `app/dashboard/settings/` maps to `/dashboard/settings`.
2. **`page.tsx` = the page itself.** Without it, the folder is not a navigable route.

```tsx
// app/about/page.tsx → renders at /about
export default function AboutPage() {
  return <h1>About</h1>;
}
```

Files *other* than the special ones (`page`, `layout`, `loading`, `error`, `not-found`, `route`, `template`, `default`) are **not** routed. You can freely keep `app/blog/_components/PostCard.tsx` or `app/blog/utils.ts` next to your routes — they are ignored by the router and just normal modules.

> **Gotcha — colocation is encouraged.** You can put components, tests, and helpers right inside route folders. Only the reserved filenames create routes. A folder prefixed with `_` (e.g. `_components`) is a "private folder" — explicitly opted out of routing.

---

## II. DYNAMIC SEGMENTS — `[param]`

Most apps need routes like `/blog/my-first-post` where the last part varies. Wrap a folder name in **square brackets** to make it a dynamic segment.

```
app/blog/[slug]/page.tsx   →  /blog/anything  (slug = "anything")
```

The matched value arrives in the `params` prop. In modern Next.js (15+), `params` is a **Promise** you `await`:

```tsx
// app/blog/[slug]/page.tsx
// In Next.js 15, params is a Promise — await it. (In 14 it was a plain object.)
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;             // e.g. "my-first-post"
  return <h1>Post: {slug}</h1>;
}
```

Multiple dynamic segments nest naturally:

```
app/shop/[category]/[product]/page.tsx  →  /shop/shoes/running-x
```

```tsx
// app/shop/[category]/[product]/page.tsx
export default async function Product({
  params,
}: {
  params: Promise<{ category: string; product: string }>;
}) {
  const { category, product } = await params;
  return <h1>{category} → {product}</h1>;
}
```

> **Gotcha — `params` is async in Next 15.** Next.js 15 made `params` (and `searchParams`) Promises so the framework can stream more aggressively. If you are on 14 and upgrade, you must add `await`. On 14 you can read them synchronously: `params.slug`. This section uses the 15 (`await`) form.

### Query strings — `searchParams`

Query parameters (`?page=2&sort=asc`) are **not** part of the path, so they do not create folders. They arrive via `searchParams` on the page:

```tsx
// app/products/page.tsx  →  /products?page=2&sort=asc
export default async function Products({
  searchParams,
}: {
  searchParams: Promise<{ page?: string; sort?: string }>;
}) {
  const { page = "1", sort = "asc" } = await searchParams;
  return <p>Page {page}, sorted {sort}</p>;
}
```

> **Gotcha — reading `searchParams` opts a route into dynamic rendering.** Because query strings are only known per-request, any page that reads `searchParams` cannot be statically pre-rendered. That is fine and expected, but know that it flips the route to dynamic (file 04).

---

## III. CATCH-ALL AND OPTIONAL SEGMENTS

Sometimes one route should handle an arbitrary depth of path, e.g. documentation pages like `/docs/getting-started/install/windows`.

| Pattern | Folder | Matches | `params` |
|---------|--------|---------|----------|
| Dynamic | `[slug]` | `/blog/a` | `{ slug: "a" }` |
| Catch-all | `[...slug]` | `/docs/a/b/c` | `{ slug: ["a","b","c"] }` |
| Optional catch-all | `[[...slug]]` | `/docs` **and** `/docs/a/b` | `{ slug: undefined }` or `{ slug: ["a","b"] }` |

```tsx
// app/docs/[...slug]/page.tsx
// Catch-all: collects every remaining segment into an array.
export default async function Docs({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;            // ["getting-started", "install", "windows"]
  return <p>Path depth: {slug.length} → {slug.join(" / ")}</p>;
}
```

The difference between `[...slug]` and `[[...slug]]` is whether the **base path with no extra segments** also matches. `[...slug]` requires at least one segment (`/docs/x`); `[[...slug]]` also matches `/docs` itself.

---

## IV. ROUTE GROUPS — `(folder)`

A folder wrapped in **parentheses** is a **route group**. It organizes files **without adding a URL segment**. This is how you share a layout among some routes, or split your app into sections, without polluting the URL.

```
app/
├── (marketing)/
│   ├── layout.tsx          ← layout for marketing pages only
│   ├── page.tsx            →  /          (NOT /marketing)
│   └── about/page.tsx      →  /about
└── (shop)/
    ├── layout.tsx          ← a DIFFERENT layout for shop pages
    ├── products/page.tsx   →  /products
    └── cart/page.tsx       →  /cart
```

The `(marketing)` and `(shop)` names never appear in the URL. They exist so you can give marketing pages one layout (say, a big footer) and shop pages another (a cart sidebar) while keeping clean top-level URLs.

> **Gotcha — two route groups can't define the same path.** If both `(marketing)/page.tsx` and `(shop)/page.tsx` resolve to `/`, you get a conflict. Groups change organization, not the uniqueness rules of the final URL.

---

## V. LAYOUTS AND NESTED LAYOUTS

A **`layout.tsx`** wraps a page and *all routes nested below it*. Critically, layouts **persist across navigation** — when you move between sibling pages, the shared layout does **not** re-render or lose state. This is what makes sidebars, nav bars, and tab state survive navigation.

```tsx
// app/layout.tsx — the ROOT layout (required). Must render <html> and <body>.
import "./globals.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

```tsx
// app/dashboard/layout.tsx — wraps everything under /dashboard
import Link from "next/link";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: "flex" }}>
      <aside>
        {/* This sidebar stays mounted while you navigate between dashboard pages */}
        <Link href="/dashboard">Overview</Link>
        <Link href="/dashboard/settings">Settings</Link>
      </aside>
      <section>{children}</section>     {/* the active nested page renders here */}
    </div>
  );
}
```

Layouts **compose** — they nest in the same shape as the folders. A request to `/dashboard/settings` renders this onion:

```
RootLayout
└── DashboardLayout
    └── SettingsPage
```

```
app/
├── layout.tsx              ← RootLayout (always)
└── dashboard/
    ├── layout.tsx          ← DashboardLayout (wraps all /dashboard/* pages)
    ├── page.tsx            ← /dashboard
    └── settings/
        └── page.tsx        ← /dashboard/settings (gets BOTH layouts)
```

> **Gotcha — layouts do not receive `params` of *deeper* dynamic segments... but they do receive their own.** A `layout.tsx` inside `app/blog/[slug]/` gets `params.slug`. The root layout does not see deeper params. Pass data down via the layout that actually owns the segment.

### `template.tsx` — when you *want* a re-mount

A `layout` keeps its state across navigation. Occasionally you want the opposite — a fresh instance each time (e.g. to re-trigger an enter animation or reset a form). `template.tsx` behaves like a layout but **re-mounts on every navigation**. Reach for it rarely; `layout` is almost always what you want.

---

## VI. LOADING UI — `loading.tsx`

Drop a **`loading.tsx`** into any route segment and Next.js automatically wraps that segment's `page` in a React **`<Suspense>`** boundary. While the page (and its data) loads, the loading UI shows instantly — and because the shared layout stays put, the user sees a responsive shell, not a blank screen.

```tsx
// app/dashboard/loading.tsx — shown instantly while dashboard/page.tsx loads
export default function Loading() {
  return <p>Loading dashboard…</p>;   // swap for a skeleton in real apps
}
```

```tsx
// app/dashboard/page.tsx — a slow Server Component
export default async function Dashboard() {
  // Simulate slow data — the user sees loading.tsx until this resolves
  const data = await fetch("https://api.example.com/stats", { cache: "no-store" })
    .then((r) => r.json());
  return <pre>{JSON.stringify(data, null, 2)}</pre>;
}
```

This is **streaming**: the layout and loading state are sent immediately, then the finished page streams in when ready. No `useState`/`useEffect` loading flags required. (Deeper in file 04.)

---

## VII. ERROR HANDLING — `error.tsx` AND `not-found.tsx`

### `error.tsx` — segment error boundary

If rendering a segment throws, Next.js catches it with the nearest **`error.tsx`** and shows that UI instead of crashing the whole app. **It must be a Client Component** (it uses interactivity — a retry button and the error object).

```tsx
"use client"; // error boundaries are always Client Components

// app/dashboard/error.tsx
export default function Error({
  error,
  reset,             // call this to attempt re-rendering the segment
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong in the dashboard.</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

> **Gotcha — `error.tsx` does NOT catch errors in the *same-level* `layout.tsx`.** An error boundary wraps the segment's *children*, so it cannot catch a throw from its sibling layout (the layout sits *above* it). To catch layout errors, put the `error.tsx` one level up, or use the special `global-error.tsx` at the root for catastrophic failures.

### `not-found.tsx` and `notFound()`

Call the `notFound()` function to render the nearest **`not-found.tsx`** (and send a 404 status). Perfect for "this record doesn't exist."

```tsx
// app/blog/[slug]/page.tsx
import { notFound } from "next/navigation";

export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await getPost(slug);          // returns null if missing

  if (!post) notFound();                      // → renders not-found.tsx, sends HTTP 404

  return <article>{post.title}</article>;
}
```

```tsx
// app/blog/[slug]/not-found.tsx
export default function NotFound() {
  return <h1>That post does not exist.</h1>;
}
```

> The root-level `app/not-found.tsx` also handles any URL that matches no route at all.

---

## VIII. NAVIGATION — `<Link>`

Use the **`<Link>`** component (from `next/link`) for navigation, not raw `<a>` tags. `<Link>` does **client-side navigation** (no full page reload) and **prefetches** the target route's code when the link enters the viewport, so clicks feel instant.

```tsx
import Link from "next/link";

export default function Nav() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      {/* dynamic + query string */}
      <Link href="/blog/hello-world">Read post</Link>
      <Link href={{ pathname: "/products", query: { page: "2" } }}>Page 2</Link>
      {/* disable prefetch for rarely-clicked links */}
      <Link href="/huge-report" prefetch={false}>Heavy report</Link>
    </nav>
  );
}
```

| Feature | `<Link>` | raw `<a>` |
|---------|----------|-----------|
| Page reload | No (client-side) | Yes (full reload) |
| Prefetching | Yes (automatic) | No |
| Preserves layout state | Yes | No |
| Use for | Internal routes | External links only |

> **Gotcha — use `<a>` for external links.** `<Link>` is for routes *inside* your app. For `https://other-site.com`, use a normal `<a href="..." target="_blank" rel="noopener noreferrer">`.

---

## IX. PROGRAMMATIC NAVIGATION AND ROUTE HOOKS

Sometimes you navigate from code (after a form submits, etc.) rather than a click. The navigation hooks come from **`next/navigation`** and are **Client Component only** — they require `"use client"`.

```tsx
"use client";

import { useRouter, usePathname, useSearchParams, useParams } from "next/navigation";

export default function NavTools() {
  const router = useRouter();
  const pathname = usePathname();          // e.g. "/blog/hello"  (current path)
  const searchParams = useSearchParams();  // read ?key=value on the client
  const params = useParams();              // dynamic segment values, client-side

  const page = searchParams.get("page");

  return (
    <div>
      <p>You are at {pathname} (page={page})</p>

      <button onClick={() => router.push("/dashboard")}>Go to dashboard</button>
      <button onClick={() => router.replace("/login")}>Replace (no history entry)</button>
      <button onClick={() => router.back()}>Back</button>
      <button onClick={() => router.refresh()}>Refresh server data</button>
    </div>
  );
}
```

| Method / hook | Purpose |
|---------------|---------|
| `router.push(url)` | Navigate, adding a history entry |
| `router.replace(url)` | Navigate, replacing current history entry (no back) |
| `router.back()` / `router.forward()` | Browser history |
| `router.refresh()` | Re-fetch server components for the current route (keeps client state) |
| `usePathname()` | Current pathname string |
| `useSearchParams()` | Read-only query params (client side) |
| `useParams()` | Dynamic route params (client side) |

For navigation from **server** code (Server Components, Server Actions, Route Handlers) you cannot use `useRouter` — there is no client. Use the **`redirect()`** function from `next/navigation` instead:

```tsx
// A Server Component that bounces unauthenticated users away.
import { redirect } from "next/navigation";

export default async function Dashboard() {
  const user = await getCurrentUser();      // server-side check
  if (!user) redirect("/login");            // throws → navigation happens, code below skipped
  return <h1>Welcome {user.name}</h1>;
}
```

> **Gotcha — `redirect()` throws.** Like `notFound()`, `redirect()` works by throwing a special internal error, so any code after it does not run. Call it *outside* `try/catch` blocks (a `try` would swallow the redirect). Use `useRouter().push()` on the client; use `redirect()` on the server.

> **Gotcha — import from `next/navigation`, not `next/router`.** `next/router` is the **old Pages Router** API. In the App Router you must import `useRouter` (and friends) from **`next/navigation`**. They are different objects — mixing them is a top-three beginner error.

A real example: a search box that updates the URL so results are shareable and back-button friendly.

```tsx
"use client";

import { useRouter, useSearchParams } from "next/navigation";

export default function SearchBox() {
  const router = useRouter();
  const params = useSearchParams();

  function onSearch(term: string) {
    const next = new URLSearchParams(params);  // clone current query
    if (term) next.set("q", term);
    else next.delete("q");
    router.push(`/search?${next.toString()}`); // URL becomes the source of truth
  }

  return (
    <input
      defaultValue={params.get("q") ?? ""}
      onChange={(e) => onSearch(e.target.value)}
      placeholder="Search…"
    />
  );
}
```

---

## X. PARALLEL ROUTES — `@slot`

**Parallel routes** let you render **two or more pages in the same layout at the same time**, each navigating independently. You define them with **named slots** — folders prefixed with `@`. A slot is *not* a URL segment; it is a named hole in the layout that the layout receives as a prop.

```
app/dashboard/
├── layout.tsx          ← receives @team and @analytics as props
├── page.tsx            ← the default {children} slot
├── @team/
│   └── page.tsx        ← renders into the `team` slot
└── @analytics/
    └── page.tsx        ← renders into the `analytics` slot
```

```tsx
// app/dashboard/layout.tsx
// Each @folder becomes a NAMED PROP (in addition to children).
export default function DashboardLayout({
  children,                                 // the implicit slot (page.tsx)
  team,                                     // from @team
  analytics,                                // from @analytics
}: {
  children: React.ReactNode;
  team: React.ReactNode;
  analytics: React.ReactNode;
}) {
  return (
    <div>
      <section>{children}</section>
      <div style={{ display: "flex" }}>
        <aside>{team}</aside>               {/* renders @team/page.tsx */}
        <aside>{analytics}</aside>          {/* renders @analytics/page.tsx */}
      </div>
    </div>
  );
}
```

Why this matters: each slot has **independent loading and error states**, and each can navigate on its own without affecting the others. A dashboard where the "team" panel and the "analytics" panel each have their own sub-navigation is the canonical use case.

### `default.tsx` — the unmatched-slot fallback

When you navigate to a sub-route that one slot doesn't define, Next.js needs to know what to render in that slot. Provide a **`default.tsx`** in the slot to act as a fallback (often returning `null`):

```tsx
// app/dashboard/@team/default.tsx
// Rendered when the current URL doesn't match a specific @team sub-route.
export default function Default() {
  return null;   // render nothing in this slot by default
}
```

> **Gotcha — missing `default.tsx` causes a 404 on hard navigation.** Soft (client-side) navigation reuses a slot's previous state, but a full page reload has no prior state. Without `default.tsx`, the unmatched slot 404s the whole page. Add a `default.tsx` to every slot.

---

## XI. INTERCEPTING ROUTES — `(.)`, `(..)`, `(...)`

**Intercepting routes** let you load a route's content *within the current layout* while keeping the URL meaningful — the classic use case is a **modal**. Click a photo in a feed and it opens in a modal overlay (with a shareable URL like `/photo/3`), but a direct visit or page refresh to `/photo/3` shows the full standalone page.

The convention uses path-relative markers, analogous to `../` in imports:

| Marker | Means "intercept a route…" |
|--------|----------------------------|
| `(.)folder` | …at the **same** level |
| `(..)folder` | …**one level up** |
| `(..)(..)folder` | …**two levels up** |
| `(...)folder` | …from the **root** `app` directory |

Combined with **parallel routes**, this produces the photo-modal pattern:

```
app/
├── layout.tsx
├── page.tsx                         ← the feed at /
├── @modal/
│   ├── default.tsx                  ← null when no modal is open
│   └── (.)photo/
│       └── [id]/
│           └── page.tsx             ← INTERCEPTS /photo/[id] → renders in the modal slot
└── photo/
    └── [id]/
        └── page.tsx                 ← the real /photo/[id] standalone page
```

```tsx
// app/layout.tsx — render the modal slot alongside children
export default function RootLayout({
  children,
  modal,
}: {
  children: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        {children}
        {modal}            {/* the intercepted modal renders here, over the feed */}
      </body>
    </html>
  );
}
```

```tsx
// app/@modal/(.)photo/[id]/page.tsx — shown when navigating CLIENT-SIDE to /photo/:id
import { Modal } from "@/components/Modal";   // a client component with a backdrop

export default async function PhotoModal({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return (
    <Modal>
      <img src={`/photos/${id}.jpg`} alt={`Photo ${id}`} />
    </Modal>
  );
}
```

The magic: clicking a `<Link href="/photo/3">` from the feed triggers the **intercepted** route (the modal), but pasting `/photo/3` into the address bar — a hard navigation — bypasses interception and renders the **real** `photo/[id]/page.tsx` standalone. Same URL, two presentations, chosen by *how you arrived*.

> **Gotcha — interception only happens on soft navigation.** A page reload or a direct URL visit always renders the actual route, never the interceptor. That is the feature, not a bug: it is what makes the modal's URL shareable.

---

## XII. LINKING IT TOGETHER — A REALISTIC TREE

Here is how the pieces compose in a real app:

```
app/
├── layout.tsx                     ← root layout (html/body, global nav)
├── page.tsx                       ← /
├── not-found.tsx                  ← global 404
├── (marketing)/
│   ├── about/page.tsx             ← /about
│   └── pricing/page.tsx           ← /pricing
├── blog/
│   ├── page.tsx                   ← /blog (list)
│   └── [slug]/
│       ├── page.tsx               ← /blog/:slug
│       ├── loading.tsx            ← skeleton while a post loads
│       └── not-found.tsx          ← post-specific 404
└── dashboard/
    ├── layout.tsx                 ← sidebar shell, persists across pages
    ├── page.tsx                   ← /dashboard
    ├── loading.tsx                ← dashboard skeleton
    ├── error.tsx                  ← dashboard error boundary (Client Component)
    └── settings/page.tsx          ← /dashboard/settings
```

Every URL the user can reach, and every loading/error state, is expressed *structurally* in the file tree. That legibility — being able to read the product from the folders — is the App Router's core gift.

---

## XIII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Importing `useRouter` from `next/router` | Hook throws / undefined in App Router | Import from `next/navigation` |
| Reading `params` synchronously in Next 15 | Type error / runtime warning | `await params` (it's a Promise in 15) |
| Using `<a>` for internal routes | Full page reloads, lost state | Use `<Link href="...">` |
| Calling navigation hooks in a Server Component | "hook can only be used in Client Component" | Add `"use client"` |
| Expecting `error.tsx` to catch sibling `layout` errors | Error escapes the boundary | Put `error.tsx` one level up / use `global-error.tsx` |
| Route group name showing in URL | `/marketing/about` instead of `/about` | `(parentheses)` groups are stripped from the URL — check brackets |
| Folder with no `page.tsx` | 404 on a folder that exists | Add `page.tsx` or `route.ts` |
| Forgetting `notFound()` returns nothing useful after | Code keeps running | `notFound()` throws — code after it does not run |
| Parallel-route slot missing `default.tsx` | Whole page 404s on reload | Add `default.tsx` (often `return null`) to every `@slot` |
| Expecting interception on page reload | Modal route shows the full page instead | Interception only fires on soft (client) navigation — by design |
| Treating `@slot` as a URL segment | Confused why `/@team` doesn't exist | `@` slots are layout props, not paths; they don't appear in the URL |

---

## 🧠 KEY TAKEAWAYS

- **Folders are routes; `page.tsx` makes them public.** The folder path from `app/` is the URL.
- **`[param]`** captures one segment, **`[...slug]`** captures many, **`[[...slug]]`** also matches the bare path. Read them from the (awaited) `params` prop; query strings come from `searchParams`.
- **`(parentheses)`** route groups organize files without changing the URL — perfect for giving different sections different layouts.
- **Parallel routes (`@slot`)** render multiple independent panes in one layout (each a layout prop with its own loading/error state); give every slot a **`default.tsx`**. **Intercepting routes (`(.)`, `(..)`, `(...)`)** load a route inside the current layout (the modal pattern) on soft navigation while preserving a shareable, standalone URL.
- **Layouts wrap pages and persist across navigation**; they nest exactly like the folders. The root layout is required and renders `<html>`/`<body>`.
- **`loading.tsx`** gives instant Suspense-based loading UI; **`error.tsx`** (a Client Component) is a per-segment error boundary; **`not-found.tsx`** + `notFound()` handle 404s.
- Navigate with **`<Link>`** (client-side, prefetching) and, when needed, the **`next/navigation`** hooks (`useRouter`, `usePathname`, `useSearchParams`) — never `next/router`.

---

**Prev:** [`01-Why-Nextjs-And-Setup.md`](./01-Why-Nextjs-And-Setup.md) · **Next:** [`03-Server-And-Client-Components.md`](./03-Server-And-Client-Components.md) · **Index:** [`00-Index.md`](./00-Index.md)
