# 🟢 01 — The Node.js Runtime

> *"JavaScript without the browser is just a language with no body. Node is the body — V8 is the brain, libuv is the nervous system, and the event loop is the heartbeat."*

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-Modules-And-NPM.md`](./02-Modules-And-NPM.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT NODE.JS ACTUALLY IS

Node.js is a **JavaScript runtime** — a program that takes JS source and executes it outside the browser. It was first released in **2009 by Ryan Dahl** with one defining design choice:

> Use **JavaScript's single-threaded event loop** + **non-blocking I/O** to handle thousands of concurrent connections without spawning thousands of threads.

That choice came from a complaint about Apache: each new connection cost a thread, threads cost memory, and most threads sat idle waiting on I/O. Node flipped the model — one thread, one queue of pending operations, and the OS does the actual waiting.

```
┌──────────────────────────────────────────────────────────────────┐
│                         Your JavaScript                          │
└──────────────────────────────────────────────────────────────────┘
            │ runs inside ▼
┌──────────────────────────────────────────────────────────────────┐
│                            Node.js                                │
│  ┌──────────────┐   ┌──────────────────────────────────────────┐ │
│  │      V8      │   │                  libuv                   │ │
│  │  (executes   │◄─►│  • event loop                            │ │
│  │   JS, JIT,   │   │  • thread pool (fs, dns, crypto, zlib)   │ │
│  │   GC, heap)  │   │  • OS async APIs (epoll, kqueue, IOCP)   │ │
│  └──────────────┘   └──────────────────────────────────────────┘ │
│                Node bindings (C++) — http, fs, net, ...          │
└──────────────────────────────────────────────────────────────────┘
                              ▼ system calls
                       Operating System
```

**Two facts to internalize:**

1. There is exactly **one thread running your JavaScript**. Two pieces of JS never execute simultaneously in the same Node process.
2. **I/O is offloaded** to the OS or to a small thread pool. While the OS is reading a file or talking to a database, your JS thread is free to do other work.

> **Gotcha — "single-threaded" is misleading.** Your JS runs on one thread; Node itself uses *multiple* threads under the hood (libuv's thread pool, V8 helper threads). The point is that *your code* is serial.

---

## II. V8 — THE ENGINE

**V8** is Google's open-source JavaScript engine, the same one in Chrome. It does the heavy lifting:

- **Parse** JS source into an AST.
- **Compile** to bytecode (Ignition interpreter), then JIT-compile **hot** functions to optimized native machine code (TurboFan).
- Manage the **heap** and run **garbage collection** (generational, mostly Orinoco / Scavenger + Mark-Sweep-Compact).

```js
// You write:
function add(a, b) { return a + b; }
for (let i = 0; i < 1e6; i++) add(i, i);  // hot — V8 optimizes it to native code

// You can ask V8 to dump optimization info (debug builds):
//   node --trace-opt --trace-deopt script.js
```

V8 uses **hidden classes** to lay out objects efficiently. If you mutate an object's "shape" repeatedly (adding/removing properties at random places), you defeat that optimization.

```js
// Predictable shape — V8 builds one hidden class for both
function Point(x, y) { this.x = x; this.y = y; }
const a = new Point(1, 2);
const b = new Point(3, 4);

// Bad — different shapes on the fly
const c = {};
c.x = 1;
c.y = 2;
c.z = 3;        // shape change
delete c.y;     // shape change again — slow path
```

> **Takeaway:** V8 is brilliant. You almost never tune it manually. But avoid wildly polymorphic objects in hot paths.

---

## III. libuv — THE ASYNC HEART

**libuv** is the C library that gives Node its async I/O. It abstracts platform differences:

| Platform | Mechanism libuv uses |
|----------|----------------------|
| Linux | `epoll` |
| macOS / BSD | `kqueue` |
| Windows | `IOCP` (I/O Completion Ports) |
| Solaris | event ports |

When you call `fs.readFile(...)`, Node hands the work to **libuv**, which either:

- Asks the OS for an **async notification** (sockets, pipes, network), or
- Uses the **thread pool** (default size **4**) to do work that has no good async OS API — file system, DNS, `crypto.pbkdf2`, `zlib`.

You can grow that pool:

```bash
# Bigger pool = more parallel CPU-bound or fs work
UV_THREADPOOL_SIZE=8 node app.js
```

> **Gotcha — the thread pool default is 4.** If you do many concurrent `bcrypt.hash` calls or heavy `pbkdf2`, they queue up. Bump `UV_THREADPOOL_SIZE` or move work to **worker threads** (file 08).

---

## IV. THE EVENT LOOP

This is the single most important diagram in Node.

```
       ┌───────────────────────────┐
   ┌──►│           timers          │  setTimeout / setInterval callbacks
   │   └─────────────┬─────────────┘
   │   ┌─────────────▼─────────────┐
   │   │     pending callbacks     │  some system errors deferred from prev loop
   │   └─────────────┬─────────────┘
   │   ┌─────────────▼─────────────┐
   │   │      idle, prepare        │  internal use only
   │   └─────────────┬─────────────┘   waits for I/O ─┐
   │   ┌─────────────▼─────────────┐                  │
   │   │           poll            │◄─ retrieves new  │
   │   └─────────────┬─────────────┘   I/O events     │
   │   ┌─────────────▼─────────────┐                  │
   │   │           check           │  setImmediate callbacks
   │   └─────────────┬─────────────┘
   │   ┌─────────────▼─────────────┐
   └───┤      close callbacks      │  socket.on('close', ...)
       └───────────────────────────┘
```

After **every phase** (and between many internal steps), Node drains:

1. **`process.nextTick` queue** — runs *before* anything else.
2. **Microtask queue** — Promise `.then` / `await` continuations.

So microtasks always beat macrotasks (timers, I/O). That single fact explains 80% of "weird order" bugs.

```js
// order.js
console.log("1: sync");

setTimeout(() => console.log("4: setTimeout"), 0);
setImmediate(() => console.log("5: setImmediate"));

Promise.resolve().then(() => console.log("3: promise (microtask)"));
process.nextTick(() => console.log("2: nextTick (before microtasks)"));

console.log("0: sync");
```

```bash
$ node order.js
1: sync
0: sync
2: nextTick (before microtasks)
3: promise (microtask)
4: setTimeout      # or 5 first — see gotcha
5: setImmediate
```

> **Gotcha — `setTimeout(fn, 0)` vs `setImmediate(fn)`.** Order is **not** guaranteed when called from the main module. Inside an I/O callback, **`setImmediate` always runs first**. Rely on neither for correctness.

```js
// Inside an I/O callback, setImmediate beats setTimeout — guaranteed
import { readFile } from "node:fs";
readFile(__filename, () => {
  setTimeout(() => console.log("timeout"), 0);
  setImmediate(() => console.log("immediate"));   // prints first
});
```

### Microtasks: nextTick vs Promise

- `process.nextTick(fn)` — runs **before** the microtask queue, before *any* other phase resumes. Use it to defer "right after this synchronous code, but before anything else."
- `queueMicrotask(fn)` / `Promise.resolve().then(fn)` — runs in the microtask queue.

> **Gotcha — nextTick starvation.** Recursing with `process.nextTick` blocks the loop forever, because Node keeps draining nextTicks before moving on. Don't loop with it; use `setImmediate` if you need to yield.

```js
// DO NOT DO THIS — starves the event loop
function evil() { process.nextTick(evil); }
// evil();   // every other timer/I/O is now blocked
```

---

## V. NON-BLOCKING I/O — THE WHOLE POINT

The win of Node is that **I/O does not block the JS thread**.

```js
// Blocking, sync — pauses the entire process
import { readFileSync } from "node:fs";
const data = readFileSync("./big.log", "utf8");   // 200ms? Nothing else runs.
console.log(data.length);

// Non-blocking, async — JS keeps going; libuv calls back later
import { readFile } from "node:fs/promises";
readFile("./big.log", "utf8").then(d => console.log(d.length));
console.log("This prints first.");
```

If you accidentally do CPU-heavy work *synchronously* on the JS thread, **everything else stalls** — every HTTP request, every timer.

```js
// CPU-bound work — bad on the main thread
function heavy(n) {
  let s = 0;
  for (let i = 0; i < n; i++) s += Math.sqrt(i);
  return s;
}
import http from "node:http";
http.createServer((req, res) => {
  heavy(5e8);                  // blocks the loop for seconds — server unresponsive
  res.end("done");
}).listen(3000);
```

**Fixes (file 08 covers each):**

- Move the work to a **worker thread**.
- Run multiple Node processes via **cluster** or **pm2**.
- Stream / chunk the work and `await` between chunks (`setImmediate` to yield).

---

## VI. `process` AND `global`

Node exposes a couple of host objects you rely on daily.

### `process`

```js
console.log(process.pid);           // OS process id
console.log(process.version);       // Node version, e.g. v20.11.1
console.log(process.platform);      // "win32" | "linux" | "darwin"
console.log(process.arch);          // "x64" | "arm64"
console.log(process.cwd());         // current working directory
console.log(process.env.NODE_ENV);  // environment variables
console.log(process.argv);          // [node, script, ...args]
console.log(process.uptime());      // seconds since process start
console.log(process.memoryUsage()); // heap, rss, external...

process.exit(1);                    // terminate (use sparingly — see graceful shutdown, file 08)
```

`process` is also an **EventEmitter**:

```js
process.on("exit",   code => console.log("exiting with", code));
process.on("uncaughtException", err => { console.error("CRASH:", err); process.exit(1); });
process.on("unhandledRejection", reason => { console.error("UNHANDLED PROMISE:", reason); });
process.on("SIGTERM", () => { /* graceful shutdown — file 08 */ });
```

> **Rule:** `uncaughtException` is a **last resort**, not a control-flow tool. Log, flush, exit — don't keep running.

### `global` and `globalThis`

- `globalThis` — the standard global object (works in browsers and Node).
- `global` — Node alias for the same thing. Avoid putting random stuff on it.

### Module-level locals (CommonJS)

Inside a CJS module, Node injects these:

```js
console.log(__dirname);   // absolute directory of the current file
console.log(__filename);  // absolute path of the current file
// require, module, exports — also injected
```

In **ESM** they don't exist. Use:

```js
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
```

---

## VII. THE NODE CLI — THE TOOLS YOU'LL ACTUALLY USE

```bash
node script.js                  # run a file
node                            # REPL — interactive
node -e "console.log(2+2)"      # one-liner
node -p "1+1"                   # print expression
node --version                  # v20.x.x
node --help                     # ALL flags

# Watch mode (Node 20+) — auto-restart on file change, no nodemon needed
node --watch index.js

# ESM / CJS toggles
node --input-type=module -e "import os from 'node:os'; console.log(os.cpus().length)"

# Inspect / debug — opens DevTools-compatible debugger
node --inspect index.js                  # 9229 default
node --inspect-brk index.js              # break on first line
# Open chrome://inspect in Chrome to attach.

# Heap snapshot
node --heapsnapshot-near-heap-limit=2 --max-old-space-size=512 index.js

# Diagnostics report (one-shot JSON of process state)
node --report-on-fatalerror --report-uncaught-exception index.js

# Profile CPU
node --prof index.js               # produces isolate-*.log
node --prof-process isolate-*.log  # human-readable summary
```

### Environment variables you should know

```bash
NODE_ENV=production node app.js     # frameworks change behavior on this
NODE_OPTIONS="--max-old-space-size=4096" node app.js
UV_THREADPOOL_SIZE=8 node app.js    # libuv thread pool
DEBUG=express:* node app.js         # the `debug` package convention
```

> **Gotcha — NODE_ENV must be exactly `production`.** Many libraries check `process.env.NODE_ENV === "production"` to disable expensive dev checks. Misspelling it costs real performance.

---

## VIII. WHEN NODE IS THE RIGHT TOOL — AND WHEN IT ISN'T

| Workload | Node? | Why |
|----------|-------|-----|
| HTTP / WebSocket APIs, real-time | ✅ Excellent | I/O-bound, async-first |
| BFFs, API gateways, SSR | ✅ Excellent | Same language as frontend |
| Streaming pipelines, proxying | ✅ Excellent | Streams + backpressure |
| CLI tools, scripts | ✅ Great | Fast startup, npm ecosystem |
| Microservices | ✅ Great | Lightweight, container-friendly |
| **CPU-heavy** (image/video, ML inference, big numerics) | ⚠️ With care | Use worker threads, native addons, or another runtime |
| Hard real-time / low-latency systems | ❌ No | GC pauses, JIT warm-up |
| Long-running batch number crunching | ❌ Often no | Use Python/Java/Go/Rust |

> **The rule of thumb:** Node thrives when most of the time is spent **waiting on I/O**. It struggles when most of the time is spent **doing math on the JS thread**.

---

## IX. A TINY HTTP SERVER — NO FRAMEWORKS

To prove Node's runtime story end-to-end, here is a working HTTP server with no dependencies:

```js
// server.js  —  run with: node server.js
import http from "node:http";

const server = http.createServer((req, res) => {
  // This callback runs on the SINGLE JS thread for every request.
  console.log(`${req.method} ${req.url} from pid=${process.pid}`);

  if (req.url === "/") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ hello: "world", uptime: process.uptime() }));
    return;
  }

  if (req.url === "/slow") {
    // Yield to the event loop — does NOT block the thread.
    setTimeout(() => {
      res.writeHead(200, { "content-type": "text/plain" });
      res.end("slow done\n");
    }, 1000);
    return;
  }

  res.writeHead(404);
  res.end("not found\n");
});

server.listen(3000, () => console.log("listening on http://localhost:3000"));

// Graceful shutdown sketch — full version in file 08.
process.on("SIGINT", () => server.close(() => process.exit(0)));
```

Try it: while `/slow` is pending, hit `/` from another terminal — it returns instantly. That is non-blocking I/O at work.

---

## X. THE EVENT LOOP IN ONE WORKED EXAMPLE

```js
// loop.js
import { readFile } from "node:fs";

console.log("A: top");

setTimeout(() => console.log("D: setTimeout"), 0);
setImmediate(() => console.log("E: setImmediate"));

readFile(__filename, () => {
  console.log("F: I/O callback");
  setTimeout(() => console.log("H: setTimeout in I/O"), 0);
  setImmediate(() => console.log("G: setImmediate in I/O"));  // wins
});

Promise.resolve().then(() => console.log("C: microtask"));
process.nextTick(() => console.log("B: nextTick"));

console.log("X: bottom");
```

Trace:

1. **Synchronous block runs to completion**: A, X.
2. After sync ends, **nextTick** queue drains: B.
3. **Microtask** queue drains: C.
4. Loop enters its phases — timers (D), check (E), then poll picks up the `readFile` completion: F.
5. Inside the I/O callback we schedule another timeout and immediate; the *check* phase comes immediately after I/O, so G prints before H.

If you can predict this output, you understand the loop well enough to debug almost anything in Node.

---

## XI. INSPECTING WHAT NODE IS DOING

```js
// loop-monitor.js — measure event-loop lag (a great health metric)
let last = process.hrtime.bigint();
setInterval(() => {
  const now = process.hrtime.bigint();
  const drift = Number(now - last) / 1e6 - 500;   // expected 500ms cadence
  if (drift > 50) console.warn("event loop lag:", drift.toFixed(0), "ms");
  last = now;
}, 500).unref();
```

In production, `clinic.js`, `0x` (flamegraphs), `--inspect`, and the built-in `node:diagnostics_channel` all help — file 08 covers monitoring.

---

## XII. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Doing CPU-heavy work on the JS thread | All requests slow / timeouts | Worker threads, cluster, or another runtime |
| `process.nextTick` recursion | Loop frozen, no I/O processed | Use `setImmediate` to yield |
| Relying on `setTimeout` vs `setImmediate` order | Flaky tests | Don't rely on it; use deterministic logic |
| Sync `fs.readFileSync` in a request handler | One slow disk read stalls the server | Use async / streams |
| Catching `uncaughtException` and continuing | Memory leaks, corrupted state | Log → flush → `process.exit(1)` |
| Misusing `NODE_ENV` (typos) | Production missing perf optimizations | Set exactly `production` |
| Default thread pool size too small | High-concurrency bcrypt/zlib stalls | `UV_THREADPOOL_SIZE` |
| Forgetting `unref()` on timers | Process won't exit | `.unref()` on long-lived timers |
| Hot-path object shape changes | Slow under load | Construct objects with stable shapes |
| Treating Node like Java threads | Race conditions where there are none | Remember: one JS thread |

---

## 🧠 KEY TAKEAWAYS

- Node = **V8** (executes JS, JIT, GC) + **libuv** (event loop, thread pool, async I/O) + Node bindings.
- One JS thread runs your code. **Microtasks (`nextTick`, Promises) run between phases**, so they always beat timers.
- The event loop has phases: **timers → pending → idle/prepare → poll → check → close**, with nextTick + microtasks drained between them.
- Non-blocking I/O is the superpower; **CPU-heavy sync work is the kryptonite**.
- `process` is your handle to the OS process; `globalThis` is the standard global; `__dirname` only exists in CJS — derive it from `import.meta.url` in ESM.
- Use `node --watch`, `--inspect`, `NODE_ENV=production`, and `UV_THREADPOOL_SIZE` deliberately.
- Pick Node for I/O-bound and real-time work; reach for another tool when the bottleneck is pure CPU.

---

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-Modules-And-NPM.md`](./02-Modules-And-NPM.md) · **Index:** [`00-Index.md`](./00-Index.md)
