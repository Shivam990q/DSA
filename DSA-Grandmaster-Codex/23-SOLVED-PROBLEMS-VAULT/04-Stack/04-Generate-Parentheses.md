# Generate Parentheses

**Platform**: LeetCode 22 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming, Backtracking · **Pattern**: Backtracking with open/close counts

---

## 📜 Problem Statement

Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

### Examples

**Example 1:**
```
Input:  n = 3
Output: ["((()))","(()())","(())()","()(())","()()()"]
```

**Example 2:**
```
Input:  n = 1
Output: ["()"]
```

**Example 3:**
```
Input:  n = 2
Output: ["(())","()()"]
```

### Constraints
```
1 <= n <= 8
```

---

## 🧠 Understanding the problem

We need to generate all **valid** (balanced) strings of length `2n` using `n` opening and `n` closing parentheses. The number of such strings is the n-th **Catalan number**: C(n) = (2n)! / ((n+1)! * n!).

The key constraint for validity: at every prefix, the count of `(` must be ≥ count of `)`. This gives us a clean backtracking rule: we can add `(` if `open < n`, and we can add `)` if `close < open`.

---

## Approach 1 — Brute force (generate all, filter valid)

### Intuition
Generate all 2^(2n) binary strings of `(` and `)`, then filter only the valid ones.

### Algorithm
1. Generate all strings of length `2n` using `(` and `)`.
2. For each string, check if it's valid (using the stack/counter method).
3. Collect valid ones.

### Code
```cpp
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        // Generate all 2^(2n) combinations
        function<void(string&)> generate = [&](string& cur) {
            if (cur.size() == 2 * n) {
                if (isValid(cur)) result.push_back(cur);
                return;
            }
            cur.push_back('(');
            generate(cur);
            cur.pop_back();
            cur.push_back(')');
            generate(cur);
            cur.pop_back();
        };
        string s;
        generate(s);
        return result;
    }
    
    bool isValid(const string& s) {
        int balance = 0;
        for (char c : s) {
            if (c == '(') balance++;
            else balance--;
            if (balance < 0) return false;
        }
        return balance == 0;
    }
};
```
```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        generate(new StringBuilder(), n, result);
        return result;
    }

    private void generate(StringBuilder cur, int n, List<String> result) {
        if (cur.length() == 2 * n) {
            if (isValid(cur.toString())) result.add(cur.toString());
            return;
        }
        cur.append('(');
        generate(cur, n, result);
        cur.deleteCharAt(cur.length() - 1);
        cur.append(')');
        generate(cur, n, result);
        cur.deleteCharAt(cur.length() - 1);
    }

    private boolean isValid(String s) {
        int balance = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') balance++;
            else balance--;
            if (balance < 0) return false;
        }
        return balance == 0;
    }
}
```
```python
class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        result = []
        
        def is_valid(s):
            balance = 0
            for c in s:
                if c == '(': balance += 1
                else: balance -= 1
                if balance < 0: return False
            return balance == 0
        
        def generate(cur):
            if len(cur) == 2 * n:
                if is_valid(cur):
                    result.append(cur)
                return
            generate(cur + '(')
            generate(cur + ')')
        
        generate("")
        return result
```

### Complexity
- **Time**: O(2^(2n) · n) — 2^(2n) strings, each validated in O(n).
- **Space**: O(n) recursion depth + O(result size).

### Verdict
Correct but generates many invalid strings. For n=8, that's 2^16 = 65536 candidates for only 1430 valid ones. Wasteful.

---

## Approach 2 — Backtracking with open/close counts (optimal) ⭐

### Intuition
Instead of generating everything and filtering, we **prune** during generation. At each step:
- We can add `(` only if we haven't used all n openers (`open < n`).
- We can add `)` only if it won't create an imbalance (`close < open`).

This ensures every string we build is valid — no filtering needed.

### Algorithm
1. Start with empty string, `open = 0`, `close = 0`.
2. If `len(current) == 2n` → add to result.
3. If `open < n` → recurse with `(` appended, `open + 1`.
4. If `close < open` → recurse with `)` appended, `close + 1`.

### Dry run for n = 2
```
""
├── "(" (open=1, close=0)
│   ├── "((" (open=2, close=0)
│   │   └── "(()" (open=2, close=1)
│   │       └── "(())" ✓
│   └── "()" (open=1, close=1)
│       └── "()(" (open=2, close=1)
│           └── "()()" ✓
```

### Code
```cpp
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        string current;
        backtrack(result, current, 0, 0, n);
        return result;
    }
    
    void backtrack(vector<string>& result, string& cur, int open, int close, int n) {
        if (cur.size() == 2 * n) {
            result.push_back(cur);
            return;
        }
        if (open < n) {
            cur.push_back('(');
            backtrack(result, cur, open + 1, close, n);
            cur.pop_back();
        }
        if (close < open) {
            cur.push_back(')');
            backtrack(result, cur, open, close + 1, n);
            cur.pop_back();
        }
    }
};
```
```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> result = new ArrayList<>();
        backtrack(result, new StringBuilder(), 0, 0, n);
        return result;
    }

    private void backtrack(List<String> result, StringBuilder cur, int open, int close, int n) {
        if (cur.length() == 2 * n) {
            result.add(cur.toString());
            return;
        }
        if (open < n) {
            cur.append('(');
            backtrack(result, cur, open + 1, close, n);
            cur.deleteCharAt(cur.length() - 1);
        }
        if (close < open) {
            cur.append(')');
            backtrack(result, cur, open, close + 1, n);
            cur.deleteCharAt(cur.length() - 1);
        }
    }
}
```
```python
class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        result = []
        
        def backtrack(cur: list[str], open: int, close: int):
            if len(cur) == 2 * n:
                result.append("".join(cur))
                return
            if open < n:
                cur.append('(')
                backtrack(cur, open + 1, close)
                cur.pop()
            if close < open:
                cur.append(')')
                backtrack(cur, open, close + 1)
                cur.pop()
        
        backtrack([], 0, 0)
        return result
```

### Complexity
- **Time**: O(4^n / √n) — the n-th Catalan number. We only generate valid strings.
- **Space**: O(n) for recursion depth + O(Catalan(n) · 2n) for storing results.

### Verdict
**The optimal answer.** Clean backtracking with two simple pruning rules. This is the standard interview solution.

---

## Approach 3 — Iterative / DP (build from smaller solutions)

### Intuition
Use the recursive structure of Catalan numbers: a valid string of n pairs can be written as `"(" + (valid string of i pairs) + ")" + (valid string of n-1-i pairs)` for i from 0 to n-1.

### Algorithm
1. `dp[0] = [""]` (empty string for 0 pairs).
2. For `k` from 1 to n:
   - For `i` from 0 to k-1:
     - For each `left` in `dp[i]` and `right` in `dp[k-1-i]`:
       - Add `"(" + left + ")" + right` to `dp[k]`.
3. Return `dp[n]`.

### Code
```cpp
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<vector<string>> dp(n + 1);
        dp[0] = {""};
        for (int k = 1; k <= n; k++) {
            for (int i = 0; i < k; i++) {
                for (const string& left : dp[i]) {
                    for (const string& right : dp[k - 1 - i]) {
                        dp[k].push_back("(" + left + ")" + right);
                    }
                }
            }
        }
        return dp[n];
    }
};
```
```java
class Solution {
    public List<String> generateParenthesis(int n) {
        List<List<String>> dp = new ArrayList<>();
        for (int i = 0; i <= n; i++) dp.add(new ArrayList<>());
        dp.get(0).add("");
        for (int k = 1; k <= n; k++) {
            for (int i = 0; i < k; i++) {
                for (String left : dp.get(i)) {
                    for (String right : dp.get(k - 1 - i)) {
                        dp.get(k).add("(" + left + ")" + right);
                    }
                }
            }
        }
        return dp.get(n);
    }
}
```
```python
class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        dp = [[] for _ in range(n + 1)]
        dp[0] = [""]
        for k in range(1, n + 1):
            for i in range(k):
                for left in dp[i]:
                    for right in dp[k - 1 - i]:
                        dp[k].append(f"({left}){right}")
        return dp[n]
```

### Complexity
- **Time**: O(4^n / √n) — same as backtracking (generates same set).
- **Space**: O(4^n / √n · n) — stores all intermediate results.

### Verdict
Elegant and shows the Catalan structure. Uses more memory than backtracking but avoids recursion.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force + filter | O(2^(2n) · n) | O(n) | Generates invalid strings |
| Backtracking | **O(4^n / √n)** | O(n) | Optimal, prunes early ⭐ |
| DP / iterative | O(4^n / √n) | O(4^n / √n · n) | No recursion, more memory |

---

## 🧪 Edge cases & pitfalls
- **n = 1** → only `["()"]`.
- **n = 0** → edge case not in constraints, but logically `[""]`.
- **Pitfall**: using `close < n` instead of `close < open` — this allows invalid strings like `)(`.
- **Pitfall**: string concatenation in Python (`cur + "("`) creates new strings each time → O(n) per call. Using a list with append/pop is faster.
- **Output order**: the problem doesn't require a specific order, but backtracking naturally produces lexicographic order.

---

## 🔗 Related problems
- **Valid Parentheses** (LC 20) — check if a given string is valid.
- **Longest Valid Parentheses** (LC 32) — find longest valid substring.
- **Letter Combinations of a Phone Number** (LC 17) — similar backtracking pattern.
- **Combination Sum** (LC 39) — backtracking with pruning.
- **Remove Invalid Parentheses** (LC 301) — generate valid by removing minimum brackets.

---

**→ Prev:** [`03-Evaluate-RPN.md`](./03-Evaluate-RPN.md) · **→ Next:** [`05-Daily-Temperatures.md`](./05-Daily-Temperatures.md) | [Problem set index](./00-Index.md)
