# 🗄️ Stack, Heap, and Memory Layout

> *"Two regions of memory, two philosophies: the stack is a disciplined soldier, the heap is a sprawling city."*

---

## I. THE PROCESS MEMORY MAP

When a program runs, the OS gives it a virtual address space, laid out (roughly) like this:

```
  high addresses
  ┌─────────────────┐
  │   STACK         │  ← grows DOWN; local variables, call frames, return addresses
  │      ↓          │
  │                 │
  │      ↑          │
  │   HEAP          │  ← grows UP; dynamically allocated data (malloc/new)
  ├─────────────────┤
  │   BSS / DATA    │  ← global & static variables
  ├─────────────────┤
  │   TEXT (code)   │  ← the compiled machine instructions (read-only)
  └─────────────────┘
  low addresses
```

The two regions you actively manage — the **stack** and the **heap** — have opposite characteristics.

---

## II. THE STACK — FAST, AUTOMATIC, SCOPED

The **call stack** stores a **frame** for each active function call. A frame holds the function's parameters, local variables, and bookkeeping (return address, saved registers).

```c
void foo() {
    int x = 5;        // x lives in foo's stack frame
    int arr[3];       // fixed-size array, also on the stack
}   // frame is POPPED here — x and arr vanish instantly, for free
```

Characteristics:
- **Allocation is trivial** — just move the stack pointer. One instruction. Blazing fast.
- **Deallocation is automatic** — when a function returns, its whole frame is discarded at once. No cleanup work.
- **LIFO discipline** — last in, first out; frames nest exactly like calls.
- **Small and fixed** — typically 1–8 MB. Size must be known at compile time. Deep recursion or huge local arrays → **stack overflow**.

The stack is why local variables are "free" and why recursion depth is limited.

---

## III. THE HEAP — FLEXIBLE, MANUAL, SLOWER

The **heap** is for data whose size or lifetime isn't known at compile time — data that must **outlive the function that created it** or is too big for the stack.

```c
int* make_array(int n) {
    int* arr = malloc(n * sizeof(int));   // heap: size known only at runtime
    return arr;   // arr survives after this function returns — impossible on the stack
}
```

Characteristics:
- **Flexible** — any size, any lifetime.
- **Slower allocation** — the allocator must *search* for a free block, track metadata, handle fragmentation.
- **Manual lifetime** — someone must free it (you in C, the GC in Java, the compiler in Rust). This is where all the danger lives.
- **Fragmentation** — after many allocs/frees, free space is scattered, wasting memory.

**Rule of thumb:** stack for small, short-lived, fixed-size values; heap for large, long-lived, or dynamically-sized data.

---

## IV. VALUES vs REFERENCES (revisited at the memory level)

The stack/heap split explains the value-vs-reference behavior from [`../01-LANGUAGE-FOUNDATIONS/04-Values-Bindings-and-Scope.md`](../01-LANGUAGE-FOUNDATIONS/04-Values-Bindings-and-Scope.md):

```
Python:  a = [1,2,3]
         ┌──────────────┐        ┌──────────────────┐
STACK    │ a → (pointer)│──────► │ HEAP: [1,2,3]     │
         └──────────────┘        └──────────────────┘
         b = a
         ┌──────────────┐              ▲
         │ b → (pointer)│──────────────┘  (b points at the SAME heap object)
         └──────────────┘
```

`b = a` copies the *pointer on the stack*, not the *list on the heap* — which is why mutating through `b` affects `a`. In C, a plain `struct` assignment copies the whole value; a pointer assignment copies just the address. Understanding what sits on the stack (the handle) versus the heap (the data) demystifies aliasing forever.

---

## V. THE CATASTROPHIC MEMORY BUGS (manual management's price)

When you manage the heap by hand (C/C++), five classic disasters await:

1. **Memory leak** — you forget to `free`. Memory grows until the program dies. Slow death.
2. **Use-after-free (dangling pointer)** — you `free` then use the pointer. Reads garbage or corrupts data. A top security exploit.
3. **Double free** — you `free` the same block twice. Corrupts the allocator's bookkeeping.
4. **Buffer overflow** — you write past an array's end, clobbering adjacent memory (or the return address → arbitrary code execution). The #1 historical security hole.
5. **Uninitialized read** — you read heap memory before writing it; you get whatever was there (leaks secrets, nondeterministic bugs).

> Microsoft and Google independently report that **~70% of their serious security vulnerabilities are memory-safety bugs.** This statistic is *the entire reason* garbage collection and Rust's ownership exist — automating away the human error that causes these.

---

## VI. STACK ALLOCATION IS AN OPTIMIZATION LEVER

Because the stack is so much faster than the heap, high-performance code minimizes heap allocation:
- **Escape analysis** — smart compilers (JVM, Go) prove an object *doesn't escape* its function and allocate it on the stack instead of the heap, avoiding GC pressure.
- **Value types / structs** — Go, C#, Rust, C++ let you keep data on the stack by default, avoiding pointer chasing (which also improves cache locality — huge for performance).
- **Arenas / pools** — allocate a big block once, hand out slices, free all at once — amortizing heap cost.

Knowing where your data lives (stack vs heap) is the foundation of performance tuning. Pointer-chasing through scattered heap objects wrecks CPU cache performance; contiguous stack/value data flies.

---

## 📌 Key Takeaways
- **Stack**: fast, automatic, LIFO, small, fixed-size — for locals and call frames. Overflow on deep recursion.
- **Heap**: flexible size and lifetime, slower, manually managed, fragments — for dynamic/long-lived data.
- Value-vs-reference behavior = whether the stack holds the data itself or just a pointer to the heap.
- Manual heap management causes leaks, use-after-free, double-free, buffer overflows — ~70% of security bugs.
- Minimizing heap allocation (stack/value types, escape analysis, cache locality) is core to performance.

**Next:** [`02-Garbage-Collection.md`](./02-Garbage-Collection.md)
