# 🎚️ State Design — The Architecture of Solutions

> *"The hardest part of DP is not the transition. It's the state."*

---

## I. THE STATE-DESIGN PROBLEM

For DP, BFS, search, simulation: define the minimal state that:

1. **Captures all decision-relevant information** (Markov property)
2. **Is small enough to enumerate / memoize**
3. **Has well-defined transitions**

A bad state design = exponential blowup. A good state design = polynomial solution.

---

## II. THE QUESTIONS OF STATE DESIGN

### Q1: **What's varying as decisions are made?**
List every piece of "context" that influences future decisions.

### Q2: **What can I drop?**
Some context is determined by other context (redundant). Drop it.

### Q3: **What can I compress?**
Sets → bitmasks. Coordinates → indices via compression. Continuous → discrete.

### Q4: **What's the dependency direction?**
Topological order: which states depend on which?

### Q5: **What's the answer to the problem in terms of states?**
Sometimes a single dp[final], sometimes a max over many states.

---

## III. EXAMPLES OF STATE DESIGN

### Example 1: Climbing stairs
- Decision: at each step, take 1 or 2.
- Varies: current step.
- State: `dp[i]` = ways to reach step i.
- Transition: `dp[i] = dp[i-1] + dp[i-2]`.
- Answer: `dp[n]`.

### Example 2: 0/1 Knapsack
- Decision: include item i or not.
- Varies: which items considered, capacity remaining.
- State: `dp[i][w]` = max value using items 0..i-1 with weight ≤ w.
- Transition: `dp[i][w] = max(dp[i-1][w], dp[i-1][w-w[i]] + v[i])`.
- Answer: `dp[n][W]`.

### Example 3: Stocks with cooldown
- Decision: buy, sell, or rest.
- Varies: day, holding stock?, just sold?
- State: `dp[i][holding]` (after sell, force rest day → augmentations).
- Or: `dp[i][0/1/2]` for held/not-held/cooldown.
- Transitions encode the rules.

### Example 4: TSP
- Decision: which city next.
- Varies: cities visited so far, current city.
- State: `dp[mask][i]` = min cost to start, visit cities in mask, end at i.
- Transition: `dp[mask | (1<<j)][j] = min(dp[mask][i] + dist[i][j])`.
- Answer: `min over j: dp[(1<<n)-1][j] + dist[j][start]`.

### Example 5: Edit distance
- Varies: position in string A, position in string B.
- State: `dp[i][j]` = edit distance between A[0..i-1] and B[0..j-1].
- Transitions: 3 operations + match case.

---

## IV. STATE EXPLOSION SYMPTOMS

If your state has:
- 4 dimensions of size 100 each → 10⁸ states. Likely too many.
- A continuous component → can't enumerate; need discretization.
- A big set as a parameter → must compress to bitmask or canonical.

**Fixes:**
- Drop redundant dimensions
- Realize one dimension is implicit from another
- Use bitmask for small sets
- Coordinate-compress
- Reformulate problem

---

## V. THE STATE-COLLAPSE TECHNIQUES

### Technique 1: **Drop time if it's just an index**
If `dp[t][x]` only uses `dp[t-1][...]`, you don't need t — just two arrays (current, previous).

### Technique 2: **Realize one dim determines another**
If state has both `(i, j, sum)` but `sum = i + j`, drop `sum`.

### Technique 3: **Combine into single number**
A position in 2D grid can be `i * cols + j` (single int).

### Technique 4: **Bitmask for subsets**
For n ≤ 20, set of items as bitmask.

### Technique 5: **Hash for arbitrary state**
For game DP / search with complex states, hash the state.

---

## VI. STATE FOR GRAPH SEARCH (BFS/DFS)

When BFS-ing, your "node" is a state. Sometimes:

- **(x, y)**: simple grid position
- **(x, y, k)**: position + remaining ability (e.g., obstacles to break)
- **(node, parity)**: node + some flag (e.g., even/odd walks)
- **(node, mask)**: node + visited subset (TSP-like)
- **(state of board)**: serialized board (8-puzzle, sliding puzzle)

**Be parsimonious**: every dimension multiplies state count. n=10⁵ × parity=2 = 2·10⁵ states (fine). n=10⁵ × mask=2⁵=32 = 3.2·10⁶ (still fine). n=10⁵ × mask=2¹⁰=1024 = 10⁸ (probably too many).

---

## VII. STATE DESIGN MISTAKES

### Mistake 1: **Over-stating**
Including irrelevant info → state space too large.

> Bad: dp[i][j][sum_so_far] when sum is not needed for future decisions.
> Good: dp[i][j].

### Mistake 2: **Under-stating**
Missing crucial info → wrong answer.

> Bad: dp[i] for stocks with cooldown without "just sold" flag.
> Good: dp[i][0/1/2].

### Mistake 3: **Wrong base case**
The smallest case isn't handled, or is wrong.

### Mistake 4: **Wrong topological order**
Computing dp[i] before its dependencies.

### Mistake 5: **Confusing "passing through" with "ending at"**
For some problems, dp[i] = answer when ending at i; for others, when passing through. Get this wrong, you mix counts.

---

## VIII. THE STATE-DESIGN CHECKLIST

For every DP problem:

- [ ] What's the smallest state capturing all decision-relevant info?
- [ ] What does dp[state] represent? (Write a 1-sentence definition.)
- [ ] What are the transitions? (For each state, what does it depend on?)
- [ ] What's the base case?
- [ ] What's the topological order?
- [ ] Where's the final answer?
- [ ] What's the time complexity? (#states × transitions)
- [ ] What's the space complexity? (#states; possibly reducible)

---

## IX. THE FINAL TRUTH

> **"State design is to DP what variable choice is to mathematics.  
>  Pick the wrong variable, the integral diverges.  
>  Pick the right one, it solves itself."**

---

**→ Next:** [`08-Invariant-Discovery.md`](./08-Invariant-Discovery.md)
