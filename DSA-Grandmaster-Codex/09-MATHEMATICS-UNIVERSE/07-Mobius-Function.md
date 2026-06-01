# 🔢 Möbius Function & Inversion

> *"The inclusion-exclusion of number theory."*

---

## I. DEFINITION
μ(n):
- μ(1) = 1
- μ(n) = (−1)^k if n is a product of k **distinct** primes (square-free)
- μ(n) = 0 if n has any squared prime factor (not square-free)

Examples: μ(1)=1, μ(2)=−1, μ(6)=1 (2·3), μ(4)=0, μ(12)=0 (4·3), μ(30)=−1 (2·3·5).

---

## II. COMPUTING μ FOR ALL n ≤ N
Via a linear/smallest-prime-factor sieve:
```cpp
vector<int> mobius(int n) {
    vector<int> mu(n+1, 0), primes;
    vector<bool> comp(n+1, false);
    mu[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!comp[i]) { primes.push_back(i); mu[i] = -1; }
        for (int p : primes) {
            if ((long long)i*p > n) break;
            comp[i*p] = true;
            if (i % p == 0) { mu[i*p] = 0; break; }
            else mu[i*p] = -mu[i];
        }
    }
    return mu;
}
```

---

## III. KEY PROPERTY
Σ_{d|n} μ(d) = [n == 1]  (1 if n=1, else 0)

This "indicator" property is what makes Möbius the inclusion-exclusion tool of number theory.

---

## IV. MÖBIUS INVERSION
If **f(n) = Σ_{d|n} g(d)**, then **g(n) = Σ_{d|n} μ(n/d) f(d)**.

Lets you "invert" sums over divisors.

---

## V. THE COPRIME-COUNTING TECHNIQUE ⭐
To count pairs (i, j) with gcd = 1, or sums over coprimality:
- Use Σ_{d | gcd} μ(d) = [gcd == 1]
- Count pairs both divisible by d, weight by μ(d), sum over d.

### Example: count coprime pairs in [1, n]
Answer = Σ_{d=1}^{n} μ(d) · C(⌊n/d⌋, 2)  (pairs both divisible by d)

### Example: count pairs with gcd = k
Reduce to coprime counting on ⌊n/k⌋.

---

## VI. DIRICHLET & MULTIPLICATIVE FUNCTIONS
- μ, φ, d, σ are **multiplicative** (f(mn)=f(m)f(n) for coprime m,n)
- **Dirichlet convolution**: (f * g)(n) = Σ_{d|n} f(d) g(n/d)
- μ is the Dirichlet inverse of the constant-1 function
- φ = μ * id (i.e., Σ_{d|n} φ(d) = n)

---

## VII. APPLICATIONS
- Counting coprime pairs / tuples
- Sum of gcd over pairs
- Counting square-free numbers
- Möbius + divisor sieve for number-theoretic sums (e.g., Σ gcd(i,j))
- Combined with **divisor-block (√n) decomposition** for sums like Σ⌊n/i⌋

---

## VIII. PROBLEMS
- Count coprime pairs ([CSES](https://cses.fi/problemset/) "Counting Coprime Pairs")
- Sum of gcd / lcm over pairs (CF problems)
- Square-free counting
- CF problems tagged "number theory" + "mobius"

---

## IX. NOTE
Möbius is a Level 6-7 CP topic. It's the natural tool whenever you need inclusion-exclusion over divisibility.

---

**→ Next:** [`08-Euler-Totient.md`](./08-Euler-Totient.md)
