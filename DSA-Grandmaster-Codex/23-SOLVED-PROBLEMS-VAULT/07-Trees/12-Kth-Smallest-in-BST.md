# Kth Smallest Element in a BST

**Platform**: LeetCode 230 · **Difficulty**: Medium · **Topics**: Tree, DFS, BST, Binary Tree · **Pattern**: In-order traversal yields sorted order

---

## 📜 Problem Statement

Given the `root` of a binary search tree, and an integer `k`, return *the* `kth` *smallest value (**1-indexed**) of all the values of the nodes in the tree*.

### Examples

**Example 1:**
```
Input:  root = [3,1,4,null,2], k = 1
Output: 1

        3
       / \
      1   4
       \
        2
In-order (sorted): 1, 2, 3, 4 → 1st smallest = 1
```

**Example 2:**
```
Input:  root = [5,3,6,2,4,null,null,1], k = 3
Output: 3

            5
           / \
          3   6
         / \
        2   4
       /
      1
In-order (sorted): 1, 2, 3, 4, 5, 6 → 3rd smallest = 3
```

**Example 3:**
```
Input:  root = [1], k = 1
Output: 1
```

### Constraints
```
The number of nodes in the tree is n.
1 <= k <= n <= 10^4
0 <= Node.val <= 10^4
```

**Follow-up:** If the BST is modified often (insert/delete) and you need to find the kth smallest frequently, how would you optimize?

---

## 🧠 Understanding the problem

The single fact that cracks this problem: **an in-order traversal of a BST visits its values in strictly increasing order.** Left subtree → node → right subtree, applied recursively, emits the sorted sequence.

So the kth smallest is simply the kth value produced by an in-order walk. We don't need to traverse the entire tree — we can **stop as soon as we have emitted k values**. That early stop is what separates the optimal solution from a naive "flatten then index."

---

## Approach 1 — In-order to a list, index k-1 (brute-ish)

### Intuition
Produce the full sorted sequence with a recursive in-order traversal, store it in a list, then return the element at index `k-1`.

### Algorithm
1. In-order traverse, appending each value to `vals`.
2. Return `vals[k-1]`.

### Code
```cpp
class Solution {
    void inorder(TreeNode* node, vector<int>& vals) {
        if (!node) return;
        inorder(node->left, vals);
        vals.push_back(node->val);
        inorder(node->right, vals);
    }
public:
    int kthSmallest(TreeNode* root, int k) {
        vector<int> vals;
        inorder(root, vals);
        return vals[k - 1];
    }
};
```
```java
class Solution {
    private void inorder(TreeNode node, List<Integer> vals) {
        if (node == null) return;
        inorder(node.left, vals);
        vals.add(node.val);
        inorder(node.right, vals);
    }
    public int kthSmallest(TreeNode root, int k) {
        List<Integer> vals = new ArrayList<>();
        inorder(root, vals);
        return vals.get(k - 1);
    }
}
```
```python
def kthSmallest(root, k):
    vals = []
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        vals.append(node.val)
        inorder(node.right)
    inorder(root)
    return vals[k - 1]
```

### Complexity
- **Time**: O(n) — traverses the whole tree even when `k` is small.
- **Space**: O(n) — the list plus O(h) recursion.

### Verdict
Correct and simple, but it always visits all `n` nodes and stores them. Fine when `k` is near `n`; wasteful when `k` is tiny. We can stop early.

---

## Approach 2 — Iterative in-order with early stop (optimal) ⭐

### Intuition
Do an iterative in-order traversal using a stack, decrementing `k` each time we *visit* a node. The moment `k` hits `0`, the node we just visited is the answer — return immediately without touching the rest of the tree.

### Algorithm
1. `stack`, `cur = root`.
2. Loop while `cur` or stack non-empty:
   - Push all left descendants: while `cur`, push `cur`, `cur = cur->left`.
   - Pop `cur` (smallest unvisited).
   - Decrement `k`; if `k == 0`, return `cur->val`.
   - Move `cur = cur->right`.

### Dry run on `[5,3,6,2,4,null,null,1], k = 3`
```
push 5,3,2,1 (all lefts); pop 1 → k=2; go right(null)
pop 2 → k=1; right(null)
pop 3 → k=0 → return 3   ✓  (stops before visiting 4,5,6)
```

### Code
```cpp
int kthSmallest(TreeNode* root, int k) {
    stack<TreeNode*> st;
    TreeNode* cur = root;
    while (cur || !st.empty()) {
        while (cur) { st.push(cur); cur = cur->left; }
        cur = st.top(); st.pop();
        if (--k == 0) return cur->val;
        cur = cur->right;
    }
    return -1;  // unreachable given valid k
}
```
```java
public int kthSmallest(TreeNode root, int k) {
    Deque<TreeNode> st = new ArrayDeque<>();
    TreeNode cur = root;
    while (cur != null || !st.isEmpty()) {
        while (cur != null) { st.push(cur); cur = cur.left; }
        cur = st.pop();
        if (--k == 0) return cur.val;
        cur = cur.right;
    }
    return -1;  // unreachable given valid k
}
```
```python
def kthSmallest(root, k):
    st = []
    cur = root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.left
        cur = st.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
    return -1  # unreachable given valid k
```

### Complexity
- **Time**: O(h + k) — descend to the smallest (O(h)) then pop `k` nodes. Far better than O(n) when `k` is small.
- **Space**: O(h) — the stack holds at most one root-to-leftmost path.

### Verdict
The optimal answer. Early termination makes it O(h + k) instead of O(n). The iterative in-order with a stack is a pattern worth memorizing cold.

---

## Approach 3 — Augmented BST (follow-up: frequent queries with updates)

### Intuition
If the tree changes often and kth-smallest is queried repeatedly, store in each node the **size of its left subtree** (count of nodes). Then locating the kth smallest is an O(h) descent: compare `k` to `leftCount + 1` to decide whether the answer is in the left subtree, is the current node, or is the `(k - leftCount - 1)`th in the right subtree. Inserts/deletes update counts along the path in O(h).

### Algorithm (query, assuming `size` of left subtree stored)
1. At `node`, let `L = size(node->left)`.
2. If `k <= L` → recurse left.
3. If `k == L + 1` → return `node->val`.
4. Else → recurse right with `k - L - 1`.

### Code
```cpp
// Node augmented with leftCount = number of nodes in its left subtree.
struct CountNode { int val, leftCount; CountNode *left, *right; };

int kthSmallest(CountNode* root, int k) {
    CountNode* node = root;
    while (node) {
        int L = node->leftCount;
        if (k <= L)        node = node->left;
        else if (k == L+1) return node->val;
        else { k -= (L + 1); node = node->right; }
    }
    return -1;
}
```
```java
// Node augmented with leftCount = number of nodes in its left subtree.
class CountNode { int val, leftCount; CountNode left, right; }

int kthSmallest(CountNode root, int k) {
    CountNode node = root;
    while (node != null) {
        int L = node.leftCount;
        if (k <= L)            node = node.left;
        else if (k == L + 1)   return node.val;
        else { k -= (L + 1);   node = node.right; }
    }
    return -1;
}
```
```python
# Node augmented with left_count = number of nodes in its left subtree.
class CountNode:
    def __init__(self, val=0):
        self.val = val
        self.left_count = 0
        self.left = None
        self.right = None

def kthSmallest(root, k):
    node = root
    while node:
        L = node.left_count
        if k <= L:
            node = node.left
        elif k == L + 1:
            return node.val
        else:
            k -= (L + 1)
            node = node.right
    return -1
```

### Complexity
- **Time**: O(h) per query (and per insert/delete to maintain counts).
- **Space**: O(1) extra per query (one integer field per node).

### Verdict
The follow-up answer. When updates and queries interleave, the subtree-size augmentation turns each kth-smallest query into a logarithmic descent on a balanced tree. Mention this when the interviewer asks "what if the tree changes a lot?"

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| In-order to list | O(n) | O(n) | simplest; visits all nodes |
| Iterative in-order early stop | **O(h + k)** | O(h) | stop at the kth; the default ⭐ |
| Augmented BST (size field) | O(h)/query | O(1) extra | best for repeated queries + updates |

For a one-off query, the early-stop in-order is the go-to. For a dynamic tree with many queries, augment with subtree sizes.

---

## 🧪 Edge cases & pitfalls
- **k = 1** → the leftmost (smallest) node.
- **k = n** → the rightmost (largest) node; in-order visits everything.
- **Single node, k = 1** → that node's value.
- **Pitfall — 1-indexed vs 0-indexed**: `k` is 1-based. With a list it's `vals[k-1]`; with the counter, return when `--k == 0`.
- **Pitfall — recursing without early exit**: a recursive in-order that ignores `k` wastes work when `k` is small. The iterative version (or a recursive one with a mutable counter and short-circuit) gives O(h + k).
- **Pitfall (augmented) — forgetting to maintain counts on update**: stale `leftCount` after an insert/delete corrupts queries; update along the entire insertion/deletion path.

---

## 🔗 Related problems
- **Validate Binary Search Tree** (LC 98) — same in-order-is-sorted insight. See [`11-Validate-BST.md`](./11-Validate-BST.md).
- **Kth Largest Element in a Stream** (LC 703) — heap-based order statistic.
- **Binary Search Tree Iterator** (LC 173) — the iterative in-order packaged as an iterator.
- **Convert BST to Greater Tree** (LC 538) — reverse in-order accumulation.

---

**→ Next:** [`13-Construct-Tree-Preorder-Inorder.md`](./13-Construct-Tree-Preorder-Inorder.md) | **← Prev:** [`11-Validate-BST.md`](./11-Validate-BST.md) | Back to [`00-Index.md`](./00-Index.md)
