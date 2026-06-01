# 🏛️ Data Structures Universe

> *"Data structures are not containers. They are *witnesses* of invariants."*

The complete kingdom of data structures, from `int x = 5` to Link-Cut Trees. For each: internal mechanics, memory layout, complexity, implementations, applications, interview & contest usage.

---

## 📚 Contents

> **📖 About the numbering:** Every data structure in this universe has a fixed catalog number (01–53, see the full list at the bottom). The **4 deep-dive files** keep their catalog number (`01-Arrays`, `07-Hash-Tables`, `26-Segment-Tree`, `32-Disjoint-Set-Union`) — these are the most interview/contest-critical structures, given full standalone treatment. **Every other number is covered inside one of the 4 compendiums** (e.g., 02–06 in Linear-Structures, 10–18 in Trees, 19–31 in Heaps-And-Range, 33–53 in Advanced-DS). So there are no "missing" files — the gaps in the deep-dive numbers are intentional; those structures live in the compendiums.

### Deep Dives (full standalone files)
1. [`01-Arrays.md`](./01-Arrays.md) — The atomic data structure (static/dynamic, amortized, cache, patterns, 30 problems) ⭐
2. [`07-Hash-Tables.md`](./07-Hash-Tables.md) — Internals, collisions, anti-hash, from-scratch implementation ⭐
3. [`26-Segment-Tree.md`](./26-Segment-Tree.md) — Recursive + iterative, aggregation, extensions ⭐
4. [`32-Disjoint-Set-Union.md`](./32-Disjoint-Set-Union.md) — Union-Find with all variants ⭐

### The Four Compendiums ⭐
Comprehensive coverage of every remaining structure:

- **[`COMPENDIUM-Linear-Structures.md`](./COMPENDIUM-Linear-Structures.md)** — Strings, Linked Lists, Stacks (+ monotonic), Queues, Deques (+ monotonic)
- **[`COMPENDIUM-Trees.md`](./COMPENDIUM-Trees.md)** — Binary Trees, BST, AVL, Red-Black, B-Trees, Splay, Treap, Trie, Suffix Tree
- **[`COMPENDIUM-Heaps-And-Range.md`](./COMPENDIUM-Heaps-And-Range.md)** — Binary/Fibonacci/Pairing Heaps, Indexed PQ, Prefix Sums, Difference Arrays, Sparse Table, BIT, Segment Tree family, Merge Sort Tree, Wavelet Tree
- **[`COMPENDIUM-Advanced-DS.md`](./COMPENDIUM-Advanced-DS.md)** — KD-Tree, Quadtree, R-Tree, Skip List, Rope, Link-Cut Tree, Euler Tour Tree, Top Trees, Li Chao Tree, vEB, Fusion Tree, Y-Fast Trie, Count-Min Sketch, HyperLogLog, MinHash/LSH, Reservoir Sampling, Suffix Array, Suffix Automaton, Aho-Corasick, Palindromic Tree

### Templates
- [`../19-TEMPLATES-AND-IMPLEMENTATIONS/`](../19-TEMPLATES-AND-IMPLEMENTATIONS/) — dsu, bit, segment-tree, segment-tree-lazy, sparse-table, trie, heap, hash-table

---

## 🧭 Recommended Learning Order

### Beginner (Level 0-2)
Arrays → Strings → Linked Lists → Stacks → Queues → Hash Tables → Binary Trees → BSTs → Binary Heap → Trie → DSU

### Intermediate (Level 3-5)
Prefix sums → Sparse Table → BIT → Segment Tree → Lazy Segtree → Treap → AVL/RB

### Advanced (Level 6-7)
Persistent Segtree → Segment Tree Beats → HLD → Centroid Decomp → Treap (implicit) → Suffix Array → Suffix Automaton → Aho-Corasick → KD-Tree

### Elite (Level 8+)
Link-Cut → Top Trees → Euler Tour Tree → vEB → Fusion → Y-Fast → Wavelet → Li Chao

---

## 📊 THE COMPLETE STRUCTURE LIST (53 structures)
All covered across the 4 deep dives + 4 compendiums:

**Linear**: Arrays, Strings, Linked Lists, Stacks, Queues, Deques
**Hash-based**: Hash Tables, Bloom Filter, Cuckoo Hashing
**Trees**: Binary Trees, BST, AVL, Red-Black, B-Trees, Splay, Treap, Trie, Suffix Tree
**Heaps**: Binary, Fibonacci, Pairing, Indexed PQ
**Range query**: Prefix Sum, Difference Array, Sparse Table, BIT, Segment Tree, Lazy Segtree, Persistent Segtree, Segment Tree Beats, Merge Sort Tree, Wavelet Tree
**Disjoint set**: DSU (+ rollback, weighted, persistent, small-to-large)
**Spatial**: KD-Tree, Quadtree, R-Tree, BVH
**Advanced**: Skip List, Rope, Link-Cut Tree, Euler Tour Tree, Top Trees, Li Chao Tree, vEB, Fusion Tree, Y-Fast Trie
**Streaming/probabilistic**: Count-Min Sketch, HyperLogLog, MinHash/LSH, Reservoir Sampling
**String-specialized**: Suffix Array, Suffix Automaton, Aho-Corasick, Palindromic Tree

---

## 📌 DEEP REFERENCE
- **[MIT 6.851](https://courses.csail.mit.edu/6.851/) Advanced Data Structures** (Erik Demaine) ⭐
- **CLRS** Chapters 6, 10-14, 18, 21
- **[CP-Algorithms.com](https://cp-algorithms.com)**
