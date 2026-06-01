# Minimum Window Substring

**Platform**: LeetCode 76 · **Difficulty**: Hard · **Topics**: String, Sliding Window, Hash Table · **Pattern**: Variable window + formed counter

---

## 📜 Problem Statement

Given two strings `s` and `t`, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such window exists, return `""`.

### Examples
```
Input: s = "ADOBECODEBANC", t = "ABC" → Output: "BANC"
Input: s = "a", t = "a" → Output: "a"
Input: s = "a", t = "aa" → Output: "" (need two 'a's, only one available)
```

### Constraints
```
1 <= s.length, t.length <= 10^5
s and t consist of uppercase and lowercase English letters.
```

---

## Approach 1 — Brute force
Check every substring of s for containing all chars of t. O(n²·m). TLE.

---

## Approach 2 — Variable sliding window (optimal) ⭐

### Key insight
Expand right until the window "has" all needed chars. Then shrink left as far as possible while still valid. Track the minimum valid window.

Use a `need` map (required counts from t) and a `formed` counter (how many distinct chars have met their required count).

### Code
```cpp
string minWindow(string s, string t) {
    if (t.empty() || s.size() < t.size()) return "";
    unordered_map<char,int> need, win;
    for (char c : t) need[c]++;
    int required = need.size(), formed = 0;
    int l = 0, bestLen = INT_MAX, bestL = 0;
    for (int r = 0; r < s.size(); r++) {
        char c = s[r]; win[c]++;
        if (need.count(c) && win[c] == need[c]) formed++;
        while (formed == required) {
            if (r - l + 1 < bestLen) { bestLen = r - l + 1; bestL = l; }
            char d = s[l++]; win[d]--;
            if (need.count(d) && win[d] < need[d]) formed--;
        }
    }
    return bestLen == INT_MAX ? "" : s.substr(bestL, bestLen);
}
```
```java
public String minWindow(String s, String t) {
    if (t.isEmpty() || s.length() < t.length()) return "";
    Map<Character, Integer> need = new HashMap<>(), win = new HashMap<>();
    for (char c : t.toCharArray()) need.merge(c, 1, Integer::sum);
    int required = need.size(), formed = 0;
    int l = 0, bestLen = Integer.MAX_VALUE, bestL = 0;
    for (int r = 0; r < s.length(); r++) {
        char c = s.charAt(r);
        win.merge(c, 1, Integer::sum);
        if (need.containsKey(c) && win.get(c).intValue() == need.get(c).intValue()) formed++;
        while (formed == required) {
            if (r - l + 1 < bestLen) { bestLen = r - l + 1; bestL = l; }
            char d = s.charAt(l++);
            win.merge(d, -1, Integer::sum);
            if (need.containsKey(d) && win.get(d) < need.get(d)) formed--;
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
}
```
```python
from collections import Counter
def minWindow(s, t):
    if not t or len(s) < len(t): return ""
    need = Counter(t)
    required = len(need)
    win = {}; formed = 0
    l = 0; best = (float('inf'), 0, 0)
    for r, c in enumerate(s):
        win[c] = win.get(c, 0) + 1
        if c in need and win[c] == need[c]: formed += 1
        while formed == required:
            if r - l + 1 < best[0]: best = (r - l + 1, l, r)
            d = s[l]; l += 1; win[d] -= 1
            if d in need and win[d] < need[d]: formed -= 1
    return "" if best[0] == float('inf') else s[best[1]:best[2]+1]
```

### Complexity: O(n + m) time, O(alphabet) space.

### Verdict: **The optimal answer.** The `formed` counter avoids re-checking all 26+ chars each step.

---

## 🧪 Edge cases
- t has duplicate chars (need count, not just presence). No valid window → "". t longer than s → "".
- **Pitfall**: comparing `win[c] == need[c]` (not `>=`) for the `formed` increment — only count when we FIRST meet the requirement.

---

**→ Next:** [`06-Sliding-Window-Maximum.md`](./06-Sliding-Window-Maximum.md) | [Index](./00-Index.md)
