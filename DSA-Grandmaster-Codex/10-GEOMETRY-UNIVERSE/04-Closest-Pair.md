# 📐 Closest Pair of Points

> *"Among n points, find the two nearest — in O(n log n), not O(n²)."*

---

## I. THE PROBLEM
Given n points in the plane, find the pair with the smallest Euclidean distance.

Brute force: check all C(n,2) pairs → O(n²). We can do **O(n log n)**.

---

## II. DIVIDE & CONQUER — O(n log n) ⭐
```
1. Sort points by x.
2. Divide into left and right halves by a vertical line.
3. Recursively find closest pair in each half; let δ = min of the two.
4. COMBINE: check the "strip" within δ of the dividing line.
   - Within the strip (sorted by y), each point compares to only the next ~7 points.
5. Return the overall minimum.
```
Recurrence T(n) = 2T(n/2) + O(n) → **O(n log n)**.

The magic: in the strip, geometry guarantees each point has at most ~7 neighbors within δ to check (a δ×2δ box holds boundedly many points that are pairwise ≥ δ apart).

---

## III. SWEEP-LINE ALTERNATIVE — O(n log n)
Sort by x; sweep left to right; maintain a set of points ordered by y within the current best distance d of the sweep line. For each new point, only check points within [y−d, y+d] in the set. Remove points farther than d behind the sweep.

Often simpler to code than full D&C.

---

## IV. KEY INSIGHTS
- Use **squared distance** for comparisons (avoid sqrt; exact for integers).
- The strip optimization is what makes the combine step O(n), not O(n²).
- Generalizes to higher dimensions (with worse constants) and to "closest pair under updates" with more machinery.

---

## V. RELATED PROBLEMS
- **k nearest neighbors** → KD-tree
- **All pairs within distance r** → grid bucketing / sweep
- **Farthest pair** → rotating calipers on convex hull, O(n log n)

---

## VI. GRID BUCKETING (randomized O(n) expected)
Place points into a grid with cell size = current best δ. Each point only compares to points in its own and adjacent cells (boundedly many). Rebuild grid when δ improves. Expected linear with randomization.

---

## VII. PROBLEMS
- Closest pair (classic; [CSES](https://cses.fi/problemset/) "Minimum Euclidean Distance")
- K Closest Points to Origin (LC 973) — different (distance to a fixed point; use heap)
- Divide-and-conquer practice on CF/UVa geometry sets

---

## VIII. COMPLEXITY SUMMARY
| Method | Time |
|--------|------|
| Brute force | O(n²) |
| Divide & conquer | O(n log n) |
| Sweep line | O(n log n) |
| Grid bucketing | O(n) expected |

---

**→ Next:** [`05-Polygon-Operations.md`](./05-Polygon-Operations.md)
