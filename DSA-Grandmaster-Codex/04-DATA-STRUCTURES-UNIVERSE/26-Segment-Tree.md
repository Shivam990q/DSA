# 📐 Segment Tree — The Range Query Workhorse

> *"A segment tree is a binary tree where each node guards an interval. Master it, and ranges bow to you."*

---

## I. THE IDEA

A segment tree is a binary tree where:
- Each leaf corresponds to a single array element
- Each internal node corresponds to the union of its children's intervals
- Each node stores aggregate info (sum, min, max, gcd, etc.) about its interval

Operations: O(log n) point update + range query (or range update + point query).

---

## II. STRUCTURE

For an array of size n, build a binary tree with 2^⌈log₂ n⌉ leaves (round up to power of 2). Total nodes ≤ 4n.

```
Array: [3, 1, 4, 1, 5, 9, 2, 6]

Tree (sums):
                  31
              /        \
           9              22
         /    \          /    \
        4      5        14     8
       / \    / \      / \    / \
      3   1  4   1    5   9  2   6
```

---

## III. RECURSIVE IMPLEMENTATION (sum query, point update)

```cpp
class SegTree {
    int n;
    vector<long long> tree;
    
    void build(vector<int>& a, int node, int l, int r) {
        if (l == r) { tree[node] = a[l]; return; }
        int mid = (l + r) / 2;
        build(a, 2*node, l, mid);
        build(a, 2*node+1, mid+1, r);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    void update(int node, int l, int r, int idx, int val) {
        if (l == r) { tree[node] = val; return; }
        int mid = (l + r) / 2;
        if (idx <= mid) update(2*node, l, mid, idx, val);
        else update(2*node+1, mid+1, r, idx, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    long long query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;       // outside
        if (ql <= l && r <= qr) return tree[node];  // fully inside
        int mid = (l + r) / 2;
        return query(2*node, l, mid, ql, qr) + query(2*node+1, mid+1, r, ql, qr);
    }
public:
    SegTree(vector<int>& a) : n(a.size()), tree(4 * a.size()) { build(a, 1, 0, n-1); }
    void update(int idx, int val) { update(1, 0, n-1, idx, val); }
    long long query(int l, int r) { return query(1, 0, n-1, l, r); }
};
```

---

## IV. ITERATIVE SEGMENT TREE (cache-friendly)

For competitive programming, iterative is faster (~2-3×):

```cpp
int n;
long long t[2 * MAX_N];  // t[1..2n-1]

void build(int n) {
    for (int i = n - 1; i > 0; --i)
        t[i] = t[2*i] + t[2*i + 1];
}

void update(int p, long long val) {
    for (t[p += n] = val; p >>= 1; )
        t[p] = t[2*p] + t[2*p + 1];
}

long long query(int l, int r) {  // [l, r)
    long long res = 0;
    for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
        if (l & 1) res += t[l++];
        if (r & 1) res += t[--r];
    }
    return res;
}
```

---

## V. AGGREGATION FUNCTION

Replace `+` with any **associative** operation:
- **Sum**: `+`, identity = 0
- **Min**: `min(a, b)`, identity = +∞
- **Max**: `max(a, b)`, identity = -∞
- **GCD**: `gcd(a, b)`, identity = 0
- **XOR**: `^`, identity = 0
- **Product**: `*`, identity = 1
- **Count of distinct max** (with tie-handling)

---

## VI. RANGE UPDATE (Lazy Propagation)

If you need to update a range (e.g., "add 5 to a[3..7]"), naive is O(n) per update. Use **lazy propagation**:
- Each internal node stores a "pending update" not yet pushed to children
- Push lazy down when querying / updating a child

See the lazy-propagation template at [`../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp) and the full family in [`COMPENDIUM-Heaps-And-Range.md`](./COMPENDIUM-Heaps-And-Range.md).

---

## VII. COMMON PROBLEMS

1. **Range Sum Query — Mutable** (LC 307)
2. **Count of Smaller Numbers After Self** (LC 315)
3. **The Skyline Problem** (LC 218)
4. **Reverse Pairs** (LC 493)
5. **Falling Squares** (LC 699)
6. **Range Module** (LC 715)
7. **Online Election** — segtree on time
8. [CSES](https://cses.fi/problemset/) Range Sum/Min Queries
9. CF EDU segment trees course

---

## VIII. EXTENSIONS

- **Lazy propagation** (range update + range query)
- **Persistent segment tree** (versioned, O(log n) per op)
- **Segment tree beats** (range chmin/chmax)
- **Merge sort tree** (each node holds sorted vector for K-th queries)
- **Wavelet tree** (rank/select queries)
- **2D segment tree** (range queries on a 2D matrix)
- **Segment tree on a tree** (with HLD or Euler tour)

---

## IX. WHEN TO USE

- **n ≤ 10⁵** with mixed updates and queries
- Aggregation operation is **associative** (and ideally has an identity)
- Need O(log n) per operation

---

## X. ALTERNATIVES

- **BIT (Fenwick)**: simpler, faster constants, but only prefix-sum aggregations
- **Sparse Table**: O(1) query but only for **idempotent** ops (min/max/gcd) AND no updates
- **Square root decomposition**: simpler code, O(√n) per op
- **Treap / balanced BST**: order-statistics + arbitrary keys

---

## XI. INTERVIEW TIPS

- Most companies ask about segment tree at L5/L6 (FAANG senior).
- Have a **memorized template**.
- Be ready to extend it (lazy, custom merge).
- Practice both recursive and iterative.

---

**→ Next:** Lazy propagation, persistent, beats & all range structures → [`COMPENDIUM-Heaps-And-Range.md`](./COMPENDIUM-Heaps-And-Range.md) · Template: [`../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp)
