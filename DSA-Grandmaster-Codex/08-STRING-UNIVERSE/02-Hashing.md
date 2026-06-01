# 🔤 String Hashing — Polynomial Rolling Hash

> *"Hashing turns a string into a number. Compare numbers in O(1) instead of strings in O(n)."*

---

## I. THE IDEA
Map a string to an integer (its "hash") so that:
- Equal strings → equal hashes (always)
- Different strings → different hashes (with high probability)

Then substring comparison becomes O(1) integer comparison.

---

## II. POLYNOMIAL ROLLING HASH
Treat the string as a number in base B:
```
H(s) = (s[0]·B^(n-1) + s[1]·B^(n-2) + ... + s[n-1]·B^0) mod P
```
- **B** (base): a number larger than the alphabet size, often prime (31, 131, 137, 1000000007-ish bases)
- **P** (modulus): a large prime (10^9+7, 10^9+9), to keep values bounded and reduce collisions

---

## III. PREFIX HASHES (the power move)
Precompute prefix hashes so ANY substring hash is O(1):
```cpp
const long long B = 131, P = 1e9 + 7;
vector<long long> h, pw;

void build(const string& s) {
    int n = s.size();
    h.assign(n + 1, 0);
    pw.assign(n + 1, 1);
    for (int i = 0; i < n; i++) {
        h[i+1] = (h[i] * B + s[i]) % P;
        pw[i+1] = (pw[i] * B) % P;
    }
}

// hash of s[l..r] inclusive, 0-indexed:
long long getHash(int l, int r) {
    return ((h[r+1] - h[l] * pw[r - l + 1]) % P + P) % P;
}
```
Build: O(n). Each substring hash: O(1).

---

## IV. ROLLING (sliding window) HASH
For Rabin-Karp pattern matching, "roll" the hash as the window slides:
```
new_hash = (old_hash - s[i]·B^(m-1)) · B + s[i+m]   (mod P)
```
This updates in O(1) instead of recomputing.

---

## V. COLLISIONS & ANTI-HASH
Two different strings can hash to the same value (collision). Probability ≈ 1/P per comparison.

### The threat (Codeforces anti-hash tests)
Adversaries craft inputs to force collisions on single-hash solutions (especially with small/known P, B).

### The defense: DOUBLE HASHING
Use TWO independent (B, P) pairs. Collision probability ≈ 1/(P1·P2) ≈ 10^-18.
```cpp
// Store hashes as pair<long long, long long> using two (B,P) sets.
// Two substrings are "equal" only if BOTH hashes match.
```

### Extra defense
- Randomize B at runtime (pick a random base in a range)
- Use P near 2^61 - 1 (a Mersenne prime) with __int128 multiplication

---

## VI. APPLICATIONS
1. **Substring equality** in O(1) — the core use
2. **Pattern matching** (Rabin-Karp): hash pattern, compare with each window
3. **Count distinct substrings**: hash all substrings, count unique (with care)
4. **Longest common substring of two strings**: binary search on length + hash sets
5. **Palindrome check**: compare forward hash with reverse hash
6. **Find repeated substrings**
7. **String periodicity / borders**

---

## VII. WORKED EXAMPLE: Longest Common Substring (binary search + hashing)
```
1. Binary search on length L
2. For candidate L: hash all length-L substrings of string A into a set
3. Check if any length-L substring of B is in the set
4. If yes, try larger L; else smaller
Complexity: O((n+m) log(min(n,m)))
```

---

## VIII. PITFALLS
- **Forgetting mod** → overflow → wrong hashes
- **Negative after subtraction** → add P before final mod
- **Single hash on CF** → hacked. Use double.
- **Comparing hashes when you should verify** → in interviews, after a hash match, optionally verify char-by-char for 100% correctness

---

## IX. PROBLEMS
- Implement strStr / Find the Index of the First Occurrence (LC 28) — via Rabin-Karp
- Repeated String Match (LC 686)
- Longest Duplicate Substring (LC 1044) — binary search + hashing ⭐
- Distinct Echo Substrings (LC 1316)
- Longest Happy Prefix (LC 1392) — KMP or hashing
- [CSES](https://cses.fi/problemset/): String Matching, Finding Borders, Finding Periods, Distinct Substrings

---

## X. TEMPLATE
See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/string-algorithms.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/string-algorithms.cpp) (StringHash struct).

---

**→ Next:** [`03-KMP.md`](./03-KMP.md) | All string algorithms → [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)
