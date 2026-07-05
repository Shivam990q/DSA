# 🧠 Memory and Runtime

> *"The runtime is where the truth lives. Every abstraction eventually cashes out as bytes moving through memory."*

Where do values actually live? Who allocates them, and who frees them? The answer to "how does a language manage memory?" is one of the deepest forks in language design — it determines safety, speed, predictability, and the entire feel of a language. This section takes you to the metal.

---

## 📚 Contents

1. [`01-Stack-Heap-and-Layout.md`](./01-Stack-Heap-and-Layout.md) — Where values live: stack vs heap, memory layout, pointers
2. [`02-Garbage-Collection.md`](./02-Garbage-Collection.md) — Automatic memory management: reference counting, tracing, generational GC
3. [`03-Ownership-and-Borrowing.md`](./03-Ownership-and-Borrowing.md) — Rust's third way: memory safety without a garbage collector

---

## 🧭 The Three Memory-Management Strategies

Every language picks one (or blends):

| Strategy | Who frees memory | Cost | Languages |
|----------|------------------|------|-----------|
| **Manual** | you (`malloc`/`free`, `new`/`delete`) | max control, max danger (leaks, use-after-free) | C, C++ |
| **Garbage collection** | an automatic runtime collector | convenience, but pauses & overhead | Java, Python, Go, JS, C# |
| **Ownership** | the compiler, via static rules | safety + speed, but a learning curve | Rust |

This one choice ripples through everything: performance predictability, whether you can build a real-time system, how hard the language is to learn, and how many memory bugs (the #1 source of security vulnerabilities) are even *possible*.

---

## 📌 Key Takeaways
- Values live on the **stack** (fast, scoped, automatic) or the **heap** (flexible, must be managed).
- Memory is managed **manually** (C), by a **garbage collector** (Java/Python/Go), or by **ownership** (Rust).
- Memory bugs (use-after-free, buffer overflow) cause ~70% of serious security vulnerabilities — which is why safe memory management is a language's most consequential decision.

**→ Start:** [`01-Stack-Heap-and-Layout.md`](./01-Stack-Heap-and-Layout.md) | Back to [`../README.md`](../README.md)
