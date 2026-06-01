# ⏳ Asynchronous JavaScript

> *"JavaScript is single-threaded. The magic is how it does many things while only ever doing one thing at a time."*

This is the file that turns you from someone who copies `async/await` snippets into someone who *understands* them. We'll build up from callbacks → promises ⭐ → async/await ⭐, then peel back the curtain on the **event loop**, microtasks, and macrotasks — the engine that makes non-blocking JavaScript possible.

---

## I. WHY ASYNC EXISTS

JavaScript runs on a **single thread**: one call stack, one operation at a time. If everything were synchronous, a 2-second network request would *freeze the entire page* — no clicks, no scrolling, nothing — for 2 seconds.

```js
// Imagine this were synchronous (it isn't, thankfully):
const data = downloadHugeFile();  // ⛔ page frozen for 5 seconds
render(data);
```

Async lets you *start* a slow operation and keep running other code; when the slow thing finishes, its handler runs. The slow work (network, disk, timers) happens **outside** the JS thread — handled by the browser or Node — and the result is queued back when ready.

---

## II. CALLBACKS — THE ORIGINAL ASYNC

A **callback** is a function you pass to be called *later*, when an operation completes.

```js
console.log("1. start");

setTimeout(() => {
  console.log("3. this runs later");  // queued, runs after the stack clears
}, 1000);

console.log("2. end");

// Output: 1. start → 2. end → 3. this runs later
```

### Callback hell (the pyramid of doom)
When async steps depend on each other, callbacks nest deeper and deeper:

```js
getUser(1, (user) => {
  getPosts(user.id, (posts) => {
    getComments(posts[0].id, (comments) => {
      getAuthor(comments[0].authorId, (author) => {
        console.log(author.name);
        // ...four levels deep, error handling duplicated everywhere 😱
      }, handleError);
    }, handleError);
  }, handleError);
}, handleError);
```
This is hard to read, hard to error-handle, and easy to get wrong. Promises were invented to fix exactly this.

---

## III. PROMISES ⭐

A **Promise** is an object representing a value that may not exist yet — the eventual result of an async operation. It's a placeholder that will eventually **settle** into one of two states.

```
        ┌──────────┐
        │ pending  │  (initial — not done yet)
        └────┬─────┘
       resolve│  │reject
         ┌────▼  ▼────┐
     ┌───┴───┐    ┌───┴────┐
     │fulfilled│   │ rejected│
     │(success)│   │ (error) │
     └─────────┘   └─────────┘
   (once settled, never changes again)
```

### Creating a promise
```js
const promise = new Promise((resolve, reject) => {
  // do async work, then call resolve(value) or reject(error)
  const success = true;
  setTimeout(() => {
    if (success) resolve("✅ data");
    else reject(new Error("❌ failed"));
  }, 1000);
});
```

### Consuming a promise: `.then` / `.catch` / `.finally`
```js
promise
  .then(value => console.log("got:", value))   // runs on fulfill
  .catch(error => console.error("err:", error)) // runs on reject (or any throw above)
  .finally(() => console.log("done"));          // always runs, settled either way
```

### Chaining — the flat alternative to callback hell
Each `.then` returns a **new promise**, so you can chain. Returning a value passes it along; returning a promise waits for it.

```js
getUser(1)
  .then(user => getPosts(user.id))       // return a promise → next .then waits
  .then(posts => getComments(posts[0].id))
  .then(comments => getAuthor(comments[0].authorId))
  .then(author => console.log(author.name))
  .catch(handleError);                   // ONE catch handles errors from ANY step
```
Compare this flat chain to the callback pyramid above — same logic, dramatically more readable, and a single error handler.

### A key chaining rule: return, don't nest
```js
// ❌ nesting defeats the purpose
getUser(1).then(user => {
  getPosts(user.id).then(posts => { /* nested again */ });
});

// ✅ return to keep it flat
getUser(1)
  .then(user => getPosts(user.id))   // RETURN the promise
  .then(posts => { /* ... */ });
```

### Combinator methods (running multiple promises)
```js
const p1 = Promise.resolve(1);
const p2 = Promise.resolve(2);
const p3 = Promise.resolve(3);

// all — wait for ALL; rejects if ANY rejects
Promise.all([p1, p2, p3]).then(results => console.log(results)); // [1, 2, 3]

// allSettled — wait for all, never rejects; reports each outcome
Promise.allSettled([Promise.resolve(1), Promise.reject("x")])
  .then(r => console.log(r));
// [{status:"fulfilled",value:1}, {status:"rejected",reason:"x"}]

// race — settles as soon as the FIRST one settles (fulfill OR reject)
Promise.race([slow, fast]).then(winner => console.log(winner));

// any — first to FULFILL wins; rejects only if all reject
Promise.any([Promise.reject("a"), Promise.resolve("b")]).then(v => console.log(v)); // "b"
```
> Use `Promise.all` to parallelize independent requests (much faster than awaiting them one by one). Use `allSettled` when you want every result even if some fail.

---

## IV. ASYNC / AWAIT ⭐

`async/await` is syntactic sugar over promises that lets you write asynchronous code that *reads* like synchronous code. It's the modern default.

```js
// An async function ALWAYS returns a promise
async function getName() {
  return "Ada";          // wrapped → Promise.resolve("Ada")
}
getName().then(n => console.log(n)); // "Ada"

// `await` pauses the function until the promise settles, then unwraps the value
async function loadUser() {
  const user = await getUser(1);          // waits, then user = resolved value
  const posts = await getPosts(user.id);  // waits again
  return posts;
}
```

### The same chain, three ways — see the evolution
```js
// Promises (.then)
function loadData() {
  return getUser(1)
    .then(user => getPosts(user.id))
    .then(posts => getComments(posts[0].id))
    .then(comments => comments[0]);
}

// async/await — reads top to bottom like sync code
async function loadData() {
  const user = await getUser(1);
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  return comments[0];
}
```

### Error handling with try/catch
```js
async function loadData() {
  try {
    const user = await getUser(1);
    const posts = await getPosts(user.id);
    return posts;
  } catch (error) {
    console.error("Something failed:", error.message); // catches ANY await above
    return [];                                          // graceful fallback
  } finally {
    console.log("cleanup");                             // always runs
  }
}
```

### ⚠️ Parallel vs sequential `await` (a real performance bug)
```js
// ❌ SLOW — sequential: 3 seconds total (1s + 1s + 1s)
async function slow() {
  const a = await fetchA();  // wait 1s
  const b = await fetchB();  // THEN wait 1s
  const c = await fetchC();  // THEN wait 1s
  return [a, b, c];
}

// ✅ FAST — parallel: ~1 second total (all start at once)
async function fast() {
  const [a, b, c] = await Promise.all([fetchA(), fetchB(), fetchC()]);
  return [a, b, c];
}
```
If the requests don't depend on each other, **start them together** with `Promise.all`. Awaiting in sequence when you don't need to is one of the most common real-world performance mistakes.

### `await` in loops
```js
// Sequential (sometimes what you want — e.g., rate-limited API)
for (const id of ids) {
  const data = await fetchById(id);  // one at a time
  process(data);
}

// Parallel (faster when order/limits don't matter)
const results = await Promise.all(ids.map(id => fetchById(id)));
```

---

## V. THE EVENT LOOP — HOW IT ALL WORKS ⭐

This is the mechanism behind everything above. Here are the moving parts:

```
   ┌─────────────────────────────┐
   │        CALL STACK           │  ← runs ONE thing at a time (synchronous)
   └─────────────┬───────────────┘
                 │ when an async API is called (setTimeout, fetch...)
                 ▼
   ┌─────────────────────────────┐
   │   Web APIs / Node APIs      │  ← timers, network, I/O run HERE (off-thread)
   └─────────────┬───────────────┘
                 │ when finished, the callback is queued
                 ▼
   ┌──────────────────┐  ┌──────────────────────┐
   │  MICROTASK QUEUE │  │   MACROTASK QUEUE     │
   │  (promises,      │  │   (setTimeout, I/O,   │
   │   queueMicrotask)│  │    setInterval)       │
   └────────┬─────────┘  └──────────┬────────────┘
            │                       │
            └────────►  EVENT LOOP  ◄┘
   The loop: when the call stack is empty, drain ALL microtasks,
   then take ONE macrotask, run it, drain ALL microtasks again, repeat.
```

### The critical rule
> When the call stack empties, the event loop **drains the entire microtask queue** before taking the **next single macrotask**. Microtasks (promises) always jump ahead of macrotasks (timers).

### The classic ordering puzzle
```js
console.log("1: sync");

setTimeout(() => console.log("2: setTimeout (macrotask)"), 0);

Promise.resolve().then(() => console.log("3: promise (microtask)"));

console.log("4: sync");

// OUTPUT:
// 1: sync
// 4: sync
// 3: promise (microtask)    ← microtasks run before timers, even with delay 0
// 2: setTimeout (macrotask)
```
Why? All synchronous code runs first (`1`, `4`). Then the stack is empty, so the loop drains microtasks (`3`). Only then does it pick up a macrotask (`2`). **A `setTimeout(fn, 0)` does not run "immediately" — it runs after all current sync code and all pending microtasks.**

### A harder one
```js
console.log("A");
setTimeout(() => console.log("B"), 0);
Promise.resolve()
  .then(() => console.log("C"))
  .then(() => console.log("D"));
console.log("E");

// A, E, C, D, B
// Sync: A, E. Microtasks drain fully: C, then D (chained). Then macrotask: B.
```

> **Takeaways:** `await x` is sugar for "schedule the rest of this function as a microtask once `x` settles." That's why promise continuations beat `setTimeout` callbacks. Long synchronous code blocks *everything* (the stack never empties) — keep heavy work off the main thread (Web Workers) or chunk it.

---

## VI. `fetch` — REAL-WORLD ASYNC

`fetch` is the built-in API for HTTP requests. It returns a promise.

```js
// Basic GET with async/await
async function getUser(id) {
  const response = await fetch(`https://api.example.com/users/${id}`);

  // ⚠️ fetch only rejects on NETWORK failure, NOT on HTTP errors (404/500)!
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }

  const data = await response.json();  // .json() also returns a promise
  return data;
}

getUser(1)
  .then(user => console.log(user))
  .catch(err => console.error("Failed:", err.message));
```

### POST with a JSON body
```js
async function createUser(user) {
  const response = await fetch("https://api.example.com/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

await createUser({ name: "Ada", role: "admin" });
```

### Timeouts and cancellation with AbortController
```js
async function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    const res = await fetch(url, { signal: controller.signal });
    return await res.json();
  } finally {
    clearTimeout(timer);   // clean up the timer either way
  }
}
```

### A robust real-world wrapper
```js
async function apiGet(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return { data: await res.json(), error: null };
  } catch (err) {
    return { data: null, error: err.message };  // never throws to the caller
  }
}

const { data, error } = await apiGet("/api/users");
if (error) showToast(error);
else render(data);
```

---

## VII. COMMON PITFALLS & GOTCHAS

**1. Forgetting `fetch` doesn't reject on 404/500**
```js
const res = await fetch(url);   // resolves even for a 500!
if (!res.ok) throw new Error(res.status); // you MUST check res.ok
```

**2. Forgetting to `await` (silent bug)**
```js
async function f() {
  const data = getUser(1);     // ❌ data is a Promise, not the user
  console.log(data.name);      // undefined
  const real = await getUser(1); // ✅
}
```

**3. Sequential awaits that should be parallel** — covered above; use `Promise.all`.

**4. Unhandled promise rejections**
```js
somePromise();                 // ❌ no .catch → unhandled rejection warning/crash
somePromise().catch(handle);   // ✅ always handle, or wrap awaits in try/catch
```

**5. Mixing `async/await` with `.then` confusingly** — pick one style per function.

**6. Thinking `setTimeout(fn, 0)` runs immediately** — it's a macrotask; all microtasks (and sync code) run first.

**7. `forEach` doesn't await**
```js
[1, 2, 3].forEach(async id => { await save(id); }); // ❌ doesn't wait — fire and forget
for (const id of [1, 2, 3]) { await save(id); }      // ✅ awaits each
await Promise.all([1, 2, 3].map(save));              // ✅ parallel + awaited
```

---

## VIII. KEY TAKEAWAYS

- JavaScript is **single-threaded**; async work (timers, network, I/O) runs **outside** the JS thread and its callbacks are queued back.
- **Callbacks** were first but lead to "callback hell"; **promises** flatten nested async into chains with one error handler.
- A **Promise ⭐** is pending → fulfilled or rejected, and once settled never changes. Consume with `.then`/`.catch`/`.finally`; combine with `Promise.all` (parallel), `allSettled`, `race`, `any`.
- **`async/await` ⭐** is sugar over promises: an `async` function returns a promise, `await` unwraps one, and `try/catch` handles errors. It reads like sync code.
- **Parallelize independent work** with `Promise.all` — sequential `await` is a common, costly mistake.
- The **event loop** drains *all* microtasks (promises) before each *single* macrotask (`setTimeout`). `setTimeout(fn, 0)` runs after current sync code and all pending microtasks.
- **`fetch`** returns a promise and only rejects on network failure — always check `response.ok` for HTTP errors, and `await response.json()` to get the body.

---

**← Prev:** [`04-The-This-Keyword-And-Prototypes.md`](./04-The-This-Keyword-And-Prototypes.md) | **→ Next:** [`06-ES6-Plus-Features.md`](./06-ES6-Plus-Features.md) | **Index:** [`00-Index.md`](./00-Index.md)
