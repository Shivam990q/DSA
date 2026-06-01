# 📓 The Mistake Log — Your Personal Feedback Loop

> *"He who refuses to record his mistakes is doomed to repeat them."*

---

## I. WHY A MISTAKE LOG?

Without one:
- You repeat the same bug categories forever
- Hidden weaknesses persist invisibly
- Growth becomes random walking

With one:
- Patterns emerge in your bugs
- Your weaknesses become *targets*
- Each mistake compounds into wisdom

---

## II. THE LOG TEMPLATE

```
Date: 2026-05-29
Problem: LC 76 — Minimum Window Substring
Time spent: 35 min (target was 25 min)
Verdict: AC after 2 WAs

ROOT CAUSE OF MISTAKES:
1. Off-by-one when shrinking window — used `<=` instead of `<`
2. Forgot to reset count map on test cases

PATTERN MISSED:
- Counter-based "valid" tracking via single integer (vs comparing two maps)

LESSON:
- For sliding window with character constraints: track count of "satisfied" 
  characters in a single int, increment when count[c] reaches required[c]

REVISIT IN: 7 days
```

---

## III. CATEGORIZE YOUR MISTAKES

After 30 entries, classify:

### Type A: **Algorithmic mistakes** (wrong approach)
- "I used DFS where BFS was needed"
- "I tried greedy where DP was correct"
- "I missed the observation that X is monotonic"

### Type B: **Implementation mistakes** (right idea, wrong code)
- Off-by-one
- Integer overflow
- Wrong loop bounds
- Uninitialized variable

### Type C: **Edge case mistakes**
- n = 0 / n = 1 not handled
- Empty input crash
- Negative input
- Maximum constraint overflow

### Type D: **Reading mistakes** (misunderstood problem)
- Missed a constraint
- Misread "min" as "max"
- Ignored modular requirement

### Type E: **Time management mistakes**
- Spent too long on wrong approach
- Skipped easier problem
- Didn't switch when stuck

---

## IV. THE PATTERN REVELATION

After 30+ entries, you'll see:
- "I always have off-by-one when shrinking sliding windows."
- "I confuse `<` and `<=` in BS termination."
- "I forget MOD on the final answer."
- "I don't read constraints carefully — always double-check n and a[i] range."

**Now you have ammunition.** These specific weaknesses become your training targets.

---

## V. HOW TO USE THE LOG

### Daily (1 min)
- After each problem: write 3-line entry

### Weekly (15 min, Sunday)
- Re-read the week's entries
- Spot recurring categories
- Set "no-go" rules: e.g., "this week, I will write `mid = lo + (hi - lo) / 2` always"

### Monthly (30 min)
- Categorize all entries by type (A-E)
- Visualize: which type dominates?
- Adjust training: more of category X drills

### Quarterly (60 min)
- Review 90 days of mistakes
- Note which categories DROPPED (you fixed them)
- Note which PERSIST (chronic issues — need targeted intervention)

---

## VI. THE LOG FORMATS

### Plain text (simplest)
- Notepad, Obsidian, Notion, Markdown file
- Human-readable, searchable

### Spreadsheet (best for analysis)
| Date | Problem | Time | Verdict | Type | Cause | Lesson | Revisit |
|------|---------|------|---------|------|-------|--------|---------|
| ...  | ...     | ...  | ...     | ...  | ...   | ...    | ...     |

### Code repo (for power users)
- A GitHub repo with one .md per problem
- Tag with categories
- Searchable by topic

Pick the simplest format you'll actually maintain.

---

## VII. SAMPLE 30-DAY LOG SUMMARY (HYPOTHETICAL)

```
Total entries: 35

By type:
  A (algorithmic): 8 (23%)
  B (implementation): 14 (40%) ← dominant!
  C (edge case): 7 (20%)
  D (reading): 4 (11%)
  E (time): 2 (6%)

Top recurring sub-categories:
  - Off-by-one in BS: 5 occurrences
  - Integer overflow on sums: 4
  - Forgot to reset state in T-cases: 3
  - n=1 edge case: 3

Action plan:
  - Memorize "while (lo < hi) ... if (...) hi = mid; else lo = mid + 1;" template
  - Default to long long for sums in CP
  - Add reset() block to multi-test-case template
  - Always test n=1 explicitly
```

---

## VIII. THE GOLDEN RULES

1. **Write entries DAILY**, not weekly. Memory fades fast.
2. **Be specific**: "off-by-one in shrinking window at line 14" > "small bug."
3. **Identify the ROOT cause**, not just the symptom.
4. **Note the LESSON in 1-2 sentences** — searchable later.
5. **Schedule REVISIT** for hard problems (7 days, then 30 days).
6. **Don't shame yourself** — this is data, not judgment.
7. **Look for patterns**, not single instances.

---

## IX. THE BUG ANTHOLOGY (THE MOST UNIVERSAL BUGS)

After 100+ entries, your top 10 will likely include:

1. **Off-by-one in loops/arrays**
2. **Integer overflow** (forgot `long long`)
3. **Modular arithmetic forgotten** in some step
4. **Forgot to reset state** between test cases
5. **Wrong initialization** of dp / dist / visited
6. **Recursion stack overflow** for n=10⁶
7. **Hash collision** in adversarial CF
8. **Wrong loop direction** (j < i vs j <= i)
9. **Integer division when float needed**
10. **Forgetting to handle empty/null inputs**

Print this list. Pin it to your monitor. Check before submitting.

---

## X. THE FINAL TRUTH

> **"You don't get better by solving more problems.  
>  You get better by *learning* from each one.  
>  The mistake log is the difference."**

---

**→ Next:** [`08-The-Pattern-Journal.md`](./08-The-Pattern-Journal.md)
