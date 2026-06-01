# Missing Number

**Platform**: LeetCode 268 · **Difficulty**: Easy · **Topics**: Array, Hash Table, Math, Bit Manipulation, Sorting · **Pattern**: XOR fold / sum formula

---

## 📜 Problem Statement

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return *the only number in the range that is missing from the array.*

### Examples

**Example 1:**
```
Input:  nums = [3,0,1]
Output: 2
Explanation: n = 3 since there are 3 numbers, so all numbers are in the range [0,3].
2 is the missing number in the range since it does not appear in nums.
```

**Example 2:**
```
Input:  nums = [0,1]
Output: 2
Explanation: n = 2 since there are 2 numbers, so all numbers are in the range [0,2].
2 is the missing number.
```

**Example 3:**
```
Input:  nums = [9,6,4,2,3,5,7,0,1]
Output: 8
Explanation: n = 9, range [0,9]; 8 is missing.
```

### Constraints
```
n == nums.length
1 <= n <= 10^4
0 <= nums[i] <= n
All the numbers of nums are unique.
```

**Follow up**: Could you implement a solution using only O(1) extra space complexity and O(n) runtime complexity?

---

## 🧠 Understanding the problem

We have `n` distinct values drawn from the `n + 1` candidates `0, 1, …, n`, so exactly one is absent. Three O(n) ideas, two of which meet the O(1)-space follow-up:

1. **Sum formula**: the complete set `0..n` sums to `n(n+1)/2`. Subtract the actual array sum; the difference is the missing number. O(1) space, but the sum could in principle overflow for large `n` (fine for 32-bit here, but be aware).
2. **XOR fold**: XOR all indices `0..n` together with all array values. Every present number appears once as a value and once as an index (or as the extra `n`), so they cancel in pairs; the missing number — which appears as an index but never as a value — survives. No overflow risk.
3. **Hash set**: store all values, then probe `0..n` for the absent one. O(n) space (fails the follow-up).

---

## Approach 1 — Hash set / sorting (baseline)

### Intuition
Put all values in a set, then find which of `0..n` is missing. (Or sort and find the first index mismatch.)

### Algorithm
1. Insert all `nums` into a set.
2. For `i` in `0..n`: if `i` not in set → return `i`.

### Dry run on `[3,0,1]`
```
set={3,0,1}; probe 0✓,1✓,2✗ → return 2
```

### Code
```cpp
int missingNumber(vector<int>& nums) {
    unordered_set<int> s(nums.begin(), nums.end());
    int n = nums.size();
    for (int i = 0; i <= n; i++)
        if (!s.count(i)) return i;
    return -1;  // unreachable
}
```
```java
public int missingNumber(int[] nums) {
    Set<Integer> s = new HashSet<>();
    for (int x : nums) s.add(x);
    int n = nums.length;
    for (int i = 0; i <= n; i++)
        if (!s.contains(i)) return i;
    return -1;  // unreachable
}
```
```python
def missingNumber(nums):
    s = set(nums)
    n = len(nums)
    for i in range(n + 1):
        if i not in s:
            return i
    return -1  # unreachable
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) — **fails the O(1)-space follow-up.**

### Verdict
Simple and clear, but the extra set breaks the constant-space requirement. Use one of the next two.

---

## Approach 2 — XOR fold (optimal) ⭐

### Intuition
XOR all indices `0..n` and all values together. Pairs cancel; the unmatched index is the missing number. Start the accumulator at `n` (the index `n` has no array slot to pair with naturally) and fold in `i ^ nums[i]` for each `i`.

### Algorithm
1. `x = n`.
2. For `i` in `0..n-1`: `x ^= i ^ nums[i]`.
3. Return `x`.

### Dry run on `[3,0,1]` (n = 3)
```
x=3
i=0: x ^= 0 ^ 3 = 3 ^ 0 ^ 3 = 0
i=1: x ^= 1 ^ 0 = 0 ^ 1 ^ 0 = 1
i=2: x ^= 2 ^ 1 = 1 ^ 2 ^ 1 = 2
answer = 2  ✓
```

### Code
```cpp
int missingNumber(vector<int>& nums) {
    int x = nums.size();
    for (int i = 0; i < (int)nums.size(); i++)
        x ^= i ^ nums[i];
    return x;
}
```
```java
public int missingNumber(int[] nums) {
    int x = nums.length;
    for (int i = 0; i < nums.length; i++)
        x ^= i ^ nums[i];
    return x;
}
```
```python
def missingNumber(nums):
    x = len(nums)
    for i, v in enumerate(nums):
        x ^= i ^ v
    return x
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**The optimal answer** — meets the follow-up and never overflows. XOR is the cleanest way to "cancel everything except the gap."

---

## Approach 3 — Gauss sum formula

### Intuition
The full range `0..n` sums to `n(n+1)/2`. Subtract the array's actual sum.

### Algorithm
1. `expected = n*(n+1)/2`.
2. Subtract every element. Return the remainder.

### Dry run on `[9,6,4,2,3,5,7,0,1]` (n = 9)
```
expected = 9*10/2 = 45
actual sum = 37
missing = 45 - 37 = 8  ✓
```

### Code
```cpp
int missingNumber(vector<int>& nums) {
    long long n = nums.size();
    long long total = n * (n + 1) / 2;
    for (int x : nums) total -= x;
    return (int)total;
}
```
```java
public int missingNumber(int[] nums) {
    long n = nums.length;
    long total = n * (n + 1) / 2;
    for (int x : nums) total -= x;
    return (int) total;
}
```
```python
def missingNumber(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
Equally optimal in time and space, very intuitive. Use `long` for the sum to dodge any overflow concern. XOR is preferred when overflow could ever matter, but both are great answers.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Hash set | O(n) | O(n) | fails O(1)-space follow-up |
| XOR fold | **O(n)** | **O(1)** | optimal, no overflow ⭐ |
| Sum formula | O(n) | O(1) | optimal, watch overflow |

---

## 🧪 Edge cases & pitfalls
- **Missing `0`** (`[1,2]`, n=2) → XOR/sum both yield 0... let's verify sum: expected 3, actual 3 → 0. Correct.
- **Missing `n`** (`[0,1]`, n=2) → missing is 2; both methods return 2.
- **Single element** (`[0]` → missing 1, or `[1]` → missing 0) → handled.
- **Pitfall — sum overflow**: with the formula, `n(n+1)/2` can exceed 32-bit for very large `n`; cast to `long`. XOR sidesteps this entirely.
- **Pitfall — XOR seed**: seed the accumulator with `n` (the highest index), otherwise the index `n` is never folded in and the answer is wrong.

---

## 🔗 Related problems
- **Single Number** (LC 136) — pure XOR cancellation (earlier).
- **Find All Numbers Disappeared in an Array** (LC 448) — multiple missing, index-marking.
- **Find the Duplicate Number** (LC 287) — the dual problem.
- **First Missing Positive** (LC 41) — harder, in-place index placement.

---

**→ Next:** [`06-Sum-of-Two-Integers.md`](./06-Sum-of-Two-Integers.md) | **Prev:** [`04-Reverse-Bits.md`](./04-Reverse-Bits.md) | [Problem set index](./00-Index.md)
