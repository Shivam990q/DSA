# 🔐 04 — Authentication Across The Stack

> *"Authentication is the one feature where a clever shortcut becomes a headline. Hash like you mean it, store tokens where scripts can't reach, rotate what you can revoke, and assume every input is an attacker until proven otherwise."*

**Prev:** [`03-Building-The-React-Frontend.md`](./03-Building-The-React-Frontend.md) · **Next:** [`05-State-File-Uploads-And-Realtime.md`](./05-State-File-Uploads-And-Realtime.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT WE ARE BUILDING — AND THE SECURITY STAKES

TaskFlow needs users. In this file we add **end-to-end authentication**:

- **Register** + **login** endpoints (bcrypt password hashing + JWT)
- The **httpOnly cookie vs localStorage** decision, spelled out honestly
- **Refresh-token rotation** (short access token, rotating refresh token)
- **Auth middleware** that protects routes and attaches `req.user`
- An **auth context** + **protected routes** on the frontend
- **Logout** and **session persistence** (silent refresh / `/me`)
- **CSRF** considerations that come with cookie auth

> 🔒 **Security flag.** This is the highest-risk code in the app. The patterns below are sound for a real product, but auth is deep — for production also read [`07-Authentication-And-Security`](../07-NODEJS-EXPRESS/07-Authentication-And-Security.md) and the [OWASP Top 10](https://owasp.org/www-project-top-ten/). Never roll your own crypto; use vetted libraries (bcrypt, jsonwebtoken) as shown.

---

## II. THE MENTAL MODEL — TWO TOKENS, TWO JOBS

We use a **two-token** scheme. Understanding *why* prevents most auth mistakes:

| Token | Lifetime | Job | Where stored |
|-------|----------|-----|--------------|
| **Access token** | short (~15 min) | proves identity on each API call | in memory (JS) **or** httpOnly cookie |
| **Refresh token** | long (~7 days) | gets a NEW access token when it expires | **httpOnly cookie only** |

```text
login ──▶ server issues   access (15m)  +  refresh (7d)
                              │                  │
       every API call uses access            when access expires,
                              │              client calls /refresh with the refresh token
                              ▼                  │
                         401 expired ───────────▶ server verifies + ROTATES refresh,
                                                  issues a fresh access (+ new refresh)
```

The point: a short access token limits the damage if it leaks (it expires fast), while the refresh token — the powerful, long-lived one — lives only in an httpOnly cookie that JavaScript cannot read, and is **rotated** on every use so a stolen one is quickly invalidated.

---

## III. INSTALL AND CONFIG

```bash
cd server
npm install bcryptjs jsonwebtoken
```

We added `JWT_SECRET` and `JWT_REFRESH_SECRET` to the validated config back in file 02. Add token lifetimes:

```js
// server/src/config/auth.config.js
import { env } from './env.js';

export const authConfig = {
  accessSecret: env.JWT_SECRET,
  refreshSecret: env.JWT_REFRESH_SECRET,
  accessTtl: '15m',          // short-lived
  refreshTtl: '7d',          // long-lived
  // cookie options reused everywhere we set the refresh cookie
  refreshCookie: {
    httpOnly: true,                                  // JS cannot read it (blocks XSS theft)
    secure: env.NODE_ENV === 'production',           // HTTPS-only in prod
    sameSite: env.NODE_ENV === 'production' ? 'none' : 'lax', // 'none' for cross-site prod
    path: '/api/auth',                               // cookie only sent to auth routes
    maxAge: 7 * 24 * 60 * 60 * 1000,                 // 7 days in ms
  },
};
```

> **Gotcha — `sameSite` and cross-site cookies.** If your frontend and backend are on *different domains* in production (e.g. Vercel + Render), the refresh cookie must be `SameSite=None; Secure` or the browser won't send it. `None` *requires* `Secure` (HTTPS). In dev (same site via proxy) `lax` is fine. This single setting causes most "auth works locally, breaks in prod" tickets (revisited in file 06).

---

## IV. PASSWORD HASHING — NEVER STORE PLAINTEXT

Passwords are **hashed with bcrypt**, never stored or logged in plaintext. bcrypt is deliberately slow and salts automatically, which is exactly what you want against brute force.

```js
// server/src/services/auth.service.js (part 1 — hashing)
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { User } from '../models/User.js';
import { AppError } from '../utils/AppError.js';
import { authConfig } from '../config/auth.config.js';

const SALT_ROUNDS = 12;   // cost factor — higher = slower = harder to brute force

function signAccess(user) {
  // Payload = minimal, NON-secret identity info. Never put passwords/secrets in a JWT.
  return jwt.sign({ sub: user._id.toString() }, authConfig.accessSecret, {
    expiresIn: authConfig.accessTtl,
  });
}

function signRefresh(user) {
  return jwt.sign({ sub: user._id.toString(), type: 'refresh' }, authConfig.refreshSecret, {
    expiresIn: authConfig.refreshTtl,
  });
}
```

> **Gotcha — a JWT is signed, not encrypted.** Anyone can base64-decode a JWT and read its payload (paste one into [jwt.io](https://jwt.io)). The signature only proves *we* issued it and it wasn't tampered with. So put **identity, not secrets** in the payload — `sub` (user id), maybe a role. Never a password, never PII you wouldn't expose.

---

## V. REGISTER AND LOGIN

```js
// server/src/services/auth.service.js (part 2 — register/login)
export const authService = {
  async register({ name, email, password }) {
    const exists = await User.findOne({ email });
    if (exists) throw AppError.badRequest('Email already in use');

    const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
    const user = await User.create({ name, email, passwordHash });
    return this.issueTokens(user);
  },

  async login({ email, password }) {
    // Must explicitly select passwordHash (schema has select:false, file 02).
    const user = await User.findOne({ email }).select('+passwordHash');
    // Same generic error whether email is unknown or password is wrong (no enumeration).
    if (!user) throw AppError.unauthorized('Invalid credentials');

    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) throw AppError.unauthorized('Invalid credentials');

    return this.issueTokens(user);
  },

  async issueTokens(user) {
    const accessToken = signAccess(user);
    const refreshToken = signRefresh(user);
    // Store the refresh token server-side so we can ROTATE and REVOKE it.
    user.refreshTokens.push(refreshToken);
    await user.save();
    return { user, accessToken, refreshToken };
  },
};
```

> **Gotcha — don't reveal which half was wrong.** Returning "no such email" vs "wrong password" lets an attacker *enumerate* valid emails. Always return the same generic "Invalid credentials". Likewise, run `bcrypt.compare` even on a missing user in high-security contexts to avoid timing leaks (here we keep it simple but use a uniform message).

---

## VI. REFRESH-TOKEN ROTATION

Rotation means: every time a refresh token is used, it is **invalidated and replaced**. If an attacker steals one and uses it, the legitimate user's next refresh fails (token already rotated), surfacing the breach; and a stolen token works at most once.

```js
// server/src/services/auth.service.js (part 3 — refresh/logout/me)
import jwt from 'jsonwebtoken';

Object.assign(authService, {
  async refresh(oldRefreshToken) {
    if (!oldRefreshToken) throw AppError.unauthorized('No refresh token');

    let payload;
    try {
      payload = jwt.verify(oldRefreshToken, authConfig.refreshSecret);
    } catch {
      throw AppError.unauthorized('Invalid refresh token');
    }

    const user = await User.findById(payload.sub).select('+refreshTokens');
    if (!user) throw AppError.unauthorized('User not found');

    // The token must be one we issued AND haven't rotated away yet.
    if (!user.refreshTokens.includes(oldRefreshToken)) {
      // Reuse of a rotated token = likely theft. Revoke ALL sessions defensively.
      user.refreshTokens = [];
      await user.save();
      throw AppError.unauthorized('Refresh token reuse detected');
    }

    // ROTATE: remove the old, add a fresh one.
    user.refreshTokens = user.refreshTokens.filter((t) => t !== oldRefreshToken);
    const accessToken = signAccess(user);
    const refreshToken = signRefresh(user);
    user.refreshTokens.push(refreshToken);
    await user.save();

    return { user, accessToken, refreshToken };
  },

  async logout(userId, refreshToken) {
    // Revoke just this session's refresh token.
    await User.updateOne({ _id: userId }, { $pull: { refreshTokens: refreshToken } });
  },

  async me(userId) {
    const user = await User.findById(userId);
    if (!user) throw AppError.unauthorized('User not found');
    return user;
  },
});
```

> **Gotcha — "reuse detection" is the whole point of rotation.** Storing issued refresh tokens lets you notice when an *already-rotated* token reappears — a strong signal of theft. The defensive response (clear all refresh tokens → force re-login everywhere) contains the breach. Without server-side storage you can issue refresh tokens but cannot revoke them, which defeats much of the benefit.

---

## VII. THE AUTH CONTROLLER — SETTING COOKIES

The controller decides *where tokens live*. We send the **access token in the JSON body** (frontend keeps it in memory) and the **refresh token in an httpOnly cookie** (JS can't touch it).

```js
// server/src/controllers/auth.controller.js
import { asyncHandler } from '../utils/asyncHandler.js';
import { ok } from '../utils/respond.js';
import { authService } from '../services/auth.service.js';
import { authConfig } from '../config/auth.config.js';

function setRefreshCookie(res, token) {
  res.cookie('refreshToken', token, authConfig.refreshCookie); // httpOnly, secure, sameSite
}

export const authController = {
  register: asyncHandler(async (req, res) => {
    const { user, accessToken, refreshToken } = await authService.register(req.body);
    setRefreshCookie(res, refreshToken);
    return ok(res, { user, accessToken }, 201);   // access token in body
  }),

  login: asyncHandler(async (req, res) => {
    const { user, accessToken, refreshToken } = await authService.login(req.body);
    setRefreshCookie(res, refreshToken);
    return ok(res, { user, accessToken });
  }),

  refresh: asyncHandler(async (req, res) => {
    const { user, accessToken, refreshToken } = await authService.refresh(req.cookies.refreshToken);
    setRefreshCookie(res, refreshToken);          // rotated cookie
    return ok(res, { user, accessToken });
  }),

  logout: asyncHandler(async (req, res) => {
    if (req.user) await authService.logout(req.user.id, req.cookies.refreshToken);
    res.clearCookie('refreshToken', { path: '/api/auth' });
    return ok(res, null);
  }),

  me: asyncHandler(async (req, res) => {
    const user = await authService.me(req.user.id);
    return ok(res, { user });
  }),
};
```

```js
// server/src/routes/auth.routes.js
import { Router } from 'express';
import { authController } from '../controllers/auth.controller.js';
import { validate } from '../middleware/validate.js';
import { protect } from '../middleware/auth.js';
import { registerSchema, loginSchema } from '../validators/auth.schema.js';

const router = Router();
router.post('/register', validate(registerSchema), authController.register);
router.post('/login', validate(loginSchema), authController.login);
router.post('/refresh', authController.refresh);             // uses the cookie, no body
router.post('/logout', protect, authController.logout);
router.get('/me', protect, authController.me);
export default router;
```

```js
// server/src/validators/auth.schema.js
import { z } from 'zod';
export const registerSchema = z.object({
  name: z.string().trim().min(1).max(80),
  email: z.string().email(),
  password: z.string().min(8, 'Password must be at least 8 characters').max(100),
});
export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});
```

---

## VIII. httpOnly COOKIE vs localStorage — THE DECISION, SPELLED OUT

This is the most argued-about choice in MERN auth. Here it is honestly:

| | localStorage | httpOnly cookie |
|---|--------------|-----------------|
| Readable by JS | **Yes** — any XSS script steals it | **No** — JS can't read it |
| Sent automatically | No (you attach it manually) | Yes (browser attaches it) |
| Vulnerable to XSS theft | **High** | Low (token not script-accessible) |
| Vulnerable to CSRF | No (not auto-sent) | **Yes** (auto-sent) → needs CSRF defense |
| Works cross-domain easily | Yes | Needs `SameSite=None; Secure` + CORS `credentials` |

**Our hybrid (recommended):**
- **Refresh token → httpOnly cookie.** It is long-lived and powerful, so we keep it out of JavaScript's reach entirely. XSS cannot exfiltrate it.
- **Access token → in memory (a JS variable / React state).** It is short-lived, so even if XSS grabs it, it expires in minutes and is not persisted anywhere a script can mine on next load.

> 🔒 **Why not put the access token in localStorage?** Because **XSS is the dominant web threat**, and anything in localStorage is one injected script away from being stolen and persisted. In-memory tokens vanish on reload (we restore the session via silent refresh, §X) and never sit in a place a script can scrape. The cost is you re-fetch a token on reload — a fair trade for not handing attackers a long-lived credential.

---

## IX. AUTH MIDDLEWARE — PROTECT ROUTES, ATTACH req.user

```js
// server/src/middleware/auth.js
import jwt from 'jsonwebtoken';
import { authConfig } from '../config/auth.config.js';
import { AppError } from '../utils/AppError.js';

export function protect(req, res, next) {
  // Access token comes from the Authorization: Bearer <token> header.
  const header = req.headers.authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : null;
  if (!token) return next(AppError.unauthorized('Authentication required'));

  try {
    const payload = jwt.verify(token, authConfig.accessSecret);
    req.user = { id: payload.sub };   // attach identity for controllers/services
    next();
  } catch (err) {
    // Distinguish expired (client should refresh) from invalid (client should re-login).
    if (err.name === 'TokenExpiredError') {
      return next(new AppError('Access token expired', 401, 'TOKEN_EXPIRED'));
    }
    return next(AppError.unauthorized('Invalid token'));
  }
}
```

The task routes from file 02 already do `router.use(protect)`, so every task endpoint now has `req.user.id` — which is exactly what the task service scopes its queries by. Authentication (who are you?) and authorization (is this your task?) click together.

> **Gotcha — signal `TOKEN_EXPIRED` distinctly.** The frontend interceptor (§XI) reacts differently to an *expired* access token (silently refresh and retry) versus a *malformed/invalid* one (log out). Returning a specific `code: 'TOKEN_EXPIRED'` lets the client tell them apart instead of treating all 401s the same.

---

## X. FRONTEND — AUTH CONTEXT AND SESSION PERSISTENCE

The access token lives in memory. On page reload that memory is gone, so we **silently refresh** on boot: call `/refresh` (the httpOnly cookie rides along automatically) to get a fresh access token and the user.

```jsx
// client/src/context/AuthContext.jsx
import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { api, setAccessToken } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [booting, setBooting] = useState(true);   // true until we know if a session exists

  // On app load: try to restore a session via the refresh cookie.
  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.post('/auth/refresh');  // cookie sent automatically
        setAccessToken(data.data.accessToken);             // store in memory
        setUser(data.data.user);
      } catch {
        setUser(null);                                     // no valid session — that's fine
      } finally {
        setBooting(false);
      }
    })();
  }, []);

  const login = useCallback(async (credentials) => {
    const { data } = await api.post('/auth/login', credentials);
    setAccessToken(data.data.accessToken);
    setUser(data.data.user);
  }, []);

  const register = useCallback(async (payload) => {
    const { data } = await api.post('/auth/register', payload);
    setAccessToken(data.data.accessToken);
    setUser(data.data.user);
  }, []);

  const logout = useCallback(async () => {
    try { await api.post('/auth/logout'); } finally {
      setAccessToken(null);
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, booting, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

Update the API client to hold the in-memory access token and attach it to every request:

```js
// client/src/api/client.js  (additions)
let accessToken = null;                          // module-scoped, in MEMORY only
export const setAccessToken = (t) => { accessToken = t; };
export const getAccessToken = () => accessToken;

// REQUEST interceptor: attach the access token if we have one.
api.interceptors.request.use((config) => {
  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;
  return config;
});
```

> **Gotcha — the `booting` flag prevents an auth flicker.** Without it, on reload the app briefly thinks "no user" (memory is empty) before `/refresh` resolves, flashing the login page for a logged-in user. Gate the UI on `booting`: show a splash/spinner until the refresh attempt settles, *then* render routes.

---

## XI. AUTOMATIC TOKEN REFRESH ON 401

When the access token expires mid-session, the API returns 401 `TOKEN_EXPIRED`. The response interceptor catches it, refreshes once, and retries the original request transparently — the user never notices.

```js
// client/src/api/client.js  (refresh-on-401 interceptor)
let refreshing = null;   // de-dupe concurrent refreshes into ONE in-flight call

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    const status = error.response?.status;
    const code = error.response?.data?.error?.code;

    // Only try to refresh on an EXPIRED token, and only ONCE per request.
    if (status === 401 && code === 'TOKEN_EXPIRED' && !original._retried) {
      original._retried = true;
      try {
        // Share one refresh among all queued requests that hit 401 together.
        refreshing = refreshing || api.post('/auth/refresh');
        const { data } = await refreshing;
        refreshing = null;
        setAccessToken(data.data.accessToken);
        original.headers.Authorization = `Bearer ${getAccessToken()}`;
        return api(original);                  // retry the original request
      } catch (e) {
        refreshing = null;
        setAccessToken(null);
        window.location.href = '/login';       // refresh failed → session is over
        return Promise.reject(e);
      }
    }
    return Promise.reject(error);
  }
);
```

> **Gotcha — the "thundering herd" of refreshes.** If 5 requests fire and all get 401 at once, naive code triggers 5 simultaneous refreshes (rotating the token 5 times, breaking everything). The shared `refreshing` promise ensures **one** refresh happens and all queued requests reuse its result. This single-flight pattern is essential for rotation to work.

---

## XII. PROTECTED ROUTES ON THE FRONTEND

```jsx
// client/src/components/ProtectedRoute.jsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Spinner } from './states';

export default function ProtectedRoute({ children }) {
  const { user, booting } = useAuth();
  const location = useLocation();

  if (booting) return <Spinner label="Restoring session…" />;  // wait for silent refresh
  if (!user) {
    // Remember where they were headed, so login can send them back.
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return children;
}
```

```jsx
// client/src/App.jsx  (wrap private routes)
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';

<Routes>
  <Route element={<RootLayout />}>
    <Route path="login" element={<LoginPage />} />
    <Route
      path="tasks"
      element={<ProtectedRoute><TasksPage /></ProtectedRoute>}
    />
    <Route
      path="tasks/:id"
      element={<ProtectedRoute><TaskDetailPage /></ProtectedRoute>}
    />
  </Route>
</Routes>
```

```jsx
// client/src/pages/LoginPage.jsx
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await login(form);
      // Send them back where they were trying to go (or /tasks).
      navigate(location.state?.from?.pathname || '/tasks', { replace: true });
    } catch (err) {
      setError(err.message || 'Login failed');
    }
  };

  return (
    <form onSubmit={onSubmit} className="auth-form">
      <h1>Log in</h1>
      <input type="email" placeholder="Email" value={form.email}
        onChange={(e) => setForm({ ...form, email: e.target.value })} />
      <input type="password" placeholder="Password" value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })} />
      <button type="submit">Log in</button>
      {error && <p className="form-error" role="alert">{error}</p>}
    </form>
  );
}
```

> 🔒 **Gotcha — frontend protection is UX, not security.** `ProtectedRoute` hides screens from the UI, but a determined user can still call your API directly. **The real gate is the backend `protect` middleware.** Never rely on hiding a route to protect data — every protected endpoint must independently verify the token server-side. The frontend guard just spares users a useless screen.

---

## XIII. CSRF CONSIDERATIONS WITH COOKIE AUTH

Cookies are sent **automatically** by the browser — which is convenient and also the root of **CSRF (Cross-Site Request Forgery)**: a malicious site can make the browser fire a request to your API *with the cookie attached*, without the user intending it.

How TaskFlow mitigates it:

- **`SameSite` cookie attribute.** `SameSite=Lax` (dev) / `None; Secure` (cross-site prod) controls when the browser attaches the cookie cross-site. `Lax` already blocks most CSRF (cookies aren't sent on cross-site POSTs).
- **Scoped cookie path.** The refresh cookie uses `path: '/api/auth'`, so it is only ever sent to auth routes, shrinking the attack surface.
- **The access token is a header, not a cookie.** Task mutations require the `Authorization: Bearer` header, which a cross-site attacker *cannot* set (it isn't auto-attached like a cookie). This means our main API is inherently CSRF-resistant.
- **For cross-site cookie setups**, add a **CSRF token** (double-submit cookie or the `csurf`-style pattern): the server issues a token the client echoes in a header, and the server checks they match. An attacker can't read the token to echo it.

> 🔒 **The XSS ↔ CSRF tradeoff, summarized.** localStorage avoids CSRF but is wide open to XSS. httpOnly cookies resist XSS theft but invite CSRF. Our hybrid (refresh in cookie + access token in a header) gets the best of both: the powerful token is unreachable by scripts, and the per-request credential is a header CSRF can't forge. There is no option with zero risk — defend both: sanitize inputs/escape output (XSS) **and** use `SameSite` + CSRF tokens where needed.

---

## XIV. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Storing plaintext passwords | Catastrophic breach | bcrypt hash, cost ≥ 12 |
| Putting secrets in a JWT payload | Data leak (JWT is readable) | Payload = identity only |
| Access token in localStorage | XSS steals long-lived credential | Access token in memory; refresh in httpOnly cookie |
| No refresh rotation/storage | Can't revoke stolen tokens | Store + rotate refresh tokens; detect reuse |
| `SameSite`/`Secure` wrong in prod | Cookie not sent cross-domain | `SameSite=None; Secure` over HTTPS |
| Many parallel refreshes | Token rotated repeatedly, logout loop | Single-flight shared refresh promise |
| Treating all 401s the same | Logout on every expiry | Distinct `TOKEN_EXPIRED` → silent refresh |
| Relying on `ProtectedRoute` for security | API exposed despite hidden UI | Enforce auth in backend middleware |
| Auth flicker on reload | Login flashes for logged-in users | Gate UI on a `booting` flag during silent refresh |
| Leaking which credential was wrong | Email enumeration | Generic "Invalid credentials" |
| Ignoring CSRF with cookies | Forged state-changing requests | `SameSite`, scoped path, header tokens / CSRF token |

---

## 🧠 KEY TAKEAWAYS

- Use a **two-token** scheme: a **short access token** (proves identity per call) and a **long refresh token** (mints new access tokens). Short lifetimes limit blast radius.
- **Hash passwords with bcrypt** (cost ≥ 12), never store/log plaintext, and return a **generic** "Invalid credentials" to prevent enumeration.
- A **JWT is signed, not encrypted** — put identity in the payload, never secrets.
- Prefer the **hybrid storage** model: **refresh token in an httpOnly cookie** (XSS can't read it), **access token in memory** (short-lived, not persisted where scripts can scrape it).
- **Rotate refresh tokens** and store issued ones server-side so you can **revoke** and **detect reuse** (a theft signal → clear all sessions).
- **Backend middleware is the real gate**; frontend `ProtectedRoute` is UX only. Restore sessions with **silent refresh** on boot and gate the UI on a `booting` flag.
- Cookie auth invites **CSRF** — defend with `SameSite`, a scoped cookie path, header-based access tokens, and CSRF tokens for cross-site setups. There's no zero-risk option; defend XSS **and** CSRF.

---

**Prev:** [`03-Building-The-React-Frontend.md`](./03-Building-The-React-Frontend.md) · **Next:** [`05-State-File-Uploads-And-Realtime.md`](./05-State-File-Uploads-And-Realtime.md) · **Index:** [`00-Index.md`](./00-Index.md)
