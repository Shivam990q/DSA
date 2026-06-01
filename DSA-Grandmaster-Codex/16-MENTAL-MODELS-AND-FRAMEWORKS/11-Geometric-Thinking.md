# 📐 Geometric Thinking

> *"Many problems live in space. Coordinates, distances, angles, and areas are your tools."*

---

## THE WORLDVIEW
When data has spatial structure (2D/3D points, intervals on a line, shapes), geometric reasoning unlocks elegant solutions.

## THE TRIGGERS
- 2D/3D coordinates
- Polygons, lines, circles
- Distances, intersections, areas
- Intervals (1D geometry)

## KEY PRIMITIVES
- **Cross product**: orientation (CCW/CW/collinear), area
- **Dot product**: projection, angle
- **Shoelace formula**: polygon area
- **Sweep line**: process events left-to-right

## MANIFESTATIONS
- Convex hull (Graham scan, Andrew monotone chain)
- Closest pair of points (divide & conquer)
- Line segment intersection (sweep line)
- Point in polygon (ray casting)
- KD-tree (nearest neighbor)
- Rotating calipers (diameter, width)

## THE 1D INSIGHT
Intervals are 1D geometry. "Merge intervals," "max overlapping," and "meeting rooms" are geometric sweeps in 1D.

## PRECISION HAZARDS
- Use epsilon comparisons for floats (`< -EPS`, `> EPS`)
- Prefer integer arithmetic (cross products) when coordinates are integers
- Watch for overflow in cross products (use long long)

## EXERCISE
1. Is point P inside triangle ABC? → 3 cross products, same sign
2. Do segments AB and CD intersect? → orientation tests
3. Area of polygon → shoelace formula
4. Max points on a line → group by slope (with care for precision)

---

**→ Next:** [`12-Algebraic-Thinking.md`](./12-Algebraic-Thinking.md) | Deep dive: [`../10-GEOMETRY-UNIVERSE/00-Index.md`](../10-GEOMETRY-UNIVERSE/00-Index.md)
