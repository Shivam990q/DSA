# 🎮 Interpreters, VMs, and JIT

> *"A compiler translates and leaves. An interpreter stays and runs. A JIT does both — translating as it runs."*

---

## I. THE SPECTRUM OF EXECUTION

There is no clean "compiled vs interpreted" binary — it's a spectrum of *when* translation happens:

```
Pure interpret ──── Bytecode VM ──── JIT ──── AOT compile
(execute AST)      (compile to      (compile hot   (compile fully
                    bytecode, then   paths at        before running)
                    interpret it)    runtime)
   Ruby (old)        CPython, JVM     JVM/HotSpot,    C, Rust, Go
                     (interpreter)    V8, PyPy, .NET
```

The tradeoff throughout: **startup speed and flexibility** (left) vs **execution speed** (right).

---

## II. TREE-WALKING INTERPRETERS — THE SIMPLEST

The most direct approach: build the AST, then **recursively walk it**, evaluating each node.

```python
def eval_node(node, env):
    kind = node[0]
    if kind == 'num':   return node[1]
    if kind == 'var':   return env[node[1]]
    if kind == 'binop':
        _, op, left, right = node
        l, r = eval_node(left, env), eval_node(right, env)
        return {'+': l+r, '-': l-r, '*': l*r, '/': l/r}[op]
```

- ✅ **Trivial to write** — great for teaching, config languages, DSLs, prototypes.
- ❌ **Slow** — re-walking the tree, dispatching on node type, and chasing pointers for every operation. No optimization.

This is how you'll first run your own language (see [`../10-LANGUAGE-DESIGN/02-Build-Your-Own-Language.md`](../10-LANGUAGE-DESIGN/02-Build-Your-Own-Language.md)). Early Ruby worked this way.

---

## III. BYTECODE VIRTUAL MACHINES — THE WORKHORSE

Most "interpreted" languages actually **compile to bytecode** — a compact, low-level instruction set for a *virtual* machine — then interpret the bytecode. This is far faster than walking a tree.

```
source.py  →  compile  →  bytecode (.pyc)  →  the VM's interpreter loop executes it
```

Two VM styles:
- **Stack-based** (JVM, CPython, .NET CLR, WASM) — operations push/pop an operand stack. `a + b` → `PUSH a; PUSH b; ADD`. Simpler, more compact bytecode.
- **Register-based** (Lua, Dalvik) — operations name virtual registers. `ADD r3, r1, r2`. Fewer instructions, often faster.

The heart of a VM is the **dispatch loop**: fetch the next bytecode, jump to its handler, execute, repeat. Optimizing this loop (computed gotos, "threaded code") is where interpreter performance lives.

**Why bytecode + VM won:** portability (compile once to bytecode, run on any CPU that has the VM — Java's "write once, run anywhere"), fast startup (no full native compile), and a foundation for JIT.

---

## IV. JUST-IN-TIME (JIT) COMPILATION — THE BEST OF BOTH

A JIT starts by interpreting bytecode, **profiles** which code runs most (the "hot" methods/loops), then **compiles those to native machine code at runtime** — using information only available while running.

```
1. Start interpreting bytecode (fast startup)
2. Count executions; find hot spots
3. Compile hot methods to optimized native code
4. Use runtime profile for speculative optimization
5. Deoptimize if an assumption breaks
```

### The JIT superpower: speculative optimization
Because it observes the running program, a JIT can bet on what it sees:
- *"This variable has been an integer 10,000 times → compile assuming integer; add a cheap guard."*
- *"This virtual call always hits the same class → inline it speculatively."*
- If a guard fails (a string shows up), **deoptimize** — fall back to the interpreter and recompile.

This is how JavaScript — a dynamically-typed language — runs *fast* in V8: the JIT speculates on types it observes and compiles specialized fast paths. It's also how the JVM's HotSpot and PyPy achieve near-native speed. A JIT can *beat* an AOT compiler precisely because AOT can't see runtime behavior.

### JIT costs
- **Warm-up** — code is slow until it's compiled (bad for short-lived programs and CLI tools).
- **Memory & CPU** — the compiler runs alongside your program.
- **Complexity** — JITs are enormous, subtle pieces of engineering (and a security surface).

---

## V. TIERED COMPILATION — THE MODERN REALITY

Production VMs (HotSpot, V8) use **multiple tiers**: a quick baseline JIT compiles hot code fast (modest optimization), and an aggressive optimizing JIT recompiles the *hottest* code with everything. This balances warm-up (get to native quickly) against peak performance (optimize the truly hot paths hard). Add **AOT/ahead-of-time snapshots** (Java's GraalVM native image, V8 snapshots) to kill warm-up for startup-sensitive workloads, and the "compiled vs interpreted" line dissolves entirely.

---

## VI. WHY THIS ALL MATTERS

- **"Python is slow" is imprecise.** CPython is a bytecode interpreter (slow); PyPy is a JIT (often 5–10× faster). The *language* isn't slow — the *implementation* is a choice.
- **Startup vs throughput is an engineering decision.** A CLI tool wants AOT (fast startup); a long-running server benefits from JIT (peak throughput after warm-up). This drives real deployment choices (e.g., GraalVM native images for serverless).
- **Understanding execution demystifies performance.** Why does the JVM get faster after running a while? (JIT warm-up.) Why is the first request slow? (Cold code.) Why can JS be fast? (Speculative JIT.) Now you know.

---

## 📌 Key Takeaways
- Execution is a spectrum: tree-walk → bytecode VM → JIT → AOT, trading startup/flexibility for speed.
- **Tree-walking** interpreters are simple but slow; great for DSLs and learning.
- **Bytecode VMs** (JVM, CPython, .NET, WASM) compile to portable low-level instructions and interpret them — the workhorse.
- **JIT** interprets, profiles, then compiles hot paths natively, using **speculative optimization** from runtime data — how JS/JVM get fast, and how a JIT can beat AOT.
- **Tiered compilation** blends baseline and optimizing JITs; the compiled/interpreted distinction is really a spectrum.

**Next:** [`../06-CONCURRENCY-MODELS/00-Index.md`](../06-CONCURRENCY-MODELS/00-Index.md)
