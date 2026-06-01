# Valid Parenthesis String

**Platform**: LeetCode 678 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming, Stack, Greedy · **Pattern**: Open-count range `[lo, hi]`

---

## 📜 Problem Statement

Given a string `s` containing only three types of characters: `'('`, `')'` and `'*'`, return `true` *if* `s` *is **valid***.

The following rules define a **valid** string:

- Any left parenthesis `'('` must have a corresponding right parenthesis `')'`.
- Any right parenthesis `')'` must have a corresponding left parenthesis `'('`.
- Left parenthesis `'('` must go before the corresponding right parenthesis `')'`.
- `'*'` could be treated as a single right parenthesis `')'`, a single left parenthesis `'('`, or an **empty string** `""`.

### Examples

**Example 1:**
```
Input:  s = "()"
Output: true
```

**Example 2:**
```
Input:  s = "(*)"
Output: true
Explanation: The '*' can be treated as empty → "()" which is valid.
```

**Example 3:**
```
Input:  s = "(*))"
Output: true
Explanation: The '*' can be treated as '(' → "(())" valid, or as empty → "())"
which is invalid, so we pick the interpretation that makes it valid.
```

### Constraints
```
1 <= s.length <= 100
s[i] is '(', ')' or '*'.
```

---

## 🧠 Understanding the problem

Without `*`, validity is the classic balance check: scan left to right, keep a counter of unmatched `(`; it must never go negative and must end at 0. The `*` wildcard adds uncertainty — each one could push the counter up (as `(`), down (as `)`), or leave it unchanged (empty).

The elegant trick: instead of branching into three worlds at every `*`, track a **range** `[lo, hi]` of all possible values the open-paren counter could take given the choices so far.

- `(` forces both bounds up: `lo++`, `hi++`.
- `)` forces both bounds down: `lo--`, `hi--`.
- `*` widens the range: it could subtract one (`lo--`) or add one (`hi++`).

Two guard rails: `hi` is the most optimistic open count; if `hi < 0` it means even using **every** `*` as `(` we still have too many `)` → impossible, return `false`. And `lo` (the most pessimistic open count) can never be negative in reality — extra closing potential is just unused, so we **clamp `lo` to 0**. At the end the string is valid iff `lo == 0`, meaning it's possible to have exactly zero unmatched `(`.

---

## Approach 1 — Dynamic programming

### Intuition
`dp[i][open]` = can the suffix starting at `i` be valid given `open` unmatched `(` so far? Branch on each character; for `*` try all three roles.

### Algorithm
1. `dp[i][open]` true if from index `i` with `open` open parens we can finish balanced.
2. Base: at `i == n`, valid iff `open == 0`.
3. Transition: `(` → `dp[i+1][open+1]`; `)` → need `open>0` and `dp[i+1][open-1]`; `*` → any of the three.
4. Answer: `dp[0][0]`.

### Dry run on `s = "(*)"`
```
Try interpretations of '*':
'(' as empty → "()" valid. dp finds this path → true.
```

### Code
```cpp
class Solution {
    int n;
    vector<vector<int>> memo;  // -1 unknown, 0 false, 1 true
    bool dp(const string& s, int i, int open) {
        if (open < 0) return false;
        if (i == n) return open == 0;
        if (memo[i][open] != -1) return memo[i][open];
        bool res;
        if (s[i] == '(')      res = dp(s, i + 1, open + 1);
        else if (s[i] == ')') res = dp(s, i + 1, open - 1);
        else res = dp(s, i + 1, open + 1) || dp(s, i + 1, open - 1) || dp(s, i + 1, open);
        return memo[i][open] = res;
    }
public:
    bool checkValidString(string s) {
        n = s.size();
        memo.assign(n + 1, vector<int>(n + 1, -1));
        return dp(s, 0, 0);
    }
};
```
```java
class Solution {
    private int n;
    private int[][] memo;  // -1 unknown, 0 false, 1 true
    public boolean checkValidString(String s) {
        n = s.length();
        memo = new int[n + 1][n + 1];
        for (int[] row : memo) Arrays.fill(row, -1);
        return dp(s, 0, 0);
    }
    private boolean dp(String s, int i, int open) {
        if (open < 0) return false;
        if (i == n) return open == 0;
        if (memo[i][open] != -1) return memo[i][open] == 1;
        boolean res;
        char c = s.charAt(i);
        if (c == '(')      res = dp(s, i + 1, open + 1);
        else if (c == ')') res = dp(s, i + 1, open - 1);
        else res = dp(s, i + 1, open + 1) || dp(s, i + 1, open - 1) || dp(s, i + 1, open);
        memo[i][open] = res ? 1 : 0;
        return res;
    }
}
```
```python
from functools import lru_cache
def checkValidString(s):
    n = len(s)
    @lru_cache(maxsize=None)
    def dp(i, open_):
        if open_ < 0:
            return False
        if i == n:
            return open_ == 0
        c = s[i]
        if c == '(':
            return dp(i + 1, open_ + 1)
        if c == ')':
            return dp(i + 1, open_ - 1)
        return dp(i + 1, open_ + 1) or dp(i + 1, open_ - 1) or dp(i + 1, open_)
    return dp(0, 0)
```

### Complexity
- **Time**: O(n²) — `n` positions × up to `n` open-counts.
- **Space**: O(n²) memo.

### Verdict
Clear and correct, fine for `n ≤ 100`. But the range trick does it in O(n) time and O(1) space, so it's the one to know.

---

## Approach 2 — Two-pass counting (forward and backward)

### Intuition
Do a forward pass treating every `*` as `(` and checking we never run out of openers; then a backward pass treating every `*` as `)` and checking we never run out of closers. If both passes survive, a valid assignment exists.

### Algorithm
1. Forward: counter `bal`; `(` and `*` → `bal++`, `)` → `bal--`; if `bal < 0` at any point → `false`.
2. Backward: counter `bal`; `)` and `*` → `bal++`, `(` → `bal--`; if `bal < 0` → `false`.
3. Return `true`.

### Dry run on `s = "(*))"`
```
forward (* as '('): +1 +1 -1 -1 = ends 0, never negative ✓
backward (* as ')'): from right: ')'+1 ')'+1 '*'+1 '('-1 → 1,2,3,2 never negative ✓
both survive → true
```

### Code
```cpp
bool checkValidString(string s) {
    int n = s.size();
    int bal = 0;
    for (int i = 0; i < n; i++) {            // '*' and '(' as openers
        bal += (s[i] == ')') ? -1 : 1;
        if (bal < 0) return false;
    }
    bal = 0;
    for (int i = n - 1; i >= 0; i--) {        // '*' and ')' as closers
        bal += (s[i] == '(') ? -1 : 1;
        if (bal < 0) return false;
    }
    return true;
}
```
```java
public boolean checkValidString(String s) {
    int n = s.length(), bal = 0;
    for (int i = 0; i < n; i++) {
        bal += (s.charAt(i) == ')') ? -1 : 1;
        if (bal < 0) return false;
    }
    bal = 0;
    for (int i = n - 1; i >= 0; i--) {
        bal += (s.charAt(i) == '(') ? -1 : 1;
        if (bal < 0) return false;
    }
    return true;
}
```
```python
def checkValidString(s):
    bal = 0
    for c in s:                # '*' and '(' count as openers
        bal += -1 if c == ')' else 1
        if bal < 0:
            return False
    bal = 0
    for c in reversed(s):      # '*' and ')' count as closers
        bal += -1 if c == '(' else 1
        if bal < 0:
            return False
    return True
```

### Complexity
- **Time**: O(n) — two passes.
- **Space**: O(1).

### Verdict
Slick and O(1) space. It's a valid optimal answer; the range method below is the single-pass form of the same insight.

---

## Approach 3 — Open-count range `[lo, hi]` (optimal, single pass) ⭐

### Intuition
Track the interval of possible unmatched-`(` counts. `(` shifts both ends up, `)` both down, `*` widens by one on each side. Clamp `lo` at 0 (you'd never keep "negative" openers). If `hi` ever drops below 0, even the most generous interpretation fails. Valid iff `0` is in the final range, i.e. `lo == 0`.

### Algorithm
1. `lo = hi = 0`.
2. For each `c`:
   - `(` → `lo++`, `hi++`.
   - `)` → `lo--`, `hi--`.
   - `*` → `lo--`, `hi++`.
   - If `hi < 0` → return `false`.
   - If `lo < 0` → `lo = 0`.
3. Return `lo == 0`.

### Dry run on `s = "(*))"`
```
start lo=0 hi=0
'(' : lo=1 hi=1
'*' : lo=0 hi=2
')' : lo=-1→clamp 0, hi=1
')' : lo=-1→clamp 0, hi=0
end lo==0 → true  ✓
```

### Code
```cpp
bool checkValidString(string s) {
    int lo = 0, hi = 0;
    for (char c : s) {
        if (c == '(')      { lo++; hi++; }
        else if (c == ')') { lo--; hi--; }
        else               { lo--; hi++; }
        if (hi < 0) return false;
        if (lo < 0) lo = 0;
    }
    return lo == 0;
}
```
```java
public boolean checkValidString(String s) {
    int lo = 0, hi = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(')      { lo++; hi++; }
        else if (c == ')') { lo--; hi--; }
        else               { lo--; hi++; }
        if (hi < 0) return false;
        if (lo < 0) lo = 0;
    }
    return lo == 0;
}
```
```python
def checkValidString(s):
    lo = hi = 0
    for c in s:
        if c == '(':
            lo += 1; hi += 1
        elif c == ')':
            lo -= 1; hi -= 1
        else:
            lo -= 1; hi += 1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**The optimal answer.** One pass, two integers, and the range invariant is easy to defend. This is what you present.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| DP (memo) | O(n²) | O(n²) | clearest correctness, heaviest |
| Two-pass | O(n) | O(1) | elegant; forward + backward |
| Range `[lo,hi]` | **O(n)** | **O(1)** | single pass, optimal ⭐ |

A stack-of-stars approach (push indices of `(` and `*`, match `)` against `(` first then `*`, then reconcile leftovers) also works in O(n) time / O(n) space — good to mention as a fourth option.

---

## 🧪 Edge cases & pitfalls
- **`hi < 0`** → too many `)` even if all `*` become `(` → fail immediately.
- **Leftover `lo > 0` at the end** → unmatched `(` that no `*` can close → `false`.
- **All stars** (`"***"`) → range stays valid, `lo` clamps to 0 → `true` (treat all as empty).
- **Pitfall**: not clamping `lo` at 0. Without the clamp, a `*` used as `)` early could drive `lo` negative and wrongly invalidate later valid configurations.
- **Pitfall**: checking `lo == 0` but forgetting the `hi < 0` early exit — you need both guards.

---

## 🔗 Related problems
- **Valid Parentheses** (LC 20) — the no-wildcard stack version.
- **Minimum Add to Make Parentheses Valid** (LC 921) — balance counting.
- **Minimum Remove to Make Valid Parentheses** (LC 1249) — stack-based fix-up.
- **Remove Invalid Parentheses** (LC 301) — BFS/DFS over removals.

---

**→ Next:** [`../16-Intervals/00-Index.md`](../16-Intervals/00-Index.md) | **Prev:** [`07-Partition-Labels.md`](./07-Partition-Labels.md) | [Problem set index](./00-Index.md)
