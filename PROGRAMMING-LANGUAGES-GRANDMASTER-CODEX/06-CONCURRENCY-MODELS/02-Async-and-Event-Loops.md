# ⏳ Async and Event Loops

> *"One thread, thousands of conversations — as long as everyone yields while they wait."*

---

## I. THE PROBLEM ASYNC SOLVES

Most servers spend their time **waiting** — for the network, the disk, the database. A thread blocked on I/O is a thread doing nothing but consuming ~1 MB of stack and a scheduler slot. Handling 10,000 simultaneous connections with 10,000 threads is wasteful and hits OS limits (the "C10k problem").

**Asynchronous concurrency** flips this: instead of blocking a thread while waiting, a task **yields** control, letting the single thread serve other tasks, and **resumes** when its data is ready. One thread juggles thousands of in-flight operations. This is *concurrency without parallelism* — ideal for **I/O-bound** work.

---

## II. THE EVENT LOOP — THE ENGINE

At async's core is the **event loop**: a single thread running a loop that dispatches ready events and callbacks.

```
loop forever:
    run all ready tasks/callbacks until they yield or finish
    ask the OS: "any I/O completed?" (epoll/kqueue/IOCP)
    for each completed I/O: schedule its continuation
    if timers are due: schedule their callbacks
```

The key OS mechanism is **non-blocking I/O + readiness notification** (`epoll` on Linux, `kqueue` on BSD/macOS, IOCP on Windows). Instead of "read this socket (and block)," it's "tell me when this socket has data," letting one thread monitor thousands of sockets. JavaScript's runtime (libuv), Python's `asyncio`, and Nginx are all built on this.

### The critical rule: never block the loop
Because it's *one thread*, any blocking operation (a synchronous file read, a CPU-heavy loop, `sleep`) **freezes everything**. In async code you must use async I/O everywhere and offload CPU-heavy work to worker threads/processes. "Don't block the event loop" is the first commandment of async programming.

---

## III. CALLBACKS → PROMISES → ASYNC/AWAIT (the evolution)

### Callbacks — the beginning (and "callback hell")
```javascript
readFile('a', (err, a) => {
  readFile('b', (err, b) => {
    readFile('c', (err, c) => { /* nested pyramid of doom */ });
  });
});
```
Error handling and composition are painful; deeply nested callbacks become unreadable.

### Promises/Futures — a value that will exist later
```javascript
readFile('a').then(a => readFile('b')).then(b => ...).catch(handleError);
```
A **promise** represents a future result; you chain transformations. Flatter, composable, unified error handling. (A promise is a monad — see [`../02-PARADIGMS/03-Functional.md`](../02-PARADIGMS/03-Functional.md).)

### Async/await — sequential-looking async
```javascript
async function load() {
  try {
    const a = await readFile('a');   // suspend here; resume when ready
    const b = await readFile('b');
    return process(a, b);
  } catch (err) { handleError(err); }
}
```
`async/await` is **syntactic sugar over promises** that lets asynchronous code read like ordinary sequential code — with normal `try/catch`, loops, and control flow. It's the modern standard across JS, Python, Rust, C#, Swift.

---

## IV. HOW ASYNC/AWAIT ACTUALLY WORKS (the magic revealed)

The compiler transforms an `async` function into a **state machine (a coroutine)**. Each `await` is a **suspension point**: the function's local state is saved, control returns to the event loop, and when the awaited value is ready, execution *resumes* right after the `await`.

```
async function f() {          becomes a state machine:
  const a = await g();          STATE 0: call g(); save state; yield
  const b = await h(a);         STATE 1: (resumed) a is ready; call h(a); save; yield
  return a + b;                 STATE 2: (resumed) b is ready; return a+b; done
}
```

This is a **stackless coroutine**: the saved state lives on the heap (not an OS thread stack), which is why you can have millions of them cheaply. `await` is essentially "save my continuation and yield to the scheduler." Understanding this demystifies async: it's not threads, it's *cooperative suspension via compiler-generated state machines*.

---

## V. COOPERATIVE vs PREEMPTIVE (the fundamental difference)

- **Threads (preemptive)** — the OS can interrupt a task *anywhere*. Hence data races (updates interrupted mid-way).
- **Async (cooperative)** — a task runs until it *voluntarily* yields (at an `await`). Between awaits, it runs uninterrupted.

This cooperative nature is a huge safety win: within a single-threaded async runtime, you *cannot* have data races between awaits — nothing interrupts you until you yield. The downside: a task that never yields (blocks) starves everyone, and you must remember where the yield points (`await`) are, because state can change across them.

---

## VI. GREEN THREADS / GOROUTINES — ASYNC WITHOUT THE `await`

Some runtimes give you async's efficiency *without* explicit `async/await` by using **lightweight (green) threads** the *runtime* schedules onto a few OS threads:
- **Go's goroutines** — `go f()` spawns a goroutine; the Go runtime multiplexes millions of them onto OS threads and automatically yields at I/O and function calls. You write blocking-looking code; the runtime makes it async.
- **Java's virtual threads** (Project Loom, 2023) — the JVM now offers millions of cheap threads scheduled onto few OS threads.
- **Erlang processes** — the BEAM VM schedules lightweight processes preemptively.

These avoid the "function-color problem" (where `async` functions can only be called by other `async` functions, splitting your ecosystem in two). It's why Go concurrency feels so clean: `go` and channels, no `await` coloring your whole codebase.

---

## 📌 Key Takeaways
- Async solves **I/O-bound** concurrency: yield while waiting so one thread serves thousands of tasks (the C10k solution).
- The **event loop** + non-blocking I/O (`epoll`/`kqueue`/IOCP) is the engine; **never block it**.
- Callbacks → **promises** → **async/await** (sugar over promises) — sequential-looking async with normal control flow.
- `await` compiles to a **state-machine coroutine**: save state, yield to the scheduler, resume when ready — cheap because state lives on the heap, not a thread stack.
- Async is **cooperative** (yield only at await) → no data races between awaits, but a blocking task starves all.
- **Green threads/goroutines/virtual threads** deliver async efficiency without `await` coloring.

**Next:** [`03-Actors-CSP-and-STM.md`](./03-Actors-CSP-and-STM.md)
