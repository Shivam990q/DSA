# Validate Binary Search Tree

**Platform**: LeetCode 98 · **Difficulty**: Medium · **Topics**: Tree, DFS, BST, Binary Tree · **Pattern**: Tightening open-interval bounds / in-order monotonicity

---

## 📜 Problem Statement

Given the `root` of a binary tree, determine if it is a **valid binary search tree (BST)**.

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys **strictly less than** the node's key.
- The right subtree of a node contains only nodes with keys **strictly greater than** the node's key.
- Both the left and right subtrees must also be binary search trees.

### Examples

**Example 1:**
```
Input:  root = [2,1,3]
Output: true

      2
     / \
    1   3      1 < 2 < 3 ✓
```

**Example 2:**
```
Input:  root = [5,1,4,null,null,3,6]
Output: false

        5
       / \
      1   4         4 is in the right subtree of 5 but 4 < 5 → invalid
         / \
        3   6
```

**Example 3:**
```
Input:  root = [5,4,6,null,null,3,7]
Output: false

        5
       / \
      4   6
         / \
        3   7      3 is in 5's right subtree but 3 < 5 → invalid (the classic trap)
```

### Constraints
```
The number of nodes in the tree is in the range [1, 10^4].
-2^31 <= Node.val <= 2^31 - 1
```

---

## 🧠 Understanding the problem

The deceptively hard part is that the BST property is **global**, not local. It is *not* enough that each node is greater than its left child and less than its right child. Every node in a node's *entire* left subtree must be smaller, and every node in its *entire* right subtree must be larger. Example 3 is the classic trap: `3` satisfies its immediate parent `6` (as `6`'s left child) but violates the ancestor `5` because it sits in `5`'s right subtree.

Two correct framings:
1. **Bounds**: each node must lie in an open interval `(low, high)` that *tightens* as you descend. Going left lowers the upper bound to the parent's value; going right raises the lower bound to the parent's value.
2. **In-order**: an in-order traversal of a valid BST yields **strictly increasing** values. Validate by checking each visited value exceeds the previous.

---

## Approach 1 — Recursive interval bounds (optimal) ⭐

### Intuition
Pass each node the open interval `(low, high)` it is allowed to occupy. The root may be anything: `(-∞, +∞)`. When we go left, the value becomes the new upper bound; when we go right, it becomes the new lower bound. A node is invalid the instant it falls outside its interval.

### Algorithm
1. `valid(node, low, high)`:
   - If `node` is null, return true.
   - If `node->val <= low` or `node->val >= high`, return false.
   - Return `valid(left, low, node->val) && valid(right, node->val, high)`.
2. Call `valid(root, -∞, +∞)` (use `long`/64-bit sentinels so `INT_MIN`/`INT_MAX` node values don't false-trigger).

### Dry run on `[5,4,6,null,null,3,7]`
```
valid(5, -inf, +inf): ok; left → (-inf,5), right → (5,+inf)
  valid(4, -inf, 5): ok (4<5); leaves null → true
  valid(6, 5, +inf): ok; left → (5,6), right → (6,+inf)
    valid(3, 5, 6): 3 <= low(5)? yes → return false
→ false   ✓ (catches the ancestor violation)
```

### Code
```cpp
class Solution {
    bool valid(TreeNode* node, long low, long high) {
        if (!node) return true;
        if (node->val <= low || node->val >= high) return false;
        return valid(node->left, low, node->val) &&
               valid(node->right, node->val, high);
    }
public:
    bool isValidBST(TreeNode* root) {
        return valid(root, LONG_MIN, LONG_MAX);
    }
};
```
```java
class Solution {
    private boolean valid(TreeNode node, long low, long high) {
        if (node == null) return true;
        if (node.val <= low || node.val >= high) return false;
        return valid(node.left, low, node.val) &&
               valid(node.right, node.val, high);
    }
    public boolean isValidBST(TreeNode root) {
        return valid(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
}
```
```python
def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return valid(node.left, low, node.val) and valid(node.right, node.val, high)
    return valid(root, float('-inf'), float('inf'))
```

### Complexity
- **Time**: O(n) — each node checked once.
- **Space**: O(h) — recursion stack.

### Verdict
The cleanest correct answer. The tightening-interval idea is the canonical mental model for BST validation and generalizes to many range problems. This is what you present.

---

## Approach 2 — Iterative in-order, check monotonicity (optimal) ⭐

### Intuition
In-order traversal visits BST nodes in **sorted** order. So validate by walking in-order and confirming each value is **strictly greater** than the previously visited value. The first violation means "not a BST."

### Algorithm
1. Use an explicit stack for iterative in-order; track `prev = -∞`.
2. Repeatedly push all left descendants, pop a node, compare `node->val` to `prev`:
   - If `node->val <= prev`, return false.
   - Set `prev = node->val`, then move to `node->right`.
3. If the traversal completes, return true.

### Dry run on `[5,1,4,null,null,3,6]`
```
in-order order would be: 1, 5, 3, 6, 4
prev=-inf → 1 (>-inf) ok, prev=1
→ 5 (>1) ok, prev=5
→ 3 (>5? no) → return false   ✓
```

### Code
```cpp
bool isValidBST(TreeNode* root) {
    stack<TreeNode*> st;
    TreeNode* cur = root;
    long prev = LONG_MIN;
    while (cur || !st.empty()) {
        while (cur) { st.push(cur); cur = cur->left; }
        cur = st.top(); st.pop();
        if (cur->val <= prev) return false;
        prev = cur->val;
        cur = cur->right;
    }
    return true;
}
```
```java
public boolean isValidBST(TreeNode root) {
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root;
    long prev = Long.MIN_VALUE;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        cur = st.pop();
        if (cur.val <= prev) return false;
        prev = cur.val;
        cur = cur.right;
    }
    return true;
}
```
```python
def isValidBST(root):
    st = []
    cur = root
    prev = float('-inf')
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        if cur.val <= prev:
            return False
        prev = cur.val
        cur = cur.right
    return True
```

### Complexity
- **Time**: O(n).
- **Space**: O(h) — the stack holds a leftmost path.

### Verdict
Equally optimal and a great alternative framing. It also early-exits at the first out-of-order value. Knowing both the bounds and in-order views shows real BST fluency.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive interval bounds | O(n) | O(h) | tightening `(low, high)`; the default ⭐ |
| Iterative in-order | O(n) | O(h) | sorted-order monotonic check ⭐ |

Both are O(n)/O(h) and both early-exit. The bounds approach is the more general mental model; the in-order approach reuses the universal "BST in-order = sorted" fact.

---

## 🧪 Edge cases & pitfalls
- **Single node** → valid.
- **Duplicate values** → invalid in a *strict* BST. The checks use `<=`/`>=` (bounds) and `<=` (in-order) to reject equals.
- **INT_MIN / INT_MAX node values** → a node may legitimately equal `2^31-1`. Using `int` bounds with `INT_MIN`/`INT_MAX` sentinels would false-reject; use `long` (or `float('-inf')`/`inf` in Python), or pass nullable bounds.
- **Pitfall — only checking parent–child**: the most common bug. `node.left.val < node.val < node.right.val` is necessary but *not sufficient* (Example 3). Validation must enforce ancestor bounds.
- **Pitfall (in-order) — initializing `prev` to 0**: a tree of all-negative values would break. Use `-∞`/`LONG_MIN` or a "first node" flag.

---

## 🔗 Related problems
- **Kth Smallest Element in a BST** (LC 230) — uses the same in-order ordering. See [`12-Kth-Smallest-in-BST.md`](./12-Kth-Smallest-in-BST.md).
- **Lowest Common Ancestor of a BST** (LC 235) — exploits the same ordering. See [`07-Lowest-Common-Ancestor-BST.md`](./07-Lowest-Common-Ancestor-BST.md).
- **Recover Binary Search Tree** (LC 99) — find two swapped nodes via in-order.
- **Range Sum of BST** (LC 938) — interval-bounded BST traversal.

---

**→ Next:** [`12-Kth-Smallest-in-BST.md`](./12-Kth-Smallest-in-BST.md) | **← Prev:** [`10-Count-Good-Nodes.md`](./10-Count-Good-Nodes.md) | Back to [`00-Index.md`](./00-Index.md)
