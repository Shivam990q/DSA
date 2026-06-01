# Longest Increasing Subsequence

**Platform**: LeetCode 300 · **Difficulty**: Medium · **Topics**: Array, Binary Search, Dynamic Programming · **Pattern**: Subsequence DP → patience sorting (tails array)

---

## 📜 Problem Statement

Given an integer array `nums`, return the **length of the longest strictly increasing subsequence**.

A **subsequence** is a sequence that can be derived from an array by deleting some or no elements without changing the order of the remaining elements.

### Examples

**Example 1:**
```
Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4
Explanation: The longest increasing subsequence is [2, 3, 7, 101], length 4.
```

**Example 2:**
```
Input:  nums = [0, 1, 0, 3, 2, 3]
Output: 4
Explanation: [0, 1, 2, 3] has length 4.
```

**Example 3:**
```
Input:  nums = [7, 7, 7, 7, 7, 7, 7]
Output: 1
Explanation: Strictly increasing — equal elements don't extend, so length 1.
```

### Constraints
```
1 <= nums.length <= 2500
-10^4 <= nums[i] <= 10^4
```

> Follow-up: Can you come up with an algorithm that runs in O(n log n) time?

---

## 🧠 Understanding the problem

We want the longest chain `nums[i1] < nums[i2] < ...` with increasing indices. Two angles:

- **DP angle**: the longest increasing subsequence *ending at index i* is `1 + max(dp[j])` over all earlier `j` with `nums[j] < nums[i]`. That's O(n²).
- **Greedy + binary search angle**: maintain `tails`, where `tails[k]` is the **smallest possible tail value** of any increasing subsequence of length `k+1`. Keeping tails as small as possible leaves the most room to extend later. Each number either extends `tails` (new longest) or replaces the first tail `>= it`. The length of `tails` is the answer. That's O(n log n).

5-step framework (DP version):
1. **State**: `dp[i]` = length of the LIS ending exactly at index `i`.
2. **Transition**: `dp[i] = 1 + max(dp[j] : j < i and nums[j] < nums[i])`.
3. **Base case**: `dp[i] = 1` (the element alone).
4. **Order**: `i` increasing.
5. **Answer**: `max(dp)`.

---

## Approach 1 — O(n²) dynamic programming

### Intuition
For each `i`, look back at every `j < i`; if `nums[j] < nums[i]`, the subsequence ending at `j` can be extended by `nums[i]`.

### Algorithm
1. Init `dp[i] = 1` for all `i`.
2. For `i` from 0, for `j` from 0 to i-1: if `nums[j] < nums[i]`, `dp[i] = max(dp[i], dp[j] + 1)`.
3. Return the maximum `dp[i]`.

### Dry run on `nums = [10, 9, 2, 5, 3, 7]`
```
dp=[1,1,1,1,1,1]
i=3(5): j=2(2<5) dp[3]=2
i=4(3): j=2(2<3) dp[4]=2
i=5(7): j=2->2,3->2,4->2; dp[5]=max(2+1)=3 (via 2,5,7 or 2,3,7)
max dp = 3 (here; full array gives 4 with 101/18 etc.)
```

### Code
```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        int n = nums.size(), best = 1;
        vector<int> dp(n, 1);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++)
                if (nums[j] < nums[i])
                    dp[i] = max(dp[i], dp[j] + 1);
            best = max(best, dp[i]);
        }
        return best;
    }
};
```
```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int n = nums.length, best = 1;
        int[] dp = new int[n];
        java.util.Arrays.fill(dp, 1);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++)
                if (nums[j] < nums[i])
                    dp[i] = Math.max(dp[i], dp[j] + 1);
            best = Math.max(best, dp[i]);
        }
        return best;
    }
}
```
```python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [1] * n
        best = 1
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
            best = max(best, dp[i])
        return best
```

### Complexity
- **Time**: O(n²).
- **Space**: O(n).

### Verdict
Passes the constraints (n ≤ 2500 → ~6M ops) and reconstructs easily, but doesn't satisfy the O(n log n) follow-up.

---

## Approach 2 — Patience sorting with binary search (optimal) ⭐

### Intuition
Keep `tails` so that `tails[k]` is the smallest tail of any increasing subsequence of length `k+1`. `tails` is always sorted. For each `x`, binary-search the first tail `>= x` (`lower_bound` for *strict* increase): replacing it keeps tails as small as possible; if none exists, `x` extends the longest chain. The answer is `len(tails)`.

### Algorithm
1. `tails = []`.
2. For each `x`: find `pos = lowerBound(tails, x)`.
   - If `pos == len(tails)`: append `x` (longer chain).
   - Else: `tails[pos] = x` (tighten that length's tail).
3. Return `len(tails)`.

### Dry run on `nums = [10, 9, 2, 5, 3, 7, 101, 18]`
```
10 -> [10]
9  -> replace 10 -> [9]
2  -> replace 9  -> [2]
5  -> append -> [2,5]
3  -> replace 5 -> [2,3]
7  -> append -> [2,3,7]
101-> append -> [2,3,7,101]
18 -> replace 101 -> [2,3,7,18]
len = 4
```

### Code
```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        vector<int> tails;
        for (int x : nums) {
            auto it = lower_bound(tails.begin(), tails.end(), x);
            if (it == tails.end()) tails.push_back(x);
            else *it = x;
        }
        return tails.size();
    }
};
```
```java
class Solution {
    public int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int x : nums) {
            int lo = 0, hi = size;
            while (lo < hi) {                 // lower_bound: first tail >= x
                int mid = (lo + hi) >>> 1;
                if (tails[mid] < x) lo = mid + 1;
                else hi = mid;
            }
            tails[lo] = x;
            if (lo == size) size++;
        }
        return size;
    }
}
```
```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails = []
        for x in nums:
            i = bisect.bisect_left(tails, x)   # first tail >= x
            if i == len(tails):
                tails.append(x)
            else:
                tails[i] = x
        return len(tails)
```

### Complexity
- **Time**: O(n log n) — binary search per element.
- **Space**: O(n) for `tails`.

### Verdict
**The optimal answer** and the follow-up's target. Caveat: `tails` is **not** an actual longest subsequence — only its *length* is meaningful. Reconstructing the subsequence needs an extra parent-index array.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| O(n²) DP | O(n²) | O(n) | intuitive, reconstructs easily |
| Patience + binary search | **O(n log n)** | **O(n)** | the answer / follow-up ⭐ |

For the **longest non-decreasing** subsequence, switch `bisect_left` → `bisect_right` (`lower_bound` → `upper_bound`), allowing equal values to extend.

---

## 🧪 Edge cases & pitfalls
- **All equal** (`[7,7,7]`) → 1: strict increase means equals don't extend; `lower_bound` always replaces position 0.
- **Strictly decreasing** (`[5,4,3]`) → 1: every element replaces `tails[0]`.
- **Single element** → 1.
- **Pitfall — `lower_bound` vs `upper_bound`**: strict LIS needs `lower_bound`/`bisect_left`. Using `upper_bound` would compute the longest *non-decreasing* subsequence and overcount on duplicates.
- **Pitfall — treating `tails` as the subsequence**: its contents can be a mix of values that never coexisted in one subsequence. Only `len(tails)` is the answer.

---

## 🔗 Related problems
- **Number of Longest Increasing Subsequences** (LC 673) — count, not just length (O(n²) DP with counts).
- **Russian Doll Envelopes** (LC 354) — 2D LIS after a clever sort.
- **Longest Increasing Path in a Matrix** (LC 329) — LIS idea on a grid via DFS + memo.
- **Maximum Length of Pair Chain** (LC 646) — interval LIS variant.

---

**→ Next:** [`12-Partition-Equal-Subset-Sum.md`](./12-Partition-Equal-Subset-Sum.md) | **→ Prev:** [`10-Word-Break.md`](./10-Word-Break.md) | Back to [`00-Index.md`](./00-Index.md)
