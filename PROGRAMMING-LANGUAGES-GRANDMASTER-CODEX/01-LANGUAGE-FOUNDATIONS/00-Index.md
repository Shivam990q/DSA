# 🧱 Language Foundations

> *"Syntax is skin. Semantics is the skeleton. Learn the skeleton."*

The atoms of every programming language. Before paradigms, types, and runtimes, you must understand what a language *is* at its core: how meaning is defined, how text becomes structure, and how names, values, and control actually work.

---

## 📚 Contents

1. [`01-What-Is-a-Programming-Language.md`](./01-What-Is-a-Programming-Language.md) — Syntax, semantics, pragmatics; the anatomy of a language
2. [`02-Syntax-vs-Semantics.md`](./02-Syntax-vs-Semantics.md) — The critical distinction; why "it compiles" ≠ "it's correct"
3. [`03-Grammars-and-Parsing.md`](./03-Grammars-and-Parsing.md) — Formal grammars, BNF, tokens, ASTs, ambiguity
4. [`04-Values-Bindings-and-Scope.md`](./04-Values-Bindings-and-Scope.md) — Variables, binding, lexical vs dynamic scope, closures, lifetimes
5. [`05-Expressions-Statements-and-Control.md`](./05-Expressions-Statements-and-Control.md) — Expressions vs statements, evaluation order, control flow, recursion

---

## 🧭 Recommended Learning Order

Walk 01 → 05 in order. Each builds on the last: you can't understand scope (04) without understanding what a value and a name are; you can't understand control flow (05) without expressions. This section is the vocabulary the entire codex speaks.

```
01 What is a PL ──► the three levels: syntax / semantics / pragmatics
02 Syntax vs Semantics ──► the distinction that prevents 90% of confusion
03 Grammars & Parsing ──► how text becomes a tree
04 Values, Bindings, Scope ──► where names get their meaning
05 Expressions & Control ──► how computation actually proceeds
```

---

## 📌 Key Takeaways
- A language = **syntax** (form) + **semantics** (meaning) + **pragmatics** (use).
- Parsing turns a flat string into a structured **abstract syntax tree (AST)**.
- **Scope** is the rulebook for connecting a name to a value; lexical scope enables closures.
- **Expressions produce values; statements produce effects.** Some languages have only one.

**→ Start:** [`01-What-Is-a-Programming-Language.md`](./01-What-Is-a-Programming-Language.md) | Back to [`../README.md`](../README.md)
