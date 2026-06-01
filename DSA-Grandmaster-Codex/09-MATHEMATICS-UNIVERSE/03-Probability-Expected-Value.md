# 🔢 Probability & Expected Value

> *"Linearity of expectation: the single most powerful trick in all of competitive math."*

---

## I. BASICS
- P(A) = favorable outcomes / total outcomes (uniform case)
- P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
- P(A ∩ B) = P(A)·P(B|A); independent ⟹ = P(A)·P(B)
- **Conditional**: P(A|B) = P(A∩B)/P(B)
- **Bayes**: P(A|B) = P(B|A)·P(A) / P(B)

---

## II. EXPECTED VALUE
E[X] = Σ x·P(X = x)
- For a fair die: E = (1+2+3+4+5+6)/6 = 3.5

---

## III. LINEARITY OF EXPECTATION ⭐⭐
**E[X + Y] = E[X] + E[Y] — ALWAYS, even if X, Y are dependent.**

This breaks complex expectations into simple ones via **indicator variables**:
- Let X_i = 1 if event i happens, else 0. Then E[#events] = Σ P(event i).

### Example: expected fixed points of a random permutation
Let X_i = 1 if position i is a fixed point. P(X_i=1) = 1/n. E[total] = n·(1/n) = **1**.

### Example: expected comparisons in randomized quicksort
P(elements ranked i and j are compared) = 2/(j−i+1). Sum over all pairs = O(n log n).

---

## IV. EXPECTATION OF PRODUCTS
E[X·Y] = E[X]·E[Y] **only if independent** (unlike sums!).

---

## V. VARIANCE
Var(X) = E[X²] − (E[X])². Var(X+Y) = Var(X)+Var(Y) if independent.

---

## VI. PROBABILITY DP / EXPECTED-VALUE DP
State holds a probability or expected value; transitions weight by probabilities.
- **Knight Probability in Chessboard** (LC 688): dp[step][r][c] = prob of being on board.
- **New 21 Game** (LC 837): sliding-window expected probability.
- **Soup Servings** (LC 808).
- Expected number of steps in random walks / absorbing Markov chains.

### Expected steps via linear equations
For random walks, set up E[state] = 1 + Σ P(next)·E[next] and solve (Gaussian elimination for cyclic dependencies).

---

## VII. COMMON DISTRIBUTIONS
- **Bernoulli** (single trial), **Binomial** (n trials), **Geometric** (trials until first success, E = 1/p)
- **Coupon collector**: expected draws to collect all n = n·H(n) ≈ n ln n

---

## VIII. MARKOV CHAINS (intro)
States with transition probabilities. Stationary distribution, absorbing states, expected hitting times. Solve via linear systems or matrix powers.

---

## IX. PROBLEMS
- Knight Probability (LC 688), New 21 Game (LC 837), Soup Servings (LC 808)
- Random Pick with Weight (LC 528), Implement Rand10 from Rand7 (LC 470)
- Airplane Seat Assignment Probability (LC 1227) — beautiful 1/2 answer via symmetry
- CF problems tagged "probabilities" / "expected value"
- [CSES](https://cses.fi/problemset/) "Dice Probability", "Moving Robots"

---

## X. THE GOLDEN RULE
When you see "expected number of ...", reach for **linearity of expectation + indicator variables** FIRST. It turns scary expectations into a sum of tiny probabilities.

---

**→ Next:** [`04-Linear-Algebra.md`](./04-Linear-Algebra.md)
