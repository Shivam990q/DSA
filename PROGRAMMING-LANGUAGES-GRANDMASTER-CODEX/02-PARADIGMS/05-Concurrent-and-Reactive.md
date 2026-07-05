# 🌊 Concurrent and Reactive Programming

> *"Concurrency is about structure — dealing with many things at once. Parallelism is about execution — doing many things at once."* — after Rob Pike

---

## I. CONCURRENCY vs PARALLELISM (the distinction everyone confuses)

- **Concurrency** — *structuring* a program as multiple independent tasks that can make progress independently. It's a way of *designing*. A single-core machine can be concurrent (interleaving tasks).
- **Parallelism** — *actually executing* multiple computations simultaneously, requiring multiple cores/machines.

Concurrency enables parallelism but isn't the same thing. A web server handling 10,000 connections is *concurrent* (10,000 logical tasks) and may be *parallel* (running on 8 cores). You can have concurrency without parallelism (async on one thread) and parallelism without much concurrency (a parallel matrix multiply).

The **concurrent paradigm** is about how a language lets you *express* independent tasks and coordinate them safely.

---

## II. THE FUNDAMENTAL CHALLENGE: SHARED MUTABLE STATE

The moment two tasks touch the same mutable data, you get **races**:

```
Thread A: read balance (100) → add 50 → write 150
Thread B: read balance (100) → add 30 → write 130   ← A's update LOST
```

The result depends on timing — a **data race**, the most insidious class of bug (nondeterministic, hard to reproduce). Every concurrency model is, at heart, a different **strategy for avoiding or taming shared mutable state**. (Deep dive: [`../06-CONCURRENCY-MODELS/00-Index.md`](../06-CONCURRENCY-MODELS/00-Index.md).)

---

## III. THE MAJOR CONCURRENCY MODELS

| Model | Idea | Exemplars |
|-------|------|-----------|
| **Threads + locks** | shared memory, protect it with mutexes | C, C++, Java |
| **Async / await** | cooperative tasks on an event loop; no OS threads per task | JavaScript, Python, Rust, C# |
| **Communicating Sequential Processes (CSP)** | tasks share *nothing*; communicate over channels | Go (goroutines + channels) |
| **Actors** | isolated actors with private state; exchange messages | Erlang/Elixir, Akka |
| **Software Transactional Memory (STM)** | memory transactions that commit atomically or retry | Haskell, Clojure |
| **Data parallelism** | apply one operation across a big dataset in parallel | GPU shaders, NumPy, map-reduce |

**The winning philosophies** avoid shared mutable state entirely:
- **Go's motto:** *"Don't communicate by sharing memory; share memory by communicating."* Pass data over channels; only one goroutine owns it at a time.
- **Erlang's motto:** *"Share nothing."* Actors have private state and only send messages. This is why Erlang powers telecom systems with 99.9999999% uptime.

---

## IV. REACTIVE PROGRAMMING — PROGRAMMING WITH STREAMS

**Reactive programming** models a program as **flows of data (streams) and the automatic propagation of change**. Instead of pulling values, you declare *how outputs react to inputs*, and the runtime pushes updates through the graph as data arrives.

```javascript
// RxJS: a stream of click events → throttled → mapped → subscribed
fromEvent(button, 'click')
  .pipe(
    throttleTime(1000),         // at most one per second
    map(e => e.clientX)         // transform each event
  )
  .subscribe(x => console.log(x));   // react to each result
```

The core idea, borrowed from spreadsheets: `C1 = A1 + B1`. Change `A1` and `C1` **updates automatically** — you declared the *relationship*, and the system propagates changes. Reactive programming brings that to event streams: user input, network responses, sensor data, WebSocket messages.

Key concepts:
- **Observable** — a stream of values over time (0, 1, or infinitely many).
- **Operators** — declarative transforms on streams (`map`, `filter`, `merge`, `debounce`).
- **Subscription** — reacting to emitted values.
- **Backpressure** — handling a fast producer feeding a slow consumer.

Reactive shines for **UIs** (events are streams), **real-time data** (prices, telemetry), and **event-driven systems**. React's "UI = f(state)" and frameworks like RxJS, Svelte's reactivity, and Elm's architecture are all reactive at heart.

---

## V. THE ASYNC REVOLUTION

`async/await` deserves special mention because it's now everywhere. It lets you write concurrent code that *looks* sequential:

```javascript
async function loadUser(id) {
  const user = await fetch(`/users/${id}`);   // yields while waiting; doesn't block
  const posts = await fetch(`/users/${id}/posts`);
  return { user, posts };
}
```

`await` **suspends** the function (freeing the thread to do other work) and **resumes** it when the awaited result is ready. One thread juggles thousands of in-flight operations. This is *concurrency without parallelism* — perfect for I/O-bound work (servers, network calls) where the bottleneck is waiting, not computing. (How it works internally — continuations and state machines — is in [`../06-CONCURRENCY-MODELS/02-Async-and-Event-Loops.md`](../06-CONCURRENCY-MODELS/02-Async-and-Event-Loops.md).)

---

## VI. THE MENTAL MODEL FOR PICKING ONE

- **I/O-bound** (waiting on network/disk) → **async/await** or an event loop. One thread, thousands of tasks.
- **CPU-bound** (heavy computation) → **parallelism** across threads/cores/GPU.
- **Independent stateful entities** (chat users, game actors, devices) → **actors**.
- **Pipelines of stages** → **CSP / channels** (Go).
- **UIs and event streams** → **reactive**.
- **Shared data you must mutate** → threads + locks (last resort — hardest to get right).

The overarching wisdom: **avoid shared mutable state.** Immutability (functional), message-passing (actors/CSP), and ownership (Rust) all attack the root cause. Locks manage the symptom.

---

## 📌 Key Takeaways
- **Concurrency** = structure (many tasks); **parallelism** = execution (many at once). Different things.
- Every model is a strategy against **shared mutable state**, the source of data races.
- Models: threads+locks, async/await, CSP (Go channels), actors (Erlang), STM, data parallelism.
- **Reactive programming** = streams + automatic change propagation (spreadsheets for events); great for UIs and real-time data.
- Pick by workload: async for I/O, parallelism for CPU, actors for stateful entities, reactive for event streams.

**Next:** [`../03-TYPE-SYSTEMS/00-Index.md`](../03-TYPE-SYSTEMS/00-Index.md)
