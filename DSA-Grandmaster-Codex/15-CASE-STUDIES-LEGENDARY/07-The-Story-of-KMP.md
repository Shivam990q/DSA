# 📖 Case Study: The Story of KMP

> *"Sometimes the greatest discovery is realizing that the wasted work isn't wasted after all."*

---

## I. THE PROBLEM

Find all occurrences of pattern P (length m) in text T (length n).

> Example: P = "abab", T = "ababcabab" → matches at positions 0, 5.

---

## II. BRUTE FORCE — O(nm)

For each i in T, compare P with T[i..i+m-1].

```cpp
for (int i = 0; i + m <= n; i++) {
    int j = 0;
    while (j < m && T[i+j] == P[j]) j++;
    if (j == m) report(i);
}
```

**Worst case**: T = "aaaaaaa...", P = "aaab" → mismatch always at last position. O(nm) = 10¹⁰ for n=m=10⁵. **TLE**.

---

## III. THE OBSERVATION (1977)

When mismatch occurs at P[j] vs T[i]:
> The last j characters of T (i.e., T[i-j..i-1]) MATCHED P[0..j-1].

So we **already know information** about T's recent history. Why throw it away?

**Key insight**: ask "what's the longest proper prefix of P[0..j-1] that's also its suffix?" Call it `fail[j]`.

If we slide P forward by `j - fail[j]`, we re-align P's prefix of length `fail[j]` with T's recent matched region. **No need to re-examine T.**

---

## IV. THE FAILURE FUNCTION

For pattern P, define:
> `fail[j]` = length of longest proper prefix of P[0..j] that is also its suffix.

Example: P = "abab"
- fail[0] = 0 (no proper prefix of "a")
- fail[1] = 0 (no prefix-suffix of "ab")
- fail[2] = 1 ("a" is both prefix and suffix of "aba")
- fail[3] = 2 ("ab" is both prefix and suffix of "abab")

---

## V. COMPUTING `fail[]` IN O(m)

```cpp
vector<int> computeFail(string& p) {
    int m = p.size();
    vector<int> fail(m, 0);
    for (int i = 1, j = 0; i < m; ) {
        if (p[i] == p[j]) {
            fail[i++] = ++j;
        } else if (j > 0) {
            j = fail[j-1];
        } else {
            fail[i++] = 0;
        }
    }
    return fail;
}
```

**Why O(m)?** Each character of P is "advanced" at most m times and "retreated" via fail at most m times. Amortized O(1) per character.

---

## VI. THE MATCHING — O(n)

```cpp
vector<int> kmp(string& T, string& P) {
    int n = T.size(), m = P.size();
    auto fail = computeFail(P);
    vector<int> matches;
    for (int i = 0, j = 0; i < n; ) {
        if (T[i] == P[j]) {
            i++; j++;
            if (j == m) {
                matches.push_back(i - m);
                j = fail[j-1];
            }
        } else if (j > 0) {
            j = fail[j-1];
        } else {
            i++;
        }
    }
    return matches;
}
```

**Why O(n+m)?** i advances at most n times. j advances at most n times (when characters match) and decreases at most n times (when fail backtracks). Total: O(n). + O(m) for fail. = O(n+m).

---

## VII. CORRECTNESS PROOF

**Claim**: KMP finds all matches.

**Proof sketch**: At any point, our algorithm maintains the invariant:
> *T[i-j..i-1] equals P[0..j-1]*

When T[i] == P[j], we extend the match (j++, i++).

When T[i] != P[j] with j > 0: we want the largest j' < j such that:
- P[0..j'-1] is a suffix of T[i-j..i-1]
- We can re-attempt matching T[i] vs P[j']

By definition of failure function, the largest such j' is `fail[j-1]`.

When T[i] != P[j] with j == 0: P doesn't start at T[i]; advance i.

By induction, no match is missed. □

---

## VIII. APPLICATIONS

### 1. Pattern matching
The original use case.

### 2. Shortest palindrome
Concat: `s + "#" + reverse(s)`. Run KMP on the concat. The failure value at the end tells you the longest palindromic prefix of s.

### 3. Longest happy prefix (LC 1392)
For string s, find longest proper prefix that's also a suffix. → fail[n-1].

### 4. Repeated substring pattern
A string is k+1 repetitions of some pattern iff `n - fail[n-1]` divides n.

### 5. Counting occurrences
KMP gives all matches in O(n).

---

## IX. MENTAL MODEL

> **"The matched portion of the pattern carries information.  
>  The failure function captures that information.  
>  The pattern's self-similarity is the key."**

This thinking — *"what does the pattern's structure tell us?"* — generalizes beyond strings.

---

## X. PATTERN EXTRACTION

### General principle
When a brute force does work it has already done, ask:
1. What information does the matched portion carry?
2. Can we precompute a function that captures it?
3. Can we use it to skip redundant work?

### Other algorithms born from this principle
- **Z-function**: similar to fail, computed differently
- **Suffix automaton**: full structure of all substrings
- **Aho-Corasick**: KMP for multiple patterns

---

## XI. ALTERNATIVES TO KMP

- **Z-algorithm**: simpler, often preferred in CP
- **Rabin-Karp**: rolling hash, O(n+m) expected
- **Boyer-Moore**: better practical performance for English text (skips ahead aggressively)

For interviews: KMP is the classic. For CP: Z-algorithm is often simpler.

---

## XII. HISTORICAL NOTE

Discovered independently by:
- Donald Knuth (1973)
- James Morris (1970)
- Vaughan Pratt

Published 1977 jointly. Became one of the foundational string algorithms.

---

**→ Next case study:** [`08-The-Story-of-Dijkstra.md`](./08-The-Story-of-Dijkstra.md)
