# Serialize and Deserialize Binary Tree

**Platform**: LeetCode 297 · **Difficulty**: Hard · **Topics**: Tree, DFS, BFS, Design, String, Binary Tree · **Pattern**: Preorder encoding with explicit null markers

---

## 📜 Problem Statement

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

### Examples

**Example 1:**
```
Input:  root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]

      1
     / \
    2   3
       / \
      4   5

serialize  → "1,2,#,#,3,4,#,#,5,#,#"   (preorder with # for null)
deserialize→ rebuilds the identical tree
```

**Example 2:**
```
Input:  root = []
Output: []
Explanation: The empty tree serializes to "#" and back to null.
```

**Example 3:**
```
Input:  root = [1,2]
Output: [1,2]

      1
     /
    2
```

### Constraints
```
The number of nodes in the tree is in the range [0, 10^4].
-1000 <= Node.val <= 1000
```

---

## 🧠 Understanding the problem

We need a **lossless round trip**: `deserialize(serialize(tree))` must reproduce the original tree exactly — same structure, same values. A plain list of values is *not* enough, because many different trees share the same value multiset (and even the same in-order or pre-order alone is ambiguous about shape).

The fix is to record **null children explicitly**. A preorder DFS that emits each node's value, then recursively serializes its left and right child — writing a sentinel (e.g. `#`) for null — captures the full shape unambiguously. Deserialization consumes the tokens in the *same* preorder order: read a token; if it is `#`, the subtree is null; otherwise build a node and recursively read its left then right child. The null markers tell the rebuilder exactly where each subtree ends.

BFS (level-order with null markers) is an equally valid encoding; the two just differ in token order.

---

## Approach 1 — Preorder DFS with null markers (optimal) ⭐

### Intuition
Preorder (root, left, right) plus a `#` for every null is a complete blueprint. Because we write nulls, there is never ambiguity about where a subtree stops, so the same recursion that wrote the string can rebuild the tree by reading tokens in order.

### Algorithm
**Serialize**
1. DFS(node): if null, append `#`; else append `node->val`, then DFS(left), DFS(right).
2. Join tokens with a delimiter (comma).

**Deserialize**
1. Split the string into tokens; keep a moving index/iterator.
2. DFS(): read the next token. If `#`, return null. Else create a node with that value, set `node->left = DFS()`, `node->right = DFS()`, return node.

### Dry run on `[1,2,3,null,null,4,5]`
```
serialize:
  1 → "1"
    left 2 → "2", its children null,null → "#","#"
    right 3 → "3"
      left 4 → "4","#","#"
      right 5 → "5","#","#"
  → "1,2,#,#,3,4,#,#,5,#,#"

deserialize "1,2,#,#,3,4,#,#,5,#,#":
  read 1 → node(1)
    left: read 2 → node(2); left read # → null; right read # → null
    right: read 3 → node(3)
      left: read 4 → node(4), #, # → leaf
      right: read 5 → node(5), #, # → leaf
  → identical tree   ✓
```

### Code
```cpp
class Codec {
    void ser(TreeNode* node, string& s) {
        if (!node) { s += "#,"; return; }
        s += to_string(node->val) + ",";
        ser(node->left, s);
        ser(node->right, s);
    }
    TreeNode* des(int& i, vector<string>& t) {
        if (t[i] == "#") { i++; return nullptr; }
        TreeNode* node = new TreeNode(stoi(t[i++]));
        node->left  = des(i, t);
        node->right = des(i, t);
        return node;
    }
public:
    string serialize(TreeNode* root) {
        string s;
        ser(root, s);
        return s;
    }
    TreeNode* deserialize(string data) {
        vector<string> t;
        string cur;
        for (char c : data) {
            if (c == ',') { t.push_back(cur); cur.clear(); }
            else cur += c;
        }
        int i = 0;
        return des(i, t);
    }
};
```
```java
public class Codec {
    private void ser(TreeNode node, StringBuilder sb) {
        if (node == null) { sb.append("#,"); return; }
        sb.append(node.val).append(",");
        ser(node.left, sb);
        ser(node.right, sb);
    }
    public String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        ser(root, sb);
        return sb.toString();
    }
    private TreeNode des(String[] t, int[] i) {
        if (t[i[0]].equals("#")) { i[0]++; return null; }
        TreeNode node = new TreeNode(Integer.parseInt(t[i[0]++]));
        node.left  = des(t, i);
        node.right = des(t, i);
        return node;
    }
    public TreeNode deserialize(String data) {
        String[] t = data.split(",");
        return des(t, new int[]{0});
    }
}
```
```python
class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):
            if not node:
                out.append("#")
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data):
        tokens = iter(data.split(","))
        def dfs():
            v = next(tokens)
            if v == "#":
                return None
            node = TreeNode(int(v))
            node.left  = dfs()
            node.right = dfs()
            return node
        return dfs()
```

### Complexity
- **Time**: O(n) — serialize and deserialize each touch every node (and each null marker) once.
- **Space**: O(n) — the string holds `n` values plus `n+1` null markers; recursion uses O(h).

### Verdict
The canonical answer. Preorder + null markers is the simplest complete encoding and the recursion symmetry between serialize and deserialize makes it easy to get right. This is what you present.

---

## Approach 2 — BFS level-order with null markers

### Intuition
Instead of preorder, encode the tree level by level (like LeetCode's own array format), writing `#` for null children. Deserialize with a queue: pop a parent, and the next two tokens are its left and right children.

### Algorithm
**Serialize**: BFS from root; for each dequeued node append its value (or `#`); if not null, enqueue both children (including nulls' parents only when non-null).
**Deserialize**: read the first token as the root, enqueue it; for each dequeued node consume the next two tokens as its children, enqueueing any non-null child.

### Code
```cpp
class Codec {
public:
    string serialize(TreeNode* root) {
        if (!root) return "#";
        string s;
        queue<TreeNode*> q; q.push(root);
        while (!q.empty()) {
            TreeNode* n = q.front(); q.pop();
            if (!n) { s += "#,"; continue; }
            s += to_string(n->val) + ",";
            q.push(n->left);
            q.push(n->right);
        }
        return s;
    }
    TreeNode* deserialize(string data) {
        if (data == "#") return nullptr;
        vector<string> t;
        string cur;
        for (char c : data) {
            if (c == ',') { t.push_back(cur); cur.clear(); }
            else cur += c;
        }
        TreeNode* root = new TreeNode(stoi(t[0]));
        queue<TreeNode*> q; q.push(root);
        int i = 1;
        while (!q.empty()) {
            TreeNode* n = q.front(); q.pop();
            if (t[i] != "#") { n->left  = new TreeNode(stoi(t[i])); q.push(n->left); }
            i++;
            if (t[i] != "#") { n->right = new TreeNode(stoi(t[i])); q.push(n->right); }
            i++;
        }
        return root;
    }
};
```
```java
public class Codec {
    public String serialize(TreeNode root) {
        if (root == null) return "#";
        StringBuilder sb = new StringBuilder();
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        while (!q.isEmpty()) {
            TreeNode n = q.poll();
            if (n == null) { sb.append("#,"); continue; }
            sb.append(n.val).append(",");
            q.offer(n.left);
            q.offer(n.right);
        }
        return sb.toString();
    }
    public TreeNode deserialize(String data) {
        if (data.equals("#")) return null;
        String[] t = data.split(",");
        TreeNode root = new TreeNode(Integer.parseInt(t[0]));
        Queue<TreeNode> q = new LinkedList<>();
        q.offer(root);
        int i = 1;
        while (!q.isEmpty()) {
            TreeNode n = q.poll();
            if (!t[i].equals("#")) { n.left  = new TreeNode(Integer.parseInt(t[i])); q.offer(n.left); }
            i++;
            if (!t[i].equals("#")) { n.right = new TreeNode(Integer.parseInt(t[i])); q.offer(n.right); }
            i++;
        }
        return root;
    }
}
```
```python
from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return "#"
        out = []
        q = deque([root])
        while q:
            n = q.popleft()
            if not n:
                out.append("#")
                continue
            out.append(str(n.val))
            q.append(n.left)
            q.append(n.right)
        return ",".join(out)

    def deserialize(self, data):
        if data == "#":
            return None
        t = data.split(",")
        root = TreeNode(int(t[0]))
        q = deque([root])
        i = 1
        while q:
            n = q.popleft()
            if t[i] != "#":
                n.left = TreeNode(int(t[i]))
                q.append(n.left)
            i += 1
            if t[i] != "#":
                n.right = TreeNode(int(t[i]))
                q.append(n.right)
            i += 1
        return root
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) — the queue and the output string.

### Verdict
Equally valid and mirrors LeetCode's display format. Slightly more bookkeeping in deserialize (paired token consumption). Choose whichever order you find clearer; preorder DFS is usually the most concise.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Preorder DFS + `#` | O(n) | O(n) | most concise; symmetric recursion ⭐ |
| BFS level-order + `#` | O(n) | O(n) | matches LeetCode array format |

Both are O(n)/O(n) and lossless. The DFS version's serialize/deserialize symmetry makes it the easier one to write correctly under pressure.

---

## 🧪 Edge cases & pitfalls
- **Empty tree** → serialize to `"#"`; deserialize must return null. Guard this explicitly in the BFS version.
- **Single node** → `"x,#,#"` (DFS) or `"x"` (BFS).
- **Negative values** → fine; `stoi`/`parseInt`/`int()` parse the sign. Don't confuse a value like `-1` with the null marker `#` — that's exactly why the marker is a non-numeric symbol.
- **Pitfall — no null markers**: without them, structure is ambiguous and the round trip fails. Always encode nulls.
- **Pitfall — trailing delimiter**: appending `"val,"` leaves a trailing comma; `split(",")` may yield a trailing empty token. The DFS deserializer is index-driven and stops once the tree is built, so it ignores extras — but be careful if you iterate all tokens.
- **Pitfall (DFS) — shared mutable index**: the read position must be shared across recursive calls (a reference/`int[]`/iterator). A by-value copy resets progress and corrupts the rebuild.
- **Pitfall (BFS) — advancing the token index**: consume exactly two tokens per dequeued node (left then right), incrementing whether or not the child is `#`.

---

## 🔗 Related problems
- **Construct Binary Tree from Preorder and Inorder** (LC 105) — reconstruction from traversals. See [`13-Construct-Tree-Preorder-Inorder.md`](./13-Construct-Tree-Preorder-Inorder.md).
- **Subtree of Another Tree** (LC 572) — serialize + substring match. See [`06-Subtree-of-Another-Tree.md`](./06-Subtree-of-Another-Tree.md).
- **Serialize and Deserialize BST** (LC 449) — BST ordering lets you drop null markers.
- **Find Duplicate Subtrees** (LC 652) — hash serialized subtrees to detect repeats.

---

**→ Next:** This is the last problem — back to [`00-Index.md`](./00-Index.md) | **← Prev:** [`14-Binary-Tree-Maximum-Path-Sum.md`](./14-Binary-Tree-Maximum-Path-Sum.md) | Up to [vault index](../00-Index.md)
