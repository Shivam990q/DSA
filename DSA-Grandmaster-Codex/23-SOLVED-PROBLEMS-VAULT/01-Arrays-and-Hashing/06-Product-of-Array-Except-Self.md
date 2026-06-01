# Product of Array Except Self

**Platform**: LeetCode 238 · **Difficulty**: Medium · **Topics**: Array, Prefix/Suffix products · **Pattern**: Prefix-suffix accumulation

---

## 📜 Problem Statement

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the **product of all the elements of `nums` except `nums[i]`**.

The product of any prefix or suffix of `nums` is **guaranteed to fit in a 32-bit integer**.

You must write an algorithm that runs in **O(n)** time and **without using the division operation**.

### Examples

**Example 1:**
```
Input:  nums = [1,2,3,4]
Output: [24,12,8,6]
Explanation: answer[0]=2*3*4=24, answer[1]=1*3*4=12, answer[2]=1*2*4=8, answer[3]=1*2*3=6.
```

**Example 2:**
```
Input:  nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

### Constraints
```
2 <= nums.length <= 10^5
-30 <= nums[i] <= 30
The product of any prefix or suffix fits in a 32-bit integer.
```

### Follow-up
Can you solve it in O(1) **extra** space? (The output array doesn't count as extra space.)

---

## 🧠 Understanding the problem

Two explicit handcuffs: **no division** and **O(n)**. Without those, the answer is trivially "total product / nums[i]". The no-division rule (and the zero case it protects against) forces a structural insight:

> The product of everything except index `i` = (product of everything to the **left** of `i`) × (product of everything to the **right** of `i`).

If we precompute left-products and right-products, each answer is one multiplication.

---

## Approach 1 — Division (what NOT to do, and why)

### Intuition
Compute the total product, then `answer[i] = total / nums[i]`.

### Why it fails
- The problem **forbids division**.
- Even if allowed, a **zero** in the array breaks division (`total/0`). You'd need special-casing: if exactly one zero, only its index is non-zero; if two or more zeros, all zero. Messy and against the rules.

```cpp
// Illustration only — disallowed by the problem.
vector<int> productExceptSelf(vector<int>& nums) {
    int total = 1, zeros = 0, zeroIdx = -1;
    for (int i = 0; i < nums.size(); i++) {
        if (nums[i] == 0) { zeros++; zeroIdx = i; }
        else total *= nums[i];
    }
    vector<int> res(nums.size(), 0);
    if (zeros > 1) return res;
    if (zeros == 1) { res[zeroIdx] = total; return res; }
    for (int i = 0; i < nums.size(); i++) res[i] = total / nums[i];
    return res;
}
```
```java
// Illustration only — disallowed by the problem.
public int[] productExceptSelf(int[] nums) {
    int total = 1, zeros = 0, zeroIdx = -1;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] == 0) { zeros++; zeroIdx = i; }
        else total *= nums[i];
    }
    int[] res = new int[nums.length];
    if (zeros > 1) return res;
    if (zeros == 1) { res[zeroIdx] = total; return res; }
    for (int i = 0; i < nums.length; i++) res[i] = total / nums[i];
    return res;
}
```

### Verdict
Educational only. Demonstrates *why* the constraints push us to prefix/suffix products.

---

## Approach 2 — Prefix and suffix arrays

### Intuition
Build two arrays: `left[i]` = product of all elements before `i`, `right[i]` = product of all elements after `i`. Then `answer[i] = left[i] * right[i]`.

### Algorithm
1. `left[0] = 1`; for `i ≥ 1`: `left[i] = left[i-1] * nums[i-1]`.
2. `right[n-1] = 1`; for `i ≤ n-2`: `right[i] = right[i+1] * nums[i+1]`.
3. `answer[i] = left[i] * right[i]`.

### Dry run on `[1,2,3,4]`
```
left  = [1, 1, 2, 6]      (1, 1, 1*2, 1*2*3)
right = [24, 12, 4, 1]    (2*3*4, 3*4, 4, 1)
answer= [1*24, 1*12, 2*4, 6*1] = [24, 12, 8, 6]
```

### Code
```cpp
vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> left(n), right(n), res(n);
    left[0] = 1;
    for (int i = 1; i < n; i++) left[i] = left[i-1] * nums[i-1];
    right[n-1] = 1;
    for (int i = n-2; i >= 0; i--) right[i] = right[i+1] * nums[i+1];
    for (int i = 0; i < n; i++) res[i] = left[i] * right[i];
    return res;
}
```
```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] left = new int[n], right = new int[n], res = new int[n];
    left[0] = 1;
    for (int i = 1; i < n; i++) left[i] = left[i-1] * nums[i-1];
    right[n-1] = 1;
    for (int i = n-2; i >= 0; i--) right[i] = right[i+1] * nums[i+1];
    for (int i = 0; i < n; i++) res[i] = left[i] * right[i];
    return res;
}
```
```python
def productExceptSelf(nums):
    n = len(nums)
    left, right, res = [1]*n, [1]*n, [0]*n
    for i in range(1, n):
        left[i] = left[i-1] * nums[i-1]
    for i in range(n-2, -1, -1):
        right[i] = right[i+1] * nums[i+1]
    for i in range(n):
        res[i] = left[i] * right[i]
    return res
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) for the two helper arrays.

### Verdict
Meets time and no-division. But uses O(n) extra space — the follow-up wants O(1) extra.

---

## Approach 3 — O(1) extra space (optimal) ⭐

### Intuition
Fold the two passes into the output array itself. First pass: store the left-product directly in `res`. Second pass: walk right-to-left with a single running `right` variable, multiplying it into `res[i]`.

### Algorithm
1. `res[i] = product of everything left of i` (first pass; `res[0]=1`).
2. Maintain `right = 1`. Walk `i` from `n-1` to `0`: `res[i] *= right; right *= nums[i]`.

### Dry run on `[1,2,3,4]`
```
Pass 1 (left products): res = [1, 1, 2, 6]
Pass 2 (right running):
  i=3: res[3]=6*1=6;   right=1*4=4
  i=2: res[2]=2*4=8;   right=4*3=12
  i=1: res[1]=1*12=12; right=12*2=24
  i=0: res[0]=1*24=24; right=24*1=24
res = [24, 12, 8, 6]
```

### Code
```cpp
vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> res(n, 1);
    for (int i = 1; i < n; i++) res[i] = res[i-1] * nums[i-1];  // left products
    int right = 1;
    for (int i = n-1; i >= 0; i--) {
        res[i] *= right;
        right *= nums[i];
    }
    return res;
}
```
```java
public int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] res = new int[n];
    res[0] = 1;
    for (int i = 1; i < n; i++) res[i] = res[i-1] * nums[i-1];  // left products
    int right = 1;
    for (int i = n-1; i >= 0; i--) {
        res[i] *= right;
        right *= nums[i];
    }
    return res;
}
```
```python
def productExceptSelf(nums):
    n = len(nums)
    res = [1] * n
    for i in range(1, n):
        res[i] = res[i-1] * nums[i-1]
    right = 1
    for i in range(n-1, -1, -1):
        res[i] *= right
        right *= nums[i]
    return res
```

### Complexity
- **Time**: O(n).
- **Space**: O(1) extra (output array excluded, as the problem allows).

### Verdict
**The optimal answer** that satisfies every constraint: O(n), no division, O(1) extra space. The zero case (Example 2) just works — no special handling — because we never divide.

---

## ⚖️ Approach comparison

| Approach | Time | Extra space | Division? | Allowed |
|----------|------|-------------|-----------|---------|
| Division | O(n) | O(1) | yes | ❌ forbidden |
| Prefix + suffix arrays | O(n) | O(n) | no | ✅ but not O(1) space |
| Two-pass into output | **O(n)** | **O(1)** | no | ✅ optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **One zero** → only that index gets a non-zero product; all others are 0. Handled automatically.
- **Two or more zeros** → every answer is 0. Handled automatically.
- **Negative numbers** → signs multiply normally.
- **Pitfall**: thinking you need division. The whole point is the prefix/suffix decomposition, which sidesteps zeros entirely.

---

## 🔗 Related problems
- **Maximum Product Subarray** (LC 152) — running max/min products.
- **Range Sum Query – Immutable** (LC 303) — the additive analogue (prefix sums).
- **Trapping Rain Water** (LC 42) — also uses left/right precomputation.

---

**→ Next:** [`07-Longest-Consecutive-Sequence.md`](./07-Longest-Consecutive-Sequence.md) | Prev: [`05-Top-K-Frequent-Elements.md`](./05-Top-K-Frequent-Elements.md) | [Index](./00-Index.md)
