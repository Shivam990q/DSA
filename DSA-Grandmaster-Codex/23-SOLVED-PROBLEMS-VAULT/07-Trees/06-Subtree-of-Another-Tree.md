# Subtree of Another Tree

**Platform**: LeetCode 572 · **Difficulty**: Easy · **Topics**: Tree, DFS, String Matching, Hashing, Binary Tree · **Pattern**: Per-node Same-Tree probe (+ serialization trick)

---

## 📜 Problem Statement

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the **same structure and node values** as `subRoot` and `false` otherwise.

A subtree of a binary tree `tree` is a tree that consists of a node in `tree` and **all of this node's descendants**. The tree `tree` could also be considered as a subtree of itself.

### Examples

**Example 1:**
```
Input:  root = [3,4,5,1,2], subRoot = [4,1,2]
Output: true

      3            4
     / \          / \
    4   5        1   2
   / \
  1   2          subRoot matches the subtree rooted at node 4
```

**Example 2:**
```
Input:  root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
Output: false

      3
     / \
    4   5
   / \
  1   2
       \
        0       the subtree at node 4 has an extra node 0 → not identical
```

**Example 3:**
```
Input:  root = [1,1], subRoot = [1]
Output: true
Explanation: The single-node subtree [1] appears as the left child.
```

### Constraints
```
The number of nodes in the root tree is in the range [1, 2000].
The number of nodes in the subRoot tree is in the range [1, 1000].
-10^4 <= root.val, subRoot.val <= 10^4
```

---

## 🧠 Understanding the problem

We must find a node in `root` such that the **entire** subtree hanging off it is identical (shape + values) to `subRoot`. "Entire" is the catch: a partial match where `subRoot` lines up with the *top* of a larger subtree does not count — every descendant must match too (that is exactly why Example 2 fails: the extra node `0`).

So the problem decomposes into two pieces we already know:
1. **"Are these two trees identical?"** — that is Same Tree (LC 100).
2. **"Try that identity check at every candidate node of `root`."**

Combine them and we have the answer. The clever alternative is to serialize both trees to strings and ask whether `subRoot`'s string is a substring of `root`'s string — turning a tree problem into string matching.

---

## Approach 1 — Same-Tree probe at every node (optimal-enough) ⭐

### Intuition
Walk `root`. At each node, ask "does the subtree rooted here equal `subRoot`?" using the lockstep Same-Tree comparison. If any node says yes, we are done; otherwise recurse into children.

### Algorithm
1. `isSame(a, b)`: standard Same-Tree (both null → true; one null or value mismatch → false; else compare children).
2. `isSubtree(root, subRoot)`:
   - If `subRoot` is null → true (empty matches anywhere).
   - If `root` is null → false (non-empty `subRoot` can't match nothing).
   - If `isSame(root, subRoot)` → true.
   - Else return `isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot)`.

### Dry run on `root = [3,4,5,1,2]`, `subRoot = [4,1,2]`
```
isSubtree(3,...): isSame(3-tree, 4-tree)? root vals 3 != 4 → false
  isSubtree(4,...): isSame(4-tree, subRoot)?
      4==4 → compare children: (1,1) ok, (2,2) ok → true
  → true   ✓
```

### Code
```cpp
class Solution {
    bool isSame(TreeNode* a, TreeNode* b) {
        if (!a && !b) return true;
        if (!a || !b || a->val != b->val) return false;
        return isSame(a->left, b->left) && isSame(a->right, b->right);
    }
public:
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        if (!subRoot) return true;
        if (!root) return false;
        if (isSame(root, subRoot)) return true;
        return isSubtree(root->left, subRoot) || isSubtree(root->right, subRoot);
    }
};
```
```java
class Solution {
    private boolean isSame(TreeNode a, TreeNode b) {
        if (a == null && b == null) return true;
        if (a == null || b == null || a.val != b.val) return false;
        return isSame(a.left, b.left) && isSame(a.right, b.right);
    }
    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        if (subRoot == null) return true;
        if (root == null) return false;
        if (isSame(root, subRoot)) return true;
        return isSubtree(root.left, subRoot) || isSubtree(root.right, subRoot);
    }
}
```
```python
def isSubtree(root, subRoot):
    def isSame(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return isSame(a.left, b.left) and isSame(a.right, b.right)

    if not subRoot:
        return True
    if not root:
        return False
    if isSame(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)
```

### Complexity
- **Time**: O(n · m) worst case — for each of `n` nodes in `root` we may run an O(m) comparison.
- **Space**: O(h) — recursion depth of `root` plus the comparison stack.

### Verdict
The standard interview answer. Easy to reason about, reuses Same Tree, and well within limits for n, m ≤ 2000/1000.

---

## Approach 2 — Serialization + substring search

### Intuition
Serialize each tree to a string with explicit null markers and value delimiters. Then `subRoot` is a subtree of `root` **iff** the serialized `subRoot` is a substring of the serialized `root`. Delimiters prevent false matches (e.g., value `12` vs `2`).

### Algorithm
1. Serialize with a leading delimiter per node and explicit `#` for nulls, e.g. `^val` so partial numeric overlaps can't fake a match.
2. Build `s = serialize(root)` and `t = serialize(subRoot)`.
3. Return whether `t` is a substring of `s` (`string::find` / `String.contains` / `in`).

### Dry run on `root = [1,2,3]`, `subRoot = [2]` (leaf with two null kids)
```
serialize(subRoot) = "^2^#^#"
serialize(root)    = "^1^2^#^#^3^#^#"
"^2^#^#" is a substring of "^1^2^#^#^3^#^#" → true
(the leading ^ guards against value-prefix collisions like 2 vs 12)
```

### Code
```cpp
class Solution {
    void serialize(TreeNode* node, string& s) {
        if (!node) { s += "^#"; return; }
        s += "^" + to_string(node->val);
        serialize(node->left, s);
        serialize(node->right, s);
    }
public:
    bool isSubtree(TreeNode* root, TreeNode* subRoot) {
        string s, t;
        serialize(root, s);
        serialize(subRoot, t);
        return s.find(t) != string::npos;
    }
};
```
```java
class Solution {
    private void serialize(TreeNode node, StringBuilder sb) {
        if (node == null) { sb.append("^#"); return; }
        sb.append("^").append(node.val);
        serialize(node.left, sb);
        serialize(node.right, sb);
    }
    public boolean isSubtree(TreeNode root, TreeNode subRoot) {
        StringBuilder s = new StringBuilder(), t = new StringBuilder();
        serialize(root, s);
        serialize(subRoot, t);
        return s.toString().contains(t.toString());
    }
}
```
```python
def isSubtree(root, subRoot):
    def serialize(node):
        if not node:
            return "^#"
        return "^" + str(node.val) + serialize(node.left) + serialize(node.right)

    return serialize(subRoot) in serialize(root)
```

### Complexity
- **Time**: O(n + m) to serialize, plus substring search — O(n + m) with KMP, or O(n · m) worst case with naive `find`/`contains`/`in` (in practice fast).
- **Space**: O(n + m) for the two strings.

### Verdict
A slick reframing that demonstrates breadth. With a KMP substring search it is linear; with the built-in finder it is usually fast but not worst-case linear. Great "can you do better?" follow-up.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Same-Tree at every node | O(n·m) | O(h) | simplest, the default answer ⭐ |
| Serialize + substring | O(n+m)* | O(n+m) | string-matching reframe; linear with KMP |

\* Linear only when paired with a linear substring algorithm (KMP/Z); the naive built-in search is O(n·m) worst case.

The first approach is what most interviewers expect. Mention serialization as the optimization, and KMP as the way to make it truly linear.

---

## 🧪 Edge cases & pitfalls
- **`subRoot` is a single node** → matches anywhere that exact leaf-value-with-null-children pattern appears.
- **`subRoot` larger than `root`** → can never match; recursion naturally returns false.
- **Pitfall — partial match at the top**: matching `subRoot` against just the upper part of a bigger subtree is wrong. Same Tree enforces full equality including the null leaves, which rejects Example 2.
- **Pitfall (serialization) — missing delimiters**: without per-node markers, values like `2` and `22`, or two trees `[12]` and `[2]`, can produce spurious substring hits. Always include both null markers and a value separator.
- **Pitfall — value-prefix collisions**: serialize with a leading symbol before each value (here `^`) so `12` cannot match inside `112`.

---

## 🔗 Related problems
- **Same Tree** (LC 100) — the equality check this builds on. See [`05-Same-Tree.md`](./05-Same-Tree.md).
- **Serialize and Deserialize Binary Tree** (LC 297) — the serialization machinery. See [`15-Serialize-Deserialize-Binary-Tree.md`](./15-Serialize-Deserialize-Binary-Tree.md).
- **Implement strStr()** (LC 28) — the substring search (KMP) used in Approach 2.
- **Find Duplicate Subtrees** (LC 652) — serialize subtrees and hash to find repeats.

---

**→ Next:** [`07-Lowest-Common-Ancestor-BST.md`](./07-Lowest-Common-Ancestor-BST.md) | **← Prev:** [`05-Same-Tree.md`](./05-Same-Tree.md) | Back to [`00-Index.md`](./00-Index.md)
