# 🌳 Level 2 — Academic / B.Tech DSA (The Scholar)

> *"You now form sentences. Time to write paragraphs."*

---

## 🎯 OUTCOME

You can:
- Implement and analyze trees, BSTs, heaps from scratch
- Apply BFS, DFS, Dijkstra to graph problems
- Solve basic DP problems (0/1 knapsack, LIS, LCS, coin change)
- Implement merge sort and quicksort with analysis
- Pass any college DSA exam in any university

---

## 📚 PREREQUISITE

Level 1 passed.

---

## 🧱 CURRICULUM (16 Modules, ~200 hours)

### Module 2.1 — Recursion Mastery & Backtracking (12 hours)

**Concepts:**
- Backtracking template:
```
void backtrack(state) {
    if (is_solution(state)) record(state);
    else for each choice c: 
        if valid(c): make_choice(c); backtrack(state); undo(c);
}
```

**Problems (15):**
1. N-Queens
2. Sudoku solver
3. Word search (board)
4. Permutations / combinations / subsets (revisit deeply)
5. Combination sum I, II, III
6. Palindrome partitioning
7. Restore IP addresses
8. Word break (with backtracking; later DP)
9. Generate parentheses
10. Letter case permutation
11. Knight's tour
12. Rat in a maze
13. M-coloring problem
14. Word ladder (preview — uses BFS)
15. Subsets with sum K

---

### Module 2.2 — Sorting Algorithms (10 hours)

**Implement from scratch & analyze:**

1. **Merge Sort** — O(n log n), stable, O(n) extra space
   - The recurrence: T(n) = 2T(n/2) + O(n)
   - Master Theorem: O(n log n)
   - Use case: external sorting, linked lists

2. **Quick Sort** — O(n log n) avg, O(n²) worst
   - Pivot strategies: first, last, random, median-of-three
   - In-place, not stable (typically)
   - Why is randomized pivot critical?

3. **Heap Sort** — O(n log n) worst, in-place, not stable
   - Build heap O(n), then n × extract-max O(log n)

4. **Counting Sort** — O(n + k), stable, requires bounded integers
5. **Radix Sort** — O(d × (n + k))
6. **Bucket Sort** — O(n) average for uniform distribution

**Compare on a table:**
| Algorithm | Best   | Avg    | Worst  | Space | Stable |
|-----------|--------|--------|--------|-------|--------|
| Merge     | nlogn  | nlogn  | nlogn  | n     | Yes    |
| Quick     | nlogn  | nlogn  | n²     | logn  | No     |
| Heap      | nlogn  | nlogn  | nlogn  | 1     | No     |
| Counting  | n+k    | n+k    | n+k    | k     | Yes    |

**Problems (8):**
1. Sort 0s, 1s, 2s (Dutch flag — already done; revisit with quicksort partition)
2. Inversions in array (using merge sort) — O(n log n) instead of O(n²)
3. Count smaller numbers after self
4. Reverse pairs
5. Maximum gap (using bucket sort)
6. Wiggle sort
7. K closest points to origin (using quickselect — O(n) average!)
8. Kth largest element (quickselect)

---

### Module 2.3 — Trees Foundation (15 hours)

**Concepts:**
- Tree = connected acyclic graph
- Binary tree: each node has ≤2 children
- Tree traversals: preorder, inorder, postorder, level-order
- Recursive vs iterative implementations

**Implementations:**
- Tree node struct
- All 4 traversals (recursive AND iterative — iterative inorder using stack is critical)
- Compute height, count nodes, count leaves, diameter

**Problems (15):**
1. Inorder/preorder/postorder/level-order traversal
2. Maximum depth of binary tree
3. Symmetric tree
4. Same tree
5. Invert binary tree
6. Diameter of binary tree
7. Lowest common ancestor (general binary tree)
8. Path sum I, II, III
9. Binary tree maximum path sum (HARD — non-trivial DP on trees)
10. Right side view
11. Top view, bottom view
12. Vertical order traversal
13. Boundary traversal
14. Construct binary tree from preorder + inorder
15. Construct binary tree from postorder + inorder

---

### Module 2.4 — Binary Search Trees (10 hours)

**Concepts:**
- BST property: left subtree < node < right subtree
- Search, insert, delete in O(h)
- Inorder traversal yields sorted sequence
- Successor / predecessor

**Implementations:**
- Insert, delete (3 cases for delete)
- Find min/max
- Find Kth smallest (inorder counter)

**Problems (10):**
1. Validate BST
2. Lowest common ancestor in BST (O(h))
3. Kth smallest in BST
4. Convert sorted array to BST
5. Convert sorted linked list to BST
6. Recover BST (two nodes swapped)
7. Find inorder successor
8. Range sum of BST
9. Trim BST
10. Two-sum in BST

**Important caveat**: BSTs become useless without balancing. We cover AVL & Red-Black at Level 3.

---

### Module 2.5 — Heaps & Priority Queues (8 hours)

**Concepts:**
- Heap = complete binary tree with heap property
- Min-heap: parent ≤ children. Max-heap: parent ≥ children.
- Array representation: parent at i, children at 2i+1, 2i+2
- Operations:
  - Insert: O(log n) — bubble up
  - Extract min/max: O(log n) — bubble down
  - Peek: O(1)
  - Build heap: O(n)
  - Heap sort: O(n log n)

**Languages:**
- C++: `priority_queue<int>` (max-heap by default), `priority_queue<int, vector<int>, greater<int>>` (min-heap)
- Python: `heapq` (min-heap only; negate for max-heap)
- Java: `PriorityQueue<Integer>` (min-heap by default)

**Problems (12):**
1. Implement a min-heap from scratch
2. Kth largest element in array
3. Top K frequent elements
4. Find median from data stream (TWO HEAPS — classic!)
5. Merge K sorted lists
6. Sort characters by frequency
7. Reorganize string
8. Last stone weight
9. K closest points to origin
10. Task scheduler
11. Network delay time (preview Dijkstra)
12. Trapping rain water II (2D, uses min-heap)

---

### Module 2.6 — Graph Foundations (15 hours)

**Concepts:**
- Graph = (V, E)
- Directed vs undirected
- Weighted vs unweighted
- Cyclic vs acyclic (DAG)
- Connected components
- Representations:
  - Adjacency matrix: O(V²) space, O(1) edge query
  - Adjacency list: O(V+E) space, O(degree) edge query
  - Edge list: O(E) space, often sorted by weight (for Kruskal)

**Implementations:**
```cpp
// Adjacency list for unweighted
vector<vector<int>> adj(n);
adj[u].push_back(v);
adj[v].push_back(u); // if undirected

// Adjacency list for weighted
vector<vector<pair<int,int>>> adj(n); // {neighbor, weight}
adj[u].push_back({v, w});
```

**Algorithms in this module:**
1. **BFS** — O(V+E), shortest path in unweighted graph
2. **DFS** — O(V+E), used for components, cycles, topological sort
3. **Topological Sort** (Kahn's algorithm + DFS-based)
4. **Cycle detection** (undirected: DFS + parent; directed: DFS + 3-color)
5. **Connected components** (DFS/BFS/Union-Find)
6. **Bipartite check** (BFS 2-coloring)

**Problems (15):**
1. Number of islands (DFS)
2. Surrounded regions
3. Pacific Atlantic water flow
4. Course schedule I, II (topological sort)
5. Number of connected components
6. Clone graph
7. Word ladder (BFS shortest path)
8. Rotting oranges (multi-source BFS)
9. Walls and gates
10. 01 matrix (BFS)
11. Bipartite check
12. All paths from source to target (DFS in DAG)
13. Find eventual safe states
14. Network delay time (Dijkstra preview)
15. Cheapest flights within k stops (Bellman-Ford preview)

---

### Module 2.7 — Dijkstra's Algorithm (6 hours)

**Concepts:**
- Single-source shortest path with non-negative weights
- Greedy: always extract closest unvisited node
- Implementation with priority queue: O((V+E) log V)

**Implementation:**
```cpp
vector<int> dijkstra(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<int> dist(n, INT_MAX);
    dist[src] = 0;
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

**Problems (6):**
1. Network delay time
2. Path with maximum probability (variant)
3. Cheapest flights within k stops
4. Shortest path in a grid with obstacles
5. Minimum cost to connect points (preview — needs MST!)
6. Swim in rising water (binary search + Dijkstra)

---

### Module 2.8 — Union-Find / DSU (8 hours)

**Concepts:**
- Disjoint Set Union: track connected components dynamically
- Operations:
  - `find(x)` — find representative of x's set
  - `union(x, y)` — merge two sets
- Optimizations: path compression + union by rank → α(n) amortized (essentially O(1))

**Implementation (canonical):**
```cpp
struct DSU {
    vector<int> parent, rank_;
    DSU(int n) : parent(n), rank_(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;
        if (rank_[x] < rank_[y]) swap(x, y);
        parent[y] = x;
        if (rank_[x] == rank_[y]) rank_[x]++;
        return true;
    }
};
```

**Problems (10):**
1. Number of connected components
2. Number of provinces
3. Redundant connection
4. Accounts merge
5. Most stones removed with same row/column
6. Number of operations to make network connected
7. Smallest string with swaps
8. Satisfiability of equality equations
9. Earliest moment when everyone become friends
10. Minimum cost to connect all points (Kruskal's MST)

---

### Module 2.9 — Minimum Spanning Tree (4 hours)

**Concepts:**
- MST: subset of edges connecting all vertices with minimum total weight
- **Kruskal's**: sort edges, greedily pick using DSU. O(E log E).
- **Prim's**: grow tree from a starting vertex using priority queue. O((V+E) log V).

**Problems (4):**
1. Connecting cities with min cost (classic Kruskal)
2. Min cost to connect all points (Prim or Kruskal)
3. Optimize water distribution
4. Find critical and pseudo-critical edges in MST

---

### Module 2.10 — Dynamic Programming Foundations (20 hours)

**Concepts:**
- DP = recursion + memoization (or tabulation)
- Two requirements:
  1. **Optimal substructure** (solution to problem composed of solutions to subproblems)
  2. **Overlapping subproblems** (same subproblem solved multiple times)
- Top-down (memoization) vs bottom-up (tabulation)
- Space optimization (rolling arrays)

**The 5-step DP framework:**
1. Define **state** (`dp[i]` means what?)
2. Define **transition** (`dp[i] = f(dp[i-1], ...)`)
3. Define **base case**
4. Determine **order of computation**
5. **Final answer** location

**Classic DP Problems (25):**

#### 1D DP:
1. Climbing stairs
2. House robber I, II
3. Longest increasing subsequence (O(n²) basic)
4. Word break
5. Decode ways
6. Maximum sum non-adjacent
7. Min cost climbing stairs
8. Fibonacci variations
9. Number of dice rolls with target sum
10. Best time to buy/sell stock with cooldown

#### 2D DP / Grid:
11. Unique paths I, II
12. Minimum path sum
13. Edit distance
14. Longest common subsequence (LCS)
15. Distinct subsequences
16. Interleaving string
17. Minimum falling path sum

#### Knapsack family:
18. 0/1 Knapsack
19. Subset sum
20. Partition equal subset sum
21. Target sum
22. Coin change I (min coins)
23. Coin change II (number of ways) — note: order of loops!
24. Last stone weight II

#### Strings:
25. Longest palindromic subsequence

---

### Module 2.11 — Bit Manipulation (6 hours)

**Concepts:**
- Bitwise operators: `&`, `|`, `^`, `~`, `<<`, `>>`
- Common tricks:
  - Check if bit is set: `n & (1 << i)`
  - Set bit: `n |= (1 << i)`
  - Clear bit: `n &= ~(1 << i)`
  - Toggle bit: `n ^= (1 << i)`
  - Count set bits: `__builtin_popcount(n)` (C++)
  - Lowest set bit: `n & -n`
  - Clear lowest set bit: `n & (n-1)`
  - Power of 2 check: `n && !(n & (n-1))`
  - XOR cancellation: `a ^ a = 0`, `a ^ 0 = a`

**Problems (10):**
1. Single number (XOR all)
2. Single number II (every element thrice except one)
3. Single number III (two unique)
4. Number of 1 bits
5. Counting bits (DP)
6. Reverse bits
7. Missing number (XOR trick)
8. Sum of two integers without `+` operator
9. Power of two / four
10. Subsets using bitmask

---

### Module 2.12 — Greedy Algorithms (8 hours)

**Concepts:**
- Greedy = make locally optimal choice at each step
- Works ONLY when **greedy choice property** + **optimal substructure** hold
- Must PROVE correctness (exchange argument typically)

**Classic Greedy Problems (10):**
1. Activity selection problem
2. Fractional knapsack
3. Job sequencing with deadlines
4. Huffman coding
5. Minimum number of coins (only for canonical coin systems!)
6. Gas station (circular tour)
7. Jump game I, II
8. Minimum platforms (railway station)
9. Candy distribution
10. Non-overlapping intervals

---

### Module 2.13 — Trie (4 hours)

**Concepts:**
- Trie = prefix tree
- Each node has children (typically array of 26 for lowercase letters or hashmap)
- Operations: insert, search, startsWith — all O(L) where L = string length

**Implementation:**
```cpp
struct TrieNode {
    TrieNode* children[26] = {};
    bool isEnd = false;
};

void insert(TrieNode* root, string& word) {
    TrieNode* cur = root;
    for (char c : word) {
        int idx = c - 'a';
        if (!cur->children[idx]) cur->children[idx] = new TrieNode();
        cur = cur->children[idx];
    }
    cur->isEnd = true;
}

bool search(TrieNode* root, string& word) {
    TrieNode* cur = root;
    for (char c : word) {
        int idx = c - 'a';
        if (!cur->children[idx]) return false;
        cur = cur->children[idx];
    }
    return cur->isEnd;
}
```

**Problems (5):**
1. Implement Trie
2. Word search II (board + dictionary)
3. Replace words
4. Design add and search words data structure (with `.` wildcard)
5. Maximum XOR of two numbers in array (using bit trie)

---

### Module 2.14 — Math Essentials (8 hours)

**Concepts:**
1. **GCD/LCM** (Euclidean algorithm, O(log(min)))
2. **Modular arithmetic** basics (`a + b mod m`, `a * b mod m`)
3. **Fast exponentiation** (binary exponentiation, O(log n))
4. **Modular inverse** (using Fermat's little theorem when m is prime)
5. **Sieve of Eratosthenes** (O(n log log n) for primes up to n)
6. **Factorization** (O(√n) trial division)

**Problems (8):**
1. Power of 2/3/4
2. Pow(x, n) — fast exponentiation
3. Sqrt(x) — using BS or Newton's
4. Excel sheet column number
5. Count primes (sieve)
6. Happy number
7. Greatest common divisor of strings
8. Modular exponentiation (homemade)

---

### Module 2.15 — Two Pointers & Sliding Window (Advanced) (6 hours)

**Patterns:**
- Fixed-size window
- Variable-size window with constraint
- Two-pointer (opposite ends)

**Problems (12):**
1. Longest substring with at most K distinct characters
2. Longest substring without repeating
3. Minimum window substring (HARD — must master)
4. Sliding window maximum
5. Permutation in string
6. Find all anagrams in string
7. Subarrays with K different integers
8. Longest repeating character replacement
9. Fruit into baskets
10. Maximum average subarray
11. Minimum size subarray sum
12. Subarray product less than K

---

### Module 2.16 — Practice Marathon (15 hours)

**[LeetCode](https://leetcode.com) targets**:
- 50 more Mediums (any topic)
- 10 Hards (your choice)

**[Codeforces](https://codeforces.com)**:
- Solve 30 problems rated 800-1200

---

## 📊 PROBLEM VOLUME

- ~150 structured problems
- **Cumulative goal**: 350 LeetCode + 50 Codeforces

---

## ⏱️ ESTIMATED TIME

- 200 hours
- ~5 months at 10 hours/week
- ~2 months at 25 hours/week

---

## ✅ EXIT TEST

In 3 hours, no references:

1. Implement merge sort.
2. Implement BFS and DFS on adjacency list.
3. Implement Dijkstra's algorithm.
4. Implement DSU with path compression + union by rank.
5. Solve [LC 322: Coin Change](https://leetcode.com/problems/coin-change) with both memoization and tabulation.
6. Solve [LC 207: Course Schedule](https://leetcode.com/problems/course-schedule).
7. Solve [LC 295: Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream).
8. Explain why DP requires "overlapping subproblems."
9. State and explain the time complexity of: BFS, Dijkstra, Kruskal, Quicksort.

**Pass**: 7/9.

---

## 📌 RESOURCES

### Books
- **Introduction to Algorithms (CLRS)** — Cormen, Leiserson, Rivest, Stein (Chapters 1-13)
- **Algorithms** — Sedgewick & Wayne
- **Algorithm Design** — Kleinberg & Tardos

### Courses
- **[MIT 6.006](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) — Introduction to Algorithms** (OCW, free) ⭐
- **Stanford CS161 — Design and Analysis of Algorithms**
- **Princeton Algorithms** (Sedgewick) on Coursera

### YouTube
- **Take U Forward** — Striver's complete graphs + DP playlists ⭐
- **[Aditya Verma](https://www.youtube.com/@AdityaVermaTheProgrammingLord)** — DP playlist (best in India)
- **[William Fiset](https://www.youtube.com/@WilliamFiset-videos)** — Graph theory playlist (gold)
- **[Abdul Bari](https://www.youtube.com/@abdul_bari)** — Algorithm fundamentals

### Practice
- **Striver A2Z Sheet** (medium-hard track)
- **Striver SDE Sheet** (180 problems)
- **[NeetCode](https://neetcode.io) 150**
- **Codeforces** — Rated rounds, Div 3 + 4

---

## 🚀 ON COMPLETION

You are now an "academically qualified" programmer. You can pass college DSA exams and basic interviews.

**→ Proceed to:** [`Level-03-Placement-DSA.md`](./Level-03-Placement-DSA.md)
