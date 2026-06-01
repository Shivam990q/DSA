# 📐 Line Sweep (Sweep Line)

> *"Imagine a vertical line sweeping left to right. Process events as it touches them."*

---

## I. THE PARADIGM
A vertical (or horizontal) line moves across the plane. As it passes "events" (point/segment endpoints), you update a data structure (often a balanced BST / set / heap keyed by the other coordinate) and compute answers.

Converts 2D problems into a sequence of 1D updates ordered by x.

---

## II. THE GENERAL TEMPLATE
```
1. Create events (e.g., segment start = +, segment end = -); sort by x.
2. Maintain an "active set" (ordered by y) of currently-intersected objects.
3. Process events in order; at each, update the active set and record results.
```

---

## III. CLASSIC APPLICATIONS

### Segment intersection (Bentley-Ottmann) — O((n+k) log n)
k = number of intersections. Sweep; maintain active segments ordered by y; check neighbors for intersection at events.

### Skyline problem (LC 218) ⭐
Events = building edges (left = add height, right = remove). Maintain a max-heap / multiset of active heights. When the max height changes, emit a keypoint. O(n log n).

### Maximum overlapping intervals / meeting rooms (LC 253)
1D sweep: sort start (+1) and end (−1) events; running counter; track max.

### Rectangle area union (LC 850) ⭐
Sweep x; maintain total covered y-length using a segment tree over compressed y-coordinates; area += covered_y × Δx.

### Closest pair (sweep variant)
Sweep x; maintain points within the current best distance in a set ordered by y.

---

## IV. EVENT TYPES
- **Point events**: a point is reached
- **Interval/segment events**: start (open) / end (close)
- **Query events** (offline): answer a query when the sweep reaches its x

Often combined with **coordinate compression** (map large coords to small indices) and a **segment tree / BIT / multiset** as the active structure.

---

## V. 1D SWEEP (the simplest, super common)
Many "interval" problems are 1D sweeps:
- Merge intervals (LC 56)
- Meeting rooms II (LC 253)
- Car pooling (LC 1094), My Calendar series (LC 729/731/732)
- Employee free time (LC 759)

Pattern: turn each interval [s, e] into events (s, +1) and (e, −1); sort; sweep with a counter or a structure.

---

## VI. PROBLEMS
- The Skyline Problem (LC 218) ⭐
- Rectangle Area II (LC 850) ⭐
- Meeting Rooms II (LC 253), Car Pooling (LC 1094)
- My Calendar I/II/III (LC 729/731/732)
- Employee Free Time (LC 759)
- Number of intersecting segments (CF/CSES)

---

## VII. WHEN TO REACH FOR SWEEP LINE
- 2D problems about intervals, rectangles, segments, points
- "How many overlap at once?", "total covered area/length", "any intersection?"
- Offline queries that can be ordered by a coordinate

---

**→ Next:** [`04-Closest-Pair.md`](./04-Closest-Pair.md)
