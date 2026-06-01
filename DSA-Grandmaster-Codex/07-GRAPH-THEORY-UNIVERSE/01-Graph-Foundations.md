# 🌐 Graph Foundations

> *"A graph is the most universal data structure. Everything is a graph if you squint."*

---

## I. DEFINITIONS

A **graph** G = (V, E):
- V = set of vertices (nodes)
- E = set of edges (connections between vertices)

### Types
- **Undirected**: edges have no direction. (u,v) = (v,u).
- **Directed (digraph)**: edges have direction. (u→v) ≠ (v→u).
- **Weighted**: edges carry weights/costs.
- **Unweighted**: all edges equal.
- **Simple**: no self-loops, no multi-edges.
- **Multigraph**: multiple edges between same pair allowed.
- **DAG**: directed acyclic graph (no cycles).
- **Tree**: connected, acyclic, undirected; n nodes, n-1 edges.
- **Forest**: disjoint union of trees.
- **Bipartite**: vertices split into two sets, edges only between sets.

---

## II. REPRESENTATIONS

### Adjacency List (most common)
```cpp
vector<vector<int>> adj(n);          // unweighted
adj[u].push_back(v);
adj[v].push_back(u);                 // if undirected

vector<vector<pair<int,int>>> adj(n); // weighted: {neighbor, weight}
adj[u].push_back({v, w});
```
- Space: O(V + E)
- Iterate neighbors of u: O(degree(u))
- Best for sparse graphs (most real graphs)

### Adjacency Matrix
```cpp
vector<vector<int>> mat(n, vector<int>(n, 0));
mat[u][v] = 1;  // or weight
```
- Space: O(V²)
- Edge query (u, v): O(1)
- Best for dense graphs, Floyd-Warshall

### Edge List
```cpp
vector<tuple<int,int,int>> edges;  // {weight, u, v}
```
- Space: O(E)
- Best for Kruskal's (sort by weight)

---

## III. KEY PROPERTIES

### Degree
- Undirected: degree(v) = number of incident edges.
- Sum of degrees = 2|E| (handshake lemma).
- Directed: in-degree + out-degree.

### Connectivity
- **Connected** (undirected): path between every pair.
- **Strongly connected** (directed): directed path between every pair.
- **Weakly connected** (directed): connected if directions ignored.

### Paths and cycles
- **Path**: sequence of distinct vertices, consecutive ones adjacent.
- **Cycle**: path that returns to start.
- **Simple cycle**: no repeated vertices (except start=end).

---

## IV. THE TWO UNIVERSAL TRAVERSALS

### BFS (Breadth-First Search)
Explores level by level. Queue-based. Finds shortest paths in unweighted graphs.

### DFS (Depth-First Search)
Explores as deep as possible before backtracking. Stack/recursion-based. Used for components, cycles, topological sort, bridges, SCCs.

See the BFS, DFS, and every graph algorithm (with code) in [`COMPENDIUM-All-Graph-Algorithms.md`](./COMPENDIUM-All-Graph-Algorithms.md) (§02-03).

---

## V. GRAPH MODELING — THE REAL SKILL

The hard part of graph problems is **recognizing the graph**.

### Examples of hidden graphs
| Problem                                   | Vertices            | Edges                          |
|-------------------------------------------|---------------------|--------------------------------|
| Word Ladder                               | words               | 1-letter differences           |
| Course Schedule                           | courses             | prerequisites                  |
| Number of Islands                         | grid cells          | adjacent land cells            |
| Sliding Puzzle                            | board states        | single moves                   |
| Network of computers                      | computers           | cables                         |
| Currency exchange                         | currencies          | exchange rates (log for arbitrage) |
| Job dependencies                          | jobs                | "must finish before"           |
| Friend recommendations                    | people              | friendships                    |

**The skill**: ask "what are the objects (vertices)? what are the relationships (edges)?"

---

## VI. CHOOSING THE RIGHT ALGORITHM

| Need                              | Algorithm                          |
|-----------------------------------|------------------------------------|
| Shortest path, unweighted         | BFS                                |
| Shortest path, weights 0/1        | 0-1 BFS                            |
| Shortest path, non-negative       | Dijkstra                          |
| Shortest path, negative weights   | Bellman-Ford                      |
| All-pairs shortest paths          | Floyd-Warshall (V≤500)            |
| Connected components              | DFS/BFS/Union-Find                |
| Topological order                 | Kahn's / DFS                      |
| Cycle detection                   | DFS (color)                       |
| Minimum spanning tree             | Kruskal / Prim                    |
| Bridges / articulation points     | Tarjan's DFS                      |
| Strongly connected components     | Tarjan / Kosaraju                 |
| Bipartite matching                | Kuhn / Hopcroft-Karp / flow       |
| Maximum flow                      | Dinic / Edmonds-Karp              |
| LCA                               | Binary lifting / Euler+RMQ        |

---

## VII. COMPLEXITY REFERENCE

| Algorithm        | Time                  |
|------------------|-----------------------|
| BFS / DFS        | O(V + E)              |
| Dijkstra (heap)  | O((V+E) log V)        |
| Bellman-Ford     | O(V·E)                |
| Floyd-Warshall   | O(V³)                 |
| Kruskal          | O(E log E)            |
| Prim (heap)      | O((V+E) log V)        |
| Tarjan SCC       | O(V + E)              |
| Dinic max flow   | O(V²·E)               |
| Kuhn's matching  | O(V·E)                |
| Hopcroft-Karp    | O(E·√V)               |

---

## VIII. PROBLEMS TO START WITH

1. Number of Islands (LC 200)
2. Clone Graph (LC 133)
3. Course Schedule (LC 207)
4. Pacific Atlantic Water Flow (LC 417)
5. Rotting Oranges (LC 994)
6. Word Ladder (LC 127)
7. Number of Connected Components (LC 323)
8. Is Graph Bipartite (LC 785)

---

**→ Next:** BFS, DFS & all graph algorithms with code → [`COMPENDIUM-All-Graph-Algorithms.md`](./COMPENDIUM-All-Graph-Algorithms.md)
