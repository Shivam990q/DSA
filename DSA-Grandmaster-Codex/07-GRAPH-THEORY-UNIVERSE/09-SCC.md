# 🌐 Strongly Connected Components (SCC)

> *"In a directed graph, which groups of nodes can all reach each other?"*

---

## I. DEFINITION
A **strongly connected component** is a maximal set of vertices where every vertex can reach every other (via directed paths). SCCs partition a directed graph.

The **condensation** (contract each SCC to one node) is always a **DAG** — enabling DAG DP on top of SCCs.

---

## II. TARJAN'S ALGORITHM (single DFS) ⭐
Uses low-link + an explicit stack of "active" vertices.
```cpp
int timer = 0, sccCount = 0;
vector<int> tin, low, comp; vector<bool> onStk; stack<int> stk;

void dfs(int u, vector<vector<int>>& adj) {
    tin[u] = low[u] = timer++;
    stk.push(u); onStk[u] = true;
    for (int v : adj[u]) {
        if (tin[v] == -1) { dfs(v, adj); low[u] = min(low[u], low[v]); }
        else if (onStk[v]) low[u] = min(low[u], tin[v]);
    }
    if (low[u] == tin[u]) {             // u is an SCC root
        while (true) {
            int w = stk.top(); stk.pop(); onStk[w] = false;
            comp[w] = sccCount;
            if (w == u) break;
        }
        sccCount++;
    }
}
```
O(V+E), one pass.

---

## III. KOSARAJU'S ALGORITHM (two DFS)
1. DFS the original graph, push nodes onto a stack in finish order.
2. Reverse all edges.
3. Pop nodes from the stack; DFS on the reversed graph — each DFS tree is one SCC.

Conceptually simpler; two passes. Also O(V+E).

---

## IV. THE CONDENSATION DAG ⭐
After finding SCCs, build a new graph with one node per SCC and edges between SCCs. This is a DAG. Use it to:
- Topologically order SCCs
- DAG DP (longest path, counting, reachability)
- Find source/sink SCCs

---

## V. APPLICATIONS
- **2-SAT** (implication graph; variable & negation in the same SCC ⟹ unsatisfiable). See [`10-2-SAT.md`](./10-2-SAT.md).
- **Condensing cyclic dependencies** → DAG, then DP.
- Finding mutually reachable groups (e.g., who-influences-whom networks).
- Minimum edges to make the whole graph strongly connected (source/sink SCC counting).

---

## VI. COMPLEXITY
O(V + E) for both Tarjan and Kosaraju.

---

## VII. PROBLEMS
- Count SCCs ([CSES](https://cses.fi/problemset/) "Planets and Kingdoms")
- Strongly Connected / condensation problems
- 2-SAT problems (CSES "Giant Pizza")
- CF problems tagged "graphs" + "dfs and similar"
- Critical for many ICPC graph problems

---

## VIII. NOTE
SCC + condensation is one of the most reusable advanced graph tools. Combine with the low-link concept from [`08-Bridges-Articulation.md`](./08-Bridges-Articulation.md). (Story: [`../15-CASE-STUDIES-LEGENDARY/09-The-Story-of-Tarjan.md`](../15-CASE-STUDIES-LEGENDARY/09-The-Story-of-Tarjan.md).)

---

**→ Next:** [`10-2-SAT.md`](./10-2-SAT.md)
