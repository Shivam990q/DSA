# 🔬 Semantics and Theory — The Mathematics of Meaning

> *"To define a language rigorously is to give its programs mathematical meaning. This is where computer science meets logic."*

The theoretical bedrock. Here we answer "what does a program *mean*?" with mathematical precision, and discover the astonishing bridge between programs and proofs. This section is optional for building things but essential for *understanding* things — and for reading programming-language research.

---

## 📚 Contents

1. [`01-Lambda-Calculus.md`](./01-Lambda-Calculus.md) — The simplest possible language; the theory of functions and computation
2. [`02-Operational-and-Denotational-Semantics.md`](./02-Operational-and-Denotational-Semantics.md) — Two rigorous ways to define what programs mean
3. [`03-Type-Theory.md`](./03-Type-Theory.md) — Types as logic; the Curry–Howard correspondence; programs as proofs

---

## 🧭 Why Theory Matters (even for engineers)

Theory isn't ivory-tower decoration. Lambda calculus *is* the model behind every functional language and closures. Operational semantics is how language specs actually define behavior. The Curry–Howard correspondence — that **programs are proofs and types are theorems** — is one of the deepest ideas in all of science, and it's why dependent types and proof assistants (verifying real software and mathematics) exist. Understanding this layer turns you from someone who *uses* languages into someone who *understands and could design* them.

```
Lambda calculus  →  the essence of computation & functions
Semantics        →  how we rigorously define "meaning"
Type theory      →  how types = logic, and programs = proofs
```

---

## 📌 Key Takeaways
- Semantics gives programs **precise mathematical meaning** — the foundation of language specs and verification.
- **Lambda calculus** is a complete model of computation using only functions.
- The **Curry–Howard correspondence** reveals that types are propositions and programs are their proofs.

**→ Start:** [`01-Lambda-Calculus.md`](./01-Lambda-Calculus.md) | Back to [`../README.md`](../README.md)
