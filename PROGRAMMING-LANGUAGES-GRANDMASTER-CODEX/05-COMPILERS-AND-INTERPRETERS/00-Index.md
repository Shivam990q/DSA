# ⚙️ Compilers and Interpreters

> *"Between `source.c` and a running process lies one of the most beautiful pipelines in all of engineering."*

How does human-readable text become something a CPU executes? This section walks the entire journey — lexing, parsing, semantic analysis, intermediate representations, optimization, code generation, and the interpreter/VM/JIT alternatives. Understanding this pipeline demystifies compiler errors, performance, and language design forever.

---

## 📚 Contents

1. [`01-Lexing-and-Parsing.md`](./01-Lexing-and-Parsing.md) — Text → tokens → abstract syntax tree
2. [`02-Semantic-Analysis-and-IR.md`](./02-Semantic-Analysis-and-IR.md) — Type checking, symbol tables, intermediate representations
3. [`03-Code-Generation-and-Optimization.md`](./03-Code-Generation-and-Optimization.md) — IR → optimized machine code
4. [`04-Interpreters-VMs-and-JIT.md`](./04-Interpreters-VMs-and-JIT.md) — Tree-walkers, bytecode VMs, and just-in-time compilation

---

## 🧭 The Compiler Pipeline

```
  SOURCE CODE
      │  ┌──────────────── FRONT END (understand the program) ─────────────┐
      ▼  │
   Lexer  → tokens
      ▼
   Parser → AST (abstract syntax tree)
      ▼
   Semantic analysis → typed AST + symbol tables   (type checking, scope resolution)
      │  └──────────────────────────────────────────────────────────────────┘
      ▼  ┌──────────────── MIDDLE END (improve it) ───────────────────────────┐
   IR generation → intermediate representation
      ▼
   Optimization → better IR   (inlining, dead-code elimination, constant folding)
      │  └──────────────────────────────────────────────────────────────────┘
      ▼  ┌──────────────── BACK END (emit it) ────────────────────────────────┐
   Code generation → target machine code / bytecode
      ▼
   MACHINE CODE / BYTECODE
```

This **front / middle / back end** split is why LLVM can support many languages (each writes a front end) and many CPUs (LLVM provides the back ends). It's one of the most important architectural ideas in software.

---

## 📌 Key Takeaways
- Compilation is a pipeline: lex → parse → analyze → IR → optimize → codegen.
- The **front/middle/back end** split decouples languages from CPUs (the LLVM insight).
- Interpreters skip codegen and execute the AST/bytecode directly; JITs compile hot paths at runtime.

**→ Start:** [`01-Lexing-and-Parsing.md`](./01-Lexing-and-Parsing.md) | Back to [`../README.md`](../README.md)
