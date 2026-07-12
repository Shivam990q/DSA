# 📬 Actors, CSP, and STM

> *"Don't communicate by sharing memory; share memory by communicating."* — the Go proverb

The most successful concurrency models attack the root cause of concurrency bugs: **shared mutable state**. Remove sharing, and races become impossible. Three approaches.

---

## I. THE ACTOR MODEL — SHARE NOTHING, MESSAGE EVERYTHING

An **actor** is an isolated unit with **private state** that no one else can touch. Actors communicate *only* by sending **asynchronous messages** to each other's mailboxes. In response to a message, an actor can:
1. update its own private state,
2. send messages to other actors,
3. create new actors.

```
   Actor A                Actor B
   ┌────────┐  message   ┌────────┐
   │ state  │ ─────────► │ mailbox│
   │(private)│           │ state  │
   └────────┘           └────────┘
   No shared memory. Ever. Only messages.
```

Because no state is shared, **there are no data races and no locks** — an actor processes its messages one at a time, serially. Concurrency emerges from many actors running independently.

**Erlang/Elixir** are the canonical actor languages (the BEAM VM). Their track record is legendary: telecom switches with **nine nines** (99.9999999%) uptime. The actor model also gives Erlang its famous fault tolerance:
- **"Let it crash"** — don't defensively code every error; let a faulty actor die.
- **Supervision trees** — supervisor actors watch worker actors and restart them on failure.

This isolation-plus-supervision is why actor systems power messaging (WhatsApp ran on Erlang with a tiny team), telecom, and distributed systems. Akka brings actors to the JVM.

---

## II. CSP — COMMUNICATING SEQUENTIAL PROCESSES (Go's model)

**CSP** (Tony Hoare, 1978) also shares nothing, but coordination happens through **channels** rather than actor mailboxes. Processes are anonymous; **channels** are the named, first-class thing they pass values through.

```go
ch := make(chan int)          // a typed channel
go func() { ch <- 42 }()      // one goroutine SENDS
value := <-ch                 // another RECEIVES (blocks until a value arrives)
```

Go's implementation:
- **Goroutines** — extremely cheap green threads (start with ~2 KB stacks; you can run millions).
- **Channels** — typed conduits; sends/receives synchronize the two goroutines (a rendezvous, unless buffered).
- **`select`** — wait on multiple channel operations at once (like a switch for communication).

The philosophy — *"share memory by communicating"* — means data is *passed* between goroutines over channels; at any moment, only one goroutine "has" it. This gives you CSP's safety with imperative-looking code. The difference from actors: CSP channels are decoupled from the processes (many can share a channel) and communication is often synchronous; actors own their mailbox and are asynchronous. Both eliminate shared mutable state.

---

## III. SOFTWARE TRANSACTIONAL MEMORY (STM)

A different idea: keep shared memory, but access it through **transactions** — like a database. You wrap operations in an atomic block; the runtime executes it optimistically, and if a conflict is detected, it **rolls back and retries**.

```haskell
atomically $ do            -- Haskell STM
  from <- readTVar accountA
  writeTVar accountA (from - 100)
  to <- readTVar accountB
  writeTVar accountB (to + 100)
-- either the WHOLE transfer commits atomically, or it retries. No partial state, no locks.
```

- ✅ **Composable** — unlike locks, you can combine two transactional operations into one atomic operation safely. (Composing two locked operations often deadlocks.)
- ✅ **No manual locks** — no lock ordering, no deadlock.
- ❌ **Retry cost** — high contention means many rollbacks/retries.
- ❌ **No side effects inside** — transactions must be retryable, so you can't do irreversible I/O mid-transaction.

STM shines in **Clojure** (refs) and **Haskell**, where immutability makes rollbacks clean. It's the most "optimistic" model: assume no conflict, detect and retry if wrong.

---

## IV. DATA PARALLELISM — A DIFFERENT AXIS

Distinct from the coordination models above: **data parallelism** applies the *same operation* across a large dataset in parallel, with no coordination needed because elements are independent.

```
map a function over a billion elements → split across cores/GPU → combine
```
Examples: GPU shaders, SIMD instructions, NumPy vectorized ops, MapReduce/Spark. This is the model for number-crunching (ML, graphics, scientific computing) — "embarrassingly parallel" work where tasks don't interact. It complements, rather than competes with, the coordination models.

---

## V. CHOOSING A MODEL — THE DECISION TABLE

| Your situation | Best model |
|----------------|-----------|
| I/O-bound (servers, network) | async/await or goroutines |
| Independent stateful entities (users, devices, games) | actors |
| Pipelines / staged processing | CSP channels (Go) |
| Fault tolerance / uptime critical | actors + supervision (Erlang) |
| Need shared data, want composability | STM |
| Number crunching on big data | data parallelism (GPU/SIMD/MapReduce) |
| Raw performance, full control | threads + locks (with great care) |
| Want the compiler to prevent races | Rust ownership + channels/async |

---

## VI. THE UNIFYING LESSON

Every robust concurrency model does one of two things:
1. **Eliminates shared mutable state** — actors (private state + messages), CSP (pass ownership via channels), functional immutability. *No sharing → no races.*
2. **Controls access to shared state** — locks (pessimistic), STM (optimistic), Rust's borrow checker (compile-time). *Sharing, but disciplined.*

The industry's hard-won wisdom leans toward #1: **the easiest concurrency bug to fix is the one you made impossible.** Message-passing and immutability scale to huge systems and huge teams because they remove the hazard rather than manage it. Reach for shared-memory-with-locks last, and when you do, let a language (Rust) or a transaction system (STM) carry the safety burden.

---

## 📌 Key Takeaways
- **Actors** (Erlang/Elixir/Akka): isolated private state + async messages; no races, plus "let it crash" + supervision → legendary uptime.
- **CSP** (Go): goroutines + typed **channels**; "share memory by communicating" — pass data, don't share it.
- **STM** (Clojure/Haskell): shared memory via retryable atomic **transactions** — composable, no manual locks, but retry cost.
- **Data parallelism** (GPU/SIMD/MapReduce): same op over independent data — for number crunching.
- Robust models either **eliminate** shared mutable state (preferred) or **discipline** access to it; make the bug impossible rather than manage it.

**Next:** [`../07-LANGUAGE-TOUR/00-Index.md`](../07-LANGUAGE-TOUR/00-Index.md)
