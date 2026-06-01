# 🌐 Bipartite Matching

> *"Pair up two groups optimally — jobs to workers, students to projects."*

---

## I. BIPARTITE GRAPHS
Vertices split into two sets L and R; edges only go between sets (never within). Test bipartiteness by 2-coloring (BFS/DFS): if you can 2-color with no conflict, it's bipartite (equivalently, no odd cycle).

---

## II. MAXIMUM BIPARTITE MATCHING
A **matching** is a set of edges with no shared vertices. Maximum matching = largest such set.

### Kuhn's Algorithm (augmenting paths) ⭐
For each left vertex, try to find an augmenting path (DFS); if found, the matching grows by 1.
```cpp
vector<int> matchR;   // matchR[r] = left vertex matched to r, or -1
bool tryKuhn(int u, vector<vector<int>>& adj, vector<bool>& used) {
    for (int v : adj[u]) {
        if (used[v]) continue;
        used[v] = true;
        if (matchR[v] == -1 || tryKuhn(matchR[v], adj, used)) {
            matchR[v] = u; return true;
        }
    }
    return false;
}
int maxMatching(int nL, int nR, vector<vector<int>>& adj) {
    matchR.assign(nR, -1); int res = 0;
    for (int u = 0; u < nL; u++) {
        vector<bool> used(nR, false);
        if (tryKuhn(u, adj, used)) res++;
    }
    return res;
}
```
O(V·E).

### Hopcroft-Karp — O(E·√V)
Faster for large bipartite graphs; finds multiple augmenting paths per phase via BFS layering + DFS.

---

## III. KÖNIG'S THEOREM & DUALITY ⭐
In bipartite graphs:
- **Max matching = Min vertex cover** (König's theorem).
- **Max independent set = V − max matching**.
- **Min path cover in a DAG = V − max matching** (of the split graph).

These dualities let you solve many problems by computing a matching.

---

## IV. MATCHING VIA MAX FLOW
Add a source → all L (cap 1), all R → sink (cap 1), edges L→R (cap 1). **Max flow = max matching.** (See [`14-Network-Flow.md`](./14-Network-Flow.md).) For weighted/assignment, use min-cost max-flow or the Hungarian algorithm.

---

## V. ASSIGNMENT PROBLEM (weighted)
Match L to R minimizing total cost (perfect matching in a weighted complete bipartite graph). Solve with the **Hungarian algorithm** O(n³) or min-cost max-flow.

---

## VI. APPLICATIONS
- Job/task assignment (workers to tasks)
- Scheduling (students to slots, courses to rooms)
- Resource allocation
- Maximum independent set / minimum vertex cover (via König)
- Minimum path cover in DAGs

---

## VII. COMPLEXITY
- Kuhn's: O(V·E)
- Hopcroft-Karp: O(E·√V)
- Hungarian (weighted): O(n³)

---

## VIII. PROBLEMS
- Maximum Bipartite Matching ([CSES](https://cses.fi/problemset/) "School Dance")
- Is Graph Bipartite (LC 785), Possible Bipartition (LC 886)
- Maximum students / assignment problems
- Minimum path cover in DAG
- CF problems tagged "matchings" / "flows"

---

**→ Next:** [`13-General-Matching.md`](./13-General-Matching.md)
