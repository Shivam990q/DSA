# 🌐 Eulerian & Hamiltonian Paths

> *"Eulerian: visit every EDGE once (easy). Hamiltonian: visit every VERTEX once (hard)."*

---

## I. EULERIAN PATH / CIRCUIT (every edge exactly once)
- **Eulerian circuit** (closed): exists iff the graph is connected (ignoring isolated vertices) AND:
  - Undirected: every vertex has **even degree**.
  - Directed: every vertex has **in-degree == out-degree**.
- **Eulerian path** (open): exists iff connected AND:
  - Undirected: exactly **0 or 2** odd-degree vertices (start/end at the odd ones).
  - Directed: exactly one vertex with out−in = 1 (start) and one with in−out = 1 (end), rest balanced.

### Hierholzer's Algorithm — O(V+E) ⭐
Greedily follow unused edges, building sub-tours and splicing them.
```cpp
void euler(int u, vector<vector<int>>& adj, vector<int>& circuit) {
    while (!adj[u].empty()) {
        int v = adj[u].back(); adj[u].pop_back();
        // for undirected, also remove (v,u)
        euler(v, adj, circuit);
    }
    circuit.push_back(u);
}
// reverse(circuit) at the end
```

---

## II. HAMILTONIAN PATH / CYCLE (every vertex exactly once)
- **NP-complete** in general — no known polynomial algorithm.
- Small n: **bitmask DP** (Held-Karp), `dp[mask][i]` = can we visit set `mask` ending at i? O(2ⁿ·n²). Feasible for n ≤ ~20.
- **TSP** is the optimization version (shortest Hamiltonian cycle). See [`../06-DYNAMIC-PROGRAMMING-UNIVERSE/12-Bitmask-DP.md`](../06-DYNAMIC-PROGRAMMING-UNIVERSE/12-Bitmask-DP.md).

---

## III. THE CRUCIAL CONTRAST ⭐
| | Eulerian | Hamiltonian |
|-|----------|-------------|
| Visits | every EDGE once | every VERTEX once |
| Existence test | degree conditions (easy) | NP-complete (hard) |
| Algorithm | Hierholzer O(V+E) | bitmask DP O(2ⁿn²) for small n |

This is a classic "looks similar, wildly different difficulty" pair — a favorite interview/contest trap.

---

## IV. APPLICATIONS
- **Eulerian**: DNA fragment assembly (de Bruijn graphs), "draw without lifting the pen," route inspection (Chinese Postman), reconstruct sequences.
- **Hamiltonian / TSP**: routing, scheduling, the traveling salesman.
- **de Bruijn sequences** (LC 753 Cracking the Safe) — Eulerian circuit on a de Bruijn graph.

---

## V. CHINESE POSTMAN (route inspection)
Find the shortest closed walk traversing every edge at least once. If Eulerian, it's the sum of edge weights; otherwise, duplicate the minimum-weight set of paths between odd-degree vertices (matching).

---

## VI. COMPLEXITY
- Eulerian path/circuit: O(V+E) (Hierholzer).
- Hamiltonian: O(2ⁿ·n²) bitmask DP (small n); NP-hard in general.

---

## VII. PROBLEMS
- Reconstruct Itinerary (LC 332) ⭐ — Eulerian path (Hierholzer)
- Cracking the Safe (LC 753) — Eulerian circuit on de Bruijn graph
- Valid Arrangement of Pairs (LC 2097) — Eulerian path
- Shortest Path Visiting All Nodes (LC 847) — Hamiltonian-ish, BFS+bitmask
- TSP problems ([CSES](https://cses.fi/problemset/) "Hamiltonian Flights")
- CSES "Mail Delivery", "Teleporters Path" (Eulerian)

---

**→ Next:** [`12-Bipartite-Matching.md`](./12-Bipartite-Matching.md)
