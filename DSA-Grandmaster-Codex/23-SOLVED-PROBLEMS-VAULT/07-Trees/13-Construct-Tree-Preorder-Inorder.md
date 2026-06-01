# Construct Binary Tree from Preorder and Inorder Traversal

**Platform**: LeetCode 105 · **Difficulty**: Medium · **Topics**: Tree, Array, Hash Table, Divide and Conquer, Binary Tree · **Pattern**: Preorder gives roots, inorder splits subtrees

---

## 📜 Problem Statement

Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return *the binary tree*.

### Examples

**Example 1:**
```
Input:  preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]

        3
       / \
      9  20
        /  \
       15   7
```

**Example 2:**
```
Input:  preorder = [-1], inorder = [-1]
Output: [-1]
```

**Example 3:**
```
Input:  preorder = [1,2], inorder = [2,1]
Output: [1,2,null]

      1
     /
    2
```

### Constraints
```
1 <= preorder.length <= 3000
inorder.length == preorder.length
-3000 <= preorder[i], inorder[i] <= 3000
preorder and inorder consist of unique values.
Each value of inorder also appears in preorder.
preorder and inorder are traversals of the same binary tree.
```

---

## 🧠 Understanding the problem

Two facts unlock the whole problem:

1. **Preorder visits root first.** So `preorder[0]` is the root of the entire tree. The next chunk of preorder is the entire left subtree (in preorder), followed by the entire right subtree (in preorder).
2. **Inorder visits left → root → right.** So once we know the root's value, its position in `inorder` splits the array: everything to the *left* of it is the left subtree's inorder, everything to the *right* is the right subtree's inorder.

Combine them: take the root from the front of preorder, find it in inorder to learn **how many nodes** are in the left subtree, then recurse on the matching slices. A hash map from value → inorder index turns the "find it in inorder" step from O(n) into O(1), giving an overall O(n) build.

---

## Approach 1 — Recursion with linear search for the root (brute force)

### Intuition
Implement the recurrence directly: the first unused preorder element is the current root; scan the current inorder range to find its index, which partitions the range into left and right subtrees.

### Algorithm
1. Maintain a global `preIdx` into `preorder` (advances as roots are consumed).
2. `build(inLo, inHi)`:
   - If `inLo > inHi`, return null.
   - `rootVal = preorder[preIdx++]`; create `root`.
   - Linear scan `inorder[inLo..inHi]` to find `mid` where `inorder[mid] == rootVal`.
   - `root->left = build(inLo, mid-1)`, `root->right = build(mid+1, inHi)`.
3. Return `build(0, n-1)`.

### Code
```cpp
class Solution {
    int preIdx = 0;
    TreeNode* build(vector<int>& pre, vector<int>& in, int inLo, int inHi) {
        if (inLo > inHi) return nullptr;
        int rootVal = pre[preIdx++];
        TreeNode* root = new TreeNode(rootVal);
        int mid = inLo;
        while (in[mid] != rootVal) mid++;          // linear search
        root->left  = build(pre, in, inLo, mid - 1);
        root->right = build(pre, in, mid + 1, inHi);
        return root;
    }
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        preIdx = 0;
        return build(preorder, inorder, 0, inorder.size() - 1);
    }
};
```
```java
class Solution {
    private int preIdx = 0;
    private TreeNode build(int[] pre, int[] in, int inLo, int inHi) {
        if (inLo > inHi) return null;
        int rootVal = pre[preIdx++];
        TreeNode root = new TreeNode(rootVal);
        int mid = inLo;
        while (in[mid] != rootVal) mid++;          // linear search
        root.left  = build(pre, in, inLo, mid - 1);
        root.right = build(pre, in, mid + 1, inHi);
        return root;
    }
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        preIdx = 0;
        return build(preorder, inorder, 0, inorder.length - 1);
    }
}
```
```python
def buildTree(preorder, inorder):
    pre_idx = 0
    def build(in_lo, in_hi):
        nonlocal pre_idx
        if in_lo > in_hi:
            return None
        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)
        mid = in_lo
        while inorder[mid] != root_val:   # linear search
            mid += 1
        root.left  = build(in_lo, mid - 1)
        root.right = build(mid + 1, in_hi)
        return root
    return build(0, len(inorder) - 1)
```

### Complexity
- **Time**: O(n²) — the linear search for the root inside each recursive call; degenerates to quadratic on a skewed tree.
- **Space**: O(h) recursion (plus O(n) worst case).

### Verdict
Correct and demonstrates the recurrence, but the repeated linear search is the bottleneck. Replace it with a hash map for O(1) lookups.

---

## Approach 2 — Hash map of inorder indices (optimal) ⭐

### Intuition
The only slow step is "find the root in inorder." Precompute a map `value → index in inorder` once. Then each root lookup is O(1), and the whole construction becomes O(n).

### Algorithm
1. Build `pos[value] = index` from `inorder`.
2. Global `preIdx = 0`.
3. `build(inLo, inHi)`:
   - If `inLo > inHi`, return null.
   - `rootVal = preorder[preIdx++]`; create `root`.
   - `mid = pos[rootVal]` (O(1)).
   - `root->left = build(inLo, mid-1)`, `root->right = build(mid+1, inHi)`.
4. Return `build(0, n-1)`.

### Dry run on `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`
```
pos = {9:0, 3:1, 15:2, 20:3, 7:4}
build(0,4): root=pre[0]=3, mid=pos[3]=1
   left = build(0,0):  root=pre[1]=9, mid=0 → left build(0,-1)=null, right build(1,0)=null → node 9
   right= build(2,4):  root=pre[2]=20, mid=pos[20]=3
        left = build(2,2): root=pre[3]=15 → leaf
        right= build(4,4): root=pre[4]=7  → leaf
result:
        3
       / \
      9  20
        /  \
       15   7        ✓
```

### Code
```cpp
class Solution {
    unordered_map<int,int> pos;
    int preIdx = 0;
    TreeNode* build(vector<int>& pre, int inLo, int inHi) {
        if (inLo > inHi) return nullptr;
        int rootVal = pre[preIdx++];
        TreeNode* root = new TreeNode(rootVal);
        int mid = pos[rootVal];
        root->left  = build(pre, inLo, mid - 1);
        root->right = build(pre, mid + 1, inHi);
        return root;
    }
public:
    TreeNode* buildTree(vector<int>& preorder, vector<int>& inorder) {
        pos.clear();
        for (int i = 0; i < (int)inorder.size(); i++) pos[inorder[i]] = i;
        preIdx = 0;
        return build(preorder, 0, inorder.size() - 1);
    }
};
```
```java
class Solution {
    private Map<Integer,Integer> pos = new HashMap<>();
    private int preIdx = 0;
    private TreeNode build(int[] pre, int inLo, int inHi) {
        if (inLo > inHi) return null;
        int rootVal = pre[preIdx++];
        TreeNode root = new TreeNode(rootVal);
        int mid = pos.get(rootVal);
        root.left  = build(pre, inLo, mid - 1);
        root.right = build(pre, mid + 1, inHi);
        return root;
    }
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        pos.clear();
        for (int i = 0; i < inorder.length; i++) pos.put(inorder[i], i);
        preIdx = 0;
        return build(preorder, 0, inorder.length - 1);
    }
}
```
```python
def buildTree(preorder, inorder):
    pos = {v: i for i, v in enumerate(inorder)}
    pre_idx = 0
    def build(in_lo, in_hi):
        nonlocal pre_idx
        if in_lo > in_hi:
            return None
        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)
        mid = pos[root_val]
        root.left  = build(in_lo, mid - 1)
        root.right = build(mid + 1, in_hi)
        return root
    return build(0, len(inorder) - 1)
```

### Complexity
- **Time**: O(n) — each node created once; O(1) root lookups.
- **Space**: O(n) — the hash map plus O(h) recursion.

### Verdict
The standard optimal answer. The hash map is the difference between O(n²) and O(n). Make sure the global `preIdx` advances exactly once per node and that left is built before right (preorder order).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Linear search per root | O(n²) | O(h) | direct recurrence; slow lookups |
| Hash map of indices | **O(n)** | O(n) | O(1) root location; the default ⭐ |

The recurrence is identical; only the root-location step differs. Always reach for the hash map.

---

## 🧪 Edge cases & pitfalls
- **Single node** → `preorder = inorder = [x]`; builds one node.
- **Left-skewed / right-skewed trees** → recursion depth O(n); fine within constraints (n ≤ 3000).
- **Pitfall — building right before left**: preorder is root → **left** → right, so after consuming the root you must build the *left* subtree first (it consumes the next preorder elements). Swapping the order corrupts the tree.
- **Pitfall — advancing `preIdx` incorrectly**: increment it exactly once when creating each node; an off-by-one desynchronizes preorder from the inorder split.
- **Pitfall — duplicate values**: the algorithm relies on unique values to locate the root in inorder. Duplicates make the split ambiguous (the constraints guarantee uniqueness).
- **Related — preorder + postorder** alone is *not* enough to reconstruct a unique tree (ambiguous for single-child nodes); inorder is what disambiguates.

---

## 🔗 Related problems
- **Construct Binary Tree from Inorder and Postorder** (LC 106) — postorder's *last* element is the root; consume from the back.
- **Construct Binary Tree from Preorder and Postorder** (LC 889) — returns *a* valid tree (not unique).
- **Serialize and Deserialize Binary Tree** (LC 297) — preorder + null markers fully encodes structure. See [`15-Serialize-Deserialize-Binary-Tree.md`](./15-Serialize-Deserialize-Binary-Tree.md).
- **Convert Sorted Array to BST** (LC 108) — middle element as root, recurse on halves.

---

**→ Next:** [`14-Binary-Tree-Maximum-Path-Sum.md`](./14-Binary-Tree-Maximum-Path-Sum.md) | **← Prev:** [`12-Kth-Smallest-in-BST.md`](./12-Kth-Smallest-in-BST.md) | Back to [`00-Index.md`](./00-Index.md)
