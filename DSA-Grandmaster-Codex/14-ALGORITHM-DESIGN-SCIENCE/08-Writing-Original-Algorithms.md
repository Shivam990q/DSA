# ✍️ Writing Original Algorithms

> *"The final test of understanding: can you create what didn't exist before?"*

---

## I. THE PIPELINE OF ORIGINAL WORK

```
1. CHOOSE a problem (open or under-explored)
2. UNDERSTAND prior work thoroughly
3. OBSERVE something others missed
4. DESIGN an algorithm around the observation
5. PROVE correctness
6. ANALYZE complexity
7. IMPLEMENT and benchmark
8. WRITE it up
9. SHARE / publish
```

---

## II. CHOOSING A PROBLEM

Good problems are:
- **Important**: someone cares about the answer
- **Tractable**: you have a realistic chance
- **Under-explored**: not already solved 10 ways
- **Aligned with your strengths**

Sources:
- "Open questions" sections of papers
- Slight generalizations of solved problems
- Practical problems from your work that lack good algorithms
- Competition problems that hint at deeper structure

---

## III. THE OBSERVATION

Original algorithms come from **one non-obvious observation**:
- "This quantity is monotonic, so binary search applies."
- "The optimal always has this structure, so we can restrict the search."
- "This can be reformulated as a known problem (matching/flow/etc.)."
- "Amortized over operations, this is cheaper than it looks."

Find the observation by:
- Computing small cases
- Looking for invariants / symmetries
- Trying to break the naive approach (failures reveal structure)

---

## IV. WRITING THE ALGORITHM UP

### Structure
1. **Problem statement** (precise, with notation)
2. **Prior work** (what exists, what's missing)
3. **Key idea** (the observation, 1-2 sentences)
4. **Algorithm** (clear pseudocode)
5. **Correctness proof**
6. **Complexity analysis**
7. **Experiments** (if applicable)
8. **Conclusion + open questions**

### Writing principles
- **Precision**: define every symbol
- **Clarity**: a smart reader should follow without you present
- **Honesty**: state limitations, failed attempts, assumptions
- **Reproducibility**: enough detail to re-implement

---

## V. PROVING YOUR ALGORITHM

- **Correctness**: state the invariant; prove init/maintenance/conclusion
- **Termination**: show a decreasing measure
- **Complexity**: count operations; use amortized/probabilistic analysis if needed
- **Optimality** (if claimed): prove a matching lower bound

If you can't prove it, you don't have a result — you have a conjecture. (Conjectures are fine — label them as such.)

---

## VI. THE IMPLEMENTATION TEST

Always implement:
- Bugs in code reveal flaws in the algorithm
- Benchmarks reveal hidden constants
- Stress-testing against brute force validates correctness
- Open-sourcing invites the world to find your errors

An algorithm that has never been coded is a hypothesis, not a result.

---

## VII. WHERE TO SHARE

| Venue                          | Audience              |
|--------------------------------|-----------------------|
| Personal blog / [Codeforces](https://codeforces.com) blog| CP community          |
| arXiv preprint                 | researchers           |
| Workshop paper                 | early-stage results   |
| Conference (SODA/ESA/etc.)     | peer-reviewed results |
| Open-source library            | practitioners         |
| GitHub + writeup               | everyone              |

Start small (blog, workshop). Build toward conferences.

---

## VIII. INCREMENTAL VS BREAKTHROUGH

Most original work is **incremental**:
- A slightly better constant
- A new application of an existing technique
- A simpler proof
- A cleaner implementation

This is REAL progress. Don't dismiss incremental work waiting for a "breakthrough." Breakthroughs are built on incremental steps.

---

## IX. THE FIRST PROJECT

A realistic first original contribution:
1. Pick a well-known algorithm (e.g., segment tree, DSU).
2. Find a non-standard variant or application.
3. Implement it cleanly with tests + benchmarks.
4. Write a thorough tutorial/blog explaining it from first principles.

This builds the muscles: understanding deeply, writing clearly, implementing correctly. Original research follows naturally.

---

## X. RECOMMENDED READING

- **Hamming**, "You and Your Research" (lecture; transformative)
- **Halmos**, "How to Write Mathematics"
- **Knuth**, "Mathematical Writing"
- **Zobel**, *Writing for Computer Science*

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | [`../15-CASE-STUDIES-LEGENDARY/00-Index.md`](../15-CASE-STUDIES-LEGENDARY/00-Index.md)
