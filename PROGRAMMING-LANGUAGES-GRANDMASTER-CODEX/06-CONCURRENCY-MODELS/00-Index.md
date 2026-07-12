# 🔀 Concurrency Models

> *"The free lunch is over. Clock speeds stopped rising; cores multiplied. Every language had to answer: how do I use them safely?"*

For decades, programs got faster because CPUs got faster. Around 2005 that ended — chips grew *more cores* instead of faster ones. Suddenly, using hardware well meant **concurrency**, and every language had to provide a model for it. This section covers the major models and, crucially, *how they actually work* under the hood.

---

## 📚 Contents

1. [`01-Threads-and-Shared-Memory.md`](./01-Threads-and-Shared-Memory.md) — OS threads, locks, atomics, memory models, and why shared state is hard
2. [`02-Async-and-Event-Loops.md`](./02-Async-and-Event-Loops.md) — Cooperative concurrency: event loops, coroutines, async/await internals
3. [`03-Actors-CSP-and-STM.md`](./03-Actors-CSP-and-STM.md) — Message-passing and transactional models that avoid shared state

---

## 🧭 The Core Tension

```
        SHARE MEMORY                       SHARE NOTHING
   (threads, locks, atomics)          (actors, CSP channels)
        │                                    │
   fast, direct, but                    safe, scalable, but
   races/deadlocks lurk                 copying/messaging cost
        │                                    │
   C, C++, Java                         Erlang, Go, Rust (safe by types)
```

Every model is an answer to one question: **how do independent tasks coordinate without corrupting shared state?** The models that "share nothing" (message-passing) have proven easier to get right at scale; the models that share memory are faster but demand extreme discipline.

---

## 📌 Key Takeaways
- Concurrency became essential when CPUs went multi-core (~2005).
- The central hazard is **shared mutable state** → data races, deadlocks, heisenbugs.
- Models split into **share-memory** (threads/locks) and **share-nothing** (actors/CSP); async is cooperative concurrency, often single-threaded.

**→ Start:** [`01-Threads-and-Shared-Memory.md`](./01-Threads-and-Shared-Memory.md) | Back to [`../README.md`](../README.md)
