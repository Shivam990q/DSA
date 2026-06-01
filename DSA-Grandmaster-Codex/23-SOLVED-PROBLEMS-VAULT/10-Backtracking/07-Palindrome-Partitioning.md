# Palindrome Partitioning

**Platform**: LeetCode 131 · **Difficulty**: Medium · **Topics**: String, Dynamic Programming, Backtracking · **Pattern**: Prefix-cut DFS

---

## 📜 Problem Statement

Given a string `s`, partition `s` such that every substring of the partition is a **palindrome**. Return *all possible palindrome partitionings of `s`*.

### Examples

**Example 1:**
```
Input:  s = "aab"
Output: [["a","a","b"], ["aa","b"]]
Explanation:
  "a"|"a"|"b"  — three single-char palindromes.
  "aa"|"b"     — "aa" is a palindrome, "b" is a palindrome.
```

**Example 2:**
```
Input:  s = "a"
Output: [["a"]]
```

**Example 3:**
```
Input:  s = "aba"
Output: [["a","b","a"], ["aba"]]
```

### Constraints
```
1 <= s.length <= 16
s contains only lowercase English letters.
```

---

## 🧠 Understanding the problem

We must cut `s` into pieces so that **every** piece is a palindrome, and return **all** such ways to cut. The natural decision at each step is: *where does the first piece end?* Try every possible end position; if the prefix `s[start..end]` is a palindrome, accept it as the next piece and recursively partition the remaining suffix `s[end+1..]`. When `start` reaches the end of the string, the current list of pieces is a complete valid partition.

This is a **combinations-style** backtracking (we move forward through the string with a `start` cursor, never backward). The branching is over "length of the next palindromic piece." The only extra work is the palindrome test on each candidate prefix — which we can do naively in O(length), or precompute with DP so each test is O(1).

With `s.length <= 16`, there are at most `2^(n-1)` cut positions, so the search is small; correctness and clean palindrome-checking are the focus.

---

## Approach 1 — Backtracking with on-the-fly palindrome check ⭐

### Intuition
Walk a `start` cursor across the string. For each `end` from `start` onward, if `s[start..end]` is a palindrome, **choose** it as the next piece, **explore** the rest from `end + 1`, then **un-choose** (pop the piece). Record the partition when `start == n`.

### Algorithm
1. `backtrack(start)`:
   - If `start == n`: record a copy of `cur`; return.
   - For `end` from `start` to `n-1`:
     - If `s[start..end]` is a palindrome:
       - **choose**: push `s.substr(start, end-start+1)`.
       - **explore**: `backtrack(end + 1)`.
       - **un-choose**: pop.
2. `isPalindrome(l, r)`: two-pointer check.

### Dry run on `s = "aab"`
```
bt(0)
 end=0 "a" pal → push "a" → bt(1)
   end=1 "a" pal → push "a" → bt(2)
     end=2 "b" pal → push "b" → bt(3) RECORD ["a","a","b"]
   end=2 "ab" not pal
 end=1 "aa" pal → push "aa" → bt(2)
   end=2 "b" pal → push "b" → bt(3) RECORD ["aa","b"]
 end=2 "aab" not pal
Result: [["a","a","b"], ["aa","b"]]
```

### Code
```cpp
class Solution {
public:
    bool isPal(const string& s, int l, int r) {
        while (l < r) if (s[l++] != s[r--]) return false;
        return true;
    }
    void backtrack(int start, const string& s,
                   vector<string>& cur, vector<vector<string>>& res) {
        if (start == (int)s.size()) { res.push_back(cur); return; }
        for (int end = start; end < (int)s.size(); end++) {
            if (isPal(s, start, end)) {
                cur.push_back(s.substr(start, end - start + 1));  // choose
                backtrack(end + 1, s, cur, res);                  // explore
                cur.pop_back();                                   // un-choose
            }
        }
    }
    vector<vector<string>> partition(string s) {
        vector<vector<string>> res;
        vector<string> cur;
        backtrack(0, s, cur, res);
        return res;
    }
};
```
```java
class Solution {
    public List<List<String>> partition(String s) {
        List<List<String>> res = new ArrayList<>();
        backtrack(0, s, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, String s,
                           List<String> cur, List<List<String>> res) {
        if (start == s.length()) { res.add(new ArrayList<>(cur)); return; }
        for (int end = start; end < s.length(); end++) {
            if (isPal(s, start, end)) {
                cur.add(s.substring(start, end + 1));   // choose
                backtrack(end + 1, s, cur, res);        // explore
                cur.remove(cur.size() - 1);             // un-choose
            }
        }
    }
    private boolean isPal(String s, int l, int r) {
        while (l < r) if (s.charAt(l++) != s.charAt(r--)) return false;
        return true;
    }
}
```
```python
class Solution:
    def partition(self, s):
        res = []
        def is_pal(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1; r -= 1
            return True
        def backtrack(start, cur):
            if start == len(s):
                res.append(cur[:]); return
            for end in range(start, len(s)):
                if is_pal(start, end):
                    cur.append(s[start:end + 1])        # choose
                    backtrack(end + 1, cur)             # explore
                    cur.pop()                           # un-choose
        backtrack(0, [])
        return res
```

### Complexity
- **Time**: O(n · 2^n) — up to `2^(n-1)` partitions, each built/copied in O(n); the palindrome check adds an O(n) factor in the worst case but is dominated by the partition count.
- **Space**: O(n) recursion depth + path (output not counted).

---

## Approach 2 — Precompute palindromes with DP, then backtrack

### Intuition
The repeated `isPalindrome` calls overlap. Precompute a table `pal[i][j]` = "is `s[i..j]` a palindrome?" once in O(n²), then each check inside backtracking is O(1). The recurrence: `s[i..j]` is a palindrome iff `s[i] == s[j]` **and** (`j - i < 2` or `pal[i+1][j-1]`).

### Algorithm
1. Build `pal[i][j]` for all `i <= j` (iterate `i` from `n-1` down, `j` from `i` up).
2. Backtrack as in Approach 1, but replace the live check with `pal[start][end]`.

### Dry run on `s = "aba"` (table highlights)
```
pal["a"]=pal["b"]=pal["a"]=true (length 1)
pal[0..2] "aba": s[0]==s[2]='a' and pal[1][1] → true
bt(0): end=0 "a" → bt(1): end=1 "b" → bt(2): end=2 "a" → RECORD ["a","b","a"]
       end=2 "aba" pal → RECORD ["aba"]
Result: [["a","b","a"], ["aba"]]
```

### Code
```cpp
class Solution {
public:
    vector<vector<string>> partition(string s) {
        int n = s.size();
        vector<vector<bool>> pal(n, vector<bool>(n, false));
        for (int i = n - 1; i >= 0; i--)
            for (int j = i; j < n; j++)
                if (s[i] == s[j] && (j - i < 2 || pal[i+1][j-1]))
                    pal[i][j] = true;
        vector<vector<string>> res;
        vector<string> cur;
        function<void(int)> bt = [&](int start) {
            if (start == n) { res.push_back(cur); return; }
            for (int end = start; end < n; end++) {
                if (pal[start][end]) {
                    cur.push_back(s.substr(start, end - start + 1));
                    bt(end + 1);
                    cur.pop_back();
                }
            }
        };
        bt(0);
        return res;
    }
};
```
```java
class Solution {
    public List<List<String>> partition(String s) {
        int n = s.length();
        boolean[][] pal = new boolean[n][n];
        for (int i = n - 1; i >= 0; i--)
            for (int j = i; j < n; j++)
                if (s.charAt(i) == s.charAt(j) && (j - i < 2 || pal[i+1][j-1]))
                    pal[i][j] = true;
        List<List<String>> res = new ArrayList<>();
        backtrack(0, s, pal, new ArrayList<>(), res);
        return res;
    }
    private void backtrack(int start, String s, boolean[][] pal,
                           List<String> cur, List<List<String>> res) {
        if (start == s.length()) { res.add(new ArrayList<>(cur)); return; }
        for (int end = start; end < s.length(); end++) {
            if (pal[start][end]) {
                cur.add(s.substring(start, end + 1));
                backtrack(end + 1, s, pal, cur, res);
                cur.remove(cur.size() - 1);
            }
        }
    }
}
```
```python
class Solution:
    def partition(self, s):
        n = len(s)
        pal = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                if s[i] == s[j] and (j - i < 2 or pal[i+1][j-1]):
                    pal[i][j] = True
        res = []
        cur = []
        def backtrack(start):
            if start == n:
                res.append(cur[:]); return
            for end in range(start, n):
                if pal[start][end]:
                    cur.append(s[start:end + 1])
                    backtrack(end + 1)
                    cur.pop()
        backtrack(0)
        return res
```

### Complexity
- **Time**: O(n · 2^n) overall — the O(n²) table build is dwarfed by enumerating up to `2^(n-1)` partitions; each palindrome check is now O(1).
- **Space**: O(n²) for the DP table + O(n) recursion.

---

## ⚖️ Approach comparison

| Approach | Time | Space | When to mention |
|----------|------|-------|-----------------|
| Live palindrome check | O(n·2^n) | O(n) | simplest; fine for `n <= 16` ⭐ |
| DP-precomputed `pal[][]` | O(n·2^n) | O(n²) | removes repeated checks; nice optimization to state aloud |

The number of outputs is itself exponential, so neither beats the other asymptotically on this problem — but the DP table is the standard "I'd precompute palindromes" optimization an interviewer wants to hear, and it's essential for the related *Palindrome Partitioning II* (min cuts).

---

## 🧪 Edge cases & pitfalls
- **Single character** `"a"` → `[["a"]]`. Every single char is a palindrome, so there is always at least the all-singletons partition.
- **All same letters** `"aaa"` → all partitions are valid (`[["a","a","a"], ["a","aa"], ["aa","a"], ["aaa"]]`).
- **Pitfall — off-by-one in substring**: the piece is `s[start..end]` inclusive, i.e. length `end - start + 1`; `s.substr(start, end-start+1)` in C++ and `s.substring(start, end+1)` in Java/Python slice `s[start:end+1]`.
- **Pitfall — recursing from `end` instead of `end + 1`**: that re-includes the last char of the current piece into the next, producing overlapping (wrong) partitions.
- **Pitfall — recomputing palindromes redundantly** for large inputs: switch to the DP table.
- **Pitfall — recording by reference** instead of copying `cur` → stored partitions get clobbered by later pops.

---

## 🔗 Related problems
- **Palindrome Partitioning II** (LC 132) — minimum cuts (pure DP, not enumeration).
- **Longest Palindromic Substring** (LC 5) — the palindrome DP/expand-around-center core.
- **Word Break II** (LC 140) — same prefix-cut backtracking, but the validity test is "is the prefix a dictionary word?"
- **Subsets** (LC 78) — the forward `start`-index skeleton underlying this. → [01-Subsets.md](./01-Subsets.md)

---

**→ Next:** [`08-Letter-Combinations-Phone-Number.md`](./08-Letter-Combinations-Phone-Number.md) | [Problem set index](./00-Index.md) | **← Prev:** [`06-Word-Search.md`](./06-Word-Search.md)
