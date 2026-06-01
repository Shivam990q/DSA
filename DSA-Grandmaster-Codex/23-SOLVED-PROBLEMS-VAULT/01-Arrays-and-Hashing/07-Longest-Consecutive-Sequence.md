# Longest Consecutive Sequence

**Platform**: LeetCode 128 · **Difficulty**: Medium · **Topics**: Array, Hash Set, Union-Find · **Pattern**: Sequence-start detection

---

## 📜 Problem Statement

Given an unsorted array of integers `nums`, return the **length of the longest consecutive elements sequence**.

You must write an algorithm that runs in **O(n)** time.

### Examples

**Example 1:**
```
Input:  nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive sequence is [1,2,3,4]. Its length is 4.
```

**Example 2:**
```
Input:  nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
Explanation: [0..8] → length 9.
```

### Constraints
```
0 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9
```

---

## 🧠 Understanding the problem

"Consecutive" means values like `…, x, x+1, x+2, …` — **regardless of their positions** in the array. The O(n) requirement rules out sorting (O(n log n)). The values span up to ±10^9, so we can't use a boolean array indexed by value either. That leaves a **hash set** for O(1) membership, plus a clever way to avoid recounting.

---

## Approach 1 — Brute force (expand each element)

### Intuition
For each value `x`, try to extend a sequence upward: is `x+1` present? `x+2`? Count the run length.

### Why it's slow
Checking membership by scanning the array is O(n) per check, and we might re-walk overlapping runs many times → O(n³)-ish. Even with a set for membership, starting an upward walk from *every* element re-traverses the same sequence repeatedly → O(n²) worst case.

### Verdict
Too slow and the naive version doesn't meet O(n). It motivates the "only start from sequence beginnings" fix.

---

## Approach 2 — Sort, then scan

### Intuition
Sort the array; consecutive numbers become adjacent. Walk once, tracking the current run length, resetting on a gap and skipping duplicates.

### Algorithm
1. Sort `nums` (handle empty input → 0).
2. Walk; if `nums[i] == nums[i-1]+1` extend the run; if equal, skip; else reset run to 1.
3. Track the max run.

### Code
```cpp
int longestConsecutive(vector<int>& nums) {
    if (nums.empty()) return 0;
    sort(nums.begin(), nums.end());
    int best = 1, cur = 1;
    for (int i = 1; i < nums.size(); i++) {
        if (nums[i] == nums[i-1]) continue;          // duplicate
        if (nums[i] == nums[i-1] + 1) cur++;          // extend
        else cur = 1;                                  // gap → reset
        best = max(best, cur);
    }
    return best;
}
```
```java
public int longestConsecutive(int[] nums) {
    if (nums.length == 0) return 0;
    Arrays.sort(nums);
    int best = 1, cur = 1;
    for (int i = 1; i < nums.length; i++) {
        if (nums[i] == nums[i-1]) continue;           // duplicate
        if (nums[i] == nums[i-1] + 1) cur++;          // extend
        else cur = 1;                                  // gap → reset
        best = Math.max(best, cur);
    }
    return best;
}
```
```python
def longestConsecutive(nums):
    if not nums:
        return 0
    nums.sort()
    best = cur = 1
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            continue
        if nums[i] == nums[i-1] + 1:
            cur += 1
        else:
            cur = 1
        best = max(best, cur)
    return best
```

### Complexity
- **Time**: O(n log n).
- **Space**: O(1) (or O(n) depending on sort).

### Verdict
Easy and correct, but **violates the O(n) requirement**. Good fallback if you can't recall the hash trick.

---

## Approach 3 — Hash set with sequence-start check (optimal) ⭐

### Intuition
Put everything in a set. A number `x` is the **start of a sequence** only if `x-1` is NOT in the set. We then walk forward from each start. The crucial point: each element is the "next" of exactly one start, so the total work across all forward-walks is O(n), not O(n²).

### Algorithm
1. Insert all numbers into a hash set (dedupes automatically).
2. For each `x` in the set:
   - If `x-1` is in the set → `x` is not a start; skip.
   - Else walk `x, x+1, x+2, …` while present, counting length; update the max.

### Dry run on `[100,4,200,1,3,2]`
```
set = {1,2,3,4,100,200}
x=100: 99 not in set → start. 101? no → len=1
x=4:   3 in set → skip (not a start)
x=200: 199 not in set → start. 201? no → len=1
x=1:   0 not in set → start. 2? yes,3? yes,4? yes,5? no → len=4  ← best
x=3:   2 in set → skip
x=2:   1 in set → skip
answer = 4
```

### Code
```cpp
int longestConsecutive(vector<int>& nums) {
    unordered_set<int> s(nums.begin(), nums.end());
    int best = 0;
    for (int x : s) {
        if (s.count(x - 1)) continue;        // not a sequence start
        int len = 1, cur = x;
        while (s.count(cur + 1)) { cur++; len++; }
        best = max(best, len);
    }
    return best;
}
```
```java
public int longestConsecutive(int[] nums) {
    Set<Integer> s = new HashSet<>();
    for (int x : nums) s.add(x);
    int best = 0;
    for (int x : s) {
        if (s.contains(x - 1)) continue;     // not a sequence start
        int len = 1, cur = x;
        while (s.contains(cur + 1)) { cur++; len++; }
        best = Math.max(best, len);
    }
    return best;
}
```
```python
def longestConsecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:
            continue
        length, cur = 1, x
        while cur + 1 in s:
            cur += 1
            length += 1
        best = max(best, length)
    return best
```

### Complexity
- **Time**: O(n) — every value is visited at most twice (once as a candidate, once inside a forward walk).
- **Space**: O(n) for the set.

### Verdict
**The optimal answer.** The "only start from x where x-1 is absent" guard is what collapses the naive O(n²) into O(n). This is the insight interviewers look for.

---

## Approach 4 — Union-Find (alternative O(n·α))

### Intuition
Union each value `x` with `x+1` when both exist; the answer is the size of the largest connected component. Conceptually clean but heavier to implement than the set trick.

### Verdict
Works and is a nice talking point, but the hash-set approach is simpler and just as fast. Mention as an alternative.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Meets O(n)? |
|----------|------|-------|-------------|
| Brute force | O(n²)+ | O(n) | ❌ |
| Sort + scan | O(n log n) | O(1) | ❌ |
| Hash set + start check | **O(n)** | O(n) | ✅ optimal ⭐ |
| Union-Find | O(n·α) | O(n) | ✅ |

---

## 🧪 Edge cases & pitfalls
- **Empty array** → 0.
- **Duplicates** (`[1,2,2,3]`) → the set dedupes; the run `1,2,3` has length 3.
- **All identical** → length 1.
- **Pitfall**: forgetting the `x-1 not in set` guard turns it into O(n²) and may TLE on adversarial inputs (long single sequence).

---

## 🔗 Related problems
- **Longest Consecutive Sequence in a Binary Tree** (LC 298) — tree variant.
- **Binary Tree Longest Consecutive Sequence II** (LC 549).
- **Number of Connected Components** (LC 323) — the union-find perspective.

---

**→ Next:** [`08-Valid-Sudoku.md`](./08-Valid-Sudoku.md) | Prev: [`06-Product-of-Array-Except-Self.md`](./06-Product-of-Array-Except-Self.md) | [Index](./00-Index.md)
