# Letter Combinations of a Phone Number

**Platform**: LeetCode 17 · **Difficulty**: Medium · **Topics**: Hash Table, String, Backtracking · **Pattern**: Positional DFS (Cartesian product)

---

## 📜 Problem Statement

Given a string containing digits from `2-9` inclusive, return *all possible letter combinations that the number could represent*. Return the answer in **any order**.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that `1` does **not** map to any letters.

```
2 → "abc"    3 → "def"    4 → "ghi"
5 → "jkl"    6 → "mno"    7 → "pqrs"
8 → "tuv"    9 → "wxyz"
```

### Examples

**Example 1:**
```
Input:  digits = "23"
Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
Explanation: 2→"abc", 3→"def"; every letter of 2 paired with every letter of 3.
```

**Example 2:**
```
Input:  digits = ""
Output: []
Explanation: No digits → no combinations (NOT [""]).
```

**Example 3:**
```
Input:  digits = "2"
Output: ["a","b","c"]
```

### Constraints
```
0 <= digits.length <= 4
digits[i] is a digit in the range ['2', '9'].
```

---

## 🧠 Understanding the problem

Each digit independently contributes one letter to a combination, and the letter is chosen from that digit's set (3 or 4 options). So the full answer is the **Cartesian product** of the per-digit letter sets — pick one letter from digit 0's set, one from digit 1's set, and so on. If the digits have set sizes `k0, k1, ...`, the number of combinations is `k0 · k1 · ...` (between `3^n` and `4^n`).

This is positional enumeration much like [Permutations](./04-Permutations.md), except the "alphabet" at each position is fixed by the digit rather than drawn from a shared pool — so there's no `used[]` bookkeeping. We branch over a digit's letters, descend to the next digit, and record a combination once we've placed a letter for every digit.

The only real edge case is the **empty input**: it must return `[]`, not `[""]`.

---

## Approach 1 — Backtracking over digit positions ⭐

### Intuition
Process digits left to right. At digit index `i`, branch over each letter the digit maps to: append the letter, recurse to digit `i + 1`, then pop. When `i` equals the number of digits, the current string is a complete combination — record it. Guard the empty input up front.

### Algorithm
1. If `digits` is empty → return `[]`.
2. Build the digit→letters map.
3. `backtrack(i, cur)`:
   - If `i == digits.length`: record `cur`; return.
   - For each letter `ch` in `map[digits[i]]`:
     - **choose** `ch`, **explore** `backtrack(i + 1, cur + ch)`, **un-choose**.

### Dry run on `digits = "23"`
```
bt(0,"")
 ch='a' → bt(1,"a")
   'd'→bt(2,"ad") RECORD ; 'e'→"ae" ; 'f'→"af"
 ch='b' → bt(1,"b") → "bd","be","bf"
 ch='c' → bt(1,"c") → "cd","ce","cf"
Result: ad ae af bd be bf cd ce cf  (3×3 = 9)
```

### Code
```cpp
class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        vector<string> mp = {"", "", "abc", "def", "ghi",
                             "jkl", "mno", "pqrs", "tuv", "wxyz"};
        vector<string> res;
        string cur;
        function<void(int)> bt = [&](int i) {
            if (i == (int)digits.size()) { res.push_back(cur); return; }
            for (char ch : mp[digits[i] - '0']) {
                cur.push_back(ch);          // choose
                bt(i + 1);                  // explore
                cur.pop_back();             // un-choose
            }
        };
        bt(0);
        return res;
    }
};
```
```java
class Solution {
    private static final String[] MP = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    public List<String> letterCombinations(String digits) {
        List<String> res = new ArrayList<>();
        if (digits == null || digits.isEmpty()) return res;
        backtrack(digits, 0, new StringBuilder(), res);
        return res;
    }
    private void backtrack(String digits, int i, StringBuilder cur,
                           List<String> res) {
        if (i == digits.length()) { res.add(cur.toString()); return; }
        String letters = MP[digits.charAt(i) - '0'];
        for (int k = 0; k < letters.length(); k++) {
            cur.append(letters.charAt(k));            // choose
            backtrack(digits, i + 1, cur, res);       // explore
            cur.deleteCharAt(cur.length() - 1);       // un-choose
        }
    }
}
```
```python
class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        mp = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
              '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
        res = []
        def backtrack(i, cur):
            if i == len(digits):
                res.append(cur); return
            for ch in mp[digits[i]]:
                backtrack(i + 1, cur + ch)            # choose + explore (+ implicit un-choose)
        backtrack(0, "")
        return res
```

### Complexity
- **Time**: O(n · 4^n) — up to `4^n` combinations, each of length `n` to build/copy.
- **Space**: O(n) recursion depth + the current string (output not counted).

---

## Approach 2 — Iterative Cartesian product (BFS-style)

### Intuition
Maintain a running list of partial combinations. For each new digit, replace the list with every existing partial extended by each of the digit's letters. This builds the product layer by layer without recursion.

### Algorithm
1. If `digits` empty → return `[]`.
2. Start `res = [""]`.
3. For each digit, set `res = { prefix + letter : prefix in res, letter in map[digit] }`.

### Dry run on `digits = "23"`
```
res = [""]
digit 2 → ["a","b","c"]
digit 3 → ["ad","ae","af","bd","be","bf","cd","ce","cf"]
```

### Code
```cpp
class Solution {
public:
    vector<string> letterCombinations(string digits) {
        if (digits.empty()) return {};
        vector<string> mp = {"", "", "abc", "def", "ghi",
                             "jkl", "mno", "pqrs", "tuv", "wxyz"};
        vector<string> res = {""};
        for (char d : digits) {
            vector<string> next;
            for (const string& prefix : res)
                for (char ch : mp[d - '0'])
                    next.push_back(prefix + ch);
            res = move(next);
        }
        return res;
    }
};
```
```java
class Solution {
    private static final String[] MP = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };
    public List<String> letterCombinations(String digits) {
        List<String> res = new ArrayList<>();
        if (digits == null || digits.isEmpty()) return res;
        res.add("");
        for (int i = 0; i < digits.length(); i++) {
            String letters = MP[digits.charAt(i) - '0'];
            List<String> next = new ArrayList<>();
            for (String prefix : res)
                for (int k = 0; k < letters.length(); k++)
                    next.add(prefix + letters.charAt(k));
            res = next;
        }
        return res;
    }
}
```
```python
class Solution:
    def letterCombinations(self, digits):
        if not digits:
            return []
        mp = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
              '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
        res = [""]
        for d in digits:
            res = [prefix + ch for prefix in res for ch in mp[d]]
        return res
```

### Complexity
- **Time**: O(n · 4^n) — same total product size.
- **Space**: O(1) auxiliary beyond the output (no recursion stack).

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| Backtracking (DFS) | O(n·4^n) | O(n) | the canonical answer; mirrors the topic template ⭐ |
| Iterative product (BFS) | O(n·4^n) | O(1) extra | no recursion; clean for explaining "it's a Cartesian product" |

Both are optimal (output size is the lower bound). Pick whichever the interviewer's framing invites — DFS to show the backtracking template, iterative to emphasize the product structure.

---

## 🧪 Edge cases & pitfalls
- **Empty input** `""` → `[]`. Must short-circuit *before* seeding the result; otherwise the loop body never runs and you'd return `[""]` (wrong) from the iterative version, or `[""]` from the DFS if you start with `[""]` and never guard.
- **Single digit** `"2"` → `["a","b","c"]`.
- **Digit 7 / 9 have 4 letters** → the only sources of the `4` in `4^n`; don't hardcode 3 letters per digit.
- **Pitfall — including `1` or `0`**: constraints exclude them, but if extending, remember `0` and `1` map to nothing.
- **Pitfall — building the map wrong**: index `mp` by `digit - '0'`; the two leading empty strings for indices `0` and `1` keep the offset correct.
- **Pitfall — mutating a shared buffer without undo**: in the DFS, either pass `cur + ch` by value (Python) or append/pop a `StringBuilder` (Java) / string (C++) consistently.

---

## 🔗 Related problems
- **Permutations** (LC 46) — positional enumeration from a shared pool (needs `used[]`). → [04-Permutations.md](./04-Permutations.md)
- **Subsets** (LC 78) — include/exclude branching. → [01-Subsets.md](./01-Subsets.md)
- **Generate Parentheses** (LC 22) — positional DFS with validity constraints.
- **Combinations** (LC 77) — choose `k` of `n` (forward `start` index).

---

**→ Next:** [`09-N-Queens.md`](./09-N-Queens.md) | [Problem set index](./00-Index.md) | **← Prev:** [`07-Palindrome-Partitioning.md`](./07-Palindrome-Partitioning.md)
