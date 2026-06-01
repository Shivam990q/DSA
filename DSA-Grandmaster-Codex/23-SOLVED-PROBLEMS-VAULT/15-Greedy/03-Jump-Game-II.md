# Jump Game II

**Platform**: LeetCode 45 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming, Greedy · **Pattern**: BFS-by-levels / interval greedy

---

## 📜 Problem Statement

You are given a **0-indexed** array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.

Each element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at `nums[i]`, you can jump to any `nums[i + j]` where `0 <= j <= nums[i]` and `i + j < n`.

Return the **minimum number of jumps** to reach `nums[n - 1]`. The test cases are generated such that you can always reach `nums[n - 1]`.

### Examples

**Example 1:**
```
Input:  nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps to reach the last index is 2.
Jump 1 step from index 0 to 1, then 3 steps to the last index.
```

**Example 2:**
```
Input:  nums = [2,3,0,1,4]
Output: 2
```

**Example 3:**
```
Input:  nums = [1]
Output: 0
Explanation: Already at the last index; no jumps needed.
```

### Constraints
```
1 <= nums.length <= 10^4
0 <= nums[i] <= 1000
It's guaranteed that you can reach nums[n - 1].
```

---

## 🧠 Understanding the problem

Now we count jumps, not just feasibility. Think of it as an **unweighted shortest path**: each index is a node, and from `i` there is an edge to every index in `[i+1, i+nums[i]]`. The minimum number of jumps is the BFS distance from `0` to `n-1`.

The beautiful part: we don't need an explicit queue. Because the reachable set from a contiguous range of indices is itself a contiguous range, BFS "levels" become **intervals**. Level 0 is just index `0`. Level 1 is everything reachable from index `0`. Level 2 is everything reachable from level 1, and so on. The number of levels we cross to include `n-1` is the answer. We can track each level with two pointers — the current level's right boundary (`curEnd`) and the farthest index any node in the current level can reach (`farthest`).

---

## Approach 1 — Dynamic programming

### Intuition
`dp[i]` = minimum jumps to reach index `i`. Relax forward: from `i`, every index in its range can be reached in `dp[i]+1` jumps. Take the minimum.

### Algorithm
1. `dp[0] = 0`, all others `= ∞`.
2. For `i` from `0` to `n-1`: for `j` in `[i+1, min(n-1, i+nums[i])]`, `dp[j] = min(dp[j], dp[i]+1)`.
3. Return `dp[n-1]`.

### Dry run on `[2,3,1,1,4]`
```
dp[0]=0
i=0 (reach 1,2): dp[1]=1, dp[2]=1
i=1 (reach 2,3,4): dp[2]=min(1,2)=1, dp[3]=2, dp[4]=2
i=2 (reach 3): dp[3]=min(2,2)=2
i=3 (reach 4): dp[4]=min(2,3)=2
answer dp[4]=2
```

### Code
```cpp
int jump(vector<int>& nums) {
    int n = nums.size();
    vector<int> dp(n, INT_MAX);
    dp[0] = 0;
    for (int i = 0; i < n; i++) {
        if (dp[i] == INT_MAX) continue;
        int far = min(n - 1, i + nums[i]);
        for (int j = i + 1; j <= far; j++)
            dp[j] = min(dp[j], dp[i] + 1);
    }
    return dp[n - 1];
}
```
```java
public int jump(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[0] = 0;
    for (int i = 0; i < n; i++) {
        if (dp[i] == Integer.MAX_VALUE) continue;
        int far = Math.min(n - 1, i + nums[i]);
        for (int j = i + 1; j <= far; j++)
            dp[j] = Math.min(dp[j], dp[i] + 1);
    }
    return dp[n - 1];
}
```
```python
def jump(nums):
    n = len(nums)
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(n):
        if dp[i] == float('inf'):
            continue
        far = min(n - 1, i + nums[i])
        for j in range(i + 1, far + 1):
            dp[j] = min(dp[j], dp[i] + 1)
    return dp[n - 1]
```

### Complexity
- **Time**: O(n²) worst case.
- **Space**: O(n).

### Verdict
Clear and correct, passes within constraints (n ≤ 10^4), but the greedy is strictly better and just as short.

---

## Approach 2 — Greedy BFS-by-levels (optimal) ⭐

### Intuition
Sweep left to right. Maintain `curEnd` = the last index reachable with the jumps we've already "spent," and `farthest` = the farthest index reachable by extending one more jump from anywhere in the current level. When the scan pointer reaches `curEnd`, we've exhausted the current level — we **must** take one more jump, so increment `jumps` and move the boundary out to `farthest`.

We loop only to `n-2`: if we ever step onto the last index we're done, and we should never "spend" a jump from the last index itself.

**Why it's correct (stay-ahead)**: after `k` jumps the greedy can reach index `curEnd`, which is the maximum index reachable in `k` jumps by *any* strategy. So the first time `curEnd >= n-1`, no faster strategy exists.

### Algorithm
1. `jumps = curEnd = farthest = 0`.
2. For `i` from `0` to `n-2`:
   - `farthest = max(farthest, i + nums[i])`.
   - If `i == curEnd`: `jumps++`, `curEnd = farthest`.
3. Return `jumps`.

### Dry run on `[2,3,1,1,4]`
```
i=0: farthest=max(0,0+2)=2; i==curEnd(0) → jumps=1, curEnd=2
i=1: farthest=max(2,1+3)=4; i(1)!=curEnd(2)
i=2: farthest=max(4,2+1)=4; i==curEnd(2) → jumps=2, curEnd=4
(loop ends at n-2=3) → answer 2
```

### Code
```cpp
int jump(vector<int>& nums) {
    int jumps = 0, curEnd = 0, farthest = 0;
    for (int i = 0; i < (int)nums.size() - 1; i++) {
        farthest = max(farthest, i + nums[i]);
        if (i == curEnd) {
            jumps++;
            curEnd = farthest;
        }
    }
    return jumps;
}
```
```java
public int jump(int[] nums) {
    int jumps = 0, curEnd = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);
        if (i == curEnd) {
            jumps++;
            curEnd = farthest;
        }
    }
    return jumps;
}
```
```python
def jump(nums):
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**Optimal.** The level-boundary insight turns an O(n²) DP into a clean O(n) scan. This is the expected answer.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| DP | O(n²) | O(n) | intuitive, passes |
| Greedy levels | **O(n)** | **O(1)** | optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Single element** (`[1]` or `[0]`) → loop runs `0` times → `0` jumps. Correct.
- **Pitfall — looping to `n-1`**: if you include the last index, the `i == curEnd` check can fire one extra time and over-count. Always iterate `i < n-1`.
- **Pitfall — counting eagerly**: don't add a jump every step; only when you exhaust the current level boundary.
- **Zeros mid-array**: harmless here because the problem guarantees reachability; `farthest` still advances from other indices in the level.

---

## 🔗 Related problems
- **Jump Game** (LC 55) — feasibility only (previous in this set).
- **Jump Game III / IV / V / VI** — graph/DP variants.
- **Minimum Number of Taps to Open to Water a Garden** (LC 1326) — same interval-cover greedy in disguise.
- **Video Stitching** (LC 1024) — identical "extend the farthest reachable end" pattern.

---

**→ Next:** [`04-Gas-Station.md`](./04-Gas-Station.md) | **Prev:** [`02-Jump-Game.md`](./02-Jump-Game.md) | [Problem set index](./00-Index.md)
