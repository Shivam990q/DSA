# 🔤 Manacher's Algorithm — Palindromes in O(n)

> *"Find the longest palindromic substring — and every palindrome — in linear time."*

---

## I. THE PROBLEM
Find the longest palindromic substring of s. Naive: O(n²) (expand around each center) or O(n³) (check all substrings). Manacher: **O(n)**.

---

## II. THE KEY INSIGHT
For each center, a palindrome has a "radius." If we're inside a known larger palindrome, we can **mirror** information from the symmetric position to skip redundant work — exactly like the Z-algorithm's box.

---

## III. THE TRANSFORM (handle even/odd uniformly)
Insert separators so every palindrome has odd length:
```
"abba"  →  "^#a#b#b#a#$"
```
(`^` and `$` are sentinels to avoid bounds checks; `#` between every char.)

Now odd and even palindromes both become odd-length in the transformed string.

---

## IV. IMPLEMENTATION
```cpp
string longestPalindrome(const string& s) {
    string t = "^";
    for (char c : s) { t += '#'; t += c; }
    t += "#$";
    int n = t.size();
    vector<int> p(n, 0);   // p[i] = radius of palindrome centered at i
    int c = 0, r = 0;      // center and right boundary of current rightmost palindrome
    for (int i = 1; i < n - 1; i++) {
        int mirror = 2 * c - i;
        if (i < r) p[i] = min(r - i, p[mirror]);   // mirror trick
        while (t[i + (1 + p[i])] == t[i - (1 + p[i])]) p[i]++;  // expand
        if (i + p[i] > r) { c = i; r = i + p[i]; } // update center
    }
    int maxLen = 0, center = 0;
    for (int i = 1; i < n - 1; i++)
        if (p[i] > maxLen) { maxLen = p[i]; center = i; }
    return s.substr((center - maxLen) / 2, maxLen);
}
```

**Why O(n)?** The right boundary `r` only moves forward; total expansion work is bounded by n.

---

## V. WHAT p[] GIVES YOU
- `p[i]` in the transformed string = the radius = the length of the palindrome centered at i in the ORIGINAL string.
- Sum of `(p[i]+1)/2` over all centers = **total count of palindromic substrings**.

---

## VI. APPLICATIONS
1. **Longest palindromic substring** (LC 5)
2. **Count palindromic substrings** (LC 647) — O(n) with Manacher
3. **Longest palindromic prefix/suffix**
4. Preprocessing for palindrome-partition DP
5. Finding all maximal palindromes

---

## VII. ALTERNATIVES
- **Expand around center**: O(n²) but simpler — fine for n ≤ a few thousand
- **DP**: O(n²) time + space — `dp[i][j]` = is s[i..j] a palindrome
- **Palindromic Tree (Eertree)**: counts distinct palindromes, also O(n)
- **Hashing**: compare forward vs reverse hash — O(1) palindrome check after O(n) build

For interviews, "expand around center" is usually enough; Manacher is the CP-grade O(n).

---

## VIII. PROBLEMS
- Longest Palindromic Substring (LC 5)
- Palindromic Substrings (LC 647)
- Longest Palindrome by Concatenating Two Letter Words (LC 2131) — different
- Maximum Product of the Length of Two Palindromic Substrings (LC 1960) — Manacher ⭐
- [CSES](https://cses.fi/problemset/): Longest Palindrome, Palindrome Queries

---

## IX. TEMPLATE
See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/string-algorithms.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/string-algorithms.cpp) (longestPalindrome).

---

**→ Next:** [`08-Suffix-Array.md`](./08-Suffix-Array.md)
