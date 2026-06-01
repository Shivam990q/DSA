# Longest Repeating Character Replacement

**Platform**: LeetCode 424 · **Difficulty**: Medium · **Topics**: String, Sliding Window · **Pattern**: Variable window + max-frequency trick

---

## 📜 Problem Statement

You are given a string `s` and an integer `k`. You can choose any character and change it to any other uppercase English letter. You can perform this operation at most `k` times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.

### Examples
```
Input: s = "AABABBA", k = 1 → Output: 4 (change one B in "AABA" → "AAAA")
Input: s = "ABAB", k = 2 → Output: 4
```

### Constraints
```
1 <= s.length <= 10^5
s consists of only uppercase English letters.
0 <= k <= s.length
```

---

## Approach — Sliding window + max frequency ⭐

### Key insight
A window [l, r] is valid if `(windowLen - maxFreqInWindow) <= k` — the non-majority chars can all be replaced.

Track `maxFreq` (the count of the most frequent char in the window). When invalid, shrink from left.

**Subtlety**: `maxFreq` doesn't need to be strictly accurate when shrinking — it never decreases the answer (the window only grows when a new maxFreq is found).

### Code
```cpp
int characterReplacement(string s, int k) {
    vector<int> cnt(26, 0);
    int l = 0, maxFreq = 0, best = 0;
    for (int r = 0; r < s.size(); r++) {
        maxFreq = max(maxFreq, ++cnt[s[r] - 'A']);
        while ((r - l + 1) - maxFreq > k) {
            cnt[s[l] - 'A']--;
            l++;
        }
        best = max(best, r - l + 1);
    }
    return best;
}
```
```java
public int characterReplacement(String s, int k) {
    int[] cnt = new int[26];
    int l = 0, maxFreq = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        maxFreq = Math.max(maxFreq, ++cnt[s.charAt(r) - 'A']);
        while ((r - l + 1) - maxFreq > k) {
            cnt[s.charAt(l) - 'A']--;
            l++;
        }
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```
```python
def characterReplacement(s, k):
    cnt = {}
    l = max_freq = best = 0
    for r, c in enumerate(s):
        cnt[c] = cnt.get(c, 0) + 1
        max_freq = max(max_freq, cnt[c])
        while (r - l + 1) - max_freq > k:
            cnt[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best
```

### Complexity: O(n) time, O(1) space (26 letters).

---

## 🧪 Edge cases
- k >= len → whole string. All same → len. k=0 → longest run of one char.

---

**→ Next:** [`04-Permutation-In-String.md`](./04-Permutation-In-String.md) | [Index](./00-Index.md)
