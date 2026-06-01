# 🌀 Backtracking — Systematic State-Space Search

> *"To find a solution, try one. If wrong, undo and try the next."*

---

## I. THE PARADIGM

Backtracking = recursion with state mutation + undo.

```
function backtrack(state):
    if is_solution(state):
        record(state)
        return
    for choice in valid_choices(state):
        make_choice(state, choice)
        backtrack(state)
        undo_choice(state, choice)
```

The "undo" is critical. Without it, branches contaminate each other.

---

## II. THE BACKTRACKING TEMPLATE

```cpp
void backtrack(vector<int>& current, /* other state */) {
    if (is_complete(current)) {
        results.push_back(current);
        return;
    }
    for (int candidate : get_candidates(current)) {
        if (is_valid(candidate, current)) {
            current.push_back(candidate);
            backtrack(current);
            current.pop_back();   // UNDO
        }
    }
}
```

---

## III. PRUNING — THE SECRET WEAPON

A pure backtracking is exponential. Pruning makes it tractable.

### Constraint pruning
If a partial solution can never become valid, abandon early.

> N-queens: as soon as two queens attack each other, prune.

### Bound pruning
If a partial solution can never beat the best so far, abandon (this is **branch & bound**).

> TSP: if current tour cost + lower-bound for rest ≥ best so far, prune.

### Symmetry pruning
Skip choices that lead to symmetric (already-explored) states.

> Subset enumeration: only consider items in increasing index order.

---

## IV. CLASSIC BACKTRACKING PROBLEMS

### 1. Subset enumeration (LC 78)
Generate all 2ⁿ subsets.

```cpp
void subsets(vector<int>& nums, int start, vector<int>& cur, vector<vector<int>>& res) {
    res.push_back(cur);
    for (int i = start; i < nums.size(); i++) {
        cur.push_back(nums[i]);
        subsets(nums, i + 1, cur, res);
        cur.pop_back();
    }
}
```

### 2. Permutations (LC 46)
Generate all n! orderings.

```cpp
void permute(vector<int>& nums, vector<bool>& used, vector<int>& cur, vector<vector<int>>& res) {
    if (cur.size() == nums.size()) { res.push_back(cur); return; }
    for (int i = 0; i < nums.size(); i++) {
        if (used[i]) continue;
        used[i] = true; cur.push_back(nums[i]);
        permute(nums, used, cur, res);
        used[i] = false; cur.pop_back();
    }
}
```

### 3. N-Queens (LC 51)
Place n queens on n×n board, no two attacking.
**Pruning**: column / diagonal sets.

### 4. Sudoku Solver (LC 37)
Fill 9×9 grid respecting constraints.
**Pruning**: row / column / box sets.

### 5. Word Search (LC 79)
Find a word in a grid via DFS.
**Pruning**: mark visited cell; unmark on return.

### 6. Combination Sum (LC 39)
Find all ways to make target from given numbers.

### 7. Palindrome Partitioning (LC 131)
Partition string into palindromes.

### 8. Letter Combinations of Phone Number (LC 17)

### 9. Generate Parentheses (LC 22)
**Pruning**: open ≤ n, close ≤ open.

### 10. Restore IP Addresses (LC 93)

---

## V. PROBLEMS (TOP 30)

1. Subsets I, II
2. Permutations I, II
3. Combinations
4. Combination sum I, II, III, IV
5. N-Queens I, II
6. Sudoku Solver
7. Word Search I, II (II uses Trie + backtrack)
8. Palindrome partitioning I, II
9. Restore IP addresses
10. Generate parentheses
11. Letter combinations of phone number
12. Letter case permutation
13. Beautiful arrangement
14. Letter tile possibilities
15. Knight's tour (Warnsdorff heuristic)
16. Rat in a maze
17. M-coloring
18. Word break II
19. Remove invalid parentheses
20. Expression add operators
21. Verbal arithmetic puzzle
22. Increasing subsequences
23. Number of squareful arrays
24. Maximum length of concatenated string with unique chars
25. Partition to K equal sum subsets
26. Matchsticks to square
27. Stickers to spell word (with memo)
28. Path with maximum gold
29. Unique paths III
30. The maze III

---

## VI. THE SUBSET-VS-PERMUTATION DICHOTOMY

These are the two fundamental backtracking templates:

### Subset-style (combinations)
Each call fixes "have I included element i?"
```python
def f(i, picked):
    if i == n: process(picked); return
    f(i+1, picked)         # don't pick
    f(i+1, picked + [a[i]]) # pick
```
2ⁿ leaves.

### Permutation-style (orderings)
At each level, pick any unused element next.
```python
def f(picked):
    if len(picked) == n: process(picked); return
    for i in unused:
        f(picked + [a[i]])
```
n! leaves.

Most backtracking problems are variants of these two.

---

## VII. WITH MEMOIZATION → DP

When backtracking has overlapping subproblems, **memoize on the relevant state**.

> Word Break: recursion + memoization on (start_index) → O(n²).
> Stickers to spell word: state = (target_remaining_mask), memoize → 2^|target|.

The line between backtracking and DP is fuzzy. Both explore state space; DP caches.

---

## VIII. THE 8 BACKTRACKING PRINCIPLES

1. **Mutate-then-recurse-then-undo**
2. **Maintain global solution set if collecting**
3. **Use start-index to avoid duplicates** (for combinations)
4. **Use `used[]` array for permutations**
5. **Prune aggressively** (bounds, constraints, symmetries)
6. **For grid problems, mark visited; unmark on return**
7. **For unique results with duplicates, sort + skip duplicates**
8. **Memoize when subproblems overlap**

---

## IX. SKIPPING DUPLICATES (CLASSIC PATTERN)

For "all unique subsets/permutations with duplicate inputs":

```cpp
sort(nums.begin(), nums.end());

void backtrack(int start, ...) {
    process(...);
    for (int i = start; i < n; i++) {
        if (i > start && nums[i] == nums[i-1]) continue;  // skip duplicate at same level
        nums[i] is chosen; recurse; unchoose;
    }
}
```

The condition `i > start` (not `i > 0`) is crucial: we skip duplicates at the **current level**, not across levels.

---

## X. RECOMMENDED READING

- **CLRS Chapter 35** — NP-completeness + backtracking
- **Skiena, Algorithm Design Manual** — backtracking chapter
- **[Aditya Verma](https://www.youtube.com/@AdityaVermaTheProgrammingLord)'s recursion playlist** (YouTube) — gold for beginners

---

**→ Next:** Branch & Bound and all other paradigms → [`COMPENDIUM-Advanced-Algorithms.md`](./COMPENDIUM-Advanced-Algorithms.md)
