# Permutation in String

**Platform**: LeetCode 567 · **Difficulty**: Medium · **Topics**: String, Sliding Window, Hash Table · **Pattern**: Fixed-size window + frequency match

---

## 📜 Problem Statement

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise. (i.e., one of `s1`'s permutations is a substring of `s2`.)

### Examples
```
Input: s1 = "ab", s2 = "eidbaooo" → Output: true ("ba" is a permutation of "ab")
Input: s1 = "ab", s2 = "eidboaoo" → Output: false
```

### Constraints
```
1 <= s1.length, s2.length <= 10^4
s1 and s2 consist of lowercase English letters.
```

---

## Approach — Fixed-size sliding window ⭐

### Key insight
A permutation of s1 has the same character frequencies. Slide a window of size `len(s1)` over s2; compare frequency arrays at each position.

### Code
```cpp
bool checkInclusion(string s1, string s2) {
    if (s1.size() > s2.size()) return false;
    vector<int> need(26, 0), win(26, 0);
    int m = s1.size();
    for (char c : s1) need[c - 'a']++;
    for (int i = 0; i < s2.size(); i++) {
        win[s2[i] - 'a']++;
        if (i >= m) win[s2[i - m] - 'a']--;
        if (win == need) return true;
    }
    return false;
}
```
```java
public boolean checkInclusion(String s1, String s2) {
    if (s1.length() > s2.length()) return false;
    int[] need = new int[26], win = new int[26];
    int m = s1.length();
    for (char c : s1.toCharArray()) need[c - 'a']++;
    for (int i = 0; i < s2.length(); i++) {
        win[s2.charAt(i) - 'a']++;
        if (i >= m) win[s2.charAt(i - m) - 'a']--;
        if (Arrays.equals(win, need)) return true;
    }
    return false;
}
```
```python
def checkInclusion(s1, s2):
    if len(s1) > len(s2): return False
    need = [0]*26; win = [0]*26
    m = len(s1)
    for c in s1: need[ord(c)-97] += 1
    for i, c in enumerate(s2):
        win[ord(c)-97] += 1
        if i >= m: win[ord(s2[i-m])-97] -= 1
        if win == need: return True
    return False
```

### Complexity: O(n) time (26-element compare is O(1)), O(1) space.

**Optimization**: instead of comparing full arrays, track a `matches` counter (how many of 26 positions match). Update on add/remove → O(1) per step without the 26-compare.

---

## 🧪 Edge cases
- s1 longer than s2 → false. s1 == s2 → true. Single char.

---

**→ Next:** [`05-Minimum-Window-Substring.md`](./05-Minimum-Window-Substring.md) | [Index](./00-Index.md)
