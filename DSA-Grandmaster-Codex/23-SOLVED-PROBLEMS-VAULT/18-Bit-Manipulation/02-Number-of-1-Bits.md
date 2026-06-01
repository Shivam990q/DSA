# Number of 1 Bits

**Platform**: LeetCode 191 · **Difficulty**: Easy · **Topics**: Divide and Conquer, Bit Manipulation · **Pattern**: `n & (n-1)` clears lowest set bit

---

## 📜 Problem Statement

Write a function that takes the binary representation of a positive integer and returns the number of set bits it has (also known as the **Hamming weight**).

### Examples

**Example 1:**
```
Input:  n = 11
Output: 3
Explanation: The input binary string 1011 has a total of three set bits.
```

**Example 2:**
```
Input:  n = 128
Output: 1
Explanation: The input binary string 10000000 has a total of one set bit.
```

**Example 3:**
```
Input:  n = 2147483645
Output: 30
Explanation: The input binary string 1111111111111111111111111111101 has thirty set bits.
```

### Constraints
```
1 <= n <= 2^31 - 1
```

**Follow up**: If this function is called many times, how would you optimize it?

---

## 🧠 Understanding the problem

We just need to count the `1`s in the binary form. The naive way checks all 32 bit positions. The slicker way uses the identity **`n & (n - 1)` clears the lowest set bit**: subtracting 1 flips the lowest `1` to `0` and turns all the zeros below it into `1`s, so ANDing with the original wipes out exactly that lowest set bit. Each such operation removes one `1`, so the number of iterations until `n` hits 0 equals the number of set bits — we only loop as many times as there are `1`s, not 32.

---

## Approach 1 — Shift and test every bit

### Intuition
Examine each of the 32 bits: add the lowest bit to a counter, then shift right.

### Algorithm
1. `count = 0`.
2. Repeat 32 times: `count += n & 1`; `n >>= 1` (use unsigned shift in Java).
3. Return `count`.

### Dry run on `n = 11` (`1011`)
```
bit0=1 → count1; bit1=1 → count2; bit2=0; bit3=1 → count3; rest 0
answer = 3
```

### Code
```cpp
int hammingWeight(uint32_t n) {
    int count = 0;
    for (int i = 0; i < 32; i++) {
        count += n & 1;
        n >>= 1;
    }
    return count;
}
```
```java
public int hammingWeight(int n) {
    int count = 0;
    for (int i = 0; i < 32; i++) {
        count += (n & 1);
        n >>>= 1;          // unsigned right shift
    }
    return count;
}
```
```python
def hammingWeight(n):
    count = 0
    for _ in range(32):
        count += n & 1
        n >>= 1
    return count
```

### Complexity
- **Time**: O(32) = O(1) per call (fixed width).
- **Space**: O(1).

### Verdict
Correct and constant-time, but always does 32 iterations regardless of how few bits are set. The `n & (n-1)` trick does fewer.

---

## Approach 2 — Clear the lowest set bit, `n & (n-1)` (optimal) ⭐

### Intuition
Each `n &= (n - 1)` deletes exactly one set bit. Count how many times you can do that before `n` becomes 0.

### Algorithm
1. `count = 0`.
2. While `n != 0`: `n &= (n - 1)`; `count++`.
3. Return `count`.

### Dry run on `n = 12` (`1100`)
```
n=1100, n&(n-1)=1100 & 1011 = 1000 → count1
n=1000, &0111=0000 → count2
n=0 → stop. answer = 2
```

### Code
```cpp
int hammingWeight(uint32_t n) {
    int count = 0;
    while (n) {
        n &= (n - 1);
        count++;
    }
    return count;
}
```
```java
public int hammingWeight(int n) {
    int count = 0;
    while (n != 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}
```
```python
def hammingWeight(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

### Complexity
- **Time**: O(number of set bits) — at most 32, often far fewer.
- **Space**: O(1).

### Verdict
**The optimal answer.** Loops only as many times as there are `1`s. Also the cleanest to state. (Languages also offer builtins: C++ `__builtin_popcount`, Java `Integer.bitCount`, Python `bin(n).count("1")` — fine to mention, but the manual trick shows understanding.)

---

## Approach 3 — Precomputed byte table (the follow-up)

### Intuition
If the function is called many times, precompute the popcount of every 8-bit value once, then sum the counts of the four bytes of `n` with table lookups. Trades a small table for near-instant queries.

### Algorithm
1. Build `table[256]` where `table[b]` = popcount of `b`.
2. For a query: `table[n & 0xFF] + table[(n>>8)&0xFF] + table[(n>>16)&0xFF] + table[(n>>24)&0xFF]`.

### Dry run on `n = 11`
```
byte0 = 11 → table[11]=3; higher bytes 0 → 0
answer = 3
```

### Code
```cpp
class Solution {
    int table[256];
    bool built = false;
    void build() {
        for (int i = 0; i < 256; i++) table[i] = (i & 1) + table[i >> 1];
        built = true;
    }
public:
    int hammingWeight(uint32_t n) {
        if (!built) build();
        return table[n & 0xFF] + table[(n >> 8) & 0xFF]
             + table[(n >> 16) & 0xFF] + table[(n >> 24) & 0xFF];
    }
};
```
```java
class Solution {
    private static final int[] TABLE = new int[256];
    static {
        for (int i = 0; i < 256; i++) TABLE[i] = (i & 1) + TABLE[i >> 1];
    }
    public int hammingWeight(int n) {
        return TABLE[n & 0xFF] + TABLE[(n >>> 8) & 0xFF]
             + TABLE[(n >>> 16) & 0xFF] + TABLE[(n >>> 24) & 0xFF];
    }
}
```
```python
class Solution:
    _table = [0] * 256
    for _i in range(256):
        _table[_i] = (_i & 1) + _table[_i >> 1]
    def hammingWeight(self, n):
        t = Solution._table
        return (t[n & 0xFF] + t[(n >> 8) & 0xFF]
                + t[(n >> 16) & 0xFF] + t[(n >> 24) & 0xFF])
```

### Complexity
- **Time**: O(1) — four lookups per query after an O(256) build.
- **Space**: O(256).

### Verdict
The textbook answer to "called many times." Constant work per call with a tiny shared table. Overkill for a single call but exactly right for the follow-up.

---

## ⚖️ Approach comparison

| Approach | Time/call | Space | Notes |
|----------|-----------|-------|-------|
| Shift & test | O(32) | O(1) | always 32 iterations |
| `n & (n-1)` | O(set bits) | O(1) | optimal single-call ⭐ |
| Byte table | O(1) | O(256) | best for many calls (follow-up) |

---

## 🧪 Edge cases & pitfalls
- **`n = 0`** → 0 set bits (constraints say `n >= 1`, but the loop handles 0 naturally).
- **All bits set** (`2^31 - 1`) → both loops run 31 times.
- **Java sign pitfall**: Java has no unsigned int. Use `>>>` (unsigned shift) in the shift-and-test method, or the `n & (n-1)` method which sidesteps the issue entirely.
- **Pitfall**: using `>>` (arithmetic shift) in Java on a negative-looking value fills with sign bits and loops forever — always `>>>`.

---

## 🔗 Related problems
- **Counting Bits** (LC 338) — popcount for a whole range, via DP (next).
- **Power of Two** (LC 231) — exactly one set bit ⇔ `n & (n-1) == 0`.
- **Hamming Distance** (LC 461) — popcount of `a ^ b`.
- **Reverse Bits** (LC 190) — bit-level processing (later).

---

**→ Next:** [`03-Counting-Bits.md`](./03-Counting-Bits.md) | **Prev:** [`01-Single-Number.md`](./01-Single-Number.md) | [Problem set index](./00-Index.md)
