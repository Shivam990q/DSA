# 🔍 Discovering Invariants

> *"To invent an algorithm, find what must stay true. Build the algorithm around protecting it."*

---

## I. INVARIANTS AS DESIGN PRIMITIVES

When inventing an algorithm, the invariant comes FIRST, the code SECOND.

> "I want to maintain: the heap property (parent ≥ children). Now what operations preserve it?"
> → That question *generates* the heap's push/pop logic.

The invariant is the *specification*; the operations are the *implementation* that protects it.

---

## II. THE INVARIANT-FIRST DESIGN METHOD

1. **State the goal** as a property to maintain.
2. **Express it as an invariant** (something true at every step).
3. **Design operations** that preserve the invariant.
4. **Prove** each operation preserves it.
5. **Derive** the answer from the invariant at termination.

---

## III. WORKED EXAMPLE: INVENTING BINARY SEARCH

**Goal**: find target in sorted array.

**Invariant**: "If target exists, it lies in [lo, hi]."

**Operations that preserve it**:
- Compute mid.
- If a[mid] < target: target can't be in [lo, mid] → set lo = mid+1. (Invariant preserved.)
- If a[mid] > target: target can't be in [mid, hi] → set hi = mid-1.
- If a[mid] == target: found.

**Termination**: when lo > hi, the interval is empty → target absent.

The invariant *generated* the algorithm.

---

## IV. WORKED EXAMPLE: INVENTING THE HEAP

**Goal**: O(log n) insert + extract-min.

**Invariant**: "Every parent ≤ its children (min-heap), tree is complete."

**Operations**:
- Insert: append at end (preserves completeness), bubble up (restores parent ≤ child).
- Extract: swap root with last, remove last, bubble down (restores property).

Both operations are *forced* by the need to restore the invariant. The invariant is the design.

---

## V. TYPES OF INVARIANTS IN ALGORITHM DESIGN

### 1. Order invariants
"This sequence is sorted." (insertion sort, BST in-order)

### 2. Balance invariants
"Height difference ≤ 1." (AVL); "no red-red edges." (RB tree)

### 3. Boundary invariants
"All elements ≤ pivot are left of index i." (quicksort partition)

### 4. Reachability invariants
"All nodes in the queue are at distance d or d+1." (BFS)

### 5. Counting invariants
"The sum of weights is preserved." (network flow conservation)

### 6. Monotonicity invariants
"The stack is strictly decreasing." (monotonic stack)

---

## VI. THE INVARIANT-DISCOVERY QUESTIONS

When designing, ask:

1. **What property, if maintained, would make the answer trivial to read off?**
2. **What's the cheapest invariant to maintain?**
3. **Which operations could violate it? How do I repair?**
4. **What's true at the very start? At the very end?**

---

## VII. INVARIANTS FOR CORRECTNESS PROOFS

Every correct loop/algorithm HAS an invariant — whether the author stated it or not.

To prove correctness:
1. State the invariant.
2. Prove it holds initially (initialization).
3. Prove each step preserves it (maintenance).
4. Show invariant + termination condition ⟹ correct output (conclusion).

If you can't find the invariant, you don't fully understand why your code works.

---

## VIII. EXERCISES

For each, state the maintaining invariant:

1. Two pointers for pair-sum in sorted array.
2. Sliding window for longest valid substring.
3. Dijkstra's main loop.
4. Kadane's algorithm.
5. The partition step of quicksort.
6. Union-Find with path compression.

---

**→ Next:** [`05-The-Inventor-Mindset.md`](./05-The-Inventor-Mindset.md)
