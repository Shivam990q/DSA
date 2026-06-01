# 📄 Reading Research Papers

> *"A research paper is compressed years of thought. Decompression takes effort — but it's the fastest learning there is."*

---

## I. THE THREE-PASS METHOD (Keshav)

### Pass 1: The Bird's-Eye View (5-10 min)
- Read title, abstract, introduction
- Read section headings
- Read conclusions
- Skim references (which do you recognize?)

**Goal**: understand WHAT the paper is about and whether to read further.

### Pass 2: The Content Grasp (1 hour)
- Read the whole paper, but skip detailed proofs
- Look at figures, diagrams, tables carefully
- Mark unfamiliar terms / unread references

**Goal**: understand the main idea and supporting evidence. Be able to summarize to someone.

### Pass 3: The Deep Dive (4-5 hours)
- Re-derive the paper as if you were the author
- Verify every assumption, every proof step
- Identify implicit assumptions, potential flaws
- Implement the algorithm if possible

**Goal**: complete understanding. Be able to reconstruct the paper from memory, critique it, extend it.

---

## II. ANATOMY OF AN ALGORITHMS PAPER

1. **Abstract**: the result in 150 words
2. **Introduction**: problem, prior work, contribution
3. **Preliminaries**: notation, definitions
4. **Main result**: the algorithm / theorem
5. **Analysis**: correctness proof + complexity
6. **Experiments** (if applied): benchmarks
7. **Conclusion**: summary + open questions
8. **References**: the lineage

---

## III. WHAT TO EXTRACT

For an algorithms paper, always extract:
- **The problem** (precisely stated)
- **The key idea / observation** (usually 1-2 sentences)
- **The algorithm** (pseudocode in your own words)
- **The complexity** (and how it improves on prior)
- **The proof technique** (induction? amortized? probabilistic?)
- **The limitations** (when does it not apply?)

---

## IV. READING PROOFS

Proofs are where papers lose most readers. Strategy:
1. **Understand the statement** before the proof.
2. **Read the proof's structure** (is it induction? contradiction? construction?).
3. **For each step, ask "why is this true?"** Fill gaps yourself.
4. **Re-derive without the paper.** If you can't, you didn't understand.

If a step seems "obvious" to the author but isn't to you, that's where your learning lives. Spend time there.

---

## V. WHERE TO FIND PAPERS

- **arXiv.org** (cs.DS, cs.DM, cs.CC) — free preprints
- **[DBLP](https://dblp.org)** — search by author/venue
- **Google Scholar** — citation tracking
- **[Semantic Scholar](https://www.semanticscholar.org)** — AI-powered search
- **ECCC** — complexity theory
- Conference proceedings: **SODA, STOC, FOCS, ICALP, ESA, SoCG**

---

## VI. BUILDING A READING HABIT

- **1 paper per week** (deep, three-pass)
- Maintain a **paper journal**: 1 page per paper with your summary
- **Implement** when possible
- **Discuss** with peers (a reading group accelerates 5×)

After 50 papers, you'll read the 51st in half the time. After 200, you read at the level of a PhD student.

---

## VII. RED FLAGS IN PAPERS

- Unstated assumptions
- "It is easy to see that..." (often it isn't)
- Experiments only on cherry-picked inputs
- Complexity hiding large constants
- Missing comparison to obvious baselines

A critical reader catches these. Don't accept claims blindly.

---

## VIII. THE STARTER PAPERS (accessible classics)

1. Dijkstra (1959) — "A Note on Two Problems in Connexion with Graphs"
2. Knuth, Morris, Pratt (1977) — "Fast Pattern Matching in Strings"
3. Cooley & Tukey (1965) — FFT
4. Tarjan (1972) — "Depth-First Search and Linear Graph Algorithms"
5. Cormen et al. (CLRS) — proofs throughout (practice on these first)

These are readable by an undergraduate. Start here before attempting modern SODA/STOC papers.

---

## IX. RECOMMENDED READING

- **Keshav**, "How to Read a Paper" (the 3-pass method; free PDF)
- **Erickson**, *Algorithms* — to practice reading rigorous proofs

---

**→ Next:** [`08-Writing-Original-Algorithms.md`](./08-Writing-Original-Algorithms.md)
