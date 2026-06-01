# Two Sum

**Platform**: LeetCode 1 · **Difficulty**: Easy · **Topics**: Array, Hash Table · **Pattern**: Complement lookup

---

## 📜 Problem Statement

Given an array of integers `nums` and an integer `target`, return the **indices** of the two numbers such that they add up to `target`.

You may assume that each input has **exactly one solution**, and you may **not use the same element twice**. You can return the answer in any order.

### Examples

**Example 1:**
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9.
```

**Example 2:**
```
Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]
```

**Example 3:**
```
Input:  nums = [3, 3], target = 6
Output: [0, 1]
```

### Constraints
```
2 <= nums.length <= 10^4
-10^9 <= nums[i] <= 10^9
-10^9 <= target <= 10^9
Only one valid answer exists.
```

### Follow-up
Can you design an algorithm with less than O(n²) time?

---

## 🧠 Understanding the problem

We must return **indices**, not values, so any sorting-based approach has to remember original positions. For each number `x`, its partner is forced: it must be `target - x` (the **complement**). So the real question becomes: *"As I walk the array, has the complement I need already appeared?"* That's a membership/lookup question → hashing.

---

## Approach 1 — Brute force (all pairs)

### Intuition
Try every pair `(i, j)` and check if it sums to target.

### Algorithm
1. For `i` from `0` to `n-1`:
   - For `j` from `i+1` to `n-1`:
     - If `nums[i] + nums[j] == target` → return `{i, j}`.

### Dry run on `[2,7,11,15], target=9`
```
i=0 (2): j=1 (7) → 2+7=9 → return [0,1]
```

### Code
```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    int n = nums.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (nums[i] + nums[j] == target) return {i, j};
    return {};
}
```
```java
public int[] twoSum(int[] nums, int target) {
    int n = nums.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (nums[i] + nums[j] == target) return new int[]{i, j};
    return new int[]{};
}
```
```python
def twoSum(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return [i, j]
```

### Complexity
- **Time**: O(n²).
- **Space**: O(1).

### Verdict
Works, but the follow-up explicitly asks us to beat O(n²). Use hashing.

---

## Approach 2 — Two-pass hash map

### Intuition
First record every value's index in a map. Then for each `x`, look up whether `target - x` exists (and isn't the same index).

### Algorithm
1. Build `idx[value] = index` for all elements.
2. For each `i`: let `need = target - nums[i]`. If `need` is in the map at an index `j != i` → return `{i, j}`.

### Code
```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> idx;
    for (int i = 0; i < nums.size(); i++) idx[nums[i]] = i;
    for (int i = 0; i < nums.size(); i++) {
        int need = target - nums[i];
        auto it = idx.find(need);
        if (it != idx.end() && it->second != i) return {i, it->second};
    }
    return {};
}
```
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> idx = new HashMap<>();
    for (int i = 0; i < nums.length; i++) idx.put(nums[i], i);
    for (int i = 0; i < nums.length; i++) {
        int need = target - nums[i];
        Integer j = idx.get(need);
        if (j != null && j != i) return new int[]{i, j};
    }
    return new int[]{};
}
```
```python
def twoSum(nums, target):
    idx = {x: i for i, x in enumerate(nums)}
    for i, x in enumerate(nums):
        need = target - x
        if need in idx and idx[need] != i:
            return [i, idx[need]]
```

### Complexity
- **Time**: O(n).
- **Space**: O(n).

### Verdict
Beats O(n²). The `!= i` guard prevents using the same element twice. Can be tightened into one pass.

---

## Approach 3 — One-pass hash map (optimal) ⭐

### Intuition
We don't need the full map up front. As we walk, **before** inserting the current number, check if its complement was seen earlier. If so, we have both indices immediately. This naturally avoids reusing an element (we look up *before* inserting).

### Algorithm
1. Empty map `seen` (value → index).
2. For each `i` with value `x`:
   - `need = target - x`.
   - If `need` is in `seen` → return `{seen[need], i}`.
   - Else `seen[x] = i`.

### Dry run on `[3,2,4], target=6`
```
i=0 x=3: need=3, seen={} → not found → seen={3:0}
i=1 x=2: need=4, seen={3:0} → not found → seen={3:0, 2:1}
i=2 x=4: need=2, seen has 2 at index 1 → return [1, 2]
```

### Code
```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int,int> seen;        // value -> index
    for (int i = 0; i < nums.size(); i++) {
        int need = target - nums[i];
        auto it = seen.find(need);
        if (it != seen.end()) return {it->second, i};
        seen[nums[i]] = i;
    }
    return {};
}
```
```java
public int[] twoSum(int[] nums, int target) {
    Map<Integer, Integer> seen = new HashMap<>();   // value -> index
    for (int i = 0; i < nums.length; i++) {
        int need = target - nums[i];
        Integer j = seen.get(need);
        if (j != null) return new int[]{j, i};
        seen.put(nums[i], i);
    }
    return new int[]{};
}
```
```python
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(n).

### Verdict
**The canonical optimal solution.** One pass, handles duplicate values correctly (e.g. `[3,3]`), and never reuses an element because the lookup precedes the insert.

---

## Approach 4 — Sort + two pointers (when indices aren't required)

### Intuition
If the problem asked for the *values* (or a boolean), sorting + two pointers gives O(n log n) with O(1) extra space. Here we'd need to carry original indices, which adds bookkeeping — included for completeness and because the sorted-array variant (LC 167) uses exactly this.

### Algorithm
1. Pair each value with its index; sort by value.
2. Two pointers `l=0`, `r=n-1`. Move based on whether the sum is too small/large.

### Code
```cpp
vector<int> twoSum(vector<int>& nums, int target) {
    int n = nums.size();
    vector<pair<int,int>> a(n);
    for (int i = 0; i < n; i++) a[i] = {nums[i], i};
    sort(a.begin(), a.end());
    int l = 0, r = n - 1;
    while (l < r) {
        int sum = a[l].first + a[r].first;
        if (sum == target) return {a[l].second, a[r].second};
        else if (sum < target) l++;
        else r--;
    }
    return {};
}
```
```java
public int[] twoSum(int[] nums, int target) {
    int n = nums.length;
    int[][] a = new int[n][2];
    for (int i = 0; i < n; i++) { a[i][0] = nums[i]; a[i][1] = i; }
    Arrays.sort(a, (x, y) -> Integer.compare(x[0], y[0]));
    int l = 0, r = n - 1;
    while (l < r) {
        int sum = a[l][0] + a[r][0];
        if (sum == target) return new int[]{a[l][1], a[r][1]};
        else if (sum < target) l++;
        else r--;
    }
    return new int[]{};
}
```
```python
def twoSum(nums, target):
    a = sorted((x, i) for i, x in enumerate(nums))
    l, r = 0, len(a) - 1
    while l < r:
        s = a[l][0] + a[r][0]
        if s == target:
            return [a[l][1], a[r][1]]
        elif s < target:
            l += 1
        else:
            r -= 1
```

### Complexity
- **Time**: O(n log n).
- **Space**: O(n) for the index-value pairs.

### Verdict
Slower than hashing here, but it's the foundation for the **sorted-input** variant and for **3Sum/4Sum**. Worth knowing as a transferable pattern.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n²) | O(1) | baseline |
| Two-pass hash | O(n) | O(n) | clear, but two scans |
| One-pass hash | **O(n)** | O(n) | optimal, the standard answer ⭐ |
| Sort + two pointers | O(n log n) | O(n) | basis for 3Sum / sorted variant |

---

## 🧪 Edge cases & pitfalls
- **Duplicate values that form the answer** (`[3,3]`) → one-pass hashing handles it; a naive "map then look up same value" must guard against returning the same index twice.
- **Negative numbers / negative target** → arithmetic works unchanged.
- **No reuse of one element** → ensured by looking up the complement *before* inserting the current value.
- **Pitfall**: building the full map first and then searching can accidentally match an element with itself if you forget the `index != i` check.

---

## 🔗 Related problems
- **Two Sum II – Input Array Is Sorted** (LC 167) — two pointers, O(1) space.
- **3Sum** (LC 15) / **4Sum** (LC 18) — fix elements + two-pointer scan.
- **Two Sum III – Data structure design** (LC 170).
- **Two Sum IV – Input is a BST** (LC 653).

---

**→ Next:** [`04-Group-Anagrams.md`](./04-Group-Anagrams.md) | Prev: [`02-Valid-Anagram.md`](./02-Valid-Anagram.md) | [Index](./00-Index.md)
