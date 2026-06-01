# 🌳 Trees Compendium

> Compact reference for: Binary Trees, BST, AVL, Red-Black, B-Trees, Splay, Treap, Trie, Suffix Tree.

---

## 10 — BINARY TREES

### Concept
A tree where each node has ≤ 2 children. Not necessarily ordered or balanced.

### Properties
- A binary tree of height h has ≤ 2^(h+1) − 1 nodes
- A binary tree of n nodes has height ≥ ⌈log₂(n+1)⌉ − 1

### Traversals

```cpp
// Recursive
void preorder(Node* n)  { if(!n) return; visit(n); preorder(n->l); preorder(n->r); }
void inorder(Node* n)   { if(!n) return; inorder(n->l); visit(n); inorder(n->r); }
void postorder(Node* n) { if(!n) return; postorder(n->l); postorder(n->r); visit(n); }

// Level-order (BFS)
void levelOrder(Node* root) {
    queue<Node*> q; q.push(root);
    while(!q.empty()) {
        Node* n = q.front(); q.pop();
        visit(n);
        if (n->l) q.push(n->l);
        if (n->r) q.push(n->r);
    }
}

// Iterative inorder using stack
void inorderIter(Node* root) {
    stack<Node*> stk;
    while (root || !stk.empty()) {
        while (root) { stk.push(root); root = root->l; }
        root = stk.top(); stk.pop();
        visit(root);
        root = root->r;
    }
}
```

### Morris Traversal (O(1) extra space, O(n) time)
Uses threaded binary tree concept; modifies and restores the tree during traversal.

### Top problems
1. Inorder/preorder/postorder/level-order (recursive + iterative)
2. Maximum depth
3. Symmetric tree
4. Same tree
5. Invert binary tree
6. Diameter of binary tree
7. Binary tree maximum path sum
8. LCA of binary tree
9. Serialize / Deserialize
10. Construct from preorder + inorder
11. Vertical order traversal
12. Top view, Bottom view, Right side view
13. All nodes at distance K
14. House robber III

---

## 11 — BINARY SEARCH TREES (BST)

### Property
Left subtree values < node < right subtree values. (No duplicates typically; can be relaxed.)

### Operations
- Search: O(h)
- Insert: O(h)
- Delete: O(h) (3 cases: leaf / one child / two children — replace with successor or predecessor)
- In-order traversal yields sorted sequence

### Pitfall
Without balancing, BSTs can degenerate to a linked list (e.g., inserting sorted data) → O(n) operations.

→ Use AVL, Red-Black, Treap, or Splay for guaranteed log.

### Top problems
1. Validate BST
2. LCA of BST (O(h))
3. Kth smallest in BST
4. Convert sorted array to balanced BST
5. Two-sum in BST
6. Range sum of BST
7. Trim BST
8. Recover BST (two swapped nodes)
9. Inorder successor / predecessor

---

## 12 — AVL TREES

### Concept
Self-balancing BST. Invariant: |height(left) − height(right)| ≤ 1 at every node.

### Operations
- Insert: O(log n) + 1 or 2 rotations
- Delete: O(log n) + O(log n) rotations (worst case)
- Search: O(log n)

### Rotations
- Left rotation, right rotation, left-right (LR), right-left (RL)
- Trigger: when balance factor becomes ±2 after insert/delete

### Use case
- When you need strict balance (slightly faster lookups than RB)
- Less common than RB in practice (RB has fewer rotations on insert/delete)

---

## 13 — RED-BLACK TREES

### Concept
Self-balancing BST. Each node colored red or black; constraints maintain ~balanced height.

### Properties (the 5 rules)
1. Every node is red or black
2. Root is black
3. Every leaf (NIL) is black
4. Red nodes have black children
5. Every path from a node to descendant NIL has the same #black nodes

### Implication
Height ≤ 2 log₂(n+1).

### Performance
- Insert/Delete: O(log n) with at most 2-3 rotations + recoloring
- Search: O(log n)

### Where used
- **Java** TreeMap, TreeSet
- **C++** std::map, std::set
- **Linux kernel** scheduler (CFS), virtual memory
- Highly tuned, tested

### Pitfall (for CP)
Implementing RB from scratch is painful. Use built-ins (`map`, `set`).

---

## 14 — B-TREES (and B+ TREES)

### Concept
m-ary balanced trees designed for **disk storage**. Each node has up to m-1 keys, m children.

### Why
- Disk reads are slow (~ms); want each node to fit in a disk page (~4KB)
- A B-tree of order 100 with n=10⁹ keys has height ~5 (5 disk reads to find any key)

### Where used
- Database indexes (MySQL InnoDB, PostgreSQL — B+ trees)
- Filesystem indexing (NTFS, HFS+)

### B+ tree variant
- Leaves linked in a list (range queries fast)
- Internal nodes only have keys; values only in leaves

For DSA interviews, light coverage. For systems / DB roles, deep coverage.

---

## 15 — SPLAY TREES

### Concept
BST that **splays** the most recently accessed node to the root via rotations. Amortized O(log n) per op.

### Key property
Self-adjusting: frequently-accessed nodes become faster to access (amortized).

### Use case
- LRU-like access patterns
- Implicit treap / sequence operations
- When you don't want to store balance info (saves memory)

### Operations
All operations route through `splay(x)`. Amortized O(log n) via potential function argument.

---

## 16 — TREAP

### Concept
Tree + Heap. Each node has a key (BST property by key) + a random priority (heap property by priority). Random priorities → expected O(log n) height.

### Why
- Simpler to implement than RB or AVL
- Versatile: split, merge in O(log n)
- Implicit treap: index by position rather than value (sequence operations)

### Operations
- `split(T, x)`: split into ≤ x and > x trees
- `merge(L, R)`: assumes all in L < all in R
- Insert = split + merge
- Delete = split twice + merge

### Implicit treap
Use treap indexed by **position**. Allows O(log n):
- Insert at position k
- Delete at position k
- Reverse subarray [l, r] (with lazy "reverse" flag)
- Cyclic shift
- Sum/min/max over range

---

## 17 — TRIE (Prefix Tree)

### Concept
Tree where each node represents a character; paths from root represent prefixes.

### Operations
- Insert string of length L: O(L)
- Search string of length L: O(L)
- StartsWith prefix of length L: O(L)

### Implementation
```cpp
struct TrieNode {
    TrieNode* children[26] = {};
    bool isEnd = false;
};

void insert(TrieNode* root, const string& word) {
    TrieNode* cur = root;
    for (char c : word) {
        int i = c - 'a';
        if (!cur->children[i]) cur->children[i] = new TrieNode();
        cur = cur->children[i];
    }
    cur->isEnd = true;
}
```

### Use cases
- Autocomplete
- Spell checker
- IP routing (longest prefix match)
- XOR maximization (binary trie)
- Word puzzles (Word Search II)

### Top problems
1. Implement Trie
2. Add and Search Word (with wildcards)
3. Word Search II (board + dictionary)
4. Replace Words
5. Maximum XOR of Two Numbers
6. Concatenated Words
7. Longest Word in Dictionary
8. Stream of Characters
9. Map Sum Pairs
10. Word Squares

### Variants
- **Compressed Trie / Radix Tree**: compress single-child chains
- **Suffix Trie**: trie of all suffixes (O(n²) space) → use suffix tree / array instead
- **Binary Trie** (over bits): for XOR problems

---

## 18 — SUFFIX TREE

### Concept
A compressed trie of all suffixes of a string. O(n) space (Ukkonen's algorithm: O(n) construction).

### Use cases
- Substring queries (does P occur in T? in O(|P|))
- Longest common substring of two strings
- Distinct substrings count
- Genome analysis

### Modern alternative
**Suffix array + LCP array**: similar power, simpler implementation, less memory. See [Universe 08: Strings](../08-STRING-UNIVERSE/).

---

**→ Next compendium:** [`COMPENDIUM-Heaps-And-Range.md`](./COMPENDIUM-Heaps-And-Range.md)
