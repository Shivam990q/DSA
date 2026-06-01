# Diameter of Binary Tree

**Platform**: LeetCode 543 · **Difficulty**: Easy · **Topics**: Tree, DFS, Binary Tree · **Pattern**: Bottom-up height + global best

---

## 📜 Problem Statement

Given the `root` of a binary tree, return the length of the **diameter** of the tree.

The diameter of a binary tree is the **length of the longest path between any two nodes** in a tree. This path may or may not pass through the `root`.

The length of a path between two nodes is represented by the **number of edges** between them.

### Examples

**Example 1:**
```
Input:  root = [1,2,3,4,5]
Output: 3

        1
       / \
      2   3
     / \
    4   5

Longest path: 4 → 2 → 1 → 3  (or 5 → 2 → 1 → 3) = 3 edges
```

**Example 2:**
```
Input:  root = [1,2]
Output: 1
Explanation: The path 2 → 1 has length 1 edge.
```

**Example 3:**
```
Input:  root = [1]
Output: 0
Explanation: A single node has no edges.
```

### Constraints
```
The number of nodes in the tree is in the range [1, 10^4].
-100 <= Node.val <= 100
```

---

## 🧠 Understanding the problem

The diameter is the longest "wiggle" path you can draw through the tree, measured in edges. The key insight is to ask, for **each node**, *"What is the longest path whose highest point is exactly this node?"*

A path turning at a node goes **down into the left subtree, up to the node, then down into the right subtree**. Its length in edges is therefore `leftHeight + rightHeight`, where height is measured in edges from the node to its deepest descendant. The global diameter is just the maximum of that quantity over all nodes.

This sets up a classic tree pattern: a single DFS computes **height** (the value each node returns to its parent) while *simultaneously* updating a **global best** with the richer "path through this node" quantity. One traversal, two purposes.

---

## Approach 1 — Height per node, recompute (brute force)

### Intuition
Directly translate the definition: the diameter through a node is `height(left) + height(right)`. Compute that for every node by calling a separate `height` function, and take the maximum.

### Algorithm
1. Write `height(node)` returning edge-height of the subtree (null → `-1` so a leaf is `0`, or null → `0` counting nodes; here we count nodes for simplicity and combine).
2. For every node, compute `height(left) + height(right)` and track the max.
3. Recurse into children to repeat for every node.

### Code
```cpp
int height(TreeNode* node) {
    if (!node) return 0;
    return 1 + max(height(node->left), height(node->right));
}
int diameterOfBinaryTree(TreeNode* root) {
    if (!root) return 0;
    int through = height(root->left) + height(root->right);
    int left  = diameterOfBinaryTree(root->left);
    int right = diameterOfBinaryTree(root->right);
    return max(through, max(left, right));
}
```
```java
private int height(TreeNode node) {
    if (node == null) return 0;
    return 1 + Math.max(height(node.left), height(node.right));
}
public int diameterOfBinaryTree(TreeNode root) {
    if (root == null) return 0;
    int through = height(root.left) + height(root.right);
    int left  = diameterOfBinaryTree(root.left);
    int right = diameterOfBinaryTree(root.right);
    return Math.max(through, Math.max(left, right));
}
```
```python
def diameterOfBinaryTree(root):
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if not root:
        return 0
    through = height(root.left) + height(root.right)
    left = diameterOfBinaryTree(root.left)
    right = diameterOfBinaryTree(root.right)
    return max(through, left, right)
```

### Complexity
- **Time**: O(n²) — for every node we recompute heights from scratch; on a skewed tree this degrades to O(n²).
- **Space**: O(h) recursion.

### Verdict
Correct but wasteful: heights are recomputed over and over. It proves we understand the definition; now we fold the two passes into one.

---

## Approach 2 — Single-pass height + global best (optimal) ⭐

### Intuition
We never needed two passes. While computing a node's height (which we must do anyway), we already know `leftHeight` and `rightHeight`. That is exactly the diameter through this node — so update a global maximum right there, then return the height upward. Each node is touched once.

### Algorithm
1. Keep a global `best = 0` (diameter in edges).
2. Define `height(node)` returning **edge-height** (null → `0` for a leaf's child, so a leaf returns `1` node-height; we'll use node-counts and subtract appropriately, or use the clean edge form below).
3. In `height(node)`:
   - If null, return `0`.
   - `l = height(left)`, `r = height(right)`.
   - Update `best = max(best, l + r)` — the path through `node` in edges.
   - Return `1 + max(l, r)`.
4. Answer is `best`.

> Here `height` returns the number of nodes on the longest downward chain; `l + r` then equals the edge count of the path bending at `node` (l edges down-left + r edges down-right).

### Dry run on `[1,2,3,4,5]`
```
height(4)=1, height(5)=1
height(2): l=1 (node4), r=1 (node5)
           best = max(0, 1+1) = 2
           return 1 + max(1,1) = 2
height(3): leaf → best stays, return 1
height(1): l=2 (subtree 2), r=1 (node3)
           best = max(2, 2+1) = 3      ← path 4→2→1→3
           return 1 + max(2,1) = 3
answer = best = 3   ✓
```

### Code
```cpp
class Solution {
    int best = 0;
    int height(TreeNode* node) {
        if (!node) return 0;
        int l = height(node->left);
        int r = height(node->right);
        best = max(best, l + r);     // edges in path bending at node
        return 1 + max(l, r);        // node-height returned upward
    }
public:
    int diameterOfBinaryTree(TreeNode* root) {
        best = 0;
        height(root);
        return best;
    }
};
```
```java
class Solution {
    private int best = 0;
    private int height(TreeNode node) {
        if (node == null) return 0;
        int l = height(node.left);
        int r = height(node.right);
        best = Math.max(best, l + r);   // edges in path bending at node
        return 1 + Math.max(l, r);      // node-height returned upward
    }
    public int diameterOfBinaryTree(TreeNode root) {
        best = 0;
        height(root);
        return best;
    }
}
```
```python
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        l = height(node.left)
        r = height(node.right)
        best = max(best, l + r)   # edges in path bending at node
        return 1 + max(l, r)      # node-height returned upward
    height(root)
    return best
```

### Complexity
- **Time**: O(n) — every node visited once.
- **Space**: O(h) — recursion stack.

### Verdict
The standard optimal answer. The "return one thing, update a global with a richer thing" pattern is the single most important DFS idiom in tree problems — it reappears in Max Path Sum, Balanced Tree, and many more.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Height per node | O(n²) | O(h) | recomputes heights; baseline only |
| Single-pass height + global | **O(n)** | O(h) | fold both passes into one ⭐ |

The optimization is the canonical "stop recomputing what the recursion already knows." Recognizing that `height` already exposes `l` and `r` is the whole trick.

---

## 🧪 Edge cases & pitfalls
- **Single node** → height chains are both `0`, diameter `0` edges.
- **Two nodes** → diameter `1`.
- **Pitfall — edges vs nodes**: the answer counts **edges**. `l + r` (where each is a node-height of the child chain) conveniently equals the edge count of the through-path. Don't add `+1` or `+2`.
- **Pitfall — the deepest path may not pass through the root**: a long left subtree can hold the diameter entirely. Updating `best` at *every* node (not just the root) is what captures this.
- **Pitfall — using a plain return instead of a global**: a single function cannot return both "height to bubble up" and "best diameter seen" cleanly without a global/outparam; trying to return only one loses information.

---

## 🔗 Related problems
- **Maximum Depth** (LC 104) — the `height` helper used here. See [`02-Maximum-Depth.md`](./02-Maximum-Depth.md).
- **Binary Tree Maximum Path Sum** (LC 124) — same "gain up / best through" structure with values. See [`14-Binary-Tree-Maximum-Path-Sum.md`](./14-Binary-Tree-Maximum-Path-Sum.md).
- **Longest Univalue Path** (LC 687) — diameter restricted to equal-valued nodes.
- **Diameter of N-Ary Tree** (LC 1522) — top two child heights.

---

**→ Next:** [`04-Balanced-Binary-Tree.md`](./04-Balanced-Binary-Tree.md) | **← Prev:** [`02-Maximum-Depth.md`](./02-Maximum-Depth.md) | Back to [`00-Index.md`](./00-Index.md)
