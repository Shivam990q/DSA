# 🔬 Semantic Analysis and Intermediate Representations

> *"Parsing tells you the program is well-formed. Semantic analysis tells you it makes sense."*

---

## I. SEMANTIC ANALYSIS — CHECKING MEANING

A program can parse perfectly and still be nonsense: using an undeclared variable, adding a string to a list, calling a function with the wrong number of arguments. **Semantic analysis** walks the AST and verifies the program *means* something valid. Its main jobs:

1. **Name resolution / scope checking** — every identifier refers to a declared, visible binding.
2. **Type checking** — every operation gets operands of compatible types.
3. **Other static rules** — definite assignment, unreachable code, exhaustive matches, `const` not reassigned, etc.

The output is a **decorated (typed) AST** — the same tree, now annotated with resolved symbols and types, ready for the middle/back end.

---

## II. THE SYMBOL TABLE

The core data structure of semantic analysis is the **symbol table**: a mapping from names to information about them (type, kind, scope, memory location).

Because of nested scopes, it's really a *stack of tables* (or a chain of scopes):

```
enter function      → push a new scope
  declare x:int     → add x to current scope
  enter block {}    → push a nested scope
    declare y:str   → add y to inner scope
    use x           → search inner scope (miss) → outer scope (hit! x:int)
  exit block        → pop inner scope (y disappears)
exit function       → pop function scope
```

Looking up a name searches from the innermost scope outward — this *is* lexical scoping, implemented. Name resolution failures ("undefined variable `foo`") and shadowing are detected here.

---

## III. TYPE CHECKING IN PRACTICE

The type checker walks the AST bottom-up, computing each expression's type and verifying rules:

```
   expr:  x + y   where x:int, y:int
   check: is '+' defined for (int, int)?  yes → result type: int
   
   expr:  "a" + 5
   check: is '+' defined for (string, int)?  → depends on the language:
          - Java: string + int → string (concatenation, defined)
          - Haskell/Rust: ERROR (no such overload)
          - Python: TypeError at runtime (dynamic)
```

For statically-typed languages, this is where most bugs are caught (the [error ladder](../01-LANGUAGE-FOUNDATIONS/02-Syntax-vs-Semantics.md) level 3). The checker also performs **type inference** (see [`../03-TYPE-SYSTEMS/02-Type-Inference.md`](../03-TYPE-SYSTEMS/02-Type-Inference.md)) where annotations are omitted, and **coercion insertion** where implicit conversions are allowed (e.g., `int` → `double`).

---

## IV. INTERMEDIATE REPRESENTATIONS (IR)

Generating machine code directly from the AST is possible but awkward — the AST is shaped for *humans*, not optimization. So compilers first lower the AST into one or more **intermediate representations**: simpler, more uniform, machine-independent forms designed for analysis and optimization.

Why an IR?
- **Optimization is easier** on a regular, low-level form than on a rich tree.
- **Portability** — the same IR can target many CPUs (write the front end once, reuse the back ends).
- **Reuse** — many languages can share one optimizer (this is LLVM's whole business model).

### Common IR forms
- **Three-address code (TAC)** — every instruction has at most three operands: `t1 = a + b`. Simple, close to assembly.
- **Control-flow graph (CFG)** — basic blocks (straight-line code) connected by branches. The canvas for most analyses.
- **Static single assignment (SSA)** — each variable is assigned *exactly once*; reassignments become new versions (`x1`, `x2`). SSA makes data-flow crystal clear and is the backbone of modern optimizers (LLVM IR is SSA-based).

```
source:   x = a + b * c
TAC:      t1 = b * c
          t2 = a + t1
          x  = t2
```

---

## V. LLVM — THE IR THAT ATE THE WORLD

**LLVM IR** is the most important IR in practice. It's a typed, SSA-based, machine-independent assembly-like language. The architecture:

```
   Clang (C/C++) ─┐
   Rust        ──┤
   Swift       ──┼──►  LLVM IR  ──►  LLVM Optimizer  ──►  x86 / ARM / RISC-V / WASM
   Julia       ──┤        (one shared middle+back end for all these languages)
   many more   ──┘
```

Any language that emits LLVM IR instantly gets LLVM's world-class optimizations and every CPU LLVM targets. This is *why* Rust, Swift, and Julia could achieve C-level performance without writing their own optimizers — they stand on LLVM. It's the front/middle/back-end decoupling from the section index, realized industrially.

---

## VI. LOWERING — CROSSING ABSTRACTION LEVELS

Compilation is a series of **lowerings** — each step translates to a lower, simpler level:

```
Typed AST  →  high-level IR  →  mid-level IR (SSA/CFG)  →  low-level IR  →  machine code
(rich, human)                                                              (bytes, CPU)
```

At each level you lose abstraction but gain optimizability and machine-proximity. `for x in list` becomes a loop with an iterator, becomes a counter and bounds check, becomes increment/compare/branch instructions. Understanding lowering demystifies "how does a `match` become a jump table?" — it's just successive translations, each mechanical.

---

## 📌 Key Takeaways
- **Semantic analysis** checks *meaning*: name resolution, type checking, and static rules → a decorated (typed) AST.
- The **symbol table** (a stack of scopes) implements lexical scoping and catches undefined-name errors.
- **Intermediate representations** (three-address code, CFGs, **SSA**) are simpler forms designed for optimization and portability.
- **LLVM IR** (typed, SSA-based) lets many languages share one optimizer and target many CPUs — the industrial front/middle/back-end split.
- Compilation is successive **lowering**: trading abstraction for machine-proximity and optimizability.

**Next:** [`03-Code-Generation-and-Optimization.md`](./03-Code-Generation-and-Optimization.md)
