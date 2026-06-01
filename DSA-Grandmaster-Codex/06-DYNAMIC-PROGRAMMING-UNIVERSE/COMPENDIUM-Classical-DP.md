# 📜 Classical DP Compendium

> Compact bible of all classical DP families with state, transition, base, complexity.

---

## 02 — 1D DP

### Climbing Stairs (LC 70)
- State: `dp[i]` = ways to reach step i
- Transition: `dp[i] = dp[i-1] + dp[i-2]`
- Base: `dp[0] = dp[1] = 1`
- Complexity: O(n) time, O(1) space (rolling)

### House Robber (LC 198)
- State: `dp[i]` = max sum considering houses 0..i
- Transition: `dp[i] = max(dp[i-1], dp[i-2] + a[i])`
- Base: `dp[0] = a[0], dp[1] = max(a[0], a[1])`

### House Robber II (LC 213, circular)
Run House Robber twice: (i) excluding last, (ii) excluding first. Take max.

### Decode Ways (LC 91)
- `dp[i]` = ways to decode s[0..i-1]
- `dp[i] = dp[i-1] (if s[i-1] valid) + dp[i-2] (if s[i-2..i-1] valid as 2-digit)`

### Min Cost Climbing Stairs (LC 746)
- `dp[i]` = min cost to reach step i
- `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`

### Maximum Subarray (LC 53, Kadane)
- `dp[i]` = max sum subarray ending at i
- `dp[i] = max(a[i], dp[i-1] + a[i])`

### Maximum Product Subarray (LC 152)
Track both max & min ending at i (negative × negative may be max).

---

## 03 — 2D DP / GRIDS

### Unique Paths (LC 62)
- `dp[i][j]` = paths to (i, j) from (0, 0)
- `dp[i][j] = dp[i-1][j] + dp[i][j-1]`
- Base: `dp[0][0] = 1`, first row & column = 1

### Unique Paths II (LC 63, with obstacles)
Skip obstacle cells (set to 0).

### Minimum Path Sum (LC 64)
- `dp[i][j] = a[i][j] + min(dp[i-1][j], dp[i][j-1])`

### Triangle (LC 120)
Bottom-up: `dp[i][j] = a[i][j] + min(dp[i+1][j], dp[i+1][j+1])`.

### Maximal Square (LC 221)
- `dp[i][j]` = side of largest all-1 square ending at (i, j)
- `dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])` if a[i][j] == 1

### Minimum Falling Path Sum (LC 931)
- `dp[i][j] = a[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])`

### Cherry Pickup (LC 741, two simultaneous traversals)
4D state collapsed to 3D using i + j = k invariant.

---

## 04 — KNAPSACK FAMILY

### 0/1 Knapsack
- State: `dp[i][w]` = max value using first i items, capacity ≤ w
- Transition: `dp[i][w] = max(dp[i-1][w], dp[i-1][w-w[i]] + v[i])` (if w[i] ≤ w)
- Base: `dp[0][*] = 0`
- Complexity: O(nW)
- Space optimization: 1D, iterate w from W down to w[i]

### Unbounded Knapsack
Same, but iterate w from w[i] to W (allows reusing item).
- Transition: `dp[w] = max(dp[w], dp[w-w[i]] + v[i])` for w from w[i] to W

### Subset Sum (boolean)
`dp[i][s]` = can we achieve sum s with first i items?

### Partition Equal Subset Sum (LC 416)
Subset sum with target = total/2.

### Target Sum (LC 494)
Reduce to subset sum: count subsets with sum = (total + target)/2.

### Coin Change (min coins, LC 322)
`dp[a]` = min coins to make a; `dp[a] = min(dp[a-c] + 1)` for each coin c.

### Coin Change II (number of ways, LC 518)
`dp[a]` = number of ways. **Loop coins outside** (avoid order duplicates).
```python
for coin in coins:
    for a in range(coin, target+1):
        dp[a] += dp[a-coin]
```

### Last Stone Weight II (LC 1049)
Subset sum closest to total/2.

---

## 05 — LIS FAMILY

### LIS (LC 300)
**O(n²)**:
- `dp[i]` = length of LIS ending at i
- `dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])`

**O(n log n)** (patience sort):
- Maintain `tails[]`: tails[k] = smallest tail of any increasing subsequence of length k+1
- For each x, binary search position in tails; replace.

```cpp
int lengthOfLIS(vector<int>& a) {
    vector<int> tails;
    for (int x : a) {
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    return tails.size();
}
```

### Number of LIS (LC 673)
Track count alongside length.

### Longest Increasing Path in Matrix (LC 329)
DFS + memoization on cells.

### Russian Doll Envelopes (LC 354)
Sort by width asc, height desc; LIS on heights.

### Longest Divisible Subset (LC 368)
LIS variant: a[j] divides a[i].

### Maximum Sum Increasing Subsequence
Like LIS but maximize sum.

---

## 06 — LCS FAMILY

### LCS (LC 1143)
- `dp[i][j]` = LCS of s1[0..i-1] and s2[0..j-1]
- If s1[i-1] == s2[j-1]: `dp[i][j] = 1 + dp[i-1][j-1]`
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

### Longest Common Substring
- `dp[i][j]` = length ending at (i, j); 0 if mismatch.

### Shortest Common Supersequence (LC 1092)
Length: `n + m - LCS`.

### Distinct Subsequences (LC 115)
Count of subsequences of s equal to t.

---

## 07 — EDIT DISTANCE FAMILY

### Edit Distance (LC 72)
- `dp[i][j]` = edit distance between s[0..i-1] and t[0..j-1]
- If s[i-1] == t[j-1]: `dp[i][j] = dp[i-1][j-1]`
- Else: `dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` (delete, insert, replace)

### Wildcard Matching (LC 44)
Patterns with `?` (any char) and `*` (any sequence).

### Regular Expression Matching (LC 10)
Patterns with `.` and `*` (zero or more of preceding).

### One Edit Distance (LC 161)
Boolean: are two strings exactly one edit apart?

---

## 08 — STOCKS DP

Each problem is 2 states (holding/not) with rules per variant.

### Best Time to Buy and Sell Stock (LC 121)
Single transaction. Track `min` so far.

### II — Multiple Transactions (LC 122)
Sum positive deltas (greedy).

### III — At Most 2 Transactions (LC 123)
4-state DP: bought1, sold1, bought2, sold2.

### IV — At Most K Transactions (LC 188)
- `dp[k][i]` = max profit with ≤ k transactions, considering first i days
- Optimization: for each i, track `max(dp[k-1][j] - prices[j])`

### With Cooldown (LC 309)
3 states: holding, just sold (cooldown), neither.

### With Transaction Fee (LC 714)
Subtract fee on sell.

---

## 09 — INTERVAL DP

### Matrix Chain Multiplication
- `dp[i][j]` = min cost to compute product of matrices i..j
- `dp[i][j] = min over k: dp[i][k] + dp[k+1][j] + cost(i, k, j)`

### Burst Balloons (LC 312)
- Reverse perspective: `dp[i][j]` = max coins from bursting balloons in (i, j)
- Pick last balloon to burst (k), recurse on left/right

### Min Cost to Cut Stick (LC 1547)
Add 0 and L sentinels; dp on cuts pair (i, j).

### Palindrome Partitioning II (LC 132)
- `dp[i]` = min cuts of s[0..i]
- Precompute `isPalin[i][j]`

### Boolean Parenthesization
Count ways to parenthesize boolean expression to evaluate True/False.

### Strange Printer (LC 664)
- `dp[i][j]` = min ops to print s[i..j]

---

## 10 — TREE DP

### Diameter of Binary Tree (LC 543)
For each node, longest path through it = left height + right height.

### Binary Tree Maximum Path Sum (LC 124)
At each node, `single_path = max(node, node + left_single, node + right_single)`. `through_node = node + max(0, left_single) + max(0, right_single)`. Track global max.

### House Robber III (LC 337)
Each node returns `(rob, not_rob)`.

### Tree DP with re-rooting
Compute subtree DP first (post-order). Then redo root → use parent contribution to compute "as if rooted here" for all nodes (re-rooting).

> Sum of distances in tree (LC 834) — classic.

---

## 11 — DAG DP

For DAG, topological order + DP works.

### Longest Path in DAG
- `dp[v]` = longest path ending at v
- `dp[v] = 1 + max(dp[u] for (u, v) in edges)`

### Cheapest Flights with K Stops (LC 787)
Bellman-Ford-like DP with k constraint, or BFS with state.

### Number of Ways to Reach Destination (LC 1976)
Dijkstra + DP for counting shortest paths.

---

## 12 — BITMASK DP

### TSP (n ≤ 22)
- `dp[mask][i]` = min cost having visited cities in mask, ending at i
- `dp[mask | (1<<j)][j] = min(dp[mask][i] + dist[i][j])`
- Answer: `min(dp[(1<<n)-1][i] + dist[i][0])`
- Complexity: O(2ⁿ × n²)

### Partition to K Equal Sum Subsets (LC 698)
`dp[mask]` = remaining capacity in current bucket if mask of items placed.

### Number of Ways to Wear Different Hats (LC 1434)
- `dp[hat][mask]` = ways using first hat hats with mask of people having a hat
- Iterate hats outer, masks inner

### Minimum Incompatibility (LC 1681)
`dp[mask]` = min total incompat for placing items in mask into k subsets (each size n/k).

### Smallest Sufficient Team (LC 1125)
`dp[mask]` = smallest team covering mask of skills.

---

## 13 — DIGIT DP

For "count numbers in [L, R] satisfying property" problems.

### Template
```python
def f(N):  # count valid numbers in [0, N]
    digits = list(map(int, str(N)))
    @cache
    def rec(pos, tight, leading_zero, state):
        if pos == len(digits): return is_valid(state)
        limit = digits[pos] if tight else 9
        ans = 0
        for d in range(limit + 1):
            new_tight = tight and d == limit
            new_lead = leading_zero and d == 0
            new_state = update(state, d, new_lead)
            ans += rec(pos + 1, new_tight, new_lead, new_state)
        return ans
    return rec(0, True, True, initial_state)

answer = f(R) - f(L - 1)
```

### Top problems
- Count numbers with unique digits (LC 357)
- Numbers at most N given digit set (LC 902)
- Count of integers (LC 2719)

---

## 14 — PROBABILITY / EXPECTED DP

### Knight Probability in Chessboard (LC 688)
- `dp[i][j][k]` = probability of being at (i, j) after k moves
- `dp[i][j][k] = sum over moves (m): dp[ni][nj][k-1] / 8`

### New 21 Game (LC 837)
- `dp[i]` = probability of reaching ≤ N starting from sum i
- Sliding window optimization

### Soup Servings (LC 808)
DP with memoization; for large N, return 1.0.

---

## 15 — DP OPTIMIZATIONS

### Knuth's Optimization
For `dp[i][j] = min over k in [i, j]: dp[i][k] + dp[k][j] + cost(i, j)` with quadrangle inequality on cost: **opt(i, j) ≤ opt(i, j+1) ≤ opt(i+1, j+1)**. Reduces O(n³) to O(n²).

### Divide and Conquer DP
For `dp[i][j] = min over k in [0, j]: dp[i-1][k] + cost(k, j)` with **opt monotonicity** (opt(i, j) ≤ opt(i, j+1)). O(kn²) → O(kn log n).

### Convex Hull Trick (CHT)
For `dp[i] = min over j < i: dp[j] + b[j] × x[i]` (linear in x[i]). Maintain convex hull of lines; binary search or incrementally add. O(n log n) or O(n) (monotonic queries).

### Li Chao Tree
Generalization of CHT supporting arbitrary queries (not just monotonic).

### Aliens Trick (Lagrangian relaxation)
For "exactly k" partition / matching: binary search a Lagrange multiplier λ; remove the "k" constraint by penalizing with λ; binary search until k matches.

---

## 16 — SOS DP (Sum over Subsets)

### Concept
Given f(mask), compute g(mask) = Σ over submasks s of mask: f(s). Naive: O(3ⁿ). SOS DP: O(n × 2ⁿ).

```cpp
for (int i = 0; i < n; i++)
    for (int mask = 0; mask < (1 << n); mask++)
        if (mask & (1 << i)) g[mask] += g[mask ^ (1 << i)];
```

### Use cases
- Bitmask DP transitions over subsets
- Subset sum convolutions
- Counting

---

## 17 — PROFILE DP

For grid problems where state is "frontier" between processed and unprocessed.

### Broken Profile DP (tile a 2×n / 3×n grid with dominoes)
- State: column index + bitmask of "protrusions" into next column
- Transitions: enumerate ways to fill current column

---

## 18 — DP WITH DATA STRUCTURES

When transition has form `dp[i] = max over j with property P(j): dp[j] + ...`, accelerate with:
- **Segment tree** indexed by some key
- **BIT** for prefix maxima
- **Monotonic deque** for sliding window
- **Set / multiset** for nearest-element queries

> Example: LIS in O(n log n) with segment tree on values.
> Example: Constrained Subsequence Sum (LC 1425) — DP + monotonic deque.

---

## 19 — DP CHEATSHEET

| Pattern              | Recognize when                                  | Approach                            |
|----------------------|-------------------------------------------------|-------------------------------------|
| 1D DP                | Single dimension state                          | dp[i] = f(dp[<i])                   |
| 2D DP grid           | Path on grid                                    | dp[i][j] = a[i][j] + min(prev)      |
| Knapsack             | Pick items with capacity                        | dp[i][w]; iterate items             |
| LIS                  | Longest increasing                              | O(n²) DP / O(n log n) BS            |
| LCS                  | Two sequences                                   | dp[i][j] on prefixes                |
| Edit distance        | Transform A → B                                 | 3 ops per cell                      |
| Stocks               | Buy/sell with rules                             | State machine                       |
| Interval DP          | "On range (i, j) divide somewhere"              | dp[i][j] = combine(dp[i][k], dp[k+1][j]) |
| Tree DP              | Tree with subtree info                          | Post-order DFS                      |
| Bitmask DP           | n ≤ 20, sets                                    | dp[mask][...]                       |
| Digit DP             | Count in [L, R]                                 | Position + tight                    |
| Probability DP       | Random / expected value                         | Float DP                            |
| Optimizations        | n ≥ 5000 with O(n²) too slow                    | CHT, Knuth, D&C, Alien              |
| SOS DP               | Sum over submasks                               | n × 2ⁿ                              |

---

## 20 — 50 CLASSIC DP PROBLEMS

(In recommended solving order)

1. Climbing Stairs (LC 70)
2. House Robber (LC 198)
3. Coin Change (LC 322)
4. Coin Change II (LC 518)
5. Maximum Subarray (LC 53)
6. Maximum Product Subarray (LC 152)
7. Word Break (LC 139)
8. Decode Ways (LC 91)
9. Best Time to Buy/Sell I-IV (LC 121, 122, 123, 188)
10. Best Time with Cooldown (LC 309)
11. Best Time with Fee (LC 714)
12. Unique Paths (LC 62)
13. Unique Paths II (LC 63)
14. Minimum Path Sum (LC 64)
15. Triangle (LC 120)
16. Maximal Square (LC 221)
17. Maximal Rectangle (LC 85)
18. Longest Common Subsequence (LC 1143)
19. Edit Distance (LC 72)
20. Distinct Subsequences (LC 115)
21. Wildcard Matching (LC 44)
22. Regular Expression Matching (LC 10)
23. LIS (LC 300)
24. Number of LIS (LC 673)
25. Russian Doll Envelopes (LC 354)
26. 0/1 Knapsack
27. Subset Sum
28. Partition Equal Subset Sum (LC 416)
29. Target Sum (LC 494)
30. Last Stone Weight II (LC 1049)
31. Burst Balloons (LC 312)
32. Matrix Chain Multiplication
33. Palindrome Partitioning II (LC 132)
34. Strange Printer (LC 664)
35. Stone Game (LC 877)
36. Stone Game II-IX
37. Cherry Pickup I, II (LC 741, 1463)
38. House Robber III (LC 337)
39. Diameter of Binary Tree (LC 543)
40. Binary Tree Maximum Path Sum (LC 124)
41. Sum of Distances in Tree (LC 834)
42. TSP / Traveling Salesman (Bitmask)
43. Partition to K Equal Sum Subsets (LC 698)
44. Smallest Sufficient Team (LC 1125)
45. Number of Ways to Wear Different Hats (LC 1434)
46. Frog Jump (LC 403)
47. Tallest Billboard (LC 956)
48. Knight Probability (LC 688)
49. New 21 Game (LC 837)
50. Profitable Schemes (LC 879)

---

**→ Next universe:** [`../07-GRAPH-THEORY-UNIVERSE/00-Index.md`](../07-GRAPH-THEORY-UNIVERSE/00-Index.md)
