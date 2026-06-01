# Valid Anagram

**Platform**: LeetCode 242 · **Difficulty**: Easy · **Topics**: String, Hash Table, Sorting · **Pattern**: Frequency counting

---

## 📜 Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an **anagram** of `s`, and `false` otherwise.

An **anagram** is a word formed by rearranging the letters of another, using **all the original letters exactly once**.

### Examples

**Example 1:**
```
Input:  s = "anagram", t = "nagaram"
Output: true
```

**Example 2:**
```
Input:  s = "rat", t = "car"
Output: false
Explanation: 'c' appears in t but not in s.
```

### Constraints
```
1 <= s.length, t.length <= 5 * 10^4
s and t consist of lowercase English letters.
```

### Follow-up
What if the inputs contain **Unicode** characters? How would you adapt your solution?

---

## 🧠 Understanding the problem

Two strings are anagrams **iff** they have the same multiset of characters — same letters with the same counts. Order doesn't matter. Two immediate consequences:

1. If lengths differ, they can't be anagrams (early exit).
2. Comparing "multisets of characters" can be done by **sorting** (canonical order) or **counting** (frequency map).

---

## Approach 1 — Sort both and compare

### Intuition
Anagrams become **identical** once sorted. `"anagram"` and `"nagaram"` both sort to `"aaagmnr"`.

### Algorithm
1. If `s.length != t.length` → return `false`.
2. Sort both strings.
3. Return whether the sorted strings are equal.

### Dry run
```
s="anagram" → "aaagmnr"
t="nagaram" → "aaagmnr"
equal → true
```

### Code
```cpp
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    sort(s.begin(), s.end());
    sort(t.begin(), t.end());
    return s == t;
}
```
```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    char[] a = s.toCharArray();
    char[] b = t.toCharArray();
    Arrays.sort(a);
    Arrays.sort(b);
    return Arrays.equals(a, b);
}
```
```python
def isAnagram(s, t):
    return sorted(s) == sorted(t)
```

### Complexity
- **Time**: O(n log n) for sorting.
- **Space**: O(1) to O(n) depending on the sort implementation.

### Verdict
Clean and short. Often the fastest to write in an interview. But we can do better than the log factor with counting.

---

## Approach 2 — Count array (optimal for lowercase letters) ⭐

### Intuition
We don't need sorted order, only the **counts**. With a fixed 26-letter alphabet, a single integer array of size 26 acts as the frequency map. Add for `s`, subtract for `t`; if everything cancels to zero, it's an anagram.

### Algorithm
1. If lengths differ → return `false`.
2. Create `count[26] = {0}`.
3. For each char in `s`: `count[c - 'a']++`.
4. For each char in `t`: `count[c - 'a']--`; if it drops below 0, return `false` early.
5. Return `true` (all counts balanced).

### Dry run on `s="rat", t="car"`
```
after s: r:1, a:1, t:1
process t:
  c → count[c] becomes -1 → return false
```

### Code
```cpp
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    array<int, 26> count{};            // all zeros
    for (char c : s) count[c - 'a']++;
    for (char c : t)
        if (--count[c - 'a'] < 0) return false;
    return true;
}
```
```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] count = new int[26];             // all zeros
    for (char c : s.toCharArray()) count[c - 'a']++;
    for (char c : t.toCharArray())
        if (--count[c - 'a'] < 0) return false;
    return true;
}
```
```python
def isAnagram(s, t):
    if len(s) != len(t):
        return False
    count = [0] * 26
    for c in s:
        count[ord(c) - 97] += 1
    for c in t:
        count[ord(c) - 97] -= 1
        if count[ord(c) - 97] < 0:
            return False
    return True
```

### Complexity
- **Time**: O(n) — two linear passes.
- **Space**: O(1) — the array is a fixed 26 ints regardless of input size.

### Verdict
**The optimal answer for the stated constraints** (lowercase English). Linear time, constant space, single early-exit.

---

## Approach 3 — Hash map (handles the Unicode follow-up) ⭐

### Intuition
The size-26 array assumes lowercase English. For arbitrary characters (Unicode), swap the fixed array for a **hash map** keyed by character. Same counting logic, now general.

### Algorithm
1. If lengths differ → `false`.
2. Count characters of `s` in a map.
3. Decrement using `t`; any missing key or negative count → `false`.
4. Return `true`.

### Code
```cpp
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    unordered_map<char,int> count;
    for (char c : s) count[c]++;
    for (char c : t)
        if (--count[c] < 0) return false;
    return true;
}
```
```java
public boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    Map<Character, Integer> count = new HashMap<>();
    for (char c : s.toCharArray()) count.merge(c, 1, Integer::sum);
    for (char c : t.toCharArray()) {
        int updated = count.merge(c, -1, Integer::sum);
        if (updated < 0) return false;
    }
    return true;
}
```
```python
from collections import Counter
def isAnagram(s, t):
    return Counter(s) == Counter(t)
```

### Complexity
- **Time**: O(n).
- **Space**: O(k) where k = number of distinct characters.

### Verdict
The right answer to the **Unicode follow-up**. Slightly more overhead than the array, but works for any alphabet. In an interview, mention: "For lowercase only I'd use a size-26 array; for Unicode I'd use a hash map."

---

## ⚖️ Approach comparison

| Approach | Time | Space | Best for |
|----------|------|-------|----------|
| Sort | O(n log n) | O(1)–O(n) | shortest to write |
| Count array | **O(n)** | **O(1)** | lowercase English (optimal) ⭐ |
| Hash map | O(n) | O(k) | Unicode / arbitrary alphabet |

---

## 🧪 Edge cases & pitfalls
- **Different lengths** → immediate `false`. Always check first; it's the cheapest filter.
- **Empty strings** → two empty strings are anagrams (`true`).
- **Same string** → `true` (a string is an anagram of itself).
- **Pitfall**: comparing only the *set* of characters (ignoring counts) is wrong — `"aab"` vs `"abb"` share the same letters but aren't anagrams. Always compare **counts**.

---

## 🔗 Related problems
- **Group Anagrams** (LC 49) — bucket strings by their anagram signature.
- **Find All Anagrams in a String** (LC 438) — sliding window of counts.
- **Valid Anagram with frequency** ideas reused in many string problems.

---

**→ Next:** [`03-Two-Sum.md`](./03-Two-Sum.md) | Prev: [`01-Contains-Duplicate.md`](./01-Contains-Duplicate.md) | [Index](./00-Index.md)
