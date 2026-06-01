# Same Tree

**Platform**: LeetCode 100 · **Difficulty**: Easy · **Topics**: Tree, DFS, BFS, Binary Tree · **Pattern**: Lockstep two-tree comparison

---

## 📜 Problem Statement

Given the roots of two binary trees `p` and `q`, write a function to check if they are the **same** or not.

Two binary trees are considered the same if they are **structurally identical**, and the nodes have the **same value**.

### Examples

**Example 1:**
```
Input:  p = [1,2,3], q = [1,2,3]
Output: true

    1        1
   / \      / \
  2   3    2   3      identical structure and values
```

**Example 2:**
```
Input:  p = [1,2], q = [1,null,2]
Output: false

    1        1
   /          \
  2            2      same values, different structure
```

**Example 3:**
```
Input:  p = [1,2,1], q = [1,1,2]
Output: false

    1        1
   / \      / \
  2   1    1   2      same structure, different values
```

### Constraints
```
The number of nodes in both trees is in the range [0, 100].
-10^4 <= Node.val <= 10^4
```

---

## 🧠 Understanding the problem

Two trees are "the same" when they agree both in **shape** and in **values** at every corresponding position. We walk both trees **in lockstep**: at each step we compare the two current nodes, then recurse into the left pair and the right pair together.

There are exactly three local outcomes at a pair of nodes:
1. Both null → this branch matches (return true).
2. Exactly one null, or values differ → mismatch (return false).
3. Both present and equal → keep comparing children.

That trichotomy is the whole algorithm. It is the foundation for Subtree of Another Tree and Symmetric Tree.

---

## Approach 1 — Recursive lockstep comparison (optimal) ⭐

### Intuition
Compare the two roots; if they match, the trees are the same exactly when their left subtrees match **and** their right subtrees match. Recurse on both pairs simultaneously.

### Algorithm
1. If both `p` and `q` are null → return true (both empty here).
2. If exactly one is null, or `p->val != q->val` → return false.
3. Return `isSameTree(p->left, q->left) && isSameTree(p->right, q->right)`.

### Dry run on `p = [1,2,1]`, `q = [1,1,2]`
```
compare(1,1): equal → recurse children
  compare(2,1): values 2 != 1 → false
  (short-circuit: right pair never evaluated)
→ false   ✓
```

### Code
```cpp
bool isSameTree(TreeNode* p, TreeNode* q) {
    if (!p && !q) return true;
    if (!p || !q || p->val != q->val) return false;
    return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
}
```
```java
public boolean isSameTree(TreeNode p, TreeNode q) {
    if (p == null && q == null) return true;
    if (p == null || q == null || p.val != q.val) return false;
    return isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
}
```
```python
def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Complexity
- **Time**: O(min(n, m)) — comparison stops at the first mismatch; at most touches every node of the smaller tree.
- **Space**: O(min(h_p, h_q)) — recursion stack.

### Verdict
The canonical answer. The three-way base case is clean and the recursion mirrors the data. This is what you present.

---

## Approach 2 — Iterative with paired queue/stack

### Intuition
If recursion is undesirable, push **pairs** of nodes onto a queue (or stack) and compare them as you pop. Enqueue child pairs whenever a node pair matches.

### Algorithm
1. Push `(p, q)` onto a queue.
2. While non-empty, pop `(a, b)`:
   - If both null, continue.
   - If exactly one null or values differ, return false.
   - Push `(a->left, b->left)` and `(a->right, b->right)`.
3. Return true.

### Code
```cpp
bool isSameTree(TreeNode* p, TreeNode* q) {
    queue<pair<TreeNode*, TreeNode*>> que;
    que.push({p, q});
    while (!que.empty()) {
        auto [a, b] = que.front(); que.pop();
        if (!a && !b) continue;
        if (!a || !b || a->val != b->val) return false;
        que.push({a->left,  b->left});
        que.push({a->right, b->right});
    }
    return true;
}
```
```java
public boolean isSameTree(TreeNode p, TreeNode q) {
    Deque<TreeNode[]> que = new ArrayDeque<>();
    que.offer(new TreeNode[]{p, q});
    while (!que.isEmpty()) {
        TreeNode[] pair = que.poll();
        TreeNode a = pair[0], b = pair[1];
        if (a == null && b == null) continue;
        if (a == null || b == null || a.val != b.val) return false;
        que.offer(new TreeNode[]{a.left,  b.left});
        que.offer(new TreeNode[]{a.right, b.right});
    }
    return true;
}
```
```python
from collections import deque

def isSameTree(p, q):
    que = deque([(p, q)])
    while que:
        a, b = que.popleft()
        if not a and not b:
            continue
        if not a or not b or a.val != b.val:
            return False
        que.append((a.left,  b.left))
        que.append((a.right, b.right))
    return True
```

### Complexity
- **Time**: O(min(n, m)).
- **Space**: O(min(n, m)) — the queue can hold a full level of pairs.

### Verdict
Same correctness, avoids recursion. Slightly more verbose; use it when an iterative solution is requested or the tree could be pathologically deep.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive lockstep | O(min(n,m)) | O(h) | cleanest; the default answer ⭐ |
| Iterative paired queue | O(min(n,m)) | O(n) | no recursion; pushes node pairs |

Both stop at the first mismatch. The recursive version is the natural expression; the iterative one is the "no recursion" variant.

---

## 🧪 Edge cases & pitfalls
- **Both empty** → `true`.
- **One empty, one not** → `false` (caught by the "exactly one null" check).
- **Same values, different shape** (Example 2) → `false`; the structural null-mismatch catches it.
- **Pitfall — checking value before null**: you must test the null cases *first*. Dereferencing `p->val` when `p` is null crashes. The ordering `(!p && !q)` then `(!p || !q || val mismatch)` guarantees safety.
- **Pitfall — comparing only values, ignoring structure**: two trees with identical in-order value sequences but different shapes are *not* the same; the lockstep recursion compares positions, not flattened values.

---

## 🔗 Related problems
- **Subtree of Another Tree** (LC 572) — calls Same Tree at every node. See [`06-Subtree-of-Another-Tree.md`](./06-Subtree-of-Another-Tree.md).
- **Symmetric Tree** (LC 101) — compare a tree against its own mirror (cross-compare left/right).
- **Invert Binary Tree** (LC 226) — the mirror operation. See [`01-Invert-Binary-Tree.md`](./01-Invert-Binary-Tree.md).
- **Leaf-Similar Trees** (LC 872) — compare leaf sequences instead of full structure.

---

**→ Next:** [`06-Subtree-of-Another-Tree.md`](./06-Subtree-of-Another-Tree.md) | **← Prev:** [`04-Balanced-Binary-Tree.md`](./04-Balanced-Binary-Tree.md) | Back to [`00-Index.md`](./00-Index.md)
