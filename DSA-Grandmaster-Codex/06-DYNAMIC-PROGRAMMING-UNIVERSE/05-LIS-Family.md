# 🧬 The LIS Family (Longest Increasing Subsequence)

> *"From O(n²) to O(n log n): the elegant leap that defines this family."*

---

## I. LIS — O(n²) DP
`dp[i]` = length of LIS ending at index i.
```cpp
for (int i = 0; i < n; i++) {
    dp[i] = 1;
    for (int j = 0; j < i; j++)
        if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
}
answer = max(dp);
```

---

## II. LIS — O(n log n) ⭐ (patience sorting)
Maintain `tails[]` where `tails[k]` = smallest possible tail of an increasing subsequence of length k+1.
```cpp
vector<int> tails;
for (int x : a) {
    auto it = lower_bound(tails.begin(), tails.end(), x);  // strictly increasing
    if (it == tails.end()) tails.push_back(x);
    else *it = x;
}
return tails.size();
```
- `lower_bound` → strictly increasing LIS.
- `upper_bound` → non-decreasing (longest non-decreasing subsequence).
- **Note**: `tails` gives the LENGTH correctly, but is NOT itself a valid LIS; to reconstruct the actual sequence, track predecessor indices.

---

## III. THE FAMILY

### Number of LIS (LC 673)
Track both length and count of LIS ending at each i.

### Longest Increasing Path in a Matrix (LC 329)
DFS + memoization on cells (DAG by increasing value).

### Russian Doll Envelopes (LC 354) ⭐
Sort by width ascending, height **descending** (so equal widths don't nest), then LIS on heights → O(n log n).

### Maximum Sum Increasing Subsequence
Like LIS but maximize the SUM, not the length (O(n²)).

### Longest Divisible Subset (LC 368)
Sort, then LIS where the condition is `a[i] % a[j] == 0`.

### Minimum number of increasing subsequences to cover
= longest non-increasing subsequence (Dilworth's theorem).

### Longest Bitonic Subsequence
LIS from left + LIS from right (decreasing) combined at each peak.

---

## IV. THE BINARY-SEARCH-ON-DP TECHNIQUE
LIS in O(n log n) generalizes: whenever a DP transition searches for the best previous state with a monotonic key, replace the linear scan with binary search (or a Fenwick/segment tree by value).

### LIS via Segment Tree (alternative O(n log n))
Coordinate-compress values; `dp[v]` stored in a segment tree by value; query max over values < a[i]. Useful when extra constraints exist (e.g., LIS with index distance limits).

---

## V. DILWORTH'S THEOREM (the deep connection)
The minimum number of increasing subsequences needed to partition a sequence = length of the longest non-increasing subsequence (and vice versa). Powers several "minimum chains/antichains" problems.

---

## VI. COMPLEXITY
| Method | Time |
|--------|------|
| Basic DP | O(n²) |
| Patience sorting (binary search) | O(n log n) |
| Segment tree by value | O(n log n) |

---

## VII. PROBLEMS
- LIS (300), Number of LIS (673)
- Russian Doll Envelopes (354) ⭐
- Longest Increasing Path in Matrix (329)
- Longest Divisible Subset (368)
- Maximum Length of Pair Chain (646)
- Make Array Strictly Increasing (1187)
- [CSES](https://cses.fi/problemset/) "Increasing Subsequence"

---

**→ Next:** [`06-LCS-Family.md`](./06-LCS-Family.md)
