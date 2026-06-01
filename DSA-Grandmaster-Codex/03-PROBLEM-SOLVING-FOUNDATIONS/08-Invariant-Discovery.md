# ⚖️ Invariant Discovery — What Never Changes is What Guides You

> *"What stays the same under transformation is what shapes truth."*

---

## I. WHAT IS AN INVARIANT?

An **invariant** is a property that **stays the same** as the system evolves (under operations, iterations, or recursion).

Invariants are how we:
- Prove correctness (loop invariants)
- Recognize impossibility (parity arguments)
- Speed up solutions (memoize on the invariant)

---

## II. TYPES OF INVARIANTS

### 1. **Conservation**
Some sum/count is preserved.

> Example: parity of inversions in a permutation is preserved by allowed swaps that swap two equal elements (vacuous), or 3-cycles.

### 2. **Relations**
Two quantities maintain a relation.

> Example: in BST, every node's left subtree values ≤ node ≤ right subtree values.

### 3. **Bounds**
Some quantity stays within a range.

> Example: in heap, parent ≥ children always.

### 4. **Structural**
Shape/configuration property holds.

> Example: AVL tree balance factor ≤ 1.

### 5. **Algebraic**
Some equation always holds.

> Example: in Floyd's tortoise-and-hare cycle detection, when slow meets fast, both are at distance L from the cycle start where L equals... (proven via algebra).

---

## III. THE INVARIANT HUNT (in problem solving)

### Step 1: Identify the operations
What are the allowed transformations?

### Step 2: Check what each operation preserves
Does sum stay same? Parity? GCD? Set membership?

### Step 3: Check what each operation changes (predictably)
Does each op change sum by exactly k? Each op flip parity?

### Step 4: Use invariant to:
- Prove impossibility ("can never reach target — invariant differs")
- Reduce state space ("group equivalent states by invariant")
- Solve the problem ("compute the invariant directly")

---

## IV. FAMOUS INVARIANT EXAMPLES

### 8-puzzle
**Operation**: slide a tile into the empty square.
**Invariant**: parity of (permutation parity + Manhattan distance of empty from corner).
**Implication**: half of all configurations are unreachable from any start.

### Lights Out
**Operation**: toggle a 5-cross of cells.
**Invariant**: certain XOR sums of configurations.
**Implication**: only some target configurations are reachable.

### Coin flipping
**Operation**: flip exactly two coins simultaneously.
**Invariant**: parity of #heads.
**Implication**: can reach config X iff parity matches.

### Heap
**Operation**: push, pop.
**Invariant**: parent ≥ children (max-heap).
**Implication**: top always max → O(1) peek.

### BST
**Operation**: insert, delete.
**Invariant** (after careful operations): in-order traversal yields sorted.
**Implication**: search/insert in O(h).

### Loop invariants (for correctness proofs)
**Example**: binary search loop invariant: target, if exists, is in [lo, hi].

```cpp
int lo = 0, hi = n - 1;
// Invariant: if target exists in arr, then arr[lo..hi] contains it.
while (lo <= hi) {
    int mid = (lo + hi) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target) lo = mid + 1;  // target is in [mid+1..hi]
    else hi = mid - 1;                     // target is in [lo..mid-1]
}
return -1;
// On exit: invariant violated (lo > hi) or target found.
```

---

## V. INVARIANT-DRIVEN SOLUTIONS

### Example 1: Parity argument
> Problem: a chessboard with two opposite corners removed. Can it be tiled by 1×2 dominoes?
> 
> **Invariant**: each domino covers one black + one white square.
> **Observation**: the two opposite corners are the same color.
> **Implication**: 30 black + 32 white. Can't tile.

### Example 2: Sum invariant
> Problem: array of integers; can repeatedly merge two adjacent into their sum, or split a number into two parts. Can we transform array A into array B?
> 
> **Invariant**: total sum of array.
> **Implication**: A and B must have the same total sum.

### Example 3: GCD invariant
> Problem: array of positive integers; in one operation, replace any two with their difference. After enough ops, what's the smallest possible element?
> 
> **Invariant**: GCD of all elements.
> **Implication**: smallest reachable element is GCD.

### Example 4: XOR invariant
> Problem: a Nim-like game with multiple piles. Can the second player win?
> 
> **Invariant**: XOR of pile sizes (Sprague-Grundy).
> **Implication**: second player wins iff XOR is 0 at start.

---

## VI. LOOP INVARIANT — THE CORRECTNESS TOOL

For any loop, write:
```
// LOOP INVARIANT: <statement that is true at the start of each iteration>
while (...) {
    ...
}
// After loop: invariant + loop exit condition together imply correctness
```

**The 4 things you must prove for a loop invariant:**
1. **Initialization**: invariant holds before the loop starts.
2. **Maintenance**: each iteration preserves the invariant.
3. **Termination**: the loop ends.
4. **Conclusion**: at termination, the invariant + exit condition imply correctness.

This is **how textbooks prove algorithms correct.** Don't just write code — write invariants.

---

## VII. EXERCISES

For each, identify the invariant:

1. Tower of Hanoi (n disks): what's preserved across allowed moves?
2. Bubble sort: after pass i, what's true about the rightmost i elements?
3. Quicksort partition: at iteration j, what regions of the array exist?
4. Building a heap (heapify-down): what's true at each step?
5. DFS: what does the "white/gray/black" coloring satisfy at each step?
6. Two pointers (sorted array, pair sum): what's true about a[l..r] relative to target?

---

## VIII. INVARIANT-FIRST PROBLEM SOLVING

When stuck:

1. **Try operations on small examples**.
2. **Note quantities** that don't change. Note quantities that change predictably.
3. **Identify the invariant**.
4. **Use it**: either as a proof technique or as a direct solution method.

> Many "is X possible" problems are settled by computing invariants of source and target — if they differ, NO; if equal, YES (often).

---

## IX. THE FINAL TRUTH

> **"Invariants are the soul of an algorithm.  
>  Any code that is correct has an invariant.  
>  Discover it, and you understand the code.  
>  Hide it, and you wrote a riddle for your future self."**

---

**→ Next:** [`09-Proof-Construction.md`](./09-Proof-Construction.md)
