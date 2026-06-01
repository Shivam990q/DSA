# Single Number

**Platform**: LeetCode 136 · **Difficulty**: Easy · **Topics**: Array, Bit Manipulation · **Pattern**: XOR fold

---

## 📜 Problem Statement

Given a **non-empty** array of integers `nums`, every element appears **twice** except for one. Find that single one.

You must implement a solution with a **linear runtime complexity** and use only **constant extra space**.

### Examples

**Example 1:**
```
Input:  nums = [2,2,1]
Output: 1
```

**Example 2:**
```
Input:  nums = [4,1,2,1,2]
Output: 4
```

**Example 3:**
```
Input:  nums = [1]
Output: 1
```

### Constraints
```
1 <= nums.length <= 3 * 10^4
-3 * 10^4 <= nums[i] <= 3 * 10^4
Each element appears twice except for one element which appears once.
```

---

## 🧠 Understanding the problem

The explicit ask — **O(n) time, O(1) space** — rules out the easy hash-set or sorting tricks (those cost extra space or a log factor). That constraint is a giant hint pointing at **XOR**.

XOR has two magical properties: `a ^ a = 0` (a value XORed with itself vanishes) and `a ^ 0 = a` (XOR with zero is identity). It's also commutative and associative, so the order doesn't matter. If we XOR **every** element together, each value that appears twice cancels to 0, and the lone value is left standing. That's a single pass with one integer of state — exactly O(n) / O(1).

---

## Approach 1 — Hash set / counting (baseline)

### Intuition
Track which numbers you've seen. Add on first sight, remove on second; whatever remains is the single one. Or count frequencies and find the one with count 1.

### Algorithm
1. Insert/erase each value in a set (toggle).
2. The set ends with exactly one element — the answer.

### Dry run on `[4,1,2,1,2]`
```
see 4 → {4}; 1 → {4,1}; 2 → {4,1,2};
1 again → erase → {4,2}; 2 again → erase → {4}
answer = 4
```

### Code
```cpp
int singleNumber(vector<int>& nums) {
    unordered_set<int> seen;
    for (int x : nums) {
        if (seen.count(x)) seen.erase(x);
        else seen.insert(x);
    }
    return *seen.begin();
}
```
```java
public int singleNumber(int[] nums) {
    Set<Integer> seen = new HashSet<>();
    for (int x : nums) {
        if (!seen.add(x)) seen.remove(x);
    }
    return seen.iterator().next();
}
```
```python
def singleNumber(nums):
    seen = set()
    for x in nums:
        if x in seen:
            seen.discard(x)
        else:
            seen.add(x)
    return next(iter(seen))
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) — **violates the constant-space requirement.**

### Verdict
Works and is O(n) time, but the O(n) space breaks the explicit constraint. It's the baseline that motivates XOR.

---

## Approach 2 — XOR fold (optimal) ⭐

### Intuition
XOR all numbers. Paired values annihilate; the unique value survives.

### Algorithm
1. `x = 0`.
2. For each `n` in `nums`: `x ^= n`.
3. Return `x`.

### Dry run on `[4,1,2,1,2]`
```
0^4=4
4^1=5
5^2=7
7^1=6
6^2=4
answer = 4  ✓  (the two 1's and two 2's cancelled)
```

### Code
```cpp
int singleNumber(vector<int>& nums) {
    int x = 0;
    for (int n : nums) x ^= n;
    return x;
}
```
```java
public int singleNumber(int[] nums) {
    int x = 0;
    for (int n : nums) x ^= n;
    return x;
}
```
```python
def singleNumber(nums):
    x = 0
    for n in nums:
        x ^= n
    return x
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1) — one integer.

### Verdict
**The optimal answer** and exactly what the constraints demand. One line of real work; the proof is the XOR cancellation algebra.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Hash set / count | O(n) | O(n) | violates O(1) space |
| XOR fold | **O(n)** | **O(1)** | optimal ⭐ |

A "sum trick" — `2 * sum(set(nums)) - sum(nums)` — also finds the single value but needs O(n) space for the set and can overflow. XOR is strictly better.

---

## 🧪 Edge cases & pitfalls
- **Single element** (`[1]`) → `0 ^ 1 = 1`. Correct.
- **Negative numbers** → XOR works bitwise regardless of sign (two's complement); no special handling.
- **Order independence** → XOR is commutative/associative, so input order never matters.
- **Pitfall**: assuming you need to find *which* value is duplicated — you don't; XOR ignores that entirely.
- **Pitfall — wrong variant**: this is "appears twice." If values appear **three** times except one (LC 137), XOR alone fails; you need bit-count mod 3 or two-accumulator logic.

---

## 🔗 Related problems
- **Single Number II** (LC 137) — every element thrice except one; bitwise mod-3 counting.
- **Single Number III** (LC 260) — two singles; XOR then split by a differing bit.
- **Missing Number** (LC 268) — XOR indices vs values (later in this set).
- **Find the Duplicate Number** (LC 287) — different technique (Floyd's cycle).

---

**→ Next:** [`02-Number-of-1-Bits.md`](./02-Number-of-1-Bits.md) | [Problem set index](./00-Index.md)
