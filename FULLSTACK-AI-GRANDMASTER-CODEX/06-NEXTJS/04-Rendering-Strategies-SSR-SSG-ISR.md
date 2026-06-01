# ▲ 04 — Rendering Strategies: SSR, SSG, ISR & Caching

> *"Rendering is a question of time. Static asks 'render once at build'; dynamic asks 'render now, per request'; incremental asks 'render once, then quietly refresh.' Caching decides how often you pay."*

**Prev:** [`03-Server-And-Client-Components.md`](./03-Server-And-Client-Components.md) · **Next:** [`05-Data-Fetching-And-Mutations.md`](./05-Data-Fetching-And-Mutations.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE CENTRAL QUESTION — *WHEN* IS THE HTML BUILT?

Every page in Next.js produces HTML. The only question that distinguishes the rendering strategies is **when** that HTML is produced and **how long it lives**:

```
        BUILD TIME                 REQUEST TIME              "STALE-THEN-REFRESH"
   ┌──────────────────┐      ┌──────────────────────┐    ┌────────────────────────┐
   │   STATIC (SSG)   │      │    DYNAMIC (SSR)      │    │  INCREMENTAL (ISR)     │
   │ render once at   │      │ render fresh on every │    │ render once, serve      │
   │ build, serve the │      │ request (per user,    │    │ cached, regenerate in   │
   │ same HTML to all │      │ always up to date)    │    │ the background every N  │
   └──────────────────┘      └──────────────────────┘    └────────────────────────┘
        fastest                    most current               best of both
```

In the App Router you rarely pick these with a config flag. Instead, **the framework infers the strategy from what your code does.** Read `cookies()`? You went dynamic. `fetch` with the default cache? You stayed static. Understanding the triggers is the whole game.

> **Mental model.** A route is **static by default**. Certain actions (reading per-request data, opting out of the cache) flip it to **dynamic**. ISR is static rendering with an expiry clock attached.

---

## II. STATIC RENDERING (SSG) — THE DEFAULT

By default, Next.js renders routes **at build time** and serves the same pre-rendered HTML to every visitor from a CDN. This is the fastest possible delivery — there is no server work per request.

```tsx
// app/about/page.tsx
// No dynamic data, no per-request APIs → STATICALLY rendered at build time.
export default function About() {
  return (
    <main>
      <h1>About us</h1>
      <p>This HTML was generated once, at build, and cached forever.</p>
    </main>
  );
}
```

Even with data, a route stays static if the data can be fetched at build time and cached:

```tsx
// app/blog/page.tsx — still STATIC: fetch defaults to caching.
export default async function Blog() {
  const posts = await fetch("https://api.example.com/posts") // cached by default
    .then((r) => r.json());
  return (
    <ul>
      {posts.map((p: { id: string; title: string }) => (
        <li key={p.id}>{p.title}</li>
      ))}
    </ul>
  );
}
```

In the `next build` route table these appear as `○ (Static)`. They cost nothing per request and scale infinitely.

> **Gotcha — build-time data can go stale.** A purely static page is frozen at the moment of build. If the underlying data changes, the page does *not* update until you rebuild — unless you add ISR (`revalidate`) or go dynamic. Choose static only for content that rarely changes, or pair it with revalidation.

---

## III. DYNAMIC RENDERING (SSR) — RENDER PER REQUEST

A route becomes **dynamic** when it depends on information only known at request time. Then Next.js renders fresh HTML on the server for *every* request. In the route table it shows as `ƒ (Dynamic)`.

### What flips a route to dynamic (the triggers)

| Trigger | Why it forces dynamic |
|---------|-----------------------|
| `cookies()` | Cookies are per-request |
| `headers()` | Headers are per-request |
| `await searchParams` | Query strings vary per request |
| `fetch(url, { cache: "no-store" })` | You explicitly opted out of caching |
| `export const dynamic = "force-dynamic"` | You said so explicitly |
| `connection()` / `noStore()` (uncached APIs) | Explicit dynamic opt-in |

```tsx
// app/dashboard/page.tsx — DYNAMIC because it reads cookies (per-request data).
import { cookies } from "next/headers";

export default async function Dashboard() {
  const cookieStore = await cookies();          // reading cookies → dynamic
  const theme = cookieStore.get("theme")?.value ?? "light";

  // no-store also forces fresh data on every request
  const stats = await fetch("https://api.example.com/stats", {
    cache: "no-store",
  }).then((r) => r.json());

  return <pre data-theme={theme}>{JSON.stringify(stats, null, 2)}</pre>;
}
```

> **Gotcha — one dynamic API "poisons" the whole route.** You cannot have *part* of a route be static and part dynamic in the classic model — calling `cookies()` anywhere in the render path makes the entire route dynamic. (Partial Prerendering, section X, is the new feature that finally breaks this all-or-nothing rule.)

---

## IV. ROUTE SEGMENT CONFIG — TAKING EXPLICIT CONTROL

When you want to *override* the inferred behavior, export configuration constants from a `page.tsx`, `layout.tsx`, or `route.ts`. These are read at build time.

```tsx
// app/feed/page.tsx — explicit segment config

// Force the rendering mode:
//   "auto" (default) | "force-dynamic" | "force-static" | "error"
export const dynamic = "force-dynamic";

// Revalidate the whole route every N seconds (ISR). false = never; 0 = always.
export const revalidate = 60;

// Override fetch caching for the whole segment.
export const fetchCache = "default-cache";

// Choose the runtime: "nodejs" (default) | "edge"
export const runtime = "nodejs";

// Are dynamic params outside generateStaticParams allowed?
export const dynamicParams = true;

export default async function Feed() {
  /* ... */
}
```

| Export | Common values | Effect |
|--------|---------------|--------|
| `dynamic` | `auto`, `force-dynamic`, `force-static`, `error` | Force the rendering strategy |
| `revalidate` | `false`, `0`, `number` | ISR interval for the segment (seconds) |
| `fetchCache` | `auto`, `default-cache`, `force-no-store` | Default cache for all `fetch`es here |
| `runtime` | `nodejs`, `edge` | Where the code executes |
| `dynamicParams` | `true`, `false` | Allow params not returned by `generateStaticParams`? |

---

## V. INCREMENTAL STATIC REGENERATION (ISR) — `revalidate`

ISR gives you static speed **and** fresh-ish data. The page is served from cache (fast), and after `revalidate` seconds the *next* request triggers a background re-render. The first visitor after expiry still gets the stale page instantly; the regenerated page is served from then on. This is **stale-while-revalidate**.

```tsx
// app/products/page.tsx — regenerate at most once per 60 seconds.
export const revalidate = 60;

export default async function Products() {
  const products = await fetch("https://api.example.com/products").then((r) => r.json());
  return <ProductGrid products={products} />;
}
```

Or set it per-fetch (more granular — different data can refresh at different rates):

```tsx
export default async function Page() {
  // This data refreshes every 10 minutes...
  const slow = await fetch("https://api.example.com/config", {
    next: { revalidate: 600 },
  }).then((r) => r.json());

  // ...while this refreshes every 30 seconds.
  const fast = await fetch("https://api.example.com/prices", {
    next: { revalidate: 30 },
  }).then((r) => r.json());

  return <Dashboard config={slow} prices={fast} />;
}
```

```
ISR timeline (revalidate = 60):

  t=0s   build/first render → cache the HTML
  t=10s  request → serve cached (fresh)          ✓ instant
  t=70s  request → serve cached (STALE) + trigger background regen
  t=71s  request → serve the NEWLY regenerated HTML
```

> **Gotcha — `revalidate` is a *minimum* age, not a schedule.** Nothing regenerates on a timer in the background by itself; regeneration is triggered *by a request* that arrives after the window expires. A page nobody visits never regenerates. For event-driven freshness, use on-demand revalidation (`revalidatePath`/`revalidateTag`, file 05) instead of, or alongside, time-based ISR.

---

## VI. PRE-RENDERING DYNAMIC ROUTES — `generateStaticParams`

A dynamic route like `app/blog/[slug]/page.tsx` is dynamic by default — Next.js doesn't know the slugs at build time. **`generateStaticParams`** tells it which params to pre-render, turning a dynamic route into a set of static pages (`● (SSG)` in the route table). This is how blogs, docs, and product catalogs get static speed.

```tsx
// app/blog/[slug]/page.tsx

// Runs at BUILD time. Return the list of params to pre-render.
export async function generateStaticParams() {
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());
  return posts.map((post: { slug: string }) => ({ slug: post.slug }));
  // → [{ slug: "hello" }, { slug: "world" }] — one static page each
}

export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await fetch(`https://api.example.com/posts/${slug}`).then((r) => r.json());
  return <article><h1>{post.title}</h1>{post.body}</article>;
}
```

Pair it with `dynamicParams` to control what happens for a slug you *didn't* pre-render:

```tsx
// true (default): render unknown slugs on-demand (and cache them) — like ISR fallback
// false: unknown slugs → 404
export const dynamicParams = true;
```

> **Gotcha — `generateStaticParams` + `revalidate` = the blog superpower.** Pre-render your known posts at build (`generateStaticParams`), set `export const revalidate = 3600`, and leave `dynamicParams = true`. Result: existing posts are static and fast, they refresh hourly, and brand-new posts render on first visit without a rebuild. This combination covers the vast majority of content sites.

---

## VII. THE FOUR CACHING LAYERS

This is the most misunderstood part of Next.js. There are **four distinct caches**, each with a different scope, lifetime, and invalidation method. Treat them as a stack data flows through.

```
   Request  ──►  ① Request Memoization  (per-render, in-memory, dedupes fetches)
                        │
                        ▼
                 ② Data Cache           (persistent across requests/deploys; fetch results)
                        │
                        ▼
                 ③ Full Route Cache      (the rendered HTML/RSC payload, at build)
                        │
                        ▼ (sent to browser)
                 ④ Router Cache          (client-side, in the browser, per session)
```

### ① Request Memoization

During a **single render pass**, if you call `fetch` with the *same URL and options* multiple times (e.g. from three different components), Next.js runs it **once** and shares the result. This means you can fetch the same data wherever you need it without prop-drilling or causing duplicate network calls.

```tsx
async function getUser(id: string) {
  // Called from layout, page, AND a nested component — fetched ONCE per request.
  return fetch(`https://api.example.com/users/${id}`).then((r) => r.json());
}
```

- **Scope:** a single render of a single request. **Lifetime:** that render only. **Applies to:** `fetch` (and functions wrapped in React `cache()`).
- **You don't manage it** — it just dedupes. It resets every request.

### ② Data Cache

The **persistent** cache for the *results* of `fetch` calls. It survives across requests and even deployments, on the server. This is what makes a "static" fetch reusable indefinitely.

```tsx
// Cached persistently (the DEFAULT in Next 14; opt-in via options in 15).
await fetch(url);                                  // → stored in the Data Cache
await fetch(url, { cache: "force-cache" });        // explicit: cache forever
await fetch(url, { cache: "no-store" });           // bypass the Data Cache entirely
await fetch(url, { next: { revalidate: 60 } });    // cache but expire after 60s
await fetch(url, { next: { tags: ["posts"] } });   // tag for on-demand invalidation
```

- **Scope:** server-wide, all users. **Lifetime:** until revalidated. **Invalidate with:** `revalidate` time, `revalidateTag()`, or `revalidatePath()`.

> **Gotcha — Next.js 14 vs 15 changed the `fetch` default.** In **14**, `fetch` is cached by default (`force-cache`). In **15**, the default became **uncached** (`no-store`) — you opt *into* caching explicitly. Always check your version, and prefer being explicit (`{ cache: "force-cache" }` or `{ next: { revalidate } }`) so behavior doesn't shift under you on upgrade.

### ③ Full Route Cache

At build time (or revalidation), Next.js caches the **fully rendered output** of static routes — the HTML and the RSC payload. Requests for that route skip rendering entirely and serve the cached output. This is *why* static pages are so fast.

- **Scope:** server-wide. **Lifetime:** until the route is revalidated or redeployed. Dynamic routes (`ƒ`) are **not** in this cache — they render per request.

### ④ Router Cache (client-side)

In the **browser**, Next.js keeps an in-memory cache of the RSC payloads for routes you've visited (and prefetched). Navigating back to a recent route is instant because it's served from this client cache — no server round-trip.

- **Scope:** the user's browser session. **Lifetime:** seconds-to-minutes (depends on static/dynamic), or until a full reload. **Invalidate with:** `router.refresh()`, a Server Action, or `revalidatePath`/`revalidateTag` (which also tells clients to refresh).

| Cache | Where | Scope | Lifetime | How to invalidate |
|-------|-------|-------|----------|-------------------|
| ① Request Memoization | Server | One render | The render | (automatic, per request) |
| ② Data Cache | Server | All users | Until revalidated | `revalidateTag`, `revalidatePath`, `revalidate` time |
| ③ Full Route Cache | Server | All users | Until revalidated/redeploy | `revalidatePath`, redeploy, dynamic rendering |
| ④ Router Cache | Browser | One session | Seconds–minutes | `router.refresh()`, Server Action, hard reload |

> **Gotcha — "my data updated in the DB but the page still shows the old value."** This is almost always a caching layer doing its job. Walk the stack: is the `fetch` cached (Data Cache)? Is the route fully cached (Full Route Cache)? Is the browser showing a stale Router Cache entry? The fix is the right invalidation — usually `revalidateTag`/`revalidatePath` after a mutation (file 05).

---

## VIII. STREAMING WITH SUSPENSE

You don't have to wait for *all* data before sending *any* HTML. **Streaming** sends the page shell immediately, then streams in slow parts as they resolve. Two ways to do it: a route-level `loading.tsx` (file 02), or fine-grained `<Suspense>` boundaries.

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";

export default function Dashboard() {
  return (
    <main>
      <h1>Dashboard</h1>            {/* sent instantly */}

      {/* Each Suspense boundary streams independently when its data is ready */}
      <Suspense fallback={<p>Loading revenue…</p>}>
        <Revenue />                {/* slow async server component */}
      </Suspense>

      <Suspense fallback={<p>Loading activity…</p>}>
        <Activity />               {/* another slow one, streams separately */}
      </Suspense>
    </main>
  );
}

async function Revenue() {
  const data = await fetch("https://api.example.com/revenue", { cache: "no-store" })
    .then((r) => r.json());
  return <div>Revenue: ${data.total}</div>;
}

async function Activity() {
  const data = await fetch("https://api.example.com/activity", { cache: "no-store" })
    .then((r) => r.json());
  return <ul>{data.items.map((i: { id: string; text: string }) => <li key={i.id}>{i.text}</li>)}</ul>;
}
```

The user sees the heading and both fallbacks immediately; each section pops in when ready. No single slow query blocks the entire page. This dramatically improves perceived performance (faster Time To First Byte and First Contentful Paint).

> **Gotcha — streaming needs independent boundaries to help.** If you wrap *everything* in one `<Suspense>`, you just recreate "wait for it all." Place boundaries around the slow, independent parts so the fast parts ship first.

---

## IX. PARTIAL PRERENDERING (PPR)

**Partial Prerendering** is the newest rendering model (experimental/incrementally stable in Next 15) that finally breaks the "one dynamic API poisons the whole route" rule. PPR serves a **static shell instantly** from the CDN and **streams in the dynamic holes** within the same response. One route, mixed rendering.

```tsx
// next.config.ts — opt in (experimental)
import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  experimental: { ppr: "incremental" },   // enable PPR per-route via the export below
};
export default nextConfig;
```

```tsx
// app/product/[id]/page.tsx
export const experimental_ppr = true;     // opt this route into PPR

import { Suspense } from "react";

export default function Product() {
  return (
    <main>
      {/* STATIC shell — prerendered, on the CDN, instant */}
      <Header />
      <ProductImages />

      {/* DYNAMIC hole — streamed per request, inside the static page */}
      <Suspense fallback={<CartSkeleton />}>
        <Cart />                {/* reads cookies → dynamic, but doesn't make the page dynamic */}
      </Suspense>
    </main>
  );
}
```

```
PPR response:
  [ static shell delivered instantly from CDN ]  +  [ dynamic <Cart/> streamed in ]
        ↑ fast like SSG                                 ↑ personalized like SSR
```

> **Gotcha — PPR is still stabilizing.** APIs and config may shift between versions. Use it on greenfield Next 15 projects where you can track releases; don't refactor a production app to depend on experimental flags. The mental model — static shell + dynamic islands — is the future direction regardless.

---

## X. CHOOSING A STRATEGY — DECISION TABLE

| Your page… | Strategy | How |
|------------|----------|-----|
| Never changes (marketing, docs) | **Static (SSG)** | Default — just don't use dynamic APIs |
| Changes occasionally, same for all users | **ISR** | `export const revalidate = N` or per-fetch `revalidate` |
| Known set of dynamic pages (blog posts) | **SSG + `generateStaticParams`** | List params at build; add `revalidate` for freshness |
| Personalized per user (dashboard, cart) | **Dynamic (SSR)** | Read `cookies()`/`headers()`, or `no-store` fetch |
| Real-time / always fresh | **Dynamic** | `export const dynamic = "force-dynamic"` |
| Mostly static with a personalized slice | **PPR** | `experimental_ppr` + `<Suspense>` around the dynamic part |
| Slow data you don't want to block on | **Streaming** | `loading.tsx` or `<Suspense>` boundaries |

---

## XI. PAGES ROUTER CONTRAST (for migrators)

The old Pages Router chose rendering with exported functions instead of inference. You will see these in legacy code:

| App Router (modern) | Pages Router (legacy) |
|---------------------|----------------------|
| Static by default | `getStaticProps` |
| `generateStaticParams` | `getStaticPaths` |
| `export const revalidate` / per-fetch `revalidate` | `getStaticProps` returning `{ revalidate: N }` |
| Dynamic via `cookies()`/`no-store` | `getServerSideProps` |
| `<Suspense>` + `loading.tsx` streaming | (no first-class equivalent) |
| Four-layer caching with `fetch` | manual, in your data layer |

```tsx
// Pages Router — for recognition only. DO NOT write new code this way.
export async function getServerSideProps() {       // → SSR, runs every request
  const data = await fetch("https://api.example.com").then((r) => r.json());
  return { props: { data } };
}
export async function getStaticProps() {            // → SSG/ISR
  const data = await fetch("https://api.example.com").then((r) => r.json());
  return { props: { data }, revalidate: 60 };       // ISR every 60s
}
```

---

## XII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Assuming the Next 14 `fetch` default in Next 15 | Data unexpectedly uncached (or vice versa) | Be explicit: `cache`/`next.revalidate`; check your version |
| One `cookies()` call making a whole route dynamic | Lost static performance | Isolate dynamic bits behind `<Suspense>`/PPR; or accept dynamic |
| Expecting ISR to refresh on a timer with no traffic | Page never updates | ISR regenerates on the first request *after* expiry; use on-demand revalidation |
| Editing DB data, page still stale | Old values shown | Walk the 4 caches; `revalidateTag`/`revalidatePath` after writes |
| Wrapping the whole page in one `<Suspense>` | No streaming benefit | Boundaries around slow, independent parts only |
| Forgetting `generateStaticParams` for a blog | Every post renders dynamically | Add it to pre-render known slugs |
| Benchmarking rendering in `next dev` | "Caching doesn't work!" | Caching only exists in `next build && next start` |
| `dynamicParams = false` with a missing slug | Unexpected 404s | Keep it `true` for ISR-style fallback, or pre-render every param |

---

## 🧠 KEY TAKEAWAYS

- A route is **static by default**; reading per-request data (`cookies`, `headers`, `searchParams`) or opting out of the cache (`no-store`, `force-dynamic`) flips it to **dynamic**.
- **ISR** (`revalidate`) is static speed with a background refresh — stale-while-revalidate, triggered by traffic after the window expires.
- **`generateStaticParams`** pre-renders dynamic routes (blogs, catalogs); combine with `revalidate` + `dynamicParams` for the ideal content-site setup.
- There are **four caches**: ① Request Memoization (per-render dedupe), ② Data Cache (persistent `fetch` results), ③ Full Route Cache (rendered HTML), ④ Router Cache (client-side). Stale data is almost always one of these.
- **Streaming** with `loading.tsx` or `<Suspense>` ships the shell first and slow parts later; **PPR** serves a static shell with dynamic holes in one response.
- **Always verify rendering against `next build`** — the route table (`○` static, `●` SSG, `ƒ` dynamic) is the source of truth.

---

**Prev:** [`03-Server-And-Client-Components.md`](./03-Server-And-Client-Components.md) · **Next:** [`05-Data-Fetching-And-Mutations.md`](./05-Data-Fetching-And-Mutations.md) · **Index:** [`00-Index.md`](./00-Index.md)
