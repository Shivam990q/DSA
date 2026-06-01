# 🧬 Probability & Expected-Value DP

> *"When the future is random, the DP table holds probabilities or expectations."*

---

## I. TWO FLAVORS
- **Probability DP**: `dp[state]` = probability of reaching/being in a state.
- **Expected-value DP**: `dp[state]` = expected value (steps, score, cost) from a state.

Both use floating point (or fractions mod p for exact CP answers).

---

## II. PROBABILITY DP
Transitions weight by the probability of each move.

### Knight Probability in Chessboard (LC 688)
`dp[step][r][c]` = probability the knight is on (r,c) after `step` moves.
```
dp[0][r0][c0] = 1
dp[s][nr][nc] += dp[s-1][r][c] / 8   for each of the 8 knight moves
answer = Σ dp[K][r][c] over on-board cells
```

### New 21 Game (LC 837)
Probability of ending with ≤ N when drawing until ≥ K; sliding-window sum optimization.

### Soup Servings (LC 808)
Probability DP with a shortcut: for large N, the answer → 1.

---

## III. EXPECTED-VALUE DP
`E[state] = (immediate cost) + Σ P(next) · E[next]`.

### Acyclic case
Process states in dependency order (topological), compute E directly.

### Cyclic case (the tricky one) ⭐
If states depend on each other cyclically (e.g., "with prob p go back to start"), you get a **system of linear equations**. Solve by:
- **Algebra**: express E[state] in terms of itself, solve (e.g., E = 1 + p·E ⟹ E = 1/(1−p)).
- **Gaussian elimination** for general systems.
- **Setting up E[i] = a·E[parent] + b** and propagating (for chain/tree structures).

### Classic: expected dice rolls / random walks
- Expected rolls to get all faces (coupon collector): n·H(n).
- Expected steps in a random walk on a line/graph (absorbing Markov chains).

---

## IV. EXACT PROBABILITIES MOD p (competitive programming)
CP problems often want the answer as a fraction P/Q reported as P·Q⁻¹ mod (10⁹+7). Do all probability arithmetic with modular inverses instead of floating point.

---

## V. LINEARITY OF EXPECTATION (often avoids DP entirely!) ⭐
Before building an expected-value DP, ask: can linearity of expectation give the answer directly via indicator variables? Often a "hard" expectation collapses to a simple sum of probabilities. (See [`../09-MATHEMATICS-UNIVERSE/03-Probability-Expected-Value.md`](../09-MATHEMATICS-UNIVERSE/03-Probability-Expected-Value.md).)

---

## VI. COMPLEXITY
- Acyclic probability/expectation DP: O(states × transitions).
- Cyclic (linear system): O(states³) Gaussian elimination, or O(states) if it telescopes.

---

## VII. PROBLEMS
- Knight Probability in Chessboard (688)
- New 21 Game (837), Soup Servings (808)
- Out of Boundary Paths (576)
- Airplane Seat Assignment Probability (1227) — symmetry gives 1/2
- [CSES](https://cses.fi/problemset/) "Dice Probability", "Moving Robots", "Stick Lengths"
- CF problems tagged "probabilities" / "dp"

---

**→ Next:** [`15-DP-Optimizations.md`](./15-DP-Optimizations.md)
