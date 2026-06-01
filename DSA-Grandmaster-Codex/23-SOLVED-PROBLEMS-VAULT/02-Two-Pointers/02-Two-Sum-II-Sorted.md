# Two Sum II – Input Array Is Sorted

**Platform**: LeetCode 167 · **Difficulty**: Medium · **Topics**: Array, Two Pointers, Binary Search · **Pattern**: Converging pointers on sorted array

---

## 📜 Problem Statement

Given a **1-indexed** array of integers `numbers` that is already **sorted in non-decreasing order**, find two numbers such that they add up to a specific `target` number. Return the indices of the two numbers (1-indexed) as `[index1, index2]` where `index1 < index2`.

The tests are generated such that there is **exactly one solution**. You may **not** use the same element twice. Your solution must use only **constant extra space**.

### Examples

**Example 1:**
```
Input:  numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: 2 + 7 = 9. Indices are 1 and 2.
```

**Example 2:**
```
Input:  numbers = [2,3,4], target = 6
Output: [1,3]
```

**Example 3:**
```
Input:  numbers = [-1,0], target = -1
Output: [1,2]
```

### Constraints
```
2 <= numbers.length <= 3 * 10^4
-1000 <= numbers[i] <= 1000
numbers is sorted in non-decreasing order.
-1000 <= target <= 1000
Exactly one solution exists.
```

---

## 🧠 Understanding the problem

The array is **sorted** — this is the key. Sorting enables two pointers (O(n)) or binary search (O(n log n)). The O(1) space constraint rules out a hash map (which would be O(n) space). So two pointers is the intended approach.

---

## Approach 1 — Brute force (all pairs)

### Intuition
Try every pair (i, j) with i < j.

### Code
```cpp
vector<int> twoSum(vector<int>& numbers, int target) {
    int n = numbers.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (numbers[i] + numbers[j] == target) return {i+1, j+1};
    return {};
}
```
```java
public int[] twoSum(int[] numbers, int target) {
    int n = numbers.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (numbers[i] + numbers[j] == target) return new int[]{i+1, j+1};
    return new int[]{};
}
```
```python
def twoSum(numbers, target):
    n = len(numbers)
    for i in range(n):
        for j in range(i+1, n):
            if numbers[i] + numbers[j] == target:
                return [i+1, j+1]
```

### Complexity
- **Time**: O(n²). **Space**: O(1).

### Verdict
Correct but too slow. Doesn't exploit the sorted property.

---

## Approach 2 — Binary search for complement

### Intuition
For each `i`, binary-search for `target - numbers[i]` in the remaining array.

### Code
```cpp
vector<int> twoSum(vector<int>& numbers, int target) {
    int n = numbers.size();
    for (int i = 0; i < n; i++) {
        int need = target - numbers[i];
        int lo = i + 1, hi = n - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (numbers[mid] == need) return {i+1, mid+1};
            else if (numbers[mid] < need) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return {};
}
```
```java
public int[] twoSum(int[] numbers, int target) {
    int n = numbers.length;
    for (int i = 0; i < n; i++) {
        int need = target - numbers[i];
        int lo = i + 1, hi = n - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (numbers[mid] == need) return new int[]{i+1, mid+1};
            else if (numbers[mid] < need) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return new int[]{};
}
```
```python
import bisect
def twoSum(numbers, target):
    for i in range(len(numbers)):
        need = target - numbers[i]
        j = bisect.bisect_left(numbers, need, i+1)
        if j < len(numbers) and numbers[j] == need:
            return [i+1, j+1]
```

### Complexity
- **Time**: O(n log n). **Space**: O(1).

### Verdict
Better than brute, uses sorted property. But two pointers is even faster.

---

## Approach 3 — Two pointers (optimal) ⭐

### Intuition
Start with `l=0` (smallest) and `r=n-1` (largest). Their sum is either:
- **Too small** → move `l` right (increase the sum).
- **Too big** → move `r` left (decrease the sum).
- **Equal** → found.

Because the array is sorted, this is guaranteed to find the unique solution in one pass.

### Why it works (proof sketch)
At any point, if the answer is `(i, j)` with `l ≤ i < j ≤ r`, we haven't eliminated it. Moving `l` right is safe when `sum < target` (the answer can't use the current `l` — it's too small). Moving `r` left is safe when `sum > target` (same logic). So the answer is never skipped.

### Code
```cpp
vector<int> twoSum(vector<int>& numbers, int target) {
    int l = 0, r = numbers.size() - 1;
    while (l < r) {
        int sum = numbers[l] + numbers[r];
        if (sum == target) return {l + 1, r + 1};
        else if (sum < target) l++;
        else r--;
    }
    return {};
}
```
```java
public int[] twoSum(int[] numbers, int target) {
    int l = 0, r = numbers.length - 1;
    while (l < r) {
        int sum = numbers[l] + numbers[r];
        if (sum == target) return new int[]{l + 1, r + 1};
        else if (sum < target) l++;
        else r--;
    }
    return new int[]{};
}
```
```python
def twoSum(numbers, target):
    l, r = 0, len(numbers) - 1
    while l < r:
        s = numbers[l] + numbers[r]
        if s == target:
            return [l + 1, r + 1]
        elif s < target:
            l += 1
        else:
            r -= 1
```

### Complexity
- **Time**: O(n) — each pointer moves at most n times total.
- **Space**: O(1).

### Verdict
**The optimal answer.** O(n) time, O(1) space, exploits sorted property perfectly.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Uses sorted? |
|----------|------|-------|--------------|
| Brute force | O(n²) | O(1) | no |
| Binary search | O(n log n) | O(1) | yes |
| Two pointers | **O(n)** | **O(1)** | yes ⭐ |
| Hash map (LC 1 style) | O(n) | O(n) | no (violates O(1) space) |

---

## 🧪 Edge cases & pitfalls
- **Negative numbers** → arithmetic works unchanged.
- **Duplicates** → two pointers handles naturally (e.g., `[1,1,2]` target 2 → [1,2]).
- **1-indexed output** → don't forget `+1`.
- **Pitfall**: using a hash map violates the "constant extra space" constraint.

---

## 🔗 Related problems
- **Two Sum** (LC 1) — unsorted, hash map approach.
- **3Sum** (LC 15) — fix one, two-pointer on rest.
- **4Sum** (LC 18) — fix two, two-pointer on rest.
- **Two Sum Less Than K** (LC 1099).

---

**→ Next:** [`03-3Sum.md`](./03-3Sum.md) | Prev: [`01-Valid-Palindrome.md`](./01-Valid-Palindrome.md) | [Index](./00-Index.md)
