# 🗂️ Graphs — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ / Java / Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Number of Islands](./01-Number-of-Islands.md) | 200 | Medium | DFS flood-fill → BFS → union-find |
| 02 | [Max Area of Island](./02-Max-Area-of-Island.md) | 695 | Medium | DFS returning size → BFS |
| 03 | [Clone Graph](./03-Clone-Graph.md) | 133 | Medium | DFS + hash map → BFS |
| 04 | [Rotting Oranges](./04-Rotting-Oranges.md) | 994 | Medium | multi-source BFS |
| 05 | [Pacific Atlantic Water Flow](./05-Pacific-Atlantic-Water-Flow.md) | 417 | Medium | brute per-cell DFS → reverse DFS from oceans |
| 06 | [Surrounded Regions](./06-Surrounded-Regions.md) | 130 | Medium | border DFS/BFS → union-find |
| 07 | [Course Schedule](./07-Course-Schedule.md) | 207 | Medium | DFS cycle detection → Kahn's BFS |
| 08 | [Course Schedule II](./08-Course-Schedule-II.md) | 210 | Medium | Kahn's BFS → DFS post-order |
| 09 | [Number of Connected Components](./09-Number-of-Connected-Components.md) | 323 | Medium | DFS/BFS count → union-find |
| 10 | [Redundant Connection](./10-Redundant-Connection.md) | 684 | Medium | union-find → DFS cycle |
| 11 | [Word Ladder](./11-Word-Ladder.md) | 127 | Hard | BFS → bidirectional BFS |
| 12 | [Walls and Gates](./12-Walls-And-Gates.md) | 286 | Medium | per-gate BFS → multi-source BFS |
| 13 | [Graph Valid Tree](./13-Graph-Valid-Tree.md) | 261 | Medium | union-find → DFS/BFS connectivity |

---

## 🎯 The pattern family

Grids ARE graphs. Almost every interview graph problem reduces to one of four templates. Learn to spot which one applies from the problem's phrasing.

### 1. Flood-fill (connected-component traversal on a grid)
Trigger words: *"islands", "regions", "area", "connected cells"*. Scan the grid; every unvisited target cell launches a DFS/BFS that "drowns" (marks visited) the entire blob. Used by: Number of Islands, Max Area of Island, Surrounded Regions, Pacific Atlantic.

### 2. BFS for shortest path / level-by-level spread
Trigger words: *"minimum steps", "shortest transformation", "time to spread", "nearest"*. BFS explores in expanding rings, so the first time you reach a node is the shortest unweighted distance. **Multi-source BFS** seeds the queue with all starting points at once. Used by: Rotting Oranges, Walls and Gates, Word Ladder.

### 3. Topological sort (ordering a DAG / detecting cycles in a directed graph)
Trigger words: *"prerequisites", "ordering", "dependencies", "can you finish"*. Either Kahn's algorithm (repeatedly remove in-degree-0 nodes) or DFS with a 3-color recursion-stack check. If you cannot order every node, a cycle exists. Used by: Course Schedule, Course Schedule II.

### 4. Union-Find (Disjoint Set Union — dynamic connectivity)
Trigger words: *"connected components", "redundant edge", "valid tree", "merge groups"*. Maintain a forest of sets with path compression + union by rank/size for near-O(1) `find`/`union`. Used by: Number of Connected Components, Redundant Connection, Graph Valid Tree (and as an alternative for Surrounded Regions).

---

## 🧭 Decision guide

```
Is it a grid with "blobs" to count/measure?        → flood-fill DFS/BFS
Do I need the MINIMUM number of steps/levels?       → BFS (multi-source if many starts)
Directed graph with ordering/dependency/cycle?      → topological sort (Kahn or DFS)
Undirected "are these connected / one extra edge"?  → union-find
```

---

**→ Start:** [`01-Number-of-Islands.md`](./01-Number-of-Islands.md) | Back to [vault index](../00-Index.md)
