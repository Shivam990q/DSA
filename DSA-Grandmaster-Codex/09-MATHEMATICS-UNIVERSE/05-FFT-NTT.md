# 🔢 FFT & NTT — Fast Polynomial Multiplication

> *"Multiply two degree-n polynomials in O(n log n) instead of O(n²)."*

For the full derivation and history, see [`../15-CASE-STUDIES-LEGENDARY/06-The-Story-of-FFT.md`](../15-CASE-STUDIES-LEGENDARY/06-The-Story-of-FFT.md).

---

## I. THE PROBLEM
Multiply polynomials A(x)·B(x), or equivalently compute the **convolution** of two sequences. Naive: O(n²). FFT: O(n log n).

---

## II. THE IDEA
1. A degree-n polynomial is determined by its values at n+1 points.
2. At the same points, (A·B)(point) = A(point)·B(point) — pointwise, O(n).
3. Use **roots of unity** as the points → evaluation (DFT) and interpolation (inverse DFT) each take O(n log n) via divide-and-conquer.

```
coefficients --FFT--> point values --pointwise multiply--> point values --inverse FFT--> coefficients
```

---

## III. FFT (over complex numbers)
```cpp
typedef complex<double> cd;
void fft(vector<cd>& a, bool inv) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * acos(-1.0) / len * (inv ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len/2; j++) {
                cd u = a[i+j], v = a[i+j+len/2]*w;
                a[i+j] = u + v; a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }
    if (inv) for (cd& x : a) x /= n;
}
```
Multiply: pad to power of 2 ≥ deg sum, FFT both, multiply pointwise, inverse FFT, round.

---

## IV. NTT (Number Theoretic Transform)
FFT has floating-point error. **NTT** does the same in modular arithmetic over a prime with a primitive root:
- p = 998244353 = 119·2²³ + 1, primitive root g = 3
- Replace roots of unity e^(2πi/n) with g^((p−1)/n) mod p
- **Exact integer** results, no precision issues — preferred when working mod a prime

For arbitrary modulus: use 3 NTT-friendly primes + CRT, or large-modulus tricks.

---

## V. APPLICATIONS
1. **Polynomial / big-integer multiplication**
2. **Convolutions**: c[k] = Σ a[i]·b[k−i]
3. **Counting**: number of pairs (i,j) with a[i]+b[j] = target (frequency convolution)
4. **String matching with wildcards** (via convolution)
5. **Subset-sum counting** (with generating functions)
6. **Polynomial operations**: inverse, log, exp, sqrt (Newton's method on FFT)
7. **FWHT** (Fast Walsh-Hadamard) for XOR/AND/OR convolutions

---

## VI. RELATED TRANSFORMS
- **FWHT**: XOR-convolution in O(n log n) — for subset/bitwise problems
- **Subset sum convolution / SOS DP**: see DP universe §16

---

## VII. PROBLEMS
- Multiply big numbers
- Counting sums/pairs via convolution
- [CSES](https://cses.fi/problemset/) "Polynomial Multiplication" (if available), CF problems tagged "fft"
- [SPOJ](https://www.spoj.com): POLYMUL, MAXMATCH (string matching via FFT)

---

## VIII. NOTE
FFT/NTT is a Level 7 (elite CP) topic. The concept (switch representations) is profound; the implementation is fiddly. Use a tested template.

---

**→ Next:** [`06-Modular-Arithmetic.md`](./06-Modular-Arithmetic.md)
