# 🔤 Suffix Array + LCP Array

> *"Sort all suffixes. Suddenly, a thousand string problems become easy."*

---

## I. WHAT IS A SUFFIX ARRAY
The suffix array SA of a string s is the array of starting indices of all suffixes of s, **sorted lexicographically**.

Example: s = `"banana"` (with suffixes)
```
suffixes sorted:        SA:
a            (idx 5)    5
ana          (idx 3)    3
anana        (idx 1)    1
banana       (idx 0)    0
na           (idx 4)    4
nana         (idx 2)    2
```
SA = [5, 3, 1, 0, 4, 2]

It's a compact alternative to a suffix tree (less memory, simpler).

---

## II. CONSTRUCTION
- **Naive**: sort n suffixes by comparison — O(n² log n)
- **Prefix-doubling**: sort by first 2^k chars, doubling each round — **O(n log² n)** (popular in CP)
- **O(n log n)** with radix sort instead of comparison sort
- **O(n)**: DC3 / SA-IS algorithms (used in libraries; complex)

### Prefix-doubling sketch (O(n log² n))
```cpp
vector<int> suffixArray(string s) {
    s += '$';                  // sentinel smaller than all chars
    int n = s.size();
    vector<int> sa(n), rank_(n), tmp(n);
    for (int i = 0; i < n; i++) { sa[i] = i; rank_[i] = s[i]; }
    for (int k = 1; k < n; k <<= 1) {
        auto cmp = [&](int a, int b) {
            if (rank_[a] != rank_[b]) return rank_[a] < rank_[b];
            int ra = a + k < n ? rank_[a + k] : -1;
            int rb = b + k < n ? rank_[b + k] : -1;
            return ra < rb;
        };
        sort(sa.begin(), sa.end(), cmp);
        tmp[sa[0]] = 0;
        for (int i = 1; i < n; i++)
            tmp[sa[i]] = tmp[sa[i-1]] + (cmp(sa[i-1], sa[i]) ? 1 : 0);
        rank_ = tmp;
    }
    return sa;
}
```

---

## III. THE LCP ARRAY (the companion)
`LCP[i]` = Longest Common Prefix between the suffixes SA[i] and SA[i-1] (adjacent in sorted order).

**Kasai's algorithm** computes LCP in O(n) given SA:
```cpp
vector<int> buildLCP(const string& s, const vector<int>& sa) {
    int n = s.size();
    vector<int> rank_(n), lcp(n, 0);
    for (int i = 0; i < n; i++) rank_[sa[i]] = i;
    int h = 0;
    for (int i = 0; i < n; i++) {
        if (rank_[i] > 0) {
            int j = sa[rank_[i] - 1];
            while (i + h < n && j + h < n && s[i + h] == s[j + h]) h++;
            lcp[rank_[i]] = h;
            if (h) h--;
        } else h = 0;
    }
    return lcp;
}
```

---

## IV. APPLICATIONS (this is the payoff)
1. **Pattern matching**: binary search P in SA — O(|P| log n)
2. **Number of distinct substrings**: `n(n+1)/2 − Σ LCP[i]` ⭐
3. **Longest repeated substring**: `max(LCP)` ⭐
4. **Longest common substring of two strings**: concatenate `s + '#' + t`, build SA+LCP, find max LCP between suffixes from different strings
5. **k-th smallest substring**
6. **Comparing substrings** in O(1) (with LCP + sparse table for RMQ)
7. **Counting substring occurrences**

---

## V. SUFFIX ARRAY VS SUFFIX AUTOMATON VS SUFFIX TREE
| Structure | Build | Memory | Best for |
|-----------|-------|--------|----------|
| Suffix Array | O(n log n) / O(n) | O(n) | sorting-based queries, distinct substrings, LCS |
| Suffix Automaton | O(n) | O(n) | counting, online, occurrences |
| Suffix Tree | O(n) | O(n) (bigger constant) | classic but complex; SA usually preferred |

---

## VI. PROBLEMS
- Longest Duplicate Substring (LC 1044) — SA or binary search + hash
- Distinct substrings count
- Longest common substring of two strings
- [CSES](https://cses.fi/problemset/): Distinct Substrings, Substring Order, String Matching, Repeating Substring
- CF problems tagged "suffix array" / "string suffix structures"

---

## VII. NOTE
Suffix arrays are a Level 7 (elite CP) topic. For interviews, hashing or KMP usually suffices. Learn SA when you hit advanced string problems on [Codeforces](https://codeforces.com)/ICPC.

Reference: https://cp-algorithms.com/string/suffix-array.html

---

**→ Next:** [`09-Suffix-Automaton.md`](./09-Suffix-Automaton.md)
