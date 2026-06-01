# Combination Sum II

**Platform**: LeetCode 40 · **Difficulty**: Medium · **Topics**: Array, Backtracking · **Pattern**: Use-once combinations + skip-dup-at-level

---

## 📜 Problem Statement

Given a collection of candidate numbers `candidates` (which **may contain duplicates**) and a target number `target`, find all **unique combinations** in `candidates` where the candidate numbers sum to `target`.

Each number in `candidates` may **only be used once** in the combination.

**Note:** The solution set must not contain duplicate combinations.

### Examples

**Example 1:**
```
Input:  candidates = [10, 1, 2, 7, 6, 1, 5], target = 8
Output: [[1,1,6], [1,2,5], [1,7], [2,6]]
Explanation: Note 1 appears twice in the input, so [1,1,6] is valid,
             but [1,7] (using either of the two 1's) must appear only once.
```

**Example 2:**
```
Input:  candidates = [2, 5, 2, 1, 2], target = 5
Output: [[1,2,2], [5]]
```

**Example 3:**
```
Input:  candidates = [1, 1], target = 3
Output: []
Explanation: 1 + 1 = 2 < 3, and no element may be reused.
```

### Constraints
```
1 <= candidates.length <= 100
1 <= candidates[i] <= 50
1 <= target <= 30
```

---

## 🧠 Understanding the problem

Two differences from [Combination Sum](./02-Combination-Sum.md) define this problem:

1. **Use once** — once you pick the element at index `i`, you must move on to `i + 1` (no reuse). That's the same advance as in [Subsets](./01-Subsets.md).
2. **Duplicate inputs, unique outputs** — the array may contain repeated *values* (e.g. two `1`s). Using each physical element at most once is fine, but the *result list* must not contain the same combination twice. Picking the first `1` vs. the second `1` for a combination like `[1,7]` would otherwise produce identical outputs.

The fix for the duplicate problem is the **skip-dup-at-level** trick: **sort** the array so equal values are adjacent, then within a single recursion level skip any value identical to the one just tried at this level. Concretely, `if (i > start && candidates[i] == candidates[i-1]) continue;`. The first occurrence of a value at a level is allowed (so `[1,1,6]` — which genuinely uses two 1's at *different* levels — still forms), but a second sibling branch starting with the same value is blocked (so `[1,7]` isn't generated twice).

This `i > start` condition is the heart of the whole topic — understand it once and Subsets II falls out for free.

---

## Approach — Sort + use-once DFS + skip-dup-at-level ⭐

### Intuition
Sort to cluster equal values. Recurse forward with `i + 1` (use-once). At each level, the first time we see a value we may branch on it; any *repeat of that value at the same level* is skipped, because exploring it would only regenerate a combination the first branch already covers. We still allow the value to recur at deeper levels, which is how genuine duplicates like `[1,1,6]` are formed.

### Algorithm
1. **Sort** `candidates` ascending.
2. `backtrack(start, remain)`:
   - If `remain == 0`: record a copy of `cur`; return.
   - For `i` from `start` to `n-1`:
     - If `candidates[i] > remain` → **break** (sorted ⇒ rest are bigger).
     - If `i > start && candidates[i] == candidates[i-1]` → **continue** (skip duplicate at this level).
     - **choose** `candidates[i]`.
     - **explore** `backtrack(i + 1, remain - candidates[i])` — `i + 1` ⇒ use-once.
     - **un-choose** (pop).

### Dry run on `candidates = [10,1,2,7,6,1,5], target = 8`
```
sort → [1,1,2,5,6,7,10]
bt(0,8)
 i=0 (1) → bt(1,7)
   i=1 (1) → bt(2,6)
     i=2 (2) → bt(3,4) → i=3(5)>4 break ... no hit
     i=3 (5) → bt(4,1) → 6>1 break
     i=4 (6) → bt(5,0) RECORD [1,1,6]
   i=2 (2) → bt(3,5) → i=3(5) → bt(4,0) RECORD [1,2,5]
   i=3 (5) → bt(4,2) → 6>2 break
   i=4 (6) → bt(5,0)? remain was 7-? actually [1,..]: i=5(7) → bt(6,0) RECORD [1,7]
 i=1 (1) → SKIP (i>start and equals candidates[0]) — avoids duplicate [1,7] etc.
 i=2 (2) → bt(3,6) → i=4(6) → bt(5,0) RECORD [2,6]
 i=3..  (5,6,7,10) → none reach 0
Result: [1,1,6], [1,2,5], [1,7], [2,6]
```
Notice `i=1 (1)` at the top level is skipped: the branch starting with the *first* 1 already enumerated everything that begins with a single leading 1.

### Code
```cpp
class Solution {
public:
    void backtrack(int start, int remain, vector<int>& cand,
                   vector<int>& cur, vector<vector<int>>& res) {
        if (remain == 0) { res.push_back(cur); return; }
        for (int i = start; i < (int)cand.size(); i++) {
            if (cand[i] > remain) break;                  // sorted ⇒ rest bigger
            if (i > start && cand[i] == cand[i-1]) continue; // skip dup at level
            cur.push_back(cand[i]);                       // choose
            backtrack(i + 1, remain - cand[i], cand, cur, res); // i+1 ⇒ use once
            cur.pop_back();                               // un-choose
        }
    }
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        sort(candidates.begin(), candidates.end());
        vector<vector<int>> res;
        vector<int> cur;
        backtrack(0, target, candidates, cur, res);
        return res;
    }
};
```
```java
class Solution {
    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, target, candidates, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int remain, int[] cand,
                           List<Integer> cur, List<List<Integer>> res) {
        if (remain == 0) { res.add(new ArrayList<>(cur)); return; }
        for (int i = start; i < cand.length; i++) {
            if (cand[i] > remain) break;                     // sorted ⇒ rest bigger
            if (i > start && cand[i] == cand[i-1]) continue; // skip dup at level
            cur.add(cand[i]);                                // choose
            backtrack(i + 1, remain - cand[i], cand, cur, res); // i+1 ⇒ use once
            cur.remove(cur.size() - 1);                      // un-choose
        }
    }
}
```
```python
class Solution:
    def combinationSum2(self, candidates, target):
        candidates.sort()
        res = []
        def backtrack(start, remain, cur):
            if remain == 0:
                res.append(cur[:]); return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:                   # sorted ⇒ rest bigger
                    break
                if i > start and candidates[i] == candidates[i-1]:
                    continue                                 # skip dup at level
                cur.append(candidates[i])                    # choose
                backtrack(i + 1, remain - candidates[i], cur)  # i+1 ⇒ use once
                cur.pop()                                    # un-choose
        backtrack(0, target, [])
        return res
```

### Complexity
- **Time**: O(2^n) worst case — every element is in/out, with the dedup and target prunes cutting branches heavily in practice.
- **Space**: O(n) recursion depth + O(n) for the path (output not counted); plus O(log n)/O(n) for the sort.

---

## 🔬 Why `i > start` and not `i > 0`

This is the single most common bug, so it's worth isolating.

- `i > start` means "I am **not** the first choice at *this* recursion level." Skipping such duplicates removes only *sibling* branches that start with the same value — exactly the ones that regenerate identical combinations.
- `i > 0` would skip a duplicate even when it is the **first** choice at the current level (i.e., the previous equal value was consumed by an *ancestor*, not a sibling). That wrongly forbids combinations like `[1,1,6]`, where the second `1` is legitimately chosen at a deeper level.

```
Level 0 picks the 1st '1'  → Level 1 may pick the 2nd '1'   (i == start here → NOT skipped) ✅
Level 0 picked the 1st '1' → Level 0 sees the 2nd '1' again (i  > start here → skipped)     ✅ avoids dup
```

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| Sort + skip-dup-at-level | O(2^n) pruned | O(n) | the standard, interview-ready answer ⭐ |
| Count-distinct + choose-k-of-each | O(2^n) | O(n) | alternative: group by value, loop "take 0..cnt of this value" — avoids the `i>start` check but needs frequency map |

The sort + skip trick is the one to internalize because it transfers verbatim to [Subsets II](./05-Subsets-II.md).

---

## 🧪 Edge cases & pitfalls
- **All identical, target unreachable** (`[1,1], target=3`) → `[]`. Use-once means at most `1+1=2`.
- **Exact single hit** (`[5], target=5`) → `[[5]]`.
- **Pitfall — `i > 0` instead of `i > start`**: drops valid multi-duplicate combinations (see the section above). The most common mistake on this problem.
- **Pitfall — recursing on `i` instead of `i + 1`**: that re-enables reuse, turning this back into Combination Sum and producing illegal repeats of the same physical element.
- **Pitfall — forgetting to sort**: the skip-dup logic relies on equal values being adjacent; without sorting it silently fails to dedup.
- **Pitfall — not copying `cur`** when recording → stored combinations get mutated by later pops.

---

## 🔗 Related problems
- **Combination Sum** (LC 39) — distinct candidates, unlimited reuse. → [02-Combination-Sum.md](./02-Combination-Sum.md)
- **Subsets II** (LC 90) — same skip-dup trick, but record at every node. → [05-Subsets-II.md](./05-Subsets-II.md)
- **Permutations II** (LC 47) — dedup permutations with duplicate inputs (skip-dup with a `used[]` twist).
- **Combination Sum III** (LC 216) — fixed count `k`, digits 1..9, no duplicates.

---

**→ Next:** [`04-Permutations.md`](./04-Permutations.md) | [Problem set index](./00-Index.md) | **← Prev:** [`02-Combination-Sum.md`](./02-Combination-Sum.md)
