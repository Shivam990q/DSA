# 🔢 Combinatorics

> *"The art of counting without counting."*

---

## I. THE TWO RULES
- **Sum rule**: disjoint choices A (a ways) OR B (b ways) → a + b
- **Product rule**: independent steps A (a ways) AND B (b ways) → a × b

---

## II. PERMUTATIONS & COMBINATIONS
- **Permutations** (order matters): nPr = n!/(n−r)!
- **Combinations** (order doesn't): nCr = n!/(r!(n−r)!)
- nCr = nC(n−r); **Pascal**: nCr = (n−1)Cr + (n−1)C(r−1)
- Permutations of multiset: n! / (n1! n2! ... nk!)

---

## III. MODULAR nCr (the CP staple)
Precompute factorials + inverse factorials mod p:
```cpp
const int MOD = 1e9 + 7, MAXN = 1e6 + 5;
long long fact[MAXN], inv_fact[MAXN];
void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; i++) fact[i] = fact[i-1]*i % MOD;
    inv_fact[MAXN-1] = modpow(fact[MAXN-1], MOD-2, MOD);
    for (int i = MAXN-2; i >= 0; i--) inv_fact[i] = inv_fact[i+1]*(i+1) % MOD;
}
long long C(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD;
}
```
- **Lucas' theorem**: nCr mod p (prime) for huge n via base-p digits.

---

## IV. STARS AND BARS
Distribute n identical items into k distinct boxes:
- **≥ 0 per box**: C(n + k − 1, k − 1)
- **≥ 1 per box**: C(n − 1, k − 1)

---

## V. CATALAN NUMBERS
C_n = (1/(n+1))·C(2n, n) = C(2n,n) − C(2n,n+1)
Sequence: 1, 1, 2, 5, 14, 42, 132, ...
**Counts**:
- Valid parenthesizations of n pairs
- Binary trees with n nodes
- Triangulations of an (n+2)-gon
- Monotonic lattice paths not crossing the diagonal
- Ways to stack-sort

---

## VI. STIRLING & BELL NUMBERS
- **Stirling 2nd kind** S(n,k): partition n labeled objects into k non-empty unlabeled subsets. S(n,k)=k·S(n−1,k)+S(n−1,k−1).
- **Stirling 1st kind**: permutations of n with k cycles.
- **Bell number** B_n = Σ_k S(n,k): total partitions of an n-set.

---

## VII. INCLUSION-EXCLUSION
|A₁ ∪ ... ∪ Aₙ| = Σ|Aᵢ| − Σ|Aᵢ∩Aⱼ| + Σ|Aᵢ∩Aⱼ∩Aₖ| − ...
- Counting derangements, surjections, numbers divisible by some set of primes, etc.
- **Derangements** D_n = n!·Σ(−1)^k/k! ≈ n!/e.

---

## VIII. BURNSIDE'S LEMMA / PÓLYA COUNTING
Number of distinct configs under a symmetry group G:
(1/|G|)·Σ_{g∈G} |Fix(g)|
- Counting necklaces, colorings up to rotation/reflection.

---

## IX. BINOMIAL IDENTITIES (handy)
- Hockey stick: Σ_{i=r}^{n} C(i,r) = C(n+1, r+1)
- Vandermonde: Σ_k C(m,k)C(n,r−k) = C(m+n, r)
- Σ_k C(n,k) = 2^n; Σ_k k·C(n,k) = n·2^(n−1)

---

## X. PROBLEMS
- Unique Paths (LC 62) = C(m+n−2, m−1)
- Pascal's Triangle (LC 118/119)
- Different ways / Catalan: Unique BSTs (LC 96), Generate Parentheses (LC 22)
- [CSES](https://cses.fi/problemset/): Binomial Coefficients, Distributing Apples, Christmas Party (derangements), Bracket Sequences
- CF problems tagged "combinatorics"

---

**→ Next:** [`03-Probability-Expected-Value.md`](./03-Probability-Expected-Value.md)
