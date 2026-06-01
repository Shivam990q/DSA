# 🔢 Modular Arithmetic

> *"When numbers get huge, we work in the world of remainders."*

---

## I. WHY MODULO
Counting problems produce astronomically large answers. We report them mod a prime (usually **10⁹+7** or **998244353**) to keep them bounded while preserving correctness of additions/multiplications.

---

## II. THE RULES
- (a + b) mod m = ((a mod m) + (b mod m)) mod m
- (a − b) mod m = ((a mod m) − (b mod m) + m) mod m  ← add m to avoid negatives
- (a · b) mod m = ((a mod m) · (b mod m)) mod m
- (a / b) mod m = a · b⁻¹ mod m  ← division needs modular inverse, NOT integer division

```cpp
long long addmod(long long a, long long b, long long m){ return (a%m + b%m) % m; }
long long submod(long long a, long long b, long long m){ return ((a-b)%m + m) % m; }
long long mulmod(long long a, long long b, long long m){ return (a%m)*(b%m) % m; }
```

---

## III. OVERFLOW AWARENESS
- For m ≈ 10⁹, products fit in `long long` (a·b ≤ 10¹⁸ < 9.2·10¹⁸). ✓
- For m ≈ 10¹⁸, use `__int128` for the multiplication: `(__int128)a*b % m`.

---

## IV. MODULAR EXPONENTIATION
a^b mod m in O(log b) (binary exponentiation):
```cpp
long long modpow(long long a, long long b, long long m) {
    long long r = 1 % m; a %= m;
    while (b) { if (b&1) r = r*a % m; a = a*a % m; b >>= 1; }
    return r;
}
```

---

## V. MODULAR INVERSE
b⁻¹ is the number with b·b⁻¹ ≡ 1 (mod m).
- **m prime** (Fermat): b⁻¹ = b^(m−2) mod m
- **gcd(b,m)=1, general**: extended Euclidean
- **All inverses 1..n mod p** in O(n): inv[i] = −(p/i)·inv[p%i] mod p

---

## VI. CHINESE REMAINDER THEOREM (CRT)
Given x ≡ a₁ (mod m₁), x ≡ a₂ (mod m₂), ... with pairwise-coprime mᵢ, there is a unique x mod M=∏mᵢ.
- Used to: combine results computed under several small primes (e.g., arbitrary-modulus FFT), solve simultaneous congruences.

---

## VII. COMMON PITFALLS ⭐
1. **Forgetting to mod** after each operation → overflow → wrong answer
2. **Negative results** after subtraction → always `(x % m + m) % m`
3. **Integer division** instead of modular inverse → wrong (a/b ≠ a·b⁻¹ with `/`)
4. **Modding the wrong prime** (read the problem: 10⁹+7 vs 998244353)
5. **Overflow in multiplication** when m is large → use __int128

---

## VIII. MODULAR nCr
Precompute factorials + inverse factorials mod p; C(n,r) = fact[n]·invfact[r]·invfact[n−r] mod p. (See [`02-Combinatorics.md`](./02-Combinatorics.md).)

---

## IX. PROBLEMS
- Any "answer mod 10⁹+7" counting problem
- Pow(x, n) (LC 50) — concept of fast exp
- Super Pow (LC 372) — modular exp with huge exponent
- [CSES](https://cses.fi/problemset/) "Exponentiation", "Exponentiation II", "Binomial Coefficients"

---

## X. TEMPLATE
See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/number-theory.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/number-theory.cpp).

---

**→ Next:** [`07-Mobius-Function.md`](./07-Mobius-Function.md)
