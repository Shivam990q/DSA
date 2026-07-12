# ♻️ Garbage Collection

> *"Let the machine track what's still reachable and reclaim the rest — so humans stop leaking memory and freeing it twice."*

---

## I. THE PROBLEM GC SOLVES

Manual memory management (`malloc`/`free`) is error-prone: forget to free → leak; free too early → use-after-free; free twice → corruption. **Garbage collection (GC)** automates deallocation: the runtime figures out which heap objects are no longer reachable and reclaims them, so the programmer never calls `free`.

The core question a GC answers: **"Is this object still reachable from the running program?"** If nothing can reach it, it's garbage, and its memory can be reclaimed.

---

## II. STRATEGY 1 — REFERENCE COUNTING

Each object keeps a count of how many references point to it. When the count hits zero, free it immediately.

```
a = obj      # obj.refcount = 1
b = obj      # obj.refcount = 2
b = None     # obj.refcount = 1
a = None     # obj.refcount = 0 → freed instantly
```

**Used by:** CPython (primary), Swift (ARC), C++ `shared_ptr`, Objective-C.

- ✅ **Immediate reclamation** — memory freed the instant it's unreachable; predictable; no big pauses.
- ✅ **Simple** and incremental.
- ❌ **Cycle problem** — if A points to B and B points to A, but nothing else points to either, their counts never reach zero → leaked. (Python bolts on a separate cycle collector to fix this.)
- ❌ **Overhead** — every reference assignment updates counts (costly, and thread-safety needs atomic ops).

---

## III. STRATEGY 2 — TRACING GC (MARK & SWEEP)

Periodically, start from the **roots** (global variables, stack variables, registers) and traverse every reachable object. Anything not reached is garbage.

```
1. MARK:   from roots, follow every reference, marking reachable objects.
2. SWEEP:  scan the heap; free everything unmarked.
```

**Used by:** the JVM, Go, JavaScript (V8), C#/.NET, most modern runtimes.

- ✅ **Handles cycles naturally** — unreachable cycles simply never get marked.
- ✅ **No per-assignment overhead** — cost is paid in batches during collection.
- ❌ **Pauses** — classic "stop-the-world": the program halts during collection. Bad for latency-sensitive apps (games, trading, real-time).
- ❌ **Unpredictable timing** — you don't control *when* a collection happens.

### Mark-Compact and Copying
Variants also **move** live objects together to eliminate fragmentation:
- **Mark-compact** — after marking, slide live objects to one end; the rest is one big free block.
- **Copying (semispace)** — copy live objects to a fresh region; abandon the old one wholesale. Fast allocation (just bump a pointer), but uses 2× memory.

---

## IV. THE KEY INSIGHT — GENERATIONAL GC

Decades of measurement revealed the **generational hypothesis**:

> *"Most objects die young."*

A request handler allocates thousands of temporary objects that become garbage almost immediately; a few objects (caches, connections) live for the whole program. So: split the heap by age.

```
YOUNG generation (nursery)   ← new objects; collected FREQUENTLY and cheaply
OLD generation (tenured)     ← survivors; collected RARELY
```

- Collect the young generation often — it's small and mostly garbage, so collection is fast and reclaims a lot.
- Promote survivors to the old generation; collect it infrequently.

This makes GC dramatically cheaper in practice, because you spend effort where the garbage actually is. The JVM, .NET, and V8 are all generational. It's the single most important GC optimization.

---

## V. MODERN GC — MINIMIZING PAUSES

The frontier is **low-latency, concurrent, and parallel** collectors that shrink or eliminate stop-the-world pauses by working *alongside* the running program:
- **Concurrent** — the collector runs at the same time as the app (mark while the app mutates, carefully tracking changes).
- **Parallel** — multiple GC threads collect at once.
- **Incremental** — collect in small slices instead of one big pause.

Examples: the JVM's **G1**, **ZGC**, and **Shenandoah** achieve sub-millisecond pauses even on huge heaps. Go's collector targets very low pause times by design. These are engineering marvels — but they trade throughput and complexity for latency.

---

## VI. THE FUNDAMENTAL GC TRADEOFF

GC juggles three goals you can't all maximize:

```
        THROUGHPUT
        (total work done)
           /    \
          /      \
   LATENCY ────── MEMORY
   (pause times)  (footprint)
```

- Want low latency? → more frequent, concurrent work → lower throughput, more CPU.
- Want high throughput? → collect in big batches → longer pauses.
- Want low memory? → collect more often → more CPU cost.

Every GC is a tuning of these dials. This is also **why GC languages struggle in hard real-time and tight-memory embedded contexts** — you can't afford unpredictable pauses in a pacemaker or an engine controller. That niche is exactly where manual management (C) and ownership (Rust) win.

---

## VII. GC vs THE ALTERNATIVES

| | GC (Java, Go, Python) | Manual (C) | Ownership (Rust) |
|---|---|---|---|
| Safety | ✅ safe | ❌ dangerous | ✅ safe |
| Pauses | ⚠️ yes | ✅ none | ✅ none |
| Predictability | ⚠️ lower | ✅ full | ✅ full |
| Ease | ✅ easy | ❌ hard | ⚠️ learning curve |
| Runtime cost | overhead + pauses | none | none |

GC trades a bit of performance and predictability for enormous gains in safety and productivity — the right call for the vast majority of software. Where you *can't* afford its costs, ownership (next file) offers safety *without* the GC.

---

## 📌 Key Takeaways
- GC automates deallocation by determining **reachability**; the programmer never calls `free`.
- **Reference counting** frees immediately but leaks cycles and taxes every assignment (CPython, Swift, `shared_ptr`).
- **Tracing (mark & sweep)** handles cycles and avoids per-assignment cost but causes stop-the-world **pauses** (JVM, Go, V8).
- **Generational GC** exploits "most objects die young" — the key optimization.
- Modern collectors (G1/ZGC/Shenandoah) minimize pauses concurrently; GC balances **throughput vs latency vs memory** and struggles in real-time/embedded niches.

**Next:** [`03-Ownership-and-Borrowing.md`](./03-Ownership-and-Borrowing.md)
