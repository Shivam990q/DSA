# 🔥 Heaps & Range Query Compendium

> Compact reference for: Heaps (binary, Fibonacci, pairing), Sparse Table, BIT, Segment Tree variants, Wavelet Tree.

---

## 19 — BINARY HEAP

### Concept
Complete binary tree (filled left-to-right). Heap property: parent ≥ children (max-heap) or parent ≤ children (min-heap).

### Array representation
For node at index i (1-indexed):
- Parent: i / 2
- Left child: 2i
- Right child: 2i + 1

### Operations
- Insert: append, **bubble up** O(log n)
- Extract root: replace with last, remove last, **bubble down** O(log n)
- Peek root: O(1)
- Build heap from array: O(n) (bottom-up heapify)

### Implementation (max-heap)
```cpp
class MaxHeap {
    vector<int> h;
    void up(int i) {
        while (i > 0 && h[(i-1)/2] < h[i]) {
            swap(h[(i-1)/2], h[i]);
            i = (i - 1) / 2;
        }
    }
    void down(int i) {
        int n = h.size();
        while (2*i + 1 < n) {
            int j = 2*i + 1;
            if (j + 1 < n && h[j + 1] > h[j]) j++;
            if (h[i] >= h[j]) break;
            swap(h[i], h[j]);
            i = j;
        }
    }
public:
    void push(int x) { h.push_back(x); up(h.size() - 1); }
    int top() { return h[0]; }
    void pop() { swap(h[0], h.back()); h.pop_back(); down(0); }
    bool empty() { return h.empty(); }
};
```

### Heap Sort
Build max-heap O(n). Repeatedly extract max O(log n) → O(n log n) total. In-place. Not stable.

### Use cases
- Priority queue
- Top-K problems
- Merge K sorted lists
- Median of stream (two heaps)
- Dijkstra's
- Prim's MST

---

## 20 — FIBONACCI HEAP

### Concept
Theoretically optimal heap with O(1) amortized for insert, decrease-key, merge; O(log n) amortized for extract-min.

### Why theoretically?
Allows Dijkstra's in O(E + V log V) instead of O((E+V) log V) with binary heap.

### Why rarely used in practice
- Massive constants
- Complex implementation
- Pairing heap is simpler and similarly fast in practice

---

## 21 — PAIRING HEAP

### Concept
Heap-ordered multi-way tree. Simple operations: insert = single-node tree merge; extract-min pulls children + multipasses-merge.

### Performance
- Insert: O(1)
- Extract-min: O(log n) amortized
- Decrease-key: O(log n) amortized (some bounds debated; o(log n) by Iacono)

Used in some Boost / LEDA libraries.

---

## 22 — INDEXED PRIORITY QUEUE

### Why
Vanilla priority_queue can't decrease-key without re-pushing (and lazy-deletion).

For Dijkstra's with decrease-key (rather than re-push), use:
```cpp
struct IndexedPQ {
    vector<int> pq, qp;  // pq: heap; qp[v] = position of v in heap; -1 if not present
    vector<int> keys;
    // ... insert, decreaseKey, extractMin all O(log n)
};
```

In practice, for Dijkstra, just push duplicates and skip stale entries on extraction. Easier; same Big-O.

---

## 23 — PREFIX SUM & DIFFERENCE ARRAY

### Prefix sum (immutable)
```cpp
vector<long long> P(n + 1, 0);
for (int i = 0; i < n; i++) P[i+1] = P[i] + a[i];
// range sum [l, r] (inclusive): P[r+1] - P[l]
```

### Difference array (range updates, point queries)
```cpp
vector<long long> D(n + 1, 0);
// add x to range [l, r]:
D[l] += x; D[r+1] -= x;
// final value at i: prefix sum of D up to i
```

### 2D prefix sum
```cpp
P[i+1][j+1] = a[i][j] + P[i][j+1] + P[i+1][j] - P[i][j];
// rect sum [r1, r2] x [c1, c2]:
sum = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1];
```

---

## 24 — SPARSE TABLE

### Concept
For static arrays + idempotent operations (min, max, gcd, AND, OR), precompute 2^k-length window aggregates. Then any range query is the union of two overlapping power-of-2 windows.

### Build O(n log n), query O(1).

```cpp
const int LOG = 20;
int sp[LOG][MAXN];
int n;
void build(vector<int>& a) {
    n = a.size();
    for (int i = 0; i < n; i++) sp[0][i] = a[i];
    for (int k = 1; k < LOG; k++)
        for (int i = 0; i + (1 << k) <= n; i++)
            sp[k][i] = min(sp[k-1][i], sp[k-1][i + (1 << (k-1))]);
}
int query(int l, int r) {  // [l, r], O(1)
    int k = __lg(r - l + 1);
    return min(sp[k][l], sp[k][r - (1 << k) + 1]);
}
```

### Limitation: NO updates. (For updates, use segtree.)

---

## 25 — FENWICK TREE / BIT

### Concept
Cleverly compressed segment tree for **prefix-sum-style** aggregates. Half the memory, simpler code.

### Operations
- Point update: O(log n)
- Prefix query: O(log n)
- Range query [l, r] = prefix(r) - prefix(l-1)

### Trick
Each i covers `i & -i` elements. `i & -i` is the lowest set bit.

```cpp
struct BIT {
    int n;
    vector<long long> t;
    BIT(int n) : n(n), t(n + 1, 0) {}
    void update(int i, long long v) {
        for (++i; i <= n; i += i & -i) t[i] += v;
    }
    long long query(int i) {  // sum [0..i]
        long long s = 0;
        for (++i; i > 0; i -= i & -i) s += t[i];
        return s;
    }
    long long range(int l, int r) { return query(r) - (l ? query(l-1) : 0); }
};
```

### Variants
- **Range update + range query BIT**: two BITs (cleverly combined).
- **2D BIT**: O(log²) for 2D prefix sum queries.

### When to choose BIT vs Segtree
- BIT: prefix-sum-only aggregates, simpler code, smaller constant.
- Segtree: arbitrary associative ops, range updates with lazy, more flexibility.

---

## 26-29 — SEGMENT TREE FAMILY

- **Basic** segment tree (point update + range query) → see [`26-Segment-Tree.md`](./26-Segment-Tree.md) ⭐
- **Lazy propagation** (range update + range query): each node stores a pending update pushed down on demand → template at [`../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/segment-tree-lazy.cpp)
- **Persistent segment tree** (versioned): each update creates O(log n) new nodes, keeping all historical versions; enables "K-th smallest in subarray [l,r]" offline/online
- **Segment tree beats**: handles range chmin/chmax + range sum in O(n log² n) amortized (Ji Driver Segment Tree); track max, second-max, count-of-max per node
- **Iterative** variants for speed (see [`26-Segment-Tree.md`](./26-Segment-Tree.md) §IV)

---

## 30 — MERGE SORT TREE

### Concept
Segment tree where each node stores a **sorted vector** of its interval's values.

### Use case
"How many elements in [l, r] are ≥ x?" — O(log² n) per query (descend segtree O(log n), binary-search each visited node's vector O(log n)).

### Tradeoff
- Build: O(n log n), Memory: O(n log n)
- No updates (or O(n) updates).

For updates + same query: use **persistent segtree** or **wavelet tree**.

---

## 31 — WAVELET TREE

### Concept
Recursive structure on values: at each level, split values into "lower half" and "upper half"; track membership via bitvectors.

### Use cases
- "K-th smallest in range [l, r]" — O(log V) per query
- "Count of x in [l, r]" — O(log V)
- "Number of values in [a, b] in range [l, r]" — O(log V)

### Build: O(n log V), Memory: O(n log V).

---

**→ Next compendium:** [`COMPENDIUM-Advanced-DS.md`](./COMPENDIUM-Advanced-DS.md)
