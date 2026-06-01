# Plus One

**Platform**: LeetCode 66 · **Difficulty**: Easy · **Topics**: Array, Math · **Pattern**: Carry from the right

---

## 📜 Problem Statement

You are given a **large integer** represented as an integer array `digits`, where each `digits[i]` is the `i`-th digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading `0`'s.

Increment the large integer by one and return *the resulting array of digits*.

### Examples

**Example 1:**
```
Input:  digits = [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123. Incrementing by one gives 124.
```

**Example 2:**
```
Input:  digits = [4,3,2,1]
Output: [4,3,2,2]
Explanation: The array represents the integer 4321. Incrementing by one gives 4322.
```

**Example 3:**
```
Input:  digits = [9]
Output: [1,0]
Explanation: 9 + 1 = 10.
```

### Constraints
```
1 <= digits.length <= 100
0 <= digits[i] <= 9
digits does not contain any leading 0's.
```

---

## 🧠 Understanding the problem

Adding one to a decimal number only matters at the rightmost digit unless it's a `9`. If the last digit is `< 9`, just bump it and we're done. If it's `9`, it becomes `0` and the carry moves one position left — and that can cascade (`999 → 1000`).

The only time the array length changes is when **every** digit is `9`: then all become `0` and a leading `1` is prepended, growing the length by one. That's the single special case.

---

## Approach 1 — Carry propagation from the right (optimal) ⭐

### Intuition
Walk from the least significant digit. If a digit is below 9, increment and return immediately (no carry beyond here). If it's 9, set it to 0 and continue left. If we fall off the left end, every digit was 9 → prepend a 1.

### Algorithm
1. For `i` from `n-1` down to `0`:
   - If `digits[i] < 9` → `digits[i]++`; return `digits`.
   - Else → `digits[i] = 0` (carry continues).
2. If we exit the loop → prepend `1`: return `[1, 0, 0, …, 0]`.

### Dry run on `[1,2,9]`
```
i=2: 9 → set 0, carry
i=1: 2 < 9 → 3, return [1,3,0]  ✓
```
Dry run on `[9,9]`:
```
i=1: 9 → 0
i=0: 9 → 0
fell off left → prepend 1 → [1,0,0]  ✓
```

### Code
```cpp
vector<int> plusOne(vector<int>& digits) {
    for (int i = digits.size() - 1; i >= 0; i--) {
        if (digits[i] < 9) { digits[i]++; return digits; }
        digits[i] = 0;
    }
    digits.insert(digits.begin(), 1);
    return digits;
}
```
```java
public int[] plusOne(int[] digits) {
    for (int i = digits.length - 1; i >= 0; i--) {
        if (digits[i] < 9) { digits[i]++; return digits; }
        digits[i] = 0;
    }
    int[] res = new int[digits.length + 1];
    res[0] = 1;                 // rest default to 0
    return res;
}
```
```python
def plusOne(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits
```

### Complexity
- **Time**: O(n) — worst case all 9's; usually O(1) (early return).
- **Space**: O(1) in place (O(n) only when a new leading digit forces a new array).

### Verdict
**Optimal.** Early return on the first non-9 makes the common case O(1). The all-9's prepend is the only branch to remember.

---

## Approach 2 — Explicit carry variable

### Intuition
Same logic written with a `carry` flag, which can read more uniformly (and generalizes to "plus k").

### Algorithm
1. `carry = 1` (the "+1").
2. For `i` from `n-1` down to `0`: `sum = digits[i] + carry`; `digits[i] = sum % 10`; `carry = sum / 10`; if `carry == 0` break.
3. If `carry` remains → prepend it.

### Dry run on `[9]`
```
carry=1; i=0: sum=10 → digit 0, carry=1
loop ends, carry=1 → prepend → [1,0]  ✓
```

### Code
```cpp
vector<int> plusOne(vector<int>& digits) {
    int carry = 1;
    for (int i = digits.size() - 1; i >= 0 && carry; i--) {
        int sum = digits[i] + carry;
        digits[i] = sum % 10;
        carry = sum / 10;
    }
    if (carry) digits.insert(digits.begin(), carry);
    return digits;
}
```
```java
public int[] plusOne(int[] digits) {
    int carry = 1;
    for (int i = digits.length - 1; i >= 0 && carry > 0; i--) {
        int sum = digits[i] + carry;
        digits[i] = sum % 10;
        carry = sum / 10;
    }
    if (carry == 0) return digits;
    int[] res = new int[digits.length + 1];
    res[0] = 1;
    System.arraycopy(digits, 0, res, 1, digits.length);
    return res;
}
```
```python
def plusOne(digits):
    carry = 1
    for i in range(len(digits) - 1, -1, -1):
        if carry == 0:
            break
        total = digits[i] + carry
        digits[i] = total % 10
        carry = total // 10
    if carry:
        return [carry] + digits
    return digits
```

### Complexity
- **Time**: O(n).
- **Space**: O(1) in place (O(n) on overflow).

### Verdict
Equivalent and slightly more general (swap the initial `carry` for any addend). Either approach is a fine answer.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Direct carry (early return) | O(n) | O(1) | shortest, common case O(1) ⭐ |
| Carry variable | O(n) | O(1) | generalizes to "+k" |

---

## 🧪 Edge cases & pitfalls
- **All 9's** (`[9,9,9]`) → `[1,0,0,0]`; the only length-changing case.
- **Single `[0]`** → `[1]`.
- **No carry** (`[1,2,3]`) → bump last digit, return immediately.
- **Pitfall — Java in-place insert**: arrays can't grow, so the all-9's case must allocate a new `n+1` array (defaults to zeros, set `res[0]=1`).
- **Pitfall**: trying to convert the array to an `int` and back — fails for 100-digit inputs, which exceed 64-bit range.

---

## 🔗 Related problems
- **Add Strings** (LC 415) — general two-number addition.
- **Add Two Numbers** (LC 2) — carry on a linked list.
- **Multiply Strings** (LC 43) — big-number arithmetic (earlier).
- **Plus One Linked List** (LC 369) — same carry idea on a list.

---

**→ Next:** [`08-Detect-Squares.md`](./08-Detect-Squares.md) | **Prev:** [`06-Happy-Number.md`](./06-Happy-Number.md) | [Problem set index](./00-Index.md)
