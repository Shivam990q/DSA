# 📖 ICPC: The "Hello World" of Hard Problems

> *"The first hard problem you upsolve changes how you see all problems."*

---

## I. WHAT MAKES AN ICPC PROBLEM HARD
- Dense statements (extract the real problem)
- Multiple concepts combined
- Tight time limits (efficient implementation required)
- Edge cases that break naive solutions

---

## II. A CLASSIC ICPC ARCHETYPE: "The Necklace" (graph + Euler)
- **Problem**: given colored beads, can they form a necklace where adjacent beads share a color? (Reduces to Eulerian path on a graph of colors.)
- **Brute**: try all orderings — factorial, infeasible.
- **Insight**: model colors as vertices, beads as edges. An Eulerian path exists iff the graph is connected and has 0 or 2 odd-degree vertices.
- **Optimal**: check Eulerian conditions + Hierholzer's, O(V+E).
- **Pattern**: reduction to Eulerian path.

---

## III. ANOTHER ARCHETYPE: "Interval Scheduling with Weights"
- **Brute**: try all subsets, O(2ⁿ).
- **Better**: greedy by end time (fails — weights matter).
- **Optimal**: DP — sort by end, dp[i] = max(skip, take + dp[last non-overlap]), O(n log n) with binary search.
- **Pattern**: weighted interval scheduling DP.

---

## IV. THE ICPC PROBLEM-SOLVING METHOD
1. Read past the story → extract the math.
2. Identify the algorithmic core (it's usually a known concept in disguise).
3. Check constraints → algorithm class.
4. Implement carefully (ICPC penalizes wrong submissions).

---

## V. WHERE TO PRACTICE
- [Codeforces](https://codeforces.com) Gym (past ICPC regionals + world finals)
- [Kattis](https://open.kattis.com) (ICPC problem archive)
- ICPC Live Archive
- UVa Online Judge

---

## VI. THE UPSOLVE DISCIPLINE
ICPC problems are best learned by upsolving:
1. Attempt during a virtual contest.
2. If unsolved, read editorial for the IDEA.
3. Re-implement from scratch.
4. Note the reduction/pattern.

---

**→ Next:** [`02-ICPC-World-Finals-Greatest-Hits.md`](./02-ICPC-World-Finals-Greatest-Hits.md)
