# 🔤 Complete String Algorithms Compendium

> Every string algorithm, with code & complexity & use case.

---

## 01 — STRING FOUNDATIONS

### Operations & complexity in C++ string
| Op                  | Complexity  |
|---------------------|-------------|
| length              | O(1)        |
| index access        | O(1)        |
| concat              | O(n + m)    |
| substr              | O(n)        |
| find (naive)        | O(nm)       |
| compare             | O(min(n,m)) |

### Naive substring search: O(nm)
For each i in t, check if t[i..i+m-1] == p.

---

## 02 — STRING HASHING

### Polynomial rolling hash
```
H(s) = (s[0]·B^(n-1) + s[1]·B^(n-2) + ... + s[n-1]) mod p
```
Common: B = 31, 131, 137; p = 10⁹+7 or 10⁹+9.

### Implementation
```cpp
const long long B = 131, P = 1e9 + 7;
vector<long long> h, pw;

void buildHash(string& s) {
    int n = s.size();
    h.assign(n + 1, 0); pw.assign(n + 1, 1);
    for (int i = 0; i < n; i++) {
        h[i+1] = (h[i] * B + s[i]) % P;
        pw[i+1] = (pw[i] * B) % P;
    }
}

long long getHash(int l, int r) {  // s[l..r], 0-indexed inclusive
    return (h[r+1] - h[l] * pw[r - l + 1] % P + P * P) % P;
}
```

### Anti-hack: double hashing
Use two different (B, P) pairs to avoid CF anti-hash attacks.

### Use cases
- Substring equality in O(1) after O(n) preprocess
- Find all occurrences of p in t (compare hashes)
- Distinct substrings (count unique hashes)

---

## 03 — KMP (Knuth-Morris-Pratt)

### Failure function
`fail[i]` = length of longest proper prefix of p[0..i] that is also a suffix.

```cpp
vector<int> computeFail(string& p) {
    int m = p.size();
    vector<int> fail(m, 0);
    for (int i = 1, j = 0; i < m; ) {
        if (p[i] == p[j]) fail[i++] = ++j;
        else if (j > 0) j = fail[j-1];
        else fail[i++] = 0;
    }
    return fail;
}

vector<int> kmp(string& t, string& p) {
    int n = t.size(), m = p.size();
    vector<int> fail = computeFail(p);
    vector<int> matches;
    for (int i = 0, j = 0; i < n; ) {
        if (t[i] == p[j]) { i++; j++; if (j == m) { matches.push_back(i - m); j = fail[j-1]; } }
        else if (j > 0) j = fail[j-1];
        else i++;
    }
    return matches;
}
```

**Complexity**: O(n + m).

### Use cases
- Pattern matching
- Shortest palindrome (KMP on s + "#" + reverse(s))
- Longest happy prefix
- Repeated substring pattern

---

## 04 — Z-ALGORITHM

`z[i]` = length of longest substring starting at i that matches a prefix of s.

```cpp
vector<int> zFunction(string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) { l = i; r = i + z[i]; }
    }
    return z;
}
```

**Complexity**: O(n).

### Pattern matching
Compute z on `p + '#' + t`. Wherever z[i] >= m, there's a match.

---

## 05 — RABIN-KARP

Rolling hash for substring search. O(n + m) expected; O(nm) worst (anti-hack).

```cpp
// Roll the hash as window slides:
// new_hash = (old_hash * B - s[i] * B^m + s[i+m]) mod P
```

---

## 06 — AHO-CORASICK

Multi-pattern matching: find all occurrences of any of P₁, P₂, ..., Pₖ in T.

### Build
1. Insert all patterns into a trie.
2. Build failure links (BFS): `fail[v]` = longest proper suffix of the string from root to v that's also a prefix in the trie.

### Search
Walk text; follow goto/fail links; report at every accept state on the suffix-link chain.

**Complexity**: O(|T| + Σ|P_i| + #matches).

### Use cases
- Multi-pattern dictionary search
- DNA sequence motif finding
- Network intrusion detection

---

## 07 — MANACHER'S ALGORITHM

Find longest palindromic substring in O(n).

### Idea
For each center, find longest palindrome. Use "mirror" to skip already-known.

```cpp
string longestPalindrome(string s) {
    string t = "^";
    for (char c : s) { t += '#'; t += c; }
    t += "#$";
    int n = t.size();
    vector<int> p(n, 0);
    int c = 0, r = 0;
    for (int i = 1; i < n - 1; i++) {
        int mirror = 2 * c - i;
        if (i < r) p[i] = min(r - i, p[mirror]);
        while (t[i + (1 + p[i])] == t[i - (1 + p[i])]) p[i]++;
        if (i + p[i] > r) { c = i; r = i + p[i]; }
    }
    int max_len = 0, center = 0;
    for (int i = 1; i < n - 1; i++)
        if (p[i] > max_len) { max_len = p[i]; center = i; }
    return s.substr((center - max_len) / 2, max_len);
}
```

---

## 08 — SUFFIX ARRAY

Sorted array of all suffix start indices.

### Construction (O(n log² n) sort-based, popular in CP)
```cpp
vector<int> suffixArray(string s) {
    s += '$';
    int n = s.size();
    vector<int> sa(n), rk(n), tmp(n);
    for (int i = 0; i < n; i++) { sa[i] = i; rk[i] = s[i]; }
    for (int k = 1; k < n; k *= 2) {
        auto cmp = [&](int a, int b) {
            if (rk[a] != rk[b]) return rk[a] < rk[b];
            int ra = a + k < n ? rk[a + k] : -1;
            int rb = b + k < n ? rk[b + k] : -1;
            return ra < rb;
        };
        sort(sa.begin(), sa.end(), cmp);
        tmp[sa[0]] = 0;
        for (int i = 1; i < n; i++)
            tmp[sa[i]] = tmp[sa[i-1]] + (cmp(sa[i-1], sa[i]) ? 1 : 0);
        rk = tmp;
    }
    return sa;
}
```

### LCP array (Kasai's, O(n))
LCP[i] = longest common prefix between sa[i] and sa[i-1].

### Use cases
- Substring queries
- Distinct substrings: n(n+1)/2 − Σ LCP[i]
- Longest repeated substring: max(LCP)
- Pattern matching: binary search

---

## 09 — SUFFIX AUTOMATON

Minimal DFA accepting all substrings of a string. Linear-time, online construction.

### Properties
- O(n) states (≤ 2n − 1)
- O(n) transitions (≤ 3n − 4)
- Each state represents an equivalence class of right extensions

### Use cases
- Number of distinct substrings: Σ (len[v] − len[link[v]])
- K-th lexicographic substring
- Substring occurrence count
- Longest common substring of two strings

```cpp
struct SAM {
    struct State { int len, link; map<char, int> next; long long cnt; };
    vector<State> st;
    int last;
    void init() { st.push_back({0, -1, {}, 0}); last = 0; }
    void extend(char c) {
        int cur = st.size(); st.push_back({st[last].len + 1, -1, {}, 1});
        int p = last;
        while (p != -1 && !st[p].next.count(c)) { st[p].next[c] = cur; p = st[p].link; }
        if (p == -1) st[cur].link = 0;
        else {
            int q = st[p].next[c];
            if (st[p].len + 1 == st[q].len) st[cur].link = q;
            else {
                int clone = st.size();
                st.push_back({st[p].len + 1, st[q].link, st[q].next, 0});
                while (p != -1 && st[p].next[c] == q) { st[p].next[c] = clone; p = st[p].link; }
                st[q].link = st[cur].link = clone;
            }
        }
        last = cur;
    }
};
```

---

## 10 — SUFFIX TREE

Compressed trie of all suffixes. O(n) construction (Ukkonen). Powerful but complex; suffix array often preferred in CP.

---

## 11 — PALINDROMIC TREE (EERTREE)

Linear-time DS where each node = a distinct palindromic substring.

### Use cases
- Count distinct palindromic substrings: O(n) total (≤ n+1 distinct palindromes)
- Number of palindromic occurrences

---

## 12 — STRING DP

### Edit distance (LC 72) ✓ in DP universe
### Longest palindromic subsequence (LC 516)
- `dp[i][j]` = longest palindromic subseq in s[i..j]
- `dp[i][j] = dp[i+1][j-1] + 2` if `s[i] == s[j]`, else `max(dp[i+1][j], dp[i][j-1])`

### Distinct subsequences (LC 115)
- `dp[i][j]` = ways to form t[0..j-1] from s[0..i-1]

### Wildcard / Regex matching ✓ in DP universe

---

## 13 — TRIE APPLICATIONS

(See [`../04-DATA-STRUCTURES-UNIVERSE/COMPENDIUM-Trees.md`](../04-DATA-STRUCTURES-UNIVERSE/COMPENDIUM-Trees.md) for fundamentals.)

### Use cases
- Autocomplete
- Spell checker (with edit distance traversal)
- IP routing (longest prefix match)
- Word search II (LC 212) — board + dictionary
- Maximum XOR of two numbers (binary trie)
- Stream of characters (online word matching)

---

## 14 — PROBLEM CATALOG

### Easy/Medium
1. Implement strStr (LC 28) — naive, KMP, Z, RK
2. Longest happy prefix (LC 1392) — KMP failure
3. Shortest palindrome (LC 214) — KMP on s+"#"+rev(s)
4. Longest palindromic substring (LC 5) — expand center / Manacher
5. Palindromic substrings (LC 647) — count
6. Distinct echo substrings (LC 1316)
7. Word break (LC 139)
8. Word break II (LC 140)
9. Longest valid parentheses (LC 32)
10. Decode ways (LC 91, 639)
11. ZigZag conversion (LC 6)
12. String to integer (LC 8)
13. Integer to roman / Roman to integer
14. Multiply strings (LC 43)
15. Compare version numbers (LC 165)

### Hard
16. Edit distance (LC 72)
17. Distinct subsequences (LC 115)
18. Wildcard matching (LC 44)
19. Regular expression matching (LC 10)
20. Substring with concatenation of all words (LC 30)
21. Minimum window substring (LC 76)
22. Word ladder I, II (LC 127, 126)
23. Word search II (LC 212) — Trie + DFS
24. Concatenated words (LC 472)
25. Stamping the sequence (LC 936)
26. Stream of characters (LC 1032)
27. Maximum XOR (LC 421) — Binary Trie
28. Distinct subsequences II (LC 940)
29. Number of substrings containing all three characters (LC 1358)
30. Frequency tracker (LC 2671)

### CP-level
31. [CSES](https://cses.fi/problemset/) "String Algorithms" (all)
32. [SPOJ](https://www.spoj.com) "Substring Cost"
33. CF problems tagged "string", "hashing"
34. UVa string problems

---

## 15 — RECOMMENDED READING

- **Algorithms on Strings, Trees, and Sequences** (Gusfield) — the bible
- **[CP-Algorithms.com](https://cp-algorithms.com)** — string section
- **Crochemore, Hancart, Lecroq** — Algorithms on Strings (advanced)

---

**→ Next universe:** [`../09-MATHEMATICS-UNIVERSE/00-Index.md`](../09-MATHEMATICS-UNIVERSE/00-Index.md)
