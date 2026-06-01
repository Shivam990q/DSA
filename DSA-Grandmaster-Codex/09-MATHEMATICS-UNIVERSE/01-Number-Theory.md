# 🔢 Number Theory

> *"The queen of mathematics, and the backbone of cryptography and competitive programming."*

---

## I. DIVISIBILITY & GCD
- a | b means "a divides b"
- **gcd(a, b)** = greatest common divisor; **lcm(a, b)** = a·b/gcd(a,b)
- **Euclidean algorithm**: gcd(a, b) = gcd(b, a mod b). O(log min(a,b)).
```cpp
long long gcd(long long a, long long b) { return b ? gcd(b, a % b) : a; }
```
- Properties: gcd(a,b)=gcd(a-b,b); gcd is associative; gcd(0,a)=a.

---

## II. EXTENDED EUCLIDEAN
Find x, y such that a·x + b·y = gcd(a, b):
```cpp
long long extgcd(long long a, long long b, long long &x, long long &y) {
    if (!b) { x = 1; y = 0; return a; }
    long long x1, y1, g = extgcd(b, a % b, x1, y1);
    x = y1; y = x1 - (a / b) * y1;
    return g;
}
```
Used for modular inverse and solving linear Diophantine equations ax + by = c.

---

## III. PRIMES
- A prime has exactly 2 divisors (1 and itself).
- **Trial division** primality: check divisors up to √n. O(√n).
- **Sieve of Eratosthenes**: all primes ≤ n in O(n log log n).
```cpp
vector<bool> sieve(int n) {
    vector<bool> is(n+1, true); is[0]=is[1]=false;
    for (int i = 2; (long long)i*i <= n; i++)
        if (is[i]) for (int j = i*i; j <= n; j += i) is[j] = false;
    return is;
}
```
- **Linear sieve**: also gives smallest prime factor (SPF) in O(n).
- **Miller-Rabin**: probabilistic (deterministic for 64-bit with fixed witnesses) primality for large n.
- **Pollard's Rho**: factorize large n in ~O(n^(1/4)).

---

## IV. MODULAR ARITHMETIC
- (a+b) mod m, (a·b) mod m: apply mod after each op to avoid overflow.
- **Fast exponentiation** (binary exp): a^b mod m in O(log b).
```cpp
long long modpow(long long a, long long b, long long m) {
    long long r = 1 % m; a %= m;
    while (b) { if (b&1) r = r*a%m; a = a*a%m; b >>= 1; }
    return r;
}
```
- **Modular inverse**:
  - If m prime: a^(-1) = a^(m-2) mod m (Fermat's little theorem).
  - General (gcd(a,m)=1): use extended Euclidean.
- **Modular division**: a/b mod m = a · b^(-1) mod m.

---

## V. KEY THEOREMS
- **Fermat's Little Theorem**: if p prime, a^(p-1) ≡ 1 (mod p) for gcd(a,p)=1.
- **Euler's Theorem**: a^φ(n) ≡ 1 (mod n) for gcd(a,n)=1.
- **Wilson's Theorem**: (p-1)! ≡ -1 (mod p) iff p prime.
- **Chinese Remainder Theorem (CRT)**: solve a system of congruences with pairwise-coprime moduli — unique solution mod the product.

---

## VI. EULER'S TOTIENT φ(n)
Count of integers in [1, n] coprime to n.
- φ(p) = p−1 for prime p
- φ(p^k) = p^k − p^(k−1)
- Multiplicative: φ(mn) = φ(m)φ(n) if gcd(m,n)=1
- φ(n) = n · Π(1 − 1/p) over distinct prime factors p

---

## VII. DIVISOR FUNCTIONS
- **d(n)** / τ(n): number of divisors = Π(e_i + 1) for prime factorization Π p_i^e_i
- **σ(n)**: sum of divisors = Π( (p_i^(e_i+1) − 1)/(p_i − 1) )
- Compute for all n ≤ N via sieve-like methods in O(N log N).

---

## VIII. MÖBIUS FUNCTION & INVERSION
- μ(1)=1; μ(n)=(−1)^k if n is product of k distinct primes; μ(n)=0 if any squared prime factor.
- **Möbius inversion**: if f(n)=Σ_{d|n} g(d), then g(n)=Σ_{d|n} μ(n/d) f(d).
- Powers many counting problems (e.g., counting coprime pairs).

---

## IX. APPLICATIONS IN CP
- Counting coprime pairs/divisors
- Modular combinatorics (nCr mod p)
- Cryptography basics (RSA uses modular exponentiation + factoring hardness)
- Cycle/period problems (modular)
- GCD/LCM over arrays, GCD-based DP

---

## X. PROBLEMS
- Count Primes (LC 204), Pow(x,n) (LC 50), GCD of Strings (LC 1071)
- [CSES](https://cses.fi/problemset/) "Mathematics" section: Exponentiation, Counting Divisors, Common Divisors, Counting Coprime Pairs, etc.
- [Project Euler](https://projecteuler.net) problems 1-100 (great number theory practice)
- CF problems tagged "number theory"

---

## XI. TEMPLATE
See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/number-theory.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/number-theory.cpp).

---

**→ Next:** [`02-Combinatorics.md`](./02-Combinatorics.md) | Full toolkit → [`11-COMPENDIUM-Math-Toolkit.md`](./11-COMPENDIUM-Math-Toolkit.md)
