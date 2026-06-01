# Reverse Integer

**Platform**: LeetCode 7 · **Difficulty**: Medium · **Topics**: Math · **Pattern**: Digit pop/push with overflow guard

---

## 📜 Problem Statement

Given a signed 32-bit integer `x`, return `x` *with its digits reversed*. If reversing `x` causes the value to go outside the signed 32-bit integer range `[-2^31, 2^31 - 1]`, then return `0`.

**Assume the environment does not allow you to store 64-bit integers (signed or unsigned).**

### Examples

**Example 1:**
```
Input:  x = 123
Output: 321
```

**Example 2:**
```
Input:  x = -123
Output: -321
```

**Example 3:**
```
Input:  x = 120
Output: 21
Explanation: Reversing 120 gives 021, and leading zeros are dropped → 21.
```

### Constraints
```
-2^31 <= x <= 2^31 - 1
```

---

## 🧠 Understanding the problem

Reversing digits is mechanical: peel the last digit with `x % 10`, append it to a running result via `result = result * 10 + digit`, and drop it from `x` with `x /= 10`. The sign takes care of itself in languages where `%` keeps the sign of the dividend (C++/Java); in Python we handle the sign separately because `%` there follows the divisor's sign.

The real challenge is the constraint: **no 64-bit storage allowed**, yet the reversed value might exceed the 32-bit range (e.g. reversing `1534236469` overflows). So we must detect overflow **before** it happens by checking, at each step, whether `result * 10 + digit` would breach `INT_MAX` / `INT_MIN`. The bounds:

- `INT_MAX = 2147483647` (last digit 7).
- `INT_MIN = -2147483648` (last digit 8).

Before doing `result = result * 10 + digit`, if `result > INT_MAX/10`, or `result == INT_MAX/10` and `digit > 7`, it would overflow positively → return 0. Symmetrically for the negative bound with digit `< -8`.

---

## Approach 1 — Pop/push digits with pre-overflow check (optimal) ⭐

### Intuition
Build the reversed number digit by digit, but guard each multiply-add against the 32-bit limits so we never actually overflow.

### Algorithm
1. `result = 0`.
2. While `x != 0`:
   - `digit = x % 10`; `x /= 10`.
   - If `result > INT_MAX/10 || (result == INT_MAX/10 && digit > 7)` → return 0.
   - If `result < INT_MIN/10 || (result == INT_MIN/10 && digit < -8)` → return 0.
   - `result = result * 10 + digit`.
3. Return `result`.

### Dry run on `x = -123`
```
result=0
digit=-3, x=-12; result=0*10-3=-3
digit=-2, x=-1;  result=-3*10-2=-32
digit=-1, x=0;   result=-32*10-1=-321
answer = -321  ✓
```
Overflow example `x = 1534236469`:
```
...builds up to result=534236469, next would be 5342364695 > INT_MAX
the guard fires (result > 214748364) → return 0
```

### Code
```cpp
int reverse(int x) {
    int result = 0;
    while (x != 0) {
        int digit = x % 10;
        x /= 10;
        if (result > INT_MAX / 10 || (result == INT_MAX / 10 && digit > 7)) return 0;
        if (result < INT_MIN / 10 || (result == INT_MIN / 10 && digit < -8)) return 0;
        result = result * 10 + digit;
    }
    return result;
}
```
```java
public int reverse(int x) {
    int result = 0;
    while (x != 0) {
        int digit = x % 10;
        x /= 10;
        if (result > Integer.MAX_VALUE / 10 ||
            (result == Integer.MAX_VALUE / 10 && digit > 7)) return 0;
        if (result < Integer.MIN_VALUE / 10 ||
            (result == Integer.MIN_VALUE / 10 && digit < -8)) return 0;
        result = result * 10 + digit;
    }
    return result;
}
```
```python
def reverse(x):
    INT_MAX, INT_MIN = 2**31 - 1, -2**31
    result = 0
    sign = 1 if x >= 0 else -1
    x = abs(x)
    while x != 0:
        digit = x % 10
        x //= 10
        # check against the positive bound, apply sign at the end
        if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > 7):
            return 0
        result = result * 10 + digit
    result *= sign
    return result if INT_MIN <= result <= INT_MAX else 0
```

### Complexity
- **Time**: O(log₁₀ x) — one iteration per digit.
- **Space**: O(1).

### Verdict
**The optimal answer** that honors the "no 64-bit" rule. The pre-multiply overflow guard is the crux; memorize the `INT_MAX/10` comparison with the trailing-digit check (`> 7` / `< -8`).

---

## Approach 2 — 64-bit accumulator then range check (if 64-bit were allowed)

### Intuition
If the environment *did* allow `long`, reverse into a 64-bit accumulator and check the range once at the end. Simpler, but it technically violates the problem's "no 64-bit storage" rule — included for contrast and because it's what you'd write when the constraint is absent.

### Algorithm
1. Reverse into a `long` result.
2. If it falls outside `[INT_MIN, INT_MAX]` → return 0; else cast to `int`.

### Dry run on `x = 1534236469`
```
reversed long = 9646324351 > 2147483647 → out of range → return 0
```

### Code
```cpp
int reverse(int x) {
    long long result = 0;
    while (x != 0) {
        result = result * 10 + x % 10;
        x /= 10;
    }
    if (result > INT_MAX || result < INT_MIN) return 0;
    return (int)result;
}
```
```java
public int reverse(int x) {
    long result = 0;
    while (x != 0) {
        result = result * 10 + x % 10;
        x /= 10;
    }
    if (result > Integer.MAX_VALUE || result < Integer.MIN_VALUE) return 0;
    return (int) result;
}
```
```python
def reverse(x):
    sign = -1 if x < 0 else 1
    rev = int(str(abs(x))[::-1]) * sign     # Python ints are unbounded
    return rev if -2**31 <= rev <= 2**31 - 1 else 0
```

### Complexity
- **Time**: O(log₁₀ x).
- **Space**: O(1).

### Verdict
Cleaner to write, and the natural solution in Python (where ints can't overflow). In C++/Java it sidesteps the stated constraint by using `long`, so prefer Approach 1 when the interviewer enforces "no 64-bit."

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Pre-overflow guard | O(log x) | O(1) | honors "no 64-bit" ⭐ |
| 64-bit + range check | O(log x) | O(1) | simplest; uses `long` (or Python big int) |

---

## 🧪 Edge cases & pitfalls
- **Overflow on reverse** (`1534236469`, `-2147483648`) → return 0. The whole point of the problem.
- **Trailing zeros** (`120 → 21`, `100 → 1`) → leading zeros vanish naturally since `result * 10 + 0` doesn't add a digit.
- **Negative numbers** → in C++/Java, `%` keeps the sign so it just works; in Python, strip the sign first and reapply.
- **`x = 0`** → loop doesn't run, returns 0.
- **`INT_MIN` itself** → its absolute value overflows 32-bit; the guard version handles it digit-by-digit, and Python's big-int avoids the issue.
- **Pitfall — checking overflow *after* the multiply**: too late, it already wrapped. Always check *before* `result = result*10 + digit`.

---

## 🔗 Related problems
- **Palindrome Number** (LC 9) — reverse half the digits to test palindromicity.
- **String to Integer (atoi)** (LC 8) — parsing with the same overflow clamps.
- **Reverse Bits** (LC 190) — the binary analog (earlier).
- **Plus One** (LC 66) — digit-array arithmetic.

---

## 🎉 Vault complete

This is the last problem of the Bit Manipulation set and the final editorial in the expanded vault. If you can solve every problem across topics 01–18 **cold, in time, with edge cases handled**, you're at the FAANG DSA bar. Re-derive the ⭐ solutions from their key insight weekly until they're automatic.

---

**→ Prev:** [`06-Sum-of-Two-Integers.md`](./06-Sum-of-Two-Integers.md) | [Problem set index](./00-Index.md) | Back to [vault index](../00-Index.md)
