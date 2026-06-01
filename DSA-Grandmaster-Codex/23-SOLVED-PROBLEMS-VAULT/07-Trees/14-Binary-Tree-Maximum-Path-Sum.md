# Binary Tree Maximum Path Sum

**Platform**: LeetCode 124 · **Difficulty**: Hard · **Topics**: Tree, DFS, Dynamic Programming, Binary Tree · **Pattern**: Gain-up return + global best (through-node)

---

## 📜 Problem Statement

A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does **not** need to pass through the root.

The **path sum** of a path is the sum of the node's values in the path.

Given the `root` of a binary tree, return *the maximum path sum of any non-empty path*.

### Examples

**Example 1:**
```
Input:  root = [1,2,3]
Output: 6

      1
     / \
    2   3      best path: 2 → 1 → 3 = 6
```

**Example 2:**
```
Input:  root = [-10,9,20,null,null,15,7]
Output: 42

        -10
        /  \
       9   20
          /  \
         15   7      best path: 15 → 20 → 7 = 42 (skips the negative root)
```

**Example 3:**
```
Input:  root = [-3]
Output: -3
Explanation: A single (negative) node is still a valid non-empty path.
```

### Constraints
```
The number of nodes in the tree is in the range [1, 3 * 10^4].
-1000 <= Node.val <= 1000
```

---

## 🧠 Understanding the problem

The tricky part is the distinction between two different quantities at each node:

1. **The best path that can be *extended upward* through this node to its parent.** Such a path can use the node plus **at most one** child branch (you cannot go down both children and still come back up to the parent — that would visit the node twice). This is what we **return** to the parent: `node->val + max(0, max(leftGain, rightGain))`.

2. **The best path that *bends* at this node (its highest point is here).** Such a path may use **both** children: `node->val + leftGain + rightGain`. This is a candidate for the global answer but **cannot** be returned upward (it has no free end to attach to the parent). So we use it only to **update a global maximum**.

The `max(0, …)` clamp is the other key idea: if a child's best gain is negative, we simply **don't take that branch** (contribute `0` instead). Because every node is a valid path on its own, the global best correctly handles all-negative trees.

This "return one value, update a global with a richer value" structure is identical to Diameter — here with weights instead of edge counts.

---

## Approach 1 — Single-pass gain with global best (optimal) ⭐

### Intuition
Define `gain(node)` = the maximum sum obtainable by starting at `node` and going **straight down** (using at most one child branch). While computing it, we already know `leftGain` and `rightGain`, so we can evaluate the "bend at this node" path (`node + leftGain + rightGain`) and fold it into a global best. Then return the up-extendable gain to the parent.

### Algorithm
1. Global `best = -∞`.
2. `gain(node)`:
   - If null, return `0`.
   - `l = max(0, gain(left))` — drop negative branches.
   - `r = max(0, gain(right))`.
   - Update `best = max(best, node->val + l + r)` — path bending here.
   - Return `node->val + max(l, r)` — path continuing upward.
3. Call `gain(root)`; return `best`.

### Dry run on `[-10,9,20,null,null,15,7]`
```
gain(9): leaves → l=r=0; best=max(-inf, 9)=9; return 9
gain(15): best=max(9,15)=15; return 15
gain(7):  best=max(15,7)=15; return 7
gain(20): l=15, r=7; best=max(15, 20+15+7=42)=42; return 20+max(15,7)=35
gain(-10): l=max(0,9)=9, r=max(0,35)=35;
           best=max(42, -10+9+35=34)=42; return -10+35=25
answer = best = 42   ✓  (path 15→20→7)
```

### Code
```cpp
class Solution {
    int best;
    int gain(TreeNode* node) {
        if (!node) return 0;
        int l = max(0, gain(node->left));
        int r = max(0, gain(node->right));
        best = max(best, node->val + l + r);   // path bending at node
        return node->val + max(l, r);          // path continuing upward
    }
public:
    int maxPathSum(TreeNode* root) {
        best = INT_MIN;
        gain(root);
        return best;
    }
};
```
```java
class Solution {
    private int best;
    private int gain(TreeNode node) {
        if (node == null) return 0;
        int l = Math.max(0, gain(node.left));
        int r = Math.max(0, gain(node.right));
        best = Math.max(best, node.val + l + r);   // path bending at node
        return node.val + Math.max(l, r);          // path continuing upward
    }
    public int maxPathSum(TreeNode root) {
        best = Integer.MIN_VALUE;
        gain(root);
        return best;
    }
}
```
```python
def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        l = max(0, gain(node.left))
        r = max(0, gain(node.right))
        best = max(best, node.val + l + r)   # path bending at node
        return node.val + max(l, r)          # path continuing upward
    gain(root)
    return best
```

### Complexity
- **Time**: O(n) — each node visited once.
- **Space**: O(h) — recursion stack.

### Verdict
The optimal answer and a textbook Hard-tier DFS. The crux is the discipline of returning the **single-branch** gain while updating the global with the **two-branch** bend. Get that distinction right and the code is tiny.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Single-pass gain + global best | **O(n)** | O(h) | the only sensible approach ⭐ |

There is no meaningfully different second approach for the optimal solution — any correct method computes, per node, the through-path while returning the up-path. (A brute force that, for every node, explores all paths would be exponential and is never used.) The single-pass DFS is *the* answer.

---

## 🧪 Edge cases & pitfalls
- **Single node** → return its value (could be negative, e.g. Example 3 → `-3`).
- **All negative values** → the answer is the single largest (least negative) node. The `max(0, …)` clamp ensures we never *force* adding a negative child, and `best` (seeded at `-∞`) captures the lone-node path. Note: we clamp the **child gains**, not the node itself — the node must always be included in `node + l + r`.
- **Pitfall — returning the two-branch sum**: never return `node + l + r` upward; that path cannot attach to a parent. Return `node + max(l, r)`.
- **Pitfall — seeding `best` with 0**: an all-negative tree would wrongly return `0`. Seed with `INT_MIN`/`-inf`.
- **Pitfall — clamping the node value too**: only the *child gains* get `max(0, …)`. The current node is mandatory in both the bend and the up-path.
- **Pitfall — integer overflow**: with up to 3×10⁴ nodes and values up to 1000, sums fit in 32-bit int; still, be mindful in languages with tighter limits.

---

## 🔗 Related problems
- **Diameter of Binary Tree** (LC 543) — identical structure, counting edges instead of summing values. See [`03-Diameter-of-Binary-Tree.md`](./03-Diameter-of-Binary-Tree.md).
- **Path Sum III** (LC 437) — count downward paths summing to a target.
- **Longest Univalue Path** (LC 687) — same gain-up/best-through with an equality constraint.
- **House Robber III** (LC 337) — tree DP returning a pair (rob / skip) upward.

---

**→ Next:** [`15-Serialize-Deserialize-Binary-Tree.md`](./15-Serialize-Deserialize-Binary-Tree.md) | **← Prev:** [`13-Construct-Tree-Preorder-Inorder.md`](./13-Construct-Tree-Preorder-Inorder.md) | Back to [`00-Index.md`](./00-Index.md)
