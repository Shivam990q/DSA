# 🧬 Interval DP

> *"Solve a range by choosing a split point or a 'last' element. dp[i][j] over intervals."*

---

## I. THE SHAPE
`dp[i][j]` = answer for the subarray/substring from i to j. Compute by trying every split point k, or by deciding the "last operation" on the interval.
```
dp[i][j] = best over k in [i, j) of: dp[i][k] + dp[k+1][j] + cost(i, k, j)
```
Iterate by **increasing interval length** so sub-intervals are ready.
```cpp
for (int len = 2; len <= n; len++)
  for (int i = 0; i + len - 1 < n; i++) {
    int j = i + len - 1;
    for (int k = i; k < j; k++)
        dp[i][j] = best(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i,k,j));
  }
```
Typically O(n³).

---

## II. CLASSIC PROBLEMS

### Matrix Chain Multiplication
Min scalar multiplications to multiply a chain of matrices. `cost(i,k,j) = p[i-1]·p[k]·p[j]`.

### Burst Balloons (LC 312) ⭐
Reverse the thinking: instead of "first balloon to burst," pick the **LAST** balloon k to burst in (i,j). Then left and right intervals are independent.
```
dp[i][j] = max over k of: dp[i][k-1] + dp[k+1][j] + a[i-1]*a[k]*a[j+1]
```

### Minimum Cost to Cut a Stick (LC 1547)
Add sentinels 0 and L; dp over pairs of cut positions.

### Palindrome Partitioning II (LC 132)
Min cuts to partition into palindromes. Precompute isPalin[i][j]; `dp[i]` = min cuts for prefix.

### Stone Game / Merge Stones (LC 1000)
Merge K consecutive piles; interval DP with an extra dimension for "number of piles mod (K-1)."

### Boolean Parenthesization
Count ways to parenthesize a boolean expression to evaluate True.

### Strange Printer (LC 664)
Min turns to print a string; interval DP merging equal characters.

### Optimal BST
Build a BST minimizing expected search cost (Knuth's optimization applies → O(n²)).

---

## III. THE "PICK THE LAST/FIRST" TRICK ⭐
The key insight for many interval DPs (esp. Burst Balloons): don't think about the FIRST action—think about the LAST. This makes the two resulting sub-intervals independent.

---

## IV. OPTIMIZATIONS
- **Knuth's optimization**: when the cost satisfies the quadrangle inequality and opt is monotonic, O(n³) → O(n²). Applies to optimal BST, some merge problems.
- See [`15-DP-Optimizations.md`](./15-DP-Optimizations.md).

---

## V. COMPLEXITY
- Basic: O(n³) (n² intervals × n splits)
- With Knuth: O(n²)

n ≤ ~500 for O(n³); n ≤ ~5000 with Knuth's optimization.

---

## VI. PROBLEMS
- Burst Balloons (312) ⭐, Minimum Cost to Cut a Stick (1547)
- Matrix Chain Multiplication (classic)
- Palindrome Partitioning II (132)
- Stone Game variants, Merge Stones (1000)
- Strange Printer (664), Remove Boxes (546, harder)
- Minimum Score Triangulation of Polygon (1039)
- [CSES](https://cses.fi/problemset/) interval problems

---

**→ Next:** [`10-Tree-DP.md`](./10-Tree-DP.md)
