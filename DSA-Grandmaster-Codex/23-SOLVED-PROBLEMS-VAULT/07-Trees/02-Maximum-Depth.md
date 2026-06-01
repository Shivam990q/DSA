# Maximum Depth of Binary Tree

**Platform**: LeetCode 104 · **Difficulty**: Easy · **Topics**: Tree, DFS, BFS, Binary Tree · **Pattern**: Structural recursion (bubble value up)

---

## 📜 Problem Statement

Given the `root` of a binary tree, return its **maximum depth**.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### Examples

**Example 1:**
```
Input:  root = [3,9,20,null,null,15,7]
Output: 3

        3            depth 1
       / \
      9  20          depth 2
        /  \
       15   7        depth 3   ← longest root-to-leaf path = 3 nodes
```

**Example 2:**
```
Input:  root = [1,null,2]
Output: 2

      1
       \
        2
```

**Example 3:**
```
Input:  root = []
Output: 0
Explanation: An empty tree has depth 0.
```

### Constraints
```
The number of nodes in the tree is in the range [0, 10^4].
-100 <= Node.val <= 100
```

---

## 🧠 Understanding the problem

"Maximum depth" is the length (in nodes) of the longest chain from the root straight down to a leaf. The crucial observation is the **self-similar recurrence**: the depth of a tree rooted at some node is `1` (for the node itself) plus the depth of whichever subtree is deeper.

That single sentence — *depth(node) = 1 + max(depth(left), depth(right))* — is the entire problem. The base case is an empty subtree, whose depth is `0`. From there the recursion writes itself, and the only real decision is whether to express it via recursion (DFS) or an explicit queue (BFS).

---

## Approach 1 — Recursive DFS (optimal) ⭐

### Intuition
Ask each node a single question: *"How deep is the subtree below me?"* A node cannot answer without knowing how deep its left and right subtrees go, so it delegates downward, takes the larger of the two answers, and adds `1` for itself.

### Algorithm
1. If `root` is null, return `0` (empty subtree contributes no depth).
2. Recursively compute `left = maxDepth(root->left)`.
3. Recursively compute `right = maxDepth(root->right)`.
4. Return `1 + max(left, right)`.

### Dry run on `[3,9,20,null,null,15,7]`
```
maxDepth(3)
  maxDepth(9)
    maxDepth(null) = 0
    maxDepth(null) = 0
    → 1 + max(0,0) = 1
  maxDepth(20)
    maxDepth(15) → 1 + max(0,0) = 1
    maxDepth(7)  → 1 + max(0,0) = 1
    → 1 + max(1,1) = 2
  → 1 + max(1, 2) = 3        ✓
```

### Code
```cpp
int maxDepth(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(maxDepth(root->left), maxDepth(root->right));
}
```
```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}
```
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### Complexity
- **Time**: O(n) — every node is visited exactly once.
- **Space**: O(h) — recursion stack, where `h` is the tree height. O(log n) for a balanced tree, O(n) for a degenerate (skewed) tree.

### Verdict
The canonical answer: three lines, the code mirrors the data, and it is optimal in time. This is what you write first.

---

## Approach 2 — Iterative BFS (level counting)

### Intuition
The maximum depth equals the **number of levels** in the tree. BFS processes the tree level by level, so if we count how many levels we peel off, we get the depth directly. This also sidesteps any deep-recursion stack concern.

### Algorithm
1. If `root` is null, return `0`.
2. Push `root` into a queue and set `depth = 0`.
3. While the queue is non-empty:
   - Increment `depth`.
   - Pop exactly `size` nodes (one full level), enqueueing each one's non-null children.
4. Return `depth`.

### Code
```cpp
int maxDepth(TreeNode* root) {
    if (!root) return 0;
    queue<TreeNode*> q;
    q.push(root);
    int depth = 0;
    while (!q.empty()) {
        int sz = q.size();
        depth++;
        for (int i = 0; i < sz; i++) {
            TreeNode* node = q.front(); q.pop();
            if (node->left)  q.push(node->left);
            if (node->right) q.push(node->right);
        }
    }
    return depth;
}
```
```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    int depth = 0;
    while (!q.isEmpty()) {
        int sz = q.size();
        depth++;
        for (int i = 0; i < sz; i++) {
            TreeNode node = q.poll();
            if (node.left != null)  q.offer(node.left);
            if (node.right != null) q.offer(node.right);
        }
    }
    return depth;
}
```
```python
from collections import deque

def maxDepth(root):
    if not root:
        return 0
    q = deque([root])
    depth = 0
    while q:
        depth += 1
        for _ in range(len(q)):
            node = q.popleft()
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
    return depth
```

### Complexity
- **Time**: O(n) — each node enqueued and dequeued once.
- **Space**: O(w) — the queue holds at most one level, up to O(n) at the widest level.

### Verdict
Same time complexity, no recursion-depth risk. Reach for it when the interviewer says "the tree could be 10⁶ deep — won't recursion overflow?"

---

## Approach 3 — Iterative DFS (explicit stack)

### Intuition
If you want DFS without recursion, carry each node together with its depth on a stack. Track the largest depth you ever see when you reach a node.

### Algorithm
1. If `root` is null, return `0`.
2. Push `(root, 1)` onto a stack; set `best = 0`.
3. While the stack is non-empty, pop `(node, d)`, update `best = max(best, d)`, and push each non-null child with depth `d + 1`.
4. Return `best`.

### Code
```cpp
int maxDepth(TreeNode* root) {
    if (!root) return 0;
    stack<pair<TreeNode*,int>> st;
    st.push({root, 1});
    int best = 0;
    while (!st.empty()) {
        auto [node, d] = st.top(); st.pop();
        best = max(best, d);
        if (node->left)  st.push({node->left,  d + 1});
        if (node->right) st.push({node->right, d + 1});
    }
    return best;
}
```
```java
public int maxDepth(TreeNode root) {
    if (root == null) return 0;
    Deque<Object[]> st = new ArrayDeque<>();
    st.push(new Object[]{root, 1});
    int best = 0;
    while (!st.isEmpty()) {
        Object[] top = st.pop();
        TreeNode node = (TreeNode) top[0];
        int d = (int) top[1];
        best = Math.max(best, d);
        if (node.left  != null) st.push(new Object[]{node.left,  d + 1});
        if (node.right != null) st.push(new Object[]{node.right, d + 1});
    }
    return best;
}
```
```python
def maxDepth(root):
    if not root:
        return 0
    st = [(root, 1)]
    best = 0
    while st:
        node, d = st.pop()
        best = max(best, d)
        if node.left:  st.append((node.left,  d + 1))
        if node.right: st.append((node.right, d + 1))
    return best
```

### Complexity
- **Time**: O(n).
- **Space**: O(h) — the stack mirrors a root-to-node path plus pending siblings.

### Verdict
A solid middle ground: DFS traversal without the call stack. Slightly noisier than recursion; use it only when explicitly asked for an iterative DFS.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive DFS | O(n) | O(h) | cleanest; the default answer ⭐ |
| Iterative BFS | O(n) | O(w) | counts levels; no recursion risk |
| Iterative DFS | O(n) | O(h) | DFS without the call stack |

All three are O(n) time. The differences are only in *space shape* and whether the call stack is used. For the given constraints (≤ 10⁴ nodes) recursion is perfectly safe.

---

## 🧪 Edge cases & pitfalls
- **Empty tree** (`root == null`) → return `0`. The base case (and the BFS/DFS guards) handle it.
- **Single node** → depth `1`.
- **Skewed tree** (a "linked list" of nodes) → depth equals the node count `n`; recursion uses O(n) stack here, the only realistic overflow scenario.
- **Pitfall — off-by-one**: depth counts **nodes**, not edges. A single node has depth `1`, not `0`. (Contrast with Diameter, which counts edges.)
- **Pitfall (BFS)**: capture `q.size()` into a local *before* the inner loop; the queue grows as you enqueue children, so reading `size()` inside the loop condition would process more than one level.

---

## 🔗 Related problems
- **Minimum Depth of Binary Tree** (LC 111) — shortest root-to-leaf path; beware the one-child case.
- **Diameter of Binary Tree** (LC 543) — builds directly on height. See [`03-Diameter-of-Binary-Tree.md`](./03-Diameter-of-Binary-Tree.md).
- **Balanced Binary Tree** (LC 110) — compares left/right heights. See [`04-Balanced-Binary-Tree.md`](./04-Balanced-Binary-Tree.md).
- **Maximum Depth of N-ary Tree** (LC 559) — same recurrence over a list of children.

---

**→ Next:** [`03-Diameter-of-Binary-Tree.md`](./03-Diameter-of-Binary-Tree.md) | **← Prev:** [`01-Invert-Binary-Tree.md`](./01-Invert-Binary-Tree.md) | Back to [`00-Index.md`](./00-Index.md)
