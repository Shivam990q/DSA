# 🛡️ Type Systems — The Science of Preventing Bad Programs

> *"A type system is a tractable syntactic method for proving the absence of certain program behaviors."* — Benjamin Pierce, *Types and Programming Languages*

A **type** classifies values by what they are and what you can do with them. A **type system** is the set of rules a language uses to assign types and reject programs that misuse them. It is the single most powerful tool for catching bugs *before* the program ever runs — a lightweight, automatic proof system built into your compiler.

---

## 📚 Contents

1. [`01-Static-vs-Dynamic.md`](./01-Static-vs-Dynamic.md) — When types are checked; strong vs weak; the great tradeoff
2. [`02-Type-Inference.md`](./02-Type-Inference.md) — How compilers deduce types you didn't write (Hindley–Milner)
3. [`03-Polymorphism-and-Generics.md`](./03-Polymorphism-and-Generics.md) — One code, many types; parametric, ad-hoc, subtype polymorphism
4. [`04-Advanced-Types.md`](./04-Advanced-Types.md) — Algebraic, dependent, linear, gradual types; the frontier

---

## 🧭 Why This Section Matters Most

If you take one thing from this codex, take this: **a good type system is a proof assistant that runs on every compile.** Rust's borrow checker, Haskell's type classes, TypeScript's inference — these move mountains of bugs from "3 a.m. production incident" to "red squiggle in your editor." Understanding types deeply changes how you write code in *every* language, typed or not.

```
Weakly typed  ─────────────────────────────► Strongly typed
(implicit coercions)                          (no silent conversions)
   C, JS, PHP                                    Haskell, Rust, Python*

Dynamically checked ────────────────────────► Statically checked
(at runtime)                                   (at compile time)
   Python, Ruby, JS                              Rust, Haskell, Java, TS
```
(*Python is strongly but dynamically typed — a common point of confusion, clarified in file 01.)

---

## 📌 Key Takeaways
- A type is a **classification + a contract**; a type system **proves** certain bugs can't happen.
- Two independent axes: **static/dynamic** (when checked) and **strong/weak** (how strictly).
- Richer types = more bugs caught at compile time, at the cost of more upfront rigor.

**→ Start:** [`01-Static-vs-Dynamic.md`](./01-Static-vs-Dynamic.md) | Back to [`../README.md`](../README.md)
