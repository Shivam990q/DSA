# 📖 Google's Hardest Interview Problems

> *"Google interviews favor open-ended problems where the journey matters as much as the destination."*

---

## I. THE GOOGLE STYLE
- Open-ended: "How would you approach...?"
- Emphasis on optimization narration and tradeoffs
- Often graph, DP, or design-flavored
- 1-2 problems per 45-min round, deep

---

## II. HARD PROBLEMS FREQUENTLY ASSOCIATED WITH GOOGLE

### 1. Regular Expression Matching (LC 10)
- 2D DP with `.` and `*`. Tricky transitions.
- **Lesson**: careful state design for the `*` case.

### 2. Word Ladder II (LC 126)
- BFS for shortest distance + backtracking to reconstruct ALL paths.
- **Lesson**: combine BFS (distances) with DFS (path reconstruction).

### 3. LFU Cache (LC 460)
- HashMap + frequency buckets + DLL per frequency.
- **Lesson**: composite data structure design.

### 4. Median of Two Sorted Arrays (LC 4)
- Binary search on partition, O(log min(n,m)).
- **Lesson**: binary search on a non-obvious quantity.

### 5. Text Justification (LC 68)
- Greedy line packing + careful spacing.
- **Lesson**: meticulous implementation, edge cases.

### 6. Number of Islands II (LC 305)
- Online island count with Union-Find.
- **Lesson**: dynamic connectivity.

### 7. Trapping Rain Water II (LC 407)
- 2D version with min-heap (priority flood-fill).
- **Lesson**: heap-based boundary expansion.

### 8. Shortest Path in a Grid with Obstacles Elimination (LC 1293)
- BFS on augmented state (position, obstacles removed).
- **Lesson**: state augmentation.

### 9. Bus Routes (LC 815)
- BFS on routes (not stops).
- **Lesson**: choose the right graph model.

### 10. Maximum Profit in Job Scheduling (LC 1235)
- Weighted interval scheduling DP + binary search.
- **Lesson**: sort + DP + binary search composition.

---

## III. WHAT GOOGLE EVALUATES
- **Problem-solving**: can you reason from brute force to optimal?
- **Communication**: do you narrate clearly?
- **Coding**: clean, correct, tested?
- **Generality**: do you consider edge cases and tradeoffs?
- **"Googliness"**: collaboration, comfort with ambiguity

---

## IV. PREPARATION
- Solve Google-tagged problems (LC Premium)
- Practice optimization narration (brute → optimal aloud)
- Mock with open-ended, deep-dive format
- Be ready for follow-ups ("what if the input is a stream?")

---

**→ Next:** [`14-Meta-Hardest-Problems.md`](./14-Meta-Hardest-Problems.md)
