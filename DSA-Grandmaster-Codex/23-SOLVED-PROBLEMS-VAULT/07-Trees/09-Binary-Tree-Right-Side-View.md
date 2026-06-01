# Binary Tree Right Side View

**Platform**: LeetCode 199 · **Difficulty**: Medium · **Topics**: Tree, BFS, DFS, Binary Tree · **Pattern**: One representative per level

---

## 📜 Problem Statement

Given the `root` of a binary tree, imagine yourself standing on the **right side** of it, return the values of the nodes you can see ordered from top to bottom.

### Examples

**Example 1:**
```
Input:  root = [1,2,3,null,5,null,4]
Output: [1,3,4]

        1            ← see 1
       / \
      2   3          ← see 3 (rightmost on this level)
       \   \
        5   4        ← see 4
```

**Example 2:**
```
Input:  root = [1,null,3]
Output: [1,3]
```

**Example 3:**
```
Input:  root = []
Output: []
```

### Constraints
```
The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100
```

---

## 🧠 Understanding the problem

Standing on the right, at each depth you see exactly **one** node: the **rightmost** node of that level. Everything to its left is hidden behind it. So the answer is "the last node of each level, top to bottom."

A subtle point: the rightmost *visible* node on a level is not always a right child. In Example 1, level 2's visible node `4` is a right child, but if the tree were `[1,2,3,4]` (only `2` has a left child `4`), level 2's only — and therefore rightmost — node is the left child `4`. So "rightmost on the level," not "follow right pointers," is the correct rule.

Two clean implementations: BFS taking the last node of each level, or DFS visiting **right before left** and recording the first node seen at each new depth.

---

## Approach 1 — BFS, last node of each level (optimal) ⭐

### Intuition
Do a standard level-order BFS. Within each level, the **last** node popped is the rightmost — record it.

### Algorithm
1. If `root` is null, return `[]`.
2. Push `root` into a queue.
3. While non-empty:
   - `sz = queue.size()`.
   - Loop `i` from `0` to `sz-1`: pop a node; if `i == sz-1` it is the rightmost → append its value; enqueue non-null children.
4. Return the result.

### Dry run on `[1,2,3,null,5,null,4]`
```
queue=[1]; sz=1 → i=0 is last → push 1; enqueue 2,3
queue=[2,3]; sz=2 → i=1 (node 3) is last → push 3; enqueue 5,4
queue=[5,4]; sz=2 → i=1 (node 4) is last → push 4
result = [1,3,4]   ✓
```

### Code
```cpp
vector<int> rightSideView(TreeNode* root) {
    vector<int> res;
    if (!root) return res;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int sz = q.size();
        for (int i = 0; i < sz; i++) {
            TreeNode* node = q.front(); q.pop();
            if (i == sz - 1) res.push_back(node->val);
            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }
    return res;
}
```
```java
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> res = new ArrayList<>();
    if (root == null) return res;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        int sz = q.size();
        for (int i = 0; i < sz; i++) {
            TreeNode node = q.poll();
            if (i == sz - 1) res.add(node.val);
            if (node.left  != null) q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
    }
    return res;
}
```
```python
from collections import deque

def rightSideView(root):
    res = []
    if not root:
        return res
    q = deque([root])
    while q:
        sz = len(q)
        for i in range(sz):
            node = q.popleft()
            if i == sz - 1:
                res.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
    return res
```

### Complexity
- **Time**: O(n) — each node processed once.
- **Space**: O(w) — queue holds at most one level, up to O(n).

### Verdict
The canonical answer. It reuses the level-order scaffold and simply keeps the last node per level. This is what you present.

---

## Approach 2 — DFS, right child first

### Intuition
If we visit **right before left** and recurse with the depth, then the *first* node we ever reach at a new depth is the rightmost one (because the right side is explored first). Record a node's value only when its depth equals the current result length.

### Algorithm
1. `dfs(node, depth)`:
   - If null, return.
   - If `depth == res.size()`, this is the first (rightmost) node at this depth → append its value.
   - Recurse right with `depth+1`, then left with `depth+1`.
2. Call `dfs(root, 0)`; return `res`.

### Dry run on `[1,2,3,null,5,null,4]`
```
dfs(1,0): depth0==len0 → push 1
  dfs(3,1): depth1==len1 → push 3
     dfs(4,2): depth2==len2 → push 4
     dfs(null,2)
  dfs(2,1): depth1==len3? no (already have level1) → skip
     dfs(5,2): depth2==len3? no → skip
result = [1,3,4]   ✓
```

### Code
```cpp
class Solution {
    void dfs(TreeNode* node, int depth, vector<int>& res) {
        if (!node) return;
        if (depth == (int)res.size()) res.push_back(node->val);
        dfs(node->right, depth + 1, res);
        dfs(node->left,  depth + 1, res);
    }
public:
    vector<int> rightSideView(TreeNode* root) {
        vector<int> res;
        dfs(root, 0, res);
        return res;
    }
};
```
```java
class Solution {
    private void dfs(TreeNode node, int depth, List<Integer> res) {
        if (node == null) return;
        if (depth == res.size()) res.add(node.val);
        dfs(node.right, depth + 1, res);
        dfs(node.left,  depth + 1, res);
    }
    public List<Integer> rightSideView(TreeNode root) {
        List<Integer> res = new ArrayList<>();
        dfs(root, 0, res);
        return res;
    }
}
```
```python
def rightSideView(root):
    res = []
    def dfs(node, depth):
        if not node:
            return
        if depth == len(res):
            res.append(node.val)
        dfs(node.right, depth + 1)
        dfs(node.left,  depth + 1)
    dfs(root, 0)
    return res
```

### Complexity
- **Time**: O(n).
- **Space**: O(h) recursion stack.

### Verdict
Elegant and slightly less memory than BFS for tall, narrow trees (O(h) vs O(w)). The "right-first, record on first visit per depth" trick is worth internalizing.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| BFS last-of-level | O(n) | O(w) | reuses level-order; the default ⭐ |
| DFS right-first | O(n) | O(h) | first node per depth is rightmost |

Both are O(n). Choose BFS when you already think in levels; choose DFS right-first for O(h) space or when recursion reads cleaner.

---

## 🧪 Edge cases & pitfalls
- **Empty tree** → `[]`.
- **Left-only tree** (`[1,2,null,3]`) → the visible node on each level is the lone left node: `[1,2,3]`. This is the case that breaks "just follow right pointers."
- **Single node** → `[val]`.
- **Pitfall — following right children only**: a right child may be missing while a left child exists; the rightmost *visible* node can be a left child. Use "last node of the level" (BFS) or "first at new depth, right-first" (DFS).
- **Pitfall (DFS) — recursing left before right**: that records the leftmost node per level (a left-side view). Right must come first.

---

## 🔗 Related problems
- **Binary Tree Level Order Traversal** (LC 102) — the BFS scaffold reused here. See [`08-Binary-Tree-Level-Order-Traversal.md`](./08-Binary-Tree-Level-Order-Traversal.md).
- **Binary Tree Left Side View** — mirror (recurse left first / first node per level).
- **Find Largest Value in Each Tree Row** (LC 515) — per-level aggregation instead of the last node.
- **Populating Next Right Pointers** (LC 116/117) — also reasons about rightmost-per-level.

---

**→ Next:** [`10-Count-Good-Nodes.md`](./10-Count-Good-Nodes.md) | **← Prev:** [`08-Binary-Tree-Level-Order-Traversal.md`](./08-Binary-Tree-Level-Order-Traversal.md) | Back to [`00-Index.md`](./00-Index.md)
