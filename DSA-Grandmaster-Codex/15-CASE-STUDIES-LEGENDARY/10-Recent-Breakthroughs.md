# 📖 Recent Algorithmic Breakthroughs

> *"The field is alive. New results reshape what we thought was settled."*

> Note: dates and bounds are approximate; verify current state via primary sources before citing.

---

## I. ALMOST-LINEAR MAX FLOW (Chen, Kyng, Liu, Peng, Probst Gutenberg, Sachdeva — 2022)
- **Result**: max flow (and min-cost flow) in m^(1+o(1)) time — essentially linear in the number of edges.
- **Significance**: max flow was a decades-long target. This used interior-point methods + dynamic data structures.
- **Impact**: theoretical; practical implementations still maturing.

---

## II. NEGATIVE-WEIGHT SHORTEST PATHS (Bernstein, Nanongkai, Wulff-Nilsen — 2022)
- **Result**: single-source shortest paths with negative weights in near-linear O(m log⁸ n) time.
- **Significance**: beat the long-standing Bellman-Ford O(mn) for this problem.

---

## III. GRAPH ISOMORPHISM (Babai — 2016)
- **Result**: graph isomorphism in quasipolynomial time 2^(O(log^c n)).
- **Significance**: a problem suspected to be "between P and NP-complete." Babai's result is a landmark, though P remains open.

---

## IV. MATRIX MULTIPLICATION (ongoing)
- **Current**: O(n^2.371...) (improvements by Williams, Le Gall, Alman, Duan, others).
- **Lower bound**: Ω(n²) (trivial).
- **The gap is OPEN** — one of the great open problems.

---

## V. AKS PRIMALITY (Agrawal, Kayal, Saxena — 2002)
- **Result**: primality testing in deterministic polynomial time.
- **Significance**: settled that PRIMES ∈ P. (Notably, two of the authors were undergraduates.)
- **Practical note**: Miller-Rabin is still preferred in practice (faster).

---

## VI. DETERMINISTIC PRIMALITY & FACTORING CONTEXT
- Primality is in P (AKS).
- Factoring is NOT known to be in P (RSA's security relies on this).
- Shor's quantum algorithm factors in polynomial time — but requires a large fault-tolerant quantum computer (not yet built).

---

## VII. WHY THESE MATTER
1. They show the field is alive — "settled" problems get reopened.
2. They demonstrate technique transfer (continuous optimization → discrete algorithms).
3. They inspire: undergraduates (AKS), persistent researchers (max flow), and bold conjectures (P vs NP).

---

## VIII. HOW TO FOLLOW BREAKTHROUGHS
- **arXiv cs.DS** — daily preprints
- **[Quanta Magazine](https://www.quantamagazine.org)** — accessible explanations of breakthroughs
- **Theory blogs**: Scott Aaronson, Terence Tao, Computational Complexity (Lance Fortnow)
- **SODA / STOC / FOCS proceedings**

---

## IX. THE OPEN FRONTIERS (as of mid-2020s)
- P vs NP
- Matrix multiplication exponent (is it 2?)
- Graph isomorphism in P?
- Deterministic near-linear algorithms for more flow variants
- Quantum advantage on practical problems
- Fine-grained complexity (SETH-based lower bounds)

These await the next generation. Perhaps you.

---

**→ Next:** [`11-Tourist-Solutions-Studied.md`](./11-Tourist-Solutions-Studied.md)
