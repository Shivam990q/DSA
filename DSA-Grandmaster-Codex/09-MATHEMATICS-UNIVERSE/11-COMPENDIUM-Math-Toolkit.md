# 📐 Complete Math Toolkit Compendium

> Every formula, every algorithm, every theorem you'll need.

---

## 01 — NUMBER THEORY

### GCD / LCM
```cpp
long long gcd(long long a, long long b) { return b == 0 ? a : gcd(b, a % b); }
long long lcm(long long a, long long b) { return a / gcd(a, b) * b; }
```
- Time: O(log min(a, b))
- Properties: gcd(a, b) = gcd(a − b, b) = gcd(a, b mod a) = gcd(a, b − a)

### Extended Euclidean
Find x, y s.t. a·x + b·y = gcd(a, b).
```cpp
long long extGcd(long long a, long long b, long long& x, long long& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    long long x1, y1;
    long long d = extGcd(b, a % b, x1, y1);
    x = y1; y = x1 - (a / b) * y1;
    return d;
}
```

### Modular inverse
- If m prime: `inv(a) = a^(m-2) mod m` (Fermat's little theorem)
- General: extended Euclidean

```cpp
long long modPow(long long b, long long e, long long m) {
    long long r = 1 % m;
    b %= m;
    while (e > 0) {
        if (e & 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}

long long modInv(long long a, long long m) {  // m prime
    return modPow(a, m - 2, m);
}
```

### Sieve of Eratosthenes
```cpp
vector<bool> sieve(int n) {
    vector<bool> is(n + 1, true);
    is[0] = is[1] = false;
    for (int i = 2; (long long)i * i <= n; i++)
        if (is[i])
            for (int j = i * i; j <= n; j += i) is[j] = false;
    return is;
}
```
Time: O(n log log n).

### Linear sieve (with smallest prime factor)
```cpp
vector<int> spf(int n) {
    vector<int> spf(n + 1, 0); vector<int> primes;
    for (int i = 2; i <= n; i++) {
        if (spf[i] == 0) { spf[i] = i; primes.push_back(i); }
        for (int p : primes) {
            if (p > spf[i] || (long long)i * p > n) break;
            spf[i * p] = p;
        }
    }
    return spf;
}
```

### Miller-Rabin primality (deterministic for 64-bit)
For n < 3.3×10²⁴, test with witnesses {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}.

### Pollard's Rho factorization
Probabilistic O(n^(1/4)) factorization.

### Euler's totient φ(n) = count of integers in [1, n] coprime to n
- For prime p: φ(p) = p - 1
- φ(p^k) = p^k − p^(k−1)
- φ(mn) = φ(m)φ(n) if gcd(m,n) = 1
- φ(n) = n · Π (1 − 1/p) for prime p | n

### Fermat's little theorem
For p prime, a^p ≡ a (mod p). If gcd(a, p) = 1, a^(p-1) ≡ 1 (mod p).

### Euler's theorem
If gcd(a, n) = 1, a^φ(n) ≡ 1 (mod n).

### Chinese Remainder Theorem (CRT)
Given x ≡ a₁ (mod m₁), x ≡ a₂ (mod m₂), ... with pairwise coprime mᵢ, there's a unique solution mod M = ∏ mᵢ.

### Möbius function μ(n)
- μ(1) = 1
- μ(n) = (−1)^k if n is product of k distinct primes
- μ(n) = 0 if n has a squared prime factor

**Möbius inversion**: if f(n) = Σ over d | n: g(d), then g(n) = Σ over d | n: μ(n/d) · f(d).

---

## 02 — COMBINATORICS

### Factorial & nCr (precomputed)
```cpp
const int MAXN = 1e6;
const int MOD = 1e9 + 7;
long long fact[MAXN], inv_fact[MAXN];

void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; i++) fact[i] = fact[i-1] * i % MOD;
    inv_fact[MAXN-1] = modInv(fact[MAXN-1], MOD);
    for (int i = MAXN-2; i >= 0; i--) inv_fact[i] = inv_fact[i+1] * (i+1) % MOD;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD;
}
```

### Pascal's identity
nCr = (n-1)Cr + (n-1)C(r-1)

### Hockey stick identity
Σ from i=r to n: iCr = (n+1)C(r+1)

### Catalan numbers
C_n = (1/(n+1)) · 2nCn = 2nCn − 2nC(n+1)

C_0 = 1, C_1 = 1, C_2 = 2, C_3 = 5, C_4 = 14, ...

**Counts**:
- Valid parentheses with n pairs
- Binary trees with n nodes
- Triangulations of (n+2)-gon
- Monotonic paths in n×n grid not crossing diagonal
- Stack permutations

### Stars and bars
Number of ways to place n indistinguishable balls in k distinguishable boxes:
- With ≥0 per box: (n + k - 1) C (k - 1)
- With ≥1 per box: (n - 1) C (k - 1)

### Stirling numbers
- **2nd kind** S(n, k): partition n objects into k non-empty subsets
- **1st kind** s(n, k): permutations of n with k cycles

### Bell numbers
B_n = number of partitions of an n-element set. B_n = Σ S(n, k).

### Inclusion-Exclusion
|A₁ ∪ A₂ ∪ ... ∪ Aₙ| = Σ|Aᵢ| − Σ|Aᵢ ∩ Aⱼ| + Σ|Aᵢ ∩ Aⱼ ∩ Aₖ| − ...

### Burnside's lemma
Number of distinct configurations under group of symmetries G:
|configs| / |G| · Σ over g in G: |fix(g)|

---

## 03 — PROBABILITY & EXPECTED VALUE

### Definitions
- P(A) = |favorable| / |total|
- E[X] = Σ x · P(X = x)

### Linearity of expectation (always holds, even for dependent variables!)
E[X + Y] = E[X] + E[Y]

### Conditional probability
P(A | B) = P(A ∩ B) / P(B)

### Bayes' theorem
P(A | B) = P(B | A) · P(A) / P(B)

### Common probability tricks
- **Indicator variables**: X_i = 1 if event i, 0 else. E[count] = Σ P(event i).
- **Independence**: P(A ∩ B) = P(A) · P(B).

### Random walk on line
After n steps, expected position = 0. Expected (position²) = n.

---

## 04 — LINEAR ALGEBRA

### Matrix multiplication
A is n×m, B is m×p. C = AB is n×p with C[i][j] = Σ A[i][k] · B[k][j].
Time: O(nmp). Strassen: O(n^2.81). Best known: O(n^2.371).

### Matrix exponentiation
For solving linear recurrences: F(n+1) = a·F(n) + b·F(n-1) → matrix [[a, b], [1, 0]]^n.

```cpp
typedef vector<vector<long long>> Matrix;

Matrix mul(const Matrix& A, const Matrix& B, long long m) {
    int n = A.size();
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int k = 0; k < n; k++)
            for (int j = 0; j < n; j++)
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % m;
    return C;
}

Matrix matPow(Matrix A, long long e, long long m) {
    int n = A.size();
    Matrix R(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++) R[i][i] = 1;  // identity
    while (e > 0) {
        if (e & 1) R = mul(R, A, m);
        A = mul(A, A, m);
        e >>= 1;
    }
    return R;
}
```

### Use cases
- Fibonacci in O(log n): [F(n+1), F(n)]^T = [[1,1],[1,0]]^n · [1, 0]^T
- Path counting in graph (adj matrix^k)
- Linear recurrences

### Gaussian elimination
Solve Ax = b in O(n³). Also computes determinant, rank, inverse.

---

## 05 — FFT / NTT

Polynomial multiplication of degree-n polynomials in O(n log n).

### FFT (over complex numbers)
- Compute DFT in O(n log n) via Cooley-Tukey divide & conquer
- Convert: time domain ↔ frequency domain
- Multiplication = pointwise in frequency

### NTT (Number Theoretic Transform)
- FFT analog mod prime p with primitive root
- p = c · 2^k + 1 (e.g., p = 998244353 = 119 · 2^23 + 1)
- Avoids floating-point errors

### Use cases
- Polynomial multiplication
- Big integer multiplication
- Counting subsets with specific sum
- String matching (with wildcards via convolution)
- Sum/XOR/AND/OR convolutions (FWHT for XOR)

---

## 06 — MODULAR ARITHMETIC PATTERNS

```cpp
// Safe modular subtract
long long subMod(long long a, long long b, long long m) { return (a - b + m) % m; }

// Modular addition
long long addMod(long long a, long long b, long long m) { return (a + b) % m; }

// Modular multiplication (with potential overflow handling)
long long mulMod(long long a, long long b, long long m) {
    return (__int128)a * b % m;  // for m up to 10^18
}
```

---

## 07 — GAME THEORY

### Combinatorial games (impartial)
Both players have same moves. Last move wins (normal play).

### Sprague-Grundy theorem
Every impartial game equivalent to a Nim heap of size = its Grundy number.

```
grundy(state) = mex({grundy(next_state) : next_state reachable})
where mex(S) = smallest non-negative integer not in S
```

For sum of independent games: grundy = XOR of grundies.

### Nim
Several piles. Each move: remove ≥1 from one pile. First player loses iff XOR of pile sizes = 0.

### Misère Nim
Slight variant: last move loses. Different (but related) analysis.

### Stone game variants
- Stone Game (LC 877): always Alice wins
- Stone Game II-IX: various DP-based game theory
- Nim-like with constraints

---

## 08 — GENERATING FUNCTIONS

### Ordinary generating function
For sequence a_n: A(x) = Σ a_n · x^n.

### Common GFs
- 1/(1-x) = Σ x^n
- x/(1-x)² = Σ n · x^n
- (1+x)^n = Σ nCk · x^k

### Use cases
- Solve recurrences (Fibonacci closed form)
- Count partitions with constraints
- Combinatorial identity proofs

---

## 09 — TOP MATH PROBLEMS

1. Pow(x, n) — fast exponentiation (LC 50)
2. Sqrt(x) — Newton or BS (LC 69)
3. Count primes (LC 204)
4. Happy number (LC 202)
5. Excel sheet column number (LC 171)
6. Fraction to recurring decimal (LC 166)
7. Permutation sequence (LC 60)
8. Reverse integer (LC 7)
9. String to integer (LC 8)
10. Integer to English words (LC 273)
11. Roman to integer / Integer to roman (LC 12, 13)
12. Basic calculator I, II, III (LC 224, 227, 772)
13. Factorial trailing zeros (LC 172)
14. Bulb switcher (LC 319) — perfect squares
15. Random pick with weight (LC 528)
16. Random point in a circle (LC 478)
17. Implement rand10 from rand7 (LC 470)
18. Super pow (LC 372)

### CP-level
19. Euler's totient computation
20. Modular nCr for large n
21. Linear recurrence via matrix exp
22. Number of solutions to ax + by = c (Diophantine)
23. CRT
24. Discrete logarithm
25. Number of distinct paths in grid (combinatorial)
26. [CSES](https://cses.fi/problemset/) "Mathematics" section (all)

---

## 10 — RECOMMENDED READING

- **Concrete Mathematics** (Knuth, Patashnik, Graham) ⭐
- **An Introduction to the Theory of Numbers** (Hardy, Wright)
- **Generatingfunctionology** (Wilf) — free
- **Mitzenmacher, Upfal**: *Probability and Computing*
- **Ross**: *A First Course in Probability*

---

**→ Next universe:** [`../10-GEOMETRY-UNIVERSE/00-Index.md`](../10-GEOMETRY-UNIVERSE/00-Index.md)
