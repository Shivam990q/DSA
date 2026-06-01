# Counting Bits

**Platform**: LeetCode 338 · **Difficulty**: Easy · **Topics**: Dynamic Programming, Bit Manipulation · **Pattern**: Bit DP recurrence

---

## 📜 Problem Statement

Given an integer `n`, return *an array* `ans` *of length* `n + 1` *such that for each* `i` (`0 <= i <= n`)*,* `ans[i]` *is the **number of** `1`*'s* *in the binary representation of* `i`.

### Examples

**Example 1:**
```
Input:  n = 2
Output: [0,1,1]
Explanation:
0 --> 0
1 --> 1
2 --> 10
```

**Example 2:**
```
Input:  n = 5
Output: [0,1,1,2,1,2]
Explanation:
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100
5 --> 101
```

**Example 3:**
```
Input:  n = 0
Output: [0]
```

### Constraints
```
0 <= n <= 10^5
```

**Follow up**:
- It is very easy to come up with a solution with a runtime of `O(n log n)`. Can you do it in linear time `O(n)` and possibly in a single pass?
- Can you do it without using any built-in function?

---

## 🧠 Understanding the problem

We need the popcount of *every* number from 0 to `n`, not just one. The naive way computes each popcount independently in O(log n), giving O(n log n) overall. The follow-up wants **O(n)**.

The trick is **dynamic programming using an already-computed smaller number**. Two clean recurrences:

1. **Right-shift relation**: `bits[i] = bits[i >> 1] + (i & 1)`. Dropping the lowest bit of `i` gives `i >> 1`, whose popcount we already know; add back the bit we dropped (`i & 1`). Since `i >> 1 < i`, it's computed.
2. **Lowest-set-bit relation**: `bits[i] = bits[i & (i - 1)] + 1`. Clearing the lowest set bit gives a smaller number with exactly one fewer `1`.

Both fill the table in a single forward pass, O(n) time.

---

## Approach 1 — Per-number popcount (baseline, O(n log n))

### Intuition
For each `i`, count its bits independently with the `i & (i-1)` trick.

### Algorithm
1. For `i` in `0..n`: count set bits of `i` via the clear-lowest-bit loop.

### Dry run on `n = 5`
```
0→0,1→1,2→1,3→2,4→1,5→2 → [0,1,1,2,1,2]
```

### Code
```cpp
vector<int> countBits(int n) {
    vector<int> ans(n + 1, 0);
    for (int i = 0; i <= n; i++) {
        int x = i, c = 0;
        while (x) { x &= (x - 1); c++; }
        ans[i] = c;
    }
    return ans;
}
```
```java
public int[] countBits(int n) {
    int[] ans = new int[n + 1];
    for (int i = 0; i <= n; i++) {
        int x = i, c = 0;
        while (x != 0) { x &= (x - 1); c++; }
        ans[i] = c;
    }
    return ans;
}
```
```python
def countBits(n):
    ans = [0] * (n + 1)
    for i in range(n + 1):
        x, c = i, 0
        while x:
            x &= x - 1
            c += 1
        ans[i] = c
    return ans
```

### Complexity
- **Time**: O(n log n) — each popcount up to O(log i).
- **Space**: O(1) extra (besides the output).

### Verdict
Correct and simple, but doesn't meet the O(n) follow-up. The DP reuses prior results to drop the log factor.

---

## Approach 2 — DP with right-shift relation (optimal) ⭐

### Intuition
`bits[i] = bits[i >> 1] + (i & 1)`. The popcount of `i` equals the popcount of `i` with its lowest bit removed, plus that lowest bit.

### Algorithm
1. `bits[0] = 0`.
2. For `i` from `1` to `n`: `bits[i] = bits[i >> 1] + (i & 1)`.
3. Return `bits`.

### Dry run on `n = 5`
```
bits[1]=bits[0]+1=1
bits[2]=bits[1]+0=1
bits[3]=bits[1]+1=2
bits[4]=bits[2]+0=1
bits[5]=bits[2]+1=2
→ [0,1,1,2,1,2]  ✓
```

### Code
```cpp
vector<int> countBits(int n) {
    vector<int> bits(n + 1, 0);
    for (int i = 1; i <= n; i++)
        bits[i] = bits[i >> 1] + (i & 1);
    return bits;
}
```
```java
public int[] countBits(int n) {
    int[] bits = new int[n + 1];
    for (int i = 1; i <= n; i++)
        bits[i] = bits[i >> 1] + (i & 1);
    return bits;
}
```
```python
def countBits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits
```

### Complexity
- **Time**: O(n) — single pass, O(1) per entry.
- **Space**: O(1) extra (besides output).

### Verdict
**The optimal answer** to the follow-up: linear, single pass, no built-ins. Memorize the `bits[i] = bits[i>>1] + (i&1)` line.

---

## Approach 3 — DP with lowest-set-bit relation

### Intuition
`bits[i] = bits[i & (i - 1)] + 1`. Clearing the lowest set bit yields a smaller already-computed index with one fewer `1`.

### Algorithm
1. `bits[0] = 0`.
2. For `i` from `1` to `n`: `bits[i] = bits[i & (i - 1)] + 1`.

### Dry run on `n = 5`
```
bits[1]=bits[0]+1=1
bits[2]=bits[0]+1=1
bits[3]=bits[2]+1=2
bits[4]=bits[0]+1=1
bits[5]=bits[4]+1=2
→ [0,1,1,2,1,2]  ✓
```

### Code
```cpp
vector<int> countBits(int n) {
    vector<int> bits(n + 1, 0);
    for (int i = 1; i <= n; i++)
        bits[i] = bits[i & (i - 1)] + 1;
    return bits;
}
```
```java
public int[] countBits(int n) {
    int[] bits = new int[n + 1];
    for (int i = 1; i <= n; i++)
        bits[i] = bits[i & (i - 1)] + 1;
    return bits;
}
```
```python
def countBits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i & (i - 1)] + 1
    return bits
```

### Complexity
- **Time**: O(n).
- **Space**: O(1) extra.

### Verdict
Equally optimal — a second elegant recurrence. Knowing both shows command of the bit identities. Either is a perfect answer.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Per-number popcount | O(n log n) | O(1) | misses the O(n) follow-up |
| DP `bits[i>>1] + (i&1)` | **O(n)** | O(1) | optimal, single pass ⭐ |
| DP `bits[i&(i-1)] + 1` | **O(n)** | O(1) | equally optimal |

---

## 🧪 Edge cases & pitfalls
- **`n = 0`** → `[0]`; both DP loops simply don't run.
- **Powers of two** → exactly one set bit; the recurrences yield 1 (`bits[2^k] = bits[2^{k-1}] + 0` in the shift version).
- **Pitfall — indexing forward correctly**: the DP relies on `i >> 1 < i` and `i & (i-1) < i`, both strictly smaller, so a forward loop guarantees the dependency is ready.
- **Pitfall — off-by-one**: the array has length `n + 1` (indices `0..n` inclusive). Forgetting the `+1` truncates the last answer.

---

## 🔗 Related problems
- **Number of 1 Bits** (LC 191) — single-number popcount (previous).
- **Single Number** (LC 136) — XOR trick (earlier).
- **Binary Watch** (LC 401) — enumerate by popcount.
- **Count Numbers with Unique Digits** (LC 357) — counting DP flavor.

---

**→ Next:** [`04-Reverse-Bits.md`](./04-Reverse-Bits.md) | **Prev:** [`02-Number-of-1-Bits.md`](./02-Number-of-1-Bits.md) | [Problem set index](./00-Index.md)
