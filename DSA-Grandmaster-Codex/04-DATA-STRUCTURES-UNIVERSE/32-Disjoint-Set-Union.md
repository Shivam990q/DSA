# 🔗 Disjoint Set Union (Union-Find)

> *"DSU is the simplest non-trivial data structure with non-trivial complexity."*

---

## I. THE PROBLEM

Maintain a partition of {0, 1, ..., n-1} supporting:
- `find(x)`: which set is x in?
- `union(x, y)`: merge x's set with y's set

**Applications**:
- Connected components in dynamic graph
- Kruskal's MST
- Cycle detection in undirected graph
- Image segmentation (connected pixels)
- Network connectivity

---

## II. NAIVE IMPLEMENTATIONS

### Naive 1: Array of labels
- `label[x]` = set ID of x
- `find(x)`: O(1)
- `union(x, y)`: scan all labels, change x's label to y's: O(n)

### Naive 2: Forest (just parent pointers)
- `parent[x]` = parent in tree; root has parent[x] = x
- `find(x)`: walk parents to root: O(h)
- `union(x, y)`: parent[find(x)] = find(y): O(h)

Without optimizations, h can be O(n) (a degenerate chain).

---

## III. THE OPTIMIZATIONS

### Optimization 1: **Union by rank** (or size)
When unioning two trees, attach the *smaller* tree under the *larger*. Keeps tree shallow.

### Optimization 2: **Path compression**
During `find(x)`, after walking to root, **point every node on the path directly to root**.

### Both together: **α(n) amortized per operation**, where α is the inverse Ackermann function (≤ 4 for any conceivable n). Effectively O(1).

---

## IV. CANONICAL IMPLEMENTATION

```cpp
struct DSU {
    vector<int> parent, rank_;
    int components;
    
    DSU(int n) : parent(n), rank_(n, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);  // parent[i] = i
    }
    
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);  // path compression
        return parent[x];
    }
    
    bool unite(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;  // already in same set
        if (rank_[x] < rank_[y]) swap(x, y);
        parent[y] = x;
        if (rank_[x] == rank_[y]) rank_[x]++;
        --components;
        return true;
    }
    
    bool connected(int x, int y) { return find(x) == find(y); }
};
```

### Iterative path compression (no recursion stack):
```cpp
int find(int x) {
    int root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {
        int next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}
```

---

## V. PROBLEMS USING DSU (TOP 30)

1. **Number of Connected Components in an Undirected Graph** (LC 323)
2. **Number of Provinces** (LC 547)
3. **Redundant Connection** (LC 684)
4. **Redundant Connection II** (LC 685)
5. **Accounts Merge** (LC 721)
6. **Most Stones Removed with Same Row or Column** (LC 947)
7. **Number of Operations to Make Network Connected** (LC 1319)
8. **Smallest String With Swaps** (LC 1202)
9. **Satisfiability of Equality Equations** (LC 990)
10. **Earliest Moment When Everyone Become Friends** (LC 1101)
11. **Connecting Cities With Minimum Cost** (LC 1135)
12. **Min Cost to Connect All Points** (LC 1584) — with Kruskal's
13. **Critical and Pseudo-Critical Edges** (LC 1489)
14. **Number of Good Paths** (LC 2421)
15. **Find Latest Group of Size M** (LC 1562)
16. **Couples Holding Hands** (LC 765)
17. **Sentence Similarity II** (LC 737)
18. **Friend Circles** ([LeetCode](https://leetcode.com) 547 — same as Provinces)
19. **Graph Valid Tree** (LC 261)
20. **Min Number of Days to Disconnect Island** (LC 1568) — partial

[CSES](https://cses.fi/problemset/):
21. Road Construction
22. Road Reparation

CF problems by tag `dsu`:
23-30. Various 1500-2200 rated problems

---

## VI. EXTENSIONS

### DSU with rollback
Don't do path compression; only union by rank. Each union pushes (parent change, rank change) to a stack. To rollback, pop and undo.

Used for: offline dynamic connectivity, link-cut alternative.

### Weighted DSU
Each edge has a weight; track `weight[x]` = total weight from x to root. Useful for:
- Tracking relative offsets between elements
- "a and b differ by w" type problems

```cpp
struct WeightedDSU {
    vector<int> parent, weight;
    
    int find(int x) {
        if (parent[x] == x) return x;
        int root = find(parent[x]);
        weight[x] += weight[parent[x]];  // accumulate
        parent[x] = root;
        return root;
    }
    
    bool unite(int x, int y, int w) {
        // a's root - b's root = w in the relation
        int rx = find(x), ry = find(y);
        if (rx == ry) return weight[x] - weight[y] == w;
        parent[rx] = ry;
        weight[rx] = weight[y] - weight[x] + w;
        return true;
    }
};
```

### Persistent DSU
Versioned: can query historical states. Used in offline problems with rollback queries.

### Small-to-large DSU
When unioning, copy data from smaller to larger set; O(n log n) total. Used for tree problems with auxiliary information per component.

---

## VII. COMMON PITFALLS

1. **Forgetting path compression** → O(log² n) per op (still fast, but not optimal)
2. **Using recursion for find with deep trees** → stack overflow on n=10⁶
3. **Path compression breaks rollback** — choose one or the other
4. **Off-by-one in 1-indexed vs 0-indexed**

---

## VIII. WHEN TO USE DSU

- "Are these connected?" / "Connect these"
- "Number of connected components?"
- Kruskal's MST
- Offline queries about connectivity over a sequence of additions
- 2-SAT (with implication graph + SCC, but DSU is simpler for some cases)

---

## IX. WHEN NOT TO USE DSU

- Need to **disconnect** edges → DSU doesn't support deletion (use Link-Cut tree or offline trick)
- Need pathfinding, not just connectivity → use BFS/DFS

---

## X. RECOMMENDED READING

- **CLRS Chapter 21** — Disjoint Sets
- **Tarjan, Van Leeuwen 1984** — original analysis with α(n)
- **[CP-Algorithms](https://cp-algorithms.com): DSU**

---

**→ Next:** KD-Tree, Skip List, Link-Cut Tree & all advanced structures → [`COMPENDIUM-Advanced-DS.md`](./COMPENDIUM-Advanced-DS.md)
