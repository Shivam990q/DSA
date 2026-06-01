# Contains Duplicate

**Platform**: LeetCode 217 · **Difficulty**: Easy · **Topics**: Array, Hash Table, Sorting · **Pattern**: Seen-before set

---

## 📜 Problem Statement

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

### Examples

**Example 1:**
```
Input:  nums = [1, 2, 3, 1]
Output: true
Explanation: The value 1 appears at index 0 and index 3.
```

**Example 2:**
```
Input:  nums = [1, 2, 3, 4]
Output: false
Explanation: All four elements are distinct.
```

**Example 3:**
```
Input:  nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
Output: true
```

### Constraints
```
1 <= nums.length <= 10^5
-10^9 <= nums[i] <= 10^9
```

---

## 🧠 Understanding the problem

We only need a **yes/no**: does ANY value repeat? We don't need to know which value, how many times, or where. That "we only need existence" observation is what lets us stop early and keep things simple.

The values can be as large as 10^9 (and negative), so we cannot index by value into a plain array — we need a structure that handles arbitrary integer keys. That points at sorting or hashing.

---

## Approach 1 — Brute force (check every pair)

### Intuition
The literal definition: a duplicate exists if some pair `(i, j)` with `i < j` has `nums[i] == nums[j]`. Check all pairs.

### Algorithm
1. For each index `i` from `0` to `n-1`:
   - For each index `j` from `i+1` to `n-1`:
     - If `nums[i] == nums[j]` → return `true`.
2. If no pair matched → return `false`.

### Dry run on `[1, 2, 3, 1]`
```
i=0 (1): compare with 2,3,1 → match at j=3 (1==1) → return true
```

### Code
```cpp
bool containsDuplicate(vector<int>& nums) {
    int n = nums.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (nums[i] == nums[j]) return true;
    return false;
}
```
```java
public boolean containsDuplicate(int[] nums) {
    int n = nums.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (nums[i] == nums[j]) return true;
    return false;
}
```
```python
def containsDuplicate(nums):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True
    return False
```

### Complexity
- **Time**: O(n²) — up to ~10^10 comparisons for n = 10^5. **Will TLE.**
- **Space**: O(1).

### Verdict
Correct but too slow for the constraints. It's the baseline that proves we understand the problem; now we optimize.

---

## Approach 2 — Sort, then scan neighbors

### Intuition
If equal values exist, sorting brings them **next to each other**. Then a single linear scan comparing adjacent elements finds any duplicate.

### Algorithm
1. Sort `nums`.
2. Scan `i` from `1` to `n-1`: if `nums[i] == nums[i-1]` → return `true`.
3. Return `false`.

### Dry run on `[1, 2, 3, 1]`
```
sort → [1, 1, 2, 3]
i=1: nums[1]=1 == nums[0]=1 → return true
```

### Code
```cpp
bool containsDuplicate(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    for (int i = 1; i < nums.size(); i++)
        if (nums[i] == nums[i-1]) return true;
    return false;
}
```
```java
public boolean containsDuplicate(int[] nums) {
    Arrays.sort(nums);
    for (int i = 1; i < nums.length; i++)
        if (nums[i] == nums[i-1]) return true;
    return false;
}
```
```python
def containsDuplicate(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True
    return False
```

### Complexity
- **Time**: O(n log n) — dominated by the sort.
- **Space**: O(1) if sorting in place (O(n) for some library sorts like Python's Timsort / merge sort).

### Verdict
Big improvement: passes the constraints. Trade-off: it **mutates the input order** and isn't the theoretical optimum. Good answer when interviewer says "without extra space."

---

## Approach 3 — Hash set (optimal) ⭐

### Intuition
We want O(1) "have I seen this value before?" A **hash set** gives exactly that. Walk once; the first time a value is already present, we've found a duplicate.

### Algorithm
1. Create an empty hash set `seen`.
2. For each `x` in `nums`:
   - If `x` is already in `seen` → return `true`.
   - Otherwise insert `x` into `seen`.
3. Return `false`.

### Dry run on `[1, 2, 3, 1]`
```
x=1 → not in {} → insert → {1}
x=2 → not in {1} → insert → {1,2}
x=3 → not in {1,2} → insert → {1,2,3}
x=1 → ALREADY in {1,2,3} → return true
```

### Code
```cpp
bool containsDuplicate(vector<int>& nums) {
    unordered_set<int> seen;
    seen.reserve(nums.size());          // avoid rehashing → faster
    for (int x : nums) {
        if (seen.count(x)) return true;
        seen.insert(x);
    }
    return false;
}
```
```java
public boolean containsDuplicate(int[] nums) {
    Set<Integer> seen = new HashSet<>(nums.length * 2);  // avoid rehashing → faster
    for (int x : nums) {
        if (seen.contains(x)) return true;
        seen.add(x);
    }
    return false;
}
```
```python
def containsDuplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**Python one-liner** (same idea — a set drops duplicates, so a size change means a duplicate existed):
```python
def containsDuplicate(nums):
    return len(set(nums)) < len(nums)
```

### Complexity
- **Time**: O(n) average. (Worst case O(n²) only under pathological hash collisions — not a concern in practice.)
- **Space**: O(n) for the set.

### Verdict
**The optimal answer.** O(n) time, single pass, doesn't touch the input order. This is what you present as your final solution.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Mutates input | When to mention |
|----------|------|-------|---------------|-----------------|
| Brute force | O(n²) | O(1) | no | only as the baseline |
| Sort + scan | O(n log n) | O(1)* | yes | "optimize for space" / no-extra-memory ask |
| Hash set | **O(n)** | O(n) | no | the default optimal answer ⭐ |

\* O(1) for in-place sort; the language's library may use O(n).

The classic interview dialogue is the **time–space trade-off**: hashing buys O(n) time by spending O(n) space; sorting saves space but costs a log factor. Stating this trade-off out loud is exactly what interviewers want to hear.

---

## 🧪 Edge cases & pitfalls
- **Single element** (`n = 1`) → no duplicate possible → `false`. All approaches handle it (loops just don't run).
- **All identical** (`[7,7,7]`) → `true` on the first repeat.
- **Negative values / large values** → fine for sorting and hashing; this is exactly why we can't use a fixed-size boolean array indexed by value.
- **Pitfall**: in the hash approach, check membership *before* inserting. Inserting first and then checking size-change works too, but the "check-then-insert" order is clearer and stops at the earliest duplicate.

---

## 🔗 Related problems
- **Contains Duplicate II** (LC 219) — duplicate within index distance `k` (sliding-window hash set).
- **Contains Duplicate III** (LC 220) — values within `t` AND indices within `k` (bucketing / ordered set).
- **Find the Duplicate Number** (LC 287) — exactly one duplicate, O(1) space via Floyd's cycle detection.
- **Single Number** (LC 136) — the opposite flavor; uses XOR.

---

**→ Next:** [`02-Valid-Anagram.md`](./02-Valid-Anagram.md) | [Problem set index](./00-Index.md)
