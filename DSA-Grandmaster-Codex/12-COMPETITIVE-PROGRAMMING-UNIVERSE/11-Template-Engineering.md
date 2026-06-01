# 🛠️ Template Engineering

> *"Your template is your weapon. Forge it. Test it. Trust it. But never let it think for you."*

---

## I. WHAT A CP TEMPLATE SHOULD HAVE
1. Headers + namespace (`#include <bits/stdc++.h>`)
2. Type aliases (`ll`, `vi`, `pii`)
3. Macros (`rep`, `all`, `pb`)
4. Fast I/O (`sync_with_stdio(false); cin.tie(NULL)`)
5. Constants (`MOD`, `INF`)
6. Common utilities (`gcd`, `modPow`, `modInv`)
7. A debug macro (under `#ifdef LOCAL`)

See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/competitive-programming-template.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/competitive-programming-template.cpp).

---

## II. THE LIBRARY (add gradually, test each)
- DSU
- Segment tree (+ lazy)
- BIT (Fenwick)
- Sparse table
- Modular arithmetic class
- Combinatorics (nCr precompute)
- Graph algorithms (Dijkstra, BFS, DFS, topo)
- String (KMP, Z, hashing)
- Number theory (sieve, Miller-Rabin)
- Geometry primitives
- FFT/NTT
- Max flow (Dinic)
- LCA, HLD

---

## III. THE RULES OF TEMPLATE ENGINEERING
1. **Test every component thoroughly** before trusting it in a contest.
2. **Don't over-template** — a 500-line template is an error magnet.
3. **Add only what you use frequently.**
4. **Keep it organized** (one file per structure, or a snippets manager).
5. **Know your template** — be able to modify it under pressure.

---

## IV. THE STRESS-TEST DISCIPLINE
Every template component must pass stress testing:
- Write a brute-force reference.
- Generate random inputs.
- Compare for thousands of cases.

A buggy template fails silently and costs you contests. Validate ruthlessly.

---

## V. SNIPPET MANAGEMENT
- VS Code snippets / Sublime snippets for fast insertion
- A `library/` folder with tested implementations
- [KACTL](https://github.com/kth-competitive-programming/kactl)-style compact reference (printable for ICPC)

---

## VI. THE DON'T-OVER-RELY WARNING
Templates speed up implementation, NOT thinking. The observation, the algorithm choice, the proof — these are yours. The template just types faster.

> "A template handles the known. Your mind handles the unknown."

---

## VII. RECOMMENDED REFERENCE LIBRARIES
- **KACTL** (KTH) — the gold standard, compact, ICPC-ready
- **[AtCoder Library (ACL)](https://github.com/atcoder/ac-library)** — official, well-tested
- **Benq's library** — comprehensive
- **EbTech's** — well-documented

Study these, adapt to your style, test everything.

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | [`12-COMPENDIUM-CP-Wisdom.md`](./12-COMPENDIUM-CP-Wisdom.md)
