# 🧬 2D DP & Grid Problems

> *"When the state needs two coordinates, the table becomes a grid."*

---

## I. THE SHAPE
State `dp[i][j]` — two dimensions. Common for: grid paths, two sequences, intervals (i,j as bounds).

---

## II. GRID PATH PROBLEMS

### Unique Paths (LC 62)
Move only right/down from top-left to bottom-right.
- `dp[i][j] = dp[i-1][j] + dp[i][j-1]`
- Base: first row & column = 1
- (Combinatorial closed form: C(m+n-2, m-1))

### Unique Paths II (LC 63) — with obstacles
Obstacle cells have dp = 0.

### Minimum Path Sum (LC 64)
- `dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])`

### Triangle (LC 120)
Bottom-up: `dp[i][j] = a[i][j] + min(dp[i+1][j], dp[i+1][j+1])`.

### Maximal Square (LC 221)
- `dp[i][j]` = side of largest all-1 square ending at (i,j)
- `dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])` if cell == 1

### Maximal Rectangle (LC 85)
Reduce each row to a histogram; apply largest-rectangle-in-histogram per row. O(nm).

### Dungeon Game (LC 174)
DP from bottom-right (health needed), since the constraint is on minimum health along the path.

### Minimum Falling Path Sum (LC 931)
- `dp[i][j] = a[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])`

### Cherry Pickup (LC 741) / Cherry Pickup II (LC 1463)
Two simultaneous traversals → collapse the 4D state (two positions) using the invariant i₁+j₁ = i₂+j₂ (same step count) → 3D.

---

## III. THE GRID DP TEMPLATE
```cpp
vector<vector<long long>> dp(n, vector<long long>(m, 0));
// base: dp[0][0], first row, first col
for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        dp[i][j] = grid[i][j] + best(dp[i-1][j], dp[i][j-1]); // guard bounds
return dp[n-1][m-1];
```

---

## IV. SPACE OPTIMIZATION
If `dp[i][*]` only depends on `dp[i-1][*]`, keep two rows (or even one row updated in place) → O(m) space instead of O(nm).

---

## V. DIRECTION MATTERS
- Right/down only → fill top-left to bottom-right.
- If movement is in all 4 directions with weights → it's a **shortest path** (Dijkstra/BFS), NOT plain DP (cycles break DP order).
- Constraint on the END (like Dungeon Game) → fill backward.

---

## VI. 2D DP THAT ISN'T A GRID
`dp[i][j]` also models:
- Two strings (LCS, edit distance) → see [`COMPENDIUM-Classical-DP.md`](./COMPENDIUM-Classical-DP.md) §06-07
- Intervals (i, j as left/right bounds) → see Interval DP
- (item index, capacity) → Knapsack

---

## VII. PROBLEMS
- Unique Paths I/II (62/63), Minimum Path Sum (64), Triangle (120)
- Maximal Square (221), Maximal Rectangle (85)
- Dungeon Game (174), Minimum Falling Path Sum (931)
- Cherry Pickup I/II (741/1463)
- Count square submatrices with all ones (1277)

---

**→ Next:** [`04-Knapsack-Family.md`](./04-Knapsack-Family.md)
