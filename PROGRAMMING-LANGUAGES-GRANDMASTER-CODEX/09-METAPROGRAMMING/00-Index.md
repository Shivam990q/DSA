# 🪞 Metaprogramming — Programs That Write Programs

> *"Code is data. Data is code. When a program can inspect and generate programs, the language becomes clay in your hands."*

Metaprogramming is writing programs that treat *other programs (or themselves)* as data — inspecting, generating, or transforming code. It's how frameworks feel magical, how DSLs are built, and how languages extend themselves.

---

## 📚 Contents

1. [`01-Macros-Reflection-and-DSLs.md`](./01-Macros-Reflection-and-DSLs.md) — Compile-time macros, runtime reflection, and domain-specific languages

---

## 🧭 The Metaprogramming Spectrum

```
COMPILE TIME ─────────────────────────────► RUN TIME
   Macros              Templates/Generics        Reflection / eval
   (Lisp, Rust)        (C++, Rust)               (Java, Python, JS)
   transform code      generate code             inspect/modify at runtime
   before compiling    during compiling          while running
```

- **Compile-time** metaprogramming (macros, templates) has zero runtime cost and full safety checking, but runs before the program executes.
- **Run-time** metaprogramming (reflection, `eval`) is maximally flexible but costs performance and safety.

---

## 📌 Key Takeaways
- Metaprogramming = code that manipulates code, at **compile time** (macros/templates) or **run time** (reflection/eval).
- It powers DSLs, ORMs, serializers, dependency injection, and "magic" framework behavior.
- Power vs cost: compile-time is safe and fast; run-time is flexible but slower and harder to analyze.

**→ Start:** [`01-Macros-Reflection-and-DSLs.md`](./01-Macros-Reflection-and-DSLs.md) | Back to [`../README.md`](../README.md)
