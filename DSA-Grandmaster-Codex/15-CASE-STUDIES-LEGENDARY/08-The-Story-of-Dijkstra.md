# 📖 Case Study: The Story of Dijkstra's Algorithm

> *"In 1959, while drinking coffee in Amsterdam, Edsger Dijkstra invented an algorithm that would route the internet."*

---

## I. THE PROBLEM

Given a weighted graph G = (V, E) with non-negative edge weights, find the shortest path from source s to all other vertices.

---

## II. THE ORIGIN

In 1956, Edsger W. Dijkstra was asked to demonstrate the new ARMAC computer at a public exhibition. He needed a problem the audience could understand.

He chose: shortest route between two Dutch cities.

> *"What is the shortest way to travel from Rotterdam to Groningen?"*

He had no paper, only a pencil. He thought for **20 minutes** in a café — and invented what we now call Dijkstra's algorithm.

He published it in 1959, three pages long.

---

## III. THE BRUTE FORCE — O((V+E) × V) or worse

For each vertex v, find the shortest path by trying all paths. Exponential without memoization.

Or: Bellman-Ford runs in O(V × E) — works but slow.

---

## IV. DIJKSTRA'S OBSERVATION

> **"At any moment, if I know the closest unvisited vertex's distance, that distance is FINAL."**

**Why?** All edge weights are non-negative. Any "longer path" via uncomputed vertices can only get longer.

This is the **greedy choice property** for shortest paths.

---

## V. THE ALGORITHM

```
1. dist[s] = 0; dist[v] = ∞ for all other v
2. Maintain set S of vertices with finalized distance (initially empty)
3. Repeat V times:
   a. Pick vertex u not in S with smallest dist[u]
   b. Add u to S
   c. For each neighbor v of u: if dist[u] + w(u, v) < dist[v]:
      dist[v] = dist[u] + w(u, v)  (relaxation)
```

---

## VI. EFFICIENT IMPLEMENTATION

### With a min-heap (priority queue): O((V + E) log V)
```cpp
vector<long long> dijkstra(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<long long> dist(n, LLONG_MAX);
    dist[src] = 0;
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;  // stale entry
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

### With Fibonacci heap: O(E + V log V)
Theoretically better. Constants too high to matter in practice.

---

## VII. WHY IT WORKS — THE PROOF

**Invariant**: when vertex u is finalized, dist[u] = true shortest distance.

**Proof by induction on order of finalization**:

Base: u = s. dist[s] = 0. ✓

Inductive step: suppose all previously finalized vertices have correct distances. Consider u just finalized with dist[u] = d.

Suppose for contradiction there's a shorter path P from s to u with cost < d.

P must contain some vertex v not yet finalized (otherwise it would be a path through finalized vertices, which we've already considered through relaxation).

Let v' be the **first** non-finalized vertex on P. By inductive hypothesis, the part of P up to v's predecessor is the true shortest. So dist[v'] (after our relaxations) ≤ length of P up to v'.

But:
- dist[u] is the smallest among non-finalized → dist[u] ≤ dist[v']
- length of P up to v' ≤ length of full P (non-negative weights from v' onward)

So dist[u] ≤ length of P. But we assumed length of P < dist[u]. **Contradiction.** □

---

## VIII. CRITICAL ASSUMPTION

> **Non-negative weights are required.**

With negative weights, the greedy choice fails — a longer path might "discount" via a negative edge later.

For negative weights: use Bellman-Ford (O(VE)).

---

## IX. APPLICATIONS

### 1. Routing
- Internet routing (OSPF protocol uses Dijkstra)
- Maps and GPS (Google Maps uses Dijkstra-derivatives + heuristics)

### 2. Network problems
- Network delay time
- Min cost path with constraints

### 3. Reduction problems
- "Minimum effort path" problems
- "Cheapest flights with K stops" (BF/DP variant)

### 4. CP problems with state augmentation
- Dijkstra on (city, time_used) state
- Dijkstra on (cell, obstacles_remaining)

---

## X. VARIANTS

### Bidirectional Dijkstra
Run Dijkstra from both source and target. They meet in the middle. Often 2× faster in practice for single-pair queries.

### A* search
Dijkstra + heuristic h(v) estimating distance to target. Faster than vanilla Dijkstra when good heuristic available.

### Contraction Hierarchies (Google Maps)
Pre-process road network: rank vertices by importance; "contract" them by adding shortcuts. Bidirectional Dijkstra on contracted graph: 1000× faster on continental-scale road networks.

### 0-1 BFS
Special case for weights only 0 or 1: replace priority queue with deque. O(V + E).

---

## XI. MENTAL MODEL

> **"Greedy works on shortest paths because of the triangle inequality + non-negative weights.  
>  The closest unfinalized point cannot be 'reached cheaper' via a detour."**

This thinking — "what local optimum extends to global?" — is the **essence of greedy**.

---

## XII. THE LEGACY

Dijkstra published this in 1959, alongside many other foundational results:
- Structured programming
- Semaphores (concurrency)
- "GO TO Considered Harmful"
- Self-stabilizing systems

He is often considered the father of structured programming and one of the most important computer scientists of the 20th century.

---

## XIII. PROBLEMS TO PRACTICE

1. Network Delay Time (LC 743)
2. Path with Maximum Probability (LC 1514)
3. Cheapest Flights with K Stops (LC 787)
4. Path with Minimum Effort (LC 1631)
5. Minimum Cost to Make at Least One Valid Path (LC 1368)
6. Swim in Rising Water (LC 778)
7. Minimum Knight Moves (LC 1197) — BFS variant
8. Shortest Path Visiting All Nodes (LC 847) — BFS + bitmask
9. Minimum Cost to Reach Destination in Time (LC 1928)
10. Number of Restricted Paths (LC 1786)

CP-level:
11. [CSES](https://cses.fi/problemset/) "Graph Algorithms" — Shortest Routes I, II
12. CF problems tagged "shortest paths"

---

**→ Next case study:** [`09-The-Story-of-Tarjan.md`](./09-The-Story-of-Tarjan.md)
