# 🛠️ Templates & Implementations

> *"A grandmaster's templates are weapons. Forge them, test them, trust them."*

All templates are battle-ready. Study them, adapt to your style, and stress-test before relying on them in contests.

---

## 📚 Available Files

### Contest Templates (multi-language)
- [`competitive-programming-template.cpp`](./competitive-programming-template.cpp) — C++17 CP template (aliases, macros, fast I/O, modular utils, custom hash, debug macros)
- [`competitive-programming-template.py`](./competitive-programming-template.py) — Python 3 / PyPy template (fast I/O, imports, recursion limit)

### Data Structures
- [`dsu.cpp`](./dsu.cpp) — Disjoint Set Union (path compression + union by rank)
- [`bit.cpp`](./bit.cpp) — Fenwick Tree (point update, range sum)
- [`segment-tree.cpp`](./segment-tree.cpp) — Recursive + iterative (generic, any associative op)
- [`segment-tree-lazy.cpp`](./segment-tree-lazy.cpp) — Lazy propagation (range update + range query)
- [`sparse-table.cpp`](./sparse-table.cpp) — O(1) RMQ (idempotent ops)
- [`trie.cpp`](./trie.cpp) — Trie (insert/search/prefix) + binary trie (XOR maximization)
- [`heap.cpp`](./heap.cpp) — Indexed priority queue (with decrease-key)
- [`hash-table.cpp`](./hash-table.cpp) — Custom hash (anti-hack) + pair hash

### Algorithms
- [`graph-algorithms.cpp`](./graph-algorithms.cpp) — BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal, Prim, topological sort
- [`string-algorithms.cpp`](./string-algorithms.cpp) — KMP, Z-function, polynomial hashing, Manacher
- [`number-theory.cpp`](./number-theory.cpp) — gcd, extended Euclidean, modPow, modInv, sieve, linear sieve, Euler totient, Miller-Rabin, combinatorics (nCr mod p)

### Utilities
- [`stress-test-runner.sh`](./stress-test-runner.sh) — automated brute-vs-solution comparison harness

---

## 🧭 HOW TO USE
1. **Study** each template — understand HOW it works (don't copy blindly).
2. **Adapt** to your coding style (naming, comments).
3. **Test** every component (stress-test against brute force).
4. **Memorize** the interfaces (know how to call under pressure).
5. **Build your own library** incrementally as you learn.

---

## 🏗️ TEMPLATES TO ADD AS YOU ADVANCE
As you reach higher levels, extend your library with: lazy segtree variants, persistent segtree, treap, HLD, centroid decomposition, Dinic's max flow, FFT/NTT, suffix array, suffix automaton, LCA (binary lifting), Li Chao tree, convex hull trick.

(Full implementations and study order: see [`../12-COMPETITIVE-PROGRAMMING-UNIVERSE/11-Template-Engineering.md`](../12-COMPETITIVE-PROGRAMMING-UNIVERSE/11-Template-Engineering.md))

---

## 📦 REFERENCE LIBRARIES
- **[KACTL](https://github.com/kth-competitive-programming/kactl)** ⭐ (KTH) — the gold standard, ICPC-ready
- **[AtCoder Library (ACL)](https://github.com/atcoder/ac-library)** — official, well-tested
- See [`../20-RESOURCES-AND-REFERENCES/09-Code-Libraries-CP.md`](../20-RESOURCES-AND-REFERENCES/09-Code-Libraries-CP.md)

---

## ⚠️ THE RULE
A template speeds up IMPLEMENTATION, not THINKING. Master the ideas first; let the template handle the typing.
