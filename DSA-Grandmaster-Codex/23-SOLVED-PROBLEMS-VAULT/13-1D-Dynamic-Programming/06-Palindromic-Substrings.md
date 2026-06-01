# Palindromic Substrings

**Platform**: LeetCode 647 · **Difficulty**: Medium · **Topics**: Two Pointers, String, Dynamic Programming · **Pattern**: Palindrome DP / expand around center (counting)

---

## 📜 Problem Statement

Given a string `s`, return the **number of palindromic substrings** in it.

A string is a palindrome when it reads the same backward as forward. A **substring** is a contiguous sequence of characters within the string. Substrings with different start/end indices are counted separately, even if they consist of the same characters.

### Examples

**Example 1:**
```
Input:  s = "abc"
Output: 3
Explanation: Three palindromic substrings: "a", "b", "c".
```

**Example 2:**
```
Input:  s = "aaa"
Output: 6
Explanation: Six palindromic substrings: "a", "a", "a", "aa", "aa", "aaa".
```

**Example 3:**
```
Input:  s = "aba"
Output: 4
Explanation: "a", "b", "a", "aba".
```

### Constraints
```
1 <= s.length <= 1000
s consists of lowercase English letters.
```

---

## 🧠 Understanding the problem

This is the counting cousin of [Longest Palindromic Substring](./05-Longest-Palindromic-Substring.md). Instead of measuring the longest palindrome, we **count every** palindromic substring (positions matter, so `"aa"` at indices `[0,1]` and `[1,2]` count twice).

Same two structural facts apply:
1. Each palindrome is symmetric about one of `2n-1` centers.
2. `s[i..j]` is a palindrome iff `s[i]==s[j]` and `s[i+1..j-1]` is a palindrome → optimal substructure for a DP table.

---

## Approach 1 — Brute force

### Intuition
Enumerate all O(n²) substrings, check each in O(n), count the palindromes.

### Algorithm
1. For each `(i, j)` with `i <= j`, test if `s[i..j]` is a palindrome.
2. Increment a counter for each palindrome.

### Dry run on `s = "aaa"`
```
len1: "a","a","a" -> 3
len2: "aa"(0,1) yes, "aa"(1,2) yes -> +2 = 5
len3: "aaa"(0,2) yes -> +1 = 6
answer = 6
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
    int countSubstrings(string s) {
        int n = s.size(), count = 0;
        for (int i = 0; i < n; i++)
            for (int j = i; j < n; j++)
                if (isPal(s, i, j)) count++;
        return count;
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
    public int countSubstrings(String s) {
        int n = s.length(), count = 0;
        for (int i = 0; i < n; i++)
            for (int j = i; j < n; j++)
                if (isPal(s, i, j)) count++;
        return count;
    }
}
```
```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        def is_pal(i: int, j: int) -> bool:
            while i < j:
                if s[i] != s[j]:
                    return False
                i += 1
                j -= 1
            return True

        n = len(s)
        count = 0
        for i in range(n):
            for j in range(i, n):
                if is_pal(i, j):
                    count += 1
        return count
```

### Complexity
- **Time**: O(n³).
- **Space**: O(1).

### Verdict
Baseline only; too slow for n = 1000.

---

## Approach 2 — Dynamic programming table

### Intuition
`dp[i][j]` = is `s[i..j]` a palindrome. Count a `+1` for every `true` entry. Process by increasing length so inner windows are already known.

### Algorithm
1. `dp[i][i] = true` → count `n` single chars.
2. For length 2..n, for each window `[i, j]`: `dp[i][j] = s[i]==s[j] && (len==2 || dp[i+1][j-1])`; if true, `count++`.

### Dry run on `s = "aba"`
```
len1: dp[i][i] -> count 3
len2: dp[0][1] 'a'!='b' false; dp[1][2] 'b'!='a' false
len3: dp[0][2] s[0]=s[2]='a' and dp[1][1]=true -> true -> count 4
answer = 4
```

### Code
```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int n = s.size(), count = 0;
        vector<vector<bool>> dp(n, vector<bool>(n, false));
        for (int i = 0; i < n; i++) { dp[i][i] = true; count++; }
        for (int len = 2; len <= n; len++)
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                if (s[i] == s[j] && (len == 2 || dp[i + 1][j - 1])) {
                    dp[i][j] = true;
                    count++;
                }
            }
        return count;
    }
};
```
```java
class Solution {
    public int countSubstrings(String s) {
        int n = s.length(), count = 0;
        boolean[][] dp = new boolean[n][n];
        for (int i = 0; i < n; i++) { dp[i][i] = true; count++; }
        for (int len = 2; len <= n; len++)
            for (int i = 0; i + len - 1 < n; i++) {
                int j = i + len - 1;
                if (s.charAt(i) == s.charAt(j) && (len == 2 || dp[i + 1][j - 1])) {
                    dp[i][j] = true;
                    count++;
                }
            }
        return count;
    }
}
```
```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0
        for i in range(n):
            dp[i][i] = True
            count += 1
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1
                if s[i] == s[j] and (length == 2 or dp[i + 1][j - 1]):
                    dp[i][j] = True
                    count += 1
        return count
```

### Complexity
- **Time**: O(n²).
- **Space**: O(n²).

### Verdict
Clear DP, but the O(n²) space is avoidable.

---

## Approach 3 — Expand around center (optimal) ⭐

### Intuition
Every palindrome corresponds to exactly one center. Expand from each of the `2n-1` centers; each successful expansion *is* one more palindrome, so just count expansions.

### Algorithm
1. For each `i`: expand odd center `(i, i)` and even center `(i, i+1)`.
2. In each `expand(l, r)`, increment the count for every match, then widen.

### Dry run on `s = "aaa"`
```
i=0 odd: 'a' (count1); expand l=-1 stop
i=0 even (0,1): "aa" (count2); l=-1 stop
i=1 odd: 'a'(count3); expand (0,2) "aaa"(count4)
i=1 even (1,2): "aa"(count5)
i=2 odd: 'a'(count6); even (2,3) out of range
answer = 6
```

### Code
```cpp
class Solution {
public:
    int countSubstrings(string s) {
        int n = s.size(), count = 0;
        auto expand = [&](int l, int r) {
            while (l >= 0 && r < n && s[l] == s[r]) {
                count++;
                l--; r++;
            }
        };
        for (int i = 0; i < n; i++) {
            expand(i, i);      // odd
            expand(i, i + 1);  // even
        }
        return count;
    }
};
```
```java
class Solution {
    private int count = 0;
    private String s;
    private void expand(int l, int r) {
        while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) {
            count++;
            l--; r++;
        }
    }
    public int countSubstrings(String s) {
        this.s = s;
        for (int i = 0; i < s.length(); i++) {
            expand(i, i);
            expand(i, i + 1);
        }
        return count;
    }
}
```
```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0

        def expand(l: int, r: int) -> None:
            nonlocal count
            while l >= 0 and r < n and s[l] == s[r]:
                count += 1
                l -= 1
                r += 1

        for i in range(n):
            expand(i, i)
            expand(i, i + 1)
        return count
```

### Complexity
- **Time**: O(n²).
- **Space**: O(1).

### Verdict
**The optimal answer.** Same time as the DP table, constant space, and the cleanest code.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n³) | O(1) | baseline, TLEs |
| DP table | O(n²) | O(n²) | explicit substructure |
| Expand around center | **O(n²)** | **O(1)** | the answer ⭐ |
| Manacher's | O(n) | O(n) | counts via radius array, rarely needed |

---

## 🧪 Edge cases & pitfalls
- **Single character** → 1.
- **All distinct** (`"abc"`) → exactly `n` (only the single chars).
- **All identical** (`"aaaa"`) → `n(n+1)/2` (every substring is a palindrome).
- **Pitfall — counting inside expand**: increment the counter *each* time the window matches, not once per center. Every widened match is a distinct palindrome.
- **Pitfall — forgetting even centers** would undercount all even-length palindromes like `"aa"`.

---

## 🔗 Related problems
- **Longest Palindromic Substring** (LC 5) — same expansion, measure instead of count.
- **Longest Palindromic Subsequence** (LC 516) — non-contiguous, interval DP.
- **Palindrome Partitioning II** (LC 132) — min cuts, uses a palindrome table.
- **Count Different Palindromic Subsequences** (LC 730) — counts *distinct* palindromic subsequences (harder DP).

---

**→ Next:** [`07-Decode-Ways.md`](./07-Decode-Ways.md) | **→ Prev:** [`05-Longest-Palindromic-Substring.md`](./05-Longest-Palindromic-Substring.md) | Back to [`00-Index.md`](./00-Index.md)
