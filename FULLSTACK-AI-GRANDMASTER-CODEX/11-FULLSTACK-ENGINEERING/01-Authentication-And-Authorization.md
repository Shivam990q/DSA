# 🔐 01 — Authentication & Authorization

> *"Identity is the front door of every system. Get the locks wrong and nothing else you build matters — the attacker is already inside."*

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-Web-Security.md`](./02-Web-Security.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. AUTHENTICATION vs AUTHORIZATION — THE TWO QUESTIONS

These two words are constantly confused, yet they answer entirely different questions. Burn the distinction into memory because every access-control bug traces back to mixing them up.

| | **Authentication (authn)** | **Authorization (authz)** |
|---|---|---|
| Question | *Who are you?* | *What are you allowed to do?* |
| Happens | First | After authn succeeds |
| Proves | Identity (login) | Permission (access) |
| Failure code | `401 Unauthorized` | `403 Forbidden` |
| Example | "This is Alice, password verified" | "Alice may read this doc but not delete it" |

```
Request ──▶ [ Authentication ] ──▶ identity known? ──no──▶ 401
                  │ yes
                  ▼
            [ Authorization ] ──▶ allowed? ──no──▶ 403
                  │ yes
                  ▼
              Handler runs
```

> **Gotcha — the HTTP status names lie.** `401 Unauthorized` actually means *unauthenticated* (you didn't prove who you are). `403 Forbidden` means *authenticated but not permitted*. The spec named them backwards. Use 401 for "log in," 403 for "you can't do that."

The rest of this file walks the full lifecycle: how you keep someone logged in (sessions vs JWT), how you delegate identity (OAuth2/OIDC/SSO), how you decide permissions (RBAC/ABAC), how you store passwords safely, and the vulnerabilities that wreck all of it.

---

## II. STATEFUL SESSIONS — THE SERVER REMEMBERS YOU

HTTP is **stateless**: every request is independent, the server forgets you between them. To stay "logged in," you need a token the browser resends on every request. The oldest, simplest answer is a **session**.

**The flow:**

```
1. POST /login (email + password)
2. Server verifies, creates a SESSION record server-side:
       sessionId "a3f9..."  →  { userId: 42, role: "admin", createdAt: ... }
3. Server sends Set-Cookie: sid=a3f9...; HttpOnly; Secure; SameSite=Lax
4. Browser auto-sends Cookie: sid=a3f9... on every later request
5. Server looks up "a3f9..." in its store → knows it's user 42
```

The **session ID is opaque** — a random string that means nothing on its own. All the real data lives server-side in a store (memory, Redis, a database).

```js
// Express + express-session backed by Redis (production-grade)
const session = require("express-session");
const { RedisStore } = require("connect-redis");
const { createClient } = require("redis");

const redisClient = createClient({ url: process.env.REDIS_URL });
redisClient.connect().catch(console.error);

app.use(session({
  store: new RedisStore({ client: redisClient }),   // NOT in-memory (see gotcha)
  secret: process.env.SESSION_SECRET,                // signs the cookie so it can't be forged
  name: "sid",                                       // don't leak "connect.sid" (framework fingerprint)
  resave: false,                                     // don't rewrite unchanged sessions
  saveUninitialized: false,                          // don't create sessions for anonymous visitors
  cookie: {
    httpOnly: true,                                  // JS cannot read it → blunts XSS token theft
    secure: process.env.NODE_ENV === "production",   // HTTPS only
    sameSite: "lax",                                 // blunts CSRF (see file 02)
    maxAge: 1000 * 60 * 60 * 2,                       // 2 hours
  },
}));

app.post("/login", async (req, res) => {
  const user = await verifyCredentials(req.body.email, req.body.password);
  if (!user) return res.status(401).json({ error: "Invalid credentials" });

  req.session.regenerate((err) => {                  // NEW id on login → prevents session fixation
    if (err) return res.status(500).end();
    req.session.userId = user.id;
    req.session.role = user.role;
    res.json({ ok: true });
  });
});

app.post("/logout", (req, res) => {
  req.session.destroy(() => res.clearCookie("sid").json({ ok: true }));
});
```

> **Gotcha — in-memory sessions don't survive.** The default `MemoryStore` loses every session when the server restarts and cannot be shared across multiple instances behind a load balancer. It is for local dev only. Production needs Redis or a DB so any instance can resolve any session.

> **Gotcha — always `regenerate()` the session ID at login.** If you keep the pre-login ID, an attacker who planted that ID in the victim's browser is now logged in as them. This is **session fixation** (see §XII).

---

## III. STATELESS JWT — THE TOKEN CARRIES THE TRUTH

A **JSON Web Token (JWT)** flips the model: instead of the server storing state, the *token itself* carries the claims, **signed** so it can't be tampered with. The server stores nothing — it just verifies the signature.

A JWT is three Base64URL parts joined by dots: `header.payload.signature`.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9   ← HEADER    {"alg":"HS256","typ":"JWT"}
.eyJzdWIiOiI0MiIsInJvbGUiOiJhZG1pbiJ9  ← PAYLOAD   {"sub":"42","role":"admin","exp":...}
.dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1g    ← SIGNATURE HMAC-SHA256(header.payload, secret)
```

- **Header** — the signing algorithm (`alg`) and type.
- **Payload** — the **claims**: `sub` (subject/user id), `exp` (expiry), `iat` (issued at), plus your own data. **Base64 is NOT encryption** — anyone can read the payload. Never put secrets in it.
- **Signature** — proves the token was issued by you and hasn't been altered. Without the secret, an attacker cannot forge a valid one.

```js
const jwt = require("jsonwebtoken");

// SIGN — at login
function issueToken(user) {
  return jwt.sign(
    { sub: String(user.id), role: user.role },   // claims (the payload)
    process.env.JWT_SECRET,                       // HMAC secret (keep it long & random)
    { expiresIn: "15m", issuer: "api.myapp.com", audience: "myapp-web" }
  );
}

// VERIFY — on every protected request (middleware)
function requireAuth(req, res, next) {
  const header = req.headers.authorization || "";
  const token = header.startsWith("Bearer ") ? header.slice(7) : null;
  if (!token) return res.status(401).json({ error: "Missing token" });

  try {
    const claims = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ["HS256"],            // PIN the algorithm — never trust the header's alg blindly
      issuer: "api.myapp.com",
      audience: "myapp-web",
    });
    req.user = { id: claims.sub, role: claims.role };
    next();
  } catch (e) {
    return res.status(401).json({ error: "Invalid or expired token" });  // exp, signature, etc.
  }
}
```

> **Gotcha — `jwt.verify` ≠ `jwt.decode`.** `decode()` just reads the payload **without checking the signature** — never trust its output for auth. Always `verify()`. And always pin `algorithms` (see the `alg:none` attack in §XII).

> **⚠️ Gotcha — JWTs can't be un-issued.** Because the server stores nothing, you cannot "log out" a valid JWT before it expires. That is the whole revocation problem — and the reason for short-lived access tokens plus refresh tokens (§V).

---

## IV. SESSIONS vs JWT — A REAL TRADEOFF, NOT A WINNER

Engineers argue about this endlessly. There is no universal winner; there are axes.

| Axis | **Sessions (stateful)** | **JWT (stateless)** |
|------|--------------------------|----------------------|
| State | Server stores it | Client carries it |
| Revocation | Instant — delete the record | Hard — valid until `exp` (need a denylist) |
| Horizontal scale | Needs shared store (Redis) | No shared store needed |
| Per-request cost | Store lookup | Signature verify (CPU only) |
| Payload size | Tiny cookie (just an ID) | Larger token on every request |
| Mobile / 3rd-party API | Awkward (cookies) | Natural (`Authorization` header) |
| Main attack surface | CSRF (cookie auto-sent) | XSS (if stored in JS-readable storage) |

**The pragmatic rule:**

- **Same-site web app, you control both ends?** Sessions (cookie-based) are simpler and revocation is free.
- **Public API, mobile clients, microservices, or third-party consumers?** JWT access tokens shine.
- **Best of both (most production apps):** short-lived JWT **access token** + long-lived **refresh token** stored in an `HttpOnly` cookie, with a server-side record so refresh tokens *can* be revoked.

---

## V. ACCESS vs REFRESH TOKENS — ROTATION & REUSE DETECTION

To get JWT's scale *and* sessions' revocability, split the token into two:

- **Access token** — short-lived (5–15 min), sent on every API call. If stolen, it's useless within minutes.
- **Refresh token** — long-lived (days/weeks), used **only** to mint new access tokens. Stored server-side so it can be revoked, and delivered to the browser in an `HttpOnly` cookie.

```
Login ──▶ access (15m) + refresh (7d, HttpOnly cookie, row in DB)
   │
   │  access token expires...
   ▼
POST /auth/refresh (sends refresh cookie)
   │  refresh valid & not used before?
   ▼
Issue NEW access + NEW refresh, INVALIDATE the old refresh   ← rotation
```

**Refresh token rotation** means each refresh is single-use: using it returns a brand-new refresh token and kills the old one. **Reuse detection** is the security payoff — if an *already-used* refresh token shows up again, someone copied it. You revoke the entire token family immediately.

```js
// Rotation + reuse detection (sketch — store: { id, userId, familyId, used, expiresAt })
app.post("/auth/refresh", async (req, res) => {
  const raw = req.cookies.refresh;
  if (!raw) return res.status(401).end();

  const record = await db.refreshTokens.findByHash(sha256(raw));   // store HASHES, never raw tokens
  if (!record || record.expiresAt < Date.now()) return res.status(401).end();

  if (record.used) {
    // ⚠️ REUSE DETECTED — this token was already rotated. Assume theft.
    await db.refreshTokens.revokeFamily(record.familyId);          // nuke every token in the chain
    return res.status(401).json({ error: "Token reuse detected — all sessions revoked" });
  }

  await db.refreshTokens.markUsed(record.id);                      // single-use
  const access = issueToken(await db.users.find(record.userId));
  const newRefresh = await rotateRefresh(record.familyId, record.userId);

  res
    .cookie("refresh", newRefresh, { httpOnly: true, secure: true, sameSite: "strict", path: "/auth/refresh" })
    .json({ access });
});
```

> **⚠️ Gotcha — store refresh tokens hashed.** A leaked database of raw refresh tokens is a leaked set of live sessions. Hash them (SHA-256 is fine for high-entropy random tokens) so the DB alone can't be replayed.

---

## VI. TOKEN STORAGE — COOKIES vs localStorage

Where the browser keeps the token decides which attack you're exposed to. This is one of the most consequential and most-fumbled decisions in frontend auth.

| Storage | Read by JS? | Sent automatically? | XSS risk | CSRF risk |
|---------|-------------|----------------------|----------|-----------|
| `localStorage` / `sessionStorage` | ✅ Yes | ❌ No (you attach it) | **High** — any XSS steals it | None |
| `HttpOnly` cookie | ❌ No | ✅ Yes (same-site rules) | Low — JS can't read it | **Yes** — needs CSRF defense |
| JS-readable cookie | ✅ Yes | ✅ Yes | High | Yes (worst of both) |

> **⚠️ The core tradeoff.** `localStorage` is convenient and immune to CSRF, but **any** XSS hole turns into total account takeover because the script can read the token. `HttpOnly` cookies can't be read by injected JS (defeating token theft) but are auto-sent, so you must add CSRF defenses (see file 02).

**Recommended pattern for most web apps:** access token kept in memory (a JS variable, gone on refresh), refresh token in an `HttpOnly`, `Secure`, `SameSite=Strict` cookie. XSS can't read the refresh token; CSRF is blunted by `SameSite`; a page reload silently re-authenticates via `/auth/refresh`.

---

## VII. OAuth2 — DELEGATED AUTHORIZATION

**OAuth2 is an authorization framework, not a login system.** It lets a user grant one app limited access to their data on another service *without sharing their password*. "Sign in with Google" feels like login, but underneath it's OAuth2 (plus OIDC, §VIII) granting your app a token.

**The four roles:**

| Role | Who | Example |
|------|-----|---------|
| **Resource Owner** | The user | You |
| **Client** | The app wanting access | "PhotoPrint" app |
| **Authorization Server** | Issues tokens | Google's OAuth server |
| **Resource Server** | Holds the data | Google Photos API |

**Grant types (how the client gets a token):**

| Grant | Use it for | Notes |
|-------|-----------|-------|
| **Authorization Code + PKCE** | Web & mobile apps with a user | The modern default for *everything* user-facing |
| Client Credentials | Machine-to-machine (no user) | Service talking to service |
| Device Code | TVs, CLIs, no browser | Enter a code on your phone |
| ~~Implicit~~ | — | **Deprecated** — insecure, don't use |
| ~~Password (ROPC)~~ | — | **Deprecated** — app sees the password |

### The Authorization Code flow with PKCE

PKCE (*Proof Key for Code Exchange*, "pixy") stops an attacker who intercepts the authorization code from exchanging it, because they lack the secret `code_verifier`.

```
1. Client generates: code_verifier (random) → code_challenge = SHA256(verifier)
2. Browser → Auth Server: /authorize?client_id&redirect_uri&code_challenge&state
3. User logs in & consents on the Auth Server (client never sees the password)
4. Auth Server → Browser redirect: /callback?code=AUTH_CODE&state
5. Client → Auth Server: POST /token { code, code_verifier }   ← proves it started step 1
6. Auth Server verifies SHA256(code_verifier) == code_challenge → returns tokens
```

```js
// Step 1 — generate PKCE pair (client side)
const verifier = base64url(crypto.randomBytes(32));
const challenge = base64url(crypto.createHash("sha256").update(verifier).digest());

// Step 2 — build the authorize URL (state defeats CSRF on the redirect)
const state = base64url(crypto.randomBytes(16));
const url = `https://auth.example.com/authorize?` + new URLSearchParams({
  response_type: "code",
  client_id: CLIENT_ID,
  redirect_uri: "https://myapp.com/callback",
  scope: "openid profile email",
  code_challenge: challenge,
  code_challenge_method: "S256",
  state,
});
// ...store verifier + state in the session, redirect the user to `url`.
```

> **Gotcha — always validate `state`.** The `state` parameter you send must come back unchanged on the callback. If it doesn't match what you stored, reject the request — this is your CSRF defense for the OAuth redirect.

---

## VIII. OPENID CONNECT — AUTHENTICATION ON TOP OF OAUTH2

OAuth2 gives you an **access token** (permission to call an API) but says nothing standard about *who the user is*. **OpenID Connect (OIDC)** is a thin identity layer on top of OAuth2 that adds an **ID token** — a JWT describing the authenticated user.

| | **OAuth2** | **OpenID Connect** |
|---|---|---|
| Purpose | Authorization (access to resources) | Authentication (who the user is) |
| Returns | Access token | Access token **+ ID token** |
| ID token | — | JWT with `sub`, `email`, `name`, `iss`, `aud`, `exp` |
| User info | — | `/userinfo` endpoint |
| "Sign in with X" | Not by itself | This is the standard |

The **ID token** is a JWT you verify like any other. Trust its `iss` (issuer) and `aud` (audience) claims, and validate the signature against the provider's published keys (JWKS).

```js
// Verify a provider's ID token against its rotating public keys (JWKS)
const { createRemoteJWKSet, jwtVerify } = require("jose");
const JWKS = createRemoteJWKSet(new URL("https://auth.example.com/.well-known/jwks.json"));

async function verifyIdToken(idToken) {
  const { payload } = await jwtVerify(idToken, JWKS, {
    issuer: "https://auth.example.com",
    audience: CLIENT_ID,
  });
  return payload;   // { sub, email, name, ... } — the authenticated identity
}
```

> **Rule of thumb.** If you only need to *call an API on the user's behalf*, OAuth2 alone suffices. If you need to *log the user in*, you want OIDC.

---

## IX. SSO — SINGLE SIGN-ON (SAML vs OIDC)

**Single Sign-On** lets a user authenticate once with a central **Identity Provider (IdP)** and access many applications (**Service Providers**) without logging in again. Think logging into Google once and getting Gmail, Drive, Calendar, and YouTube.

The two dominant protocols:

| | **SAML 2.0** | **OIDC** |
|---|---|---|
| Era / style | 2005, XML | 2014, JSON/REST |
| Token | XML `SAMLResponse` (signed) | JWT ID token |
| Transport | Browser form POST / redirect | OAuth2 flows |
| Best fit | Enterprise, legacy SaaS, B2B | Modern web/mobile, APIs |
| Complexity | Heavy (XML signatures, metadata) | Lighter |

Both rely on the same trust model: the app redirects to the IdP, the IdP authenticates the user and returns a **signed assertion**, the app verifies the signature and trusts the identity. New apps generally choose OIDC; SAML persists because enterprise IdPs (Okta, Azure AD, Ping) and older SaaS standardized on it.

> **Gotcha — SAML's danger is XML signature wrapping.** Malformed/duplicated XML can trick naive parsers into trusting an unsigned assertion. Always use a vetted SAML library; never hand-roll XML signature validation.

---

## X. RBAC vs ABAC — DECIDING WHAT'S ALLOWED

Once you know *who* the user is, authorization decides *what they can do*. Two dominant models:

**RBAC (Role-Based Access Control)** — permissions attach to **roles**, users get roles. Simple, auditable, ubiquitous.

```js
const permissions = {
  admin:  ["post:create", "post:delete", "user:ban"],
  editor: ["post:create", "post:edit"],
  viewer: ["post:read"],
};

function can(role, action) {
  return (permissions[role] || []).includes(action);
}

function authorize(action) {                      // middleware factory
  return (req, res, next) =>
    can(req.user.role, action) ? next() : res.status(403).json({ error: "Forbidden" });
}

app.delete("/posts/:id", requireAuth, authorize("post:delete"), deletePost);
```

**ABAC (Attribute-Based Access Control)** — decisions are computed from **attributes** of the user, the resource, the action, and the environment. More expressive, handles rules RBAC can't ("an editor may edit a post **only if they own it** and it's **not published**").

```js
// ABAC policy: a function of (subject, action, resource, context) → boolean
function canEditPost(user, post, ctx) {
  if (user.role === "admin") return true;                         // admins always
  if (user.role === "editor"
      && post.authorId === user.id                                // ownership attribute
      && post.status !== "published"                              // resource attribute
      && ctx.ip_in_office) return true;                           // environment attribute
  return false;
}
```

| | **RBAC** | **ABAC** |
|---|---|---|
| Decision basis | Role membership | Arbitrary attributes & policies |
| Granularity | Coarse | Fine-grained, contextual |
| Complexity | Low — easy to audit | Higher — needs a policy engine |
| "Role explosion" | Risk as rules multiply | Avoids it |
| Tooling | Built-in everywhere | OPA / Cedar / Casbin |

> **Practical advice.** Start with RBAC. Add ABAC-style checks (ownership, status, tenancy) exactly where you need them. Most real systems are RBAC with a sprinkle of attribute checks. Reach for a policy engine (Open Policy Agent, AWS Cedar) only when rules get genuinely complex.

---

## XI. PASSWORD HASHING — bcrypt & argon2

**Never store passwords.** Store a **slow, salted hash**. If your DB leaks, attackers should face years of brute-force, not a plaintext dump.

Why not SHA-256? Because it's *fast* — a GPU computes billions per second. Password hashing must be **deliberately slow** and memory-hard.

- **Salt** — a unique random value per password, stored alongside the hash. Defeats precomputed **rainbow tables** and ensures two users with the same password get different hashes. (bcrypt/argon2 generate and embed the salt for you.)
- **Cost / work factor** — a tunable that makes hashing slower as hardware improves. Raise it over time.
- **Pepper** — an *additional* secret (an app-wide key, **not** in the DB) mixed in before hashing. If only the DB leaks, the pepper still protects the hashes.

```js
// bcrypt — the battle-tested default
const bcrypt = require("bcrypt");
const COST = 12;                                  // 2^12 iterations; tune so a hash takes ~250ms

const hash = await bcrypt.hash(plainPassword, COST);   // salt is generated & embedded automatically
const ok   = await bcrypt.compare(plainPassword, hash); // constant-time comparison
```

```js
// argon2id — the modern winner (Password Hashing Competition), memory-hard
const argon2 = require("argon2");

const hash = await argon2.hash(plainPassword, {
  type: argon2.argon2id,        // resists both GPU and side-channel attacks
  memoryCost: 19456,            // ~19 MB — memory-hardness is argon2's superpower
  timeCost: 2,                  // iterations
  parallelism: 1,
});
const ok = await argon2.verify(hash, plainPassword);
```

```js
// Peppering: HMAC the password with an app secret BEFORE hashing
const peppered = crypto.createHmac("sha256", process.env.PEPPER).update(plainPassword).digest("hex");
const hash = await argon2.hash(peppered);     // DB leak alone is now insufficient
```

| | **bcrypt** | **argon2id** |
|---|---|---|
| Year | 1999 | 2015 (PHC winner) |
| Hardness | CPU | CPU **+ memory** (GPU-resistant) |
| Max input | 72 bytes (truncates!) | No practical limit |
| Default choice | Safe, everywhere | Preferred for new systems |

> **⚠️ Gotcha — bcrypt silently truncates at 72 bytes.** Long passphrases beyond 72 bytes are ignored after the cutoff. Either pre-hash (e.g. SHA-256 → base64) before bcrypt, or use argon2 which has no such limit.

> **⚠️ Always compare in constant time.** Use the library's `compare`/`verify` — a naive `==` on hashes can leak information through timing. Never roll your own.

---

## XII. MFA / 2FA AND TOTP

**Multi-Factor Authentication** requires two or more *different kinds* of proof:

1. **Something you know** — password
2. **Something you have** — phone, security key
3. **Something you are** — fingerprint, face

**TOTP (Time-based One-Time Password)** powers authenticator apps (Google Authenticator, Authy). Server and app share a secret; both compute a 6-digit code from `HMAC(secret, current_30s_window)`. No network needed — it's just math on synchronized clocks.

```js
const speakeasy = require("speakeasy");
const QRCode = require("qrcode");

// SETUP — generate a per-user secret, show it as a QR code to scan
const secret = speakeasy.generateSecret({ name: "MyApp (alice@example.com)" });
await db.users.update(userId, { totpSecret: secret.base32, totpEnabled: false });
const qrDataUrl = await QRCode.toDataURL(secret.otpauth_url);   // render this <img> at setup

// VERIFY — on login, after password passes
const valid = speakeasy.totp.verify({
  secret: user.totpSecret,
  encoding: "base32",
  token: req.body.code,        // the 6 digits the user typed
  window: 1,                   // accept ±1 step (~30s) for clock drift
});
if (!valid) return res.status(401).json({ error: "Invalid 2FA code" });
```

> **⚠️ Always issue recovery codes.** Generate ~10 single-use backup codes at MFA setup, store them **hashed**, and show them once. Without them, a lost phone means a permanently locked-out user — and a support nightmare.

> **Gotcha — SMS is the weakest second factor.** SIM-swapping and SS7 attacks defeat it. Prefer TOTP apps or, best of all, **WebAuthn / passkeys** (phishing-resistant hardware-backed credentials) for high-value accounts.

---

## XIII. COOKIE SECURITY FLAGS

Cookies carry your session/refresh tokens, so their flags *are* your security posture.

```
Set-Cookie: sid=a3f9...; HttpOnly; Secure; SameSite=Strict; Domain=app.com; Path=/; Max-Age=7200
```

| Flag | What it does | Why it matters |
|------|--------------|----------------|
| `HttpOnly` | JS (`document.cookie`) cannot read it | Stops XSS from stealing the token |
| `Secure` | Sent only over HTTPS | Stops network sniffing on plaintext |
| `SameSite=Strict` | Never sent on cross-site requests | Strong CSRF defense (can break some flows) |
| `SameSite=Lax` | Sent on top-level GET navigations only | Good default — CSRF defense + usability |
| `SameSite=None` | Sent cross-site (requires `Secure`) | Needed for true cross-site cookies; risky |
| `Domain` | Which hosts get the cookie | Too broad = leak to subdomains |
| `Path` | Which URL paths get the cookie | Scope refresh tokens to `/auth/refresh` |
| `Max-Age` / `Expires` | Lifetime | Short = smaller theft window |

> **⚠️ Gotcha — `Domain=.example.com` shares the cookie with every subdomain.** A compromised or untrusted subdomain (`blog.example.com`) then receives your auth cookie. Set `Domain` as narrowly as possible, and isolate untrusted subdomains.

> **Gotcha — `SameSite=None` without `Secure` is rejected.** Modern browsers drop it. If you genuinely need cross-site cookies (embedded widgets, separate API domain), you must also set `Secure` and accept the larger CSRF surface.

---

## XIV. COMMON AUTH VULNERABILITIES

| Vulnerability | What happens | Fix |
|---------------|--------------|-----|
| **Session fixation** | Attacker plants a session ID, victim logs in with it, attacker is now them | `regenerate()` the session ID on every login |
| **`alg:none` attack** | Attacker sets JWT header `alg:none`, sends an unsigned token; naive verifiers accept it | Pin allowed `algorithms` in `verify()`; reject `none` |
| **Weak JWT secret** | Short/guessable HMAC secret is brute-forced offline, tokens forged | Long random secret (≥256-bit) or RS256 keypair |
| **Algorithm confusion (RS256→HS256)** | Attacker signs with the *public* key as an HMAC secret | Pin the exact algorithm; never let the token choose |
| **IDOR** | `GET /orders/123` returns anyone's order — no ownership check | Authorize *every* object access against the current user |
| **JWT in localStorage + XSS** | One injected script reads and exfiltrates the token | `HttpOnly` cookies; eliminate XSS (file 02) |
| **No logout/revocation** | Stolen JWT works until expiry | Short access TTL + refresh rotation + denylist |
| **Missing rate limit on login** | Credential stuffing / brute force succeeds | Rate-limit + lockout + MFA (file 02) |
| **User enumeration** | "No such email" vs "wrong password" reveals valid accounts | Identical generic error + identical timing |

### IDOR — the one people forget

Authentication tells you *who* is calling; it does **not** check that this user owns *this* object. That's authorization, and skipping it is **Insecure Direct Object Reference** — one of the most common real-world breaches.

```js
// ❌ VULNERABLE — any logged-in user can read any order by guessing the id
app.get("/orders/:id", requireAuth, async (req, res) => {
  res.json(await db.orders.find(req.params.id));
});

// ✅ SAFE — scope the lookup to the authenticated owner
app.get("/orders/:id", requireAuth, async (req, res) => {
  const order = await db.orders.findOne({ id: req.params.id, userId: req.user.id });
  if (!order) return res.status(404).end();    // 404 (not 403) — don't reveal it exists
  res.json(order);
});
```

> **⚠️ The golden rule of authorization.** *Authenticate once, authorize every access.* For every request that touches an object, ask: "Is **this** user allowed to do **this** action on **this** specific resource?" Never trust an ID from the client as proof of ownership.

---

## XV. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| In-memory sessions in production | Logged out on every deploy / load-balancer hop | Redis or DB session store |
| Not regenerating session on login | Session fixation | `req.session.regenerate()` at login |
| `jwt.decode` used for auth | Forged tokens accepted | Always `jwt.verify` with pinned `algorithms` |
| Secrets in JWT payload | Sensitive data readable by anyone | Payload is public — never put secrets there |
| JWT in `localStorage` | XSS → full account takeover | `HttpOnly` cookie; kill XSS |
| No refresh-token revocation | Can't log users out / stop theft | Server-side records + rotation + reuse detection |
| Fast hash (MD5/SHA) for passwords | DB leak = instant cracking | bcrypt / argon2id, tuned cost |
| bcrypt with >72-byte passwords | Silent truncation | Pre-hash or use argon2 |
| Missing ownership checks | IDOR data exposure | Authorize every object access |
| `SameSite=None` without `Secure` | Cookie dropped / CSRF wide open | Set `Secure`; prefer `Lax`/`Strict` |
| SMS as the only 2FA | SIM-swap account takeover | TOTP or WebAuthn/passkeys |
| User-enumeration via login errors | Account discovery | Generic error + constant timing |

---

## 🧠 KEY TAKEAWAYS

- **Authentication = who you are (401); authorization = what you may do (403).** Authenticate once, authorize *every* object access.
- **Sessions** keep state server-side (easy revocation, needs a shared store); **JWTs** carry signed state (scale freely, hard to revoke). Most apps combine short-lived access tokens with rotating, revocable refresh tokens.
- **Storage decides your attack surface:** `localStorage` → XSS risk; `HttpOnly` cookies → CSRF risk. Prefer access-token-in-memory + refresh-in-`HttpOnly`-cookie.
- **OAuth2** delegates *authorization*; **OIDC** adds *authentication* (ID token). Use **Authorization Code + PKCE** for all user-facing apps, and always validate `state`.
- **RBAC** (roles) covers most needs; add **ABAC** attribute checks (ownership, status, tenancy) where rules get contextual.
- **Hash passwords slowly** with bcrypt or argon2id (salt built in; add a pepper; tune cost). Never use fast hashes; mind bcrypt's 72-byte limit.
- **MFA** with TOTP beats SMS; always issue hashed recovery codes; passkeys/WebAuthn are the phishing-resistant gold standard.
- **Cookie flags are security:** `HttpOnly` + `Secure` + `SameSite` + tight `Domain`/`Path` + short `Max-Age`.
- **Know the classic breaks:** session fixation, `alg:none`, weak/confused JWT algorithms, and **IDOR** — the access-control bug everyone forgets.

---

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-Web-Security.md`](./02-Web-Security.md) · **Index:** [`00-Index.md`](./00-Index.md)
