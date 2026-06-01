# 🔬 The Doctrine of First Principles

> *"To memorize is to borrow. To derive is to own."*

---

## I. WHAT FIRST-PRINCIPLES THINKING IS

First-principles thinking means: **breaking knowledge down to atomic, undeniable truths and rebuilding from those atoms.**

For DSA, the atoms are:
- **Counting** (cardinality, combinatorics)
- **Comparison** (ordering, equality)
- **Movement** (state transitions)
- **Memory** (storage, lookup)
- **Recursion** (self-similarity)
- **Invariants** (things that don't change)

Every algorithm is a *composition* of these atoms. When you see "binary search," you should not see "binary search." You should see: *bisecting a monotonic predicate using comparison and movement to converge in O(log n) memory accesses.*

---

## II. WHY MOST PEOPLE NEVER ESCAPE MEMORIZATION

Most students learn: **"Use Dijkstra for shortest path with non-negative weights."**

A first-principles thinker derives:
1. We want minimum-cost paths from a source.
2. **Greedy choice property**: if all weights ≥ 0, the closest unvisited node's distance is final (no shorter path can reach it via a longer detour).
3. We need to repeatedly find the closest unvisited node → **priority queue**.
4. When we finalize a node, its neighbors get *relaxed* (try the new path).
5. → This *is* Dijkstra. We just *invented* it.

**The memorizer fails when the problem disguises Dijkstra.** The first-principles thinker re-derives in any disguise.

---

## III. THE FIVE QUESTIONS OF FIRST PRINCIPLES

For any algorithm or data structure you encounter, ask:

### Q1: **WHAT problem does it solve?** (the *purpose*)
What's the input? Output? Constraints? Why does this matter?

### Q2: **WHY does it work?** (the *correctness*)
What invariant does it maintain? What's the inductive proof? What's the loop invariant?

### Q3: **HOW is it constructed?** (the *mechanism*)
Step by step, what does it do? What are the data structure mutations?

### Q4: **WHEN does it fail?** (the *limits*)
Edge cases. Adversarial inputs. Where does the analysis break?

### Q5: **WHAT could replace it?** (the *alternatives*)
What other algorithms solve this? What are the tradeoffs?

If you cannot answer all 5, you have not understood — you have memorized.

---

## IV. THE ATOMIC TRUTHS OF DSA

These are the **non-negotiable axioms** from which everything else is derived:

### 🧱 Atom 1: Comparison-based sorting has a Ω(n log n) lower bound.
**Proof sketch**: There are n! permutations. A decision tree distinguishing them has height ≥ log₂(n!) = Ω(n log n).
**Implication**: No comparison sort can beat n log n. Period.

### 🧱 Atom 2: Hashing achieves O(1) expected, O(n) worst-case.
**Why**: Pigeonhole guarantees collisions. Adversary can force them. Randomization breaks adversary's predictions.

### 🧱 Atom 3: A balanced binary tree of n nodes has height ⌈log₂(n+1)⌉.
**Why**: A tree with height h has at most 2^(h+1)-1 nodes. Solve for h.

### 🧱 Atom 4: BFS finds shortest paths in unweighted graphs.
**Why**: Layer-by-layer expansion guarantees first time we reach v is via shortest path.

### 🧱 Atom 5: DP is just memoized recursion + topological order.
**Why**: Overlapping subproblems → memoize. Acyclic dependency → fill in order.

### 🧱 Atom 6: Greedy works iff the problem has the *exchange property* OR matroid structure.
**Why**: If swapping any element of the optimal with greedy's choice doesn't worsen, greedy = optimal.

### 🧱 Atom 7: Two pointers / sliding window works iff the predicate is *monotonic* in window size.
**Why**: Monotonicity = once invalid, always invalid → can advance left without missing answers.

### 🧱 Atom 8: Divide & conquer: T(n) = aT(n/b) + f(n) → Master Theorem.
**Why**: Recursion tree has log_b(n) levels, level i has a^i nodes of size n/b^i.

---

## V. THE METHOD OF DERIVATION

When facing a new algorithm, derive it as follows:

```
Step 1: STATE THE PROBLEM mathematically (no English ambiguity)
Step 2: ATTEMPT brute force. State its complexity.
Step 3: IDENTIFY the bottleneck (which step is expensive? which work is repeated?)
Step 4: PROPOSE an invariant that, if maintained, removes the bottleneck.
Step 5: DESIGN a data structure that maintains that invariant cheaply.
Step 6: PROVE correctness (induction or contradiction).
Step 7: ANALYZE complexity (amortized if needed).
Step 8: STRESS TEST against brute force.
```

This is the **scientific method for algorithm design**. It is how Dijkstra, Tarjan, Knuth, and Tarjan all worked.

---

## VI. EXAMPLE DERIVATION: KMP from First Principles

**Problem**: Find pattern P of length m in text T of length n.

**Step 1 (Brute force)**: For each i in T, compare P[0..m-1] with T[i..i+m-1]. O(nm).

**Step 3 (Bottleneck)**: When mismatch occurs at P[j], we *throw away* all the matching we did for P[0..j-1]. That's wasteful.

**Step 4 (Invariant)**: When mismatch occurs at P[j] vs T[i], we know:
> The last j characters of T (i.e., T[i-j..i-1]) equal P[0..j-1].

So instead of going back in T, we ask: **what is the longest proper prefix of P[0..j-1] that is also a suffix?** Call it `fail[j]`. Then we can shift P to align this prefix with the matched suffix in T — *without re-examining T*.

**Step 5 (Data structure)**: Precompute `fail[]` array (failure function) in O(m). Use it during scan.

**Step 6 (Proof)**: By the invariant + the definition of `fail[]`, no match is missed: any shift smaller than `j - fail[j]` would require a longer prefix-suffix match in P[0..j-1] than `fail[j]` — contradiction.

**Step 7 (Complexity)**: Each character of T is "examined" at most twice (advanced or backtracked-via-fail). Total O(n+m).

**Congratulations. You just derived KMP.** No memorization required. Forever.

---

## VII. THE FIRST-PRINCIPLES TEST

Before claiming you "know" any algorithm, pass this test:

1. ✅ Can you state the problem in 1 sentence?
2. ✅ Can you write the brute force in 5 minutes?
3. ✅ Can you identify the bottleneck?
4. ✅ Can you state the key invariant?
5. ✅ Can you prove correctness in 3 sentences?
6. ✅ Can you derive complexity?
7. ✅ Can you implement it in <20 minutes from scratch?
8. ✅ Can you teach it to a smart 16-year-old in 15 minutes?

If yes → **you own it**. If no → **you rent it**.

---

## VIII. THE LAW

> **You will never derive what you have only memorized.  
> You will always re-derive what you have once derived.**

---

**→ Next:** [`03-The-Grandmaster-Code.md`](./03-The-Grandmaster-Code.md)
