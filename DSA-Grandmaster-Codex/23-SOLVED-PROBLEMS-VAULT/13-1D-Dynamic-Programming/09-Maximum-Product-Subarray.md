# Maximum Product Subarray

**Platform**: LeetCode 152 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming · **Pattern**: Running best ending here — track max AND min

---

## 📜 Problem Statement

Given an integer array `nums`, find a subarray that has the **largest product**, and return the product.

The test cases are generated so that the answer will fit in a **32-bit** integer.

A **subarray** is a contiguous non-empty sequence of elements within an array.

### Examples

**Example 1:**
```
Input:  nums = [2, 3, -2, 4]
Output: 6
Explanation: [2, 3] has the largest product 6.
```

**Example 2:**
```
Input:  nums = [-2, 0, -1]
Output: 0
Explanation: The result cannot be 2, because [-2, -1] is not contiguous.
```

**Example 3:**
```
Input:  nums = [-2, 3, -4]
Output: 24
Explanation: The whole array [-2, 3, -4] has product 24.
```

### Constraints
```
1 <= nums.length <= 2 * 10^4
-10 <= nums[i] <= 10
The product of any subarray is guaranteed to fit in a 32-bit integer.
```

---

## 🧠 Understanding the problem

For *sums*, the running-best (Kadane) approach tracks one value: the best subarray ending here. **Products break that** because of signs:

- A **negative** number flips the sign: the largest product so far becomes the smallest, and vice versa.
- A **zero** annihilates any product, resetting the run.

So the maximum product ending at `i` could come from `nums[i]` alone, from `maxEndingHere * nums[i]`, or — if `nums[i]` is negative — from `minEndingHere * nums[i]` (a very negative running min times a negative becomes a big positive). We must therefore track **both** the running max and the running min.

5-step framework:
1. **State**: `curMax`, `curMin` = the max / min product of a subarray ending at the current index.
2. **Transition**: with `x = nums[i]`, `curMax = max(x, curMax·x, curMin·x)` and `curMin = min(x, curMax·x, curMin·x)`.
3. **Base case**: `curMax = curMin = nums[0]`.
4. **Order**: left to right.
5. **Answer**: the max of all `curMax` values seen.

---

## Approach 1 — Brute force (all subarrays)

### Intuition
Try every subarray, multiply it out, keep the maximum.

### Algorithm
1. For each start `i`, run a product over `j = i..n-1`, updating the global best.

### Dry run on `nums = [2, 3, -2, 4]`
```
i=0: 2, 6, -12, -48
i=1: 3, -6, -24
i=2: -2, -8
i=3: 4
best = 6
```

### Code
```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int n = nums.size(), best = nums[0];
        for (int i = 0; i < n; i++) {
            int prod = 1;
            for (int j = i; j < n; j++) {
                prod *= nums[j];
                best = max(best, prod);
            }
        }
        return best;
    }
};
```
```java
class Solution {
    public int maxProduct(int[] nums) {
        int n = nums.length, best = nums[0];
        for (int i = 0; i < n; i++) {
            int prod = 1;
            for (int j = i; j < n; j++) {
                prod *= nums[j];
                best = Math.max(best, prod);
            }
        }
        return best;
    }
}
```
```python
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        n = len(nums)
        best = nums[0]
        for i in range(n):
            prod = 1
            for j in range(i, n):
                prod *= nums[j]
                best = max(best, prod)
        return best
```

### Complexity
- **Time**: O(n²).
- **Space**: O(1).

### Verdict
Correct, fine for small inputs, but O(n²) risks TLE near n = 2×10⁴. The insight below makes it linear.

---

## Approach 2 — Track running max and min (optimal) ⭐

### Intuition
Carry both the best and worst product ending at the current position. When the new element is negative, the roles swap (max↔min) before we extend, because multiplying by a negative turns the largest into the smallest. Restarting the run from `x` alone handles zeros and sign resets automatically.

### Algorithm
1. `best = curMax = curMin = nums[0]`.
2. For each `x` from index 1:
   - If `x < 0`, swap `curMax` and `curMin`.
   - `curMax = max(x, curMax * x)`.
   - `curMin = min(x, curMin * x)`.
   - `best = max(best, curMax)`.
3. Return `best`.

### Dry run on `nums = [-2, 3, -4]`
```
start: best=curMax=curMin=-2
x=3 (>=0): curMax=max(3,-6)=3; curMin=min(3,-6)=-6; best=max(-2,3)=3
x=-4 (<0): swap -> curMax=-6, curMin=3
           curMax=max(-4, -6*-4=24)=24; curMin=min(-4, 3*-4=-12)=-12
           best=max(3,24)=24
return 24
```

### Code
```cpp
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int best = nums[0], curMax = nums[0], curMin = nums[0];
        for (int i = 1; i < (int)nums.size(); i++) {
            int x = nums[i];
            if (x < 0) swap(curMax, curMin);
            curMax = max(x, curMax * x);
            curMin = min(x, curMin * x);
            best = max(best, curMax);
        }
        return best;
    }
};
```
```java
class Solution {
    public int maxProduct(int[] nums) {
        int best = nums[0], curMax = nums[0], curMin = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            if (x < 0) {
                int t = curMax; curMax = curMin; curMin = t;
            }
            curMax = Math.max(x, curMax * x);
            curMin = Math.min(x, curMin * x);
            best = Math.max(best, curMax);
        }
        return best;
    }
}
```
```python
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        best = cur_max = cur_min = nums[0]
        for x in nums[1:]:
            if x < 0:
                cur_max, cur_min = cur_min, cur_max
            cur_max = max(x, cur_max * x)
            cur_min = min(x, cur_min * x)
            best = max(best, cur_max)
        return best
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**The optimal answer.** The whole trick is "track the min alongside the max so a future negative can turn it into the max."

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n²) | O(1) | baseline, may TLE at 2×10⁴ |
| Track max & min | **O(n)** | **O(1)** | the answer ⭐ |

A symmetric alternative to the swap trick is the **prefix/suffix product** scan: sweep products left-to-right and right-to-left, resetting to 1 after a zero, and take the max seen. It's also O(n)/O(1) and avoids the explicit min tracking — handy to mention as a second optimal.

---

## 🧪 Edge cases & pitfalls
- **Single element** → that element (even if negative). The init `best = nums[0]` covers it.
- **Contains zero** (`[-2, 0, -1]`) → multiplying by 0 collapses the run; restarting from `x` lets the run recover after the zero.
- **All negatives** (`[-2, -3, -4]`) → an even count multiplies to a large positive; an odd count means dropping one factor. The min-tracking handles both.
- **Pitfall — using only the running max** (Kadane-for-sums) → fails on `[-2, 3, -4]`, returning 3 instead of 24.
- **Pitfall — overwriting `curMax` before computing `curMin`**: compute `curMin` from the *old* `curMax`. Either swap first (as here) or stash the old value before reassigning.

---

## 🔗 Related problems
- **Maximum Subarray** (LC 53) — the additive version (Kadane), single running value.
- **Product of Array Except Self** (LC 238) — prefix/suffix products without division.
- **Subarray Product Less Than K** (LC 713) — sliding window on products.
- **Maximum Product of Three Numbers** (LC 628) — sign-handling with sorting.

---

**→ Next:** [`10-Word-Break.md`](./10-Word-Break.md) | **→ Prev:** [`08-Coin-Change.md`](./08-Coin-Change.md) | Back to [`00-Index.md`](./00-Index.md)
