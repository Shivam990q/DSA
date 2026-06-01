# 🧠 Memory Models — Where Data Lives

> *"You cannot reason about an algorithm whose memory you do not understand."*

---

## I. THE MEMORY HIERARCHY

```
┌─────────────────────────────────────────┐
│  CPU Registers       (~32-64 bytes)     │  ~0.3 ns
├─────────────────────────────────────────┤
│  L1 Cache            (~32-64 KB)        │  ~1 ns
├─────────────────────────────────────────┤
│  L2 Cache            (~256 KB - 1 MB)   │  ~3 ns
├─────────────────────────────────────────┤
│  L3 Cache            (~10-40 MB)        │  ~10 ns
├─────────────────────────────────────────┤
│  Main Memory (DRAM)  (~16-128 GB)       │  ~100 ns
├─────────────────────────────────────────┤
│  SSD / NVMe          (~1-4 TB)          │  ~10-100 μs
├─────────────────────────────────────────┤
│  HDD                 (~4-20 TB)         │  ~10 ms
├─────────────────────────────────────────┤
│  Network             (anywhere)         │  ~50-500 ms
└─────────────────────────────────────────┘
```

**Implication**: each step down is ~10× slower. Cache-friendly code can be *100×* faster than cache-unfriendly code with the same Big-O.

---

## II. STACK vs HEAP

### Stack
- **Where**: contiguous, grows downward (typically)
- **Lifetime**: function scope (push on call, pop on return)
- **Size**: small (1-8 MB typical thread limit)
- **Speed**: very fast (just decrement stack pointer)
- **Contents**: local variables, function arguments, return addresses

### Heap
- **Where**: dynamic memory pool managed by allocator
- **Lifetime**: explicit (malloc/free, new/delete) or via GC
- **Size**: large (gigabytes)
- **Speed**: slower (allocator must find space, fragmentation)
- **Contents**: dynamically allocated objects

```cpp
void f() {
    int x = 5;                  // STACK
    int* p = new int(10);       // p on STACK, *p on HEAP
    vector<int> v = {1, 2, 3};  // v's metadata on STACK, data on HEAP
    delete p;                   // free heap
}                               // x and v's stack memory popped
```

---

## III. CACHE LINES & LOCALITY

A **cache line** is typically **64 bytes**. Memory is fetched a line at a time.

**Implication**: accessing `a[0]` and `a[1]` is essentially free if `a[0]` is already cached. Accessing `a[0]` and `a[10000]` is expensive (two cache misses).

### Spatial locality
Accessing nearby memory is fast.
> Iterating `for (i = 0; i < n; i++) sum += a[i];` is cache-friendly.

### Temporal locality
Accessing recently-used memory is fast.
> A small loop body that reuses the same variables.

### Cache-friendly patterns
- Iterate arrays in row-major order in C/C++ (`for i: for j: a[i][j]`)
- Use struct-of-arrays (SoA) over array-of-structs (AoS) when iterating one field
- Linear scans > random access (where possible)

### Cache-unfriendly patterns
- Linked lists (each node a pointer chase)
- Random hash map access (each access lands in a random bucket)
- Iterating column-major in row-major language

---

## IV. ARRAY vs LINKED LIST: A MEMORY STORY

```
ARRAY:    [1][2][3][4][5]        ← contiguous, cache-line-friendly
                                  ← Iteration: 1 cache miss for ~16 ints

LINKED:   [1|→][2|→][3|→][4|→][5|null]   ← pointer-chasing
                                          ← Iteration: 1 cache miss per node
```

**Practical**: Iterating a `vector<int>` of size 1M is ~10× faster than a `list<int>` of size 1M. Even though both are O(n).

---

## V. THE C++ MEMORY MODEL

Six categories of memory:
1. **Code** (read-only)
2. **Static / global** (initialized at startup)
3. **Stack** (function locals)
4. **Heap / free store** (new/malloc)
5. **Memory-mapped** (mmap'd files, shared memory)
6. **Thread-local** (per-thread storage)

---

## VI. POINTERS, REFERENCES, AND OWNERSHIP

```cpp
int x = 5;
int& r = x;     // reference: alias for x
int* p = &x;    // pointer: holds address of x
*p = 10;        // dereference: x is now 10
```

**Modern C++ ownership:**
- `unique_ptr<T>` — single ownership, RAII
- `shared_ptr<T>` — ref-counted shared ownership
- `weak_ptr<T>` — non-owning observation

**Java/Python**: every object is a heap pointer (almost). GC handles cleanup. Easier but less control.

---

## VII. THE STACK FRAME

When you call `f(3, 4)`:
```
┌──────────────┐ ← stack pointer
│  return addr │
│  saved regs  │
│  arg: 4      │
│  arg: 3      │
│  local vars  │
└──────────────┘
```

**Recursion depth** is bounded by stack size. Each call adds a frame. Too-deep recursion → **stack overflow**.

In C++, default stack is ~8 MB. Each frame ~50-200 bytes. → ~50K-100K recursion depth before overflow. Use `ulimit -s unlimited` (Linux) or convert to iteration if needed.

---

## VIII. MEMORY ALIGNMENT

Most CPUs require multi-byte values be aligned: 4-byte int at address divisible by 4, 8-byte double at address divisible by 8.

**Struct padding example:**
```cpp
struct A {
    char c;     // 1 byte
    // 3 bytes padding
    int i;      // 4 bytes
};              // sizeof(A) == 8, not 5!

struct B {
    int i;      // 4 bytes
    char c;     // 1 byte
    // 3 bytes padding (for arrays of B)
};              // sizeof(B) == 8
```

**Lesson**: order struct fields largest-to-smallest to minimize padding.

---

## IX. THE COST OF ALLOCATION

`new`/`malloc` is expensive (≈100-1000 ns each). For many small allocations, use:
- **Object pools** (preallocate, reuse)
- **Arena allocators** (allocate one big block, parcel out)
- **Stack allocation** (when possible — `alloca` in C, fixed arrays)

**CP wisdom**: allocate all memory upfront. Avoid `vector::push_back` in hot loops; reserve capacity.

---

## X. WHAT THIS MEANS FOR ALGORITHMS

1. An O(n²) cache-friendly algorithm can beat an O(n log n) cache-unfriendly one for small n.
2. Linked-based DSes (linked list, BST) are slower than they look due to cache misses.
3. **vEB layout**, **B-trees**, **van Emde Boas tree** are designed for cache hierarchy.
4. SIMD can give 4-16× speedup for data-parallel algorithms.
5. Multi-threading helps only if memory bandwidth isn't saturated.

---

## XI. RECOMMENDED READING

- **What Every Programmer Should Know About Memory** — Ulrich Drepper (free PDF)
- **Computer Systems: A Programmer's Perspective** (Bryant & O'Hallaron)
- **Hennessy & Patterson** — *Computer Architecture: A Quantitative Approach*

---

**→ Next:** [`03-Programming-Paradigms.md`](./03-Programming-Paradigms.md)
