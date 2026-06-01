# Combination Sum

**Platform**: LeetCode 39 · **Difficulty**: Medium · **Topics**: Array, Backtracking · **Pattern**: Combinations with reuse + pruning

---

## 📜 Problem Statement

Given an array of **distinct** integers `candidates` and a target integer `target`, return *a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`*. You may return the combinations in **any order**.

The **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to `target` is **less than 150** combinations for the given input.

### Examples

**Example 1:**
```
Input:  candidates = [2, 3, 6, 7], target = 7
Output: [[2,2,3], [7]]
Explanation:
  2 + 2 + 3 = 7  → [2,2,3]
  7            = 7  → [7]
  These are the only two combinations.
```

**Example 2:**
```
Input:  candidates = [2, 3, 5], target = 8
Output: [[2,2,2,2], [2,3,3], [3,5]]
```

**Example 3:**
```
Input:  candidates = [2], target = 1
Output: []
Explanation: No combination of 2's can sum to 1.
```

### Constraints
```
1 <= candidates.length <= 30
2 <= candidates[i] <= 40
All elements of candidates are distinct.
1 <= target <= 40
```

---

## 🧠 Understanding the problem

We want every **multiset** of candidates whose sum equals `target`. "Multiset" because a value can repeat (unlimited reuse), but the *collection* is unordered — `[2,2,3]` and `[2,3,2]` are the same combination and must appear once. So this is a **combinations** problem (order doesn't matter), with the twist that an element may be picked multiple times.

The defining decision is: when I pick `candidates[i]`, am I allowed to pick it again? Yes. So the recursion that explores "use `candidates[i]`" must be allowed to land on `i` again — we recurse with the **same** start index `i`, not `i + 1`. To still avoid duplicate *unordered* combinations, we never look *backward* (we never revisit indices before `i`). That single rule — "stay at `i` for reuse, never go below `start`" — captures the whole problem.

Because all candidates are `>= 2` and `target <= 40`, the depth of any combination is bounded (at most 20 twos), keeping the search small. Two natural prunes — stop a branch the moment the remaining target goes negative, and (after sorting) break the loop once a candidate exceeds the remaining target — keep it brisk.

---

## Approach 1 — Backtracking with reuse (stay at `i`) ⭐

### Intuition
Standard combinations skeleton, but the "explore" step recurses with the **same index** `i` so the current candidate can be reused. We subtract from `target` as we go and record a combination when `target` hits exactly `0`. If `target` drops below `0`, the branch is dead — prune it.

### Algorithm
1. `backtrack(start, remain)`:
   - If `remain == 0`: record a copy of `cur`; return.
   - If `remain < 0`: return (dead branch).
   - For `i` from `start` to `n-1`:
     - **choose** `candidates[i]`.
     - **explore** `backtrack(i, remain - candidates[i])` — note `i`, allowing reuse.
     - **un-choose** (pop).

### Dry run on `candidates = [2,3,6,7], target = 7`
```
bt(0,7)
 i=0 +2 → bt(0,5)
   i=0 +2 → bt(0,3)
     i=0 +2 → bt(0,1)
       i=0 +2 → bt(0,-1) dead
       i=1 +3 → bt(1,-2) dead ... pop
     i=1 +3 → bt(1,0) RECORD [2,2,3]
     i=2 +6 → bt(2,-3) dead
   i=1 +3 → bt(1,0)? remain was 5 → +3 → bt(1,2) ... no hit
   ...
 i=1 +3 → bt(1,4) → +3 → bt(1,1) → no hit
 i=3 +7 → bt(3,0) RECORD [7]
Result: [2,2,3], [7]
```

### Code
```cpp
class Solution {
public:
    void backtrack(int start, int remain, vector<int>& cand,
                   vector<int>& cur, vector<vector<int>>& res) {
        if (remain == 0) { res.push_back(cur); return; }
        if (remain < 0) return;
        for (int i = start; i < (int)cand.size(); i++) {
            cur.push_back(cand[i]);                 // choose
            backtrack(i, remain - cand[i], cand, cur, res); // i → reuse allowed
            cur.pop_back();                         // un-choose
        }
    }
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
        vector<vector<int>> res;
        vector<int> cur;
        backtrack(0, target, candidates, cur, res);
        return res;
    }
};
```
```java
class Solution {
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, target, candidates, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int remain, int[] cand,
                           List<Integer> cur, List<List<Integer>> res) {
        if (remain == 0) { res.add(new ArrayList<>(cur)); return; }
        if (remain < 0) return;
        for (int i = start; i < cand.length; i++) {
            cur.add(cand[i]);                          // choose
            backtrack(i, remain - cand[i], cand, cur, res); // i → reuse allowed
            cur.remove(cur.size() - 1);                // un-choose
        }
    }
}
```
```python
class Solution:
    def combinationSum(self, candidates, target):
        res = []
        def backtrack(start, remain, cur):
            if remain == 0:
                res.append(cur[:]); return
            if remain < 0:
                return
            for i in range(start, len(candidates)):
                cur.append(candidates[i])              # choose
                backtrack(i, remain - candidates[i], cur)  # i → reuse allowed
                cur.pop()                              # un-choose
        backtrack(0, target, [])
        return res
```

### Complexity
- **Time**: O(N^(T/M + 1)) loosely, where `N` = number of candidates, `T` = target, `M` = smallest candidate — the search tree has depth up to `T/M` and branching up to `N`. In practice the result-size guarantee (< 150) keeps it small.
- **Space**: O(T/M) recursion depth + O(T/M) for the `cur` path.

---

## Approach 2 — Sort + early-break pruning (faster) ⭐

### Intuition
Sort the candidates ascending. Now inside the loop, the moment `candidates[i] > remain`, every later candidate is also too big, so we can **break** instead of `continue`. This turns the `remain < 0` check into an early exit and prunes whole tails of the loop.

### Algorithm
1. Sort `candidates`.
2. `backtrack(start, remain)`:
   - If `remain == 0`: record; return.
   - For `i` from `start`: if `candidates[i] > remain` → **break** (sorted ⇒ rest are bigger).
     - choose / explore with index `i` / un-choose.

### Dry run on `candidates = [2,3,5], target = 8` (already sorted)
```
bt(0,8)
 +2 → bt(0,6) → +2 → bt(0,4) → +2 → bt(0,2) → +2 → bt(0,0) RECORD [2,2,2,2]
                                          5>2 break
                    +3 → bt(1,1) → 3>1 break
       +3 → bt(1,3) → +3 → bt(1,0) RECORD [2,3,3]
                       5>0 break
 +3 → bt(1,5) → +3 → bt(1,2) 3>2 break ; +5 → bt(2,0) RECORD [3,5]
 +5 → bt(2,3) → 5>3 break
Result: [2,2,2,2], [2,3,3], [3,5]
```

### Code
```cpp
class Solution {
public:
    void backtrack(int start, int remain, vector<int>& cand,
                   vector<int>& cur, vector<vector<int>>& res) {
        if (remain == 0) { res.push_back(cur); return; }
        for (int i = start; i < (int)cand.size(); i++) {
            if (cand[i] > remain) break;            // sorted ⇒ rest are bigger
            cur.push_back(cand[i]);                 // choose
            backtrack(i, remain - cand[i], cand, cur, res); // reuse
            cur.pop_back();                         // un-choose
        }
    }
    vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
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
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> res = new ArrayList<>();
        backtrack(0, target, candidates, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, int remain, int[] cand,
                           List<Integer> cur, List<List<Integer>> res) {
        if (remain == 0) { res.add(new ArrayList<>(cur)); return; }
        for (int i = start; i < cand.length; i++) {
            if (cand[i] > remain) break;               // sorted ⇒ rest are bigger
            cur.add(cand[i]);                          // choose
            backtrack(i, remain - cand[i], cand, cur, res); // reuse
            cur.remove(cur.size() - 1);                // un-choose
        }
    }
}
```
```python
class Solution:
    def combinationSum(self, candidates, target):
        candidates.sort()
        res = []
        def backtrack(start, remain, cur):
            if remain == 0:
                res.append(cur[:]); return
            for i in range(start, len(candidates)):
                if candidates[i] > remain:             # sorted ⇒ rest are bigger
                    break
                cur.append(candidates[i])              # choose
                backtrack(i, remain - candidates[i], cur)  # reuse
                cur.pop()                              # un-choose
        backtrack(0, target, [])
        return res
```

### Complexity
- **Time**: Same worst-case order as Approach 1, but the sorted early-break prunes many dead branches in practice.
- **Space**: O(T/M) recursion depth + sort's O(log N) / O(N).

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| Backtrack with reuse | exponential, pruned by `remain<0` | O(T/M) | the core idea: recurse on `i` for reuse |
| Sort + early break | exponential, better pruning | O(T/M) | the version to write in an interview ⭐ |

The key concept either way: **reuse = recurse on `i`, no reuse = recurse on `i+1`**. Compare with [Combination Sum II](./03-Combination-Sum-II.md), which forbids reuse and must also dodge duplicate candidates.

---

## 🧪 Edge cases & pitfalls
- **No solution** (`candidates = [2], target = 1`) → returns `[]`. The base cases handle it: branches die when `remain < 0` and nothing reaches `remain == 0`.
- **Single candidate that divides target** (`[2], target = 6`) → `[[2,2,2]]`; reuse builds the whole combination from one value.
- **Pitfall — recursing on `i+1`**: that would forbid reuse and silently turn this into a *use-once* problem, dropping valid answers like `[2,2,3]`.
- **Pitfall — recursing on `0` or `start` of the parent**: looking backward regenerates the same multiset in different orders → duplicates. Always pass `i` (current), never an index below `start`.
- **Pitfall — forgetting to copy `cur`** when recording: store a snapshot, not the live, still-mutating path.
- **Pitfall — `continue` vs `break`**: with sorted input use `break` after `cand[i] > remain`; `continue` still works but wastes time scanning the bigger tail.

---

## 🔗 Related problems
- **Combination Sum II** (LC 40) — each candidate used once, input may contain duplicates. → [03-Combination-Sum-II.md](./03-Combination-Sum-II.md)
- **Combination Sum III** (LC 216) — exactly `k` numbers from 1..9 summing to `n`.
- **Combination Sum IV** (LC 377) — *count* ordered combinations (it's really a DP, order matters).
- **Subsets** (LC 78) — the underlying "choose forward with a start index" skeleton. → [01-Subsets.md](./01-Subsets.md)
- **Coin Change II** (LC 518) — count combinations summing to amount (DP cousin).

---

**→ Next:** [`03-Combination-Sum-II.md`](./03-Combination-Sum-II.md) | [Problem set index](./00-Index.md) | **← Prev:** [`01-Subsets.md`](./01-Subsets.md)
