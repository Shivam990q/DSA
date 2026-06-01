# 📐 Proof Construction — Conviction without Doubt

> *"To submit code is to claim it is correct. Without proof, you are gambling."*

---

## I. WHY PROVE?

Without proof:
- You don't know if your greedy works.
- You don't know if your DP transition is exhaustive.
- You don't know if your "invariant" actually holds.
- You submit, fail, blame the judge. (It's never the judge.)

With proof: you submit with calm certainty. Your time isn't spent debugging — it's spent thinking.

---

## II. PROOF TECHNIQUES (THE CORE FIVE)

### 1. **Direct Proof**
Assume hypothesis. Apply known facts. Derive conclusion.

> Theorem: if n is even, n² is even.
> Proof: n = 2k for some integer k. Then n² = 4k² = 2(2k²), which is even. □

### 2. **Proof by Contradiction**
Assume the negation. Derive a contradiction.

> Theorem: √2 is irrational.
> Proof: Assume √2 = p/q in lowest terms. Then 2q² = p². So p² is even, p is even, p = 2k. Then 2q² = 4k², q² = 2k², so q is even. But then p, q are both even — contradicts "lowest terms." □

### 3. **Proof by Induction**
Base case + inductive step.

> Theorem: 1 + 2 + ... + n = n(n+1)/2 for all n ≥ 1.
> Base (n=1): 1 = 1·2/2. ✓
> Step: Assume true for n. Show for n+1.
>   1+...+n+(n+1) = n(n+1)/2 + (n+1) = (n+1)(n+2)/2. ✓ □

### 4. **Proof by Contrapositive**
P → Q ≡ ¬Q → ¬P.

> Theorem: if n² is odd, n is odd.
> Contrapositive: if n is even, n² is even. (Already proved.) □

### 5. **Proof by Construction**
Build the object explicitly.

> Theorem: there exists a graph with chromatic number 3 but no triangle.
> Proof: the Petersen graph. (Constructive demonstration.) □

---

## III. PROVING ALGORITHMS

### Proving Termination
For any loop or recursion, show:
- A "rank" decreases with each step
- The rank is bounded below
- Therefore, only finitely many steps possible

> Quicksort: each recursive call has strictly smaller subarray; size 0 is the base.

### Proving Correctness (loop invariant)
1. State the invariant.
2. Prove **initialization** (true before loop).
3. Prove **maintenance** (preserved by each iteration).
4. Use **termination** + invariant to derive correctness.

### Proving Greedy
Two main techniques:

#### Exchange argument
Show: any "non-greedy" optimal solution can be transformed into a greedy one without decreasing quality.

> Activity selection: if optimal doesn't pick the earliest-finishing activity, swap it in. Same number of activities. → Greedy is optimal.

#### Greedy stays ahead
At each step, greedy's partial answer is at least as good as any other algorithm's.

### Proving DP correctness
1. State subproblem definition (`dp[i][j]` represents...).
2. Prove transition exhaustively considers all possibilities.
3. Prove base case.
4. By induction on the topological order, dp[final] is correct.

### Proving Lower Bounds
Show no algorithm can do better than X.

> Comparison sorting Ω(n log n): a comparison-based sort produces a decision tree of size n!. The tree has height ≥ log₂(n!) = Ω(n log n). Therefore worst-case ≥ this. □

---

## IV. EXAMPLE: PROVING DIJKSTRA'S CORRECTNESS

**Claim**: Dijkstra's algorithm finds shortest paths from source s to all vertices, when all edge weights are non-negative.

**Proof** (by induction on order of finalization):

**Invariant**: when vertex v is "finalized" (popped from priority queue), dist[v] = true shortest distance from s to v.

**Base**: first finalized = s, dist[s] = 0 = trivial shortest.

**Inductive step**: suppose all previously finalized vertices have correct dist. Consider next finalized v with current dist d. Suppose for contradiction there's a shorter path P to v with cost < d.

P has some first vertex v' that is *not* yet finalized. The portion of P up to v' has length ≥ dist[v'] (we set dist[v'] when relaxing the predecessor on this shorter path; or it's still ∞, contradiction). The remaining portion has length ≥ 0 (non-negative weights). So total ≥ dist[v']. But v was chosen as the unfinalized vertex with smallest dist, so dist[v] ≤ dist[v']. So total ≥ dist[v] = d, contradicting "< d." □

---

## V. WHEN PROOF FAILS — THE ALGORITHM IS WRONG

If you can't prove correctness, your algorithm is probably wrong. Don't submit. Find the missing case.

If you spent 30 minutes failing to prove → either:
- The algorithm has a bug (find counterexample)
- The algorithm is right but the proof is hard (look for invariant)

**Stress test** is a poor man's substitute for proof. Use both.

---

## VI. PROOF IN CONTESTS

You won't write formal proofs in contests. But you must:

1. **Convince yourself** of correctness in 2-3 sentences before coding.
2. **Identify the proof technique** (exchange, induction, etc.).
3. **Spot the counterexample** if proof feels fishy.

> "Greedy: pick smallest at each step. Why? Because if optimal picked larger, we can swap..." → if you can't finish that sentence, your greedy might be wrong.

---

## VII. EXERCISES

For each, prove correctness in 3-5 sentences:

1. **Two-sum (sorted, two pointers)**: at each step, l moves right or r moves left; never miss a pair.
2. **Kadane's algorithm**: at each i, dp[i] = max subarray ending at i.
3. **Floyd's cycle detection**: tortoise and hare meet iff cycle exists.
4. **Activity selection (greedy by end time)**: optimal includes earliest-finishing.
5. **Kruskal's MST**: at each step, adding the smallest non-cycle-forming edge is safe.
6. **Heap-based scheduling**: extracting min always gives correct order.

---

## VIII. PROOF-FREE LIVING IS PROOF-LESS LIVING

> Most beginners argue "I think it's right." That's not enough.
> Most experts say "It's right because of X." That's enough.

The transition is the proof habit.

---

## IX. RECOMMENDED READING

- **Erickson, Algorithms** ⭐ (free) — exemplary proofs throughout
- **Polya, How to Solve It** — proof techniques
- **Velleman, How to Prove It** — gentle intro to formal proofs
- **CLRS** — every algorithm comes with a proof

---

**→ Next:** [`10-Edge-Case-Analysis.md`](./10-Edge-Case-Analysis.md)
