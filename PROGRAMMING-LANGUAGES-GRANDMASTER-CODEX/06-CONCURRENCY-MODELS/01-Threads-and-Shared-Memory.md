# 🧵 Threads and Shared Memory

> *"Shared mutable state and concurrency: pick at most one, or bring extraordinary discipline."*

---

## I. WHAT A THREAD IS

A **thread** is an independent sequence of execution within a process. All threads in a process **share the same heap and globals** but each has its **own stack** and registers. The OS scheduler multiplexes threads onto CPU cores, switching between them (a **context switch**).

```
   PROCESS
   ┌───────────────────────────────────┐
   │  Shared: heap, globals, code       │
   │  ┌────────┐ ┌────────┐ ┌────────┐  │
   │  │Thread 1│ │Thread 2│ │Thread 3│  │  ← each has its own stack + registers
   │  │ stack  │ │ stack  │ │ stack  │  │
   │  └────────┘ └────────┘ └────────┘  │
   └───────────────────────────────────┘
```

Threads are *preemptive* — the OS can pause any thread between (almost) any two instructions. This is the source of both their power and their danger: shared data can be interrupted mid-update.

---

## II. THE DATA RACE — THE ORIGINAL SIN

```
Two threads run:  balance += 100   (which is really: read, add, write)

Thread A: read balance = 100
Thread B: read balance = 100        ← reads before A writes!
Thread A: write 200
Thread B: write 200                 ← should be 300; A's update is LOST
```

`balance += 100` is **not atomic** — it's three steps, and a context switch between them corrupts the result. This is a **data race**: concurrent access to shared mutable data where at least one access is a write, without synchronization. Data races are:
- **Nondeterministic** — depend on scheduling timing; may work 999 times and fail once.
- **Heisenbugs** — adding a print or a debugger changes timing and hides the bug.
- **Catastrophic** — corrupted data, crashes, security holes.

---

## III. SYNCHRONIZATION PRIMITIVES

To tame shared state, languages provide primitives:

### Mutex (mutual exclusion lock)
Only one thread holds the lock at a time; others wait. The critical section is serialized.
```java
lock.lock();
try { balance += 100; }   // only one thread here at a time
finally { lock.unlock(); }
```

### Other primitives
- **Semaphore** — allow up to N threads (a counting lock).
- **Read-write lock** — many readers OR one writer (readers don't conflict).
- **Condition variable** — wait until some condition holds (e.g., queue non-empty).
- **Atomic operations** — hardware-level indivisible ops (`compare-and-swap`, atomic increment) — lock-free for simple cases.
- **Barrier** — all threads wait until everyone reaches a point.

---

## IV. THE NEW HAZARDS LOCKS INTRODUCE

Locks fix races but create their own disasters:

### Deadlock
Two threads each hold a lock the other needs → both wait forever.
```
Thread A: holds Lock1, wants Lock2
Thread B: holds Lock2, wants Lock1   ← frozen forever
```
The four Coffman conditions for deadlock: mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one to prevent it (e.g., **always acquire locks in a global order** to kill circular wait).

### Other lock pathologies
- **Livelock** — threads keep reacting to each other and make no progress (like two people stepping aside in a hallway forever).
- **Starvation** — a thread never gets the lock because others keep grabbing it.
- **Priority inversion** — a low-priority thread holds a lock a high-priority thread needs (famously nearly doomed the Mars Pathfinder).
- **Convoying / contention** — many threads queuing on one hot lock destroys the parallelism you wanted.

Correct lock-based concurrency is genuinely hard — which is why the field moved toward models that avoid shared mutable state entirely.

---

## V. THE MEMORY MODEL — THE DEEPEST RABBIT HOLE

Here's the horror most programmers never learn: **modern CPUs and compilers reorder memory operations** for speed. Without synchronization, one thread may see another's writes *out of order* — or not at all (cached in a register).

```
Initial: x = 0, ready = 0

Thread A:  x = 42;  ready = 1;
Thread B:  while (ready == 0) {}  print(x);   // might print 0!
```
You'd expect `42`, but the CPU/compiler may reorder A's two writes, or B may see `ready=1` before `x=42` is visible. A **memory model** defines the rules for what a thread is guaranteed to observe. **Memory barriers/fences** and properly-used atomics (with acquire/release semantics) enforce ordering. Java's `volatile`, C++'s `std::atomic` with memory orderings, and the Java/C++ memory models exist precisely to make this tractable. This is why "just add `volatile`" folklore exists — and why getting lock-free code right is expert-only work.

---

## VI. THE GIL — A PRAGMATIC SHORTCUT

CPython and (historically) Ruby use a **Global Interpreter Lock**: only one thread executes bytecode at a time. This trivially prevents races in the interpreter's own data structures and makes single-threaded code simple and fast — but it means **threads can't run Python bytecode in parallel** (no CPU-bound speedup from threads). Python threads still help for I/O-bound work (a thread releases the GIL while waiting on I/O), but for CPU parallelism you need multiprocessing or native extensions. (Python 3.13+ is introducing an optional GIL-free build — a major ongoing change.)

---

## VII. THE VERDICT

Threads + shared memory are the **most powerful and most dangerous** concurrency model: maximum control and performance, but you must manually prevent races, deadlocks, and reordering bugs — and the failures are nondeterministic and brutal to debug. Use them when you need raw parallel performance and can afford the rigor. Otherwise, prefer models that don't share mutable state (async, actors, CSP — next files) or a language that checks safety for you (Rust's ownership makes data races a *compile error*).

---

## 📌 Key Takeaways
- Threads share the heap but have separate stacks; the OS preempts them anytime → shared updates can be interrupted.
- A **data race** (unsynchronized concurrent access, one a write) is nondeterministic and catastrophic.
- **Mutexes/semaphores/atomics** synchronize access but introduce **deadlock, livelock, starvation, priority inversion, contention**.
- **Memory models** exist because CPUs/compilers reorder memory ops; barriers/atomics enforce visibility and ordering.
- The **GIL** trades parallelism for simplicity in CPython/Ruby.
- Most powerful, most dangerous model — prefer share-nothing models or Rust's compile-time race prevention when you can.

**Next:** [`02-Async-and-Event-Loops.md`](./02-Async-and-Event-Loops.md)
