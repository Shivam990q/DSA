# 🪜 Abstraction & Decomposition — The Two Superpowers

> *"Abstraction is the ladder. Decomposition is the saw."*

---

## I. ABSTRACTION

**Definition**: hiding implementation details behind a cleaner interface.

### Levels of abstraction in software
1. Physics (electrons, atoms)
2. Transistors
3. Logic gates
4. CPU architecture
5. Machine code
6. Assembly
7. C / system languages
8. High-level languages (Python, Java)
9. Frameworks / libraries
10. Domain models (e.g., Stripe API)

Each layer **abstracts** the layer below. You write Python without thinking about transistors. The cost: lost control. The benefit: massive productivity.

### Abstraction in algorithms
- A `set` abstracts the implementation (hash table or balanced BST). You just need: insert, find, delete, in O(log n) or O(1).
- A `priority_queue` abstracts heap. You just need: push, top, pop.
- A `Graph` interface abstracts adjacency list / matrix.

**Implication**: code against interfaces, not implementations. Switch implementations easily.

---

## II. THE LEAKY ABSTRACTION

> *"All non-trivial abstractions, to some degree, are leaky."* — Joel Spolsky

A `set` *says* O(log n) — but if you fill it with strings of length 10⁶, each comparison is O(10⁶), and your "log n" is misleading.

**Lesson**: know what's underneath your abstractions, especially for performance.

---

## III. DECOMPOSITION

**Definition**: breaking a problem (or system) into smaller, independent parts.

### Top-down decomposition
Start with the goal. Break into subgoals. Each subgoal is solved by a function/module.

```
Build a chess engine
├── Board representation
├── Move generation
│   ├── Sliding pieces
│   ├── Knights
│   ├── Pawns (with en passant, promotion)
│   └── Castling
├── Position evaluation
├── Search (minimax + alpha-beta)
└── Time management
```

### Bottom-up decomposition
Start with primitives. Build composites.

```
Bytes → Bitboards → Move generators → Position → Engine
```

### Modular decomposition
Each module:
- Has a clear responsibility (single-responsibility principle)
- Has a minimal interface
- Hides implementation
- Can be tested independently
- Can be replaced/improved

---

## IV. THE THREE QUESTIONS OF DECOMPOSITION

For any complex task:

1. **What are the major parts?**
2. **How do they communicate?** (interfaces)
3. **What's the dependency order?** (DAG)

---

## V. DECOMPOSITION IN ALGORITHMS

### Divide-and-conquer (D&C)
Recursively split into halves. Solve each. Combine.

> Merge sort: split into halves → recursively sort → merge.

### Dynamic programming (DP)
Decompose into overlapping subproblems. Solve each once. Cache.

> LIS: `dp[i]` = longest increasing subsequence ending at i.

### Reduction
Decompose by transforming the problem into a known one.

> "Find a Hamiltonian path" → reduce to "find a Hamiltonian cycle in modified graph."

### Layering
Solve simpler version first, then layer in complexity.

> First, solve TSP for small n with brute force. Then add bitmask DP. Then add Held-Karp optimization.

---

## VI. EXAMPLE: DECOMPOSING "TWO SUM"

**Problem**: given array, find two indices that sum to target.

**Decomposition**:
1. **Sub-problem 1**: for each i, find j > i such that a[i] + a[j] = target.
2. **Reformulation**: for each i, find j such that a[j] = target - a[i].
3. **Sub-problem**: "find a value in an array" → use hash map.
4. **Optimization**: build hash map as we go (one pass).

→ O(n) algorithm.

---

## VII. EXAMPLE: DECOMPOSING "DESIGN URL SHORTENER"

**Sub-systems**:
1. ID generation (sequential? hash? Snowflake?)
2. Storage (key-value: short → long)
3. Reverse storage (long → short, for de-dup)
4. Cache (popular URLs)
5. Analytics (count clicks)
6. Custom URLs / collisions
7. API layer (REST endpoints)
8. Rate limiting

Each is a self-contained module with a clear interface.

---

## VIII. ABSTRACTIONS IN DSA — KEY EXAMPLES

| Abstract concept    | Concrete data structure                   |
|---------------------|-------------------------------------------|
| Stack               | Array, linked list                        |
| Queue               | Circular array, linked list, deque        |
| Set                 | Hash set, balanced BST, bitset           |
| Map                 | Hash map, balanced BST                    |
| Priority Queue      | Binary heap, Fibonacci heap, pairing heap |
| Graph               | Adjacency list, matrix, edge list         |
| Sequence            | Array, linked list, rope                  |
| Range query DS      | Segment tree, BIT, sparse table          |

**Choose abstraction first, implementation second.** This guides clear thinking.

---

## IX. SIGNS OF BAD DECOMPOSITION

- One module knows about every other (god class)
- Changing one module forces changes in many others (tight coupling)
- A module has multiple unrelated responsibilities
- Dependencies form cycles (instead of DAG)
- Names are vague or misleading

---

## X. THE FINAL TRUTH

> **"Abstraction is what you remove. Decomposition is how you organize what's left.  
>  Together they let one mind comprehend something a thousand times its size."**

---

**→ Next:** [`10-Compilation-and-Execution.md`](./10-Compilation-and-Execution.md)
