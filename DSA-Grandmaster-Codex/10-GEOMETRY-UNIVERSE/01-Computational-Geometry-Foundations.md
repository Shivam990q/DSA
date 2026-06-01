# 📐 Computational Geometry Foundations

> *"Points, vectors, and the cross product. From these three, all geometry flows."*

---

## I. POINTS & VECTORS
```cpp
struct P {
    double x, y;
    P operator+(P o) const { return {x+o.x, y+o.y}; }
    P operator-(P o) const { return {x-o.x, y-o.y}; }
    P operator*(double t) const { return {x*t, y*t}; }
    double dot(P o) const { return x*o.x + y*o.y; }
    double cross(P o) const { return x*o.y - y*o.x; }
    double norm() const { return sqrt(x*x + y*y); }
    double norm2() const { return x*x + y*y; }  // avoid sqrt when possible
};
```
For integer coordinates, use `long long` (cross products can overflow int!).

---

## II. THE CROSS PRODUCT ⭐ (the most important tool)
For 2D vectors u, v: cross = u.x·v.y − u.y·v.x.
- **Sign tells orientation**:
  - cross(B−A, C−A) > 0 → A,B,C turn **counterclockwise (left)**
  - < 0 → **clockwise (right)**
  - = 0 → **collinear**
- **Magnitude** = area of the parallelogram; half = triangle area.

```cpp
int orient(P a, P b, P c) {
    double v = (b-a).cross(c-a);
    return (v > EPS) - (v < -EPS);  // +1 CCW, -1 CW, 0 collinear
}
```

---

## III. THE DOT PRODUCT
u·v = |u||v|cos θ.
- = 0 → perpendicular
- > 0 → angle < 90°
- < 0 → angle > 90°
- Used for projections and angle tests.

---

## IV. DISTANCES
- Point-point: |B − A|
- Point-line, point-segment: projection + clamping
- Use squared distances (norm2) when only comparing — avoids sqrt and precision loss.

---

## V. PRECISION (the eternal hazard) ⭐
Floating point is treacherous:
- Use an **epsilon** for comparisons: `abs(x) < EPS` for "zero", with EPS ≈ 1e-9.
- **Prefer integer arithmetic** when coordinates are integers (cross products stay exact).
- Avoid division when you can multiply.
- Beware accumulated error in long computations.

```cpp
const double EPS = 1e-9;
bool eq(double a, double b) { return abs(a - b) < EPS; }
```

---

## VI. ORIENTATION-BASED PRIMITIVES
With `orient`, you can build:
- **Segment intersection** (do AB and CD cross?)
- **Point in triangle / polygon**
- **Convex hull** (turn directions)
- **Left/right tests** for sweep algorithms

---

## VII. COMMON OPERATIONS
- **Polygon area** (shoelace): ½|Σ (xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ)|
- **Point on segment**: collinear + within bounding box
- **Line intersection**: solve 2×2 system (Cramer's rule)
- **Angle / atan2** for sorting by polar angle

---

## VIII. THE GEOMETRY MINDSET
1. Reduce to cross/dot products (avoid trig when possible).
2. Use integers for exactness when inputs are integers.
3. Handle degenerate cases (collinear, coincident, zero-length).
4. Think in terms of orientation, not coordinates.

---

## IX. PROBLEMS
- Max Points on a Line (LC 149)
- Valid Boomerang (LC 1037), Check if points make a straight line (LC 1232)
- Convex Polygon (LC 469)
- K Closest Points to Origin (LC 973)
- [CSES](https://cses.fi/problemset/) Geometry: Point Location Test, Segment Intersection, Polygon Area, Point in Polygon

---

## X. NOTE
This file is the foundation. Full algorithms (convex hull, sweep line, closest pair) and all code are in [`08-COMPENDIUM-Geometry.md`](./08-COMPENDIUM-Geometry.md).

---

**→ Next:** [`02-Convex-Hull.md`](./02-Convex-Hull.md)
