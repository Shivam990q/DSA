# Reverse Bits

**Platform**: LeetCode 190 · **Difficulty**: Easy · **Topics**: Divide and Conquer, Bit Manipulation · **Pattern**: Bit-by-bit pull and push

---

## 📜 Problem Statement

Reverse bits of a given 32 bits unsigned integer.

**Note**:
- Note that in some languages, such as Java, there is no unsigned integer type. In this case, both input and output will be given as a signed integer type. They should not affect your implementation, as the integer's internal binary representation is the same, whether it is signed or unsigned.
- In Java, the compiler represents the signed integers using **2's complement notation**. Therefore, in **Example 2** below, the input represents the signed integer `-3` and the output represents the signed integer `-1073741825`.

### Examples

**Example 1:**
```
Input:  n = 00000010100101000001111010011100
Output:    964176192 (00111001011110000010100101000000)
Explanation: The input binary string 00000010100101000001111010011100 represents
the unsigned integer 43261596, so return 964176192 which its binary representation
is 00111001011110000010100101000000.
```

**Example 2:**
```
Input:  n = 11111111111111111111111111111101
Output:   3221225471 (10111111111111111111111111111111)
Explanation: The input represents the unsigned integer 4294967293, return
3221225471 which its binary representation is 10111111111111111111111111111111.
```

### Constraints
```
The input must be a binary string of length 32.
```

**Follow up**: If this function is called many times, how would you optimize it?

---

## 🧠 Understanding the problem

We want bit position `i` of the input to land at position `31 - i` of the output. The simplest mechanical way: repeatedly pull the **lowest** bit off the input and push it onto the **lowest** position of the result, shifting the result left each step. After 32 iterations, the first bit pulled (input bit 0) has been shifted all the way to position 31 — exactly the reversal.

Language note: in **Java/Python** there's no native 32-bit unsigned type, so we must use unsigned shifts (`>>>` in Java) and mask to 32 bits (in Python) to avoid sign issues.

---

## Approach 1 — Bit-by-bit reversal (optimal for one call) ⭐

### Intuition
Each step: shift `res` left by 1 (making room at the bottom), OR in the lowest bit of `n`, then shift `n` right by 1.

### Algorithm
1. `res = 0`.
2. Repeat 32 times: `res = (res << 1) | (n & 1)`; `n >>= 1` (unsigned).
3. Return `res`.

### Dry run on a 4-bit toy `n = 1011` (reverse → `1101`)
```
res=0
bit1: res=(0<<1)|1=1;  n=101
bit1: res=(1<<1)|1=11; n=10
bit0: res=(11<<1)|0=110; n=1
bit1: res=(110<<1)|1=1101; n=0
result = 1101  ✓  (full problem does 32 iterations)
```

### Code
```cpp
uint32_t reverseBits(uint32_t n) {
    uint32_t res = 0;
    for (int i = 0; i < 32; i++) {
        res = (res << 1) | (n & 1);
        n >>= 1;
    }
    return res;
}
```
```java
public int reverseBits(int n) {
    int res = 0;
    for (int i = 0; i < 32; i++) {
        res = (res << 1) | (n & 1);
        n >>>= 1;            // unsigned right shift
    }
    return res;
}
```
```python
def reverseBits(n):
    res = 0
    for _ in range(32):
        res = (res << 1) | (n & 1)
        n >>= 1
    return res & 0xFFFFFFFF
```

### Complexity
- **Time**: O(32) = O(1).
- **Space**: O(1).

### Verdict
**The optimal single-call answer.** 32 fixed iterations, no tricks beyond the pull/push. The `& 0xFFFFFFFF` in Python keeps the result within 32 bits.

---

## Approach 2 — Swap groups (divide and conquer)

### Intuition
Reverse by swapping halves, then quarters, then eighths, down to single bits — like a butterfly network. Reverse adjacent 16-bit halves, then 8-bit groups, 4, 2, 1. Each step is a masked shift. This is `O(log 32)` operations.

### Algorithm
1. Swap the two 16-bit halves.
2. Swap 8-bit groups within each half.
3. Swap 4-bit, then 2-bit, then 1-bit groups.

### Dry run (conceptual)
```
ABCD (4 groups of 8) → swap halves → CDAB → swap within → DCBA ... down to single bits
each mask/shift halves the group size
```

### Code
```cpp
uint32_t reverseBits(uint32_t n) {
    n = (n >> 16) | (n << 16);
    n = ((n & 0xff00ff00) >> 8) | ((n & 0x00ff00ff) << 8);
    n = ((n & 0xf0f0f0f0) >> 4) | ((n & 0x0f0f0f0f) << 4);
    n = ((n & 0xcccccccc) >> 2) | ((n & 0x33333333) << 2);
    n = ((n & 0xaaaaaaaa) >> 1) | ((n & 0x55555555) << 1);
    return n;
}
```
```java
public int reverseBits(int n) {
    n = (n >>> 16) | (n << 16);
    n = ((n & 0xff00ff00) >>> 8) | ((n & 0x00ff00ff) << 8);
    n = ((n & 0xf0f0f0f0) >>> 4) | ((n & 0x0f0f0f0f) << 4);
    n = ((n & 0xcccccccc) >>> 2) | ((n & 0x33333333) << 2);
    n = ((n & 0xaaaaaaaa) >>> 1) | ((n & 0x55555555) << 1);
    return n;
}
```
```python
def reverseBits(n):
    n = ((n >> 16) | (n << 16)) & 0xFFFFFFFF
    n = (((n & 0xff00ff00) >> 8) | ((n & 0x00ff00ff) << 8)) & 0xFFFFFFFF
    n = (((n & 0xf0f0f0f0) >> 4) | ((n & 0x0f0f0f0f) << 4)) & 0xFFFFFFFF
    n = (((n & 0xcccccccc) >> 2) | ((n & 0x33333333) << 2)) & 0xFFFFFFFF
    n = (((n & 0xaaaaaaaa) >> 1) | ((n & 0x55555555) << 1)) & 0xFFFFFFFF
    return n
```

### Complexity
- **Time**: O(log 32) = 5 masked operations, O(1).
- **Space**: O(1).

### Verdict
A beautiful constant-step reversal that avoids the 32-iteration loop. Worth knowing for the "optimize" prompt; the bit-by-bit loop is easier to recall under pressure.

---

## Approach 3 — Byte-cache memoization (the follow-up)

### Intuition
For "called many times," precompute the reversal of every 8-bit value, then assemble the 32-bit result from four reversed bytes placed in swapped positions, with caching.

### Algorithm
1. `reverseByte(b)` reverses an 8-bit value (cache results).
2. For input `n`, reverse each of the 4 bytes and place byte `k` at position `(3-k)`.

### Dry run (conceptual)
```
n = [b3 b2 b1 b0] → result = [rev(b0) rev(b1) rev(b2) rev(b3)]
```

### Code
```cpp
class Solution {
    unordered_map<uint32_t, uint32_t> cache;
    uint32_t reverseByte(uint32_t b) {
        auto it = cache.find(b);
        if (it != cache.end()) return it->second;
        uint32_t r = 0, x = b;
        for (int i = 0; i < 8; i++) { r = (r << 1) | (x & 1); x >>= 1; }
        cache[b] = r;
        return r;
    }
public:
    uint32_t reverseBits(uint32_t n) {
        uint32_t res = 0;
        for (int i = 0; i < 4; i++) {
            uint32_t byte = (n >> (8 * i)) & 0xFF;
            res |= (reverseByte(byte) << (8 * (3 - i)));
        }
        return res;
    }
};
```
```java
class Solution {
    private final Map<Integer, Integer> cache = new HashMap<>();
    public int reverseBits(int n) {
        int res = 0;
        for (int i = 0; i < 4; i++) {
            int b = (n >>> (8 * i)) & 0xFF;
            int r = cache.computeIfAbsent(b, key -> {
                int v = 0, x = key;
                for (int k = 0; k < 8; k++) { v = (v << 1) | (x & 1); x >>= 1; }
                return v;
            });
            res |= (r << (8 * (3 - i)));
        }
        return res;
    }
}
```
```python
class Solution:
    _cache = {}
    def reverseBits(self, n):
        res = 0
        for i in range(4):
            b = (n >> (8 * i)) & 0xFF
            if b in Solution._cache:
                r = Solution._cache[b]
            else:
                r, x = 0, b
                for _ in range(8):
                    r = (r << 1) | (x & 1)
                    x >>= 1
                Solution._cache[b] = r
            res |= r << (8 * (3 - i))
        return res & 0xFFFFFFFF
```

### Complexity
- **Time**: O(1) per call (four cached byte lookups after warm-up).
- **Space**: O(256) cache.

### Verdict
The intended answer to "called many times": cache byte reversals and stitch. The divide-and-conquer (Approach 2) is also constant-time without a cache.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Bit-by-bit | O(32) | O(1) | simplest, recommended single-call ⭐ |
| Swap groups | O(1) (5 ops) | O(1) | branchless, elegant |
| Byte cache | O(1) | O(256) | best for many calls (follow-up) |

---

## 🧪 Edge cases & pitfalls
- **`n = 0`** → `0`.
- **All ones** → all ones (palindrome).
- **Java sign pitfall**: must use `>>>` (unsigned shift); `>>` would smear the sign bit. The result `int` may *look* negative — that's the correct unsigned bit pattern.
- **Python width pitfall**: Python ints are unbounded, so mask with `& 0xFFFFFFFF` to confine the result to 32 bits.
- **Pitfall — shifting result the wrong way**: you shift `res` **left** and pull `n`'s **lowest** bit; reversing those directions reverses nothing.

---

## 🔗 Related problems
- **Number of 1 Bits** (LC 191) — bit iteration / byte table (earlier).
- **Reverse Integer** (LC 7) — decimal-digit reversal (later).
- **Sum of Two Integers** (LC 371) — bit-level arithmetic (next).
- **Bitwise AND of Numbers Range** (LC 201) — common prefix of bits.

---

**→ Next:** [`05-Missing-Number.md`](./05-Missing-Number.md) | **Prev:** [`03-Counting-Bits.md`](./03-Counting-Bits.md) | [Problem set index](./00-Index.md)
