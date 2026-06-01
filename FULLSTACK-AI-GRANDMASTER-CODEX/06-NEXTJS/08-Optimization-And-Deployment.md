# ▲ 08 — Optimization & Deployment

> *"A fast app that nobody can find is a tree falling in an empty forest. Optimization makes it quick; metadata makes it discoverable; deployment makes it real. This is where the code becomes a product."*

**Prev:** [`07-Auth-And-Full-Stack-Nextjs.md`](./07-Auth-And-Full-Stack-Nextjs.md) · **Next:** _(end of section)_ · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE METADATA API — SEO BY CONVENTION

Search engines, social previews, and browsers read `<head>` tags: title, description, Open Graph, canonical URLs. Next.js generates them from a typed **Metadata API** — you export an object (or a function) and Next renders the tags.

### Static metadata

```tsx
// app/layout.tsx — root metadata, applies to the whole app.
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: {
    default: "Acme — Build faster",
    template: "%s | Acme",            // child pages fill %s → "Pricing | Acme"
  },
  description: "Acme helps teams ship software faster.",
  metadataBase: new URL("https://acme.com"),   // resolves relative OG/canonical URLs
  openGraph: {
    title: "Acme",
    description: "Ship faster.",
    url: "https://acme.com",
    siteName: "Acme",
    images: ["/og.png"],             // resolved against metadataBase
    type: "website",
  },
  twitter: { card: "summary_large_image" },
  robots: { index: true, follow: true },
};
```

A child page sets just its own title; the template wraps it:

```tsx
// app/pricing/page.tsx
import type { Metadata } from "next";
export const metadata: Metadata = { title: "Pricing" };  // → "Pricing | Acme"
export default function Pricing() { return <h1>Pricing</h1>; }
```

### Dynamic metadata — `generateMetadata`

When the title depends on data (a blog post, a product), export an async **`generateMetadata`**:

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from "next";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getPost(slug);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { images: [post.coverImage] },
  };
}

export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
  /* ... renders the post ... */
}
```

> **Gotcha — `metadata` and `generateMetadata` only work in Server Components (`page`/`layout`).** You cannot export `metadata` from a `"use client"` file, and you cannot put it in a regular component. Keep SEO data in the route's server-rendered `page.tsx`/`layout.tsx`.

---

## II. SITEMAP, ROBOTS & STRUCTURED DATA

Next.js turns special files into the crawl-control endpoints search engines expect.

```ts
// app/sitemap.ts → serves /sitemap.xml
import type { MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();
  const postUrls = posts.map((p) => ({
    url: `https://acme.com/blog/${p.slug}`,
    lastModified: p.updatedAt,
  }));
  return [
    { url: "https://acme.com", lastModified: new Date() },
    { url: "https://acme.com/pricing" },
    ...postUrls,
  ];
}
```

```ts
// app/robots.ts → serves /robots.txt
import type { MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: "/admin" },
    sitemap: "https://acme.com/sitemap.xml",
  };
}
```

For rich results (stars, breadcrumbs), inject **JSON-LD** structured data as a script in the page:

```tsx
// app/blog/[slug]/page.tsx — JSON-LD for an article.
export default async function Post({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await getPost(slug);
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    datePublished: post.publishedAt,
    author: { "@type": "Person", name: post.author },
  };
  return (
    <article>
      <script
        type="application/ld+json"
        // safe: this is your own server-generated data, not user input
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <h1>{post.title}</h1>
    </article>
  );
}
```

> **Gotcha — `metadataBase` fixes broken social previews.** If your Open Graph image is a relative path (`/og.png`) and you didn't set `metadataBase`, crawlers receive a relative URL they can't fetch, and previews break. Set `metadataBase` to your production origin in the root layout.

---

## III. IMAGE OPTIMIZATION — `next/image`

The `<Image>` component is one of Next.js's biggest performance wins. It automatically resizes, serves modern formats (WebP/AVIF), lazy-loads, and prevents layout shift by reserving space.

```tsx
import Image from "next/image";

export default function Hero() {
  return (
    <Image
      src="/hero.jpg"          // local import or path under /public
      alt="Product hero"        // required — accessibility + SEO
      width={1200}              // intrinsic size (reserves space → no layout shift)
      height={630}
      priority                  // preload above-the-fold images (skip lazy-load)
    />
  );
}
```

For images whose dimensions you don't know (CMS content), use `fill` with a sized container:

```tsx
<div style={{ position: "relative", width: "100%", height: 400 }}>
  <Image src={post.cover} alt={post.title} fill style={{ objectFit: "cover" }} />
</div>
```

Remote images require allow-listing the host (a security measure):

```ts
// next.config.ts
import type { NextConfig } from "next";
const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
      { protocol: "https", hostname: "cdn.acme.com" },
    ],
  },
};
export default nextConfig;
```

| `<img>` | `next/image` |
|---------|--------------|
| You handle sizing/formats | Auto resize + WebP/AVIF |
| Eager load by default | Lazy-load by default |
| Layout shift risk | Space reserved via width/height |
| No host restriction | Remote hosts must be allow-listed |

> **Gotcha — always set `width`/`height` (or `fill`), and `alt`.** Missing dimensions cause layout shift (hurts the CLS Core Web Vital) or a build error. Use `priority` on the largest above-the-fold image (the LCP element) and *only* there — overusing it defeats lazy loading.

---

## IV. FONT OPTIMIZATION — `next/font`

`next/font` self-hosts fonts at build time, removing the network request to Google Fonts, eliminating layout shift (it computes fallback metrics), and improving privacy (no external request).

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",          // show fallback text immediately, swap when font loads
  variable: "--font-inter", // expose as a CSS variable (great with Tailwind)
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

Local fonts work too:

```tsx
import localFont from "next/font/local";
const myFont = localFont({ src: "./fonts/Custom.woff2", display: "swap" });
```

> **Gotcha — `next/font` downloads fonts at *build* time, not runtime.** There's zero external request from the user's browser — the font ships from your own domain. This is why it eliminates the render-blocking Google Fonts request and the associated layout shift. Use `display: "swap"` so text is visible immediately.

---

## V. SCRIPTS & THIRD-PARTY CODE — `next/script`

Third-party scripts (analytics, chat widgets) are a top cause of slow pages. `<Script>` controls *when* they load so they don't block rendering.

```tsx
import Script from "next/script";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html><body>
      {children}
      {/* afterInteractive (default): load after the page is interactive */}
      <Script src="https://analytics.example.com/script.js" strategy="afterInteractive" />
      {/* lazyOnload: load during idle time — for low-priority widgets */}
      <Script src="https://widget.example.com/chat.js" strategy="lazyOnload" />
    </body></html>
  );
}
```

| Strategy | Loads | Use for |
|----------|-------|---------|
| `beforeInteractive` | Before hydration | Critical (rare — bot detection, polyfills) |
| `afterInteractive` | After hydration (default) | Analytics, tag managers |
| `lazyOnload` | Browser idle time | Chat, social embeds |

---

## VI. PERFORMANCE & CORE WEB VITALS

Next.js gives strong defaults (code splitting, prefetching, image/font optimization), but you still measure and tune. The metrics that matter (Google's **Core Web Vitals**):

| Metric | Measures | Good | Lever in Next.js |
|--------|----------|------|------------------|
| **LCP** (Largest Contentful Paint) | Load speed of the main element | < 2.5s | `<Image priority>`, SSG/ISR, streaming |
| **CLS** (Cumulative Layout Shift) | Visual stability | < 0.1 | Image dimensions, `next/font` |
| **INP** (Interaction to Next Paint) | Responsiveness | < 200ms | Less client JS, smaller bundles |

Practical levers:

```ts
// next.config.ts — analyze your bundle to find bloat.
// npm i -D @next/bundle-analyzer
import withBundleAnalyzer from "@next/bundle-analyzer";
const analyze = withBundleAnalyzer({ enabled: process.env.ANALYZE === "true" });
export default analyze({ /* nextConfig */ });
// Run: ANALYZE=true npm run build  → opens a treemap of your JS
```

```tsx
// Dynamically import heavy client-only components so they don't bloat first load.
import dynamic from "next/dynamic";
const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <p>Loading chart…</p>,
  ssr: false,                       // skip server-rendering a client-only lib
});
```

> **Gotcha — the biggest perf lever is "ship less JavaScript."** Every `"use client"` adds to the bundle. Keep components on the server (file 03), lazy-load heavy client widgets with `next/dynamic`, and prefer static/ISR rendering. Re-read the `next build` route table's "First Load JS" column — that number is what users download.

---

## VII. DEPLOYING TO VERCEL

Vercel is built by the Next.js team; it's the path of least resistance and supports every feature (ISR, streaming, Edge, image optimization) with zero config.

```bash
# Option A — Git integration (recommended)
# 1. Push your repo to GitHub/GitLab/Bitbucket
# 2. Import it at vercel.com → it detects Next.js automatically
# 3. Add env vars in the dashboard (DATABASE_URL, AUTH_SECRET, ...)
# 4. Every push to main deploys to production; every PR gets a preview URL

# Option B — Vercel CLI
npm i -g vercel
vercel            # deploy a preview
vercel --prod     # deploy to production
```

What you get automatically: global CDN, automatic HTTPS, preview deployments per branch, serverless/Edge functions for your dynamic routes and handlers, and built-in image optimization.

> **Gotcha — set environment variables in the Vercel dashboard, not in committed files.** Your `.env.local` is gitignored and never uploaded. Re-enter each server secret (`DATABASE_URL`, `AUTH_SECRET`, provider keys) in **Project → Settings → Environment Variables**, and scope them to Production/Preview/Development as needed. A missing var is the #1 cause of "works locally, 500s in production."

---

## VIII. SELF-HOSTING

You are not locked into Vercel. Next.js runs anywhere Node.js does, and most features work when self-hosted (image optimization needs `sharp`, which is included).

### Plain Node server

```bash
npm run build     # produces .next/
npm run start     # runs `next start` — a production Node server on :3000
```

Put it behind a reverse proxy (Nginx/Caddy) for TLS and load balancing.

### Docker (with `output: "standalone"`)

`standalone` output bundles only the files needed to run, producing a tiny image:

```ts
// next.config.ts
const nextConfig = { output: "standalone" };
export default nextConfig;
```

```dockerfile
# Dockerfile — multi-stage build for a lean production image.
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build                  # emits .next/standalone

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]          # standalone emits its own server.js
```

| Concern | Vercel | Self-host |
|---------|--------|-----------|
| Setup effort | Near zero | You manage the server/CDN/TLS |
| ISR / revalidation | Built in | Works; needs persistent storage for the cache |
| Image optimization | Automatic | Needs `sharp` (bundled) + CPU/memory |
| Edge runtime | Native | Limited — most self-hosts run Node only |
| Scaling | Automatic | Your responsibility |

> **Gotcha — ISR cache and serverless filesystems.** Self-hosted ISR writes regenerated pages to disk. On ephemeral/containerized hosts that filesystem may not persist or be shared across instances, so revalidation can behave inconsistently. Use a shared cache handler (`cacheHandler` in `next.config`) or a persistent volume for multi-instance ISR.

---

## IX. MONITORING & ANALYTICS

Once live, you measure. Options:

```tsx
// Vercel's first-party, privacy-friendly analytics + Web Vitals:
// npm i @vercel/analytics @vercel/speed-insights
import { Analytics } from "@vercel/analytics/react";
import { SpeedInsights } from "@vercel/speed-insights/next";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html><body>
      {children}
      <Analytics />          {/* page views */}
      <SpeedInsights />      {/* real-user Core Web Vitals */}
    </body></html>
  );
}
```

You can also report Web Vitals yourself to any backend:

```tsx
"use client";
import { useReportWebVitals } from "next/web-vitals";

export function WebVitals() {
  useReportWebVitals((metric) => {
    // send {metric.name, metric.value} to your analytics endpoint
    navigator.sendBeacon("/api/vitals", JSON.stringify(metric));
  });
  return null;
}
```

For errors and traces, integrate an APM (Sentry, etc.) — they ship Next.js SDKs that capture both server and client errors.

> **Gotcha — measure real users, not just your laptop.** Lab tools (Lighthouse, `next build` output) are useful but run on fast machines/networks. Field data (Vercel Speed Insights, Chrome UX Report) reflects your actual users' devices, which is what Core Web Vitals scoring uses for SEO.

---

## X. PAGES ROUTER CONTRAST (deployment & meta)

For migrators recognizing legacy code:

| App Router (modern) | Pages Router (legacy) |
|---------------------|----------------------|
| Metadata API (`metadata` / `generateMetadata`) | `next/head` `<Head>` component |
| `app/sitemap.ts`, `app/robots.ts` | manual files in `public/` or libraries |
| `next/image`, `next/font` (same) | `next/image`, `next/font` (same) |
| `next/script` (same) | `next/script` (same) |
| Deploy is identical | Deploy is identical |

Image, font, script, and deployment stories are largely **shared** between the routers — the big difference is metadata (`<Head>` vs the Metadata API).

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Exporting `metadata` from a client component | Ignored / build error | Metadata only in server `page`/`layout` |
| No `metadataBase` | Broken OG image previews | Set it to your production origin |
| `<Image>` without dimensions | Layout shift / error | Provide `width`/`height` or `fill` + sized parent |
| `priority` on every image | Defeats lazy-loading | Only the LCP/above-the-fold image |
| Remote image host not allow-listed | Runtime error | Add it to `images.remotePatterns` |
| Env vars not set on the host | Works locally, 500 in prod | Re-add secrets in the platform dashboard |
| Heavy client lib in first-load JS | Slow LCP/INP | `next/dynamic` with `ssr: false` |
| Self-host ISR on ephemeral FS | Inconsistent revalidation | Persistent volume or custom `cacheHandler` |
| Judging perf only from Lighthouse | Field scores differ | Track real-user Web Vitals |

---

## 🧠 KEY TAKEAWAYS

- The **Metadata API** (`metadata` / `generateMetadata`, server-only) generates SEO tags; set `metadataBase` and use a `title.template`. Add `sitemap.ts`, `robots.ts`, and JSON-LD for full crawlability.
- **`next/image`** auto-optimizes (resize, WebP/AVIF, lazy-load, no layout shift) — always set dimensions and `alt`, allow-list remote hosts, and `priority` only the LCP image.
- **`next/font`** self-hosts fonts at build time (no external request, no layout shift); **`next/script`** controls third-party load timing.
- The #1 performance lever is **shipping less JavaScript**: default to server components, lazy-load heavy client widgets, and watch "First Load JS." Tune toward **LCP / CLS / INP**.
- **Vercel** deploys Next.js with zero config and full feature support; set env vars in its dashboard. **Self-hosting** works via `next start` or a Docker `standalone` image — mind ISR cache persistence and `sharp` for images.
- **Monitor real users** with Web Vitals/analytics and an error APM — field data, not lab data, is what counts.

---

**Prev:** [`07-Auth-And-Full-Stack-Nextjs.md`](./07-Auth-And-Full-Stack-Nextjs.md) · **Next:** _(end of section — back to_ [`00-Index.md`](./00-Index.md)_)_ · **Index:** [`00-Index.md`](./00-Index.md)
