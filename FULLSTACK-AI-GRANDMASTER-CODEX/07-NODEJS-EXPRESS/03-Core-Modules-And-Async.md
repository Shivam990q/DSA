# 🟢 03 — Core Modules & Async

> *"Frameworks come and go. The core modules — fs, http, events, stream, buffer — outlive them all. Learn the standard library and you can rebuild Express on a napkin."*

**Prev:** [`02-Modules-And-NPM.md`](./02-Modules-And-NPM.md) · **Next:** [`04-Express-Fundamentals.md`](./04-Express-Fundamentals.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE `node:` SCHEME AND WHY IT MATTERS

Modern Node prefers explicit core-module imports with the `node:` prefix:

```js
import fs from "node:fs/promises";
import path from "node:path";
import { EventEmitter } from "node:events";
```

Two reasons:

1. **No collision** — a future user-package called `fs` cannot shadow the core module.
2. **Faster resolution** — the loader doesn't walk `node_modules`.

Both `fs` and `node:fs` work; **prefer `node:`** in new code.

---

## II. THE FILE SYSTEM (`fs`) — THREE FLAVORS

Node ships **three APIs** for the file system:

```js
import fs from "node:fs";              // callback API + sync siblings
import fsSync from "node:fs";           // ...same module
import fsP from "node:fs/promises";     // promise API — preferred
```

### Callback API (the original)

```js
import { readFile } from "node:fs";
readFile("./hello.txt", "utf8", (err, data) => {
  if (err) return console.error("read failed", err);   // error-first
  console.log(data);
});
```

### Synchronous API (use sparingly)

```js
import { readFileSync, writeFileSync } from "node:fs";
const txt = readFileSync("./hello.txt", "utf8");       // BLOCKS the event loop
writeFileSync("./out.txt", txt.toUpperCase());
```

> **Rule:** sync `fs` is fine for **CLI tools, build scripts, and startup config**. **Never** in a request handler.

### Promise API (preferred for app code)

```js
import { readFile, writeFile, stat, mkdir, readdir, rm } from "node:fs/promises";

const text = await readFile("./hello.txt", "utf8");
await writeFile("./out.txt", text.toUpperCase());

const info = await stat("./hello.txt");
console.log(info.size, info.isFile(), info.mtime);

await mkdir("./logs", { recursive: true });             // mkdir -p
const entries = await readdir(".");                      // string[]
const detailed = await readdir(".", { withFileTypes: true }); // Dirent[]

await rm("./tmp", { recursive: true, force: true });    // rm -rf
```

### Reading huge files — use streams

```js
import { createReadStream } from "node:fs";
const rs = createReadStream("./bigfile.log", { encoding: "utf8", highWaterMark: 64 * 1024 });
rs.on("data", chunk => process.stdout.write(chunk));
rs.on("end", () => console.log("done"));
rs.on("error", err => console.error(err));
```

> **Gotcha — encoding matters.** Without `"utf8"`, you get a `Buffer`. Strings concatenate; buffers don't, and decoding a buffer mid-multibyte-char breaks Unicode.

> **Gotcha — relative paths are relative to the cwd**, not the file. If you want "next to my source file," combine `__dirname` (CJS) or `import.meta.url` (ESM) with `path.resolve`.

### File watching

```js
import { watch } from "node:fs";
watch("./src", { recursive: true }, (event, filename) => {
  console.log(event, filename);            // "change" | "rename"
});
```

`watch` is platform-quirky (sometimes fires twice, may miss on network mounts). For real apps use **chokidar** from npm.

---

## III. `path` — DON'T BUILD PATHS BY HAND

Different OSes use different separators (`\` on Windows, `/` elsewhere). `path` solves it.

```js
import path from "node:path";

path.join("a", "b", "..", "c");          // 'a/c'        (or 'a\\c' on Windows)
path.resolve("a", "b");                  // ABSOLUTE path
path.dirname("/a/b/c.txt");              // '/a/b'
path.basename("/a/b/c.txt");             // 'c.txt'
path.basename("/a/b/c.txt", ".txt");     // 'c'
path.extname("/a/b/c.txt");              // '.txt'
path.parse("/a/b/c.txt");                // { root, dir, base, ext, name }

path.sep;                                 // '/' or '\\'
path.posix.join("a", "b");                // always POSIX
path.win32.join("a", "b");                // always Windows

import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url));   // ESM "__dirname"
```

> **Rule:** never hand-concatenate paths with `+` or template strings. Always `path.join` / `path.resolve`. Saves you on Windows, on edge cases (`..`), and on URLs.

---

## IV. `os` — KNOW THY HOST

```js
import os from "node:os";

os.platform();          // 'linux' | 'darwin' | 'win32'
os.arch();              // 'x64' | 'arm64'
os.cpus().length;       // logical CPU count — useful for clustering
os.totalmem();          // bytes
os.freemem();
os.hostname();
os.userInfo();          // { username, homedir, shell, ... }
os.tmpdir();            // OS temp dir
os.networkInterfaces(); // IPs by interface
os.uptime();            // seconds
os.loadavg();           // [1m, 5m, 15m] (POSIX only)
os.EOL;                 // '\n' or '\r\n' — use this in cross-platform output
```

---

## V. RAW `http` — A SERVER FROM SCRATCH

Express is a wrapper around this. Knowing the raw API helps you debug *anything*.

```js
import http from "node:http";

const server = http.createServer((req, res) => {
  // req: IncomingMessage  (a Readable stream)
  // res: ServerResponse   (a Writable stream)

  console.log(req.method, req.url, req.headers["user-agent"]);

  if (req.method === "POST" && req.url === "/echo") {
    let body = "";
    req.on("data",  chunk => body += chunk);     // chunks are Buffers; coerce to string
    req.on("end",   () => {
      res.writeHead(200, { "content-type": "application/json" });
      res.end(JSON.stringify({ youSent: body }));
    });
    req.on("error", err => res.destroy(err));
    return;
  }

  if (req.url === "/") {
    res.statusCode = 200;
    res.setHeader("content-type", "text/plain");
    res.end("hello\n");
    return;
  }

  res.writeHead(404, { "content-type": "text/plain" });
  res.end("not found\n");
});

server.listen(3000, () => console.log("http://localhost:3000"));
```

### HTTP client — talk to APIs without a library

```js
// Built-in fetch (Node 18+) — preferred
const r = await fetch("https://api.github.com/users/torvalds");
const data = await r.json();
console.log(data.bio);

// Or the lower-level http.request
import http from "node:http";
const req = http.request("http://example.com", res => {
  let body = "";
  res.on("data", c => body += c);
  res.on("end",  () => console.log(res.statusCode, body.length));
});
req.end();
```

### HTTPS

```js
import https from "node:https";
import { readFileSync } from "node:fs";

https.createServer({
  key:  readFileSync("./key.pem"),
  cert: readFileSync("./cert.pem"),
}, (req, res) => res.end("secure")).listen(8443);
```

In production you usually terminate TLS at a reverse proxy (nginx, Caddy, a load balancer) and run plain HTTP behind it. Node *can* serve TLS directly; it's just often not the simplest deployment.

---

## VI. EVENTS & `EventEmitter`

Half of Node is an `EventEmitter` under the hood: `req`, `res`, `process`, `Server`, every stream.

```js
import { EventEmitter } from "node:events";

class Counter extends EventEmitter {
  constructor() { super(); this.n = 0; }
  inc() {
    this.n++;
    this.emit("tick", this.n);                 // synchronous fan-out
    if (this.n === 10) this.emit("done");
  }
}

const c = new Counter();
c.on("tick", n => console.log("tick", n));
c.once("done", () => console.log("done!"));     // fires once then auto-removes
c.on("error", err => console.error("oops", err)); // ALWAYS handle 'error'

for (let i = 0; i < 10; i++) c.inc();
```

### Important methods

| Method | Use |
|--------|-----|
| `on(event, fn)` / `addListener` | Subscribe |
| `once(event, fn)` | Subscribe for a single firing |
| `off(event, fn)` / `removeListener` | Unsubscribe |
| `removeAllListeners([event])` | Clean up |
| `emit(event, ...args)` | Fire synchronously |
| `setMaxListeners(n)` | Default warns at 10 — bump if intentional |
| `listenerCount(event)` | Count subscribers |

### `'error'` events are special

If you `emit('error', err)` and **no listener exists**, Node **crashes the process**. Always attach an `'error'` handler to anything that can fail (streams, sockets, child processes).

```js
// Bad — uncaught 'error' will kill the process
emitter.emit("error", new Error("boom"));

// Good
emitter.on("error", err => console.error("handled:", err));
```

### Async iteration over events (Node 12+)

```js
import { on, once } from "node:events";

const ee = new EventEmitter();
setTimeout(() => ee.emit("ping", 1), 100);
setTimeout(() => ee.emit("ping", 2), 200);
setTimeout(() => ee.emit("close"), 300);

// Wait for a single event
const [n] = await once(ee, "ping");

// Iterate many events with for-await
for await (const [val] of on(ee, "ping")) {
  console.log("got", val);
  if (val === 2) break;
}
```

---

## VII. STREAMS — NODE'S MASTER CONCEPT

Streams are how Node does **chunked, memory-bounded I/O with backpressure**. Every server, file, socket, and zlib pipeline is a stream. Four kinds:

| Kind | What it is | Example |
|------|------------|---------|
| **Readable** | You consume data from it | `fs.createReadStream`, HTTP request |
| **Writable** | You write data to it | `fs.createWriteStream`, HTTP response |
| **Duplex** | Both | TCP socket |
| **Transform** | Duplex that modifies the data | gzip, encryption, parsers |

### Reading a Readable

```js
import { createReadStream } from "node:fs";
const rs = createReadStream("./input.txt", { encoding: "utf8" });

rs.on("data",  chunk => console.log("chunk size", chunk.length));
rs.on("end",   () => console.log("done"));
rs.on("error", err => console.error(err));

// Or async-iterate it (cleaner):
for await (const chunk of rs) {
  console.log(chunk.length);
}
```

### Writing a Writable

```js
import { createWriteStream } from "node:fs";
const ws = createWriteStream("./out.txt");

const ok = ws.write("hello\n");           // returns false if internal buffer is full
if (!ok) ws.once("drain", () => ws.write("more"));   // backpressure handling

ws.end("bye\n");                           // flush + close
ws.on("finish", () => console.log("written"));
```

### `pipe` — connecting them up

```js
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";

createReadStream("./big.log")
  .pipe(createGzip())
  .pipe(createWriteStream("./big.log.gz"))
  .on("finish", () => console.log("zipped"));
```

`.pipe()` handles backpressure for you. Errors do **not** propagate by default — use `pipeline` instead:

```js
import { pipeline } from "node:stream/promises";   // promise version
import { createReadStream, createWriteStream } from "node:fs";
import { createGzip } from "node:zlib";

await pipeline(
  createReadStream("./big.log"),
  createGzip(),
  createWriteStream("./big.log.gz")
);
console.log("done — errors propagated to the awaiter");
```

> **Rule:** in production, **always use `pipeline`** instead of chained `.pipe()`. It cleans up streams and surfaces errors.

### Custom transforms

```js
import { Transform } from "node:stream";

const upper = new Transform({
  transform(chunk, _enc, cb) {
    cb(null, chunk.toString().toUpperCase());
  }
});

process.stdin.pipe(upper).pipe(process.stdout);    // type, see uppercased echo
```

### Object-mode streams

By default streams move bytes (Buffers/strings). You can move arbitrary objects:

```js
import { Readable } from "node:stream";
const events = Readable.from([{ id: 1 }, { id: 2 }, { id: 3 }]);   // sync iterable → stream
for await (const obj of events) console.log(obj);
```

### Web Streams interop

Node 18+ supports the **Web Streams API** (`ReadableStream`, `WritableStream`, `TransformStream`) — the same one that powers browser `fetch`. Helpers convert between them:

```js
import { Readable } from "node:stream";
const nodeStream = createReadStream("./x.txt");
const webStream  = Readable.toWeb(nodeStream);     // -> ReadableStream
const back       = Readable.fromWeb(webStream);    // -> Readable
```

This matters because `fetch().body` is a Web stream, and many edge runtimes (Cloudflare Workers, Bun, Deno) only speak Web streams.

---

## VIII. BUFFERS — RAW BINARY DATA

`Buffer` is Node's binary container. Strings are for text; Buffers are for bytes.

```js
const a = Buffer.from("hello", "utf8");         // 5 bytes
const b = Buffer.alloc(8);                      // 8 zero-filled bytes
const c = Buffer.allocUnsafe(8);                // FAST but contains old memory — fill before reading

console.log(a.length);                          // 5
console.log(a.toString("utf8"));                 // 'hello'
console.log(a.toString("hex"));                  // '68656c6c6f'
console.log(a.toString("base64"));               // 'aGVsbG8='

a[0] = 72;                                       // mutate a byte
console.log(a.toString());                       // 'Hello'

const merged = Buffer.concat([a, Buffer.from(" world")]);
console.log(merged.toString());                  // 'Hello world'

// Read structured binary
const buf = Buffer.from([0xDE, 0xAD, 0xBE, 0xEF]);
console.log(buf.readUInt32BE(0).toString(16));   // 'deadbeef'
```

> **Security note — `allocUnsafe`.** `Buffer.allocUnsafe(n)` is fast because Node skips zeroing; it can contain leftover data from prior allocations. Only use it when you'll fully overwrite it.

> **Encoding pitfall.** Multi-byte UTF-8 characters can be split across stream chunks. To decode safely, use `string_decoder`:
>
> ```js
> import { StringDecoder } from "node:string_decoder";
> const decoder = new StringDecoder("utf8");
> for await (const chunk of stream) process.stdout.write(decoder.write(chunk));
> process.stdout.write(decoder.end());
> ```

---

## IX. `crypto` — HASHING, RANDOM, ENCRYPTION

```js
import crypto from "node:crypto";

// Cryptographically secure random
const id = crypto.randomUUID();                   // e.g. '0a8b...4f'
const token = crypto.randomBytes(32).toString("hex");

// One-way hashing (NOT for passwords — use bcrypt/argon2; see file 07)
const sha = crypto.createHash("sha256").update("hello").digest("hex");

// HMAC — message authentication code
const sig = crypto.createHmac("sha256", "secret").update("payload").digest("hex");

// Constant-time string comparison (prevents timing attacks)
const equal = crypto.timingSafeEqual(Buffer.from("abc"), Buffer.from("abc"));
```

> **Gotcha — never `==` for secrets.** Use `crypto.timingSafeEqual` so an attacker cannot guess byte-by-byte by measuring response times.

`crypto` also does AES, RSA, KDFs (`pbkdf2`, `scrypt`), and JWT primitives. We dive deeper in file 07 (auth & security).

---

## X. `util` — THE QUIET WORKHORSE

```js
import util from "node:util";

// promisify — turn a callback API into a promise
import { exec as execCb } from "node:child_process";
const exec = util.promisify(execCb);
const { stdout } = await exec("git rev-parse HEAD");

// callbackify — the reverse (rare)
const fn = util.callbackify(async () => 42);

// inspect — prettier console.log
console.log(util.inspect({ a: 1, b: [1,2,3] }, { colors: true, depth: 4 }));

// types — runtime type checks
util.types.isPromise(Promise.resolve());                    // true
util.types.isUint8Array(new Uint8Array());                   // true

// format — printf-like
console.log(util.format("user %s id=%d cfg=%j", "ada", 42, { x: 1 }));
```

---

## XI. CALLBACKS → PROMISES → ASYNC/AWAIT — THE EVOLUTION

### Callback hell (don't do this anymore)

```js
import { readFile, writeFile } from "node:fs";
readFile("a.txt", "utf8", (err, a) => {
  if (err) return console.error(err);
  readFile("b.txt", "utf8", (err, b) => {
    if (err) return console.error(err);
    writeFile("c.txt", a + b, err => {
      if (err) return console.error(err);
      console.log("done");                        // ← four levels deep
    });
  });
});
```

### Promises — flat chains

```js
import { readFile, writeFile } from "node:fs/promises";
readFile("a.txt", "utf8")
  .then(a => readFile("b.txt", "utf8").then(b => [a, b]))
  .then(([a, b]) => writeFile("c.txt", a + b))
  .then(() => console.log("done"))
  .catch(console.error);
```

### `async`/`await` — sync-looking, async-running

```js
import { readFile, writeFile } from "node:fs/promises";

async function combine(out, ...inputs) {
  const parts = await Promise.all(inputs.map(f => readFile(f, "utf8")));
  await writeFile(out, parts.join(""));
}

try {
  await combine("c.txt", "a.txt", "b.txt");
} catch (err) {
  console.error("failed:", err);
}
```

### Promise combinators — pick the right one

| Combinator | Resolves when | Rejects when |
|------------|---------------|--------------|
| `Promise.all([p1, p2])` | All resolve | Any rejects (fail-fast) |
| `Promise.allSettled([p1, p2])` | All settle | Never rejects — gives `{status, value/reason}` |
| `Promise.race([p1, p2])` | First settles | First settles with rejection |
| `Promise.any([p1, p2])` | First resolves | All reject (`AggregateError`) |

```js
const results = await Promise.allSettled(urls.map(u => fetch(u)));
const ok = results.filter(r => r.status === "fulfilled").map(r => r.value);
```

### Sequential vs parallel — easy to confuse

```js
// Sequential — slower, awaits one at a time
for (const u of urls) {
  const r = await fetch(u);                      // each waits for the previous
  console.log(await r.text());
}

// Parallel — kicks off all, awaits together
const responses = await Promise.all(urls.map(u => fetch(u)));
```

### `util.promisify` for old-school callback APIs

```js
import { promisify } from "node:util";
import { execFile as execFileCb } from "node:child_process";
const execFile = promisify(execFileCb);
const { stdout } = await execFile("node", ["--version"]);
```

### Async iterators — for-await-of

```js
async function* take(iter, n) {
  let i = 0;
  for await (const x of iter) {
    if (i++ >= n) return;
    yield x;
  }
}
import { createReadStream } from "node:fs";
for await (const line of take(createReadStream("./big.log"), 5)) {
  console.log(line.toString().slice(0, 80));
}
```

---

## XII. ERROR-FIRST CALLBACKS — THE NODE CONVENTION

If you read older Node code, every callback's first argument is `err`:

```js
function readJSON(path, cb /* (err, data) */) {
  fs.readFile(path, "utf8", (err, txt) => {
    if (err) return cb(err);
    try { cb(null, JSON.parse(txt)); }
    catch (e) { cb(e); }
  });
}
```

Rules:

1. First argument is the error (or `null`/`undefined` on success).
2. The callback is invoked **exactly once**.
3. Sync errors must not "escape" — wrap risky calls (`JSON.parse`) and forward through the callback.

> **Promote it forward.** If you hit one in 2024+, wrap it with `util.promisify` and never look back.

---

## XIII. `AbortController` — CANCELLING ASYNC WORK

Every modern async API in Node (and browsers) accepts an `AbortSignal`:

```js
const ctrl = new AbortController();

setTimeout(() => ctrl.abort(new Error("too slow")), 100);

try {
  const r = await fetch("https://httpbin.org/delay/3", { signal: ctrl.signal });
  console.log(r.status);
} catch (e) {
  console.error("aborted:", e.message);          // 'too slow' or AbortError
}

// fs supports it too:
import { readFile } from "node:fs/promises";
const ac = new AbortController();
setTimeout(() => ac.abort(), 50);
await readFile("./huge.bin", { signal: ac.signal });
```

Use it for HTTP timeouts, cancellable workflows, and graceful shutdown.

---

## XIV. A REAL EXAMPLE — A MINI LOG-STREAMER (CLI)

```js
// tail-and-count.js
// Usage:  node tail-and-count.js ./access.log
import { createReadStream } from "node:fs";
import { Transform, pipeline } from "node:stream";
import { promisify } from "node:util";
const pipe = promisify(pipeline);

const file = process.argv[2];
if (!file) { console.error("usage: node tail-and-count.js <file>"); process.exit(1); }

let bytes = 0, lines = 0;

const counter = new Transform({
  transform(chunk, _enc, cb) {
    bytes += chunk.length;
    for (const b of chunk) if (b === 10) lines++;     // 10 = '\n'
    cb(null, chunk);                                    // pass through
  }
});

await pipe(createReadStream(file), counter, process.stdout);
console.error(`\n${lines.toLocaleString()} lines, ${bytes.toLocaleString()} bytes`);
```

This builds a streaming pipeline with bounded memory: it would happily process a 50 GB file.

---

## XV. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Sync `fs` in a request handler | All requests stall | Use `node:fs/promises` |
| Forgetting `'error'` listener | Unhandled stream/EE error crashes process | Always `.on('error', ...)` |
| Plain `pipe` chain | Errors swallowed, leaks | `stream.pipeline` (or `pipeline` from `node:stream/promises`) |
| Decoding multibyte strings naively | Garbled chars | `StringDecoder` or stream `setEncoding` |
| `Buffer.allocUnsafe` w/o overwriting | Leaked memory contents | Use `Buffer.alloc` unless you'll fill it |
| `==` for tokens/HMACs | Timing attack | `crypto.timingSafeEqual` |
| `await` inside a `.forEach` | Doesn't wait | Use `for...of` or `Promise.all(map)` |
| `Promise.all` for tasks that can fail independently | One rejection kills others | `Promise.allSettled` |
| Sequential `await` in a loop when parallel is fine | Slow | `Promise.all(map)` |
| Hand-built paths | Breaks on Windows | `path.join` / `path.resolve` |
| Relative paths off the cwd | "Works in dev, fails when cron runs" | Anchor with `__dirname` / `import.meta.url` |
| EventEmitter listener leak | "Possible MaxListenersExceeded" warning | `off()` listeners or set `setMaxListeners` deliberately |
| Mixing sync and async fs | Race conditions | Pick one API, stay with it |

---

## 🧠 KEY TAKEAWAYS

- Use the `node:` prefix and the **promise** flavor of core modules (`node:fs/promises`).
- `path` and `os` exist so your code is portable; never hand-build paths.
- The raw `http` module is enough to write a server — Express is a layer on top.
- **Everything is an `EventEmitter`**: listen, unlisten, always handle `'error'`.
- **Streams + backpressure** are how Node moves big data without big memory; use `pipeline`, not `pipe`.
- `Buffer` is bytes; strings are text — and they decode differently across chunks.
- Async lifecycle in Node: callbacks → promises → **async/await**. Use `Promise.all` for parallelism, `allSettled` when failures are independent.
- `AbortController` cancels timers, fetches, and fs reads — wire it into request timeouts and graceful shutdown.

---

**Prev:** [`02-Modules-And-NPM.md`](./02-Modules-And-NPM.md) · **Next:** [`04-Express-Fundamentals.md`](./04-Express-Fundamentals.md) · **Index:** [`00-Index.md`](./00-Index.md)
