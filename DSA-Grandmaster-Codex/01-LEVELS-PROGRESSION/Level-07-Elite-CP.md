# 🌌 Level 7 — Elite Competitive Programming (The Grandmaster Aspirant)

> *"The ordinary problem yields to study. The legendary problem yields only to obsession."*

---

## 🎯 OUTCOME

You can:
- Achieve **[Codeforces](https://codeforces.com) Candidate Master (1900) → Master (2100) → International Master (2300) → Grandmaster (2400+)**
- Achieve **[AtCoder](https://atcoder.jp) Yellow / Orange / Red**
- Reach **ICPC World Finals**
- Solve Div 1 Problem D-E in contests
- Implement the entire [CP-Algorithms](https://cp-algorithms.com) library from memory under time pressure

---

## 📚 PREREQUISITE

Level 6 passed. CF Expert (1600+) sustained.

---

## 🧱 CURRICULUM (15 Modules, ~1000 hours)

### Module 7.1 — Heavy-Light Decomposition (HLD) (15 hours)

**Concept**: decompose tree into chains; each path on tree intersects O(log n) chains; segment tree per chain.

Operations on tree paths in O(log² n).

**Problems (8):** Path sum on tree, path max, path update, etc.

---

### Module 7.2 — Centroid Decomposition (15 hours)

**Concept**: recursively pick tree centroid; gives a "log n levels" structure for path queries.

**Problems (8):** Tree problems requiring path queries with O(n log² n).

---

### Module 7.3 — Persistent Data Structures (20 hours)

**Topics:**
1. Persistent segment tree
2. Persistent array
3. Persistent trie
4. Persistent stacks/queues

**Use cases**: Kth-smallest in subarray, version control, offline queries.

**Problems (10):** CF/AtCoder persistent-tagged.

---

### Module 7.4 — Link-Cut Tree (15 hours)

**Concept**: dynamic tree connectivity, splay tree-based, O(log n) amortized operations.

**Problems (5):** Hard tree dynamic connectivity.

---

### Module 7.5 — Treap & Splay Trees (10 hours)

**Topics:**
1. Treap (randomized BST) — implicit treap for sequences
2. Splay tree (amortized O(log n))
3. Operations: split, merge, insert, delete, rotate

**Problems (8):** Sequence operations (reverse subarray, insert at position, etc.).

---

### Module 7.6 — Segment Tree Beats (15 hours)

**Concept**: handle min/max + add range updates in O(n log² n) amortized.

**Use case**: Chtholly tree, range floor/ceiling operations.

**Problems (5):** CF segment-tree-beats problems.

---

### Module 7.7 — FFT / NTT (Polynomial Multiplication) (25 hours)

**Topics:**
1. Discrete Fourier Transform
2. Fast Fourier Transform (Cooley-Tukey)
3. Number Theoretic Transform (modular)
4. Convolutions (sum, XOR, AND, OR)
5. Polynomial inverse, exp, log
6. Multipoint evaluation
7. Linear recurrences via NTT

**Problems (10):** CF/codechef FFT-tagged.

---

### Module 7.8 — Convex Hull Trick (Advanced) & Li Chao (15 hours)

**Topics:**
1. CHT with monotone queries (sorted by slope)
2. CHT with arbitrary queries (Li Chao)
3. CHT in DP optimizations

**Problems (8):** DP problems where transitions form lines.

---

### Module 7.9 — Network Flows (Deep) (25 hours)

**Topics:**
1. Dinic's algorithm — O(V² E)
2. Min-cost max-flow with potentials
3. Bipartite matching → flow reduction
4. Assignment problem (Hungarian algorithm)
5. Project selection problem
6. Edge-disjoint vs vertex-disjoint paths
7. Multi-source multi-sink flows

**Problems (12):** CF, ICPC archives flow problems.

---

### Module 7.10 — 2-SAT & SAT-Reductions (10 hours)

**Topics:**
1. Build implication graph
2. SCC → satisfiability
3. Reductions to 2-SAT

**Problems (6):** Constructive problems with binary choices.

---

### Module 7.11 — Advanced Geometry (20 hours)

**Topics:**
1. Convex hull trick (geometric)
2. Half-plane intersection
3. Voronoi diagrams (basic)
4. Delaunay triangulation
5. Rotating calipers
6. Minimum enclosing circle (Welzl's)
7. Closest pair (D&C in 2D)
8. Polygon clipping

**Problems (10):** ICPC/CF geometry-tagged at 2200+.

---

### Module 7.12 — Advanced Number Theory (15 hours)

**Topics:**
1. Quadratic residues, Legendre symbol
2. Tonelli-Shanks
3. Dirichlet convolutions
4. Möbius inversion (deep)
5. Euler product, Dirichlet series
6. Polynomial multiplication mod prime (NTT)
7. Multiplicative function evaluation

**Problems (8):** AtCoder grand contest, CF round problems on number theory.

---

### Module 7.13 — Constructive & Ad-hoc Mastery (30 hours)

**This is what makes Grandmasters.**

**Patterns:**
- Pattern observation (compute small cases, find regularity)
- Symmetry exploitation
- Greedy with proof by exchange
- Operations preserving invariants
- "Surely it must be ≤ k" arguments

**Practice**: 50 CF problems rated 2200-2700, ad-hoc/constructive tagged.

---

### Module 7.14 — Contest Marathon (200 hours)

- **80 Codeforces rounds** (Div 1 / Div 2 with rating focus)
- **30 AtCoder Regular/Grand Contests**
- **10 ICPC virtual contests** (with team if possible)
- **Upsolve EVERYTHING**

This is the largest time sink. **Show up. Compete. Lose. Upsolve. Repeat.**

---

### Module 7.15 — Reading Editorials & Researcher Mode (50 hours)

**Discipline**: read 1 editorial per day, even of problems you didn't attempt.

**Key blogs/resources:**
- Codeforces editorial archive
- Adamant's blog
- [Errichto](https://www.youtube.com/@Errichto)'s blog
- [KACTL](https://github.com/kth-competitive-programming/kactl) (KTH Algorithm Competition Template Library)
- ProgrammingTeam blog (MIT)

---

## 📊 PROBLEM VOLUME

- ~300 elite problems
- 80+ contest rounds
- **Cumulative**: 2500+ problems

---

## ⏱️ ESTIMATED TIME

- 1000 hours
- ~25 months at 10 hours/week
- ~10 months at 25 hours/week

---

## ✅ EXIT TEST

1. Achieve **Codeforces Master (2100+)** sustained for 60 days.
2. Solve a Div 1 C in <30 minutes during live contest.
3. Implement from scratch in <30 minutes each:
   - HLD with segtree
   - Centroid decomposition
   - Dinic's algorithm
   - FFT
   - Suffix automaton
4. Read and re-implement a top-rated ICPC final problem from any year.

---

## 📌 RESOURCES

### Books
- **[Competitive Programming 4](https://cpbook.net)** (Halim) — every chapter mastered
- **Algorithm Design Manual** (Skiena)
- **Concrete Mathematics** (Knuth, Patashnik, Graham) — math foundation

### Templates / Code Libraries
- **KACTL** ⭐ (KTH) — compact, contest-ready
- **AC Library (AtCoder)**
- **PolyMath** (AtCoder polynomial library)
- **JCantin's CP library**

### Channels
- **Tourist's streams** (rare gems)
- **Um_nik blog & solutions**
- **rng_58's posts** (AtCoder admin)
- **Petr's blog** (legendary)

### Sites
- **[AtCoder DP Contest](https://atcoder.jp/contests/dp)** (Educational DP)
- **[AtCoder Library Practice Contest](https://atcoder.jp/contests/practice2)**
- **Codeforces Edu** (advanced segment trees, etc.)
- **[Project Euler](https://projecteuler.net)** (math + algorithm puzzles)
- **[DMOJ](https://dmoj.ca)**, **Yandex.Algorithm** (alternative sites)

---

## 🚀 ON COMPLETION

You're a Codeforces Master / Candidate Master. ICPC World Finals territory.

You now have a choice:
- **Path A (Industry/Engineering)**: Level 8 (Algorithm Engineering) — apply this in production systems
- **Path B (Research)**: Level 9 (Research-Level Algorithms) — read papers, implement state-of-the-art
- **Path C (Both)**: Walk both. The greatest grandmasters do.

**→ Proceed to:** [`Level-08-Algorithm-Engineering.md`](./Level-08-Algorithm-Engineering.md)
