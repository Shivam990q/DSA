# 📖 Case Study: Tarjan and the Power of DFS

> *"Robert Tarjan looked at depth-first search and saw not a traversal, but a microscope."*

---

## I. THE MAN

Robert Endre Tarjan (b. 1948) is one of the most prolific algorithm designers in history. Turing Award winner (1986, with John Hopcroft). His contributions:
- DFS-based bridges, articulation points
- Strongly connected components (Tarjan's SCC)
- Lowest common ancestor (offline)
- Splay trees
- Fibonacci heaps
- Link-cut trees
- Union-Find amortized analysis (α(n))

His superpower: seeing the **structure DFS reveals**.

---

## II. THE INSIGHT — DFS DISCOVERY TIMES

When you DFS a graph, each vertex gets:
- **discovery time** `tin[v]`: when first visited
- **finish time** `tout[v]`: when fully processed

These two numbers + the DFS tree structure encode an astonishing amount about the graph.

### The "low-link" value
> `low[v]` = the smallest discovery time reachable from v's subtree using at most one back edge.

This single value powers bridges, articulation points, and SCCs.

---

## III. BRIDGES (cut edges)

A **bridge** is an edge whose removal disconnects the graph.

**Tarjan's observation**: edge (u, v) (v is child of u in DFS tree) is a bridge iff:
> `low[v] > tin[u]`

Meaning: v's subtree cannot reach u or any ancestor of u without using edge (u,v).

```cpp
int timer = 0;
vector<int> tin, low;
vector<bool> visited;
vector<pair<int,int>> bridges;

void dfs(int u, int parent, vector<vector<int>>& adj) {
    visited[u] = true;
    tin[u] = low[u] = timer++;
    for (int v : adj[u]) {
        if (v == parent) continue;
        if (visited[v]) {
            low[u] = min(low[u], tin[v]);   // back edge
        } else {
            dfs(v, u, adj);
            low[u] = min(low[u], low[v]);   // tree edge
            if (low[v] > tin[u]) bridges.push_back({u, v});  // BRIDGE!
        }
    }
}
```

O(V + E).

---

## IV. ARTICULATION POINTS (cut vertices)

A vertex whose removal disconnects the graph.

**Tarjan's condition**: vertex u is an articulation point iff:
- u is the DFS root with ≥ 2 children, OR
- u is non-root and has a child v with `low[v] >= tin[u]`

Same DFS, slightly different condition.

---

## V. STRONGLY CONNECTED COMPONENTS

An SCC is a maximal set of vertices where every vertex reaches every other.

**Tarjan's SCC** (single DFS):
- Maintain a stack of "active" vertices
- When `low[u] == tin[u]`, u is the "root" of an SCC; pop the stack until u to form the component

```cpp
int timer = 0, sccCount = 0;
vector<int> tin, low, sccId;
vector<bool> onStack;
stack<int> stk;

void dfs(int u, vector<vector<int>>& adj) {
    tin[u] = low[u] = timer++;
    stk.push(u); onStack[u] = true;
    for (int v : adj[u]) {
        if (tin[v] == -1) {
            dfs(v, adj);
            low[u] = min(low[u], low[v]);
        } else if (onStack[v]) {
            low[u] = min(low[u], tin[v]);
        }
    }
    if (low[u] == tin[u]) {  // root of SCC
        while (true) {
            int w = stk.top(); stk.pop(); onStack[w] = false;
            sccId[w] = sccCount;
            if (w == u) break;
        }
        sccCount++;
    }
}
```

O(V + E), single pass. (Kosaraju's needs two passes.)

---

## VI. THE GENERAL PRINCIPLE

> **"DFS imposes a tree structure on the graph.  
>  The discovery/finish times + low-link values encode global structure.  
>  Reading these numbers reveals bridges, cut vertices, SCCs, and more."**

This is **the power of structured traversal**: a simple DFS, augmented with bookkeeping, exposes deep properties.

---

## VII. UNION-FIND AMORTIZED ANALYSIS

Tarjan (with Van Leeuwen) proved that Union-Find with **path compression + union by rank** achieves **O(α(n))** amortized per operation, where α is the inverse Ackermann function — essentially constant (α(n) ≤ 4 for any n in the universe).

This was a landmark in **amortized analysis**.

---

## VIII. SPLAY TREES & LINK-CUT TREES

Tarjan (with Sleator) invented:
- **Splay trees** (1985): self-adjusting BSTs, amortized O(log n)
- **Link-cut trees**: dynamic tree connectivity in O(log n) amortized

These power advanced data structure problems.

---

## IX. MENTAL MODEL FROM TARJAN

When facing a graph problem, ask:
1. **What does DFS reveal here?**
2. **What do discovery/finish times tell me?**
3. **Is there a low-link-style value that captures the structure?**
4. **Can I bookkeep during traversal to extract the answer?**

This "augmented traversal" thinking is broadly powerful.

---

## X. PROBLEMS TO PRACTICE

1. Critical Connections (LC 1192) — bridges
2. Find articulation points (GFG)
3. Number of SCCs ([CSES](https://cses.fi/problemset/))
4. 2-SAT (uses SCC)
5. Redundant Connection (LC 684) — DSU
6. Count strongly connected components
7. CSES "Flight Routes Check"
8. CSES "Planets and Kingdoms" (SCC)

---

## XI. FURTHER READING

- **Tarjan (1972)**, "Depth-First Search and Linear Graph Algorithms"
- **Tarjan**, *Data Structures and Network Algorithms* ⭐
- **[CP-Algorithms](https://cp-algorithms.com)** bridges/articulation/SCC pages

---

**→ Next case study:** [`10-Recent-Breakthroughs.md`](./10-Recent-Breakthroughs.md)
