# Invert Binary Tree

**Platform**: LeetCode 226 · **Difficulty**: Easy · **Topics**: Tree, DFS, BFS, Binary Tree · **Pattern**: Structural recursion (mirror)

---

## 📜 Problem Statement

Given the `root` of a binary tree, invert the tree, and return its root.

Inverting a binary tree means swapping the left and right children of **every** node, recursively. The result is the mirror image of the original tree.

### Examples

**Example 1:**
```
Input:  root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]

        4                4
       / \              / \
      2   7    ──►      7   2
     / \ / \          / \  / \
    1  3 6  9        9  6 3   1
```

**Example 2:**
```
Input:  root = [2,1,3]
Output: [2,3,1]

      2          2
     / \   ──►  / \
    1   3      3   1
```

**Example 3:**
```
Input:  root = []
Output: []
Explanation: An empty tree inverts to an empty tree.
```

### Constraints
```
The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100
```

---

## 🧠 Understanding the problem

"Invert" sounds intimidating, but the operation at a single node is trivial: **swap its two children**. The only question is *how do we apply that swap to every node?*

The key realization is that the tree is **self-similar**: a tree is a root plus a left subtree plus a right subtree, and each subtree is itself a tree. So if we can swap the two children of the root, then recursively invert each subtree, the whole tree gets mirrored. This is structural recursion — the shape of the code mirrors the shape of the data.

Crucially, it does not matter *when* you swap relative to the recursive calls (before or after), as long as every node gets its children swapped exactly once. Order independence is what makes this problem a great warm-up for tree recursion.

---

## Approach 1 — Recursive swap (optimal) ⭐

### Intuition
At every node, swap `left` and `right`, then recurse into both subtrees so they get mirrored too. The base case is an empty node, which inverts to itself (nothing to do).

### Algorithm
1. If `root` is null, return null (empty tree / past a leaf).
2. Swap `root->left` and `root->right`.
3. Recursively invert the (new) left subtree.
4. Recursively invert the (new) right subtree.
5. Return `root`.

### Dry run on `[4,2,7,1,3,6,9]`
```
invert(4): swap children → left=7, right=2
   invert(7): swap children → left=9, right=6
      invert(9): leaf, children null → returns 9
      invert(6): leaf → returns 6
   invert(2): swap children → left=3, right=1
      invert(3): leaf → returns 3
      invert(1): leaf → returns 1
final: 4 with left=7(/9,6), right=2(/3,1)  → mirrored ✓
```

### Code
```cpp
TreeNode* invertTree(TreeNode* root) {
    if (!root) return nullptr;
    swap(root->left, root->right);
    invertTree(root->left);
    invertTree(root->right);
    return root;
}
```
```java
public TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    TreeNode tmp = root.left;
    root.left = root.right;
    root.right = tmp;
    invertTree(root.left);
    invertTree(root.right);
    return root;
}
```
```python
def invertTree(root):
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

### Complexity
- **Time**: O(n) — every node is visited exactly once.
- **Space**: O(h) — recursion stack, where `h` is the tree height. O(log n) for a balanced tree, O(n) worst case for a degenerate (skewed) tree.

### Verdict
The canonical answer. Clean, minimal, and the recursion exactly mirrors the data structure. This is what you present in an interview.

---

## Approach 2 — Iterative BFS (queue)

### Intuition
If the interviewer asks "what if the tree is so deep that recursion overflows the stack?", switch to an explicit data structure. Use a queue (BFS): pop a node, swap its children, then enqueue the children to process them later.

### Algorithm
1. If `root` is null, return null.
2. Push `root` onto a queue.
3. While the queue is non-empty:
   - Pop a node, swap its `left` and `right`.
   - Enqueue any non-null children.
4. Return `root`.

### Code
```cpp
TreeNode* invertTree(TreeNode* root) {
    if (!root) return nullptr;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        TreeNode* node = q.front(); q.pop();
        swap(node->left, node->right);
        if (node->left)  q.push(node->left);
        if (node->right) q.push(node->right);
    }
    return root;
}
```
```java
public TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    while (!q.isEmpty()) {
        TreeNode node = q.poll();
        TreeNode tmp = node.left;
        node.left = node.right;
        node.right = tmp;
        if (node.left != null)  q.offer(node.left);
        if (node.right != null) q.offer(node.right);
    }
    return root;
}
```
```python
from collections import deque

def invertTree(root):
    if not root:
        return None
    q = deque([root])
    while q:
        node = q.popleft()
        node.left, node.right = node.right, node.left
        if node.left:  q.append(node.left)
        if node.right: q.append(node.right)
    return root
```

### Complexity
- **Time**: O(n) — each node processed once.
- **Space**: O(w) — the queue holds at most one level, up to O(n) at the widest level.

### Verdict
Same time complexity, no recursion stack risk. Use it when depth is a concern or the interviewer explicitly asks for an iterative solution.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive swap | O(n) | O(h) | cleanest; the default answer ⭐ |
| Iterative BFS | O(n) | O(w) | avoids deep-recursion stack overflow |

Both are O(n) time. The choice is about *space shape*: recursion uses the call stack (height-bounded), BFS uses an explicit queue (width-bounded). For this constraint range (≤ 100 nodes) either is perfectly safe.

---

## 🧪 Edge cases & pitfalls
- **Empty tree** (`root == null`) → return null. The base case handles it.
- **Single node** → no children to swap, returns itself unchanged.
- **Pitfall (recursion order)**: in C++/Java, swap first *then* recurse, OR recurse first then swap — both work, but don't recurse into `root->left` *after* swapping while still thinking it's the original left. In Python the one-liner `root.left, root.right = invertTree(root.right), invertTree(root.left)` evaluates the right-hand side fully before assigning, so it is safe.
- **Pitfall (returning nothing)**: remember to return `root`; LeetCode expects the (same) root back.

---

## 🔗 Related problems
- **Symmetric Tree** (LC 101) — check if a tree is a mirror of *itself* (compare invert-equality without modifying).
- **Same Tree** (LC 100) — the lockstep two-tree comparison this builds on.
- **Maximum Depth** (LC 104) — another minimal structural recursion.
- **Binary Tree Level Order Traversal** (LC 102) — uses the same BFS queue scaffold.

---

**→ Next:** [`02-Maximum-Depth.md`](./02-Maximum-Depth.md) | Back to [`00-Index.md`](./00-Index.md)
