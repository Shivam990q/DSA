# 🌌 Advanced & Exotic Data Structures Compendium

> Compact reference for: KD-Tree, Quadtree, R-Tree, Skip List, Rope, Link-Cut Tree, Euler Tour Tree, Top Trees, Li Chao, vEB, Fusion, Y-Fast, Count-Min, HyperLogLog, MinHash/LSH, Reservoir, Suffix Array, Suffix Automaton, Aho-Corasick, Palindromic Tree.

---

## 33 — KD-TREE (k-Dimensional Tree)

### Concept
Binary tree where each level alternates which dimension to split on (cycle through k dims).

### Operations
- Build: O(n log n)
- Range search: O(n^(1-1/k) + r) where r = result count
- Nearest neighbor: O(log n) average; O(n) worst-case

### Use cases
- Spatial nearest-neighbor queries
- Range searches in low dimensions (k ≤ ~20; bad for high d due to "curse of dimensionality")
- Game development (collision queries)

---

## 34 — QUADTREE

### Concept
2D recursive subdivision: each node has 4 children (NW, NE, SW, SE quadrants).

### Use cases
- 2D image compression (sparse representation)
- 2D collision detection
- Game maps / GIS

---

## 35 — R-TREE

### Concept
Tree of bounding boxes. Each node = MBR (minimum bounding rectangle) of its children.

### Use cases
- Spatial DB indexing (PostGIS, Oracle Spatial)
- 2D/3D range queries
- "Find all points within rectangle"

---

## 36 — BVH (Bounding Volume Hierarchy)

### Concept
A tree of nested **bounding volumes** (usually axis-aligned boxes, AABBs). Each leaf wraps one object; each internal node's box encloses all its children's boxes. Closely related to the R-Tree, but tuned for ray/collision queries rather than database paging.

### Operations
- Build: O(n log n) (top-down split by longest axis / surface-area heuristic).
- Ray / collision query: O(log n) average — descend only into boxes the ray (or query object) actually hits, pruning whole subtrees.

### Use cases
- **Ray tracing / rendering** (the dominant acceleration structure in graphics).
- **Physics engines** — broad-phase collision detection.
- **Games** — frustum culling, picking.

### vs KD-Tree / R-Tree
- **KD-Tree**: splits space by planes; great for point nearest-neighbor.
- **R-Tree**: balanced, disk-oriented, database indexing.
- **BVH**: object-centric boxes, rebuilt/refit per frame; best for moving objects in 3D.

---

## 37 — SKIP LIST

### Concept
Linked list with multiple "express" levels. Each node has a tower of forward pointers, with probability 1/2 of going up to next level.

### Performance
- Search: O(log n) expected
- Insert/Delete: O(log n) expected
- Range queries: O(log n + k)

### Why
- Concurrent variants are simpler than concurrent BSTs
- Used in Redis sorted sets, LevelDB MemTable

---

## 38 — ROPE

### Concept
Tree of small string fragments. Concatenation: O(1). Substring/insert/delete in middle: O(log n).

### Use cases
- Text editors (vim, emacs)
- Versioned strings

---

## 39 — LINK-CUT TREE

### Concept
Splay tree-based structure for **dynamic forest**. Operations:
- `link(u, v)`: connect u (root of its tree) to v
- `cut(u)`: disconnect u from its parent
- `findRoot(u)`: which tree is u in?
- `pathOp(u, v)`: aggregate over u-to-v path

All O(log n) amortized.

### Use cases
- Dynamic MST (online edge insertions/deletions)
- Maximum flow (Dinic with LCT acceleration)
- Online 2-edge-connected components

---

## 40 — EULER TOUR TREE

### Concept
Maintain Euler tour of a tree as a balanced BST keyed by tour position. Allows dynamic forest connectivity.

### Use cases
- Holm-Lichtenberg-Thorup decremental connectivity
- Dynamic graph problems

---

## 41 — TOP TREES

### Concept
Hierarchical decomposition of a tree, supporting more complex queries (e.g., diameter, center) on dynamic forests in O(log n).

### Use cases
- Advanced research-level dynamic tree problems

---

## 42 — LI CHAO TREE

### Concept
Segment tree where each node stores a **line** (or arbitrary function). Supports:
- Insert line: O(log n) amortized
- Query "minimum y at x": O(log n)

### Use cases
- DP optimization where transitions are linear in i: `dp[i] = min over j: m_j × i + b_j`
- Convex hull trick generalization (allows non-monotonic insertions/queries)

---

## 43 — VAN EMDE BOAS TREE

### Concept
Recursive structure on integer keys in [0, U). Operations in O(log log U).

### Memory
O(U) — unfortunately big.

### Use cases
- Theoretical efficiency on small integer keys
- Rarely used in practice (Y-Fast Trie is more memory-efficient)

---

## 44 — FUSION TREE

### Concept
Word-RAM tree exploiting machine-word parallelism for O(log_w n) operations on integer keys (w = word size, e.g., 64).

### Theoretical
With w = log² n, fusion tree achieves O(log n / log log n) per op.

### Use cases
Theoretical / research. Rarely implemented.

---

## 45 — Y-FAST TRIE

### Concept
Combines:
- An x-fast trie (binary trie with hash table per level) for O(log log U) predecessor
- Balanced BSTs in leaves for O(log log U) update

### Performance
- Predecessor: O(log log U)
- Insert/Delete: O(log log U) amortized

### Use cases
Theoretical; predecessor problem on integers.

---

## 46 — COUNT-MIN SKETCH

### Concept
Probabilistic frequency counter. d hash functions × w columns; insert(x) increments d cells; query(x) takes min of d cells.

### Performance
- Insert / Query: O(d) (d ≈ log(1/δ))
- Memory: O(w · d)
- Error: count(x) ≤ true_count(x) + ε · n with probability ≥ 1 − δ

### Use cases
- Heavy hitters in streams
- Network packet counting
- Real-time analytics

---

## 47 — HYPERLOGLOG

### Concept
Probabilistic cardinality estimator. Hash items, track max trailing-zeros pattern, estimate via formula.

### Performance
- Memory: ~12-16 KB for billions of items
- Error: ~2% relative

### Use cases
- "How many unique users today?" (Reddit, Stripe, etc.)
- Database query planning

---

## 48 — MINHASH + LSH

### MinHash
Estimate Jaccard similarity of two sets via m random hash functions; signature = min hash for each function. Estimated similarity = fraction of signatures matching.

### LSH (Locality-Sensitive Hashing)
Hash similar items to same bucket with high probability; dissimilar items to different buckets.

### Use cases
- Near-duplicate detection (web pages, images)
- Clustering big data
- Recommendation (item similarity)

---

## 49 — RESERVOIR SAMPLING

### Concept
Sample k items uniformly at random from a stream of unknown size n.

### Algorithm (k=1):
For i-th element of stream, replace current sample with it with probability 1/i.

### Algorithm (k=R):
Keep first R. For i-th (i > R), replace random one with probability R/i.

### Use case
- Sampling from infinite stream
- A/B test bucketing

---

## 50 — SUFFIX ARRAY

### Concept
Sorted array of all suffix start indices.

### Construction
- Naive: O(n² log n)
- DC3: O(n)
- SA-IS: O(n) (used in libraries)
- O(n log² n) sort-based (popular in CP)

### LCP array
Longest common prefix between adjacent suffixes in SA. Constructible in O(n) given SA (Kasai's).

### Use cases
- Substring queries
- Distinct substrings count: n(n+1)/2 − Σ LCP[i]
- Longest repeated substring: max(LCP)
- Pattern matching: binary search

---

## 51 — SUFFIX AUTOMATON

### Concept
Minimal DFA accepting all substrings of a string. Built online in O(n).

### Use cases
- Number of distinct substrings: sum (len[v] − len[link[v]]) over all states
- K-th lexicographic substring
- Substring occurrence counting
- Longest common substring of two strings (build on s, walk on t)

---

## 52 — AHO-CORASICK

### Concept
Trie + KMP-like failure links. Supports multiple-pattern matching in O(|T| + |P| + #matches).

### Use cases
- Spell-check / dictionary search
- Network intrusion detection (multiple signatures)
- Word puzzles (find all words from dictionary in text)

---

## 53 — PALINDROMIC TREE (EERTREE)

### Concept
Each node represents a distinct palindromic substring. Built in O(n) with O(n) distinct palindromes.

### Use cases
- Count distinct palindromic substrings
- Number of palindromic occurrences
- Palindrome partitioning DP variants

---

## 🧭 LEARNING PATH FOR ADVANCED DS

| Order | Structure          | Difficulty | Level |
|-------|--------------------|-----------|-------|
| 1     | Sparse Table       | Medium    | 4     |
| 2     | BIT                | Medium    | 4     |
| 3     | Segment Tree       | Medium-Hard | 4    |
| 4     | Lazy Segtree       | Hard      | 5     |
| 5     | Treap              | Hard      | 6     |
| 6     | Persistent Segtree | Hard      | 7     |
| 7     | HLD                | Hard      | 7     |
| 8     | Centroid Decomp    | Hard      | 7     |
| 9     | Suffix Array       | Hard      | 7     |
| 10    | Suffix Automaton   | Very Hard | 7     |
| 11    | Link-Cut Tree      | Very Hard | 8     |
| 12    | Top Trees          | Research  | 9     |

---

**→ Next universe:** [`../05-ALGORITHMS-UNIVERSE/00-Index.md`](../05-ALGORITHMS-UNIVERSE/00-Index.md)
