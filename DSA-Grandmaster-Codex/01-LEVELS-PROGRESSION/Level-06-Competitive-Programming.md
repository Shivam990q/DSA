# ⚔️ Level 6 — Competitive Programming (The Codeforces Warrior)

> *"Speed is correctness compounded by intuition."*

---

## 🎯 OUTCOME

You can:
- Achieve **Codeforces Specialist (1400-1599)** → **Expert (1600-1899)** rating
- Reach **[AtCoder](https://atcoder.jp) Brown / Green** rating
- Solve Div 2 Problem D consistently in contests
- Qualify for **ICPC regionals**
- Implement advanced data structures from scratch under time pressure
- Read and apply editorials from any problem on [CP-Algorithms.com](https://cp-algorithms.com)

---

## 📚 PREREQUISITE

Level 5 passed. (Or: Level 4 + dedicated CP focus)

---

## 🧱 CURRICULUM (15 Modules, ~600 hours)

### Module 6.1 — Setup CP Environment (4 hours)

**Tools:**
- C++17/20 with `g++` and `-O2 -std=c++17`
- Competitive Companion browser extension (parses problems)
- A debug template (e.g., `dbg(x)` macro)
- Stress-test setup (`gen.cpp`, `brute.cpp`, `solve.cpp`, comparison script)

**My CP template skeleton** (provided in `19-TEMPLATES-AND-IMPLEMENTATIONS/competitive-programming-template.cpp`):

```cpp
#include <bits/stdc++.h>
using namespace std;
#define int long long
#define vi vector<int>
#define pii pair<int,int>
#define all(x) (x).begin(), (x).end()
#define rep(i, a, b) for (int i = a; i < (b); i++)

void solve() {
    // problem code
}

int32_t main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t = 1;
    cin >> t;
    while (t--) solve();
}
```

---

### Module 6.2 — Number Theory Deep (25 hours)

**Topics:**
1. Modular inverse via Extended Euclidean
2. Linear sieve (smallest prime factor in O(n))
3. Multiplicative functions (φ, μ, σ, τ)
4. Möbius function & Möbius inversion
5. Chinese Remainder Theorem
6. Discrete logarithm (baby-step giant-step)
7. Primality testing: Miller-Rabin
8. Integer factorization: Pollard's rho
9. Lucas theorem (nCr mod prime)
10. Wilson's theorem
11. Fermat's little theorem & generalizations

**Problems (15):** From CF tags `number-theory`, rating 1500-2000.
- CF 1295D, 1499D, 1542C, 1542D2, 1499E1
- AtCoder ABC ranges around C-E in number theory

---

### Module 6.3 — Combinatorics (15 hours)

**Topics:**
1. Permutations, combinations (with/without repetition)
2. Stars and bars
3. Inclusion-exclusion
4. Catalan numbers (5+ formulas)
5. Stirling numbers (1st & 2nd kind)
6. Bell numbers
7. Lucas theorem
8. Burnside's lemma (basic)
9. Generating functions (basic)

**Problems (12):** CF/AtCoder around 1500-2000 rating, combinatorics-tagged.

---

### Module 6.4 — Advanced Graphs (30 hours)

**Topics:**
1. **Dijkstra variations** (with state, on grids, with constraints)
2. **0-1 BFS** (deque-based)
3. **SPFA** (queue-based Bellman-Ford, careful — can TLE on adversarial)
4. **Bridges & Articulation Points** (Tarjan's, deep)
5. **SCC** (Tarjan's & Kosaraju's, deep)
6. **2-SAT** (using SCC)
7. **Eulerian path/circuit** (Hierholzer's)
8. **Maximum bipartite matching** (Kuhn's, Hopcroft-Karp)
9. **Maximum flow** (Ford-Fulkerson, Edmonds-Karp, Dinic's)
10. **Min-cut max-flow theorem**
11. **Min-cost max-flow** (SPFA-based)
12. **LCA** (binary lifting, Euler tour + RMQ)
13. **Tree center, centroid, centroid decomposition**
14. **Heavy-Light Decomposition** (preview — full at Level 7)
15. **Small-to-large merging on trees**

**Problems (25):** Curated CF graph problems 1700-2200.

---

### Module 6.5 — Segment Tree Mastery (25 hours)

**Topics:**
1. Iterative segment tree (cache-friendly, fast)
2. Lazy propagation (range update + range query)
3. Segment tree with structs (max + count, etc.)
4. Persistent segment tree (preview)
5. Merge sort tree
6. Segment tree beats (preview)
7. Segment tree on tree (with HLD or Euler tour)
8. 2D segment tree (preview)

**Lazy Propagation Template:**
```cpp
struct LazySegTree {
    int n;
    vector<long long> tree, lazy;
    
    void push(int node, int start, int end) {
        if (lazy[node]) {
            tree[node] += lazy[node] * (end - start + 1);
            if (start != end) {
                lazy[2*node] += lazy[node];
                lazy[2*node+1] += lazy[node];
            }
            lazy[node] = 0;
        }
    }
    
    void update(int node, int start, int end, int l, int r, long long val) {
        push(node, start, end);
        if (r < start || end < l) return;
        if (l <= start && end <= r) {
            lazy[node] += val;
            push(node, start, end);
            return;
        }
        int mid = (start + end) / 2;
        update(2*node, start, mid, l, r, val);
        update(2*node+1, mid+1, end, l, r, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    long long query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        push(node, start, end);
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return query(2*node, start, mid, l, r) + query(2*node+1, mid+1, end, l, r);
    }
public:
    LazySegTree(int n) : n(n), tree(4 * n), lazy(4 * n) {}
};
```

**Problems (15):** Range update, range query problems on CF.

---

### Module 6.6 — DP Mastery (Part 3) — Optimizations (30 hours)

**Topics:**
1. **Knuth's optimization** (for problems with quadrangle inequality)
2. **Divide & Conquer DP** (when opt(i) ≤ opt(i+1))
3. **Convex Hull Trick (CHT)** — for DP with linear functions
4. **Li Chao Tree** — generalization of CHT
5. **Aliens trick** (Lagrangian relaxation)
6. **SOS DP** (sum over subsets) — O(n·2ⁿ)
7. **Profile DP** (broken profile)

**Problems (15):** From IOI archive, AtCoder [Educational DP Contest](https://atcoder.jp/contests/dp), CF.

---

### Module 6.7 — String Algorithms (Advanced) (25 hours)

**Topics:**
1. **Suffix Array + LCP array** (O(n log² n) and O(n log n))
2. **Suffix Automaton** (linear-time, online construction)
3. **Aho-Corasick** (multiple pattern matching)
4. **Palindromic Tree (Eertree)**
5. **Hashing** (single & double, anti-hash strategies)
6. **Z-function applications**
7. **String DP**

**Problems (15):**
- Suffix Array: distinct substrings, longest repeated substring
- Suffix Automaton: number of distinct substrings, occurrences
- Aho-Corasick: word matching in stream
- Eertree: distinct palindromic substrings

---

### Module 6.8 — Geometry Foundation (15 hours)

**Topics:**
1. Vector operations (cross product, dot product)
2. Orientation (CCW/CW/collinear)
3. Line intersection
4. Polygon area (shoelace formula)
5. Point in polygon (ray casting)
6. Convex hull (Graham scan, Andrew monotone chain)
7. Closest pair of points (D&C, O(n log n))
8. Sweep line basics

**Problems (10):** CF/Codechef geometry-tagged.

---

### Module 6.9 — Game Theory (10 hours)

**Topics:**
1. Combinatorial games (impartial)
2. Sprague-Grundy theorem
3. Nim and variants
4. Misère games
5. Games on graphs
6. DP on games

**Problems (10):** Stone game series, CF game-theory tagged.

---

### Module 6.10 — Probability & Expected Value (10 hours)

**Topics:**
1. Linearity of expectation (POWERFUL!)
2. Probability DP
3. Markov chains (basic)
4. Random walks
5. Coupon collector
6. Birthday paradox

**Problems (8):** CF probability-tagged.

---

### Module 6.11 — Bitmask DP & Bit Tricks (15 hours)

**Topics:**
1. Bitmask DP (revisit, deeper)
2. Bitwise tricks: `__builtin_popcount`, `__builtin_ctz`, `__builtin_clz`
3. Bitset for O(n/64) speedup
4. Meet in the middle (n=40)
5. SOS DP (sum over subsets)

**Problems (12):** CF bitmask-tagged at 1700-2100.

---

### Module 6.12 — Square Root Techniques (15 hours)

**Topics:**
1. **Square root decomposition** (block decomposition for arrays)
2. **Mo's algorithm** (offline range queries, O((n+q)·√n))
3. **Mo's on trees** (Euler tour + Mo's)
4. **Heavy & light vertices** (in graphs/trees with degree threshold)

**Problems (10):** Range query problems where segtree is overkill.

---

### Module 6.13 — Constructive Algorithms (15 hours)

This is what separates Specialist from Expert.

**Patterns:**
- Build by induction (handle small cases, generalize)
- Pigeonhole / counting arguments
- Symmetry
- Greedy with proof
- "Find any valid" — multiple solutions exist

**Practice:** 30 CF constructive problems rated 1500-2000. CF tag `constructive-algorithms`.

---

### Module 6.14 — Contest Practice (Heavy) (60 hours)

- **40 Codeforces rounds** (Div 2, virtuals if not live)
- **Upsolve every contest** (the unsolved problems are gold)
- **20 AtCoder Beginner Contests**

Track rating progression. Goal: **Specialist → Expert by end of this module**.

---

### Module 6.15 — Intensive Topical Drilling (30 hours)

Take your 3 weakest topics. For each:
- Read CP-Algorithms.com chapter
- Solve 20 tagged problems
- Write a personal blog/note

---

## 📊 PROBLEM VOLUME

- ~250 structured CP problems
- ~40 contest rounds
- **Cumulative**: 1500+ unique problems

---

## ⏱️ ESTIMATED TIME

- 600 hours
- ~15 months at 10 hours/week
- ~6 months at 25 hours/week

---

## ✅ EXIT TEST

1. Achieve Codeforces **Expert (1600+)** rating sustained for 30 days.
2. Solve a Div 2 D in <40 minutes during a live contest.
3. Implement the following from scratch in <10 minutes each:
   - Dijkstra
   - Segment tree (point update + range sum)
   - DSU
   - Modular inverse (Extended Euclidean)
   - KMP
4. Complete the [CSES Problem Set](https://cses.fi/problemset/) "Sorting and Searching" + "Tree Algorithms" + "Graph Algorithms" sections.

---

## 📌 RESOURCES

### Books
- **[Competitive Programming 4](https://cpbook.net)** (Halim & Halim) — your CP bible
- **[Competitive Programmer's Handbook](https://cses.fi/book/book.pdf)** (Antti Laaksonen) — FREE, complete
- **Guide to Competitive Programming** — Laaksonen (Springer)

### Sites
- **CP-Algorithms.com** ⭐ — encyclopedia of CP algorithms
- **[CSES Problem Set](https://cses.fi/problemset/)** ⭐ — structured, must-do
- **A2OJ Ladders** — structured progression
- **[USACO Guide](https://usaco.guide)** — phenomenal curriculum
- **codeforces.com/edu** — interactive courses

### Practice
- **Codeforces** — Div 2 + Educational rounds + Virtual contests
- **AtCoder** — ABC, ARC
- **[CodeChef](https://www.codechef.com)** — Long Challenge, Cookoff
- **[HackerEarth](https://www.hackerearth.com)** — competitive monthly contests

### Channels
- **[Errichto](https://www.youtube.com/@Errichto)** ⭐ — best CP teacher on YouTube
- **[William Lin](https://www.youtube.com/@tmwilliamlin168)** — IOI gold's perspective
- **Algorithms Live!** (Stephen Grady) — long-form CP
- **[SecondThread](https://www.youtube.com/@SecondThread)** — explained CP
- **Tourist** — for inspiration (his streams)

### Communities
- **Codeforces Blog** — daily discussions, editorials
- **r/CompetitiveProgramming**
- **CP Discord servers**

---

## 🚀 ON COMPLETION

You're a Codeforces Expert. ICPC Regionals are within reach. The competitive bug has bitten you.

**→ Proceed to:** [`Level-07-Elite-CP.md`](./Level-07-Elite-CP.md)
