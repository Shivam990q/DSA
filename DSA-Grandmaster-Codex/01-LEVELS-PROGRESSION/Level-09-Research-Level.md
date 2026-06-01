# 🔬 Level 9 — Research-Level Algorithms (The Researcher)

> *"The textbook ends where research begins."*

---

## 🎯 OUTCOME

You can:
- Read & comprehend SODA, STOC, FOCS, ESA, ICALP papers
- Implement state-of-the-art algorithms from research papers
- Identify gaps in the literature
- Contribute novel results (incremental or breakthrough)
- Teach research-level material

---

## 📚 PREREQUISITE

Level 7 (Elite CP) + Level 8 (Algorithm Engineering) ideally.

---

## 🧱 CURRICULUM (8 Modules, ~1500 hours)

### Module 9.1 — Theoretical Computer Science Foundation (200 hours)

**Topics:**
1. Computability theory (Turing machines, decidability)
2. Complexity theory (P, NP, NP-complete, NP-hard, PSPACE, EXP)
3. Reductions (Karp, Cook, polynomial-time)
4. Approximation algorithms (PTAS, FPTAS, APX-hardness)
5. Randomized complexity (RP, BPP, ZPP)
6. Circuit complexity
7. Communication complexity
8. Online algorithms (competitive ratio)
9. Streaming algorithms
10. Sublinear algorithms

**Books:**
- **Sipser** — *Introduction to the Theory of Computation*
- **Arora & Barak** — *Computational Complexity: A Modern Approach* ⭐
- **Vazirani** — *Approximation Algorithms*
- **Motwani, Raghavan** — *Randomized Algorithms*

---

### Module 9.2 — Algorithm Design Techniques (Research) (200 hours)

**Topics:**
1. Linear programming (simplex, interior point, primal-dual)
2. Semi-definite programming (SDP)
3. Convex optimization
4. Spectral methods (eigenvalue-based)
5. Random projections (Johnson-Lindenstrauss)
6. Markov chain Monte Carlo
7. Locality-sensitive hashing (deep)
8. Submodular optimization
9. Matroid theory
10. Algebraic methods in CS

**Books:**
- **Williamson, Shmoys** — *The Design of Approximation Algorithms*
- **Boyd, Vandenberghe** — *Convex Optimization*
- **Mitzenmacher, Upfal** — *Probability and Computing*

---

### Module 9.3 — Reading Research Papers (200 hours)

**Method**:
1. Read 1 paper/week from top venues (SODA, STOC, FOCS, ICALP, ESA)
2. Implement the algorithm if possible
3. Write a personal blog post explaining it
4. Attempt to find a flaw or improvement

**Top venues:**
- **SODA** (ACM-SIAM Symposium on Discrete Algorithms)
- **STOC** (Symposium on Theory of Computing)
- **FOCS** (Foundations of Computer Science)
- **ICALP** (International Colloquium on Automata, Languages and Programming)
- **ESA** (European Symposium on Algorithms)
- **SoCG** (Symposium on Computational Geometry)

---

### Module 9.4 — Specialized Topics (300 hours)

Pick **one** to specialize deeply:

#### 9.4.A — String Algorithms Research
- Suffix array construction in O(n) (DC3, SA-IS)
- Compressed suffix arrays
- BWT-based indexes
- LZ77/LZ78 compression algorithms
- Bidirectional search in compressed space

#### 9.4.B — Graph Algorithms Research
- Dynamic graph connectivity
- Min-cut in O(m log²n) (Karger)
- Approximate distances oracles
- Distance labeling
- Graph isomorphism (Babai's quasipoly result)

#### 9.4.C — Computational Geometry Research
- Voronoi diagrams in higher dimensions
- Geometric range searching
- Persistent geometric structures
- Approximate nearest neighbors (ANN)
- Computational topology

#### 9.4.D — Online & Streaming Research
- Online matching (Karp-Vazirani-Vazirani)
- Online learning (multiplicative weights)
- Streaming complexity bounds
- Sliding window algorithms

#### 9.4.E — Quantum Algorithms
- Grover's search
- Shor's factoring
- Quantum Fourier transform
- HHL for linear systems

---

### Module 9.5 — Open Problems Survey (100 hours)

Maintain a list of currently open problems in your specialty. Some examples:

- Is there a deterministic O(n log n) algorithm for online minimum spanning forest?
- Can we beat O(n log² n) for batch shortest paths in directed graphs with negative weights?
- Is graph isomorphism in P?
- P vs NP (the king of open problems)
- Strong Exponential Time Hypothesis (SETH) and conditional lower bounds

---

### Module 9.6 — Contribute (300 hours)

- Implement an open-source project (segment-tree library, suffix-array library)
- Submit improvements to existing libraries
- Write a survey on a topic
- Submit a paper to a workshop or conference (most accept beginner papers)
- Mentor at IOI / ICPC training camps

---

### Module 9.7 — Conference Attendance & Discussion (100 hours)

- Attend 1+ algorithm conferences/workshops per year
- Engage on Theory CS Stack Exchange
- Follow researchers on Twitter / Mastodon
- Read latest preprints on arXiv (cs.DS, cs.DM)

---

### Module 9.8 — Original Work (100 hours and beyond)

- Identify a small open problem
- Make a non-trivial observation
- Develop a result
- Write it up
- Submit / publish

---

## 📊 RESEARCH OUTPUT VOLUME

This level is measured in **comprehension and contribution**, not problem counts:
- **~50 research papers** read deeply (≈1/week for a year) across SODA/STOC/FOCS/ICALP/ESA
- **1 chosen specialization** taken to the research frontier (Module 9.4)
- **1+ open-source implementation** of a state-of-the-art algorithm
- **1 original contribution** — a survey, a workshop paper, or a novel result

---

## ⏱️ ESTIMATED TIME

- ~1500 hours
- ~3 years at 10 hours/week
- ~15 months at 25 hours/week
- (Open-ended — research runs on no fixed clock.)

---

## ✅ EXIT TEST

Submit a paper (workshop/conference acceptable). Even a survey paper counts.

OR: implement & open-source a state-of-the-art algorithm with benchmarks demonstrating it matches or beats existing libraries.

---

## 📌 RESOURCES

### Foundational Books
- Arora & Barak, *Computational Complexity*
- Goldreich, *Computational Complexity: A Conceptual Perspective*
- Cormen et al., *Introduction to Algorithms* (CLRS)
- Knuth, *The Art of Computer Programming* (TAOCP) — vol 1-4
- Erickson, *Algorithms* (free online) ⭐ — for deep proof exposure
- Tarjan, *Data Structures and Network Algorithms*
- Kleinberg & Tardos, *Algorithm Design*

### Online Lectures
- **MIT 6.046J** — Design and Analysis of Algorithms
- **[MIT 6.851](https://courses.csail.mit.edu/6.851/)** — Advanced Data Structures (Erik Demaine) ⭐⭐⭐
- **MIT 6.852** — Distributed Algorithms
- **CMU 15-451** — Algorithm Design and Analysis
- **Stanford CS255** — Cryptography
- **Berkeley CS270** — Combinatorial Algorithms

### Papers
- arXiv.org/list/cs.DS — Data Structures and Algorithms
- [DBLP](https://dblp.org) — Author and venue search

### Communities
- **TheoryNet** mailing list
- **Theory CS Stack Exchange**
- **Theoretical Computer Science Subreddit**

---

## 🚀 ON COMPLETION

You can read, implement, and extend the research frontier. You don't just use algorithms — you contribute to the literature that creates them.

**→ Proceed to:** [`Level-10-Algorithm-Designer.md`](./Level-10-Algorithm-Designer.md)
