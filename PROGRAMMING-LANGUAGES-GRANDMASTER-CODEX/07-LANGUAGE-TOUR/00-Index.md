# 🌍 The Language Tour

> *"Eight languages, to the metal. Not tutorials — dissections. Where each sits in the design space, and why."*

Now we apply the theory. Each file dissects one language: its history and purpose, where it sets the [tradeoff dials](../00-PHILOSOPHY-AND-DOCTRINE/03-Language-Tradeoffs.md), its defining features, its soul, and when to reach for it. The goal isn't to teach you syntax (docs do that) — it's to help you *understand* each language as a coherent set of decisions.

---

## 📚 Contents

1. [`01-C.md`](./01-C.md) — The portable assembler; the mother of modern languages
2. [`02-Cpp.md`](./02-Cpp.md) — Zero-cost abstraction; power and complexity
3. [`03-Rust.md`](./03-Rust.md) — Safety and speed via ownership; the systems revolution
4. [`04-Go.md`](./04-Go.md) — Radical simplicity and built-in concurrency
5. [`05-Java.md`](./05-Java.md) — The enterprise workhorse; the JVM ecosystem
6. [`06-Python.md`](./06-Python.md) — Readability, batteries, and the language of data/AI
7. [`07-JavaScript-and-TypeScript.md`](./07-JavaScript-and-TypeScript.md) — The language of the web, and its typed savior
8. [`08-Haskell.md`](./08-Haskell.md) — Pure functional; the language that rewires your brain

---

## 🧭 The Eight, Placed on the Dials

| Language | Typing | Memory | Paradigm lean | Superpower | Pays with |
|----------|--------|--------|---------------|-----------|-----------|
| **C** | static, weak | manual | procedural | total control, ubiquity | safety (footguns) |
| **C++** | static, weak | manual + RAII | multi | zero-cost abstraction | vast complexity |
| **Rust** | static, strong | ownership | multi | safety + speed, no GC | learning curve |
| **Go** | static, strong | GC | procedural + CSP | simplicity, concurrency | expressiveness |
| **Java** | static, strong | GC (JVM) | OOP | ecosystem, portability, tooling | verbosity, footprint |
| **Python** | dynamic, strong | GC | multi | readability, libraries | raw speed |
| **JS/TS** | dyn/gradual | GC | multi | runs everywhere (the web) | JS's warts (TS fixes many) |
| **Haskell** | static, strong | GC (lazy) | pure functional | correctness, expressiveness | steep concepts |

---

## 🎯 How to read a language file
For each language, watch for the *coherence*: its features aren't random — they follow from its founding purpose. C's danger follows from "be a portable assembler." Go's missing features follow from "a big team must read this in a week." Rust's difficulty follows from "safety without GC." Once you see the through-line, the language stops being a pile of syntax and becomes a philosophy.

**→ Start:** [`01-C.md`](./01-C.md) | Back to [`../README.md`](../README.md)
