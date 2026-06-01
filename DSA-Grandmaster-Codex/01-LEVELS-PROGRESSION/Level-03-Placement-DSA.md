# 🎯 Level 3 — Placement DSA (The Job-Ready Engineer)

> *"You can think. Now think under pressure, with a story."*

---

## 🎯 OUTCOME

You can:
- Crack tier-1 Indian product company interviews (Flipkart, Paytm, Zomato, MakeMyTrip, Swiggy)
- Crack mid-level startup interviews
- Communicate solutions clearly under whiteboard pressure
- Solve 80% of [LeetCode](https://leetcode.com) Mediums in <30 minutes
- Solve 30% of LeetCode Hards in <60 minutes

---

## 📚 PREREQUISITE

Level 2 passed.

---

## 🧱 CURRICULUM (12 Modules, ~250 hours)

### Module 3.1 — Advanced Recursion & Backtracking (15 hours)

Beyond Level 2: now we deal with **state-space explosion** carefully.

**Patterns to master:**
- Subset selection with constraints
- Permutation with branches pruned
- Tree of choices with early termination
- Iterative deepening (preview)

**Problems (15):**
1. Combination sum III, IV
2. Word break II (return all sentences)
3. Word ladder II (return all shortest paths)
4. Expression add operators
5. Remove invalid parentheses
6. Beautiful arrangement
7. Letter tile possibilities
8. Sudoku solver (revisit; with optimization)
9. N-Queens II (count, no return)
10. Verbal arithmetic puzzle
11. Increasing subsequences
12. Number of squareful arrays
13. Maximum length of concatenated string
14. Partition to K equal subsets
15. Matchsticks to square

---

### Module 3.2 — Dynamic Programming Mastery (Part 1) (25 hours)

**Categorization:**
1. **1D DP**: state = position
2. **2D DP**: state = (i, j) — for grids, intervals, two strings
3. **DP on subsequences**: pick/not-pick
4. **DP on substrings**: i, j as boundaries
5. **DP on stocks**: state with cooldown / transactions
6. **DP with state machine**: e.g., paint house

**Problems (30):**

#### LIS family:
1. Longest increasing subsequence — O(n²) and O(n log n) (patience sorting)
2. Longest divisible subset
3. Number of LIS
4. Russian doll envelopes
5. Maximum sum increasing subsequence

#### LCS family:
6. Longest common subsequence
7. Longest common substring
8. Shortest common supersequence
9. Edit distance
10. Distinct subsequences
11. Wildcard matching
12. Regular expression matching

#### Stocks:
13. Best time to buy/sell stock I, II, III, IV
14. Best time with cooldown
15. Best time with transaction fee

#### Partition / Interval DP:
16. Matrix chain multiplication
17. Burst balloons (HARD — interval DP)
18. Min cost to cut stick
19. Palindrome partitioning II (min cuts)
20. Boolean parenthesization

#### State machine:
21. Paint house I, II
22. Paint fence
23. Knight dialer
24. Domino and tromino tiling

#### Tree DP (preview):
25. House robber III (tree)
26. Diameter of binary tree
27. Binary tree maximum path sum
28. Sum of distances in tree
29. Longest path in tree

#### Bonus:
30. Minimum cost for tickets

---

### Module 3.3 — Graph Algorithms (Advanced) (15 hours)

**New algorithms:**
1. **Bellman-Ford** — handles negative weights, O(VE), detects negative cycle
2. **Floyd-Warshall** — all-pairs shortest path, O(V³)
3. **0-1 BFS** — when weights are only 0 or 1, use deque, O(V+E)
4. **Multi-source BFS** — start from multiple sources simultaneously
5. **Topological sort + DP** — DAG longest/shortest path
6. **Cycle detection** — directed (3-color), undirected (parent), counting cycles

**Problems (15):**
1. Cheapest flights with K stops (Bellman-Ford bounded)
2. Currency arbitrage detection (Bellman-Ford)
3. Floyd-Warshall: count cities with smallest reachable
4. 01 matrix (0-1 BFS or BFS)
5. Path with min effort (Dijkstra variant)
6. Shortest path visiting all nodes (BFS + bitmask, preview)
7. Critical edges & nodes (bridges, articulation points — preview)
8. Reconstruct itinerary (Hierholzer's for Eulerian — preview)
9. Network delay time (Dijkstra/BF)
10. Find the city with smallest number of neighbors at threshold
11. Minimum cost to make at least one valid path
12. Path with maximum minimum value
13. Swim in rising water
14. Bus routes (BFS on routes, not stops)
15. Sliding puzzle (BFS on states)

---

### Module 3.4 — Trees Mastery (15 hours)

**Concepts:**
- Tree DP (general)
- LCA (binary lifting — preview)
- Euler tour
- Re-rooting technique

**Problems (15):**
1. Diameter of binary tree (revisit, full proof)
2. Maximum path sum (binary tree)
3. House robber III (tree DP)
4. Sum of distances in tree (re-rooting)
5. Longest univalue path
6. Binary tree maximum width
7. Serialize and deserialize binary tree
8. Construct from preorder + postorder
9. All nodes at distance K
10. Vertical order traversal
11. Minimum number of cameras (greedy + tree)
12. Smallest subtree with all deepest nodes
13. Count complete tree nodes (O(log² n))
14. Find leaves of binary tree
15. Tree of coprimes (LCA + colored ancestor problem)

---

### Module 3.5 — Heaps Advanced (8 hours)

**Patterns:**
- "Top K" anything
- "K-way merge"
- "Median in stream"
- "Schedule with priority"

**Problems (10):**
1. Find K pairs with smallest sums
2. Kth smallest element in sorted matrix
3. Smallest range covering elements from K lists
4. Find K closest elements
5. Sliding window median
6. IPO
7. Minimize deviation in array
8. Furthest building you can reach
9. Process tasks using servers
10. Single-threaded CPU

---

### Module 3.6 — Stack Mastery (Monotonic) (10 hours)

**The Monotonic Stack/Queue Pattern:**
> *Maintain a stack where elements are monotonically increasing or decreasing. When pushing a new element, pop elements that violate the property — these "popped" elements have found their answer.*

**Use cases:**
- Next greater / smaller element
- Largest rectangle in histogram
- Maximum rectangle in binary matrix
- Stock span
- Sliding window maximum (deque variant)

**Problems (12):**
1. Daily temperatures
2. Next greater element I, II, III
3. Stock span problem
4. Largest rectangle in histogram (CLASSIC)
5. Maximal rectangle (2D extension)
6. Trapping rain water (also doable with two pointers)
7. Sum of subarray minimums (HARD)
8. Sum of subarray ranges
9. Remove K digits
10. Maximum binary tree
11. 132 pattern
12. Constrained subsequence sum

---

### Module 3.7 — Binary Search Mastery (8 hours)

**Beyond sorted arrays:**
- Binary search on **answer** (when monotonic predicate)
- Binary search on **range** (real numbers — bisection)
- Binary search on **2D** (matrix)

**Problems (12):**
1. Search in rotated sorted array
2. Find minimum in rotated sorted array
3. Search a 2D matrix I, II
4. Find peak element
5. Median of two sorted arrays (HARD)
6. Capacity to ship packages within D days
7. Koko eating bananas
8. Aggressive cows ([SPOJ](https://www.spoj.com) classic)
9. Allocate minimum number of pages
10. Split array largest sum
11. Minimum days to make M bouquets
12. Find the smallest divisor given threshold

**The "Binary Search on Answer" Template:**
```cpp
int lo = MIN_POSSIBLE, hi = MAX_POSSIBLE;
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;
    if (canDoIt(mid)) hi = mid;  // we want smallest valid
    else lo = mid + 1;
}
return lo;
```

---

### Module 3.8 — String Algorithms Foundation (10 hours)

**Patterns:**
- Pattern matching (naive, Rabin-Karp, KMP — Level 4)
- Palindrome detection (expand-around-center, Manacher's — Level 4)
- String DP (already in DP module)

**Problems (12):**
1. Implement strStr (naive O(nm))
2. Repeated substring pattern
3. Longest palindromic substring
4. Palindromic substrings (count)
5. Palindrome partitioning
6. Word break I, II
7. Longest valid parentheses
8. Decode ways I, II
9. Roman to integer
10. ZigZag conversion
11. Multiply strings (no built-in big-int)
12. Add strings

---

### Module 3.9 — Sliding Window Hard (5 hours)

**Problems (8):**
1. Minimum window substring
2. Substring with concatenation of all words
3. Longest substring with at most 2 distinct characters
4. Get equal substrings within budget
5. Maximum points you can obtain from cards
6. Subarrays with K different integers
7. Count number of nice subarrays
8. Replace the substring for balanced string

---

### Module 3.10 — Design Problems (15 hours)

**Patterns**: combine DSes into custom systems.

**Problems (12):**
1. LRU cache (HashMap + Doubly Linked List)
2. LFU cache
3. Implement Trie
4. Min stack
5. Max stack
6. Time-based key-value store
7. Insert delete getRandom O(1) (HashMap + Vector)
8. Insert delete getRandom O(1) duplicates allowed
9. Design Twitter
10. Design hit counter
11. Design tic-tac-toe
12. Design parking system / phone directory / underground system

---

### Module 3.11 — Mathematical Problems (10 hours)

**Problems (12):**
1. Reverse integer (overflow careful!)
2. String to integer (atoi)
3. Pow(x, n) (binary exp)
4. Excel sheet column title/number
5. Sqrt(x) (BS or Newton)
6. Happy number
7. Count primes (sieve)
8. Plus one
9. Add binary
10. Permutation sequence (factorial number system)
11. Fraction to recurring decimal (HASH MAP!)
12. Basic calculator I, II

---

### Module 3.12 — Mock Interview Marathon (15 hours)

**Strategy:**
- 5 mock interviews on [Pramp](https://www.pramp.com) / [interviewing.io](https://interviewing.io) with random pairs
- 5 timed self-mocks: random LC Medium, 30 min, narrate aloud
- 3 system-design lite (LRU cache, hit counter, etc.)

**Speak as you code:**
1. Restate the problem.
2. Provide examples (especially edge cases).
3. State brute force, complexity.
4. Identify bottleneck.
5. Propose optimization.
6. Code while narrating.
7. Test on given example + edge cases.
8. Discuss complexity, alternatives.

---

## 📊 PROBLEM VOLUME

- ~180 structured problems
- **Cumulative**: 500+ LeetCode + 100+ [Codeforces](https://codeforces.com)

---

## ⏱️ ESTIMATED TIME

- 250 hours
- ~6 months at 10 hours/week
- ~2.5 months at 25 hours/week

---

## ✅ EXIT TEST

In 4 hours, no references — *under interview-style pressure*:

1. [LC 76: Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring) — solve & explain.
2. [LC 84: Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram).
3. [LC 124: Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum).
4. [LC 23: Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists).
5. [LC 146: LRU Cache](https://leetcode.com/problems/lru-cache).
6. [LC 72: Edit Distance](https://leetcode.com/problems/edit-distance).
7. Mock interview walkthrough of any Medium problem in 25 minutes — narrated.

**Pass**: 5/7 + good narration on the mock.

---

## 📌 RESOURCES

### Sheets
- **Striver SDE Sheet** (180 problems) ⭐
- **[NeetCode](https://neetcode.io) 150** ⭐
- **Blind 75**
- **LeetCode Top Interview 150**

### Books
- **Cracking the Coding Interview** (Gayle McDowell) — full read
- **Elements of Programming Interviews** (EPI) — your language version

### Mock Interview Platforms
- **Pramp** (free)
- **interviewing.io** (paid but excellent)
- **Excalidraw** for whiteboarding solo

### Channels
- **Take U Forward** — Striver's full SDE sheet videos ⭐
- **NeetCode** — explanations of every Blind 75 + 150 ⭐
- **Kunal Kushwaha** (for Indian audience)
- **[Aditya Verma](https://www.youtube.com/@AdityaVermaTheProgrammingLord)** (DP & recursion gold)

---

## 🚀 ON COMPLETION

You're now ready to crack tier-1 Indian product companies. Most "good enough" software engineers stop here. **You won't.**

**→ Proceed to:** [`Level-04-Product-Based-DSA.md`](./Level-04-Product-Based-DSA.md)