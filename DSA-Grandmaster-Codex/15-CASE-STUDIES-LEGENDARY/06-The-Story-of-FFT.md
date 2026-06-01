# 📖 Case Study: The Story of FFT

> *"Cooley and Tukey discovered an algorithm that hadn't been hidden — it had been overlooked."*

---

## I. THE PROBLEM

Multiply two polynomials of degree n in O(n log n) instead of O(n²).

Equivalently: compute convolutions in O(n log n).

---

## II. WHY POLYNOMIAL MULTIPLICATION MATTERS

Many things ARE polynomial multiplication:
- **Big integer multiplication** (each digit = polynomial coefficient)
- **Convolution** (signal processing)
- **String matching with wildcards**
- **Counting subset sums** (XOR/AND/OR convolutions are FFT cousins)

---

## III. THE BRUTE FORCE — O(n²)

```
(a[0] + a[1]x + ... + a[n-1]x^(n-1)) × (b[0] + b[1]x + ... + b[n-1]x^(n-1))
```

Each pair (i, j) contributes to coefficient (i+j). n² pairs.

For n = 10⁶, that's 10¹² ops → way too slow.

---

## IV. THE OBSERVATION (Cooley-Tukey 1965)

A polynomial of degree n is fully determined by its values at n+1 distinct points.

If we evaluate A(x) and B(x) at the same n points, then:
> A·B at those points = A(point_i) × B(point_i)

That's pointwise multiplication: O(n).

The work is now in **evaluation** and **interpolation**. Naive evaluation at n points is O(n²) per polynomial — back to where we started!

**The trick**: choose **special** points where evaluation is fast — namely, **complex roots of unity**.

---

## V. ROOTS OF UNITY

For n a power of 2, the n-th roots of unity are:
> ω = e^(2πi/n), and ω^k for k = 0, 1, ..., n-1.

These have a magical property: **the n-th roots of unity have recursive structure**.

The set {ω^0, ω^2, ω^4, ..., ω^(n-2)} is the set of (n/2)-th roots of unity.

This recursive structure enables divide-and-conquer.

---

## VI. THE FFT ALGORITHM (Recursive)

Given polynomial A of degree n (n a power of 2):

1. Split A into:
   - A_even(y) = a[0] + a[2]y + a[4]y² + ... (using even-indexed coefficients)
   - A_odd(y)  = a[1] + a[3]y + a[5]y² + ... (using odd-indexed coefficients)

2. Note: A(x) = A_even(x²) + x · A_odd(x²)

3. Recursively evaluate A_even and A_odd at (n/2)-th roots of unity.

4. Combine: for k in 0..n/2-1:
   - A(ω^k)       = A_even(ω^(2k)) + ω^k · A_odd(ω^(2k))
   - A(ω^(k+n/2)) = A_even(ω^(2k)) − ω^k · A_odd(ω^(2k))

(The combination uses the symmetry ω^(k+n/2) = -ω^k.)

Recurrence: T(n) = 2T(n/2) + O(n) → **O(n log n)** by Master Theorem.

---

## VII. INVERSE FFT (interpolation)

To go back from values to coefficients: run FFT with ω replaced by ω^(-1), then divide by n.

```
A(x) at n points → IFFT → coefficients
```

---

## VIII. THE FULL POLYNOMIAL MULTIPLICATION

```
1. Pad A and B to length 2n (next power of 2)
2. Compute FFT of A and B (at 2n-th roots of unity)
3. Pointwise multiply
4. Inverse FFT to recover the coefficients of C = A × B
```

Total: O(n log n).

---

## IX. NTT (Number Theoretic Transform)

Floating-point FFT has precision issues. **NTT** is FFT done in modular arithmetic over a prime.

Use a prime p with a primitive 2^k-th root of unity. Common choices:
- p = 998244353 = 119 × 2²³ + 1, ω = 3 (primitive root)
- p = 754974721

Same algorithm, exact integer arithmetic. No precision issues.

---

## X. CODE (FFT skeleton)

```cpp
typedef complex<double> cd;
const double PI = acos(-1);

void fft(vector<cd>& a, bool invert) {
    int n = a.size();
    if (n == 1) return;
    
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    
    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; j++) {
                cd u = a[i+j], v = a[i+j+len/2] * w;
                a[i+j] = u + v;
                a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }
    
    if (invert) for (cd& x : a) x /= n;
}
```

---

## XI. APPLICATIONS

1. **Polynomial multiplication** (the obvious)
2. **Big integer multiplication** (Karatsuba O(n^1.585) → FFT O(n log n))
3. **String matching with wildcards** (via convolution)
4. **Convolutions in signal processing** (audio, image)
5. **Counting problems** in CP (subset sum convolutions)
6. **Cross-correlation** in computer vision
7. **Solving recurrences** via generating functions

---

## XII. MENTAL MODEL

> **"Choose your representation wisely.  
>  Polynomials in coefficient form: hard to multiply.  
>  Polynomials in value form: easy to multiply.  
>  FFT is the bridge."**

This — **switching representations** — is a powerful algorithmic principle.

---

## XIII. THE FORGOTTEN INVENTOR

Cooley & Tukey published in 1965 — but Carl Friedrich Gauss had used the algorithm in 1805 to compute orbits of asteroids! He never published. The algorithm waited 160 years for a modern computer to need it.

---

## XIV. PROBLEMS

1. Multiply two big integers (LC 43 — naive; FFT version)
2. Number of subarrays with given XOR (FFT for XOR convolution)
3. Counting paths in a graph (matrix exp + FFT for some variants)
4. Polynomial inverse (Newton's method on FFT)
5. [CSES](https://cses.fi/problemset/) "Polynomial multiplication"
6. CF problems tagged "fft"

---

## XV. FURTHER READING

- **Cooley-Tukey 1965** — original paper
- **CLRS Chapter 30** — clean exposition
- **[CP-Algorithms](https://cp-algorithms.com) FFT page**
- **Numerical Recipes** — practical FFT details

---

**→ Next case study:** [`07-The-Story-of-KMP.md`](./07-The-Story-of-KMP.md)
