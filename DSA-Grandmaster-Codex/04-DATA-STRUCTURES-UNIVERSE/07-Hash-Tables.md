# 🗺️ Hash Tables — The O(1) Magic

> *"A hash table is a wager: with a good hash, you spend O(1). With a bad one, you pay forever."*

---

## I. THE IDEA

**Goal**: store key→value pairs with O(1) expected insert, lookup, delete.

**Mechanism**:
1. Hash function `h(k)` maps key to integer (the "hash").
2. Table of size `m`. Bucket = `h(k) mod m`.
3. Place value in bucket.
4. Lookup: re-hash, find bucket, retrieve.

```
Key "apple" → hash = 0xABCDEF → bucket = 0xABCDEF mod 16 = 5
            → store at table[5]
```

---

## II. COLLISIONS

If two keys hash to the same bucket → collision.

### Resolution 1: **Chaining** (separate chaining)
Each bucket = linked list (or vector). On collision, append to list.

```
table[5] → [("apple", 3) → ("banana", 7) → ...]
```

### Resolution 2: **Open Addressing**
On collision, find another bucket via a probing sequence.
- **Linear probing**: try bucket+1, bucket+2, ...
- **Quadratic probing**: bucket+1, bucket+4, bucket+9, ...
- **Double hashing**: bucket + i × h₂(k)

---

## III. LOAD FACTOR & RESIZING

**Load factor α = n / m** (entries / buckets).

- α small (< 0.5): wasted memory, fast ops.
- α large (> 0.7): more collisions, slow ops.
- α = 1: chaining still works; open addressing fails.

When α exceeds threshold (e.g., 0.75 in Java's HashMap), **resize**: allocate new table 2× size, rehash all entries. O(n) cost, amortized O(1) per insert.

---

## IV. HASH FUNCTION QUALITY

A good hash function:
- **Uniform**: distributes keys evenly across buckets
- **Fast**: O(1) per call
- **Deterministic**: same key always same hash

For integers: `h(k) = k mod m` (with prime m), or `(a*k + b) mod p mod m` (universal hashing).

For strings: polynomial rolling hash:
```
h(s) = (s[0] + s[1]·B + s[2]·B² + ... + s[n-1]·B^(n-1)) mod p
```
Common: B = 31 or 131, p = 10⁹+7.

For **adversarial** inputs (CF anti-hash), use **two hashes** with different bases.

---

## V. PYTHON DICT INTERNALS

CPython's `dict` is a **hash table with open addressing** + **probing sequence based on hash perturbation**.

- Each slot stores: hash, key, value
- On collision, perturbation moves through slots
- Resizes at 2/3 load factor (grows or shrinks)
- Insertion order preserved (since Python 3.7)

### Why dict can be slow for adversarial input
For CP, hash collisions can be intentional (string keys with crafted hashes). Use `defaultdict` or convert to int keys when possible.

---

## VI. C++ STL: unordered_map vs map

| Feature       | `unordered_map` (hash) | `map` (BST)      |
|---------------|------------------------|-------------------|
| Avg lookup    | O(1)                    | O(log n)          |
| Worst lookup  | O(n) (collisions)       | O(log n)          |
| Memory        | More (table + chains)   | Less              |
| Ordering      | None                    | Sorted by key     |
| Iteration     | Arbitrary               | Sorted            |
| Anti-hash     | Vulnerable in CP        | Safe              |

**For CP**: prefer `map` unless you specifically need O(1) and have non-adversarial data. For [LeetCode](https://leetcode.com)/interviews: `unordered_map` is fine.

### Anti-hack in C++
```cpp
struct custom_hash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
        x = x ^ (x >> 31);
        return x;
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + FIXED_RANDOM);
    }
};

unordered_map<long long, int, custom_hash> safe_map;
```

---

## VII. HASH SET

Same as hash map but only stores keys. Common ops:
- `insert(k)`: add k
- `contains(k)`: O(1) check
- `erase(k)`: O(1) remove

Use cases: deduplication, "have I seen?" queries, set operations.

---

## VIII. PROBLEMS WHERE HASH TABLES SHINE

1. **Two Sum** — hash for complement
2. **Group Anagrams** — sorted string as hash key
3. **First Unique Character** — frequency map
4. **Longest Consecutive Sequence** — set membership for chain detection
5. **Subarray Sum Equals K** — prefix sum count via hash
6. **Top K Frequent Elements** — frequency counter + heap/sort
7. **Isomorphic Strings** — bidirectional mapping
8. **Word Pattern** — bijection via two maps
9. **Happy Number** — cycle detection via set
10. **Valid Sudoku** — sets per row/col/box

---

## IX. WHEN NOT TO USE HASH TABLES

- When you need ordering (use BST/sorted container)
- When you need range queries (use segment tree, not hash)
- When key comparison is expensive (sometimes BST faster due to cache)
- When worst-case must be O(log n) (against adversaries)

---

## X. FROM SCRATCH IMPLEMENTATION (C++)

```cpp
struct HashMap {
    static const int M = 1 << 20;  // power of 2
    vector<vector<pair<int, int>>> table;
    HashMap() : table(M) {}
    
    int h(int k) { return (k * 2654435761u) >> (32 - 20); }  // Knuth multiplicative
    
    void put(int k, int v) {
        int b = h(k);
        for (auto& [key, val] : table[b])
            if (key == k) { val = v; return; }
        table[b].push_back({k, v});
    }
    
    int get(int k) {
        int b = h(k);
        for (auto& [key, val] : table[b])
            if (key == k) return val;
        return -1;
    }
    
    void erase(int k) {
        int b = h(k);
        auto& chain = table[b];
        for (auto it = chain.begin(); it != chain.end(); ++it)
            if (it->first == k) { chain.erase(it); return; }
    }
};
```

---

## XI. RECOMMENDED READING

- **CLRS Chapter 11** — exhaustive treatment
- **[CP-Algorithms](https://cp-algorithms.com): hashing** — for CP-style usage
- **Cuckoo hashing paper** (Pagh, Rodler 2001) — for guaranteed O(1) worst case

---

## 08 — BLOOM FILTER (hash-based set, probabilistic)

### Concept
A space-efficient **probabilistic set**. A bit array of size m + k independent hash functions. To insert x: set the k bits `h₁(x), …, h_k(x)`. To query x: if ALL k bits are set → "possibly present"; if ANY bit is 0 → "definitely absent".

### Key property
- **No false negatives** (if it says absent, it's truly absent).
- **False positives possible** (it may say "present" for an item never inserted).
- **Cannot delete** (clearing a bit could break other items) — use a **Counting Bloom Filter** (counters instead of bits) if deletion is needed.

### Complexity
- Insert / query: O(k) — constant.
- Memory: ~m bits for n items; false-positive rate ≈ (1 − e^(−kn/m))^k. Optimal k = (m/n)·ln2.

### Use cases
- "Have I seen this URL/key before?" before an expensive DB/disk lookup (databases, caches, Chrome's malicious-URL check, Bitcoin SPV).

```cpp
struct BloomFilter {
    vector<bool> bits; int m, k;
    BloomFilter(int m, int k) : bits(m, false), m(m), k(k) {}
    size_t hash(long long x, int i) const {
        return (std::hash<long long>{}(x) ^ (i * 0x9e3779b97f4a7c15ULL)) % m;
    }
    void add(long long x) { for (int i = 0; i < k; i++) bits[hash(x, i)] = true; }
    bool maybe(long long x) const {
        for (int i = 0; i < k; i++) if (!bits[hash(x, i)]) return false; // definitely absent
        return true; // possibly present
    }
};
```

---

## 09 — CUCKOO HASHING (worst-case O(1) lookup)

### Concept
Use **two** hash tables with two hash functions h₁, h₂. Every key x lives at EITHER `h₁(x)` in table 1 or `h₂(x)` in table 2 — so lookup checks just **two** slots → **worst-case O(1)** (not just average).

### Insertion (the "cuckoo" kick-out)
Place x at `h₁(x)`. If occupied, evict the resident y, place x there, then re-place y at its alternate slot — repeat. If a cycle/too-many-kicks occurs, **rehash** with new hash functions.

### Complexity
- Lookup / delete: **O(1) worst-case** (exactly 2 probes).
- Insert: O(1) amortized expected (occasional rehash).
- Load factor must stay below ~50% (2 tables) or ~91% (with buckets) to avoid frequent rehashing.

### Use cases
- Hardware routers / switches (guaranteed lookup time).
- Cuckoo filter (a modern alternative to Bloom filter that also supports deletion).

---

**→ Next:** KD-Tree, Skip List & all advanced structures → [`COMPENDIUM-Advanced-DS.md`](./COMPENDIUM-Advanced-DS.md)
