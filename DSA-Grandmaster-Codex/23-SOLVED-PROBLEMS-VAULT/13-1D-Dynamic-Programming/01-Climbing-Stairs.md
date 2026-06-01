# Climbing Stairs

**Platform**: LeetCode 70 · **Difficulty**: Easy · **Topics**: Math, Dynamic Programming, Memoization · **Pattern**: Linear recurrence (Fibonacci)

---

## 📜 Problem Statement

You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb **1** or **2** steps. In how many **distinct ways** can you climb to the top?

### Examples

**Example 1:**
```
Input:  n = 2
Output: 2
Explanation: There are two ways to climb to the top.
1. 1 step + 1 step
2. 2 steps
```

**Example 2:**
```
Input:  n = 3
Output: 3
Explanation: There are three ways to climb to the top.
1. 1 + 1 + 1
2. 1 + 2
3. 2 + 1
```

**Example 3:**
```
Input:  n = 4
Output: 5
Explanation: 1+1+1+1, 1+1+2, 1+2+1, 2+1+1, 2+2
```

### Constraints
```
1 <= n <= 45
```

---

## 🧠 Understanding the problem

We want to *count* paths, not enumerate them. The key realization: the **last** move to reach step `n` was either a single step (from step `n-1`) or a double step (from step `n-2`). Those two groups of paths are disjoint and together cover every possibility.

So `ways(n) = ways(n-1) + ways(n-2)`. That is exactly the **Fibonacci recurrence**. The whole problem is recognizing this structure and then choosing how efficiently to evaluate it.

Following the 5-step framework:
1. **State**: `dp[i]` = number of distinct ways to reach step `i`.
2. **Transition**: `dp[i] = dp[i-1] + dp[i-2]`.
3. **Base case**: `dp[0] = 1` (one way to "be" at the ground — do nothing), `dp[1] = 1`.
4. **Order**: compute `i` from `2` up to `n`.
5. **Answer**: `dp[n]`; each entry needs only the previous two → O(1) space.

---

## Approach 1 — Plain recursion (exponential)

### Intuition
Translate the recurrence directly into a function. To reach step `n`, recurse into `n-1` and `n-2` and add.

### Algorithm
1. If `n <= 2`, return `n` (1 way for n=1, 2 ways for n=2).
2. Otherwise return `climb(n-1) + climb(n-2)`.

### Dry run on `n = 4`
```
climb(4) = climb(3) + climb(2)
climb(3) = climb(2) + climb(1) = 2 + 1 = 3
climb(2) = 2
=> climb(4) = 3 + 2 = 5
```
Notice `climb(2)` is recomputed multiple times — that's the wasted work.

### Code
```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) return n;
        return climbStairs(n - 1) + climbStairs(n - 2);
    }
};
```
```java
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        return climbStairs(n - 1) + climbStairs(n - 2);
    }
}
```
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        return self.climbStairs(n - 1) + self.climbStairs(n - 2)
```

### Complexity
- **Time**: O(2ⁿ) — the recursion tree branches twice at almost every node.
- **Space**: O(n) recursion stack depth.

### Verdict
Correct but exponential. It demonstrates the recurrence but recomputes the same subproblems exponentially often. Every following approach exists to kill that repetition.

---

## Approach 2 — Top-down memoization

### Intuition
The recursion repeats subproblems. **Cache** each `climb(i)` the first time it's computed; reuse it afterward. Now each state is solved once.

### Algorithm
1. Keep a `memo` array (size `n+1`), initialized to a sentinel (0 / -1).
2. In the recursive function, if `memo[n]` is set, return it.
3. Compute `climb(n-1) + climb(n-2)`, store in `memo[n]`, return.

### Dry run on `n = 4`
```
climb(4) -> needs climb(3), climb(2)
climb(3) -> needs climb(2)[computed=2 stored], climb(1) -> 3 stored
climb(2) reused from memo (no recomputation)
answer = 5
```

### Code
```cpp
class Solution {
    vector<int> memo;
    int climb(int n) {
        if (n <= 2) return n;
        if (memo[n]) return memo[n];
        return memo[n] = climb(n - 1) + climb(n - 2);
    }
public:
    int climbStairs(int n) {
        memo.assign(n + 1, 0);
        return climb(n);
    }
};
```
```java
class Solution {
    private int[] memo;
    private int climb(int n) {
        if (n <= 2) return n;
        if (memo[n] != 0) return memo[n];
        return memo[n] = climb(n - 1) + climb(n - 2);
    }
    public int climbStairs(int n) {
        memo = new int[n + 1];
        return climb(n);
    }
}
```
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def climb(k: int) -> int:
            if k <= 2:
                return k
            return climb(k - 1) + climb(k - 2)

        return climb(n)
```

### Complexity
- **Time**: O(n) — each state computed once.
- **Space**: O(n) for the memo + recursion stack.

### Verdict
Exponential → linear with one cache. This is the natural "I see the repetition" fix.

---

## Approach 3 — Bottom-up tabulation

### Intuition
Instead of recursing down and caching, fill the table **upward** from the base cases. No recursion stack, same O(n).

### Algorithm
1. `dp[1] = 1`, `dp[2] = 2`.
2. For `i` from `3` to `n`: `dp[i] = dp[i-1] + dp[i-2]`.
3. Return `dp[n]`.

### Dry run on `n = 4`
```
dp[1]=1, dp[2]=2
dp[3]=dp[2]+dp[1]=3
dp[4]=dp[3]+dp[2]=5
```

### Code
```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n <= 2) return n;
        vector<int> dp(n + 1);
        dp[1] = 1; dp[2] = 2;
        for (int i = 3; i <= n; i++)
            dp[i] = dp[i - 1] + dp[i - 2];
        return dp[n];
    }
};
```
```java
class Solution {
    public int climbStairs(int n) {
        if (n <= 2) return n;
        int[] dp = new int[n + 1];
        dp[1] = 1; dp[2] = 2;
        for (int i = 3; i <= n; i++)
            dp[i] = dp[i - 1] + dp[i - 2];
        return dp[n];
    }
}
```
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        dp = [0] * (n + 1)
        dp[1], dp[2] = 1, 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) for the table.

### Verdict
Clean and stack-free. But we still keep the whole array even though we only ever look back two steps.

---

## Approach 4 — Space-optimized rolling variables (optimal) ⭐

### Intuition
`dp[i]` depends only on `dp[i-1]` and `dp[i-2]`. Keep just those two scalars and roll them forward.

### Algorithm
1. `a = 1` (ways to reach step 0), `b = 1` (ways to reach step 1).
2. For `i` from `2` to `n`: `c = a + b`; shift `a = b`, `b = c`.
3. Return `b`.

### Dry run on `n = 4`
```
a=1, b=1
i=2: c=2 -> a=1, b=2
i=3: c=3 -> a=2, b=3
i=4: c=5 -> a=3, b=5
return 5
```

### Code
```cpp
class Solution {
public:
    int climbStairs(int n) {
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
};
```
```java
class Solution {
    public int climbStairs(int n) {
        int a = 1, b = 1;
        for (int i = 2; i <= n; i++) {
            int c = a + b;
            a = b;
            b = c;
        }
        return b;
    }
}
```
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        a = b = 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
**The optimal answer.** Linear time, constant space, no recursion. This is what you present.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Plain recursion | O(2ⁿ) | O(n) | baseline; shows the recurrence, TLEs conceptually |
| Memoization | O(n) | O(n) | top-down cache |
| Tabulation | O(n) | O(n) | bottom-up, no stack |
| Rolling variables | **O(n)** | **O(1)** | the answer ⭐ |

The progression here is the canonical DP story: exponential recursion → cache it → flip to bottom-up → shrink the table to a window. Internalize this ladder; nearly every 1D DP follows it.

---

## 🧪 Edge cases & pitfalls
- **`n = 1`** → 1 way. Handled directly by the `n <= 2` guard or by the rolling loop simply not running.
- **`n = 2`** → 2 ways.
- **Pitfall — base case off-by-one**: `dp[0]` is naturally 1 (the empty climb). Setting `dp[1]=1, dp[2]=2` directly avoids confusion. In the rolling version both seeds are `1` because `a` represents step 0 and `b` represents step 1.
- **Overflow**: with `n <= 45`, the answer fits comfortably in a 32-bit int (it's the 46th Fibonacci number, ~1.8×10⁹, still under 2³¹−1). Larger `n` would need 64-bit.

---

## 🔗 Related problems
- **Fibonacci Number** (LC 509) — the same recurrence, literally.
- **Min Cost Climbing Stairs** (LC 746) — add a cost per step and minimize.
- **Decode Ways** (LC 91) — count paths with a 1-or-2 character lookahead.
- **House Robber** (LC 198) — same `dp[i-1]` vs `dp[i-2]` shape, but maximizing.
- **N-th Tribonacci Number** (LC 1137) — depends on the previous three.

---

**→ Next:** [`02-Min-Cost-Climbing-Stairs.md`](./02-Min-Cost-Climbing-Stairs.md) | Back to [`00-Index.md`](./00-Index.md)
