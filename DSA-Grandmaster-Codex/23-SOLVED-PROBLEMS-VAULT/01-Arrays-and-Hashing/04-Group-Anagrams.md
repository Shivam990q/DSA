# Group Anagrams

**Platform**: LeetCode 49 · **Difficulty**: Medium · **Topics**: Array, Hash Table, String, Sorting · **Pattern**: Canonical signature + bucketing

---

## 📜 Problem Statement

Given an array of strings `strs`, **group the anagrams** together. You can return the answer in any order.

### Examples

**Example 1:**
```
Input:  strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

**Example 2:**
```
Input:  strs = [""]
Output: [[""]]
```

**Example 3:**
```
Input:  strs = ["a"]
Output: [["a"]]
```

### Constraints
```
1 <= strs.length <= 10^4
0 <= strs[i].length <= 100
strs[i] consists of lowercase English letters.
```

---

## 🧠 Understanding the problem

Anagrams share something invariant — a **canonical signature** that is identical for all members of a group and different across groups. If we can compute that signature cheaply, we just bucket strings into a hash map keyed by signature.

Two natural signatures:
1. **Sorted string**: `"eat" → "aet"`, `"tea" → "aet"`. Same signature ⇒ same group.
2. **Character-count tuple**: count of each of 26 letters. `"eat" → (a:1,e:1,t:1)`.

---

## Approach 1 — Sorted-string key

### Intuition
Sort each string; anagrams collapse to the same sorted key. Group by that key.

### Algorithm
1. For each string `s`: compute `key = sorted(s)`.
2. Append `s` to `map[key]`.
3. Return all the map's value lists.

### Dry run
```
"eat" → "aet"  → map: {aet:[eat]}
"tea" → "aet"  → map: {aet:[eat,tea]}
"tan" → "ant"  → map: {aet:[eat,tea], ant:[tan]}
"ate" → "aet"  → map: {aet:[eat,tea,ate], ant:[tan]}
"nat" → "ant"  → {..., ant:[tan,nat]}
"bat" → "abt"  → {..., abt:[bat]}
result: [[eat,tea,ate],[tan,nat],[bat]]
```

### Code
```cpp
vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (string& s : strs) {
        string key = s;
        sort(key.begin(), key.end());
        groups[key].push_back(s);
    }
    vector<vector<string>> res;
    for (auto& [k, v] : groups) res.push_back(move(v));
    return res;
}
```
```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        char[] key = s.toCharArray();
        Arrays.sort(key);
        groups.computeIfAbsent(new String(key), k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```
```python
from collections import defaultdict
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

### Complexity
- **Time**: O(n · k log k), where n = number of strings, k = max string length (sorting each).
- **Space**: O(n · k).

### Verdict
Simple and reliable. The sort per string adds a `log k` factor we can remove.

---

## Approach 2 — Character-count key (optimal) ⭐

### Intuition
Instead of sorting, build a **count of the 26 letters** and use that as the key. Two strings are anagrams iff their counts match, and building the count is O(k) instead of O(k log k).

### Algorithm
1. For each string `s`: build `count[26]`.
2. Turn the count into a hashable key (e.g. a 26-length string like `"#1#0#0...#2"`, or a tuple).
3. Append `s` to `map[key]`.

### Dry run on `"eat"`
```
count = [a:1, ..., e:1, ..., t:1, ...]
key = "1#0#0#0#1#...#1#..."  (deterministic)
```

### Code
```cpp
vector<vector<string>> groupAnagrams(vector<string>& strs) {
    unordered_map<string, vector<string>> groups;
    for (string& s : strs) {
        int cnt[26] = {0};
        for (char c : s) cnt[c - 'a']++;
        // build a stable key from counts
        string key;
        for (int i = 0; i < 26; i++) {
            key += '#';
            key += to_string(cnt[i]);
        }
        groups[key].push_back(s);
    }
    vector<vector<string>> res;
    for (auto& [k, v] : groups) res.push_back(move(v));
    return res;
}
```
```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String s : strs) {
        int[] cnt = new int[26];
        for (char c : s.toCharArray()) cnt[c - 'a']++;
        // build a stable key from counts
        StringBuilder key = new StringBuilder();
        for (int i = 0; i < 26; i++) {
            key.append('#');
            key.append(cnt[i]);
        }
        groups.computeIfAbsent(key.toString(), k -> new ArrayList<>()).add(s);
    }
    return new ArrayList<>(groups.values());
}
```
```python
from collections import defaultdict
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - 97] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
```

### Complexity
- **Time**: O(n · k) — linear in total input size.
- **Space**: O(n · k).

### Verdict
**The optimal solution.** Removes the sort's log factor. The `#`-separator (or tuple) is important so that counts like `(1,12)` and `(11,2)` don't collide into the same string `"112"`.

---

## ⚖️ Approach comparison

| Approach | Key | Time | Space |
|----------|-----|------|-------|
| Sorted string | `sorted(s)` | O(n·k log k) | O(n·k) |
| Count tuple | 26-length count | **O(n·k)** | O(n·k) ⭐ |

For short strings the difference is negligible; for long strings the count key wins. The sorted key is more concise to write — a fine interview choice if you state the count alternative.

---

## 🧪 Edge cases & pitfalls
- **Empty string** `""` → its key is the empty/zero signature; all empty strings group together.
- **Single string** → one group of one.
- **Pitfall (count key)**: concatenating counts without a separator can collide. Use `#` between counts or a tuple.
- **Output order** doesn't matter, nor does order within a group.

---

## 🔗 Related problems
- **Valid Anagram** (LC 242) — the 2-string version (the signature idea originates here).
- **Find All Anagrams in a String** (LC 438) — sliding-window counts.
- **Group Shifted Strings** (LC 249) — same bucketing idea with a different signature.

---

**→ Next:** [`05-Top-K-Frequent-Elements.md`](./05-Top-K-Frequent-Elements.md) | Prev: [`03-Two-Sum.md`](./03-Two-Sum.md) | [Index](./00-Index.md)
