# 📐 KD-Tree

> *"A binary tree that partitions space, alternating dimensions — for fast spatial queries."*

---

## I. WHAT IS IT
A **k-dimensional tree** is a binary tree that recursively splits points by alternating coordinate axes (x, then y, then x, ... in 2D).

- At depth d, split by dimension (d mod k).
- Left subtree = points below the split; right = above.

---

## II. CONSTRUCTION — O(n log n)
At each level, choose the splitting coordinate (cycle through dims), pick the median (via nth_element), recurse on the two halves.
```
build(points, depth):
    if empty: return null
    axis = depth % k
    sort/select median by axis
    node = median point
    node.left  = build(points < median on axis, depth+1)
    node.right = build(points > median on axis, depth+1)
```

---

## III. QUERIES

### Nearest Neighbor — O(log n) average, O(n) worst
Descend toward the query point; backtrack, checking the other branch only if the splitting plane is closer than the current best distance.

### Range Search (points in a rectangle/region) — O(√n + result) in 2D
Recurse, pruning subtrees whose bounding region doesn't intersect the query region.

### k-Nearest Neighbors
Maintain a max-heap of size k during the nearest-neighbor traversal.

---

## IV. THE CURSE OF DIMENSIONALITY ⭐
KD-trees work well for **low dimensions** (k ≤ ~10-20). In high dimensions, nearly all points end up "close," queries degrade toward O(n), and KD-trees lose their advantage. For high-dimensional ANN, use **LSH** or specialized structures (HNSW, Annoy, FAISS).

---

## V. ALTERNATIVES (spatial structures)
| Structure | Best for |
|-----------|----------|
| **KD-tree** | low-dim nearest neighbor / range |
| **Quadtree/Octree** | 2D/3D spatial partitioning, images, collision |
| **R-tree** | bounding-box indexing (spatial databases) |
| **BVH** | ray tracing, collision (graphics) |
| **Grid/bucket** | uniform point distributions |
| **LSH / HNSW** | high-dimensional approximate NN |

---

## VI. APPLICATIONS
- Nearest-neighbor search (recommendations, ML, graphics)
- Range queries on 2D points
- Collision detection (games)
- Geographic / spatial databases
- k-NN classification

---

## VII. CP USAGE
KD-trees appear in CP for:
- Offline nearest-point queries
- 2D range queries (though BIT/segment tree on compressed coords often preferred)
- Some "closest point" problems

In CP, they have large constants; often a sweep + BIT is faster for 2D range queries.

---

## VIII. PROBLEMS
- K Closest Points to Origin (LC 973) — heap is simpler here
- Nearest neighbor / range query problems
- CF/ICPC geometry problems with spatial queries

---

**→ Next:** [`07-Voronoi-Delaunay.md`](./07-Voronoi-Delaunay.md)
