# 🔤 KMP — Knuth-Morris-Pratt

> *"When a mismatch occurs, the matched portion tells you where to continue. Don't throw that away."*

For the full story, derivation, and case study, see [`../15-CASE-STUDIES-LEGENDARY/07-The-Story-of-KMP.md`](../15-CASE-STUDIES-LEGENDARY/07-The-Story-of-KMP.md).

---

## I. THE PROBLEM
Find all occurrences of pattern P (length m) in text T (length n) in O(n+m).

---

## II. THE FAILURE FUNCTION
`fail[i]` = length of the longest proper prefix of P[0..i] that is also a suffix.

When a mismatch occurs at P[j], instead of restarting, jump to P[fail[j-1]] — reusing the matched prefix.

---

## III. IMPLEMENTATION
```cpp
vector<int> computeFail(const string& p) {
    int m = p.size();
    vector<int> fail(m, 0);
    for (int i = 1, j = 0; i < m; ) {
        if (p[i] == p[j]) fail[i++] = ++j;
        else if (j > 0) j = fail[j-1];
        else fail[i++] = 0;
    }
    return fail;
}

vector<int> kmp(const string& t, const string& p) {
    int n = t.size(), m = p.size();
    auto fail = computeFail(p);
    vector<int> matches;
    for (int i = 0, j = 0; i < n; ) {
        if (t[i] == p[j]) {
            i++; j++;
            if (j == m) { matches.push_back(i - m); j = fail[j-1]; }
        } else if (j > 0) j = fail[j-1];
        else i++;
    }
    return matches;
}
```

---

## IV. WHY O(n+m)
Each character of T is examined a bounded number of times (amortized via the failure function). The pointer j increases at most n times and decreases at most n times. Total O(n) + O(m) for the failure function.

---

## V. APPLICATIONS
- Pattern matching
- Shortest palindrome: KMP on `s + "#" + reverse(s)`
- Longest happy prefix (LC 1392): `fail[n-1]`
- Repeated substring pattern: `n - fail[n-1]` divides `n`
- Counting occurrences

---

## VI. PROBLEMS
- Implement strStr (LC 28)
- Shortest Palindrome (LC 214)
- Longest Happy Prefix (LC 1392)
- Repeated Substring Pattern (LC 459)

---

**→ Next:** Z-algorithm, Rabin-Karp, Aho-Corasick, Suffix Array/Automaton & more → [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)
