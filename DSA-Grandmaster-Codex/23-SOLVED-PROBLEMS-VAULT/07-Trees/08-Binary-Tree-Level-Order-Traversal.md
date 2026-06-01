# Binary Tree Level Order Traversal

**Platform**: LeetCode 102 · **Difficulty**: Medium · **Topics**: Tree, BFS, DFS, Binary Tree · **Pattern**: BFS by level (size snapshot)

---

## 📜 Problem Statement

Given the `root` of a binary tree, return the **level order traversal** of its nodes' values. (i.e., from left to right, level by level).

### Examples

**Example 1:**
```
Input:  root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

        3            level 0 → [3]
       / \
      9  20          level 1 → [9, 20]
        /  \
       15   7        level 2 → [15, 7]
```

**Example 2:**
```
Input:  root = [1]
Output: [[1]]
```

**Example 3:**
```
Input:  root = []
Output: []
```

### Constraints
```
The number of nodes in the tree is in the range [0, 2000].
-1000 <= Node.val <= 1000
```

---

## 🧠 Understanding the problem

We must output values **grouped by depth**: one inner list per level, left to right. The natural tool is **breadth-first search** with a queue, which visits nodes in exactly that order.

The one technique that makes per-level grouping clean: at the start of each outer iteration, **snapshot the current queue size**. That count is precisely the number of nodes on the current level. Process exactly that many nodes, collecting their values into one list, while enqueueing their children for the next level. Capturing the size *before* the inner loop is essential, because the queue grows as you enqueue children.

A DFS variant also works by passing the current depth and appending into `res[depth]`.

---

## Approach 1 — BFS with level-size snapshot (optimal) ⭐

### Intuition
A queue naturally yields nodes in breadth-first order. To know where one level ends and the next begins, record how many nodes are currently queued — that is one full level — and drain exactly that many before starting the next.

### Algorithm
1. If `root` is null, return `[]`.
2. Push `root` into a queue.
3. While the queue is non-empty:
   - `sz = queue.size()` (snapshot).
   - Repeat `sz` times: pop a node, append its value to the current `level`, enqueue its non-null children.
   - Append `level` to the result.
4. Return the result.

### Dry run on `[3,9,20,null,null,15,7]`
```
queue=[3]
sz=1 → pop 3, level=[3], enqueue 9,20 → res=[[3]], queue=[9,20]
sz=2 → pop 9 (no kids), pop 20 (enqueue 15,7), level=[9,20] → res=[[3],[9,20]], queue=[15,7]
sz=2 → pop 15, pop 7, level=[15,7] → res=[[3],[9,20],[15,7]], queue=[]
done → [[3],[9,20],[15,7]]   ✓
```

### Code
```cpp
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> res;
    if (!root) return res;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int sz = q.size();
        vector<int> level;
        for (int i = 0; i < sz; i++) {
            TreeNode* node = q.front(); q.pop();
            level.push_back(node->val);
            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
        res.push_back(level);
    }
    return res;
}
```
```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int sz = q.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < sz; i++) {
            TreeNode node = q.poll();
            level.add(node.val);
            if (node.left  != null) q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
        res.add(level);
    }
    return res;
}
```
```python
from collections import deque

def levelOrder(root):
    res = []
    if not root:
        return res
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res
```

### Complexity
- **Time**: O(n) — each node enqueued and dequeued exactly once.
- **Space**: O(n) — the queue holds up to one full level (up to ~n/2 leaves) and the output stores all values.

### Verdict
The canonical answer. The size-snapshot idiom is the single most reused trick across level-based tree problems (Right Side View, Zigzag, Average of Levels). This is what you write.

---

## Approach 2 — DFS with explicit level index

### Intuition
DFS can produce level groups too: carry the current `depth`. The first time you reach a given depth, create a new inner list; otherwise append to the existing one. Pre-order DFS (node before children, left before right) preserves left-to-right order within each level.

### Algorithm
1. `dfs(node, depth)`:
   - If `node` is null, return.
   - If `depth == res.size()`, append a new empty list.
   - Append `node->val` to `res[depth]`.
   - Recurse `dfs(left, depth+1)` then `dfs(right, depth+1)`.
2. Call `dfs(root, 0)`; return `res`.

### Code
```cpp
class Solution {
    void dfs(TreeNode* node, int depth, vector<vector<int>>& res) {
        if (!node) return;
        if (depth == (int)res.size()) res.push_back({});
        res[depth].push_back(node->val);
        dfs(node->left,  depth + 1, res);
        dfs(node->right, depth + 1, res);
    }
public:
    vector<vector<int>> levelOrder(TreeNode* root) {
        vector<vector<int>> res;
        dfs(root, 0, res);
        return res;
    }
};
```
```java
class Solution {
    private void dfs(TreeNode node, int depth, List<List<Integer>> res) {
        if (node == null) return;
        if (depth == res.size()) res.add(new ArrayList<>());
        res.get(depth).add(node.val);
        dfs(node.left,  depth + 1, res);
        dfs(node.right, depth + 1, res);
    }
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(root, 0, res);
        return res;
    }
}
```
```python
def levelOrder(root):
    res = []
    def dfs(node, depth):
        if not node:
            return
        if depth == len(res):
            res.append([])
        res[depth].append(node.val)
        dfs(node.left,  depth + 1)
        dfs(node.right, depth + 1)
    dfs(root, 0)
    return res
```

### Complexity
- **Time**: O(n).
- **Space**: O(h) recursion stack + O(n) output.

### Verdict
A neat demonstration that level grouping isn't exclusively a BFS task. BFS is more idiomatic for "level order," but this DFS is worth knowing and is sometimes cleaner to extend.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| BFS size-snapshot | O(n) | O(n) | idiomatic for level order; the default ⭐ |
| DFS with depth index | O(n) | O(h)+O(n) | recursion; groups by `res[depth]` |

Both produce identical output. BFS matches the problem's "level by level" phrasing most directly; DFS is the elegant alternative.

---

## 🧪 Edge cases & pitfalls
- **Empty tree** → return `[]`.
- **Single node** → `[[val]]`.
- **Skewed tree** → one node per level; output has `h` singleton lists.
- **Pitfall — reading `queue.size()` inside the loop**: the size changes as children are enqueued. Snapshot it into `sz` before the inner loop, or you will merge levels.
- **Pitfall (DFS) — wrong recursion order**: recurse left before right so each level fills left-to-right; swapping them reverses each row.
- **Pitfall — forgetting the null-root guard**: pushing a null root, or not returning early, yields a stray empty level.

---

## 🔗 Related problems
- **Binary Tree Right Side View** (LC 199) — keep only the last node of each level. See [`09-Binary-Tree-Right-Side-View.md`](./09-Binary-Tree-Right-Side-View.md).
- **Binary Tree Zigzag Level Order Traversal** (LC 103) — alternate row direction.
- **Average of Levels in Binary Tree** (LC 637) — same scaffold, aggregate per level.
- **Binary Tree Level Order Traversal II** (LC 107) — same BFS, reverse the result.

---

**→ Next:** [`09-Binary-Tree-Right-Side-View.md`](./09-Binary-Tree-Right-Side-View.md) | **← Prev:** [`07-Lowest-Common-Ancestor-BST.md`](./07-Lowest-Common-Ancestor-BST.md) | Back to [`00-Index.md`](./00-Index.md)
