# Decode Ways

**Platform**: LeetCode 91 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming · **Pattern**: Prefix DP with 1-or-2 character lookahead

---

## 📜 Problem Statement

A message containing letters from `A-Z` can be **encoded** into numbers using the mapping:
```
'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
```

To **decode** an encoded message, all the digits must be grouped, then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, `"11106"` can be mapped into:
- `"AAJF"` with the grouping `(1, 1, 10, 6)`
- `"KJF"` with the grouping `(11, 10, 6)`

Note that the grouping `(1, 11, 06)` is **invalid** because `"06"` cannot be mapped into `'F'` since `"6"` is different from `"06"`.

Given a string `s` containing only digits, return the **number of ways** to decode it. The test cases are generated so that the answer fits in a **32-bit** integer.

### Examples

**Example 1:**
```
Input:  s = "12"
Output: 2
Explanation: "12" could be decoded as "AB" (1 2) or "L" (12).
```

**Example 2:**
```
Input:  s = "226"
Output: 3
Explanation: "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
```

**Example 3:**
```
Input:  s = "06"
Output: 0
Explanation: "06" cannot be mapped to "F" because of the leading zero ("6" != "06").
```

### Constraints
```
1 <= s.length <= 100
s contains only digits and may contain leading zero(s).
```

---

## 🧠 Understanding the problem

Read the string left to right. At each position you decide how many digits the *last* letter consumed:
- **One digit** `s[i-1]`: valid only if it's `'1'..'9'` (not `'0'`).
- **Two digits** `s[i-2..i-1]`: valid only if the pair is `"10".."26"`.

The number of ways to decode a prefix is the sum of the ways reachable by those two valid last-moves. This is the Climbing-Stairs recurrence with **validity gates** on each step.

5-step framework:
1. **State**: `dp[i]` = number of ways to decode the first `i` characters.
2. **Transition**: `dp[i] = (s[i-1] != '0' ? dp[i-1] : 0) + (10 <= s[i-2..i-1] <= 26 ? dp[i-2] : 0)`.
3. **Base case**: `dp[0] = 1` (empty string: one way — decode nothing), `dp[1] = (s[0] != '0')`.
4. **Order**: `i` from `2` to `n`.
5. **Answer**: `dp[n]`; needs only the last two → O(1) space.

The `'0'` digit is the whole difficulty: a `'0'` can never stand alone, so it *must* pair with a preceding `'1'` or `'2'`, else the decoding is impossible.

---

## Approach 1 — Top-down memoization

### Intuition
`solve(i)` = ways to decode the suffix starting at index `i`. Try taking one digit (if non-zero), then try taking two digits (if 10..26).

### Algorithm
1. If `i == n`, return 1 (reached the end successfully).
2. If `s[i] == '0'`, return 0 (no letter starts with 0).
3. `ways = solve(i+1)`; if `i+1 < n` and `s[i..i+1]` in 10..26, add `solve(i+2)`.
4. Memoize on `i`.

### Dry run on `s = "226"`
```
solve(0): s[0]='2'
  one digit -> solve(1)
  two "22"<=26 -> solve(2)
solve(1): s[1]='2' -> solve(2) + ("26"<=26) solve(3)
solve(2): s[2]='6' -> solve(3)=1
solve(3)=1
=> solve(2)=1, solve(1)=1+1=2, solve(0)=2+1=3
```

### Code
```cpp
class Solution {
    vector<int> memo;
    string s;
    int solve(int i) {
        int n = s.size();
        if (i == n) return 1;
        if (s[i] == '0') return 0;
        if (memo[i] != -1) return memo[i];
        int ways = solve(i + 1);
        if (i + 1 < n) {
            int two = (s[i] - '0') * 10 + (s[i + 1] - '0');
            if (two <= 26) ways += solve(i + 2);
        }
        return memo[i] = ways;
    }
public:
    int numDecodings(string s) {
        this->s = s;
        memo.assign(s.size(), -1);
        return solve(0);
    }
};
```
```java
class Solution {
    private int[] memo;
    private String s;
    private int solve(int i) {
        int n = s.length();
        if (i == n) return 1;
        if (s.charAt(i) == '0') return 0;
        if (memo[i] != -1) return memo[i];
        int ways = solve(i + 1);
        if (i + 1 < n) {
            int two = (s.charAt(i) - '0') * 10 + (s.charAt(i + 1) - '0');
            if (two <= 26) ways += solve(i + 2);
        }
        return memo[i] = ways;
    }
    public int numDecodings(String s) {
        this.s = s;
        memo = new int[s.length()];
        java.util.Arrays.fill(memo, -1);
        return solve(0);
    }
}
```
```python
class Solution:
    def numDecodings(self, s: str) -> int:
        from functools import lru_cache
        n = len(s)

        @lru_cache(maxsize=None)
        def solve(i: int) -> int:
            if i == n:
                return 1
            if s[i] == '0':
                return 0
            ways = solve(i + 1)
            if i + 1 < n and int(s[i:i + 2]) <= 26:
                ways += solve(i + 2)
            return ways

        return solve(0)
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) memo + stack.

### Verdict
Reads almost exactly like the problem statement. Now go bottom-up.

---

## Approach 2 — Bottom-up tabulation

### Intuition
`dp[i]` = ways to decode the first `i` chars, built from `dp[i-1]` and `dp[i-2]` with the validity gates.

### Algorithm
1. `dp[0] = 1`. `dp[1] = (s[0] != '0') ? 1 : 0`.
2. For `i` from 2 to n:
   - If `s[i-1] != '0'`: `dp[i] += dp[i-1]`.
   - Let `two = s[i-2..i-1]`; if `10 <= two <= 26`: `dp[i] += dp[i-2]`.
3. Return `dp[n]`.

### Dry run on `s = "12"`
```
dp[0]=1, dp[1]=1 (s[0]='1')
i=2: s[1]='2'!='0' -> dp[2]+=dp[1]=1; two=12 in [10,26] -> dp[2]+=dp[0]=1 => dp[2]=2
answer = 2
```

### Code
```cpp
class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        vector<int> dp(n + 1, 0);
        dp[0] = 1;
        dp[1] = (s[0] != '0') ? 1 : 0;
        for (int i = 2; i <= n; i++) {
            if (s[i - 1] != '0') dp[i] += dp[i - 1];
            int two = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
            if (two >= 10 && two <= 26) dp[i] += dp[i - 2];
        }
        return dp[n];
    }
};
```
```java
class Solution {
    public int numDecodings(String s) {
        int n = s.length();
        int[] dp = new int[n + 1];
        dp[0] = 1;
        dp[1] = (s.charAt(0) != '0') ? 1 : 0;
        for (int i = 2; i <= n; i++) {
            if (s.charAt(i - 1) != '0') dp[i] += dp[i - 1];
            int two = (s.charAt(i - 2) - '0') * 10 + (s.charAt(i - 1) - '0');
            if (two >= 10 && two <= 26) dp[i] += dp[i - 2];
        }
        return dp[n];
    }
}
```
```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1 if s[0] != '0' else 0
        for i in range(2, n + 1):
            if s[i - 1] != '0':
                dp[i] += dp[i - 1]
            two = int(s[i - 2:i])
            if 10 <= two <= 26:
                dp[i] += dp[i - 2]
        return dp[n]
```

### Complexity
- **Time**: O(n).
- **Space**: O(n).

### Verdict
Clean bottom-up. Note `dp` only ever reaches back two entries.

---

## Approach 3 — Space-optimized rolling variables (optimal) ⭐

### Intuition
Keep `prev2 = dp[i-2]` and `prev1 = dp[i-1]`; roll forward.

### Algorithm
1. If `s[0] == '0'`, return 0. Set `prev2 = 1`, `prev1 = 1`.
2. For `i` from 2 to n: compute `cur` with the same two gates; shift `prev2 = prev1`, `prev1 = cur`.
3. Return `prev1`.

### Dry run on `s = "226"`
```
prev2=1, prev1=1
i=2: s[1]='2' -> cur=prev1=1; two=22 -> cur+=prev2=1 => cur=2; shift prev2=1,prev1=2
i=3: s[2]='6' -> cur=prev1=2; two=26 -> cur+=prev2=1 => cur=3; prev1=3
return 3
```

### Code
```cpp
class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        if (s[0] == '0') return 0;
        int prev2 = 1, prev1 = 1;     // dp[0], dp[1]
        for (int i = 2; i <= n; i++) {
            int cur = 0;
            if (s[i - 1] != '0') cur += prev1;
            int two = (s[i - 2] - '0') * 10 + (s[i - 1] - '0');
            if (two >= 10 && two <= 26) cur += prev2;
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
};
```
```java
class Solution {
    public int numDecodings(String s) {
        int n = s.length();
        if (s.charAt(0) == '0') return 0;
        int prev2 = 1, prev1 = 1;     // dp[0], dp[1]
        for (int i = 2; i <= n; i++) {
            int cur = 0;
            if (s.charAt(i - 1) != '0') cur += prev1;
            int two = (s.charAt(i - 2) - '0') * 10 + (s.charAt(i - 1) - '0');
            if (two >= 10 && two <= 26) cur += prev2;
            prev2 = prev1;
            prev1 = cur;
        }
        return prev1;
    }
}
```
```python
class Solution:
    def numDecodings(self, s: str) -> int:
        if s[0] == '0':
            return 0
        prev2, prev1 = 1, 1           # dp[0], dp[1]
        for i in range(2, len(s) + 1):
            cur = 0
            if s[i - 1] != '0':
                cur += prev1
            two = int(s[i - 2:i])
            if 10 <= two <= 26:
                cur += prev2
            prev2, prev1 = prev1, cur
        return prev1
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
**The optimal answer.** Linear time, constant space.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(n) | O(n) | mirrors the statement |
| Tabulation | O(n) | O(n) | bottom-up array |
| Rolling variables | **O(n)** | **O(1)** | the answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Leading zero** (`"0"`, `"06"`) → 0. A `'0'` can never start a letter and can only attach as the second digit of `"10"`/`"20"`.
- **Standalone middle zero** (`"100"`) → 0: the second `0` cannot pair (`"00"` invalid) nor stand alone.
- **`"10"`, `"20"`** → 1 (the only valid grouping is the two-digit one).
- **`"27"`, `"30"`** → for `"27"`: `2` then `7` = 1 way (27 > 26). For `"30"`: 0 (`0` can't stand alone, `30 > 26`).
- **Pitfall — using `dp[i-2]` for a zero second digit**: the one-digit branch is gated by `s[i-1] != '0'`, and the two-digit branch by `10 <= two <= 26`. A pair like `"30"` passes neither, correctly yielding 0.
- **Pitfall — `dp[0] = 1`**: the empty prefix has exactly one decoding (the empty message). This seed is what makes a valid two-digit first letter (`"12"`) count correctly.

---

## 🔗 Related problems
- **Climbing Stairs** (LC 70) — same `dp[i-1] + dp[i-2]` skeleton without the validity gates.
- **Decode Ways II** (LC 639) — adds the `'*'` wildcard; same DP with many more cases.
- **Number of Ways to ... (combinatorial counting DPs)** — the "sum over valid last moves" template recurs widely.

---

**→ Next:** [`08-Coin-Change.md`](./08-Coin-Change.md) | **→ Prev:** [`06-Palindromic-Substrings.md`](./06-Palindromic-Substrings.md) | Back to [`00-Index.md`](./00-Index.md)
