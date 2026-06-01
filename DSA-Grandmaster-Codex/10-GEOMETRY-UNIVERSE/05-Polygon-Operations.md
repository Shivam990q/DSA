# 📐 Polygon Operations

> *"Area, containment, and the secrets hidden in a polygon's vertices."*

---

## I. POLYGON AREA — SHOELACE FORMULA ⭐
For polygon with vertices (x₀,y₀), ..., (xₙ₋₁,yₙ₋₁) in order:
```
Area = ½ |Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|   (indices mod n)
```
```cpp
double polygonArea(vector<P>& p) {
    int n = p.size();
    double a = 0;
    for (int i = 0; i < n; i++)
        a += p[i].cross(p[(i+1)%n]);
    return abs(a) / 2.0;
}
```
- The **sign** of the sum tells orientation (CCW positive, CW negative).

---

## II. POINT IN POLYGON
### Ray casting (any simple polygon) — O(n)
Cast a ray from the point; count edge crossings. Odd = inside, even = outside.

### Convex polygon — O(log n)
Binary search the wedge (triangle fan from vertex 0) containing the point.

### Winding number
Alternative robust method: sum signed angles / count signed crossings.

---

## III. PICK'S THEOREM (lattice polygons)
For a polygon with integer (lattice) vertices:
```
Area = I + B/2 − 1
```
where I = interior lattice points, B = boundary lattice points.
- B on an edge from (x₁,y₁) to (x₂,y₂) = gcd(|x₂−x₁|, |y₂−y₁|).
- Lets you count lattice points from area, or vice versa.

---

## IV. CONVEXITY TEST
A polygon is convex iff all consecutive cross products (turns) have the same sign. O(n).

---

## V. POLYGON CENTROID
Centroid (center of mass) of a polygon has a closed form using the same cross-product sums as the shoelace area.

---

## VI. POLYGON CLIPPING & INTERSECTION
- **Sutherland-Hodgman**: clip a polygon against a convex polygon (half-planes).
- **Convex polygon intersection**: O(n+m).
- General polygon boolean ops (union/intersection/difference): Weiler-Atherton (complex).

---

## VII. PERIMETER & OTHER MEASURES
- Perimeter: sum of edge lengths.
- Diameter of a convex polygon: rotating calipers, O(n).
- Width: minimum distance between parallel supporting lines.

---

## VIII. PROBLEMS
- Polygon area ([CSES](https://cses.fi/problemset/) "Polygon Area")
- Point in polygon (CSES "Point in Polygon")
- Lattice points inside polygon (CSES "Polygon Lattice Points" — Pick's theorem)
- Convex polygon test (LC 469)
- Largest triangle / Erect the Fence (LC 587, 812)

---

## IX. PRECISION NOTE
For lattice problems, keep everything in integers (shoelace with `long long`, gcd for boundary points). For floating polygons, mind EPS.

---

**→ Next:** [`06-KD-Tree.md`](./06-KD-Tree.md)
