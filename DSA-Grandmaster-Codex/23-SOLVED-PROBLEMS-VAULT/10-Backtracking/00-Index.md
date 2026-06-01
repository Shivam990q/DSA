# 🗂️ Backtracking — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++, Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY the template (choose → explore → un-choose) shapes each one. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Subsets](./01-Subsets.md) | 78 | Medium | include/exclude → start-index loop → bitmask |
| 02 | [Combination Sum](./02-Combination-Sum.md) | 39 | Medium | reuse-allowed DFS → pruning |
| 03 | [Combination Sum II](./03-Combination-Sum-II.md) | 40 | Medium | sort + skip-dup-at-level |
| 04 | [Permutations](./04-Permutations.md) | 46 | Medium | used[] array → in-place swap |
| 05 | [Subsets II](./05-Subsets-II.md) | 90 | Medium | sort + skip-dup-at-level |
| 06 | [Word Search](./06-Word-Search.md) | 79 | Medium | grid DFS + visited sentinel |
| 07 | [Palindrome Partitioning](./07-Palindrome-Partitioning.md) | 131 | Medium | prefix DFS → DP precompute |
| 08 | [Letter Combinations of a Phone Number](./08-Letter-Combinations-Phone-Number.md) | 17 | Medium | digit-position DFS → iterative |
| 09 | [N-Queens](./09-N-Queens.md) | 51 | Hard | row-by-row DFS + conflict sets |

---

## 🎯 The pattern family

**Backtracking** is depth-first search over a tree of *partial solutions*. You build a candidate one decision at a time; whenever a decision can still lead somewhere valid you **explore**, and when you return you **undo** that decision so the next sibling branch starts from a clean slate. Every node in the search tree runs the same three-line ritual:

```
choose   → push a decision onto the current path / mutate shared state
explore  → recurse to make the next decision
un-choose→ pop the decision / restore shared state   (THE backtrack step)
```

The whole topic is variations on **what a "decision" is** and **when you record a solution**.

### The choose → explore → un-choose template

```
def backtrack(state):
    if is_complete(state):        # reached a leaf / goal
        record(state)
        return
    for choice in choices(state): # branch over the next decision
        if not valid(choice):     # prune dead branches early
            continue
        apply(choice)             # CHOOSE  — mutate path/shared state
        backtrack(state)          # EXPLORE — recurse
        undo(choice)              # UN-CHOOSE — restore for the next sibling
```

Three knobs decide the flavor of any problem:
- **What is a "choice"?** an index to include, a candidate to add, a cell to step into, a column for a queen.
- **When do I record?** at *every node* (subsets) vs. only at *leaves* (permutations, combination targets, full board).
- **How do I avoid re-visiting?** a `start` index (combinations — order doesn't matter), a `used[]` array (permutations — order matters), or a sentinel mark (grid search).

### The subset-vs-permutation dichotomy ⭐

This single distinction explains most of the files in this folder:

| | **Subsets / Combinations** | **Permutations** |
|---|---|---|
| Does order matter? | **No** — `{1,2}` = `{2,1}` | **Yes** — `[1,2]` ≠ `[2,1]` |
| How to avoid repeats | pass a **`start` index**; each recursive call only looks **forward** (`i ≥ start`) | use a **`used[]` flag** (or swap); every call may look at **all** unused elements |
| Loop shape | `for i in range(start, n)` → `dfs(i or i+1)` | `for i in range(n): if used[i] ...` → `dfs()` |
| Branch count | each element is "in or out" → up to `2^n` leaves | each position picks an unused element → `n!` leaves |
| Examples here | Subsets, Subsets II, Combination Sum, Combination Sum II, Palindrome Partitioning | Permutations |

**Mantra:** *"Combinations move forward with a `start` index; permutations look everywhere with a `used` flag."* If you can answer "does order matter?" you already know which skeleton to write.

### Handling duplicate inputs (the skip-at-level trick)

When the input may contain **duplicate values** and the answer must be **unique** (Combination Sum II, Subsets II), the canonical fix is:

1. **Sort** the input so equal values sit adjacently.
2. Inside the loop, skip a value that equals its predecessor **at the same recursion depth**:
   ```
   if (i > start && nums[i] == nums[i-1]) continue;
   ```

The condition `i > start` is the crux: it allows the *first* occurrence of a value at this level (so the value can still be used), but blocks the *2nd, 3rd, …* occurrences from starting a duplicate sibling branch. Using `i > 0` instead would wrongly forbid legitimately reusing the value at a deeper level.

### Pruning — what turns exponential into "fast enough"

Backtracking is exponential by nature, so cutting dead branches early is the main lever:
- **Bound checks** (`remain < 0 → return`) and **sorted early-break** (`if cand[i] > remain break`) in Combination Sum.
- **Constraint sets** for O(1) validity in N-Queens (columns + both diagonals).
- **Sentinel marking** so Word Search never reuses a cell on the current path.

---

**→ Start:** [`01-Subsets.md`](./01-Subsets.md) | Back to [vault index](../00-Index.md)
