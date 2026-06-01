# Lowest Common Ancestor of a Binary Search Tree

**Platform**: LeetCode 235 · **Difficulty**: Medium · **Topics**: Tree, DFS, BST, Binary Tree · **Pattern**: BST ordering to find the split point

---

## 📜 Problem Statement

Given a binary search tree (BST), find the **lowest common ancestor (LCA)** of two given nodes in the BST.

The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow **a node to be a descendant of itself**).

### Examples

**Example 1:**
```
Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6

              6
           /     \
          2       8
         / \     / \
        0   4   7   9
           / \
          3   5
p=2 and q=8 split at the root → LCA = 6
```

**Example 2:**
```
Input:  root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
Explanation: A node can be a descendant of itself; q=4 lies under p=2, so LCA = 2.
```

**Example 3:**
```
Input:  root = [2,1], p = 2, q = 1
Output: 2
```

### Constraints
```
The number of nodes in the tree is in the range [2, 10^5].
-10^9 <= Node.val <= 10^9
All Node.val are unique.
p != q
Both p and q exist in the BST.
```

---

## 🧠 Understanding the problem

This is the LCA problem, but with a **BST** — and the BST ordering (`left < node < right`) makes it dramatically easier than the general-tree version.

Stand at any node and compare it to `p` and `q`:
- If **both** `p` and `q` are **smaller** than the node, the LCA must be in the left subtree → go left.
- If **both** are **larger**, the LCA is in the right subtree → go right.
- Otherwise they **split** here (one ≤ node ≤ other, or the node equals one of them). This is the *first* node where the paths to `p` and `q` diverge — that is the LCA.

Because each comparison discards an entire subtree, the walk is O(height), not O(n). No need to inspect the whole tree.

---

## Approach 1 — Iterative BST walk (optimal) ⭐

### Intuition
Descend from the root following the BST comparison rule until `p` and `q` fall on opposite sides (or one equals the current node). The node where they no longer agree on direction is the split point — the LCA.

### Algorithm
1. Start `node = root`.
2. Loop:
   - If both `p->val` and `q->val` `< node->val` → `node = node->left`.
   - Else if both `> node->val` → `node = node->right`.
   - Else → return `node` (split point / one equals node).

### Dry run on Example 1 (`p = 2, q = 8`)
```
node=6: p=2<6 and q=8>6 → not both-less, not both-greater → split → return 6  ✓
```
On `p = 2, q = 4`:
```
node=6: both < 6 → go left → node=2
node=2: p=2 == 2 (not both-less since one equals), q=4>2 → split → return 2  ✓
```

### Code
```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    TreeNode* node = root;
    while (node) {
        if (p->val < node->val && q->val < node->val)
            node = node->left;
        else if (p->val > node->val && q->val > node->val)
            node = node->right;
        else
            return node;
    }
    return nullptr;
}
```
```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    TreeNode node = root;
    while (node != null) {
        if (p.val < node.val && q.val < node.val)
            node = node.left;
        else if (p.val > node.val && q.val > node.val)
            node = node.right;
        else
            return node;
    }
    return null;
}
```
```python
def lowestCommonAncestor(root, p, q):
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
    return None
```

### Complexity
- **Time**: O(h) — one node per level until the split; O(log n) for a balanced BST, O(n) worst case for a skewed one.
- **Space**: O(1) — only a moving pointer; no recursion, no extra structures.

### Verdict
The optimal answer: O(h) time and O(1) space. The iterative form is preferred because it avoids recursion entirely. This is what you present.

---

## Approach 2 — Recursive BST walk

### Intuition
The same rule expressed recursively: recurse left when both targets are smaller, right when both are larger, otherwise the current node is the LCA.

### Algorithm
1. If both values `< root->val` → recurse on `root->left`.
2. If both values `> root->val` → recurse on `root->right`.
3. Otherwise return `root`.

### Code
```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (p->val < root->val && q->val < root->val)
        return lowestCommonAncestor(root->left, p, q);
    if (p->val > root->val && q->val > root->val)
        return lowestCommonAncestor(root->right, p, q);
    return root;
}
```
```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (p.val < root.val && q.val < root.val)
        return lowestCommonAncestor(root.left, p, q);
    if (p.val > root.val && q.val > root.val)
        return lowestCommonAncestor(root.right, p, q);
    return root;
}
```
```python
def lowestCommonAncestor(root, p, q):
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor(root.right, p, q)
    return root
```

### Complexity
- **Time**: O(h).
- **Space**: O(h) — recursion stack (the only downside vs the iterative form).

### Verdict
Equally correct and arguably the most readable. Costs O(h) stack space, so the iterative version edges it out in practice. Either is interview-acceptable.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Iterative BST walk | O(h) | **O(1)** | optimal; no recursion ⭐ |
| Recursive BST walk | O(h) | O(h) | most readable; uses call stack |

Both exploit BST ordering to discard half the tree at each step. The only difference is stack usage. Note: the **general-tree** LCA (LC 236) cannot use ordering and needs an O(n) post-order search instead.

---

## 🧪 Edge cases & pitfalls
- **One node is an ancestor of the other** (Example 2) → the ancestor itself is the LCA. The "split" branch handles it because equality breaks the strict `<`/`>` checks.
- **p and q on opposite sides of the root** → root is the LCA immediately.
- **Skewed BST** → walk degrades to O(n), still correct.
- **Pitfall — using `<=` / `>=`**: with strict `<` and `>`, the case "current node equals `p` or `q`" correctly falls through to `return node`. Using `<=`/`>=` would wrongly step past an answer node.
- **Pitfall — forgetting BST ⇒ ordering**: applying the generic O(n) LCA here works but throws away the BST advantage; interviewers want the O(h) ordering solution.

---

## 🔗 Related problems
- **Lowest Common Ancestor of a Binary Tree** (LC 236) — general tree, no ordering; post-order recursion returning the first node that sees both.
- **Validate Binary Search Tree** (LC 98) — same BST-interval reasoning. See [`11-Validate-BST.md`](./11-Validate-BST.md).
- **Insert into a BST** (LC 701) — same downward comparison walk.
- **Search in a BST** (LC 700) — the simplest version of this descent.

---

**→ Next:** [`08-Binary-Tree-Level-Order-Traversal.md`](./08-Binary-Tree-Level-Order-Traversal.md) | **← Prev:** [`06-Subtree-of-Another-Tree.md`](./06-Subtree-of-Another-Tree.md) | Back to [`00-Index.md`](./00-Index.md)
