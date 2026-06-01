# 📊 Sheet Tracker Template

> *"What gets tracked gets finished. What's untracked gets abandoned."*

---

## THE SPREADSHEET COLUMNS
Copy this into Google Sheets / Excel / Notion:

| # | Problem | Sheet | Topic/Pattern | Difficulty | Date Attempted | Time (min) | Status | Mistakes | Revisit Date | Notes |
|---|---------|-------|---------------|-----------|----------------|-----------|--------|----------|-------------|-------|

### Status values
- `TODO` — not started
- `ATTEMPTED` — tried, not solved
- `SOLVED-HELP` — solved after editorial
- `SOLVED` — solved independently
- `MASTERED` — re-solved at day 7+ without help

---

## THE PROGRESS DASHBOARD (auto-computed)
```
Total problems:        ____
Solved:                ____ (___%)
Solved independently:  ____ (___%)
Mastered:              ____ (___%)
Avg time (Medium):     ____ min
Current streak:        ____ days
```

---

## THE WEEKLY REVIEW (every Sunday)
```
☐ Problems solved this week: ____
☐ New patterns learned: ____
☐ Recurring mistake categories: ____
☐ Problems to revisit (due this week): ____
☐ Next week's focus topic: ____
```

---

## THE SPACED-REPETITION SCHEDULE
For every hard/important problem:
- Solve → set Revisit Date = +7 days
- Re-solve at +7 → if smooth, set +30 days
- Re-solve at +30 → if smooth, MASTERED
- If struggled at any revisit → reset to +7

---

## TOOLS FOR TRACKING
- **Google Sheets / Excel** — simplest, flexible
- **Notion** — databases + notes combined
- **[takeuforward.org](https://takeuforward.org)** / **neetcode.io** — built-in trackers for their sheets
- **[LeetCode](https://leetcode.com)** — built-in solved tracker + lists
- **Anki** — flashcards for patterns (spaced repetition automated)

---

## THE TEMPLATE ROW (example)
```
1 | Two Sum | NeetCode | Hashing/Complement | Easy | 2026-05-29 | 8 | SOLVED | none | 2026-06-05 | hash complement pattern
2 | LRU Cache | Striver SDE | Design (HashMap+DLL) | Medium | 2026-05-30 | 42 | SOLVED-HELP | forgot to move node to head on get | 2026-06-06 | DLL ordering
```

---

## WHY THIS MATTERS
- You SEE your progress (motivation)
- You SPOT recurring mistakes (targeted improvement)
- You KNOW what to revisit (retention)
- You FINISH the sheet (completion)

---

**→ Back to:** [`00-Index.md`](./00-Index.md)
