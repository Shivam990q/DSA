# 🌐 General Graph Matching (Blossom)

> *"Matching in NON-bipartite graphs — where odd cycles ('blossoms') make it hard."*

---

## I. THE PROBLEM
Maximum matching in a **general** (not necessarily bipartite) graph: largest set of edges with no shared vertex.

In bipartite graphs, augmenting paths are simple (Kuhn's). In general graphs, **odd-length cycles** ("blossoms") break the simple augmenting-path approach.

---

## II. EDMONDS' BLOSSOM ALGORITHM ⭐
Jack Edmonds' 1965 algorithm ("Paths, Trees, and Flowers") finds maximum matching in general graphs in polynomial time by **contracting blossoms** (odd cycles) into single vertices, finding augmenting paths in the contracted graph, then lifting back.
- Complexity: O(V³) (or O(V·E·α) with refinements; O(E·√V) with the Micali-Vazirani algorithm).
- This was historically important: it helped define the class **P** (polynomial-time problems).

---

## III. WHY BLOSSOMS ARE HARD
In bipartite graphs there are no odd cycles, so alternating paths behave nicely. In general graphs, an odd cycle can "hide" an augmenting path; the blossom contraction resolves this. The implementation is intricate.

---

## IV. WEIGHTED GENERAL MATCHING
Maximum/minimum **weight** matching in general graphs is also polynomial (weighted blossom algorithm), but quite complex. For most applications, libraries (or simpler reductions) are used.

---

## V. WHEN YOU NEED IT
- Non-bipartite maximum matching (e.g., pairing people where anyone can pair with anyone, with compatibility edges).
- Some scheduling/pairing problems that aren't bipartite.

If the graph IS bipartite, use the much simpler Kuhn's / Hopcroft-Karp / flow ([`12-Bipartite-Matching.md`](./12-Bipartite-Matching.md)).

---

## VI. PRACTICAL ADVICE
- General matching (blossom) is **rare** in interviews and uncommon even in CP.
- When it appears, most competitors use a **pre-written, tested blossom template** rather than implementing from scratch.
- First confirm the graph isn't bipartite (if it is, use the easy method).

---

## VII. COMPLEXITY
- Unweighted general matching (blossom): O(V³) typical; O(E√V) (Micali-Vazirani).
- Weighted general matching: polynomial but heavy.

---

## VIII. PROBLEMS
- General (non-bipartite) maximum matching (rare; CF "blossom" tag)
- Pairing problems on arbitrary compatibility graphs
- Some ICPC problems

---

## IX. NOTE
This is a Level 7+/research topic, included for completeness. Edmonds' blossom algorithm is a landmark in algorithm history (it helped define polynomial-time tractability), even if you rarely implement it.

---

**→ Next:** [`14-Network-Flow.md`](./14-Network-Flow.md)
