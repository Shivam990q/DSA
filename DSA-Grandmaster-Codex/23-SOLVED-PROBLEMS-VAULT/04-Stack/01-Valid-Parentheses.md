# Valid Parentheses

**Platform**: LeetCode 20 · **Difficulty**: Easy · **Topics**: String, Stack · **Pattern**: Stack matching / nesting

---

## 📜 Problem Statement

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

### Examples

**Example 1:**
```
Input:  s = "()"
Output: true
```

**Example 2:**
```
Input:  s = "()[]{}"
Output: true
```

**Example 3:**
```
Input:  s = "(]"
Output: false
```

### Constraints
```
1 <= s.length <= 10^4
s consists of parentheses only '()[]{}' .
```

---

## 🧠 Understanding the problem

We need to verify **proper nesting**. The key insight: the most recently opened bracket must be the first one closed. That's exactly LIFO — a stack.

A string like `"([{}])"` is valid because every closer matches the most recent unmatched opener. A string like `"([)]"` is invalid because `]` tries to close `[` but the most recent opener is `(`.

---

## Approach 1 — Brute force (repeated removal)

### Intuition
If we repeatedly remove adjacent valid pairs `()`, `[]`, `{}`, a valid string will eventually become empty. An invalid one won't.

### Algorithm
1. While the string contains `"()"`, `"[]"`, or `"{}"`:
   - Replace each occurrence with `""`.
2. If the string is empty → `true`, else → `false`.

### Code
```cpp
class Solution {
public:
    bool isValid(string s) {
        string prev;
        while (s != prev) {
            prev = s;
            // erase all adjacent pairs
            size_t pos;
            while ((pos = s.find("()")) != string::npos) s.erase(pos, 2);
            while ((pos = s.find("[]")) != string::npos) s.erase(pos, 2);
            while ((pos = s.find("{}")) != string::npos) s.erase(pos, 2);
        }
        return s.empty();
    }
};
```
```java
class Solution {
    public boolean isValid(String s) {
        String prev = null;
        while (!s.equals(prev)) {
            prev = s;
            // erase all adjacent pairs
            s = s.replace("()", "");
            s = s.replace("[]", "");
            s = s.replace("{}", "");
        }
        return s.isEmpty();
    }
}
```
```python
class Solution:
    def isValid(self, s: str) -> bool:
        while "()" in s or "[]" in s or "{}" in s:
            s = s.replace("()", "")
            s = s.replace("[]", "")
            s = s.replace("{}", "")
        return s == ""
```

### Complexity
- **Time**: O(n²) — each pass removes at least one pair, but `replace` scans the whole string each time.
- **Space**: O(n) for string copies.

### Verdict
Correct but slow. Good for understanding the problem; not the interview answer.

---

## Approach 2 — Stack (optimal) ⭐

### Intuition
Push every opener onto a stack. When we see a closer, the top of the stack must be its matching opener — if not, invalid. At the end, the stack must be empty (no unmatched openers).

### Algorithm
1. Create an empty stack and a map: `)` → `(`, `]` → `[`, `}` → `{`.
2. For each character `c` in `s`:
   - If `c` is an opener → push onto stack.
   - Else (closer):
     - If stack is empty → return `false` (nothing to match).
     - Pop the top; if it doesn't match `c` → return `false`.
3. Return `stack.empty()`.

### Dry run on `"([{}])"`
```
c='(' → push → stack: ['(']
c='[' → push → stack: ['(', '[']
c='{' → push → stack: ['(', '[', '{']
c='}' → pop '{' matches → stack: ['(', '[']
c=']' → pop '[' matches → stack: ['(']
c=')' → pop '(' matches → stack: []
End: stack empty → true
```

### Code
```cpp
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty()) return false;
                char top = st.top(); st.pop();
                if (c == ')' && top != '(') return false;
                if (c == ']' && top != '[') return false;
                if (c == '}' && top != '{') return false;
            }
        }
        return st.empty();
    }
};
```
```java
class Solution {
    public boolean isValid(String s) {
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.isEmpty()) return false;
                char top = st.pop();
                if (c == ')' && top != '(') return false;
                if (c == ']' && top != '[') return false;
                if (c == '}' && top != '{') return false;
            }
        }
        return st.isEmpty();
    }
}
```
```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        match = {')': '(', ']': '[', '}': '{'}
        for c in s:
            if c in match:  # closer
                if not stack or stack[-1] != match[c]:
                    return False
                stack.pop()
            else:  # opener
                stack.append(c)
        return len(stack) == 0
```

### Complexity
- **Time**: O(n) — single pass, each character pushed/popped at most once.
- **Space**: O(n) — worst case all openers (e.g., `"(((("` fills the stack).

### Verdict
**The optimal answer.** Clean, O(n), and directly demonstrates stack mastery.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Repeated removal | O(n²) | O(n) | Simple but slow |
| Stack matching | **O(n)** | O(n) | Optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Single character** (`"("` or `")"`) → odd length always invalid. Quick early return: `if (s.size() % 2 != 0) return false;`
- **Only openers** (`"((("`) → stack non-empty at end → `false`.
- **Only closers** (`")))"`) → stack empty when we try to pop → `false`.
- **Interleaved wrong** (`"([)]"`) → `]` doesn't match top `(` → `false`.
- **Empty string** → constraints say `length >= 1`, but if allowed, empty is valid.
- **Pitfall**: forgetting to check `stack.empty()` at the end — `"(("` would incorrectly return `true`.

---

## 🔗 Related problems
- **Minimum Add to Make Parentheses Valid** (LC 921) — count unmatched.
- **Longest Valid Parentheses** (LC 32) — DP or stack with indices.
- **Remove Invalid Parentheses** (LC 301) — BFS/backtracking.
- **Valid Parenthesis String** (LC 678) — `*` can be `(`, `)`, or empty.

---

**→ Next:** [`02-Min-Stack.md`](./02-Min-Stack.md) | [Problem set index](./00-Index.md)
