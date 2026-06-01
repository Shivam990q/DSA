# Happy Number

**Platform**: LeetCode 202 · **Difficulty**: Easy · **Topics**: Hash Table, Math, Two Pointers · **Pattern**: Cycle detection

---

## 📜 Problem Statement

Write an algorithm to determine if a number `n` is **happy**.

A **happy number** is a number defined by the following process:

- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals `1` (where it will stay), or it **loops endlessly in a cycle** which does not include `1`.
- Those numbers for which this process **ends in 1** are happy.

Return `true` *if* `n` *is a happy number, and* `false` *if not*.

### Examples

**Example 1:**
```
Input:  n = 19
Output: true
Explanation:
1^2 + 9^2 = 82
8^2 + 2^2 = 68
6^2 + 8^2 = 100
1^2 + 0^2 + 0^2 = 1
```

**Example 2:**
```
Input:  n = 2
Output: false
Explanation: 2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 → ... (cycle, never 1).
```

**Example 3:**
```
Input:  n = 7
Output: true
Explanation: 7 → 49 → 97 → 130 → 10 → 1.
```

### Constraints
```
1 <= n <= 2^31 - 1
```

---

## 🧠 Understanding the problem

Define `next(n)` = sum of squares of `n`'s digits. Iterating `next` produces a sequence. A classic number-theory fact guarantees this sequence is **bounded** (for any starting point it eventually drops below 1000 and stays in a small range), so it must either reach `1` or fall into a repeating **cycle**. The only cycle not containing 1 is the well-known `4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4`.

So the problem reduces to **cycle detection**: follow the sequence; if we ever revisit a value, we're in a loop → not happy. If we reach `1`, it's happy. We can detect the revisit with a hash set, or with Floyd's tortoise-and-hare (constant space) — exactly the same trick as Linked List Cycle.

---

## Approach 1 — Hash set of seen values

### Intuition
Keep a set of every value we've produced. If `next` ever yields something already in the set (and it isn't 1), we've cycled.

### Algorithm
1. `seen = {}`.
2. While `n != 1` and `n` not in `seen`: insert `n`, set `n = next(n)`.
3. Return `n == 1`.

### Dry run on `n=19`
```
19 → 82 → 68 → 100 → 1 → stop, n==1 → true
none repeated → happy
```

### Code
```cpp
class Solution {
    int next(int n) {
        int s = 0;
        while (n) { int d = n % 10; s += d * d; n /= 10; }
        return s;
    }
public:
    bool isHappy(int n) {
        unordered_set<int> seen;
        while (n != 1 && !seen.count(n)) {
            seen.insert(n);
            n = next(n);
        }
        return n == 1;
    }
};
```
```java
class Solution {
    private int next(int n) {
        int s = 0;
        while (n > 0) { int d = n % 10; s += d * d; n /= 10; }
        return s;
    }
    public boolean isHappy(int n) {
        Set<Integer> seen = new HashSet<>();
        while (n != 1 && !seen.contains(n)) {
            seen.add(n);
            n = next(n);
        }
        return n == 1;
    }
}
```
```python
def isHappy(n):
    def nxt(x):
        return sum(int(d) ** 2 for d in str(x))
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = nxt(n)
    return n == 1
```

### Complexity
- **Time**: O(log n) per `next` step; the number of steps is bounded by a constant (the sequence collapses into a small range), so effectively O(log n) total.
- **Space**: O(k) for the set, where `k` is the number of distinct values visited (small/bounded).

### Verdict
Simplest and very readable. Perfectly fine, but uses extra space — Floyd removes that.

---

## Approach 2 — Floyd's fast/slow pointers (optimal space) ⭐

### Intuition
Treat the sequence `n → next(n) → next(next(n)) → …` as a linked list with a possible cycle. Advance `slow` by one `next` and `fast` by two. If there's a cycle they meet; if `fast` reaches `1`, it's happy.

### Algorithm
1. `slow = n`, `fast = next(n)`.
2. While `fast != 1` and `slow != fast`: `slow = next(slow)`, `fast = next(next(fast))`.
3. Return `fast == 1`.

### Dry run on `n=2`
```
slow=2 fast=4
slow=4 fast=next(next(4))=next(16)=37
slow=16 fast=next(next(37))=next(58)=89
... slow and fast eventually coincide inside the 4→16→37... cycle, fast never 1
→ false  ✓
```

### Code
```cpp
class Solution {
    int next(int n) {
        int s = 0;
        while (n) { int d = n % 10; s += d * d; n /= 10; }
        return s;
    }
public:
    bool isHappy(int n) {
        int slow = n, fast = next(n);
        while (fast != 1 && slow != fast) {
            slow = next(slow);
            fast = next(next(fast));
        }
        return fast == 1;
    }
};
```
```java
class Solution {
    private int next(int n) {
        int s = 0;
        while (n > 0) { int d = n % 10; s += d * d; n /= 10; }
        return s;
    }
    public boolean isHappy(int n) {
        int slow = n, fast = next(n);
        while (fast != 1 && slow != fast) {
            slow = next(slow);
            fast = next(next(fast));
        }
        return fast == 1;
    }
}
```
```python
def isHappy(n):
    def nxt(x):
        s = 0
        while x:
            d = x % 10
            s += d * d
            x //= 10
        return s
    slow, fast = n, nxt(n)
    while fast != 1 and slow != fast:
        slow = nxt(slow)
        fast = nxt(nxt(fast))
    return fast == 1
```

### Complexity
- **Time**: O(log n) per step, bounded number of steps → effectively constant rounds.
- **Space**: O(1) — no set.

### Verdict
**The optimal answer** when asked for constant space. Same idea as detecting a cycle in a linked list; a great way to show you recognize the pattern.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Hash set | O(log n)·(bounded) | O(k) | simplest, most readable |
| Floyd fast/slow | O(log n)·(bounded) | **O(1)** | constant space ⭐ |

Both terminate because the sequence is provably bounded; there is no risk of running forever.

---

## 🧪 Edge cases & pitfalls
- **`n = 1`** → already happy → `true` (set loop exits immediately; Floyd's `fast = next(1) = 1`).
- **Single-digit non-happy** (`2,3,4,5,6,8,9`) → fall into the 4-cycle → `false`.
- **Large `n` near 2^31** → `next` quickly shrinks it; no overflow because digit-square sums stay small.
- **Pitfall — Floyd init**: start `fast = next(n)` (one ahead), not `fast = n`, or the `slow != fast` check passes the first iteration trivially and you must restructure the loop.
- **Pitfall — infinite loop fear**: it's safe; the math guarantees a bound, so you don't need an iteration cap.

---

## 🔗 Related problems
- **Linked List Cycle** (LC 141) — the same Floyd's algorithm on a real list.
- **Find the Duplicate Number** (LC 287) — Floyd on an implicit functional graph.
- **Add Digits** (LC 258) — digit-process variant (digital root).
- **Ugly Number** (LC 263) — another "process until termination" number check.

---

**→ Next:** [`07-Plus-One.md`](./07-Plus-One.md) | **Prev:** [`05-Multiply-Strings.md`](./05-Multiply-Strings.md) | [Problem set index](./00-Index.md)
