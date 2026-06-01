# Pow(x, n)

**Platform**: LeetCode 50 · **Difficulty**: Medium · **Topics**: Math, Recursion · **Pattern**: Fast (binary) exponentiation

---

## 📜 Problem Statement

Implement `pow(x, n)`, which calculates `x` raised to the power `n` (i.e., `x^n`).

### Examples

**Example 1:**
```
Input:  x = 2.00000, n = 10
Output: 1024.00000
```

**Example 2:**
```
Input:  x = 2.10000, n = 3
Output: 9.26100
```

**Example 3:**
```
Input:  x = 2.00000, n = -2
Output: 0.25000
Explanation: 2^-2 = 1/2^2 = 1/4 = 0.25
```

### Constraints
```
-100.0 < x < 100.0
-2^31 <= n <= 2^31 - 1
n is an integer.
Either x is not zero or n > 0.
-10^4 <= x^n <= 10^4
```

---

## 🧠 Understanding the problem

The naive `x * x * ... * x` (n times) is O(n), and with `n` up to ~2×10^9 that's far too slow. The key identity is **exponentiation by squaring**:

- `x^n = (x^2)^{n/2}` when `n` is even.
- `x^n = x · (x^2)^{(n-1)/2}` when `n` is odd.

Each step squares the base and halves the exponent, so we reach `n = 0` in O(log n) steps. Reading `n` in binary, we multiply the running base into the result exactly at the positions where `n` has a set bit.

Negative exponents: `x^{-n} = 1 / x^n`. Handle the sign by inverting `x` and negating `n`. The one trap: `n = INT_MIN` can't be negated in 32-bit, so widen to a 64-bit `long` *before* negating.

---

## Approach 1 — Naive linear multiplication

### Intuition
Multiply `x` by itself `|n|` times; invert at the end if `n` was negative.

### Algorithm
1. If `n < 0`: `x = 1/x`, work with `|n|`.
2. Multiply `result *= x`, `|n|` times.

### Dry run on `x=2, n=10`
```
multiply 2 ten times → 1024
```

### Code
```cpp
double myPow(double x, int n) {
    long long e = n;
    if (e < 0) { x = 1 / x; e = -e; }
    double result = 1.0;
    for (long long i = 0; i < e; i++) result *= x;
    return result;
}
```
```java
public double myPow(double x, int n) {
    long e = n;
    if (e < 0) { x = 1 / x; e = -e; }
    double result = 1.0;
    for (long i = 0; i < e; i++) result *= x;
    return result;
}
```
```python
def myPow(x, n):
    e = n
    if e < 0:
        x, e = 1 / x, -e
    result = 1.0
    for _ in range(e):
        result *= x
    return result
```

### Complexity
- **Time**: O(n) — up to ~2×10^9 iterations. **TLE.**
- **Space**: O(1).

### Verdict
Correct but far too slow for the constraint range. It motivates squaring.

---

## Approach 2 — Fast exponentiation, iterative (optimal) ⭐

### Intuition
Square the base and halve the exponent. Whenever the current lowest bit of `n` is set, fold the current base into the result.

### Algorithm
1. Widen `n` to `long e`; if `e < 0`, set `x = 1/x`, `e = -e`.
2. `result = 1`. While `e > 0`:
   - If `e & 1` → `result *= x`.
   - `x *= x`; `e >>= 1`.
3. Return `result`.

### Dry run on `x=2, n=10`
```
e=10 (1010b)
e&1=0; x=4;  e=5
e&1=1; result=4; x=16; e=2
e&1=0; x=256; e=1
e&1=1; result=4*256=1024; x=...; e=0
return 1024  ✓
```

### Code
```cpp
double myPow(double x, int n) {
    long long e = n;
    if (e < 0) { x = 1 / x; e = -e; }
    double result = 1.0;
    while (e > 0) {
        if (e & 1) result *= x;
        x *= x;
        e >>= 1;
    }
    return result;
}
```
```java
public double myPow(double x, int n) {
    long e = n;
    if (e < 0) { x = 1 / x; e = -e; }
    double result = 1.0;
    while (e > 0) {
        if ((e & 1) == 1) result *= x;
        x *= x;
        e >>= 1;
    }
    return result;
}
```
```python
def myPow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result
```

### Complexity
- **Time**: O(log n) — exponent halves each step.
- **Space**: O(1).

### Verdict
**The optimal answer.** Iterative squaring avoids recursion overhead and the INT_MIN trap (via the `long` widening). This is what to present.

---

## Approach 3 — Fast exponentiation, recursive

### Intuition
Same identity, expressed recursively: `pow(x, n) = pow(x*x, n/2)` for even `n`, times an extra `x` for odd `n`.

### Algorithm
1. Base: `pow(x, 0) = 1`.
2. `half = pow(x, n/2)`; if `n` even → `half*half`, else → `half*half*x`.
3. Handle negativity at the top by inverting.

### Dry run on `x=2, n=10`
```
pow(2,10)=pow(4,5)
pow(4,5)=4*pow(16,2)
pow(16,2)=pow(256,1)
pow(256,1)=256*pow(...,0)=256
→ 256, *? back up: pow(16,2)=256, pow(4,5)=4*256=1024, pow(2,10)=1024  ✓
```

### Code
```cpp
class Solution {
    double fastPow(double x, long long e) {
        if (e == 0) return 1.0;
        double half = fastPow(x, e / 2);
        return (e % 2 == 0) ? half * half : half * half * x;
    }
public:
    double myPow(double x, int n) {
        long long e = n;
        if (e < 0) { x = 1 / x; e = -e; }
        return fastPow(x, e);
    }
};
```
```java
class Solution {
    public double myPow(double x, int n) {
        long e = n;
        if (e < 0) { x = 1 / x; e = -e; }
        return fastPow(x, e);
    }
    private double fastPow(double x, long e) {
        if (e == 0) return 1.0;
        double half = fastPow(x, e / 2);
        return (e % 2 == 0) ? half * half : half * half * x;
    }
}
```
```python
def myPow(x, n):
    def fast(b, e):
        if e == 0:
            return 1.0
        half = fast(b, e // 2)
        return half * half if e % 2 == 0 else half * half * b
    if n < 0:
        x, n = 1 / x, -n
    return fast(x, n)
```

### Complexity
- **Time**: O(log n).
- **Space**: O(log n) recursion stack.

### Verdict
Equally fast in time, but uses O(log n) stack. The iterative version is preferred; the recursive one reads more naturally to some.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Naive loop | O(n) | O(1) | TLE for large n |
| Fast pow (iterative) | **O(log n)** | **O(1)** | optimal ⭐ |
| Fast pow (recursive) | O(log n) | O(log n) | clean but uses stack |

---

## 🧪 Edge cases & pitfalls
- **`n = 0`** → `1` for any `x` (including `x` near 0 per constraints).
- **`n = INT_MIN`** → `-n` overflows 32-bit. **Always widen to `long`/`long long` before negating.** This is the single most common bug.
- **Negative `x` with odd `n`** → result is negative; squaring handles the sign correctly.
- **`x` very close to 0 with large positive `n`** → underflows toward 0; that's the expected mathematical result.
- **Pitfall — floating error**: repeated squaring accumulates tiny error, but it's within the judge's tolerance; don't try to "round."

---

## 🔗 Related problems
- **Sqrt(x)** (LC 69) — binary search / Newton's method.
- **Super Pow** (LC 372) — modular fast exponentiation with array exponents.
- **Count Good Numbers** (LC 1922) — modular power at scale.
- **Multiply Strings** (LC 43) — big-number arithmetic (next).

---

**→ Next:** [`05-Multiply-Strings.md`](./05-Multiply-Strings.md) | **Prev:** [`03-Set-Matrix-Zeroes.md`](./03-Set-Matrix-Zeroes.md) | [Problem set index](./00-Index.md)
