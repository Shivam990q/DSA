# 🔤 Rabin-Karp — Hashing-Based Pattern Matching

> *"Hash the pattern once. Roll the hash across the text. Match in O(n) expected."*

---

## I. THE IDEA
1. Compute the hash of the pattern P (length m).
2. Compute the hash of the first window T[0..m-1].
3. Slide the window one char at a time, **rolling** the hash in O(1).
4. When hashes match, (optionally) verify char-by-char to rule out collisions.

---

## II. THE ROLLING HASH UPDATE
When the window moves from [i, i+m-1] to [i+1, i+m]:
```
new = (old - T[i]·B^(m-1)) · B + T[i+m]   (mod P)
```
This removes the leftmost char's contribution, shifts, and adds the new rightmost char — all O(1).

---

## III. IMPLEMENTATION
```cpp
const long long B = 131, P = 1e9 + 7;

vector<int> rabinKarp(const string& t, const string& p) {
    int n = t.size(), m = p.size();
    if (m > n) return {};
    long long pHash = 0, tHash = 0, power = 1;
    for (int i = 0; i < m; i++) {
        pHash = (pHash * B + p[i]) % P;
        tHash = (tHash * B + t[i]) % P;
        if (i) power = (power * B) % P;
    }
    vector<int> res;
    for (int i = 0; i + m <= n; i++) {
        if (pHash == tHash) {
            // verify to avoid collision false positives
            if (t.compare(i, m, p) == 0) res.push_back(i);
        }
        if (i + m < n) {
            tHash = ((tHash - t[i] * power % P + P * P) % P * B + t[i + m]) % P;
        }
    }
    return res;
}
```

---

## IV. COMPLEXITY
- **Average / expected**: O(n + m)
- **Worst case**: O(nm) — when many hash collisions force verification (adversarial)
- Use **double hashing** to make collisions astronomically unlikely (skip verification)

---

## V. RABIN-KARP VS KMP/Z
| Aspect | Rabin-Karp | KMP / Z |
|--------|-----------|---------|
| Worst case | O(nm) (collisions) | O(n+m) guaranteed |
| Average | O(n+m) | O(n+m) |
| Multiple patterns | easy (hash set of pattern hashes) ⭐ | needs Aho-Corasick |
| 2D pattern matching | extends naturally ⭐ | harder |
| Simplicity | very simple | medium |

**Use Rabin-Karp when**: multiple patterns of the same length, 2D matching, or you already have a hashing setup.

---

## VI. MULTI-PATTERN MATCHING (Rabin-Karp's strength)
To search for k patterns all of length m:
1. Hash all k patterns into a hash set.
2. Roll one hash across the text.
3. At each window, check if the hash is in the set.

O(n + k·m) expected.

---

## VII. 2D RABIN-KARP
For finding a 2D pattern in a 2D grid: hash each row, then hash columns of row-hashes. Powerful for image/matrix matching.

---

## VIII. PROBLEMS
- Implement strStr (LC 28)
- Repeated String Match (LC 686)
- Longest Duplicate Substring (LC 1044) — binary search + rolling hash ⭐
- Distinct Echo Substrings (LC 1316)
- Find substring with concatenation (variations)

---

**→ Next:** [`06-Aho-Corasick.md`](./06-Aho-Corasick.md) | Full toolkit → [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)
