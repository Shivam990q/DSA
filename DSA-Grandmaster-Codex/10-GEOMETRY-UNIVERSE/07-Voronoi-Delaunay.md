# 📐 Voronoi Diagrams & Delaunay Triangulation

> *"Two sides of the same coin: partition the plane by nearest site, or triangulate to maximize the smallest angle."*

---

## I. VORONOI DIAGRAM
Given n "sites" (points), the Voronoi diagram partitions the plane into n **cells**, where each cell contains all points closest to one particular site.
- Cell boundaries are perpendicular bisectors between sites.
- Vertices are equidistant from ≥ 3 sites.
- Construction: **Fortune's algorithm** (sweep line), O(n log n).

### Uses
- Nearest-site queries (after preprocessing)
- Facility location, coverage analysis
- Natural neighbor interpolation
- "Closest of many sources" problems

---

## II. DELAUNAY TRIANGULATION
The **dual** of the Voronoi diagram: connect sites whose Voronoi cells share an edge → a triangulation.
- **Property**: maximizes the minimum angle over all triangulations (avoids skinny triangles).
- **Empty circumcircle property**: no point lies inside any triangle's circumcircle.
- Construction: O(n log n) (divide & conquer, incremental, or via Fortune's).

### Uses
- Mesh generation (graphics, FEM)
- Terrain modeling
- Euclidean Minimum Spanning Tree (EMST ⊆ Delaunay edges) ⭐
- Nearest-neighbor graphs

---

## III. THE DUALITY ⭐
```
Voronoi diagram  ←dual→  Delaunay triangulation
  (cells by nearest site)   (triangles of sites)
```
- Voronoi vertex ↔ Delaunay triangle (its circumcenter)
- Voronoi edge ↔ Delaunay edge (perpendicular)

---

## IV. EUCLIDEAN MST CONNECTION
The **Euclidean Minimum Spanning Tree** of n points is a subgraph of the Delaunay triangulation. So:
1. Compute Delaunay (O(n log n)) → O(n) edges
2. Run MST (Kruskal/Prim) on those edges
→ EMST in O(n log n) instead of O(n²) on the complete graph.

---

## V. PRACTICAL NOTE
- Voronoi/Delaunay are **advanced** (Level 7+ / research). Implementations are intricate and precision-sensitive.
- In CP, they appear rarely; when "nearest of many points" arises, often a multi-source BFS/Dijkstra (on a grid) or KD-tree suffices.
- Libraries (CGAL, scipy.spatial) provide robust implementations for real-world use.

---

## VI. RELATED / HIGHER-DIMENSIONAL
- Voronoi/Delaunay generalize to 3D and higher (with rising complexity).
- **Convex hull connection**: Delaunay in d-D ↔ convex hull in (d+1)-D (lifting to a paraboloid).

---

## VII. APPLICATIONS SUMMARY
- GIS / mapping (nearest hospital, coverage)
- Computer graphics (mesh generation)
- Robotics (path planning, clearance)
- Scientific computing (interpolation, FEM meshes)
- ML (natural-neighbor methods)

---

## VIII. PROBLEMS / PRACTICE
- Euclidean MST problems (via Delaunay)
- "Largest empty circle", "nearest site" queries
- Mostly ICPC/research-level; scipy/CGAL for applied work

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | All code → [`08-COMPENDIUM-Geometry.md`](./08-COMPENDIUM-Geometry.md)
