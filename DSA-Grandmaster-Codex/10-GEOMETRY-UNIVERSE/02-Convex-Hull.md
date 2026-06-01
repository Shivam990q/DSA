# 📐 Convex Hull

> *"The smallest convex polygon enclosing a set of points — like a rubber band snapping around nails."*

---

## I. THE PROBLEM
Given n points, find the smallest convex polygon containing all of them. Output its vertices in order.

---

## II. ANDREW'S MONOTONE CHAIN — O(n log n) ⭐
The cleanest method. Sort points; build lower hull then upper hull using cross-product turn tests.
```cpp
vector<P> convexHull(vector<P> pts) {
    sort(pts.begin(), pts.end(), [](P a, P b){
        return a.x < b.x || (a.x == b.x && a.y < b.y);
    });
    int n = pts.size(), k = 0;
    vector<P> h(2*n);
    // lower hull
    for (int i = 0; i < n; i++) {
        while (k >= 2 && (h[k-1]-h[k-2]).cross(pts[i]-h[k-2]) <= 0) k--;
        h[k++] = pts[i];
    }
    // upper hull
    for (int i = n-2, t = k+1; i >= 0; i--) {
        while (k >= t && (h[k-1]-h[k-2]).cross(pts[i]-h[k-2]) <= 0) k--;
        h[k++] = pts[i];
    }
    h.resize(k-1);
    return h;
}
```
- `<= 0` removes collinear points; use `< 0` to keep them.

---

## III. GRAHAM SCAN — O(n log n)
Alternative: pick the bottom-most point, sort the rest by polar angle around it, then sweep maintaining a stack, popping on non-left turns.

---

## IV. GIFT WRAPPING (Jarvis March) — O(nh)
h = number of hull points. Start at the leftmost point, repeatedly pick the most counterclockwise next point. Good when h is tiny; bad when most points are on the hull.

---

## V. WHAT THE HULL UNLOCKS
- **Diameter** of a point set (farthest pair) → rotating calipers on the hull, O(n)
- **Width**, **smallest enclosing rectangle** → rotating calipers
- **Convexity tests**
- **Point-in-convex-polygon** in O(log n)
- Base for many geometry algorithms

---

## VI. DYNAMIC / UPPER-LOWER HULLS
- **Convex Hull Trick (CHT)** for DP optimization is a different "hull" — the lower/upper envelope of *lines* (see DP universe §15 and Li Chao Tree).
- 3D convex hull exists (incremental / divide-and-conquer) but is much harder.

---

## VII. PRECISION & DEGENERACIES
- Use integer coordinates + integer cross products when possible (exact).
- Handle: all points collinear, duplicate points, < 3 points.

---

## VIII. PROBLEMS
- Erect the Fence (LC 587) — convex hull ⭐
- Largest Triangle Area (LC 812)
- [CSES](https://cses.fi/problemset/) "Convex Hull"
- Many ICPC/CF geometry problems start with a hull
- Rotating calipers: diameter of points, minimum width

---

## IX. COMPLEXITY
- Monotone chain / Graham: O(n log n) (dominated by sort)
- Jarvis: O(nh)

---

**→ Next:** [`03-Line-Sweep.md`](./03-Line-Sweep.md) | Code → [`08-COMPENDIUM-Geometry.md`](./08-COMPENDIUM-Geometry.md)
