# 📨 HTTP and HTTPS

> *"HTTP is just text. Two computers exchanging carefully formatted messages. Once you can read it, the whole web stops being magic."*

The previous chapter got bytes from one machine to another. This chapter is about *what those bytes say*. **HTTP** (HyperText Transfer Protocol) is the language clients and servers use to ask for and deliver things on the web. Every API call, every page load, every image fetch is an HTTP request and response. Understanding it deeply is non-negotiable for backend, frontend, and full-stack work alike.

---

## I. THE REQUEST–RESPONSE MODEL

HTTP is a **request–response** protocol. The client sends a **request**; the server sends back a **response**. The client always speaks first. HTTP is also **stateless** — each request is independent; the server does not remember previous requests on its own. (We bolt state on top with cookies/tokens — see §VIII.)

```
CLIENT                                    SERVER
  │                                         │
  │ ───── HTTP Request ──────────────────▶  │
  │   "GET /products HTTP/1.1"              │  (server processes,
  │                                         │   maybe hits a DB)
  │ ◀──── HTTP Response ──────────────────  │
  │   "200 OK" + JSON/HTML body             │
  │                                         │
```

---

## II. ANATOMY OF AN HTTP REQUEST

Every request has up to four parts:

```
GET /api/products?category=books HTTP/1.1      ← 1. Request line (method, path+query, version)
Host: shop.example.com                          ┐
User-Agent: Mozilla/5.0 ...                     │  2. Headers
Accept: application/json                        │     (metadata: key: value)
Authorization: Bearer eyJhbGci...               ┘
                                                ← 3. Blank line (separates headers from body)
{ "no body for GET, but POST/PUT would put data here" }   ← 4. Body (optional)
```

1. **Request line** — the *method* (what to do), the *path* (+ optional query string), and the HTTP version.
2. **Headers** — metadata as `Key: Value` pairs (who's asking, what formats they accept, auth, etc.).
3. **Blank line** — marks the end of headers.
4. **Body** — the payload, for methods that send data (POST/PUT/PATCH). GET typically has none.

---

## III. ANATOMY OF AN HTTP RESPONSE

```
HTTP/1.1 200 OK                                 ← Status line (version, status code, reason)
Content-Type: application/json                  ┐
Content-Length: 87                              │  Headers
Cache-Control: max-age=3600                     ┘
                                                ← Blank line
{ "products": [ { "id": 1, "name": "Clean Code" } ] }   ← Body (the actual data)
```

- **Status line** — the HTTP version, a numeric **status code**, and a short reason phrase.
- **Headers** — metadata about the response (content type, length, caching rules, cookies to set).
- **Body** — the actual content: HTML, JSON, an image, a file, or nothing.

---

## IV. HTTP METHODS (VERBS)

The **method** declares the *intent* of a request. The common ones map neatly onto CRUD (Create, Read, Update, Delete) operations.

| Method | Purpose | CRUD | Has body? | Idempotent? | Safe? |
|---|---|---|---|---|---|
| **GET** | Retrieve a resource | Read | No | ✅ Yes | ✅ Yes |
| **POST** | Create a resource / submit data | Create | Yes | ❌ No | ❌ No |
| **PUT** | Replace a resource entirely | Update | Yes | ✅ Yes | ❌ No |
| **PATCH** | Partially update a resource | Update | Yes | ❌ Not necessarily | ❌ No |
| **DELETE** | Remove a resource | Delete | Optional | ✅ Yes | ❌ No |

Two important properties:
- **Safe** = doesn't change server state (only GET, really). A GET should *never* modify data.
- **Idempotent** = doing it once or many times has the same effect. `PUT /users/5` with the same body, run 10 times, leaves the same result. `POST` is not idempotent — calling it twice creates two resources.

```http
GET    /api/users/5            → fetch user 5
POST   /api/users             → create a new user (body has the data)
PUT    /api/users/5            → replace user 5 entirely (body = full new representation)
PATCH  /api/users/5            → update part of user 5 (body = just the changed fields)
DELETE /api/users/5            → delete user 5
```

> **Gotcha:** The methods are *conventions*, not enforced by HTTP itself. A badly designed API *could* delete data on a GET — and that's a real bug, because crawlers and prefetchers fire GETs freely. Respect the semantics: GET = read only.

### Other methods you'll meet
- **HEAD** — like GET but returns only headers (no body); used to check existence/size cheaply.
- **OPTIONS** — asks what's allowed; central to CORS preflight (see `06-...Security-Basics.md`).

---

## V. STATUS CODES

The server's response always carries a 3-digit **status code** telling the client how it went. They're grouped by first digit:

| Range | Class | Meaning |
|---|---|---|
| **1xx** | Informational | Request received, continuing (rarely seen directly) |
| **2xx** | Success | It worked |
| **3xx** | Redirection | Go look elsewhere |
| **4xx** | Client error | *You* (the client) made a mistake |
| **5xx** | Server error | *The server* broke |

### The ones you must know cold

| Code | Name | When |
|---|---|---|
| **200** | OK | Standard success |
| **201** | Created | Success, and a new resource was created (after POST) |
| **204** | No Content | Success, nothing to return (often after DELETE) |
| **301** | Moved Permanently | Resource has a new permanent URL (SEO-relevant) |
| **302 / 307** | Found / Temporary Redirect | Temporary redirect |
| **304** | Not Modified | Your cached copy is still valid (saves bandwidth) |
| **400** | Bad Request | Malformed request / invalid input |
| **401** | Unauthorized | You're not authenticated (log in first) |
| **403** | Forbidden | You're authenticated but *not allowed* |
| **404** | Not Found | No such resource |
| **409** | Conflict | Request conflicts with current state (e.g. duplicate) |
| **422** | Unprocessable Entity | Syntactically fine but semantically invalid (validation) |
| **429** | Too Many Requests | Rate limited — slow down |
| **500** | Internal Server Error | The server threw an unhandled error |
| **502** | Bad Gateway | A server upstream gave a bad response |
| **503** | Service Unavailable | Server overloaded or down for maintenance |

> **The 401 vs 403 trap:** **401** = "I don't know who you are" (authentication missing/invalid). **403** = "I know who you are, and you can't do this" (authorization failed). Mixing these up is one of the most common API bugs.

```javascript
// A well-behaved Express endpoint using correct status codes
app.post("/api/posts", async (req, res) => {
  if (!req.user)            return res.status(401).json({ error: "Login required" });
  if (!req.user.canPost)    return res.status(403).json({ error: "Not allowed" });
  if (!req.body.title)      return res.status(400).json({ error: "Title is required" });

  const post = await db.createPost(req.body);
  return res.status(201).json(post);   // 201 = created
});
```

---

## VI. HEADERS — THE METADATA OF THE WEB

Headers are `Key: Value` pairs carrying everything *about* the request/response that isn't the body itself. A few you'll use constantly:

### Request headers
| Header | Purpose |
|---|---|
| `Host` | Which domain the request is for (one IP can serve many sites) |
| `User-Agent` | What client is asking (browser/OS/bot) |
| `Accept` | What content types the client can handle (`application/json`, `text/html`) |
| `Content-Type` | The format of the request *body* you're sending |
| `Authorization` | Credentials, e.g. `Bearer <token>` |
| `Cookie` | Cookies the client is sending back to the server |
| `Accept-Encoding` | Compression the client supports (`gzip`, `br`) |

### Response headers
| Header | Purpose |
|---|---|
| `Content-Type` | The format of the response body |
| `Content-Length` | Size of the body in bytes |
| `Set-Cookie` | Tells the browser to store a cookie |
| `Cache-Control` | How/whether to cache this response |
| `Location` | Where to go (used with 3xx redirects, and 201) |
| `Access-Control-Allow-Origin` | CORS — who may read this response (see ch. 6) |

> **Gotcha — `Content-Type` matters:** If you send JSON but set `Content-Type: text/plain`, many clients won't parse it as JSON. If a form posts as `application/x-www-form-urlencoded` but your server expects `application/json`, the body arrives empty. Always match the header to the actual body format.

---

## VII. SEEING HTTP YOURSELF

The best way to learn HTTP is to *watch it*. Two tools:

```bash
# curl: make raw requests from the terminal
curl -i https://api.github.com           # -i shows response headers + body
curl -X POST https://httpbin.org/post \
     -H "Content-Type: application/json" \
     -d '{"name":"Ada"}'                  # send a JSON body

curl -v https://example.com 2>&1 | head   # -v = verbose: see request AND response lines
```

In the **browser**: press **F12 → Network tab**, reload a page, and click any request. You'll see its method, status, headers, and body — exactly the anatomy from §II–III. Do this often; it makes HTTP tangible.

---

## VIII. STATE: COOKIES, SESSIONS, AND TOKENS

HTTP is **stateless** — the server forgets you between requests. But real apps need to remember "this is the logged-in user." We add state on top:

### Cookies
A **cookie** is a small piece of data the server asks the browser to store and send back on every future request to that site.

```http
# 1. Server response sets a cookie:
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict; Max-Age=3600

# 2. Browser automatically includes it on subsequent requests:
Cookie: session_id=abc123
```

Important cookie attributes (security-critical):
| Attribute | Effect |
|---|---|
| `HttpOnly` | JavaScript *cannot* read it → mitigates XSS theft |
| `Secure` | Only sent over HTTPS |
| `SameSite` | Controls whether it's sent on cross-site requests → mitigates CSRF |
| `Max-Age` / `Expires` | How long it lives |
| `Domain` / `Path` | Scope of where it applies |

### Two common auth patterns
1. **Session-based:** server stores session data; the cookie holds only a session ID. Server looks up the rest. Easy to revoke; needs server-side storage.
2. **Token-based (JWT):** server issues a signed token (often a **JWT**) the client sends in the `Authorization: Bearer <token>` header. Server verifies the signature without storing anything. Stateless and scalable; harder to revoke early.

(Both are covered deeply in `11-FULLSTACK-ENGINEERING`.)

> **Gotcha:** Storing auth tokens in `localStorage` exposes them to XSS (any injected JS can read them). `HttpOnly` cookies can't be read by JS but are vulnerable to CSRF unless protected by `SameSite`/anti-CSRF tokens. There's no free lunch — understand the tradeoff before choosing.

---

## IX. HTTPS — HTTP, BUT ENCRYPTED

**HTTPS** is HTTP running inside an encrypted, authenticated channel provided by **TLS** (Transport Layer Security; the successor to SSL). It provides three guarantees:

1. **Confidentiality** — eavesdroppers see only scrambled bytes, not your data/passwords.
2. **Integrity** — data can't be tampered with in transit without detection.
3. **Authenticity** — you're really talking to `example.com`, not an impostor (verified via certificates).

### The TLS handshake (simplified)

```
Client ──── ClientHello ───────▶ Server     "Here are the encryption methods I support."
Client ◀─── ServerHello + Cert ─ Server     "Let's use this method. Here's my certificate."
       (Client verifies the certificate against trusted Certificate Authorities)
Client ──── key exchange ───────▶ Server     Both derive a shared secret session key.
       ◀════ encrypted data ═════▶           All further HTTP is encrypted with that key.
```

- **Certificates** are issued by **Certificate Authorities (CAs)** — trusted third parties (e.g. Let's Encrypt, which issues them free). Your browser ships with a list of CAs it trusts; a cert signed by one of them proves the site's identity.
- After the handshake, encryption uses fast **symmetric** keys; the slow **asymmetric** (public/private key) crypto is only used to securely agree on those keys.

### Why HTTPS is mandatory now
- Browsers mark plain HTTP sites as "Not Secure."
- Features like service workers, geolocation, and HTTP/2 require HTTPS.
- It protects users on shared/public networks from eavesdropping and injection.

> **Gotcha:** HTTPS protects data *in transit*, not data *at rest* on the server, and not from a malicious site itself. A phishing site can have a perfectly valid HTTPS certificate — the padlock means "encrypted connection to *this* domain," not "this site is trustworthy."

---

## X. HTTP VERSIONS (BRIEF)

| Version | Key improvement |
|---|---|
| **HTTP/1.1** | Persistent connections (reuse a TCP connection for multiple requests) |
| **HTTP/2** | **Multiplexing** — many requests in parallel over one connection; header compression |
| **HTTP/3** | Runs over **QUIC** (UDP-based) — faster setup, no head-of-line blocking |

You rarely choose this directly (the server/CDN does), but it explains performance differences. Multiplexing in HTTP/2+ is why the old trick of bundling everything into one file matters less than it used to.

---

## XI. COMMON PITFALLS / GOTCHAS

- **Using GET to change data.** GET must be safe and idempotent. Crawlers and prefetchers fire GETs unprompted — a "GET /delete?id=5" link will get clicked by a bot.
- **Wrong status codes.** Returning `200 OK` with an `{ "error": ... }` body breaks clients that check the status. Use the right code (400/401/403/404/500).
- **401 vs 403 confusion.** Authentication vs authorization — see §V.
- **Mismatched `Content-Type`.** Header must match the actual body format, or parsing silently fails.
- **Trusting client input.** Anyone can craft any request with curl/Postman, bypassing your frontend validation entirely. The server must re-validate everything.
- **Assuming HTTPS = safe site.** It means encrypted transport to that domain, not a trustworthy operator.
- **Forgetting HTTP is stateless.** The server doesn't "remember" you — every request must carry its own identity (cookie/token).

---

## ✅ KEY TAKEAWAYS

- HTTP is a **stateless, text-based, request–response** protocol. The client always asks first.
- A request = **method + path + headers + (optional) body**; a response = **status code + headers + body**.
- **Methods** declare intent: GET (read, safe), POST (create), PUT (replace), PATCH (partial update), DELETE (remove). Respect *safe* and *idempotent* semantics.
- **Status codes** by class: 2xx success, 3xx redirect, 4xx client error, 5xx server error. Know 200/201/204/301/304/400/401/403/404/409/422/429/500/502/503 — especially the **401 vs 403** distinction.
- **Headers** carry metadata (`Content-Type`, `Authorization`, `Cache-Control`, `Set-Cookie`...); match `Content-Type` to your body.
- State is added with **cookies** (session-based) or **tokens/JWT** (stateless); secure cookies with `HttpOnly`, `Secure`, `SameSite`.
- **HTTPS = HTTP over TLS**, giving confidentiality, integrity, and authenticity via CA-issued certificates and a handshake. It protects the connection, not the trustworthiness of the site.
- **Watch real HTTP** with `curl -v` and the browser Network tab — it's the fastest way to make this concrete.

---

**→ Next:** [`03-Browsers-And-Rendering.md`](./03-Browsers-And-Rendering.md) — what the browser does with the response
**← Prev:** [`01-How-The-Internet-Works.md`](./01-How-The-Internet-Works.md)
**🗺️ Index:** [`00-Index.md`](./00-Index.md)
