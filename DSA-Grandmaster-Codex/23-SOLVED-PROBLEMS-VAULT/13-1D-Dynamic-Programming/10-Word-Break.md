# Word Break

**Platform**: LeetCode 139 · **Difficulty**: Medium · **Topics**: Hash Table, String, Dynamic Programming, Trie, Memoization · **Pattern**: Prefix DP (segmentation reachability)

---

## 📜 Problem Statement

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

Note that the same word in the dictionary may be **reused multiple times** in the segmentation.

### Examples

**Example 1:**
```
Input:  s = "leetcode", wordDict = ["leet", "code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".
```

**Example 2:**
```
Input:  s = "applepenapple", wordDict = ["apple", "pen"]
Output: true
Explanation: "apple pen apple". Note that you are allowed to reuse a dictionary word.
```

**Example 3:**
```
Input:  s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
Output: false
```

### Constraints
```
1 <= s.length <= 300
1 <= wordDict.length <= 1000
1 <= wordDict[i].length <= 20
s and wordDict[i] consist of only lowercase English letters.
All the strings of wordDict are unique.
```

---

## 🧠 Understanding the problem

We ask: can the whole string be cut into dictionary words? The natural sub-question: *can the prefix of length `i` be fully segmented?* The prefix of length `i` is segmentable if there's some split point `j < i` such that the prefix of length `j` is segmentable **and** the chunk `s[j..i)` is a dictionary word.

Naively trying every cut is exponential (each position is a possible cut). Memoizing on "starting index" collapses it to polynomial because the segmentability of a suffix doesn't depend on how we got there.

5-step framework:
1. **State**: `dp[i]` = can `s[0..i)` (first `i` chars) be segmented.
2. **Transition**: `dp[i] = OR over j<i of (dp[j] AND s[j..i) in dict)`.
3. **Base case**: `dp[0] = true` (empty prefix trivially segmented).
4. **Order**: `i` from 1 to n.
5. **Answer**: `dp[n]`.

Put the dictionary in a hash set for O(1) (well, O(length)) membership.

---

## Approach 1 — Top-down memoization

### Intuition
`canBreak(start)` = can the suffix beginning at `start` be segmented. Try every end position; if `s[start..end)` is a word and the rest can break, succeed. Cache per `start`.

### Algorithm
1. If `start == n`, return true.
2. For `end` from `start+1` to `n`: if `s[start..end)` is in the dict and `canBreak(end)` → true.
3. Memoize on `start`.

### Dry run on `s = "leetcode", dict = {leet, code}`
```
canBreak(0): try "l","le",..., "leet" in dict -> canBreak(4)
canBreak(4): try "c",...,"code" in dict -> canBreak(8)
canBreak(8): start==n -> true
=> true
```

### Code
```cpp
class Solution {
    vector<int> memo;     // -1 unknown, 0 false, 1 true
    int n;
    bool solve(const string& s, int start, unordered_set<string>& dict) {
        if (start == n) return true;
        if (memo[start] != -1) return memo[start];
        for (int end = start + 1; end <= n; end++) {
            if (dict.count(s.substr(start, end - start)) && solve(s, end, dict))
                return memo[start] = 1;
        }
        return memo[start] = 0;
    }
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> dict(wordDict.begin(), wordDict.end());
        n = s.size();
        memo.assign(n + 1, -1);
        return solve(s, 0, dict);
    }
};
```
```java
class Solution {
    private Integer[] memo;
    private int n;
    private boolean solve(String s, int start, java.util.Set<String> dict) {
        if (start == n) return true;
        if (memo[start] != null) return memo[start];
        for (int end = start + 1; end <= n; end++) {
            if (dict.contains(s.substring(start, end)) && solve(s, end, dict)) {
                return memo[start] = true;
            }
        }
        return memo[start] = false;
    }
    public boolean wordBreak(String s, java.util.List<String> wordDict) {
        java.util.Set<String> dict = new java.util.HashSet<>(wordDict);
        n = s.length();
        memo = new Integer[n + 1];
        return solve(s, 0, dict);
    }
}
```
```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        from functools import lru_cache
        words = set(wordDict)
        n = len(s)

        @lru_cache(maxsize=None)
        def solve(start: int) -> bool:
            if start == n:
                return True
            for end in range(start + 1, n + 1):
                if s[start:end] in words and solve(end):
                    return True
            return False

        return solve(0)
```

### Complexity
- **Time**: O(n² × L) — n start positions, n ends, each substring/hash costs O(L).
- **Space**: O(n) memo + recursion + O(total dict chars) for the set.

### Verdict
Clean and natural. Bottom-up is the same idea iteratively.

---

## Approach 2 — Bottom-up tabulation (optimal) ⭐

### Intuition
Build `dp[i]` for prefixes left to right. `dp[i]` is true if some earlier reachable cut `dp[j]` is true and the chunk `s[j..i)` is a word.

### Algorithm
1. `dp[0] = true`.
2. For `i` from 1 to n, for `j` from 0 to i-1: if `dp[j]` and `s[j..i)` in dict, set `dp[i] = true` and break.
3. Return `dp[n]`.

### Dry run on `s = "applepenapple", dict = {apple, pen}`
```
dp[0]=true
dp[5]: j=0 dp[0]&&"apple" -> true
dp[8]: j=5 dp[5]&&"pen" -> true
dp[13]: j=8 dp[8]&&"apple" -> true
answer = true
```

### Code
```cpp
class Solution {
public:
    bool wordBreak(string s, vector<string>& wordDict) {
        unordered_set<string> dict(wordDict.begin(), wordDict.end());
        int n = s.size();
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int i = 1; i <= n; i++)
            for (int j = 0; j < i; j++)
                if (dp[j] && dict.count(s.substr(j, i - j))) {
                    dp[i] = true;
                    break;
                }
        return dp[n];
    }
};
```
```java
class Solution {
    public boolean wordBreak(String s, java.util.List<String> wordDict) {
        java.util.Set<String> dict = new java.util.HashSet<>(wordDict);
        int n = s.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        for (int i = 1; i <= n; i++)
            for (int j = 0; j < i; j++)
                if (dp[j] && dict.contains(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
        return dp[n];
    }
}
```
```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in words:
                    dp[i] = True
                    break
        return dp[n]
```

### Complexity
- **Time**: O(n² × L) (substring + hash per pair).
- **Space**: O(n) for `dp` + O(total dict chars).

### Verdict
**The standard answer.** A common micro-optimization: bound the inner split lengths by the maximum word length, so `j` only ranges over `[i - maxLen, i)`.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Memoization | O(n²·L) | O(n) | top-down on start index |
| Tabulation | O(n²·L) | O(n) | the standard answer ⭐ |

> A Trie of dictionary words replaces hash lookups with prefix walks and can prune early when no word extends the current prefix; same worst-case bound, faster in practice on large dictionaries.

---

## 🧪 Edge cases & pitfalls
- **Single-word match** (`s` itself is a dictionary word) → `dp[n]` becomes true via `j = 0`.
- **Unsegmentable tail** (`"catsandog"`) → false because no cut leaves `"og"` (or `"dog"` preceded by a valid prefix) as words.
- **Reuse allowed** → there is no "used" flag; the dictionary is a set, so words repeat freely.
- **Pitfall — early termination**: `break` after setting `dp[i] = true` is just an optimization; correctness doesn't require it.
- **Pitfall — substring cost**: each `s.substr/substring` is O(L). On very long strings, restricting `j` to within `maxWordLen` of `i` matters.

---

## 🔗 Related problems
- **Word Break II** (LC 140) — return *all* segmentations (backtracking + memo).
- **Concatenated Words** (LC 472) — words formed from other words (Word Break per candidate).
- **Palindrome Partitioning** (LC 131) — same "cut the string" shape with palindrome chunks.
- **Implement Trie** (LC 208) — the data structure used for the Trie-based optimization.

---

**→ Next:** [`11-Longest-Increasing-Subsequence.md`](./11-Longest-Increasing-Subsequence.md) | **→ Prev:** [`09-Maximum-Product-Subarray.md`](./09-Maximum-Product-Subarray.md) | Back to [`00-Index.md`](./00-Index.md)
