# 🔢 Euler's Totient Function φ(n)

> *"How many numbers below n are coprime to it? That count powers modular arithmetic."*

---

## I. DEFINITION
φ(n) = count of integers in [1, n] that are coprime to n (gcd = 1).
- φ(1) = 1, φ(2) = 1, φ(6) = 2 (1,5), φ(9) = 6, φ(p) = p−1 for prime p.

---

## II. FORMULA
For n = p₁^a₁ · p₂^a₂ · ... · pₖ^aₖ:
```
φ(n) = n · Π (1 − 1/pᵢ)   over distinct prime factors pᵢ
```
- φ(p) = p − 1
- φ(p^k) = p^k − p^(k−1) = p^(k−1)·(p−1)
- **Multiplicative**: φ(mn) = φ(m)·φ(n) when gcd(m,n)=1

---

## III. COMPUTING φ
### Single n: O(√n)
```cpp
long long phi(long long n) {
    long long result = n;
    for (long long p = 2; p*p <= n; p++)
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    if (n > 1) result -= result / n;
    return result;
}
```
### All φ(1..N): O(N log log N) (sieve)
```cpp
vector<int> phiSieve(int n) {
    vector<int> phi(n+1);
    iota(phi.begin(), phi.end(), 0);
    for (int i = 2; i <= n; i++)
        if (phi[i] == i)  // i is prime
            for (int j = i; j <= n; j += i)
                phi[j] -= phi[j] / i;
    return phi;
}
```

---

## IV. EULER'S THEOREM
If gcd(a, n) = 1: **a^φ(n) ≡ 1 (mod n)**.
- Generalizes Fermat's little theorem (which is the case n = prime, φ(p)=p−1).
- Used for **modular inverse** when m is not prime: a⁻¹ = a^(φ(m)−1) mod m (needs gcd(a,m)=1).
- **Reducing huge exponents**: a^b mod n = a^(b mod φ(n)) mod n (with conditions; "Euler's theorem for exponents" / extended for non-coprime case).

---

## V. KEY IDENTITY
**Σ_{d|n} φ(d) = n**

(The sum of totients over all divisors of n equals n.) Beautiful and useful in divisor-sum manipulations and Dirichlet convolutions (φ = μ * id).

---

## VI. APPLICATIONS
- Counting coprime numbers/fractions (Farey sequence length = Σφ)
- Modular inverse for non-prime modulus
- Reducing exponents in modular exponentiation (tower of powers)
- Number-theoretic sums (with Möbius)
- Order of elements in modular groups, primitive roots

---

## VII. PROBLEMS
- [CSES](https://cses.fi/problemset/) "Counting Coprime Pairs", "Euler's Totient" style problems
- Count coprime numbers ≤ n
- Sum of φ over a range
- Tower of exponents mod m (a^a^a... mod m using φ recursively)
- CF problems tagged "number theory"

---

## VIII. NOTE
φ is fundamental — appears in cryptography (RSA: φ(pq)=(p−1)(q−1)), modular inverses, and countless CP number-theory problems.

---

**→ Next:** [`09-Game-Theory.md`](./09-Game-Theory.md)
