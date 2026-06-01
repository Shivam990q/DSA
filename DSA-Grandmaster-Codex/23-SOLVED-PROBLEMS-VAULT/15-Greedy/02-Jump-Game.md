# Jump Game

**Platform**: LeetCode 55 · **Difficulty**: Medium · **Topics**: Array, Dynamic Programming, Greedy · **Pattern**: Farthest-reach scan

---

## 📜 Problem Statement

You are given an integer array `nums`. You are initially positioned at the array's **first index**, and each element in the array represents your **maximum jump length** at that position.

Return `true` if you can reach the **last index**, or `false` otherwise.

### Examples

**Example 1:**
```
Input:  nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
```

**Example 2:**
```
Input:  nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump
length is 0, which makes it impossible to reach the last index.
```

**Example 3:**
```
Input:  nums = [0]
Output: true
Explanation: You are already at the last index.
```

### Constraints
```
1 <= nums.length <= 10^4
0 <= nums[i] <= 10^5
```

---

## 🧠 Understanding the problem

From index `i` you may land on any index in `[i+1, i+nums[i]]`. The question is purely reachability — can index `n-1` be touched at all? We don't need the path or the number of jumps (that's Jump Game II).

The crucial reframing: instead of tracking *which* cells are reachable, track only the **single farthest index reachable so far**. Reachability is "downward closed" — if you can reach index `k`, you can reach every index `≤ k` that lies on the way. So one number, `reach`, fully summarizes the frontier. If at any point your current index `i` is beyond `reach`, there is a gap you can never cross (a zero stalled you), and the answer is `false`.

---

## Approach 1 — Backtracking (brute force)

### Intuition
From position `i`, try every possible jump length and recurse. If any path reaches the end, succeed.

### Algorithm
1. `canReach(i)`: if `i == n-1` return `true`.
2. For each step `s` in `1..nums[i]`, try `canReach(i+s)`; if any succeeds, return `true`.
3. Return `false`.

### Dry run on `[3,2,1,0,4]`
```
From 0 we can reach 1,2,3. From each, the farthest we ever get is index 3
(value 0 → no further jumps). Index 4 is never reachable → false.
(Exponential branching explores the same dead ends repeatedly.)
```

### Code
```cpp
class Solution {
    bool dfs(vector<int>& nums, int i) {
        if (i >= (int)nums.size() - 1) return true;
        int far = min((int)nums.size() - 1, i + nums[i]);
        for (int nxt = i + 1; nxt <= far; nxt++)
            if (dfs(nums, nxt)) return true;
        return false;
    }
public:
    bool canJump(vector<int>& nums) { return dfs(nums, 0); }
};
```
```java
public boolean canJump(int[] nums) {
    return dfs(nums, 0);
}
private boolean dfs(int[] nums, int i) {
    if (i >= nums.length - 1) return true;
    int far = Math.min(nums.length - 1, i + nums[i]);
    for (int nxt = i + 1; nxt <= far; nxt++)
        if (dfs(nums, nxt)) return true;
    return false;
}
```
```python
def canJump(nums):
    n = len(nums)
    def dfs(i):
        if i >= n - 1:
            return True
        far = min(n - 1, i + nums[i])
        for nxt in range(i + 1, far + 1):
            if dfs(nxt):
                return True
        return False
    return dfs(0)
```

### Complexity
- **Time**: O(2^n) worst case — exponential. **TLE.**
- **Space**: O(n) recursion depth.

### Verdict
Correct but explodes. It motivates memoization next.

---

## Approach 2 — Dynamic programming (memoized reachability)

### Intuition
Cache whether each index can reach the end so we never recompute. `dp[i] = true` if some reachable next index has `dp = true`. Iterating right-to-left is cleanest: an index is "good" if it can jump to a known good index.

### Algorithm
1. Mark `dp[n-1] = GOOD`.
2. For `i` from `n-2` down to `0`: scan `j` in `[i+1, min(n-1, i+nums[i])]`; if any `dp[j]` is GOOD, set `dp[i] = GOOD`.
3. Return `dp[0]`.

### Dry run on `[2,3,1,1,4]`
```
dp[4]=GOOD
dp[3]: can reach 4 → GOOD
dp[2]: reaches 3 → GOOD
dp[1]: reaches 2..4 → GOOD
dp[0]: reaches 1..2 → GOOD → true
```

### Code
```cpp
bool canJump(vector<int>& nums) {
    int n = nums.size();
    vector<bool> good(n, false);
    good[n - 1] = true;
    for (int i = n - 2; i >= 0; i--) {
        int far = min(n - 1, i + nums[i]);
        for (int j = i + 1; j <= far; j++)
            if (good[j]) { good[i] = true; break; }
    }
    return good[0];
}
```
```java
public boolean canJump(int[] nums) {
    int n = nums.length;
    boolean[] good = new boolean[n];
    good[n - 1] = true;
    for (int i = n - 2; i >= 0; i--) {
        int far = Math.min(n - 1, i + nums[i]);
        for (int j = i + 1; j <= far; j++)
            if (good[j]) { good[i] = true; break; }
    }
    return good[0];
}
```
```python
def canJump(nums):
    n = len(nums)
    good = [False] * n
    good[n - 1] = True
    for i in range(n - 2, -1, -1):
        far = min(n - 1, i + nums[i])
        for j in range(i + 1, far + 1):
            if good[j]:
                good[i] = True
                break
    return good[0]
```

### Complexity
- **Time**: O(n²) worst case — each index scans its reachable range.
- **Space**: O(n).

### Verdict
Polynomial and passes, but still does redundant scanning. The greedy collapses the inner loop entirely.

---

## Approach 3 — Greedy farthest reach (optimal) ⭐

### Intuition
Walk left to right tracking `reach`, the farthest index reachable using everything seen so far. If the current index `i` ever exceeds `reach`, a zero (or too-small value) created an unbridgeable gap → return `false`. Otherwise update `reach = max(reach, i + nums[i])`. If we finish the loop without falling behind, the end is reachable.

**Why it's correct (stay-ahead)**: `reach` is the union of all positions reachable from any earlier index. Because reachability is contiguous up to `reach`, knowing the single max is enough — there's never a reason to remember individual cells.

### Algorithm
1. `reach = 0`.
2. For `i` from `0` to `n-1`:
   - If `i > reach` → return `false`.
   - `reach = max(reach, i + nums[i])`.
   - (Optional early exit: if `reach >= n-1` return `true`.)
3. Return `true`.

### Dry run on `[3,2,1,0,4]`
```
i=0: reach=max(0,0+3)=3
i=1: 1<=3, reach=max(3,1+2)=3
i=2: 2<=3, reach=max(3,2+1)=3
i=3: 3<=3, reach=max(3,3+0)=3
i=4: 4 > reach(3) → return false  ✓
```

### Code
```cpp
bool canJump(vector<int>& nums) {
    int reach = 0, n = nums.size();
    for (int i = 0; i < n; i++) {
        if (i > reach) return false;
        reach = max(reach, i + nums[i]);
    }
    return true;
}
```
```java
public boolean canJump(int[] nums) {
    int reach = 0, n = nums.length;
    for (int i = 0; i < n; i++) {
        if (i > reach) return false;
        reach = Math.max(reach, i + nums[i]);
    }
    return true;
}
```
```python
def canJump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**Optimal.** One number, one pass. The "track the frontier" idea generalizes to many reachability problems.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Backtracking | O(2^n) | O(n) | baseline; TLE |
| DP reachability | O(n²) | O(n) | passes but quadratic |
| Greedy reach | **O(n)** | **O(1)** | optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Single element** (`[0]`) → already at the last index → `true` (`reach=0`, loop never falls behind).
- **Leading zero with length > 1** (`[0,1]`) → at `i=1`, `1 > reach(0)` → `false`.
- **Large values** → `i+nums[i]` could exceed `n-1`; that's fine, we only compare against `i`.
- **Pitfall**: an alternative greedy walks backward checking a "last good index." It also works but the forward `reach` is simpler — just don't mix the two and confuse yourself.
- **Pitfall**: forgetting the `i > reach` check *before* updating reach; if you update first you can mask the gap.

---

## 🔗 Related problems
- **Jump Game II** (LC 45) — minimum number of jumps (next in this set).
- **Jump Game III** (LC 1306) — jump `±nums[i]`, reach any zero.
- **Jump Game VI** (LC 1696) — max score with a sliding-window-max DP.
- **Gas Station** (LC 134) — another single-pass feasibility scan.

---

**→ Next:** [`03-Jump-Game-II.md`](./03-Jump-Game-II.md) | **Prev:** [`01-Maximum-Subarray.md`](./01-Maximum-Subarray.md) | [Problem set index](./00-Index.md)
