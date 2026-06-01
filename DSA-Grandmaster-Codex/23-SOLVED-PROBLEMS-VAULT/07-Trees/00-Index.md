# 🌳 Trees — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

> Trees are the single biggest interview topic. Nearly every tree problem reduces to one of two engines: **DFS** (recursion that bubbles values up from children) or **BFS** (a queue that processes the tree level by level). Master those two engines and the rest is variation.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Invert Binary Tree](./01-Invert-Binary-Tree.md) | 226 | Easy | recursive swap → iterative BFS/DFS |
| 02 | [Maximum Depth of Binary Tree](./02-Maximum-Depth.md) | 104 | Easy | recursive DFS → iterative BFS → iterative DFS |
| 03 | [Diameter of Binary Tree](./03-Diameter-of-Binary-Tree.md) | 543 | Easy | brute height-per-node → single-pass height+global |
| 04 | [Balanced Binary Tree](./04-Balanced-Binary-Tree.md) | 110 | Easy | top-down O(n²) → bottom-up sentinel O(n) |
| 05 | [Same Tree](./05-Same-Tree.md) | 100 | Easy | recursive → iterative |
| 06 | [Subtree of Another Tree](./06-Subtree-of-Another-Tree.md) | 572 | Easy | recursive sameTree → serialization + substring |
| 07 | [Lowest Common Ancestor of a BST](./07-Lowest-Common-Ancestor-BST.md) | 235 | Medium | recursive BST walk → iterative BST walk |
| 08 | [Binary Tree Level Order Traversal](./08-Binary-Tree-Level-Order-Traversal.md) | 102 | Medium | BFS queue → DFS with level index |
| 09 | [Binary Tree Right Side View](./09-Binary-Tree-Right-Side-View.md) | 199 | Medium | BFS last-of-level → DFS right-first |
| 10 | [Count Good Nodes in Binary Tree](./10-Count-Good-Nodes.md) | 1448 | Medium | DFS carrying path-max → iterative |
| 11 | [Validate Binary Search Tree](./11-Validate-BST.md) | 98 | Medium | range bounds DFS → in-order monotonic |
| 12 | [Kth Smallest Element in a BST](./12-Kth-Smallest-in-BST.md) | 230 | Medium | in-order list → iterative in-order early-stop |
| 13 | [Construct Tree from Preorder & Inorder](./13-Construct-Tree-Preorder-Inorder.md) | 105 | Medium | O(n²) search → hashmap index O(n) |
| 14 | [Binary Tree Maximum Path Sum](./14-Binary-Tree-Maximum-Path-Sum.md) | 124 | Hard | single-pass gain + global best |
| 15 | [Serialize and Deserialize Binary Tree](./15-Serialize-Deserialize-Binary-Tree.md) | 297 | Hard | preorder + null markers → BFS encoding |

---

## 🧱 The TreeNode definition

Every problem in this set uses LeetCode's standard binary-tree node. Internalize all three so the signatures below read naturally.

**C++**
```cpp
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *l, TreeNode *r) : val(x), left(l), right(r) {}
};
```

**Java**
```java
public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
```

**Python**
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## 🎯 The pattern family

Tree problems are dominated by two traversal engines. Learning which engine a problem wants is 80% of the battle.

**1. DFS — recursion that bubbles values up (the workhorse).**
The mental model: *"What do I need from my left and right subtrees to answer for myself, and what do I return to my parent?"* This single sentence solves the majority of tree problems.
- **Return a computed value upward** → Maximum Depth, Diameter, Balanced, Count Good Nodes, Max Path Sum. The recurring trick: return one quantity to the parent while updating a *global best* with a richer quantity.
- **Compare / mirror two trees in lockstep** → Same Tree, Subtree, Invert.
- **Carry context downward** → Count Good Nodes (path max), Validate BST (open interval bounds).

**2. BFS — a queue, level by level.**
The mental model: *"I care about depth, or about per-level aggregation."* Process exactly `queue.size()` nodes per iteration to isolate one level.
- **Per-level grouping** → Level Order Traversal.
- **One representative per level** → Right Side View (the last node of each level).

**3. BST-specific ordering.**
A Binary Search Tree adds the invariant *left < node < right*. Two superpowers fall out:
- **In-order traversal yields sorted order** → Kth Smallest, Validate BST.
- **Compare target values to the node to prune half the tree** → LCA of a BST (O(h) walk).

**4. Reconstruction & encoding.**
- **Rebuild structure from traversals** → Construct from Preorder + Inorder (preorder gives roots, inorder splits subtrees).
- **Flatten to a string and back** → Serialize/Deserialize (preorder with explicit null markers captures structure uniquely).

> **Complexity intuition**: a full traversal is O(n) time. Recursion uses O(h) stack space where `h` is height — O(log n) for balanced trees, O(n) for a degenerate (linked-list-shaped) tree. BFS uses O(w) space where `w` is the maximum level width, up to O(n).

---

**→ Start:** [`01-Invert-Binary-Tree.md`](./01-Invert-Binary-Tree.md) | Back to [vault index](../00-Index.md)
