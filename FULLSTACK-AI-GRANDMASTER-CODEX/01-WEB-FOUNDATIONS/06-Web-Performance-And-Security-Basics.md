# ⚡🔒 Web Performance and Security Basics

> *"A slow site loses users; an insecure site loses everything. Both are foundational responsibilities, not afterthoughts."*

You now understand the network (ch.1), HTTP (ch.2), the browser (ch.3), and HTML/CSS (ch.4–5). This final foundations chapter covers two qualities every professional site needs: **performance** (making it fast) and **security** (making it safe). These are introductions — each topic gets deeper treatment in `11-FULLSTACK-ENGINEERING` — but the concepts here are essential vocabulary you'll use immediately.

---

# PART 1 — PERFORMANCE

## I. WHY PERFORMANCE MATTERS

Performance is not vanity. Studies across the industry consistently link slower pages to higher abandonment and lost revenue, and search engines factor speed into rankings. Every extra second of load time costs you users. The good news: most wins come from a handful of well-understood techniques.

The mental model from `03-Browsers-And-Rendering.md` is the key: performance work is about **reducing the number and size of requests, and reducing the work the browser must redo.**

---

## II. CACHING — DON'T FETCH WHAT YOU ALREADY HAVE

**Caching** stores a copy of a resource so it doesn't have to be re-fetched or recomputed. It happens at many levels:

```
Browser cache  →  CDN cache  →  Server/app cache  →  Database cache
  (on device)     (edge)         (in memory)         (query results)
   closest = fastest & cheapest ───────────────────▶ farthest = slowest
```

The closer the cache to the user, the faster. The browser controls its cache via HTTP headers the server sends:

```http
# Cache this for 1 hour; don't re-request until then:
Cache-Control: max-age=3600

# Never cache (for sensitive/always-fresh data):
Cache-Control: no-store

# Cache, but revalidate with the server before using:
Cache-Control: no-cache

# Validation: server sends a fingerprint; browser asks "still valid?" → 304 if unchanged
ETag: "abc123"
```

### Cache busting
Aggressive caching is great until you ship an update and users keep the stale file. The standard fix is **fingerprinting filenames**: `app.a1b2c3.js`. When the content changes, the hash changes, so the URL changes, so the browser fetches the new file — while still caching each version forever. (Build tools like Vite/Webpack do this automatically.)

> **Gotcha:** Cache HTML *carefully* (it points to your fingerprinted assets) but cache fingerprinted JS/CSS/images aggressively (`max-age` of a year). Caching HTML too long means users never see new deployments.

---

## III. CDN — CONTENT CLOSE TO THE USER

A **CDN (Content Delivery Network)** is a global network of servers ("edge locations") that store copies of your static assets near users. Recall from ch.1 that latency is bounded by physical distance — a CDN shrinks that distance.

```
Without CDN:  User in Tokyo ───── 10,000 km ─────▶ Your server in New York   (slow)
With CDN:     User in Tokyo ──▶ Tokyo edge node (cached copy)                 (fast)
```

CDNs also absorb traffic spikes, provide DDoS protection, and handle TLS. Use one for all static assets (images, CSS, JS, fonts). Examples: Cloudflare, Fastly, CloudFront.

---

## IV. REDUCING AND OPTIMIZING REQUESTS

| Technique | What it does |
|---|---|
| **Minification** | Strip whitespace/comments from JS/CSS → smaller files |
| **Compression** | `gzip`/`brotli` shrink text transfers by ~70–90% (server sets `Content-Encoding`) |
| **Bundling (judiciously)** | Combine files to cut request count (less critical with HTTP/2 multiplexing) |
| **Image optimization** | Use modern formats (WebP/AVIF), right-size images, compress |
| **Tree-shaking** | Build tools remove unused code from bundles |
| **Code splitting** | Load only the JS needed for the current page, fetch the rest on demand |

```html
<!-- Responsive images: browser picks the right size, saving bandwidth on small screens -->
<img
  src="photo-800.jpg"
  srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w"
  sizes="(max-width: 600px) 400px, 800px"
  alt="A descriptive caption"
  width="800" height="600"
/>
```

---

## V. LAZY LOADING — DEFER WHAT ISN'T NEEDED YET

**Lazy loading** delays loading resources until they're actually needed (e.g. when they're about to scroll into view). Why download 50 images when the user sees 5?

```html
<!-- Native lazy loading for images and iframes — one attribute, no JS -->
<img src="photo.jpg" alt="..." loading="lazy" width="800" height="600" />
<iframe src="video" loading="lazy"></iframe>
```

```javascript
// For custom lazy loading, the modern API is IntersectionObserver
// (efficient: the browser tells you when an element enters the viewport).
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;   // load the real image now
      observer.unobserve(img);
    }
  });
});
document.querySelectorAll("img[data-src]").forEach(img => observer.observe(img));
```

> **Gotcha:** Don't lazy-load *above-the-fold* content (what's visible without scrolling) or your largest hero image — that delays the very thing the user is waiting for and *hurts* your Largest Contentful Paint. Lazy-load below the fold only.

---

## VI. CORE WEB VITALS (THE METRICS THAT MATTER)

Google's **Core Web Vitals** are the standard user-centric performance metrics:

| Metric | Measures | Good target |
|---|---|---|
| **LCP** (Largest Contentful Paint) | Loading: when the main content appears | < 2.5 s |
| **INP** (Interaction to Next Paint) | Responsiveness: delay before UI responds to input | < 200 ms |
| **CLS** (Cumulative Layout Shift) | Visual stability: how much content jumps around | < 0.1 |

```html
<!-- Preventing CLS: always set width/height (or aspect-ratio) so the browser
     reserves space and content doesn't "jump" when the image loads. -->
<img src="banner.jpg" alt="..." width="1200" height="400" />
```

Measure with Chrome DevTools → **Lighthouse**, or the Performance panel. You can't improve what you don't measure.

---

# PART 2 — SECURITY

## VII. THE SECURITY MINDSET

> **The golden rule: never trust the client.** Anything from the browser — form inputs, URLs, headers, cookies — can be forged by an attacker using curl, Postman, or DevTools. All validation and authorization that *matters* must happen on the server.

Most web vulnerabilities come from **mixing untrusted data with trusted contexts** (data treated as code, or one site acting on behalf of another). The big four below are the ones every developer must know.

---

## VIII. XSS — CROSS-SITE SCRIPTING

**XSS** is when an attacker injects malicious JavaScript that runs in *other users'* browsers, in the context of your trusted site. That script can steal cookies/tokens, log keystrokes, or impersonate the user.

### How it happens
You render user-supplied content as HTML without sanitizing it:

```javascript
// ❌ VULNERABLE: user input inserted as raw HTML
const comment = getUserInput();          // attacker submits: <img src=x onerror="steal(document.cookie)">
element.innerHTML = comment;             // the injected script now runs for every viewer!
```

### How to prevent it
```javascript
// ✅ Use textContent — inserts as TEXT, not HTML. The browser won't execute it.
element.textContent = comment;           // <img...> shows as literal text, harmless

// ✅ If you must render HTML, sanitize it with a vetted library (e.g. DOMPurify)
element.innerHTML = DOMPurify.sanitize(comment);
```

**Defenses, layered:**
1. **Escape/encode output by context** — frameworks like React do this automatically (`{userInput}` in JSX is auto-escaped). This is the #1 reason to render via a framework rather than raw `innerHTML`.
2. **Sanitize** any HTML you genuinely must allow (use a maintained sanitizer; don't roll your own).
3. **`HttpOnly` cookies** — so injected JS can't read auth cookies (see ch.2).
4. **Content Security Policy (CSP)** — an HTTP header that restricts which scripts may run:
```http
Content-Security-Policy: default-src 'self'; script-src 'self'
```

> **React/JSX note:** `{value}` is auto-escaped and safe. The escape hatch `dangerouslySetInnerHTML` bypasses that protection — its scary name is a deliberate warning. Sanitize before using it.

---

## IX. CSRF — CROSS-SITE REQUEST FORGERY

**CSRF** tricks a logged-in user's browser into making an unwanted request to your site. Because browsers *automatically* attach cookies, a request from a malicious site can ride on the victim's existing session.

### How it happens
```html
<!-- Victim is logged into bank.com. They visit evil.com, which contains: -->
<img src="https://bank.com/transfer?to=attacker&amount=1000" />
<!-- The browser sends the request WITH the victim's bank.com cookies attached.
     If the server trusts the cookie alone, the transfer succeeds. -->
```

### How to prevent it
1. **`SameSite` cookies** (the modern default defense): `SameSite=Strict` or `Lax` tells the browser *not* to send the cookie on cross-site requests.
```http
Set-Cookie: session=abc; HttpOnly; Secure; SameSite=Strict
```
2. **Anti-CSRF tokens** — the server embeds a random, per-session token in forms; requests without the matching token are rejected. An attacker's site can't know the token.
3. **Require non-cookie auth for state-changing APIs** — e.g. a token in an `Authorization` header (which browsers don't auto-attach cross-site).
4. **Respect HTTP semantics** — GET must never change state (recall ch.2), so it can't be weaponized via an `<img>`/link.

> **XSS vs CSRF in one line:** XSS = the attacker runs *their script* on *your site*. CSRF = the attacker makes *the victim's browser* send a *forged request* using the victim's session. XSS is generally the more dangerous (it can defeat CSRF tokens too), so fix XSS first.

---

## X. CORS — CROSS-ORIGIN RESOURCE SHARING

**CORS** is frequently misunderstood. It is *not* an attack — it's a browser **security feature** you'll constantly bump into when your frontend and backend are on different origins.

### The Same-Origin Policy
By default, browsers block JavaScript on one **origin** from reading responses from a *different* origin. An **origin** = scheme + host + port. These are all different origins:
```
https://app.com          vs   http://app.com          (different scheme)
https://app.com          vs   https://api.app.com      (different host)
https://app.com           vs   https://app.com:8080     (different port)
```
This stops a malicious site from silently reading your bank's API using your session.

### Where CORS comes in
When your frontend (`https://app.com`) legitimately needs to call your API (`https://api.app.com`), the *server* must opt in by sending CORS headers permitting it:

```http
# Server response headers that allow the cross-origin request:
Access-Control-Allow-Origin: https://app.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

For "non-simple" requests (e.g. with custom headers or methods like PUT/DELETE), the browser first sends a **preflight** `OPTIONS` request to ask permission, then the real request if allowed.

```javascript
// Express: enable CORS for your frontend's origin
const cors = require("cors");
app.use(cors({ origin: "https://app.com", credentials: true }));
```

> **Gotcha #1:** The dreaded *"blocked by CORS policy"* error in the console is a **server** configuration issue, not a frontend bug — the *server* must send the right `Access-Control-Allow-*` headers. You can't fix it purely in frontend code.
>
> **Gotcha #2:** `Access-Control-Allow-Origin: *` (allow everyone) is convenient but insecure for authenticated APIs, and it *cannot* be combined with `credentials: true`. Specify exact trusted origins for anything sensitive.

---

## XI. HTTPS AND OTHER ESSENTIAL DEFENSES

- **HTTPS everywhere** (ch.2) — encrypts traffic; mandatory. Redirect all HTTP → HTTPS. Use **HSTS** (`Strict-Transport-Security`) to force browsers to always use HTTPS.
- **Never trust client input** — validate and sanitize on the server, *always*.
- **Use parameterized queries / prepared statements** to prevent **SQL injection** (the database analog of XSS — covered in `08-SQL-DATABASES`). Never build SQL by string concatenation with user input.
- **Hash passwords** with a slow, salted algorithm (bcrypt/argon2) — never store plaintext (covered in `11-FULLSTACK-ENGINEERING`).
- **Keep dependencies updated** — most breaches exploit known vulnerabilities in outdated packages. Run `npm audit`; pin versions.
- **Don't leak secrets** — API keys and credentials belong in server-side environment variables, never in frontend code or committed to Git.
- **Set security headers** — CSP, `X-Content-Type-Options: nosniff`, `X-Frame-Options` (anti-clickjacking). Helmet automates these for Express.

> **Security note for network services:** any endpoint you expose without authentication is reachable by anyone who finds it. Default to requiring auth on anything that reads or writes real data, and treat "open by default" as a deliberate, justified choice — not an accident.

---

## XII. COMMON PITFALLS / GOTCHAS

**Performance**
- Lazy-loading above-the-fold content → hurts LCP. Lazy-load below the fold only.
- Caching HTML too aggressively → users never get new deploys. Fingerprint assets, cache HTML carefully.
- Shipping unoptimized images → often the single biggest payload. Compress, resize, use modern formats.
- Not setting image `width`/`height` → layout shift (bad CLS).

**Security**
- Trusting client-side validation for security → always re-validate on the server.
- Using `innerHTML` with user data → XSS. Use `textContent` or sanitize.
- Relying on cookies alone for state-changing requests → CSRF. Use `SameSite` + tokens.
- `Access-Control-Allow-Origin: *` on authenticated APIs → over-exposure. Whitelist origins.
- Storing secrets in frontend code → anyone can read them. Server-side env vars only.
- Thinking CORS errors are a frontend bug → it's server configuration.

---

## ✅ KEY TAKEAWAYS

**Performance**
- Performance = **fewer/smaller requests + less browser rework**. Use **caching** (closest cache wins; fingerprint assets for cache-busting), a **CDN** (content near the user), **minification/compression**, **image optimization**, and **lazy loading** (below the fold only).
- Track **Core Web Vitals**: **LCP** (loading < 2.5s), **INP** (responsiveness < 200ms), **CLS** (visual stability < 0.1). Measure with Lighthouse — you can't improve what you don't measure.

**Security**
- **Never trust the client** — all meaningful validation and authorization happen server-side.
- **XSS** = injected script runs on your site → escape output (frameworks auto-escape), sanitize HTML, use `HttpOnly` cookies + CSP.
- **CSRF** = forged request rides the victim's session → `SameSite` cookies, anti-CSRF tokens, keep GET side-effect-free.
- **CORS** is a browser *protection* (Same-Origin Policy), not an attack; cross-origin calls require the **server** to send `Access-Control-Allow-*` headers. `*` + credentials is forbidden.
- Layer in **HTTPS/HSTS**, parameterized queries (anti-SQL-injection), password hashing, dependency updates, secret management, and security headers.

---

🎉 **You've completed Web Foundations!** You now understand the full journey — network → HTTP → browser → HTML → CSS → performance & security. You're ready for the language that brings it all to life.

**→ Next section:** [`../02-JAVASCRIPT-MASTERY/00-Index.md`](../02-JAVASCRIPT-MASTERY/00-Index.md) — JavaScript from zero to expert *(coming in this codex)*
**← Prev:** [`05-CSS-Essentials.md`](./05-CSS-Essentials.md)
**🗺️ Index:** [`00-Index.md`](./00-Index.md)
