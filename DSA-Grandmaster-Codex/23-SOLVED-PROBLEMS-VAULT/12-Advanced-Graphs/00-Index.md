# 🗂️ Advanced Graphs — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ / Java / Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Network Delay Time](./01-Network-Delay-Time.md) | 743 | Medium | Dijkstra → Bellman-Ford |
| 02 | [Cheapest Flights Within K Stops](./02-Cheapest-Flights-K-Stops.md) | 787 | Medium | Bellman-Ford (k rounds) → BFS layers |
| 03 | [Min Cost to Connect All Points](./03-Min-Cost-Connect-Points.md) | 1584 | Medium | Prim's MST → Kruskal's MST |
| 04 | [Swim in Rising Water](./04-Swim-In-Rising-Water.md) | 778 | Hard | Dijkstra (min-max path) → binary search + DFS → Kruskal/DSU |
| 05 | [Reconstruct Itinerary](./05-Reconstruct-Itinerary.md) | 332 | Hard | Hierholzer's Eulerian path |
| 06 | [Min Cost to Make Network Connected](./06-Min-Cost-Make-Network-Connected.md) | 1319 | Medium | Union-Find → DFS component count |

---

## 🎯 The pattern family

This tier is about **weights** and **constraints** on top of plain connectivity. Four algorithm families cover nearly all of it.

### 1. Dijkstra — single-source shortest path, non-negative weights
A min-heap repeatedly finalizes the closest unsettled node. Each node is popped (settled) once with its true shortest distance. Variants generalize the "cost" of a path: it can be a sum of weights (Network Delay Time) or the **maximum edge** on the path (Swim in Rising Water). Trigger words: *"shortest time", "minimum cost path", "earliest arrival"* with non-negative edges.

### 2. Bellman-Ford — shortest path with a bound on edges / negative weights
Relax all edges repeatedly. After `i` rounds, distances using at most `i` edges are finalized. This bounded-rounds property is exactly what "at most K stops" needs. Trigger words: *"at most K edges/stops", "negative weights", "detect negative cycle"*.

### 3. MST (Prim / Kruskal) — cheapest way to connect everything
Connect all nodes with minimum total edge weight, no cycles. **Prim** grows a tree from a seed using a min-heap; **Kruskal** sorts edges and unions with DSU, skipping cycles. Trigger words: *"connect all", "minimum total cost to link", "spanning"*.

### 4. Eulerian path (Hierholzer) — use every edge exactly once
When you must traverse **every edge** once (e.g., use every ticket), it is an Eulerian path. Hierholzer's algorithm walks greedily, backtracking dead-ends into the route in post-order. Trigger words: *"use all edges/tickets exactly once", "itinerary"*.

Union-Find also appears as a stand-alone tool for component counting (Min Cost to Make Network Connected) and inside Kruskal.

---

## 🧭 Decision guide

```
Shortest path, non-negative weights, no edge limit?     → Dijkstra (min-heap)
Shortest path with "at most K edges/stops" or negatives? → Bellman-Ford (bounded rounds)
Minimum total cost to connect ALL nodes?                 → MST (Prim heap / Kruskal DSU)
Path cost = MAX edge (not sum)?                          → Dijkstra on max, or binary search + DFS
Must use every edge exactly once?                        → Eulerian path (Hierholzer)
Just counting components / spare-edge logic?             → Union-Find
```

---

**→ Start:** [`01-Network-Delay-Time.md`](./01-Network-Delay-Time.md) | Back to [vault index](../00-Index.md)
