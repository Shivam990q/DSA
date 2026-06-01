# 🟢 07 — Authentication & Security

> *"You will write code that is read by everyone — including attackers. Treat every input as hostile, every secret as already leaking, every user as a potential adversary. Then build something kind for the honest 99%."*

> ⚠️ **Security warning.** This file shows real-world patterns. Code that handles passwords, tokens, and cookies has very narrow correct shapes. Read it twice, copy-paste carefully, and never invent your own crypto.

**Prev:** [`06-Middleware-And-Error-Handling.md`](./06-Middleware-And-Error-Handling.md) · **Next:** [`08-Advanced-Node-And-Deployment.md`](./08-Advanced-Node-And-Deployment.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. AUTHN vs AUTHZ — KNOW THE DIFFERENCE

| Term | Question it answers |
|------|---------------------|
| **Authentication (authn)** | "Who are you?" |
| **Authorization (authz)** | "Are you allowed to do this?" |

A login form is **authentication**. The middleware that says "only admins can DELETE this" is **authorization**. They are independent concerns; mixing them up is how access-control bugs ship.

---

## II. PASSWORDS — NEVER STORE THEM, EVER

Storing plaintext passwords is malpractice. Storing them with `sha256` is also wrong (fast → brute-forceable). Use a **slow, salted KDF**: **bcrypt** (default), **scrypt**, or **argon2** (modern best).

### `bcrypt` — the safe default

```bash
npm install bcrypt
```

```js
import bcrypt from "bcrypt";

const COST = 12;                                   // ~250ms on a laptop in 2024 — adjust by year

const hash = await bcrypt.hash("hunter2", COST);   // returns "$2b$12$...." — salt is BAKED IN
const ok   = await bcrypt.compare("hunter2", hash);
```

What's stored is `$2b$12$<salt><hash>`. Bcrypt:

- generates a unique salt per password (defends against rainbow tables),
- iterates 2^cost times (`cost=12` ≈ ~4096 iterations, slow on purpose),
- is **non-reversible** — only `bcrypt.compare` can verify.

> **Rule:** never write your own password hashing. **bcrypt** or **argon2id** only. Never store the salt separately — bcrypt embeds it.

### `argon2id` — modern alternative

```bash
npm install argon2
```

```js
import argon2 from "argon2";
const hash = await argon2.hash("hunter2", { type: argon2.argon2id });
const ok   = await argon2.verify(hash, "hunter2");
```

Argon2id wins memory-hardness benchmarks; bcrypt wins ubiquity. Either is fine.

### Password policies that don't suck

- **Length matters more than complexity.** Allow 12+ chars. Don't force a digit and a symbol.
- **Check breach lists** (`haveibeenpwned` Pwned Passwords API).
- **Don't truncate**. Don't strip characters.
- **Rate limit** login attempts per IP and per username.
- **Never reveal** which field was wrong — "Invalid email or password" is the only safe response.

---

## III. SESSIONS vs JWT — TWO PATHS

You have to decide once per project: **sessions** (state on server) or **stateless tokens (JWT)**.

| | Sessions | JWT |
|---|----------|-----|
| Server state | Yes (DB / Redis) | No |
| Revocation | Trivial (delete row) | Hard (need a denylist) |
| Mobile / cross-domain | Cookie limitations | Easy |
| Microservices | Each service hits the session store | Each service verifies a signature |
| Default for traditional web apps | ✅ | — |
| Default for SPAs / mobile | — | ✅ (with care) |

**Pragmatic recommendation:**

- **Cookie session for browser-only apps** — simple, secure with the right cookie flags.
- **Short-lived JWT access tokens + opaque refresh tokens** for APIs consumed by mobile apps or multiple frontends.
- **Don't store JWTs in `localStorage`** — XSS reads it. Use **HttpOnly cookies** even for JWTs when possible.

---

## IV. SESSIONS WITH `express-session`

```bash
npm install express-session connect-redis ioredis
```

```js
import session from "express-session";
import RedisStore from "connect-redis";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

app.use(session({
  store: new RedisStore({ client: redis, prefix: "sess:" }),
  name: "sid",
  secret: process.env.SESSION_SECRET,        // long random string from a secret manager
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,             // JS can't read it (defends against XSS theft)
    secure:   process.env.NODE_ENV === "production",  // HTTPS only
    sameSite: "lax",            // 'lax' | 'strict' | 'none' — see CSRF section
    maxAge:   1000 * 60 * 60 * 24 * 7   // 1 week
  }
}));
```

```js
// login
app.post("/auth/login", async (req, res) => {
  const user = await verifyCredentials(req.body);  // bcrypt.compare
  if (!user) return res.status(401).json({ error: "Invalid credentials" });

  // Session fixation defense — regenerate the session ID on login
  req.session.regenerate((err) => {
    if (err) return res.status(500).end();
    req.session.userId = user.id;
    res.json({ ok: true });
  });
});

// logout
app.post("/auth/logout", (req, res) => {
  req.session.destroy(() => res.clearCookie("sid").json({ ok: true }));
});
```

> **Always regenerate session IDs on login** to defeat session-fixation. **Always destroy sessions on logout.**

---

## V. JWT — JSON WEB TOKENS, DONE PROPERLY

A JWT is `header.payload.signature`. You sign with a secret (HMAC) or a private key (RSA/EC). Anyone with the public secret/key can verify it.

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0MiIsImlhdCI6MTcwMDAwMDAwMH0.SIGNATURE
─── header ──── ─────── payload (base64) ──────── ────── HMAC ──────
```

Decode (not verify!) at <https://jwt.io>.

```bash
npm install jsonwebtoken
```

```js
import jwt from "jsonwebtoken";

const ACCESS_SECRET  = process.env.JWT_ACCESS_SECRET;   // 64+ random bytes
const REFRESH_SECRET = process.env.JWT_REFRESH_SECRET;  // different from access

export const signAccess  = (user) => jwt.sign(
  { sub: user.id, role: user.role },
  ACCESS_SECRET,
  { expiresIn: "15m", issuer: "myapp", audience: "myapp.web" }
);

export const signRefresh = (user, jti) => jwt.sign(
  { sub: user.id, jti },                   // jti = unique id we can revoke
  REFRESH_SECRET,
  { expiresIn: "30d", issuer: "myapp", audience: "myapp.web" }
);

export const verifyAccess = (token) => jwt.verify(token, ACCESS_SECRET, {
  issuer: "myapp", audience: "myapp.web"
});
```

### Auth middleware

```js
// middleware/auth.js
import jwt from "jsonwebtoken";

export const requireAuth = (req, res, next) => {
  const header = req.headers.authorization ?? "";
  const token  = header.startsWith("Bearer ") ? header.slice(7) : null;
  if (!token) return res.status(401).json({ error: "Missing token" });

  try {
    const payload = jwt.verify(token, process.env.JWT_ACCESS_SECRET, {
      issuer: "myapp", audience: "myapp.web"
    });
    req.user = { id: payload.sub, role: payload.role };
    next();
  } catch (err) {
    res.status(401).json({ error: "Invalid or expired token" });
  }
};
```

### Refresh-token rotation (the safe pattern)

The access token is **short-lived (5–15 min)**. The refresh token is **long-lived (days–weeks)**, stored as an **HttpOnly cookie** (or in mobile keychain), and **rotated on every use**.

```js
// routes/auth.routes.js
import { Router } from "express";
import { randomUUID } from "node:crypto";
import jwt from "jsonwebtoken";
import { signAccess, signRefresh } from "../lib/tokens.js";
import { db } from "../lib/db.js";

const router = Router();

router.post("/login", async (req, res) => {
  const user = await verifyCredentials(req.body);   // bcrypt.compare
  if (!user) return res.status(401).json({ error: "Invalid credentials" });

  const jti = randomUUID();
  await db.refreshToken.create({ data: { jti, userId: user.id, expiresAt: thirtyDays() } });

  res.cookie("rt", signRefresh(user, jti), {
    httpOnly: true, secure: true, sameSite: "lax",
    maxAge: 30 * 24 * 3600 * 1000, path: "/auth"
  });
  res.json({ accessToken: signAccess(user) });
});

router.post("/refresh", async (req, res) => {
  const rt = req.cookies?.rt;
  if (!rt) return res.status(401).json({ error: "No refresh token" });

  let payload;
  try { payload = jwt.verify(rt, process.env.JWT_REFRESH_SECRET); }
  catch { return res.status(401).json({ error: "Invalid refresh token" }); }

  // Look up the JTI; rotate (delete old, issue new). If JTI is missing, REVOKE everything for that user (token reuse detected).
  const stored = await db.refreshToken.findUnique({ where: { jti: payload.jti } });
  if (!stored) {
    await db.refreshToken.deleteMany({ where: { userId: payload.sub } });
    return res.status(401).json({ error: "Reuse detected — all sessions revoked" });
  }

  await db.refreshToken.delete({ where: { jti: payload.jti } });
  const newJti = randomUUID();
  await db.refreshToken.create({ data: { jti: newJti, userId: payload.sub, expiresAt: thirtyDays() } });

  const user = { id: payload.sub, role: stored.role };
  res.cookie("rt", signRefresh(user, newJti), {
    httpOnly: true, secure: true, sameSite: "lax",
    maxAge: 30 * 24 * 3600 * 1000, path: "/auth"
  });
  res.json({ accessToken: signAccess(user) });
});

router.post("/logout", async (req, res) => {
  // Best effort: revoke this refresh token. Always clear the cookie.
  try {
    const rt = req.cookies?.rt;
    if (rt) {
      const p = jwt.verify(rt, process.env.JWT_REFRESH_SECRET);
      await db.refreshToken.delete({ where: { jti: p.jti } }).catch(() => {});
    }
  } finally {
    res.clearCookie("rt", { path: "/auth" }).status(204).end();
  }
});
```

### JWT pitfalls — read carefully

| Pitfall | Why it bites | Fix |
|---------|--------------|-----|
| Storing JWT in `localStorage` | XSS reads it instantly | Use HttpOnly cookies, or accept the risk + iron-clad CSP |
| `none` algorithm | Forged tokens | Always specify `algorithm` in `verify` |
| Same secret for access and refresh | Token confusion | Two different secrets / keys |
| Long-lived access tokens | Can't revoke | Keep them ≤ 15m |
| No `iss` / `aud` checks | Token from another app accepted | Set + verify both |
| Putting secrets in payload | JWT payload is base64, **not encrypted** | Never; use a session for secrets |
| Forgetting `expiresIn` | Tokens valid forever | Always set it |
| Using `HS256` with a weak secret | Brute-force | 64+ random bytes |

---

## VI. OAUTH 2.0 / OPENID CONNECT — IN ONE PAGE

OAuth 2.0 is **delegated authorization** — "Let App X act on my behalf at Service Y." OpenID Connect (OIDC) layers **identity** (login with Google/GitHub/...) on top of OAuth.

The flow you'll use almost always: **Authorization Code with PKCE**.

```
1. User clicks "Sign in with Google"
2. Your app redirects to Google's /authorize with response_type=code, scope, redirect_uri, code_challenge
3. User logs in at Google
4. Google redirects back to your /callback?code=...
5. Your server POSTs code + code_verifier to Google's /token endpoint, gets id_token + access_token
6. You verify id_token (signature, iss, aud, exp), look up / create the user, issue YOUR session/JWT
```

In Express, the easiest path is **Passport.js** with `passport-google-oauth20` (or `passport-github2`, `passport-microsoft`):

```bash
npm install passport passport-google-oauth20 express-session
```

```js
import passport from "passport";
import { Strategy as GoogleStrategy } from "passport-google-oauth20";

passport.use(new GoogleStrategy({
  clientID:     process.env.GOOGLE_CLIENT_ID,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  callbackURL:  "https://api.example.com/auth/google/callback",
  scope:        ["profile", "email"]
}, async (_at, _rt, profile, done) => {
  const user = await upsertUserFromGoogle(profile);
  done(null, user);
}));

passport.serializeUser  ((user, done) => done(null, user.id));
passport.deserializeUser(async (id, done) => done(null, await db.user.findUnique({ where: { id } })));

app.use(passport.initialize());
app.use(passport.session());

app.get("/auth/google",          passport.authenticate("google"));
app.get("/auth/google/callback", passport.authenticate("google", { failureRedirect: "/login" }),
  (req, res) => res.redirect("/dashboard"));
```

> **Modern alternative:** delegate to a managed identity service like **Auth0**, **Clerk**, **Supabase Auth**, **AWS Cognito**, or **Keycloak**. Lower risk than rolling your own.

---

## VII. AUTHORIZATION — RBAC AND ABAC

### Role-Based Access Control (RBAC)

```js
// middleware/requireRole.js
export const requireRole = (...allowed) => (req, res, next) => {
  if (!req.user)                          return res.status(401).end();
  if (!allowed.includes(req.user.role))   return res.status(403).end();
  next();
};

router.delete("/users/:id", requireAuth, requireRole("admin"), ctrl.removeUser);
```

### Resource-level checks (ownership)

```js
// "Only the owner or an admin can update this todo"
export const canEditTodo = async (req, res, next) => {
  const todo = await db.todo.findUnique({ where: { id: Number(req.params.id) } });
  if (!todo) return res.status(404).end();
  const isOwner = todo.userId === req.user.id;
  const isAdmin = req.user.role === "admin";
  if (!isOwner && !isAdmin) return res.status(403).end();
  req.todo = todo;
  next();
};

router.put("/todos/:id", requireAuth, canEditTodo, ctrl.update);
```

### Attribute-Based (ABAC) and policy engines

For complex rules ("manager can read tickets in their department, on weekdays, after onboarding"), reach for a policy engine: **CASL** (JS), **Oso**, or **Open Policy Agent**. Don't try to express that in if-statements.

> **Rule (very important):** **never** trust a client-sent `userId` for authorization. Always read `req.user.id` from the verified token/session.

---

## VIII. SECURITY MIDDLEWARE — THE BIG SIX

### 1. `helmet` — sensible HTTP security headers

```bash
npm install helmet
```

```js
import helmet from "helmet";
app.use(helmet());                   // a stack of best-practice headers

// CSP — opt-in, tune for your app
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc:  ["'self'"],
    styleSrc:   ["'self'", "'unsafe-inline'"],
    imgSrc:     ["'self'", "data:"],
    connectSrc: ["'self'", "https://api.example.com"]
  }
}));
```

Headers helmet sets (excerpt):

| Header | Defends against |
|--------|-----------------|
| `Strict-Transport-Security` | Protocol downgrade |
| `X-Content-Type-Options: nosniff` | MIME sniffing |
| `X-Frame-Options: DENY` | Clickjacking |
| `Referrer-Policy` | Referer leaks |
| `Content-Security-Policy` | XSS — the big one |

### 2. `cors` — Cross-Origin Resource Sharing

```bash
npm install cors
```

```js
import cors from "cors";
app.use(cors({
  origin: ["https://app.example.com", /\.example\.com$/],
  credentials: true,                                // required if you send cookies
  methods: ["GET", "POST", "PUT", "PATCH", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"]
}));
```

Beware: `Access-Control-Allow-Origin: *` + `credentials: true` is rejected by browsers. Always specify exact origins when you use cookies.

### 3. Rate limiting — `express-rate-limit`

```bash
npm install express-rate-limit
```

```js
import { rateLimit } from "express-rate-limit";

// Global lighter limiter
app.use(rateLimit({ windowMs: 60_000, max: 120, standardHeaders: true, legacyHeaders: false }));

// Stricter limit on auth endpoints
const loginLimiter = rateLimit({ windowMs: 15 * 60_000, max: 10, standardHeaders: true });
app.use("/auth/login", loginLimiter);
```

In production, back the limiter with **Redis** (`rate-limit-redis`) so multiple Node processes share counters.

### 4. Input sanitization — `xss`, `dompurify`, `validator`

For JSON APIs, **proper output encoding in the frontend** beats input sanitization (don't mangle the user's data). For HTML bodies (rich text, comments), sanitize before storage:

```bash
npm install isomorphic-dompurify
```

```js
import DOMPurify from "isomorphic-dompurify";
const safe = DOMPurify.sanitize(req.body.html);
```

For Mongo apps, use **`express-mongo-sanitize`** to strip `$`/`.` in input keys (defends against operator injection).

### 5. HTTP Parameter Pollution — `hpp`

```bash
npm install hpp
```

```js
import hpp from "hpp";
app.use(hpp());
```

Prevents `?role=user&role=admin` from confusing your code (the second `role` won by default).

### 6. CSRF — `csurf` (deprecated, use a maintained fork) or **double-submit cookie**

CSRF matters when you authenticate with **cookies**. JWT-in-Authorization-header APIs are immune (browsers don't auto-send Authorization).

The **double-submit cookie** pattern: server sets a CSRF cookie; clients must send the same value in a header (e.g. `X-CSRF-Token`). Server checks they match.

```js
// On login, set a non-HttpOnly CSRF cookie:
res.cookie("csrfToken", token, { sameSite: "lax", secure: true });

// Middleware on mutating routes:
export const csrfCheck = (req, res, next) => {
  const cookie = req.cookies?.csrfToken;
  const header = req.get("X-CSRF-Token");
  if (!cookie || cookie !== header) return res.status(403).end();
  next();
};
```

> **`SameSite=Lax` cookies** block most CSRF for top-level navigations automatically. Combined with the double-submit pattern, you're solid.

---

## IX. OWASP TOP 10 — IN PRACTICE

The OWASP Top 10 (current era) maps onto Node concerns like this:

| OWASP item | What it means in Node |
|------------|------------------------|
| **A01 Broken Access Control** | Trusting `req.body.userId`; missing `requireRole`; IDOR | Always use `req.user.id`; check ownership |
| **A02 Cryptographic Failures** | Plaintext passwords, weak JWT secrets, no TLS | bcrypt/argon2; long random secrets; HTTPS everywhere |
| **A03 Injection** | SQLi, NoSQLi, command injection | Parameterized queries; never `eval`/`exec` user input; validate everything |
| **A04 Insecure Design** | Auth/authz bolted on late | Threat-model early; least privilege |
| **A05 Security Misconfiguration** | `debug` enabled in prod, default secrets, missing helmet | `NODE_ENV=production`, helmet, env-validated config |
| **A06 Vulnerable Components** | Outdated `express`, `lodash`, etc. | `npm audit`, Dependabot, lockfile |
| **A07 Identification & Authn Failures** | Weak passwords, no rate limit, no MFA | Strong passwords, rate limit, MFA, lockouts |
| **A08 Software & Data Integrity** | Trusting `JSON.parse` of untrusted YAML/pickle/RCE chains | Avoid risky deserialization; sign artifacts |
| **A09 Logging & Monitoring Failures** | No alerts for repeated failures | Structured logs + alerts on auth failures, 5xx spikes |
| **A10 SSRF** | Server fetches user-supplied URL → internal network | URL allowlists; block private IP ranges; Linkerd/proxy controls |

### Specific Node-flavored attacks to know

- **Prototype pollution.** Merging untrusted input into objects (`Object.assign`, `lodash.merge`) can set `__proto__.foo` and pollute every object. **Mitigate:** use `Object.create(null)`, structured cloning, or schema-based parsing (zod) that strips unknown keys.

```js
// BAD — prototype pollution risk if input contains "__proto__"
Object.assign({}, untrusted);

// SAFER — zod parses to a typed shape, dropping unknown keys
const safe = schema.parse(untrusted);
```

- **ReDoS (regex denial of service).** Catastrophic backtracking on patterns like `(a+)+$`. Use `RegExp` test timeouts (Node 21+ has `re.exec` with limits) or `safe-regex` to lint.
- **Command injection.** Don't pass user input to `child_process.exec`. Use `execFile`/`spawn` with arg arrays, or escape rigorously.
- **Path traversal.** When serving files by name, **`path.join(root, name)` is not enough** — `name` could be `../../etc/passwd`. Compute with `path.resolve` then check it starts with `root`:

```js
import path from "node:path";
const rootDir = path.resolve("./uploads");
const target  = path.resolve(rootDir, req.params.name);
if (!target.startsWith(rootDir + path.sep)) return res.status(400).end();
res.sendFile(target);
```

- **SSRF.** Resolve user-supplied URLs to IPs; reject private ranges (`10.0.0.0/8`, `192.168.0.0/16`, `127.0.0.0/8`, `169.254.0.0/16`, IPv6 link-locals). Use a vetted lib like `ssrf-req-filter`.

---

## X. SECRETS, CONFIG & THE 12-FACTOR APP

> **Rule:** code in git, secrets in a vault.

```bash
npm install dotenv
```

```bash
# .env (gitignored!)
DATABASE_URL=postgres://user:pass@localhost:5432/app
JWT_ACCESS_SECRET=<64+ random hex chars>
JWT_REFRESH_SECRET=<different 64+ random hex chars>
COOKIE_SECRET=<64+ random hex chars>
SESSION_SECRET=<64+ random hex chars>
NODE_ENV=development
PORT=3000
CORS_ORIGIN=http://localhost:5173
```

```js
// config/env.js — validate on boot, fail fast
import "dotenv/config";
import { z } from "zod";

const Schema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT:     z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_ACCESS_SECRET:  z.string().min(32),
  JWT_REFRESH_SECRET: z.string().min(32),
  COOKIE_SECRET:      z.string().min(32),
  CORS_ORIGIN: z.string().url()
});

export const env = Schema.parse(process.env);
```

In **production**, never use `.env` files — inject via your deployment platform (AWS/GCP/Azure secrets, Doppler, Vault, Kubernetes secrets, Docker secrets). Generate strong secrets:

```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

> **If a secret leaks into a git commit, rotate it.** Removing the commit is not enough — assume the world has it.

---

## XI. FILE UPLOADS — `multer`, SAFELY

```bash
npm install multer
```

```js
// middleware/upload.js
import multer from "multer";
import path from "node:path";
import { randomUUID } from "node:crypto";

const ALLOWED = new Set(["image/jpeg", "image/png", "image/webp"]);

export const upload = multer({
  storage: multer.diskStorage({
    destination: "./uploads",
    filename: (_req, file, cb) =>
      cb(null, randomUUID() + path.extname(file.originalname).toLowerCase())
  }),
  limits: { fileSize: 5 * 1024 * 1024, files: 1 },         // 5 MB
  fileFilter: (_req, file, cb) => {
    if (!ALLOWED.has(file.mimetype)) return cb(new Error("Unsupported file type"));
    cb(null, true);
  }
});

// route
router.post("/avatar", requireAuth, upload.single("avatar"), (req, res) => {
  res.json({ url: `/uploads/${req.file.filename}` });
});
```

### Upload safety checklist

- **Whitelist** mime types — never blacklist.
- **Cap size** with `limits.fileSize` and configure your reverse proxy too (`client_max_body_size`).
- **Rename files** to a UUID so `../../evil.png` can't escape and `report.html` can't be served as HTML.
- **Don't trust** `file.originalname` for anything but display.
- **Re-encode images** with `sharp` if you want to strip embedded payloads / EXIF.
- For real apps, store files in **S3 / GCS / R2** (presigned uploads), not on the app server's disk.

---

## XII. HTTPS & COOKIE FLAGS

In production, terminate TLS at a reverse proxy (Nginx, Caddy, AWS ALB, Cloudflare). Set:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

(helmet does this for you).

For cookies (sessions, refresh tokens, CSRF), the four flags that matter:

| Flag | What it does | Recommended value |
|------|--------------|-------------------|
| `HttpOnly` | JS cannot read the cookie | `true` (almost always) |
| `Secure` | Only sent over HTTPS | `true` in prod |
| `SameSite` | Restricts cross-site sending | `Lax` (or `Strict` for high-risk) |
| `Path` / `Domain` | Where the cookie applies | `/` for sessions, `/auth` for refresh |

If you must allow cross-origin (e.g. SPA on a different domain), use `SameSite=None; Secure` and **always** check origin/CSRF.

---

## XIII. TWO-FACTOR (TOTP) IN ~20 LINES

```bash
npm install otplib qrcode
```

```js
import { authenticator } from "otplib";
import qrcode from "qrcode";

// 1. Enroll: server creates a secret, user scans the QR code
const secret = authenticator.generateSecret();
const otpauth = authenticator.keyuri(user.email, "MyApp", secret);
const qr = await qrcode.toDataURL(otpauth);
await db.user.update({ where: { id: user.id }, data: { totpSecret: secret } });

// 2. Verify on login
const ok = authenticator.verify({ token: req.body.code, secret: user.totpSecret });
if (!ok) return res.status(401).json({ error: "Invalid code" });
```

Pair with **recovery codes** (10 single-use random codes printed once) and store them hashed.

---

## XIV. DEPENDENCIES ARE A SECURITY SURFACE

- Run `npm audit` and treat **high/critical** like P0 bugs.
- Use **Dependabot** or **Renovate** for automated bumps.
- Use **`npm ci --ignore-scripts`** in CI to skip risky install scripts.
- Pin versions, commit the lockfile, vendor critical deps if regulated.
- **Don't paste random `npm install` commands** from blog posts. Verify the package: weekly downloads, GitHub stars, last release date, maintainers.

---

## XV. WORKED EXAMPLE — A SECURE LOGIN ENDPOINT

```js
// routes/auth.routes.js
import { Router } from "express";
import bcrypt from "bcrypt";
import { rateLimit } from "express-rate-limit";
import { z } from "zod";
import { signAccess, signRefresh } from "../lib/tokens.js";
import { db } from "../lib/db.js";
import { validateBody } from "../middleware/validate.js";

const router = Router();

const loginLimiter = rateLimit({
  windowMs: 15 * 60_000,
  max: 10,                    // 10 attempts per 15 min per IP
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Too many attempts. Try again later." }
});

const loginSchema = z.object({
  email:    z.string().email().toLowerCase().trim(),
  password: z.string().min(8).max(200)
});

router.post("/login", loginLimiter, validateBody(loginSchema), async (req, res) => {
  const { email, password } = req.body;

  const user = await db.user.findUnique({ where: { email } });
  // ALWAYS run bcrypt.compare to keep timing constant — even when user is missing
  const dummy = "$2b$12$0123456789012345678901aabbccddeeffgghhiijjkkllmmnnoo";
  const ok    = await bcrypt.compare(password, user?.passwordHash ?? dummy);

  if (!user || !ok) {
    req.log?.warn({ email }, "login failed");
    return res.status(401).json({ error: "Invalid credentials" });
  }
  if (user.locked) return res.status(423).json({ error: "Account locked" });

  // Issue tokens
  const jti = crypto.randomUUID();
  await db.refreshToken.create({ data: { jti, userId: user.id, expiresAt: thirtyDays() } });

  res.cookie("rt", signRefresh(user, jti), {
    httpOnly: true, secure: true, sameSite: "lax", path: "/auth",
    maxAge: 30 * 24 * 3600 * 1000
  });
  res.json({ accessToken: signAccess(user), user: toPublicUser(user) });
});

export default router;
```

Notice: **rate limit, schema validation, constant-time compare, generic error message, structured log, secret cookie flags, refresh-token tracked in DB**. That is one route doing the full job.

---

## XVI. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Plaintext or `sha256` passwords | Catastrophic on a leak | bcrypt or argon2id |
| JWT in `localStorage` | XSS owns your sessions | HttpOnly cookies (or live with it + iron-clad CSP) |
| Same secret for access/refresh | Token confusion | Two distinct secrets/keys |
| Missing `expiresIn` | Tokens valid forever | Always set + verify it |
| Trusting `req.body.userId` | IDOR / privilege escalation | Use `req.user.id` from verified token |
| `Access-Control-Allow-Origin: *` with credentials | Browser rejects; or worse, accepts | Specific origin + `credentials: true` |
| Logging tokens or passwords | Secrets in log files | Redact in pino/winston |
| `eval`/`Function`/`exec` of user input | RCE | Don't. Ever. |
| `JSON.parse` of untrusted YAML/pickle | RCE chain | Stick to JSON; validate after parsing |
| Unbounded JSON body | DoS via huge body | `express.json({ limit: "1mb" })` |
| Missing rate limit on login | Credential stuffing | `express-rate-limit` (+ Redis in prod) |
| File serving by user-controlled name | Path traversal | `path.resolve` + prefix check |
| Forgetting CSRF on cookie-auth APIs | State-changing XSRF | SameSite=Lax + double-submit CSRF |
| Exposing stack traces in 500s | Info disclosure | Sanitize errors in prod |
| Node out of date | Known CVEs | Use Active LTS; keep updated |

---

## 🧠 KEY TAKEAWAYS

- **Authn vs authz** are different problems. Solve them separately.
- Hash passwords with **bcrypt** (cost ≥ 12) or **argon2id**. Never roll your own.
- **Sessions** are great for browsers; **JWT (short access + rotated refresh)** for APIs. Don't put JWTs in `localStorage` if you can avoid it.
- **OAuth/OIDC** for "sign in with X" — use a vetted library (Passport) or a managed provider.
- The big six: **helmet, cors, rate limiting, hpp, sanitization, CSRF (when using cookies)**.
- Authorization checks live on the **server**, **per resource**, using `req.user.id`. Never trust client-supplied IDs.
- Validate every input with **zod**; protect against prototype pollution, ReDoS, command injection, path traversal, SSRF.
- Secrets live in env/vaults. **Never commit them.** Validate them on boot. Rotate when they leak.
- File uploads: whitelist types, size-cap, rename, re-encode, store off-box.
- Run `npm audit`, keep deps fresh, use HTTPS everywhere, set the right cookie flags.

---

**Prev:** [`06-Middleware-And-Error-Handling.md`](./06-Middleware-And-Error-Handling.md) · **Next:** [`08-Advanced-Node-And-Deployment.md`](./08-Advanced-Node-And-Deployment.md) · **Index:** [`00-Index.md`](./00-Index.md)
