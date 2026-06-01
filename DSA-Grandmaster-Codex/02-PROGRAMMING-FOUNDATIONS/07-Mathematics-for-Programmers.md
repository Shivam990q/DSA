# ➗ Mathematics for Programmers

> *"You don't need to be a mathematician. But you need to think like one."*

---

## I. THE TOOLKIT (TOP 30)

The math you'll use in DSA / CP / interviews:

### Discrete Math
1. **Sets, relations, functions**
2. **Logic** (and, or, not, implications, quantifiers)
3. **Proof techniques** (direct, contradiction, induction, contrapositive)
4. **Permutations & combinations** (factorials, nCr, nPr)
5. **Pigeonhole principle**
6. **Inclusion-exclusion**
7. **Recurrences and generating functions**

### Number Theory
8. **Divisibility, GCD, LCM, Euclidean algorithm**
9. **Primes and Sieve of Eratosthenes**
10. **Modular arithmetic** (mod m, modular inverse)
11. **Fermat's little theorem**, **Euler's theorem**
12. **CRT (Chinese Remainder Theorem)**
13. **Mobius function, Euler's totient**

### Combinatorics
14. **Binomial coefficients, Pascal's triangle**
15. **Catalan numbers**
16. **Stirling numbers**
17. **Bell numbers**
18. **Stars and bars**

### Algebra
19. **Polynomials** (multiplication, division)
20. **Matrices** (multiplication, exponentiation, inverse)
21. **Linear systems** (Gaussian elimination)
22. **Determinants** (basic)

### Probability
23. **Discrete probability, expected value**
24. **Linearity of expectation** (powerful!)
25. **Conditional probability, Bayes**
26. **Random variables, variance**

### Calculus (light)
27. **Derivatives** (for optimization, e.g., ternary search)
28. **Limits** (for asymptotic analysis)
29. **Integration** (for geometry / probability / generating functions)

### Geometry
30. **Trigonometry** (sin, cos, tan, identities)

---

## II. THE CRUCIAL FORMULAS

Memorize these. Tattoo them on your soul.

### Sums
- 1 + 2 + ... + n = n(n+1)/2
- 1² + 2² + ... + n² = n(n+1)(2n+1)/6
- 1³ + 2³ + ... + n³ = (n(n+1)/2)²
- 1 + 2 + 4 + ... + 2ⁿ = 2^(n+1) - 1
- a + ar + ar² + ... + ar^(n-1) = a(rⁿ-1)/(r-1) (geometric)

### Combinatorics
- n! = 1·2·...·n; 0! = 1
- nCr = n!/(r!(n-r)!) = nC(n-r)
- Pascal: nCr = (n-1)Cr + (n-1)C(r-1)
- Catalan: C_n = (1/(n+1)) · 2nCn = 2nCn − 2nC(n+1)
- Number of binary trees with n nodes: C_n
- Number of valid parens with n pairs: C_n

### Logarithm identities
- log(ab) = log a + log b
- log(a^n) = n log a
- log_b(x) = log_a(x) / log_a(b)

### Modular
- (a + b) mod m = ((a mod m) + (b mod m)) mod m
- (a · b) mod m = ((a mod m) · (b mod m)) mod m
- a^(-1) mod p = a^(p-2) mod p (when p prime, by Fermat)

### Probability
- P(A ∩ B) = P(A) · P(B|A)
- E[X + Y] = E[X] + E[Y] (always, even if not independent — **linearity of expectation!**)
- E[X · Y] = E[X] · E[Y] only if independent

---

## III. THE PIGEONHOLE PRINCIPLE

**Statement**: if n+1 pigeons go into n holes, at least one hole has ≥ 2 pigeons.

**Use**: prove that *some* configuration must occur.

> Example: among any 5 numbers, two have the same parity. (2 holes: even/odd; 5 pigeons.)

> Example: in a sequence of n integers, some contiguous subsequence has sum divisible by n. (Prefix sums mod n; n+1 prefix sums in n+1 boxes... and 2 must be equal → their difference is divisible by n.)

---

## IV. INCLUSION-EXCLUSION

|A ∪ B| = |A| + |B| − |A ∩ B|

|A ∪ B ∪ C| = |A| + |B| + |C| − |A ∩ B| − |A ∩ C| − |B ∩ C| + |A ∩ B ∩ C|

General: |⋃ A_i| = Σ|A_i| − Σ|A_i ∩ A_j| + Σ|A_i ∩ A_j ∩ A_k| − ...

**Use**: count things that satisfy at least one of several properties (e.g., divisible by 2 or 3 or 5).

---

## V. LINEARITY OF EXPECTATION (the secret weapon)

**Statement**: E[X + Y] = E[X] + E[Y] for ANY random variables X, Y. No independence needed.

This breaks "complex" expectation into simple ones.

> Example: expected number of comparisons in random quicksort. Define X_ij = 1 if elements i, j are compared, 0 otherwise. E[total] = Σ E[X_ij]. Compute each P(i, j compared) = 2/(j-i+1). Sum: O(n log n).

---

## VI. PROOF TECHNIQUES

### Direct proof
Assume hypothesis. Apply rules. Conclude.

### Proof by contradiction
Assume the negation. Derive a contradiction. Therefore the original holds.

> Example: √2 is irrational. Assume rational p/q in lowest terms. Then 2q² = p², so p² is even, so p is even, so p = 2k, so 2q² = 4k², so q² = 2k², so q is even — contradicts "lowest terms."

### Proof by induction
Base case + inductive step.

> Example: prove 1 + 2 + ... + n = n(n+1)/2.
> Base: n=1: 1 = 1·2/2. ✓
> Step: Assume true for n. Then 1+...+n+(n+1) = n(n+1)/2 + (n+1) = (n+1)(n+2)/2. ✓

### Proof by contrapositive
"P → Q" ≡ "¬Q → ¬P". Often easier.

### Constructive vs non-constructive
Constructive: build the object. Non-constructive: show it must exist (often via pigeonhole or counting).

---

## VII. THE INDUCTION-RECURSION CORRESPONDENCE

Recursive function ↔ inductive proof.

When you write `f(n) = ... + f(n-1)`, you're doing induction. The base case = base case. The recursive call = inductive hypothesis. The combination = inductive step.

Mastering induction → mastering recursion → mastering DP → mastering algorithms.

---

## VIII. EXERCISES

For each, *prove* the claim:

1. The sum of the first n odd numbers is n².
2. There are 2ⁿ subsets of an n-element set.
3. n! grows faster than 2ⁿ for n ≥ 4.
4. In any group of 100 people, two have birthdays in the same month.
5. The number of paths in a grid from (0,0) to (m,n) using only right/up moves is C(m+n, m).
6. The Fibonacci sequence has F(n) ≤ 2ⁿ.
7. Any tree with n nodes has n-1 edges.
8. A graph with n nodes and ≥ n edges contains a cycle.

---

## IX. RECOMMENDED READING

- **Concrete Mathematics** (Knuth, Patashnik, Graham) ⭐ — the bible
- **Discrete Mathematics and Its Applications** (Rosen)
- **A Walk Through Combinatorics** (Bóna)
- **An Introduction to Probability Theory and Its Applications** (Feller)

---

**→ Next:** [`08-Logic-and-Discrete-Math.md`](./08-Logic-and-Discrete-Math.md)
