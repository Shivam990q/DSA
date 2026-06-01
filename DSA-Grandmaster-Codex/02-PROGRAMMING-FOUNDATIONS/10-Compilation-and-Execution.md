# ⚙️ Compilation & Execution — From Source to Silicon

> *"To master your code, know what it becomes."*

---

## I. THE PIPELINE

For C++:
```
Source (.cpp)
   │ preprocessor (handles #include, #define, macros)
   ▼
Translation unit (.i)
   │ compiler (parsing, semantic analysis, optimization)
   ▼
Assembly (.s)
   │ assembler
   ▼
Object file (.o)
   │ linker (resolves cross-file symbols, libraries)
   ▼
Executable (a.out / .exe)
   │ loader
   ▼
Process in memory
   │ CPU executes
   ▼
Output
```

For Python:
```
Source (.py)
   │ compiler
   ▼
Bytecode (.pyc)
   │ Python virtual machine (CPython)
   ▼
Runtime execution
```

For Java:
```
Source (.java)
   │ javac
   ▼
Bytecode (.class)
   │ JVM (with JIT compiler)
   ▼
Native machine code (at runtime)
   │ CPU
   ▼
Output
```

---

## II. COMPILED VS INTERPRETED

| Compiled                       | Interpreted                       |
|--------------------------------|-----------------------------------|
| Source → machine code (once)   | Source → executed (each run)      |
| Fast execution                 | Slower execution                  |
| Slower iteration (compile time)| Fast iteration                    |
| Errors caught early            | Errors at runtime                 |
| Examples: C, C++, Rust, Go     | Examples: Python, Ruby, JS (interpreted historically) |

**Hybrid (JIT)**: bytecode + just-in-time compilation. Java, JavaScript (V8), .NET. Best of both.

---

## III. COMPILER OPTIMIZATIONS (Why C++ -O2 matters)

Modern compilers perform:
- **Constant folding**: `5 + 3` → `8` at compile time
- **Dead code elimination**: code with no observable effect removed
- **Loop unrolling**: `for(i=0;i<4;i++) a[i]++;` → `a[0]++; a[1]++; a[2]++; a[3]++;`
- **Inlining**: function calls replaced by body
- **Vectorization**: scalar loops → SIMD when safe
- **Strength reduction**: `i*2` → `i<<1`
- **Common subexpression elimination**

For CP: always compile with `-O2` (or `-O3`). The speedup can be 5-10×.

---

## IV. WHAT YOUR CODE BECOMES

```cpp
int sum(int* a, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    return s;
}
```

Becomes (simplified x86-64 assembly):
```
sum:
    xor eax, eax        ; eax = 0 (s)
    test edi, edi       ; n == 0?
    jle .end
    xor ecx, ecx        ; i = 0
.loop:
    add eax, [rdi+rcx*4] ; s += a[i]
    inc ecx              ; i++
    cmp ecx, edi         ; i < n?
    jl .loop
.end:
    ret
```

With AVX-512, the loop body becomes a single SIMD instruction operating on 16 ints at a time.

**Lesson**: the inner loop matters enormously. Ten lines of C++ can become 3 assembly instructions; or 30. Profile and read assembly when desperate.

---

## V. UNDEFINED BEHAVIOR (UB)

**C and C++ have undefined behavior**: certain operations have no defined meaning. The compiler can do anything (literally — including time travel, formatting your hard drive).

**Common UB**:
- Signed integer overflow
- Reading uninitialized variables
- Out-of-bounds array access
- Dereferencing nullptr
- Modifying string literals
- Race conditions

**Implication**: in CP, when you have signed `int` overflowing in `i*j`, the compiler may *assume it doesn't happen* and produce wrong code.

**Defense**: use `unsigned` if overflow is intentional, or `long long`, or check bounds.

---

## VI. STATIC vs DYNAMIC LINKING

- **Static**: library code copied into your executable. Bigger binary, no runtime dependencies.
- **Dynamic** (DLL/.so): library loaded at runtime. Smaller binary, may "fail at runtime" if missing.

For CP: doesn't matter (single .cpp file).

---

## VII. THE STACK FRAME (revisited deeper)

When `f(a, b)` calls `g(c)`:

```
[caller's frame]    
[a, b]               ← f's args
[saved EBP]          ← f's frame pointer
[f's locals]         
[saved registers]    ← if needed
[c]                  ← g's arg
[return addr to f]   
[saved EBP]          ← g's frame pointer
[g's locals]         ← stack pointer here
```

When `g` returns: SP and BP restored, return address jumped to.

---

## VIII. HEAP ALLOCATION

`malloc(n)` / `new T[n]`:
1. Find a free block of size ≥ n
2. Mark it allocated
3. Return pointer
4. May fragment memory over many alloc/free cycles

**Modern allocators** (jemalloc, tcmalloc): thread-local caches, segregated free lists, very fast for typical workloads.

**Cost**: ≈ 50-200 cycles per allocation (a "function call" worth of cycles). Avoid in hot loops.

---

## IX. DYNAMIC DISPATCH (vtables)

In C++ with virtual functions:
```cpp
class Shape { virtual void draw() = 0; };
class Circle : public Shape { void draw() override; };
class Square : public Shape { void draw() override; };

Shape* s = new Circle();
s->draw();   // dispatched via vtable lookup
```

vtable = per-class table of function pointers. Each object has a hidden pointer to its class's vtable.

**Cost**: 1-2 cache misses per virtual call. In hot loops, prefer static dispatch (templates, CRTP) when possible.

---

## X. PYTHON INTERNALS (briefly)

Python is *much* slower than C++ for raw computation due to:
1. **Everything is a `PyObject*`** — even an `int` is a heap-allocated object
2. **Reference counting** + occasional GC
3. **Dynamic types** — every operation is a hash lookup of methods
4. **GIL** (Global Interpreter Lock) — only one Python thread executes Python bytecode at a time

**Speedups**:
- NumPy / pandas: bulk ops in C
- Numba: JIT compile Python
- PyPy: alternative interpreter with JIT
- Cython: write Python-like, compile to C

For CP, Python is ~10-30× slower than C++ in tight numeric loops.

---

## XI. JAVA / JVM

Java compiles to bytecode. JVM interprets initially, then **JIT-compiles** hot methods to native code.

After warm-up, Java can be within 1.5-2× of C++ for many workloads.

JIT optimizations: inlining, escape analysis, devirtualization, on-stack replacement.

---

## XII. WHAT THIS MEANS FOR YOUR CODE

1. **Hot loops dominate**. 90% of time is in 10% of code. Optimize that 10%.
2. **Allocation is expensive**. Reuse buffers; reserve vector capacity.
3. **Cache locality matters**. Iterate contiguous memory.
4. **Branch prediction matters**. Predictable branches are nearly free; unpredictable ones cost ~20 cycles.
5. **UB is dangerous**. Especially in optimized C++ builds.

---

## XIII. RECOMMENDED READING

- **Computer Systems: A Programmer's Perspective** (Bryant & O'Hallaron) ⭐
- **Engineering a Compiler** (Cooper, Torczon)
- **Crafting Interpreters** (Nystrom) — free online
- **Optimization Manuals** (Agner Fog) — for hard-core perf

---

**→ Next universe:** [`../03-PROBLEM-SOLVING-FOUNDATIONS/00-Index.md`](../03-PROBLEM-SOLVING-FOUNDATIONS/00-Index.md)
