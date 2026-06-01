# 📐 Computational Geometry Compendium

---

## 01 — POINT, VECTOR, BASIC OPS

```cpp
struct Point {
    double x, y;
    Point operator-(const Point& o) const { return {x - o.x, y - o.y}; }
    Point operator+(const Point& o) const { return {x + o.x, y + o.y}; }
    double dot(const Point& o) const { return x * o.x + y * o.y; }
    double cross(const Point& o) const { return x * o.y - y * o.x; }
    double norm() const { return sqrt(x*x + y*y); }
};

double dist(Point a, Point b) { return (a - b).norm(); }
```

### Cross product sign → orientation
- Cross(B − A, C − A) > 0: A, B, C are CCW
- Cross < 0: CW
- Cross == 0: collinear

```cpp
int orient(Point a, Point b, Point c) {
    double v = (b - a).cross(c - a);
    if (v > 0) return 1;
    if (v < 0) return -1;
    return 0;
}
```

---

## 02 — LINE / SEGMENT INTERSECTION

### Two lines (infinite) ax + by = c
Cramer's rule.

### Two segments
1. Bounding box check (early reject).
2. Orientation tests:
   - segments AB and CD intersect iff orient(A,B,C) ≠ orient(A,B,D) AND orient(C,D,A) ≠ orient(C,D,B).
3. Special: collinear case (project on x or y axis, check overlap).

---

## 03 — POLYGON AREA (Shoelace formula)

```cpp
double polygonArea(vector<Point>& p) {
    int n = p.size();
    double a = 0;
    for (int i = 0; i < n; i++)
        a += p[i].cross(p[(i+1) % n]);
    return abs(a) / 2;
}
```

For lattice points: **Pick's theorem**: A = I + B/2 − 1, where I = interior lattice points, B = boundary.

---

## 04 — POINT IN POLYGON

### Ray casting (works for any simple polygon)
Cast a horizontal ray from p; count edge crossings; odd = inside, even = outside.

### Convex polygon: O(log n) with binary search
Binary search for the wedge containing p.

---

## 05 — CONVEX HULL

### Andrew's monotone chain (O(n log n))
```cpp
vector<Point> convexHull(vector<Point> p) {
    sort(p.begin(), p.end(), [](const Point& a, const Point& b){
        return a.x < b.x || (a.x == b.x && a.y < b.y);
    });
    int n = p.size(), k = 0;
    vector<Point> h(2 * n);
    // Lower hull
    for (int i = 0; i < n; i++) {
        while (k >= 2 && (h[k-1] - h[k-2]).cross(p[i] - h[k-2]) <= 0) k--;
        h[k++] = p[i];
    }
    // Upper hull
    int t = k + 1;
    for (int i = n - 2; i >= 0; i--) {
        while (k >= t && (h[k-1] - h[k-2]).cross(p[i] - h[k-2]) <= 0) k--;
        h[k++] = p[i];
    }
    h.resize(k - 1);
    return h;
}
```

### Graham scan
Sort by polar angle from bottom-most point; sweep with stack rejecting non-CCW turns.

---

## 06 — CLOSEST PAIR OF POINTS — O(n log n)

D&C approach:
1. Sort by x.
2. Recursively find closest pair in left and right halves.
3. Check pairs across the dividing line within strip of width 2δ.
4. Crucially, in the strip, each point need only compare to ≤ 7 next points (sorted by y).

---

## 07 — SWEEP LINE

### Segment intersection (Bentley-Ottmann)
Process events (segment endpoints + intersections) in x order. Maintain set of active segments by y. Time: O((n + k) log n) where k = intersections.

### Skyline problem (LC 218)
Sweep x; events = building start/end. Maintain max heap of active heights. When max height changes, output keypoint.

### Maximum overlapping intervals
Sort start/end events; sweep; maintain count.

---

## 08 — KD-TREE

Recursive 2D BST splitting alternately on x, y. Range/nearest-neighbor queries in O(log n) avg.

---

## 09 — ROTATING CALIPERS

For convex polygon: sweep two parallel "calipers" rotating around the hull. Solves diameter, width, min bounding rect in O(n) post-hull.

---

## 10 — VORONOI / DELAUNAY

### Voronoi diagram
Partition plane into regions where each region is closer to one site than any other.

### Delaunay triangulation
Dual of Voronoi. Triangulation maximizing minimum angle.

Construction: O(n log n) (Fortune's, randomized incremental).

---

## 11 — TYPICAL PROBLEMS

1. Compute polygon area
2. Point in polygon
3. Convex hull
4. Closest pair of points
5. Number of segment intersections
6. Maximum number of points on a line (LC 149)
7. K closest points to origin (LC 973)
8. Erect the fence (LC 587) — convex hull
9. Largest triangle area
10. Minimum area rectangle (LC 939)
11. Valid square / triangle / boomerang
12. Skyline problem (LC 218)
13. Rectangle area I, II (LC 223, 850)
14. Maximum sub-axis-aligned rectangle in matrix
15. Number of lattice points in triangle (Pick's)

### CP-level
16. [CSES](https://cses.fi/problemset/) Geometry
17. CF problems "geometry" tagged

---

## 12 — PRECISION HAZARDS

Floating point gotchas:
- Use `< -EPS` and `> EPS` for sign checks (EPS ≈ 1e-9)
- Avoid division when possible (multiply both sides)
- Use `long long` for integer coordinates when feasible
- Cross product can overflow int → use long long

---

## 13 — RECOMMENDED READING

- **de Berg et al.**, *Computational Geometry: Algorithms and Applications* ⭐
- **O'Rourke**, *Computational Geometry in C*
- **[CP-Algorithms.com](https://cp-algorithms.com)** geometry section

---

**→ Next:** [`../11-ADVANCED-PARADIGMS-UNIVERSE/00-Index.md`](../11-ADVANCED-PARADIGMS-UNIVERSE/00-Index.md)
