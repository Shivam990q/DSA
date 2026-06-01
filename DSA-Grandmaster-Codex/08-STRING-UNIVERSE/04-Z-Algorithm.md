# 🔤 Z-Algorithm

> *"For each position, how long does the prefix match starting here? Answer all of them in O(n)."*

---

## I. THE Z-ARRAY
For a string s of length n, `z[i]` = length of the longest substring starting at index i that is **also a prefix of s**.

By convention `z[0] = 0` (or n; not used).

Example: s = `"aabaab"`
```
index:  0 1 2 3 4 5
char:   a a b a a b
z:      0 1 0 3 1 0
```
(z[3]=3 because "aab" starting at index 3 matches the prefix "aab".)

---

## II. THE ALGORITHM (O(n))
Maintain a "Z-box" [l, r] = the rightmost interval that matches a prefix.

```cpp
vector<int> zFunction(const string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i < r) z[i] = min(r - i, z[i - l]);   // reuse previous computation
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;  // extend
        if (i + z[i] > r) { l = i; r = i + z[i]; }  // update box
    }
    return z;
}
```

**Why O(n)?** The `r` pointer only moves forward, total at most n. Each character comparison either advances r or fails once per i.

---

## III. PATTERN MATCHING WITH Z
To find pattern P in text T:
1. Build string `S = P + '#' + T` (# is a separator not in either)
2. Compute Z-array of S
3. Wherever `z[i] >= |P|`, there's a match at position `i - |P| - 1` in T

```cpp
vector<int> match(const string& text, const string& pat) {
    string s = pat + "#" + text;
    auto z = zFunction(s);
    int m = pat.size();
    vector<int> res;
    for (int i = m + 1; i < (int)s.size(); i++)
        if (z[i] >= m) res.push_back(i - m - 1);
    return res;
}
```
O(n + m).

---

## IV. Z vs KMP
| Aspect | Z-algorithm | KMP |
|--------|------------|-----|
| Computes | prefix-match length at each position | failure function (longest proper prefix-suffix) |
| Pattern matching | yes (with separator) | yes (native) |
| Simplicity | often considered simpler/cleaner | classic |
| Use in CP | very popular | popular |

Both are O(n+m). Many competitors prefer Z for its conceptual clarity.

---

## V. APPLICATIONS
1. **Pattern matching** (above)
2. **Count occurrences of pattern**
3. **Number of distinct substrings** (with suffix structures, Z helps in some constructions)
4. **String periodicity / smallest period**
5. **Longest prefix that is also a suffix** (borders)
6. **Compression detection** (find repeating units)

---

## VI. PERIODICITY VIA Z
A string s has period p (i.e., s[i] == s[i+p]) related to positions where `z[i] + i == n`. The smallest period can be derived from the Z-array.

---

## VII. PROBLEMS
- Implement strStr (LC 28)
- Shortest Palindrome (LC 214) — Z on rev(s) + "#" + s
- Longest Happy Prefix (LC 1392)
- Sum of Scores of Built Strings (LC 2223) — direct Z-function application ⭐
- [CSES](https://cses.fi/problemset/): String Matching, Finding Borders, Finding Periods

---

## VIII. TEMPLATE
See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/string-algorithms.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/string-algorithms.cpp) (zFunction).

---

**→ Next:** Rabin-Karp, Aho-Corasick, Manacher, Suffix structures → [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)
