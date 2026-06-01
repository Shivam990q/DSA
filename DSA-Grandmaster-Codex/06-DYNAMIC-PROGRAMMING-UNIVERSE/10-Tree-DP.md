# 🧬 Tree DP

> *"Compute an answer for each subtree, bubble it up. Then re-root to answer for every node."*

---

## I. THE SHAPE
`dp[v]` = answer for the subtree rooted at v, computed from children's dp values via a **post-order DFS** (children before parent).
```cpp
void dfs(int v, int parent) {
    for (int c : adj[v]) if (c != parent) {
        dfs(c, v);
        // combine dp[c] into dp[v]
    }
    // finalize dp[v]
}
```

---

## II. CLASSIC SUBTREE DPs

### Subtree size / sum
`size[v] = 1 + Σ size[c]`.

### Tree height / depth
`height[v] = 1 + max(height[c])`.

### Diameter of Tree (LC 543 for binary)
At each node, longest path through it = (top two child heights summed). Track global max.

### Maximum Path Sum (LC 124)
At each node: `gain[v] = val + max(0, max child gain)`; update answer with `val + top two child gains`.

### House Robber III (LC 337)
Each node returns a pair `(rob_v, skip_v)`:
- `rob_v = val + Σ skip_child`
- `skip_v = Σ max(rob_child, skip_child)`

### Independent set / vertex cover / dominating set on trees
2-state DP per node (in set / not in set).

### Counting / coloring on trees
DP over (node, state) where state captures the constraint with the parent.

---

## III. RE-ROOTING TECHNIQUE ⭐ (the power move)
When you need the answer "as if rooted at v" for **every** node v (not just one root):
1. **First DFS** (post-order): compute subtree dp with an arbitrary root.
2. **Second DFS** (pre-order): push information DOWN from parent to child, combining the parent's "everything except this child's subtree" with the child's subtree.

Result: every node's full-tree answer in **O(n)** total instead of O(n²).

### Example: Sum of Distances in Tree (LC 834)
- First DFS: count[v] (subtree size) and dp[root] (sum of distances from root).
- Second DFS: `dp[child] = dp[parent] − count[child] + (n − count[child])`.

---

## IV. SMALL-TO-LARGE MERGING
For "auxiliary info per subtree" (e.g., distinct colors in subtree): merge children's sets into the parent, always merging the smaller into the larger → O(n log n) total. Used for subtree query problems.

---

## V. TREE DP + BITMASK / EXTRA STATE
`dp[v][state]` where state is small (color, count mod k, in/out of set). Common in tree coloring, matching, k-domination.

---

## VI. COMPLEXITY
- Subtree DP: O(n) (one DFS).
- Re-rooting: O(n) (two DFS).
- With extra state s: O(n·s).
- Small-to-large: O(n log n).

⚠️ Use **iterative DFS** or raise the recursion limit for n up to 10⁵-10⁶ to avoid stack overflow.

---

## VII. PROBLEMS
- Diameter of Binary Tree (543), Binary Tree Max Path Sum (124)
- House Robber III (337)
- Sum of Distances in Tree (834) ⭐ (re-rooting)
- Distribute Coins in Binary Tree (979)
- Binary Tree Cameras (968) — greedy/DP on tree
- Longest Path with Different Adjacent Characters (2246)
- [CSES](https://cses.fi/problemset/) "Tree Distances I/II" (re-rooting), "Subordinates", "Tree Matching"

---

**→ Next:** [`11-Graph-DP-DAG.md`](./11-Graph-DP-DAG.md)
