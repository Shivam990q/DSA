# 🏭 Code Generation and Optimization (The Back End)

> *"The optimizer's job: make the program faster and smaller without changing what it means."*

---

## I. CODE GENERATION — IR TO MACHINE CODE

The back end translates optimized IR into actual instructions for a target CPU. Three central problems:

### 1. Instruction selection
Map IR operations to real machine instructions. One IR op may map to several instructions, or one clever instruction may cover several IR ops (e.g., x86's `lea` can do `a*4 + b` in one instruction).

### 2. Register allocation
CPUs have very few fast registers (x86-64 has ~16 general-purpose). The compiler must decide which values live in registers and which "spill" to slower stack memory. This is modeled as **graph coloring** (an NP-hard problem, solved heuristically) — one of the most impactful optimizations, since register access is ~100× faster than memory.

### 3. Instruction scheduling
Reorder instructions to keep the CPU's pipeline busy and avoid stalls (e.g., start a slow memory load early so its result is ready when needed), respecting data dependencies.

The output is assembly/machine code, then linked with libraries into an executable.

---

## II. THE MAJOR OPTIMIZATIONS

Optimizations transform IR into equivalent-but-better IR. The classics:

| Optimization | What it does | Example |
|--------------|-------------|---------|
| **Constant folding** | compute constants at compile time | `3 * 4` → `12` |
| **Constant propagation** | replace variables with known constant values | `x=5; y=x+1` → `y=6` |
| **Dead code elimination** | remove code whose result is never used | delete unused assignments |
| **Common subexpression elimination** | compute a repeated expression once | `a*b + a*b` → `t=a*b; t+t` |
| **Function inlining** | replace a call with the function body | avoids call overhead, unlocks more optimization |
| **Loop-invariant code motion** | hoist unchanging computation out of loops | move `x=a+b` above the loop |
| **Strength reduction** | replace expensive ops with cheap ones | `x*2` → `x<<1`; `x*4` in a loop → repeated add |
| **Loop unrolling** | duplicate loop body to cut branch overhead | fewer iterations, more straight-line code |
| **Tail-call optimization** | reuse the stack frame for tail recursion | recursion as cheap as a loop |
| **Vectorization (SIMD)** | process multiple data elements per instruction | sum 8 floats at once |

**Inlining is the "mother optimization"** — by pasting a function's body into the caller, it exposes constants, dead code, and common subexpressions that were hidden across the call boundary, enabling *all the other* optimizations to fire. This is why "zero-cost abstractions" work: a tiny getter or iterator adaptor gets inlined away to nothing.

---

## III. WHY SSA MAKES OPTIMIZATION EASY

Recall SSA (each variable assigned once) from the previous file. It makes optimizations almost trivial:
- **Dead code elimination**: if a variable version is never used, delete its definition — one pass.
- **Constant propagation**: since each variable has one definition, propagating its value is unambiguous.
- **Use-def chains** are explicit: you instantly know where each value comes from and goes.

This is why LLVM, GCC's GIMPLE, and virtually every serious optimizer use SSA form.

---

## IV. AHEAD-OF-TIME vs JUST-IN-TIME OPTIMIZATION

- **AOT (ahead-of-time)** — optimize fully at build time (C, Rust, Go). Pros: fast startup, no runtime overhead, optimize hard (slow compiles are OK). Cons: can't use runtime information; must target a fixed CPU or the lowest common denominator.
- **JIT (just-in-time)** — optimize at run time (JVM, V8, .NET). Pros: uses *profile-guided* info — it sees which branches actually happen, which types actually flow — and optimizes the *hot* paths accordingly, even speculatively. Cons: warm-up time, runtime overhead, memory. (Covered in the next file.)

A JIT can sometimes *beat* an AOT compiler because it knows things only observable at runtime (e.g., "this virtual call always hits the same class → inline it speculatively"). AOT can't know that; JIT profiles and exploits it.

---

## V. THE OPTIMIZATION LEVELS YOU ACTUALLY USE

Every compiler exposes tiers:
- `-O0` — no optimization; fast compile, easy debugging (variables map to source).
- `-O1`/`-O2` — the standard: most safe optimizations. `-O2` is the usual production choice.
- `-O3` — aggressive (heavy inlining, vectorization); sometimes bigger/slower — measure!
- `-Os`/`-Oz` — optimize for size (embedded, WASM).
- `-Ofast` — allow math reassociation that may change floating-point results — use with care.

**The engineer's discipline:** optimizations must be *semantics-preserving* — but a few (fast-math, reordering) can subtly change floating-point results. And aggressive optimization can *expose* latent undefined behavior in C/C++ (the compiler assumes UB never happens and optimizes accordingly, producing "impossible" bugs). Know what your flags actually permit.

---

## VI. WHAT THIS MEANS FOR YOU AS A PROGRAMMER

- **Don't micro-optimize what the compiler already does.** `x*2` → `x<<1`, hoisting invariants, folding constants — the compiler does these better than you. Write clear code.
- **Do help the optimizer**: keep functions small (inlinable), avoid unnecessary indirection, use `const`/`final`/immutability (enables assumptions), and keep hot data contiguous (cache locality — the optimizer can't fix a bad data layout).
- **Profile before optimizing.** The optimizer handles the small stuff; your job is algorithms (the DSA codex) and data layout. Measure to find the real hot spot.

---

## 📌 Key Takeaways
- Code generation solves **instruction selection**, **register allocation** (graph coloring), and **scheduling**.
- Key optimizations: constant folding/propagation, dead-code elimination, CSE, **inlining** (the mother optimization), loop-invariant motion, strength reduction, vectorization, TCO.
- **SSA form** makes most optimizations simple and is used by all serious compilers.
- **AOT** optimizes at build time; **JIT** uses runtime profiles and can sometimes win.
- Write clear code and fix algorithms/data layout — let the compiler handle micro-optimizations; profile first.

**Next:** [`04-Interpreters-VMs-and-JIT.md`](./04-Interpreters-VMs-and-JIT.md)
