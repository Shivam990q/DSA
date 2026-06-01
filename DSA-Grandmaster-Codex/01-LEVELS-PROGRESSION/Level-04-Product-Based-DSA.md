# 🦄 Level 4 — Product-Based DSA (The Unicorn-Ready)

> *"You can solve. Now solve elegantly, in many ways, with proof."*

---

## 🎯 OUTCOME

You can:
- Crack senior interviews at unicorns: Razorpay, Atlassian, Stripe (junior), Uber, Airbnb, ServiceNow, Salesforce
- Approach 90% of [LeetCode](https://leetcode.com) Mediums and 50% of Hards
- Reason about multiple solutions and tradeoffs
- Write clean, optimal, edge-case-safe code under pressure
- Explain solutions with mathematical rigor

---

## 📚 PREREQUISITE

Level 3 passed.

---

## 🧱 CURRICULUM (10 Modules, ~300 hours)

### Module 4.1 — Advanced DP (Part 2) (40 hours)

**Topics:**
1. **DP on Trees** (revisited deeply)
   - Subtree DP
   - Re-rooting DP (compute answer from each node as root)
2. **DP on Graphs (DAGs)**
3. **Digit DP** — count numbers with property in [L, R]
4. **Bitmask DP** — small n (≤ 20) with subset states
5. **Probability DP / Expected value DP**
6. **DP with Data Structures** (segment tree + DP)
7. **DP optimization techniques** (preview — full at Level 6)

**Problems (25):**

#### Tree DP:
1. Sum of distances in tree (re-rooting)
2. Tree with maximum cost (re-rooting)
3. Binary tree cameras
4. Number of ways to reorder array to get same BST
5. Maximum sum BST in binary tree

#### DAG DP:
6. Longest path in DAG
7. Cheapest flights (revisit, with DP)
8. Number of ways to reach destination
9. Course schedule III

#### Digit DP:
10. Count numbers with unique digits
11. Numbers at most N given digit set
12. Count of integers
13. Numbers with repeated digits

#### Bitmask DP:
14. Traveling salesman (TSP) — n ≤ 20
15. Partition to K equal sum subsets
16. Find minimum time to finish all jobs
17. Maximum students taking exam
18. Number of ways to wear different hats
19. Beautiful arrangement
20. Minimum incompatibility

#### Probability DP:
21. Knight probability in chessboard
22. New 21 game
23. Out of boundary paths
24. Soup servings

#### Hard DP:
25. Frog jump

---

### Module 4.2 — Graph Theory Advanced (25 hours)

**New algorithms:**
1. **Bridges & Articulation points** (Tarjan's, O(V+E))
2. **Strongly Connected Components** (Tarjan's / Kosaraju's, O(V+E))
3. **Eulerian path / circuit** (Hierholzer's algorithm)
4. **Bipartite matching** (Kuhn's algorithm — Level 5)
5. **Network flow basics** (Ford-Fulkerson, Edmonds-Karp — Level 5)
6. **2-SAT** (preview)

**Problems (15):**
1. Critical connections in a network (bridges)
2. Find articulation points
3. Find SCCs (output components)
4. Reconstruct itinerary (Eulerian path)
5. Cracking the safe (Eulerian circuit on de Bruijn graph)
6. Minimum number of vertices to reach all nodes (in-degree 0)
7. Course schedule IV (transitive closure)
8. Find all people with secret (Union-Find with timing)
9. Smallest string with swaps
10. Friend circles (Union-Find)
11. Redundant connection I, II
12. Number of operations to make network connected
13. Critical and pseudo-critical edges in MST
14. Build a matrix with conditions
15. Minimum reverse to make path

---

### Module 4.3 — Segment Tree Foundation (20 hours)

**Concepts:**
- Segment tree = binary tree over array intervals
- Operations: point update + range query OR range update + point query
- Each node represents a segment; combines children
- Build: O(n), query: O(log n), update: O(log n)

**Implementation (recursive):**
```cpp
class SegTree {
    int n;
    vector<long long> tree;
    
    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) { tree[node] = arr[start]; return; }
        int mid = (start + end) / 2;
        build(arr, 2*node, start, mid);
        build(arr, 2*node+1, mid+1, end);
        tree[node] = tree[2*node] + tree[2*node+1];  // sum query
    }
    
    void update(int node, int start, int end, int idx, int val) {
        if (start == end) { tree[node] = val; return; }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2*node, start, mid, idx, val);
        else update(2*node+1, mid+1, end, idx, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    long long query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return query(2*node, start, mid, l, r) + query(2*node+1, mid+1, end, l, r);
    }
public:
    SegTree(vector<int>& arr) : n(arr.size()), tree(4 * n) { build(arr, 1, 0, n-1); }
    void update(int idx, int val) { update(1, 0, n-1, idx, val); }
    long long query(int l, int r) { return query(1, 0, n-1, l, r); }
};
```

**Problems (12):**
1. Range sum query — mutable
2. Count of smaller numbers after self
3. Falling squares
4. Range minimum query
5. Reverse pairs
6. The skyline problem (or use multiset)
7. My calendar III (lazy propagation needed — preview)
8. Range update queries (preview lazy)
9. Maximum frequency stack (separate but related)
10. Number of longest increasing subsequence (using BIT/segtree by value)
11. Maximum sum BIT problem
12. Russian doll envelopes (with BIT — alternative to LIS)

---

### Module 4.4 — Binary Indexed Tree / Fenwick Tree (8 hours)

**Concepts:**
- BIT = compressed segment tree for prefix sums
- O(log n) update + prefix sum query
- Trick: `i & -i` gives lowest set bit

**Implementation:**
```cpp
struct BIT {
    int n;
    vector<long long> tree;
    BIT(int n) : n(n), tree(n + 1, 0) {}
    void update(int i, long long delta) {
        for (++i; i <= n; i += i & -i) tree[i] += delta;
    }
    long long query(int i) {  // sum [0..i]
        long long s = 0;
        for (++i; i > 0; i -= i & -i) s += tree[i];
        return s;
    }
    long long query(int l, int r) { return query(r) - (l ? query(l-1) : 0); }
};
```

**Problems (8):**
1. Range sum query (immutable + mutable)
2. Count of smaller numbers after self
3. Reverse pairs
4. Count number of teams (3-element)
5. Create sorted array through instructions
6. Number of longest increasing subsequence
7. Pairs with the largest sum
8. Sum of beauty of all substrings

---

### Module 4.5 — String Algorithms (Advanced) (15 hours)

**New algorithms:**
1. **KMP** — pattern matching in O(n+m)
2. **Z-algorithm** — prefix array
3. **Rabin-Karp** — rolling hash, expected O(n+m)
4. **Manacher's** — longest palindromic substring in O(n)
5. **Suffix array** (preview — Level 6)
6. **Trie + DP** combinations

**KMP Implementation:**
```cpp
vector<int> computeFailure(string& p) {
    int m = p.size();
    vector<int> fail(m, 0);
    for (int i = 1, j = 0; i < m; ) {
        if (p[i] == p[j]) fail[i++] = ++j;
        else if (j > 0) j = fail[j-1];
        else fail[i++] = 0;
    }
    return fail;
}

vector<int> kmp(string& t, string& p) {
    vector<int> fail = computeFailure(p);
    vector<int> matches;
    int n = t.size(), m = p.size();
    for (int i = 0, j = 0; i < n; ) {
        if (t[i] == p[j]) { i++; j++; if (j == m) { matches.push_back(i-m); j = fail[j-1]; } }
        else if (j > 0) j = fail[j-1];
        else i++;
    }
    return matches;
}
```

**Problems (10):**
1. Implement strStr (KMP)
2. Shortest palindrome (KMP on s + "#" + reverse(s))
3. Longest happy prefix
4. Repeated substring pattern (KMP)
5. Find beautiful indices in given array
6. Longest palindromic substring (Manacher)
7. Count palindromic substrings (Manacher)
8. Distinct echo substrings
9. Sum of scores of strings (Z-function)
10. String matching in array (Z-function)

---

### Module 4.6 — Math (Number Theory + Combinatorics) (15 hours)

**Topics:**
1. Modular arithmetic in depth
2. Modular inverse (Fermat's, Extended Euclidean)
3. Linear sieve for primes + smallest prime factor
4. Euler's totient function (φ)
5. Combinatorics: nCr precomputation, Pascal's triangle, modular nCr
6. Catalan numbers
7. Stars and bars
8. Inclusion-Exclusion principle

**Problems (12):**
1. Unique paths (combinatorial)
2. Catalan numbers (count valid parens, BSTs, etc.)
3. Climbing stairs with k steps
4. Number of ways to split a string
5. Number of ways to fill array
6. Count submatrices with sum of all 1
7. nCr modulo prime
8. nth digit of pi sequence (Euler-related)
9. Number of GCD subsequences
10. Subarrays with GCD = 1
11. Smallest value of GCD-LCM
12. Sum of GCDs

---

### Module 4.7 — Hard Patterns (15 hours)

**Pattern**: Sweep line / event-based
**Pattern**: Coordinate compression
**Pattern**: Offline queries

**Problems (12):**
1. Skyline problem (sweep line)
2. Meeting rooms II
3. Employee free time
4. Number of recent calls
5. Range module
6. My calendar I, II, III
7. Falling squares
8. Rectangle area I, II
9. Perfect rectangle
10. Number of submatrices that sum to target
11. Maximum sum rectangle in 2D matrix
12. Maximum number of events that can be attended

---

### Module 4.8 — Advanced Patterns (15 hours)

**Patterns:**
- Meet in the middle (n=40 → split, O(2^(n/2)))
- Square root decomposition (preview)
- Mo's algorithm (preview)

**Problems (8):**
1. Subset sum (n=40, MITM)
2. 4-sum (with hashing or MITM)
3. Closest subset sum (MITM)
4. Find two non-overlapping subarrays with each having target sum
5. Number of ways to split array (with constraint)
6. Maximum sum rectangle ≤ K
7. Distance from grid to all points
8. Minimum operations to reach target (BFS / MITM)

---

### Module 4.9 — Concurrency (Bonus, 8 hours)

For senior interviews at certain companies:

**Concepts:**
- Threads, locks, semaphores
- Producer-consumer
- Reader-writer
- Race conditions, deadlocks

**Problems (6):**
1. Print in order (3 threads)
2. Print foo bar alternately
3. Building H2O
4. Fizz buzz multithreaded
5. Web crawler multithreaded
6. The dining philosophers

---

### Module 4.10 — System Design Lite (20 hours)

For senior product company interviews:

**Topics**:
- Caching (LRU, LFU, write-through, write-back)
- Rate limiting (token bucket, leaky bucket)
- Consistent hashing
- Database sharding
- CAP theorem (basic)
- Pub-sub model

**Practice with these designs (DSA-flavored):**
1. Design Twitter
2. Design URL shortener
3. Design key-value store
4. Design rate limiter
5. Design news feed
6. Design parking lot
7. Design elevator system
8. Design hit counter
9. Design Snake game
10. Design file system

---

### Module 4.11 — Mock Interview & Speed Practice (10 hours)

**Targets:**
- 10 mock interviews
- 30 timed LC Mediums (25 min each)
- 5 timed LC Hards (45 min each)

---

## 📊 PROBLEM VOLUME

- ~150 structured + 50 design/concurrency
- **Cumulative**: 700+ LeetCode + 200+ [Codeforces](https://codeforces.com)

---

## ⏱️ ESTIMATED TIME

- 300 hours
- ~7 months at 10 hours/week
- ~3 months at 25 hours/week

---

## ✅ EXIT TEST

In 5 hours:

1. Implement segment tree from scratch (with point update + range sum).
2. Implement KMP from scratch.
3. Solve [LC 218: The Skyline Problem](https://leetcode.com/problems/the-skyline-problem).
4. Solve [LC 727: Minimum Window Subsequence](https://leetcode.com/problems/minimum-window-subsequence) — DP.
5. Solve [LC 312: Burst Balloons](https://leetcode.com/problems/burst-balloons) — interval DP.
6. Solve [LC 1192: Critical Connections](https://leetcode.com/problems/critical-connections-in-a-network) — Tarjan's bridges.
7. 25-min mock on a random Medium with narration.

**Pass**: 5/7 + clean mock.

---

## 📌 RESOURCES

### Sheets
- **LeetCode Hard list** (gradually solve top 50)
- **Striver SDE Sheet** + **A2Z Sheet** (deep dive)
- **GFG SDE Sheet (450)**

### Books
- **Competitive Programming Handbook** (Antti Laaksonen) — Chapters 1-12
- **Algorithms** (Sedgewick) — Trees, graphs, strings chapters

### Channels
- **[Errichto](https://www.youtube.com/@Errichto)** (algorithm topics, advanced)
- **[William Lin](https://www.youtube.com/@tmwilliamlin168)** (CP perspective)
- **Take U Forward** (advanced playlists)

### CP-Algorithms.com
- The encyclopedia. Bookmark every page.

---

## 🚀 ON COMPLETION

You're now interview-ready for senior roles at unicorns. The next level is FAANG.

**→ Proceed to:** [`Level-05-FAANG-DSA.md`](./Level-05-FAANG-DSA.md)
