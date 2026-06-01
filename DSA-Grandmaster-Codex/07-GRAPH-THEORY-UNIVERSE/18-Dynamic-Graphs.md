# 🌐 Dynamic Graphs

> *"Edges appear and vanish. Can you keep answering connectivity/queries efficiently?"*

---

## I. THE PROBLEM
Maintain a graph under **updates** (add/remove edges) while answering queries (connectivity, component size, MST weight, etc.). The difficulty depends on which updates are allowed.

---

## II. INCREMENTAL (only ADD edges) — easy ⭐
**Union-Find (DSU)** handles edge additions + connectivity in O(α) amortized. Can't delete. Track component count/size easily.
- Use for: "process edges in order, answer connectivity," offline problems where you sort and add.

---

## III. DECREMENTAL (only REMOVE edges)
Trickier. Common trick: **process in reverse** — if all deletions are known offline, reverse time so deletions become additions, then use DSU.

---

## IV. FULLY DYNAMIC (add AND remove, online)
Hard. Options:
- **Link-Cut Trees** (Sleator-Tarjan): dynamic FOREST connectivity, path aggregates, in O(log n) amortized. For trees/forests. (See [`../04-DATA-STRUCTURES-UNIVERSE/COMPENDIUM-Advanced-DS.md`](../04-DATA-STRUCTURES-UNIVERSE/COMPENDIUM-Advanced-DS.md).)
- **Euler Tour Trees**: dynamic forest connectivity.
- **Holm-de Lichtenberg-Thorup (HDT)**: fully dynamic connectivity in general graphs, O(log² n) amortized.

---

## V. OFFLINE DYNAMIC CONNECTIVITY ⭐ (the CP workhorse)
When all updates/queries are known in advance:
- Build a **segment tree over TIME**. Each edge "exists" during an interval of time → add it to the O(log Q) segment-tree nodes covering that interval.
- DFS the time-segment-tree; use **DSU with rollback** (union by rank, NO path compression) to add edges entering a node and undo them when leaving.
- Answer queries at the leaves.

Complexity: O((Q + E) log Q · α). This elegantly handles "edges that exist during time intervals."

---

## VI. DYNAMIC MST
Maintaining the MST under edge weight changes / additions: link-cut trees support "find max edge on path" → decide whether a new edge improves the MST. O(log n) per update.

---

## VII. APPLICATIONS
- Connectivity under a stream of add/remove operations
- "Was there a path between u and v at time t?"
- Dynamic MST / network reliability over time
- Offline queries with time intervals

---

## VIII. COMPLEXITY SUMMARY
| Setting | Tool | Per-op |
|---------|------|--------|
| Incremental | DSU | O(α) |
| Decremental (offline) | reverse + DSU | O(α) |
| Fully dynamic forest | Link-Cut / Euler Tour Tree | O(log n) |
| Fully dynamic general | HDT | O(log² n) |
| Offline interval | segtree-on-time + DSU rollback | O(log Q · α) |

---

## IX. PROBLEMS
- Offline dynamic connectivity (CF "dsu" + "divide and conquer")
- "Add/remove edges, query connectivity at times"
- Dynamic MST problems
- CF Div 1 data-structure problems

---

## X. NOTE
Dynamic graphs are Level 7-8 (elite CP / advanced). The **offline segtree-on-time + DSU-with-rollback** technique is the most practical and widely used in contests. Fully-online general dynamic connectivity (HDT) is rare and heavy.

---

**→ Next:** [`19-Planar-Graphs.md`](./19-Planar-Graphs.md)
