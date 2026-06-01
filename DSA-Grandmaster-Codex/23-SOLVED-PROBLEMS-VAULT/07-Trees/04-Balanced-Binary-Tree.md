# Balanced Binary Tree

**Platform**: LeetCode 110 · **Difficulty**: Easy · **Topics**: Tree, DFS, Binary Tree · **Pattern**: Bottom-up height with sentinel short-circuit

---

## 📜 Problem Statement

Given a binary tree, determine if it is **height-balanced**.

A height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of *every* node never differs by more than one.

### Examples

**Example 1:**
```
Input:  root = [3,9,20,null,null,15,7]
Output: true

        3
       / \
      9  20
        /  \
       15   7      every node's subtrees differ in height by ≤ 1
```

**Example 2:**
```
Input:  root = [1,2,2,3,3,null,null,4,4]
Output: false

            1
           / \
          2   2
         / \
        3   3
       / \
      4   4        node 1's left subtree is height 3, right is height 0 → unbalanced
```

**Example 3:**
```
Input:  root = []
Output: true
Explanation: An empty tree is balanced.
```

### Constraints
```
The number of nodes in the tree is in the range [0, 5000].
-10^4 <= Node.val <= 10^4
```

---

## 🧠 Understanding the problem

"Balanced" must hold at **every** node, not just the root: for each node the heights of its left and right subtrees may differ by at most `1`. So we need two pieces of information at every node — its height, and whether its subtree is already balanced.

The naive route computes height separately from the balance check, which recomputes heights wastefully. The elegant route fuses them: a single DFS returns the height **and** signals imbalance using a sentinel value (`-1`). Once any subtree reports `-1`, that answer propagates all the way up and short-circuits the rest of the work.

---

## Approach 1 — Top-down (height inside check) — O(n²)

### Intuition
Translate the definition literally. For each node, compute the heights of both subtrees, verify they differ by ≤ 1, then recursively confirm both subtrees are themselves balanced.

### Algorithm
1. `height(node)` returns node-height (null → `0`).
2. `isBalanced(node)`: if null, return true.
3. Check `abs(height(left) - height(right)) <= 1`.
4. AND recursively `isBalanced(left)` AND `isBalanced(right)`.

### Code
```cpp
int height(TreeNode* node) {
    if (!node) return 0;
    return 1 + max(height(node->left), height(node->right));
}
bool isBalanced(TreeNode* root) {
    if (!root) return true;
    if (abs(height(root->left) - height(root->right)) > 1) return false;
    return isBalanced(root->left) && isBalanced(root->right);
}
```
```java
private int height(TreeNode node) {
    if (node == null) return 0;
    return 1 + Math.max(height(node.left), height(node.right));
}
public boolean isBalanced(TreeNode root) {
    if (root == null) return true;
    if (Math.abs(height(root.left) - height(root.right)) > 1) return false;
    return isBalanced(root.left) && isBalanced(root.right);
}
```
```python
def isBalanced(root):
    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    if not root:
        return True
    if abs(height(root.left) - height(root.right)) > 1:
        return False
    return isBalanced(root.left) and isBalanced(root.right)
```

### Complexity
- **Time**: O(n²) — `height` is recomputed for every node; on a skewed tree this is quadratic.
- **Space**: O(h) recursion.

### Verdict
Correct and readable, but it recomputes heights repeatedly. The fix is to compute height once, bottom-up.

---

## Approach 2 — Bottom-up sentinel (optimal) ⭐

### Intuition
Process children **before** the parent. Each call returns the subtree height, but if it ever discovers an imbalance, it returns the sentinel `-1` instead. Because we check children first, the moment one returns `-1`, the parent immediately returns `-1` too — no height arithmetic, no further recursion. This collapses the work to a single O(n) traversal.

### Algorithm
1. Define `check(node)` returning height, or `-1` if any descendant subtree is unbalanced.
2. If null, return `0`.
3. `l = check(left)`; if `l == -1` return `-1`.
4. `r = check(right)`; if `r == -1` return `-1`.
5. If `abs(l - r) > 1` return `-1`.
6. Otherwise return `1 + max(l, r)`.
7. `isBalanced` returns `check(root) != -1`.

### Dry run on `[1,2,2,3,3,null,null,4,4]`
```
check(4)=1, check(4)=1
check(3 with two 4s): l=1, r=1, |0|≤1 → return 2
check(3 leaf): return 1
check(2): l=check(3-subtree)=2, r=check(3 leaf)=1, |2-1|≤1 → return 3
check(2 right leaf): return 1
check(1): l=3, r=1, |3-1| = 2 > 1 → return -1
isBalanced = (-1 != -1) → false   ✓
```

### Code
```cpp
class Solution {
    int check(TreeNode* node) {
        if (!node) return 0;
        int l = check(node->left);
        if (l == -1) return -1;
        int r = check(node->right);
        if (r == -1) return -1;
        if (abs(l - r) > 1) return -1;
        return 1 + max(l, r);
    }
public:
    bool isBalanced(TreeNode* root) {
        return check(root) != -1;
    }
};
```
```java
class Solution {
    private int check(TreeNode node) {
        if (node == null) return 0;
        int l = check(node.left);
        if (l == -1) return -1;
        int r = check(node.right);
        if (r == -1) return -1;
        if (Math.abs(l - r) > 1) return -1;
        return 1 + Math.max(l, r);
    }
    public boolean isBalanced(TreeNode root) {
        return check(root) != -1;
    }
}
```
```python
def isBalanced(root):
    def check(node):
        if not node:
            return 0
        l = check(node.left)
        if l == -1:
            return -1
        r = check(node.right)
        if r == -1:
            return -1
        if abs(l - r) > 1:
            return -1
        return 1 + max(l, r)
    return check(root) != -1
```

### Complexity
- **Time**: O(n) — each node visited once; `-1` short-circuits the rest.
- **Space**: O(h) — recursion stack.

### Verdict
The optimal answer. The sentinel `-1` overloads the return value to mean both "height" and "already failed," which is what kills the redundant recomputation. This bottom-up fusion is the lesson of the problem.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Top-down height-in-check | O(n²) | O(h) | recomputes heights; baseline |
| Bottom-up sentinel | **O(n)** | O(h) | compute height once, signal `-1` ⭐ |

Same as Diameter, the win is "don't recompute what the recursion already produced." The extra trick here is encoding failure into the same return value so it propagates instantly.

---

## 🧪 Edge cases & pitfalls
- **Empty tree** → balanced (`true`).
- **Single node** → balanced.
- **Perfectly skewed tree** (a chain) → unbalanced as soon as a height gap exceeds 1.
- **Pitfall — checking only the root**: balance must hold at *every* node. The recursion enforces it everywhere; checking just the root's two subtree heights is wrong.
- **Pitfall — returning height when unbalanced**: once you decide a subtree is unbalanced you must return the sentinel `-1`, not a real height, otherwise the parent computes a misleading balanced result.
- **Pitfall — short-circuit order**: check `l == -1` *before* recursing right to gain the early exit; checking after still works but does extra work.

---

## 🔗 Related problems
- **Maximum Depth** (LC 104) — the height computation reused here. See [`02-Maximum-Depth.md`](./02-Maximum-Depth.md).
- **Diameter of Binary Tree** (LC 543) — same bottom-up height fusion. See [`03-Diameter-of-Binary-Tree.md`](./03-Diameter-of-Binary-Tree.md).
- **Convert Sorted Array to BST** (LC 108) — builds a height-balanced tree.
- **Balanced Binary Tree (AVL concepts)** — the real-world structure that maintains this invariant on insertion.

---

**→ Next:** [`05-Same-Tree.md`](./05-Same-Tree.md) | **← Prev:** [`03-Diameter-of-Binary-Tree.md`](./03-Diameter-of-Binary-Tree.md) | Back to [`00-Index.md`](./00-Index.md)
