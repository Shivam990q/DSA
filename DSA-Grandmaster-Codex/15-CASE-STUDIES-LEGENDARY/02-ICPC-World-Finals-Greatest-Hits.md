# 📖 ICPC World Finals — Greatest Hits

> *"The World Finals problems are where the best teams on Earth meet their limits."*

---

## I. THE NATURE OF WORLD FINALS PROBLEMS
- 11-13 problems, 5 hours, top ~135 teams
- Range: one trivial, several medium, a few that only 1-2 teams solve
- Combine multiple advanced techniques
- Reward deep observation + flawless implementation

---

## II. RECURRING THEMES AT WORLD FINALS
1. **Computational geometry** (convex hull, half-plane, rotating calipers)
2. **Advanced graph theory** (flows, matching, 2-SAT)
3. **Heavy DP** (with optimizations: CHT, Knuth, D&C)
4. **String algorithms** (suffix automaton, Aho-Corasick)
5. **Number theory + FFT**
6. **Ad-hoc constructive** (the "aha" problems)

---

## III. AN ARCHETYPE: "Network Flow in Disguise"
Many WF problems are max-flow / min-cost-flow hidden behind a story.
- **Skill**: recognize "assignment / matching / capacity" structure → model as flow.
- **Tool**: Dinic's / MCMF.

---

## IV. AN ARCHETYPE: "Geometry + Sweep"
- Problems involving line segments, intersections, areas.
- **Tool**: sweep line + balanced BST of active segments.

---

## V. HOW TOP TEAMS APPROACH WF
1. Read ALL problems in first 30 min (split among 3).
2. Identify the "easy trio" — secure points fast.
3. For hard problems: pair-program (one thinks, one verifies).
4. Manage the single computer ruthlessly.
5. Submit only tested code (penalty matters).

---

## VI. STUDYING WORLD FINALS
- Solve them on [Codeforces](https://codeforces.com) Gym (full archive)
- Read team solutions + editorials
- Note the reductions and the implementations
- Don't expect to solve all — even the best teams don't

---

## VII. THE LESSON FOR YOU
World Finals problems teach:
- **Pattern composition** (multiple techniques in one problem)
- **Implementation rigor** (clean, fast, bug-free)
- **Observation depth** (the key insight is often subtle)

Even if you never compete, upsolving WF problems will make you formidable.

---

**→ Next:** [`03-IOI-Ciphers-Mecho-Cake.md`](./03-IOI-Ciphers-Mecho-Cake.md)
