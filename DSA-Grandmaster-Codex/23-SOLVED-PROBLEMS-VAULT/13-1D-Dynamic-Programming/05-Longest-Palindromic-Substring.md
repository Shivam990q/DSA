# Longest Palindromic Substring

**Platform**: LeetCode 5 · **Difficulty**: Medium · **Topics**: Two Pointers, String, Dynamic Programming · **Pattern**: Palindrome DP / expand around center

---

## 📜 Problem Statement

Given a string `s`, return the **longest palindromic substring** in `s`.

A string is a palindrome when it reads the same forward and backward. A **substring** is a contiguous, non-empty sequence of characters.

### Examples

**Example 1:**
```
Input:  s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.
```

**Example 2:**
```
Input:  s = "cbbd"
Output: "bb"
```

**Example 3:**
```
Input:  s = "a"
Output: "a"
```

### Constraints
```
1 <= s.length <= 1000
s consists of only digits and English letters.
```

---

## 🧠 Understanding the problem

We need the longest **contiguous** block that is a palindrome. Two structural facts drive every solution:

1. A palindrome is symmetric about its center. A length-`L` palindrome has a center — a single character (odd length) or the gap between two characters (even length). There are `2n-1` such centers.
2. **Palindromes have optimal substructure**: `s[i..j]` is a palindrome iff `s[i] == s[j]` **and** `s[i+1..j-1]` is a palindrome. That recurrence is the basis of the DP table.

We'll build up from the brute force, to the DP table (which makes the substructure explicit), to expand-around-center (the practical winner).

---

## Approach 1 — Brute force (check every substring)

### Intuition
Try all O(n²) substrings; for each, verify it's a palindrome in O(n). Track the longest.

### Algorithm
1. For every pair `(i, j)` with `i <= j`, check if `s[i..j]` is a palindrome.
2. Keep the longest valid one.

### Dry run on `s = "babad"`
```
"b","a","b","a","d" all palindromes (len 1)
"bab" (i=0,j=2): s[0]==s[2]='b', inner "a" palindrome -> palindrome len 3 -> best
"aba" (i=1,j=3): also len 3
answer = "bab" (first found of max length)
```

### Code
```cpp
class Solution {
    bool isPal(const string& s, int i, int j) {
        while (i < j) {
            if (s[i] != s[j]) return false;
            i++; j--;
        }
        return true;
    }
public:
    string longestPalindrome(string s) {
        int n = s.size(), bestStart = 0, bestLen = 1;
        for (int i = 0; i < n; i++)
            for (int j = i; j < n; j++)
                if (j - i + 1 > bestLen && isPal(s, i, j)) {
                    bestStart = i;
                    bestLen = j - i + 1;
                }
        return s.substr(bestStart, bestLen);
    }
};
```
```java
class Solution {
    private boolean isPal(String s, int i, int j) {
        while (i < j) {
            if (s.charAt(i) != s.charAt(j)) return false;
            i++; j--;
        }
        return true;
    }
    public String longestPalindrome(String s) {
        int n = s.length(), bestStart = 0, bestLen = 1;
        for (int i = 0; i < n; i++)
            for (int j = i; j < n; j++)
                if (j - i + 1 > bestLen && isPal(s, i, j)) {
                    bestStart = i;
                    bestLen = j - i + 1;
                }
        return s.substring(bestStart, bestStart + bestLen);
    }
}
```
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def is_pal(i: int, j: int) -> bool:
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True

        n = len(s)
        best_start, best_len = 0, 1
        for i in range(n):
            for j in range(i, n):
                if j - i + 1 > best_len and is_pal(i, j):
                    best_start, best_len = i, j - i + 1
        return s[best_start:best_start + best_len]
```

### Complexity
- **Time**: O(n³) — O(n²) substrings × O(n) check.
- **Space**: O(1).

### Verdict
Correct, far too slow for n = 1000 (10⁹ ops). It's the baseline that establishes the palindrome check.

---

## Approach 2 — Dynamic programming table

### Intuition
Make the substructure explicit. `dp[i][j]` = "is `s[i..j]` a palindrome?" Then `dp[i][j] = (s[i]==s[j]) && (j-i < 2 || dp[i+1][j-1])`. The check becomes O(1) given the inner result, so total work is O(n²).

### Algorithm
1. Every single char is a palindrome: `dp[i][i] = true`.
2. Iterate by increasing length `len` from 2 to `n` (so inner substrings are already computed).
3. For each window `[i, j=i+len-1]`: `dp[i][j] = s[i]==s[j] && (len == 2 || dp[i+1][j-1])`.
4. Track the longest `[i, j]` that is `true`.

### Dry run on `s = "cbbd"`
```
len1: dp[i][i]=true for all
len2: dp[1][2]: s[1]=s[2]='b' -> true, len 2 -> best "bb"
      others false
len3,4: none extend
answer = "bb"
```

### Code
```cpp
class Solution {
public:
    string longestPalindrome(string s) {
        int n = s.size();
        vector<vector<bool>> dp(n, vector<bool>(n, false));
        int bestStart = 0, bestLen = 1;
        for (int i = 0; i < n; i++) dp[i][i] = true;
        for (int len = 2; len <= n; len++)
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                if (s[i] == s[j] && (len == 2 || dp[i + 1][j - 1])) {
                    dp[i][j] = true;
                    if (len > bestLen) { bestStart = i; bestLen = len; }
                }
            }
        return s.substr(bestStart, bestLen);
    }
};
```
```java
class Solution {
    public String longestPalindrome(String s) {
        int n = s.length();
        boolean[][] dp = new boolean[n][n];
        int bestStart = 0, bestLen = 1;
        for (int i = 0; i < n; i++) dp[i][i] = true;
        for (int len = 2; len <= n; len++)
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                if (s.charAt(i) == s.charAt(j) && (len == 2 || dp[i + 1][j - 1])) {
                    dp[i][j] = true;
                    if (len > bestLen) { bestStart = i; bestLen = len; }
                }
            }
        return s.substring(bestStart, bestStart + bestLen);
    }
}
```
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        best_start, best_len = 0, 1
        for i in range(n):
            dp[i][i] = True
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and (length == 2 or dp[i + 1][j - 1]):
                    dp[i][j] = True
                    if length > best_len:
                        best_start, best_len = i, length
        return s[best_start:best_start + best_len]
```

### Complexity
- **Time**: O(n²).
- **Space**: O(n²) for the table.

### Verdict
This is the "textbook DP" answer and shows the substructure cleanly. The O(n²) space is its weakness — and unnecessary, as the next approach shows.

---

## Approach 3 — Expand around center (optimal in practice) ⭐

### Intuition
We don't need a table — just visit each of the `2n-1` centers and expand outward while the two ends match. Each expansion is O(n), giving O(n²) time with **O(1)** space.

### Algorithm
1. For each index `i`:
   - Expand an **odd** palindrome centered at `(i, i)`.
   - Expand an **even** palindrome centered at `(i, i+1)`.
2. Each `expand(l, r)` widens while `s[l]==s[r]`; record the longest span seen.

### Dry run on `s = "babad"`
```
center i=0 odd: "b"
center i=1 odd: expand 'a' -> s[0]='b',s[2]='b' match -> "bab" (len 3) -> best
center i=2 odd: expand 'b' -> s[1]='a',s[3]='a' -> "aba" (len 3) tie (keep first)
even centers: no length>1
answer = "bab"
```

### Code
```cpp
class Solution {
    int start = 0, maxLen = 1;
    void expand(const string& s, int l, int r) {
        while (l >= 0 && r < (int)s.size() && s[l] == s[r]) { l--; r++; }
        if (r - l - 1 > maxLen) { maxLen = r - l - 1; start = l + 1; }
    }
public:
    string longestPalindrome(string s) {
        if (s.empty()) return "";
        for (int i = 0; i < (int)s.size(); i++) {
            expand(s, i, i);       // odd length
            expand(s, i, i + 1);   // even length
        }
        return s.substr(start, maxLen);
    }
};
```
```java
class Solution {
    private int start = 0, maxLen = 1;
    private void expand(String s, int l, int r) {
        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
        if (r - l - 1 > maxLen) { maxLen = r - l - 1; start = l + 1; }
    }
    public String longestPalindrome(String s) {
        if (s.isEmpty()) return "";
        for (int i = 0; i < s.length(); i++) {
            expand(s, i, i);
            expand(s, i, i + 1);
        }
        return s.substring(start, start + maxLen);
    }
}
```
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ""

        def expand(l: int, r: int) -> str:
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            return s[l + 1:r]

        for i in range(len(s)):
            for cand in (expand(i, i), expand(i, i + 1)):
                if len(cand) > len(res):
                    res = cand
        return res
```

### Complexity
- **Time**: O(n²) — n centers, each expands up to O(n).
- **Space**: O(1) (excluding the output string).

### Verdict
**The practical optimal.** Same time as the DP table but constant space and very little code. This is the standard interview answer. (For the theoretically optimal O(n), see Manacher's algorithm in Related problems.)

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n³) | O(1) | baseline, TLEs |
| DP table | O(n²) | O(n²) | makes substructure explicit |
| Expand around center | **O(n²)** | **O(1)** | the answer ⭐ |
| Manacher's | O(n) | O(n) | theoretical optimum, rarely needed |

---

## 🧪 Edge cases & pitfalls
- **Single character** → that character (length 1 is always a palindrome).
- **All same characters** (`"aaaa"`) → the whole string; expansion runs to both ends.
- **No palindrome longer than 1** (`"abcd"`) → return any single character (the first, given `maxLen` starts at 1).
- **Pitfall — forgetting even centers**: handling only odd centers misses `"bb"`. You must expand both `(i,i)` and `(i,i+1)`.
- **Pitfall — span arithmetic**: after `expand`, the loop overshoots by one on each side, so the matched length is `r - l - 1` and it starts at `l + 1`.

---

## 🔗 Related problems
- **Palindromic Substrings** (LC 647) — count all palindromic substrings (same expansion, count instead of measure).
- **Longest Palindromic Subsequence** (LC 516) — subsequence (non-contiguous), needs a 2D interval DP.
- **Palindrome Partitioning** (LC 131) — backtracking using palindrome checks.
- **Manacher's Algorithm** — O(n) longest palindromic substring.

---

**→ Next:** [`06-Palindromic-Substrings.md`](./06-Palindromic-Substrings.md) | **→ Prev:** [`04-House-Robber-II.md`](./04-House-Robber-II.md) | Back to [`00-Index.md`](./00-Index.md)
