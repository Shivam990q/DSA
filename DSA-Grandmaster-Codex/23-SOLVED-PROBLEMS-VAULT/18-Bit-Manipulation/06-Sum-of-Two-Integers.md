# Sum of Two Integers

**Platform**: LeetCode 371 · **Difficulty**: Medium · **Topics**: Math, Bit Manipulation · **Pattern**: XOR sum + AND carry

---

## 📜 Problem Statement

Given two integers `a` and `b`, return *the sum of the two integers without using the operators* `+` *and* `-`.

### Examples

**Example 1:**
```
Input:  a = 1, b = 2
Output: 3
```

**Example 2:**
```
Input:  a = 2, b = 3
Output: 5
```

**Example 3:**
```
Input:  a = -1, b = 1
Output: 0
```

### Constraints
```
-1000 <= a, b <= 1000
```

---

## 🧠 Understanding the problem

Addition forbidden `+`/`-`, so we rebuild it from bitwise operations. Split a binary add into two pieces:

- **Sum without carry** = `a ^ b`. XOR adds each bit position ignoring any carry (`1+1` gives `0` here, not `10`).
- **Carry** = `(a & b) << 1`. A carry is generated wherever **both** bits are 1, and it belongs to the *next* higher position, hence the left shift.

The real sum is "sum-without-carry plus carry", but we can't use `+`. So we **repeat**: set `a = a ^ b` (partial sum) and `b = (a & b) << 1` (carry to add), looping until the carry is 0. When there's no carry left, `a` holds the answer. This always terminates because carries shift left and eventually fall off the 32-bit width.

**Python caveat**: Python ints are arbitrary precision, so the carry never "falls off." We mask to 32 bits with `0xFFFFFFFF` each iteration and, at the end, reinterpret values `> 0x7FFFFFFF` as negative two's-complement numbers.

---

## Approach 1 — Iterative XOR + carry (optimal) ⭐

### Intuition
Loop: compute carry, fold the no-carry sum, repeat until carry is gone.

### Algorithm
1. While `b != 0`:
   - `carry = (a & b) << 1`.
   - `a = a ^ b`.
   - `b = carry`.
2. Return `a`.

### Dry run on `a = 2 (010), b = 3 (011)`
```
iter1: carry=(010 & 011)<<1=(010)<<1=100=4; a=010^011=001=1; b=4
iter2: carry=(001 & 100)<<1=0; a=001^100=101=5; b=0
b==0 → answer = 5  ✓
```

### Code
```cpp
int getSum(int a, int b) {
    while (b != 0) {
        unsigned carry = (unsigned)(a & b) << 1;   // avoid signed-shift UB
        a = a ^ b;
        b = (int)carry;
    }
    return a;
}
```
```java
public int getSum(int a, int b) {
    while (b != 0) {
        int carry = (a & b) << 1;
        a = a ^ b;
        b = carry;
    }
    return a;
}
```
```python
def getSum(a, b):
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1
        a = a ^ b
        b = carry
    a &= mask
    # reinterpret as signed 32-bit
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
```

### Complexity
- **Time**: O(1) — at most ~32 iterations (one per bit position).
- **Space**: O(1).

### Verdict
**The optimal answer.** The XOR-sum / AND-carry decomposition is the canonical full-adder built in software. The language notes (unsigned shift in C++, masking in Python) are the only subtleties.

---

## Approach 2 — Recursive form

### Intuition
The exact same recurrence, expressed recursively: `getSum(a, b) = getSum(a ^ b, (a & b) << 1)`, bottoming out when `b == 0`.

### Algorithm
1. If `b == 0` → return `a`.
2. Return `getSum(a ^ b, (a & b) << 1)`.

### Dry run on `a = 1, b = 2`
```
getSum(1,2): a^b=3, carry=(1&2)<<1=0 → getSum(3,0) → 3  ✓
```

### Code
```cpp
int getSum(int a, int b) {
    if (b == 0) return a;
    unsigned carry = (unsigned)(a & b) << 1;
    return getSum(a ^ b, (int)carry);
}
```
```java
public int getSum(int a, int b) {
    if (b == 0) return a;
    return getSum(a ^ b, (a & b) << 1);
}
```
```python
def getSum(a, b):
    mask = 0xFFFFFFFF
    if b & mask == 0:
        a &= mask
        return a if a <= 0x7FFFFFFF else ~(a ^ mask)
    return getSum((a ^ b) & mask, ((a & b) << 1) & mask)
```

### Complexity
- **Time**: O(1) — ≤ 32 recursive calls.
- **Space**: O(1) call-stack depth (≤ 32 frames).

### Verdict
Equivalent; some find the recursion clearer. The iterative version avoids stack frames and is the usual pick.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Iterative XOR+carry | O(1) | O(1) | canonical, recommended ⭐ |
| Recursive XOR+carry | O(1) | O(1) (≤32 frames) | same logic, recursive |

There is no meaningful "brute force" without `+`/`-`; the bit decomposition *is* the technique.

---

## 🧪 Edge cases & pitfalls
- **Negative numbers** → two's complement makes XOR/AND/shift "just work" in C++/Java; the loop terminates when the carry shifts past bit 31.
- **`a = -1, b = 1`** → `0` (carry propagates all the way and cancels).
- **Zero operands** → `getSum(x, 0) = x` immediately.
- **C++ pitfall — signed left shift overflow** is undefined behavior; cast the `(a & b)` to `unsigned` before `<< 1`.
- **Python pitfall** — without masking, the carry grows forever (no overflow), so the loop never ends. Mask each step with `0xFFFFFFFF` and reinterpret the sign at the end.
- **Java**: no unsigned type, but `<<` on `int` wraps mod 2^32 as needed, so no extra masking is required.

---

## 🔗 Related problems
- **Add Binary** (LC 67) — string-based binary addition (uses the same carry logic).
- **Add Two Numbers** (LC 2) — carry over a linked list.
- **Reverse Bits** (LC 190) — bit-level manipulation (earlier).
- **Divide Two Integers** (LC 29) — division without `*`/`/`/`%`, similar spirit.

---

**→ Next:** [`07-Reverse-Integer.md`](./07-Reverse-Integer.md) | **Prev:** [`05-Missing-Number.md`](./05-Missing-Number.md) | [Problem set index](./00-Index.md)
