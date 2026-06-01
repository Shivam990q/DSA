# 🧬 Profile DP (Broken Profile DP)

> *"Tile and fill grids by tracking the jagged boundary between done and undone."*

---

## I. THE PROBLEM TYPE
Filling a grid with tiles/pieces under adjacency constraints:
- Tile an n×m board with 1×2 dominoes — count the ways.
- Place non-attacking pieces / fill cells respecting neighbor rules.
- Count colorings of a grid with constraints between adjacent cells.

When one dimension is small (m ≤ ~14-20), encode the "frontier" as a bitmask.

---

## II. PROFILE = THE FRONTIER
Process the grid cell by cell (or column by column). The **profile** is a bitmask describing which cells on the boundary are already filled (protruding into the unprocessed region).

- **Broken profile**: process one CELL at a time; the mask has m bits describing the staircase boundary.
- **Column profile**: process one COLUMN at a time; the mask describes which cells of the current column boundary are filled.

---

## III. DOMINO TILING (the canonical example)
Count ways to tile an n×m board with 1×2 dominoes (m small).
- `dp[i][mask]` = ways to fill up to cell i with boundary profile `mask`.
- At each cell, decide: leave empty (must be filled by a horizontal/vertical domino later), place a vertical domino, or place a horizontal domino — updating the mask accordingly.

O(n·m·2ᵐ).

---

## IV. THE GENERAL APPROACH
```
state: (position in grid, profile bitmask of the frontier)
transition: enumerate valid ways to fill the current cell/column
            given the profile, producing the next profile
```
Carefully enumerate which cells can be covered and how the frontier updates. This is fiddly — derive the transitions on paper first.

---

## V. WHEN TO USE
- 2D filling/tiling/placement problems
- One dimension is small (m ≤ ~14-20 so 2ᵐ is tractable)
- Adjacency constraints between cells

Telltale: "count ways to tile/fill an n×m grid" with small m.

---

## VI. RELATED
- **Bitmask DP** (general subsets) — profile DP is bitmask DP where the mask is a grid frontier.
- **Plug DP / connection profile** — advanced variant tracking connectivity (e.g., counting Hamiltonian-like fillings), uses a "broken profile with connection states." Very advanced.

---

## VII. COMPLEXITY
- Broken profile: O(n·m·2ᵐ) typically.
- Choose the smaller dimension as m (the one in the exponent).

---

## VIII. PROBLEMS
- Domino tiling of an n×m board ([CSES](https://cses.fi/problemset/) "Counting Tilings") ⭐
- Tiling with various pieces under constraints
- Maximum Students Taking Exam (LC 1349) — profile/bitmask over rows
- Grid coloring with adjacency constraints
- CF problems tagged "dp" + "bitmasks" (grid filling)

---

## IX. NOTE
Profile DP is Level 7 elite-CP. It's intricate; practice on the domino-tiling problem first, then generalize. Connection/plug DP is research-grade.

---

**→ Next:** [`18-DP-with-Data-Structures.md`](./18-DP-with-Data-Structures.md)
