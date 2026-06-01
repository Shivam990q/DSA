# Longest Substring Without Repeating Characters

**Platform**: LeetCode 3 · **Difficulty**: Medium · **Topics**: String, Hash Table, Sliding Window · **Pattern**: Variable-size window + last-seen map

---

## 📜 Problem Statement

Given a string `s`, find the length of the **longest substring** without repeating characters.

### Examples

**Example 1:**
```
Input:  s = "abcabcbb"
Output: 3
Explanation: "abc" (length 3).
```

**Example 2:**
```
Input:  s = "bbbbb"
Output: 1
```

**Example 3:**
```
Input:  s = "pwwkew"
Output: 3
Explanation: "wke" (length 3). Note: "pwke" is a subsequence, not a substring.
```

### Constraints
```
0 <= s.length <= 5 * 10^4
s consists of English letters, digits, symbols and spaces.
```

---

## Approach 1 — Brute force

Check every substring for uniqueness. O(n³) with set check, O(n²) with early break.

### Complexity: O(n²) best, O(n³) naive. TLE.

---

## Approach 2 — Sliding window + hash set

### Intuition
Maintain window [l, r] with all distinct chars (tracked in a set). Expand r; if duplicate, shrink l until unique again.

### Code
```cpp
int lengthOfLongestSubstring(string s) {
    unordered_set<char> win;
    int l = 0, best = 0;
    for (int r = 0; r < s.size(); r++) {
        while (win.count(s[r])) win.erase(s[l++]);
        win.insert(s[r]);
        best = max(best, r - l + 1);
    }
    return best;
}
```
```java
public int lengthOfLongestSubstring(String s) {
    Set<Character> win = new HashSet<>();
    int l = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        while (win.contains(s.charAt(r))) win.remove(s.charAt(l++));
        win.add(s.charAt(r));
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```
```python
def lengthOfLongestSubstring(s):
    win = set()
    l = best = 0
    for r, c in enumerate(s):
        while c in win:
            win.remove(s[l]); l += 1
        win.add(c)
        best = max(best, r - l + 1)
    return best
```

### Complexity: O(n) time (each char added/removed once), O(min(n, alphabet)) space.

---

## Approach 3 — Sliding window + last-index map (optimal) ⭐

### Intuition
Instead of shrinking one-by-one, jump `l` directly past the last occurrence of the duplicate char.

### Code
```cpp
int lengthOfLongestSubstring(string s) {
    unordered_map<char, int> last;
    int l = 0, best = 0;
    for (int r = 0; r < s.size(); r++) {
        if (last.count(s[r]) && last[s[r]] >= l)
            l = last[s[r]] + 1;
        last[s[r]] = r;
        best = max(best, r - l + 1);
    }
    return best;
}
```
```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> last = new HashMap<>();
    int l = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        if (last.containsKey(c) && last.get(c) >= l)
            l = last.get(c) + 1;
        last.put(c, r);
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```
```python
def lengthOfLongestSubstring(s):
    last = {}
    l = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= l:
            l = last[c] + 1
        last[c] = r
        best = max(best, r - l + 1)
    return best
```

### Complexity: O(n) time, O(min(n, alphabet)) space.

### Verdict: **Optimal.** Single pass, no inner while loop.

---

## 🧪 Edge cases
- Empty string → 0. Single char → 1. All same → 1. All distinct → n.
- **Pitfall**: `last[c] >= l` check is essential — old occurrences before `l` are irrelevant.

---

## 🔗 Related
- LC 159/340: Longest with at most K distinct. LC 424: Longest repeating char replacement.

---

**→ Next:** [`03-Longest-Repeating-Char-Replacement.md`](./03-Longest-Repeating-Char-Replacement.md) | [Index](./00-Index.md)
