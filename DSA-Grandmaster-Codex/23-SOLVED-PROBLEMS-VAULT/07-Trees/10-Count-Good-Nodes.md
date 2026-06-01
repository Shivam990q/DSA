# Count Good Nodes in Binary Tree

**Platform**: LeetCode 1448 · **Difficulty**: Medium · **Topics**: Tree, DFS, BFS, Binary Tree · **Pattern**: DFS carrying context (path maximum) downward

---

## 📜 Problem Statement

Given a binary tree `root`, a node *X* in the tree is named **good** if in the path from root to *X* there are no nodes with a value **greater than** *X*.

Return the number of **good** nodes in the binary tree.

### Examples

**Example 1:**
```
Input:  root = [3,1,4,3,null,1,5]
Output: 4

           3                3 is good (root is always good)
          / \
         1   4              4 is good (path max before it is 3 ≤ 4)
        /   / \
       3   1   5            3 is good (3,1,3: max so far 3 ≤ 3)
                            5 is good (3,4,5: max 4 ≤ 5)
                            1 (under 4) is NOT good (4 > 1)
Good nodes: 3, 4, 3, 5 → 4
```

**Example 2:**
```
Input:  root = [3,3,null,4,2]
Output: 3

        3
       /
      3            good (3 ≤ 3)
     / \
    4   2          4 good (3,3,4 → 4 ≥ max 3);  2 NOT good (max 3 > 2)
Good nodes: 3, 3, 4 → 3
```

**Example 3:**
```
Input:  root = [1]
Output: 1
Explanation: The root is always a good node.
```

### Constraints
```
The number of nodes in the binary tree is in the range [1, 10^5].
Each node's value is between [-10^4, 10^4].
```

---

## 🧠 Understanding the problem

A node is "good" when **no ancestor on its root-to-node path has a strictly larger value** — equivalently, the node's value is `>=` the maximum value seen along the path from the root to it (inclusive of nothing above, but compared against ancestors). The root is always good (nothing precedes it).

This is the **"carry context downward"** flavor of tree DFS, the complement of the "bubble values up" flavor. As we descend, we thread along a single piece of state: the **maximum value seen so far** on the current path. At each node, compare its value to that running max to decide goodness, then pass the updated max to its children. Counting is a simple sum over the subtree.

---

## Approach 1 — DFS carrying path maximum (optimal) ⭐

### Intuition
Walk down from the root tracking `maxSoFar`. A node is good iff `node->val >= maxSoFar`. Before recursing into children, update `maxSoFar = max(maxSoFar, node->val)` so descendants compare against the true path maximum. Sum the good counts from both subtrees.

### Algorithm
1. `dfs(node, maxSoFar)`:
   - If `node` is null, return `0`.
   - `good = (node->val >= maxSoFar) ? 1 : 0`.
   - `m = max(maxSoFar, node->val)`.
   - Return `good + dfs(left, m) + dfs(right, m)`.
2. Call `dfs(root, INT_MIN)` so the root always counts.

### Dry run on `[3,1,4,3,null,1,5]`
```
dfs(3, -inf): 3>=-inf → good(1); m=3
  dfs(1, 3): 1>=3? no → 0; m=3
    dfs(3, 3): 3>=3 → good(1); m=3 → +0+0 = 1
  dfs(4, 3): 4>=3 → good(1); m=4
    dfs(1, 4): 1>=4? no → 0
    dfs(5, 4): 5>=4 → good(1) → 1
total = 1(root) + (1) + (1 + 0 + 1) = 4   ✓
```

### Code
```cpp
class Solution {
    int dfs(TreeNode* node, int maxSoFar) {
        if (!node) return 0;
        int good = (node->val >= maxSoFar) ? 1 : 0;
        int m = max(maxSoFar, node->val);
        return good + dfs(node->left, m) + dfs(node->right, m);
    }
public:
    int goodNodes(TreeNode* root) {
        return dfs(root, INT_MIN);
    }
};
```
```java
class Solution {
    private int dfs(TreeNode node, int maxSoFar) {
        if (node == null) return 0;
        int good = (node.val >= maxSoFar) ? 1 : 0;
        int m = Math.max(maxSoFar, node.val);
        return good + dfs(node.left, m) + dfs(node.right, m);
    }
    public int goodNodes(TreeNode root) {
        return dfs(root, Integer.MIN_VALUE);
    }
}
```
```python
def goodNodes(root):
    def dfs(node, max_so_far):
        if not node:
            return 0
        good = 1 if node.val >= max_so_far else 0
        m = max(max_so_far, node.val)
        return good + dfs(node.left, m) + dfs(node.right, m)
    return dfs(root, float('-inf'))
```

### Complexity
- **Time**: O(n) — every node visited once.
- **Space**: O(h) — recursion stack.

### Verdict
The canonical answer. It is the textbook example of threading **downward context** (the path max) instead of returning upward. Clean, single pass, optimal.

---

## Approach 2 — Iterative DFS with explicit (node, max) stack

### Intuition
Same logic without recursion: push pairs of `(node, maxSoFar)` onto a stack. Pop, test goodness, push children with the updated max. Use an explicit counter.

### Algorithm
1. If root is null, return `0`.
2. Push `(root, INT_MIN)`; set `count = 0`.
3. While the stack is non-empty, pop `(node, m)`:
   - If `node->val >= m`, increment `count`.
   - `nm = max(m, node->val)`.
   - Push non-null children with `nm`.
4. Return `count`.

### Code
```cpp
int goodNodes(TreeNode* root) {
    if (!root) return 0;
    stack<pair<TreeNode*,int>> st;
    st.push({root, INT_MIN});
    int count = 0;
    while (!st.empty()) {
        auto [node, m] = st.top(); st.pop();
        if (node->val >= m) count++;
        int nm = max(m, node->val);
        if (node->left)  st.push({node->left,  nm});
        if (node->right) st.push({node->right, nm});
    }
    return count;
}
```
```java
public int goodNodes(TreeNode root) {
    if (root == null) return 0;
    Deque<Object[]> st = new ArrayDeque<>();
    st.push(new Object[]{root, Integer.MIN_VALUE});
    int count = 0;
    while (!st.isEmpty()) {
        Object[] top = st.pop();
        TreeNode node = (TreeNode) top[0];
        int m = (int) top[1];
        if (node.val >= m) count++;
        int nm = Math.max(m, node.val);
        if (node.left  != null) st.push(new Object[]{node.left,  nm});
        if (node.right != null) st.push(new Object[]{node.right, nm});
    }
    return count;
}
```
```python
def goodNodes(root):
    if not root:
        return 0
    st = [(root, float('-inf'))]
    count = 0
    while st:
        node, m = st.pop()
        if node.val >= m:
            count += 1
        nm = max(m, node.val)
        if node.left:  st.append((node.left,  nm))
        if node.right: st.append((node.right, nm))
    return count
```

### Complexity
- **Time**: O(n).
- **Space**: O(h) — stack holds a root-to-node path plus pending siblings.

### Verdict
Functionally identical, avoids the call stack. Use it if recursion depth is a concern (a 10⁵-node skewed tree could be deep). Otherwise the recursive form reads better.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive DFS + path max | O(n) | O(h) | cleanest; the default answer ⭐ |
| Iterative DFS + stack | O(n) | O(h) | no recursion; carries `(node, max)` |

Both carry the running path maximum downward. The difference is only recursion vs explicit stack.

---

## 🧪 Edge cases & pitfalls
- **Root only** → `1` (root is always good).
- **All increasing path** → every node good → count `= n`.
- **All decreasing path** → only the root is good → count `= 1`.
- **Equal values along the path** → ties count as good (`>=`, not `>`); the problem says "no node *greater than*," so equal ancestors are fine. See Example 2's two `3`s.
- **Pitfall — using `>` instead of `>=`**: a node equal to the running max is still good. Strict `>` would undercount.
- **Pitfall — initial max too high**: seed with `INT_MIN` / `-inf` so the root (and any negative-valued tree) is counted. Seeding with `0` breaks trees with negative values.

---

## 🔗 Related problems
- **Validate Binary Search Tree** (LC 98) — also threads bounds downward. See [`11-Validate-BST.md`](./11-Validate-BST.md).
- **Path Sum** (LC 112) / **Path Sum II** (LC 113) — carry the remaining target downward.
- **Sum Root to Leaf Numbers** (LC 129) — accumulate a value along the path.
- **Maximum Depth** (LC 104) — the simplest downward/upward DFS. See [`02-Maximum-Depth.md`](./02-Maximum-Depth.md).

---

**→ Next:** [`11-Validate-BST.md`](./11-Validate-BST.md) | **← Prev:** [`09-Binary-Tree-Right-Side-View.md`](./09-Binary-Tree-Right-Side-View.md) | Back to [`00-Index.md`](./00-Index.md)
