# 🧬 DP Foundations — The 5-Step Framework

> *"DP is the discipline of trading repeated computation for memory."*

---

## I. WHAT IS DP?

Dynamic Programming = solving a problem by combining solutions to **overlapping subproblems**, each solved **once** and **cached**.

Two requirements:
1. **Optimal substructure**: the optimal solution contains optimal solutions to subproblems.
2. **Overlapping subproblems**: the same subproblem appears multiple times in a naive recursion.

If both hold → DP applies. If only #1 → likely D&C. If only #2 → memoization helps but not classical DP.

---

## II. TOP-DOWN VS BOTTOM-UP

### Top-down (memoization)
Recursion + cache.
```python
@cache
def solve(state):
    if base_case: return base_value
    return combine(solve(smaller_state) for ...)
```
- Pros: natural; only computes needed subproblems
- Cons: recursion overhead; stack depth

### Bottom-up (tabulation)
Iterative table fill in topological order.
```python
dp = [base_values]
for state in topological_order:
    dp[state] = combine(dp[smaller_state] for ...)
return dp[final]
```
- Pros: no recursion overhead; easier to space-optimize
- Cons: must figure out fill order; might compute unneeded states

**Same complexity. Same correctness.** Choose by taste / problem.

---

## III. THE 5-STEP DP FRAMEWORK

For ANY DP problem:

### Step 1: Define the STATE
> "What information do I need to characterize a subproblem?"

`dp[state]` = answer to subproblem identified by `state`.

> Example (LIS): `dp[i]` = length of LIS ending at index i.
> Example (knapsack): `dp[i][w]` = max value using items 0..i with capacity w.
> Example (TSP): `dp[mask][i]` = min cost to visit cities in mask, ending at i.

### Step 2: Define the TRANSITION
> "How does dp[state] depend on smaller states?"

> Example (LIS): `dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])`.
> Example (knapsack): `dp[i][w] = max(dp[i-1][w], dp[i-1][w-w[i]] + v[i])`.

### Step 3: Define the BASE CASE
> "What's the answer for the smallest subproblem?"

> Example (LIS): `dp[i] = 1` for any i (LIS of single element is 1).
> Example (knapsack): `dp[0][w] = 0` (no items → no value).

### Step 4: Determine the COMPUTATION ORDER
> "In what order should I fill the table?"

For top-down, recursion handles this automatically. For bottom-up, ensure that when computing dp[state], all dependencies are already filled.

### Step 5: Locate the FINAL ANSWER
> "Where in dp is the final answer?"

> Example (LIS): `max(dp)`.
> Example (knapsack): `dp[n][W]`.
> Example (TSP): `min(dp[(1<<n)-1][i] + dist[i][0] for all i)`.

---

## IV. THE MEMOIZATION TEMPLATE (C++)

```cpp
int dp[MAX_STATES];
memset(dp, -1, sizeof dp);  // -1 = uncomputed

int solve(int state) {
    if (is_base(state)) return base_value(state);
    if (dp[state] != -1) return dp[state];
    int ans = INT_MAX;  // or 0, depending on op
    for (auto t : transitions(state))
        ans = min(ans, cost(t) + solve(next_state(state, t)));
    return dp[state] = ans;
}
```

---

## V. THE TABULATION TEMPLATE (C++)

```cpp
vector<int> dp(N + 1, base_value);
dp[0] = ...;  // base case
for (int i = 1; i <= N; i++)
    for (auto t : transitions(i))
        dp[i] = combine(dp[i], dp[prev_state(i, t)]);
return dp[N];
```

---

## VI. SPACE OPTIMIZATION

If `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, you don't need full array. Use rolling variables:

```cpp
// Fibonacci, O(1) space:
int a = 0, b = 1;
for (int i = 2; i <= n; i++) {
    int c = a + b;
    a = b; b = c;
}
return b;
```

For 2D DP where `dp[i][j]` only depends on `dp[i-1][...]`: use two rows alternately, reducing O(nm) to O(m).

---

## VII. THE 4 STAGES OF DP UNDERSTANDING

| Stage | Symptom                                            |
|-------|----------------------------------------------------|
| 1     | "I see this is a DP problem."                      |
| 2     | "Given the state, I can write the transition."     |
| 3     | "I can identify the state from the problem."       |
| 4     | "I can derive a custom DP for novel problems."     |

Levels 4-5 reach Stage 4. The Codex aims for Stage 4.

---

## VIII. WARNING SIGNS YOU NEED DP

- "Number of ways to..."
- "Minimum/maximum cost/length/sum..."
- "Longest/shortest..."
- Constraints suggest O(n²) or O(n × k)
- Problem has natural recursive substructure with overlap

---

## IX. WARNING SIGNS DP WILL FAIL

- No overlap in recursion (use D&C)
- State space too big to enumerate (use heuristics, branch & bound, or matheuristics)
- Subproblems aren't independent (need different paradigm)

---

## X. EXERCISES

For each, do the 5-step framework on paper:

1. Climbing stairs (1 or 2 steps; count ways to climb n)
2. Coin change (min coins for target)
3. House robber (max sum no two adjacent)
4. Word break (boolean: can s be split into dictionary words?)
5. Edit distance (transform A → B with min insertions/deletions/substitutions)

---

**→ Next:** [`02-1D-DP.md`](./02-1D-DP.md)
