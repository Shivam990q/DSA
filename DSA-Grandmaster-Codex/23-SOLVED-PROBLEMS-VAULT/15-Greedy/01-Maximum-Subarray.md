# Maximum Subarray

**Platform**: LeetCode 53 · **Difficulty**: Medium · **Topics**: Array, Divide and Conquer, Dynamic Programming · **Pattern**: Kadane / running-state scan

---

## 📜 Problem Statement

Given an integer array `nums`, find the **contiguous subarray** (containing at least one number) which has the largest sum, and return *its sum*.

A **subarray** is a contiguous, non-empty sequence of elements within an array.

### Examples

**Example 1:**
```
Input:  nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.
```

**Example 2:**
```
Input:  nums = [1]
Output: 1
Explanation: The single element 1 is the whole subarray.
```

**Example 3:**
```
Input:  nums = [5,4,-1,7,8]
Output: 23
Explanation: The entire array sums to 23.
```

### Constraints
```
1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
```

**Follow-up**: If you have figured out the O(n) solution, try coding another solution using the **divide and conquer** approach, which is more subtle.

---

## 🧠 Understanding the problem

We want a window of consecutive elements whose sum is maximal. The catch is the negative numbers — a subarray can dip through a negative as long as the surrounding positives more than pay for it (that's why `[4,-1,2,1]` beats `[4]` alone).

The single most important observation: while scanning left to right, ask of each prefix sum *"is the running total still helping me, or is it dragging me down?"* The moment a running sum becomes negative, it can only **hurt** any subarray that extends past it — you'd be better off starting fresh from the next element. That one idea is Kadane's algorithm.

A second observation handles the all-negative case: we must pick **at least one** element, so the answer is the largest single value when everything is negative. Initializing the answer to `nums[0]` (not `0`) captures this.

---

## Approach 1 — Brute force (every subarray)

### Intuition
Enumerate every start `i` and end `j`, sum the elements between them, and keep the max. This is the literal definition.

### Algorithm
1. Initialize `best = -∞`.
2. For each start `i` from `0` to `n-1`:
   - Maintain a running `sum = 0`.
   - For each end `j` from `i` to `n-1`: add `nums[j]` to `sum`, update `best`.
3. Return `best`.

(The inner running sum avoids a third loop, keeping this at O(n²) rather than O(n³).)

### Dry run on `[-2, 1, -3, 4]`
```
i=0: sums -2, -1, -4, 0           → best so far 0
i=1: sums 1, -2, 2                → best 2
i=2: sums -3, 1                   → best 2
i=3: sums 4                       → best 4
answer = 4
```

### Code
```cpp
int maxSubArray(vector<int>& nums) {
    int n = nums.size();
    int best = INT_MIN;
    for (int i = 0; i < n; i++) {
        int sum = 0;
        for (int j = i; j < n; j++) {
            sum += nums[j];
            best = max(best, sum);
        }
    }
    return best;
}
```
```java
public int maxSubArray(int[] nums) {
    int n = nums.length;
    int best = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        int sum = 0;
        for (int j = i; j < n; j++) {
            sum += nums[j];
            best = Math.max(best, sum);
        }
    }
    return best;
}
```
```python
def maxSubArray(nums):
    n = len(nums)
    best = float('-inf')
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            best = max(best, s)
    return best
```

### Complexity
- **Time**: O(n²) — ~10^10 operations at n = 10^5. **Will TLE.**
- **Space**: O(1).

### Verdict
Correct baseline, too slow. It does prove we understand "contiguous" and that we must allow at least one element.

---

## Approach 2 — Divide and conquer

### Intuition
Split the array in half. The maximum subarray is one of three things: entirely in the **left** half, entirely in the **right** half, or it **crosses** the midpoint. The first two come from recursion; the crossing one is the best suffix of the left half joined to the best prefix of the right half.

### Algorithm
1. Base case: a single element returns itself.
2. Recurse on left half and right half.
3. Compute the **cross sum**: from `mid` walk left accumulating the max suffix, from `mid+1` walk right accumulating the max prefix; add them.
4. Return `max(left, right, cross)`.

### Dry run on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`
```
The recursion eventually isolates [4,-1,2,1] across a midpoint:
  best suffix ending at the split + best prefix after it = 4 + (-1+2+1) = 6
Left/right halves never beat 6 → answer 6.
```

### Code
```cpp
class Solution {
    int solve(vector<int>& nums, int lo, int hi) {
        if (lo == hi) return nums[lo];
        int mid = lo + (hi - lo) / 2;
        int leftBest = solve(nums, lo, mid);
        int rightBest = solve(nums, mid + 1, hi);
        int sum = 0, leftCross = INT_MIN;
        for (int i = mid; i >= lo; i--) { sum += nums[i]; leftCross = max(leftCross, sum); }
        sum = 0; int rightCross = INT_MIN;
        for (int i = mid + 1; i <= hi; i++) { sum += nums[i]; rightCross = max(rightCross, sum); }
        int cross = leftCross + rightCross;
        return max({leftBest, rightBest, cross});
    }
public:
    int maxSubArray(vector<int>& nums) {
        return solve(nums, 0, nums.size() - 1);
    }
};
```
```java
public int maxSubArray(int[] nums) {
    return solve(nums, 0, nums.length - 1);
}
private int solve(int[] nums, int lo, int hi) {
    if (lo == hi) return nums[lo];
    int mid = lo + (hi - lo) / 2;
    int leftBest = solve(nums, lo, mid);
    int rightBest = solve(nums, mid + 1, hi);
    int sum = 0, leftCross = Integer.MIN_VALUE;
    for (int i = mid; i >= lo; i--) { sum += nums[i]; leftCross = Math.max(leftCross, sum); }
    sum = 0; int rightCross = Integer.MIN_VALUE;
    for (int i = mid + 1; i <= hi; i++) { sum += nums[i]; rightCross = Math.max(rightCross, sum); }
    int cross = leftCross + rightCross;
    return Math.max(Math.max(leftBest, rightBest), cross);
}
```
```python
def maxSubArray(nums):
    def solve(lo, hi):
        if lo == hi:
            return nums[lo]
        mid = (lo + hi) // 2
        left_best = solve(lo, mid)
        right_best = solve(mid + 1, hi)
        s, left_cross = 0, float('-inf')
        for i in range(mid, lo - 1, -1):
            s += nums[i]
            left_cross = max(left_cross, s)
        s, right_cross = 0, float('-inf')
        for i in range(mid + 1, hi + 1):
            s += nums[i]
            right_cross = max(right_cross, s)
        return max(left_best, right_best, left_cross + right_cross)
    return solve(0, len(nums) - 1)
```

### Complexity
- **Time**: O(n log n) — `T(n) = 2T(n/2) + O(n)`.
- **Space**: O(log n) recursion stack.

### Verdict
This is the answer to the **follow-up**. Elegant, but slower and heavier than Kadane. Worth knowing for the "another approach" prompt and as a segment-tree warm-up.

---

## Approach 3 — Kadane's algorithm (greedy / DP) ⭐

### Intuition
Carry a single running sum `cur`. At each element decide: *extend* the previous subarray (`cur + x`) or *start fresh* at `x`. Pick whichever is larger. Whenever `cur` would go negative it's never worth carrying forward, so starting fresh wins automatically. Track the best `cur` ever seen.

The DP framing: let `cur` = the maximum subarray sum **ending at index i**. Then `cur = max(nums[i], cur + nums[i])`, and the answer is the max `cur` over all `i`.

### Algorithm
1. `best = cur = nums[0]`.
2. For each `x` in `nums[1:]`:
   - `cur = max(x, cur + x)`.
   - `best = max(best, cur)`.
3. Return `best`.

### Dry run on `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`
```
start: best=cur=-2
x=1 : cur=max(1,-2+1=-1)=1     best=1
x=-3: cur=max(-3,1-3=-2)=-2    best=1
x=4 : cur=max(4,-2+4=2)=4      best=4
x=-1: cur=max(-1,4-1=3)=3      best=4
x=2 : cur=max(2,3+2=5)=5       best=5
x=1 : cur=max(1,5+1=6)=6       best=6
x=-5: cur=max(-5,6-5=1)=1      best=6
x=4 : cur=max(4,1+4=5)=5       best=6
answer = 6
```

### Code
```cpp
int maxSubArray(vector<int>& nums) {
    int best = nums[0], cur = nums[0];
    for (int i = 1; i < (int)nums.size(); i++) {
        cur = max(nums[i], cur + nums[i]);
        best = max(best, cur);
    }
    return best;
}
```
```java
public int maxSubArray(int[] nums) {
    int best = nums[0], cur = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);
        best = Math.max(best, cur);
    }
    return best;
}
```
```python
def maxSubArray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**The optimal answer.** One pass, constant space, and the "discard a negative prefix" intuition is easy to explain. This is what you present.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n²) | O(1) | baseline; TLE at 10^5 |
| Divide & conquer | O(n log n) | O(log n) | the follow-up answer |
| Kadane | **O(n)** | **O(1)** | optimal; greedy = DP here ⭐ |

The key dialogue point: Kadane is simultaneously a **greedy** ("drop a prefix that hurts") and a **1D DP** ("best subarray ending here"). Being able to articulate both views signals depth.

---

## 🧪 Edge cases & pitfalls
- **All negatives** (`[-3,-1,-2]`) → answer is `-1`, the largest single element. This is why `best` and `cur` start at `nums[0]`, **not** `0`. Initializing to `0` is the classic bug.
- **Single element** → loop body never runs, returns `nums[0]`.
- **All positives** → the whole array; `cur` keeps growing.
- **Pitfall**: returning the subarray itself. The problem only asks for the *sum*; if asked for indices, track the start whenever you "start fresh."
- **Overflow**: with n ≤ 10^5 and |values| ≤ 10^4 the max magnitude is 10^9, which fits in a 32-bit `int`. For larger constraints use `long`.

---

## 🔗 Related problems
- **Maximum Product Subarray** (LC 152) — track both max and min running products (negatives flip sign).
- **Maximum Sum Circular Subarray** (LC 918) — Kadane plus the "total − minimum subarray" trick.
- **Best Time to Buy and Sell Stock** (LC 121) — Kadane on the difference array.
- **Maximum Subarray Sum with One Deletion** (LC 1186) — Kadane with a "skip one" state.

---

**→ Next:** [`02-Jump-Game.md`](./02-Jump-Game.md) | [Problem set index](./00-Index.md)
