# Koko Eating Bananas

**Platform**: LeetCode 875 · **Difficulty**: Medium · **Topics**: Array, Binary Search · **Pattern**: Binary search on the answer

---

## 📜 Problem Statement

Koko loves to eat bananas. There are `n` piles of bananas, the `i`-th pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.

Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has fewer than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the **minimum integer** `k` such that she can eat all the bananas within `h` hours.

### Examples

**Example 1:**
```
Input:  piles = [3,6,7,11], h = 8
Output: 4
Explanation: At speed 4 → ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4)
                        =   1   +   2   +   2   +   3   = 8 hours. ✅
At speed 3 it would take 1+2+3+4 = 10 > 8 hours, so 4 is the minimum.
```

**Example 2:**
```
Input:  piles = [30,11,23,4,20], h = 5
Output: 30
Explanation: There are 5 piles and 5 hours, so she must finish one pile per hour.
The minimum speed must clear the biggest pile (30) in a single hour.
```

**Example 3:**
```
Input:  piles = [30,11,23,4,20], h = 6
Output: 23
```

### Constraints
```
1 <= piles.length <= 10^4
piles.length <= h <= 10^9
1 <= piles[i] <= 10^9
```

---

## 🧠 Understanding the problem

First, decode the eating rule. Koko eats from **one pile per hour**, and she can't "carry over" leftover capacity to another pile in the same hour. So a pile of size `p` eaten at speed `k` takes `ceil(p / k)` hours — for example a pile of 7 at speed 4 takes 2 hours (4 then 3), wasting part of the second hour.

Total hours at speed `k`:
```
hours(k) = Σ ceil(piles[i] / k)
```

We want the **smallest** `k` with `hours(k) <= h`.

The crucial observation is **monotonicity**. As `k` increases, `hours(k)` can only **decrease or stay the same** — eating faster never takes more time. So if we list speeds `1, 2, 3, ...` and mark each "can she finish in time?":

```
k:        1   2   3   4   5   6  ...
finish?:  N   N   N   Y   Y   Y  ...
                      ↑ first Yes = answer
```

This false→true boundary is **exactly** what binary search finds. This is the textbook "**binary search on the answer**" pattern: we don't search the array, we search the *space of possible speeds*.

What are the bounds for `k`?
- **Minimum** sensible speed is `1` (she must eat at least one banana per hour).
- **Maximum** useful speed is `max(piles)`: at that speed every pile takes exactly 1 hour, which is the fewest possible (one pile per hour). Going faster never helps because she still spends a whole hour per pile. And since `h >= piles.length`, speed `max(piles)` always finishes in time, so the answer is in `[1, max(piles)]`.

---

## Approach 1 — Linear scan over speeds (baseline)

### Intuition
Try every speed `k = 1, 2, 3, ...` in order and return the first that finishes within `h` hours. Because of monotonicity, the first success is the minimum.

### Algorithm
1. For `k` from `1` to `max(piles)`:
   - Compute `hours(k) = Σ ceil(piles[i] / k)`.
   - If `hours(k) <= h` → return `k`.

### Code

```cpp
class Solution {
public:
    int minEatingSpeed(vector<int>& piles, int h) {
        int hi = *max_element(piles.begin(), piles.end());
        for (int k = 1; k <= hi; k++) {
            long long hours = 0;
            for (int p : piles) hours += (p + k - 1) / k;   // ceil
            if (hours <= h) return k;
        }
        return hi;
    }
};
```
```java
class Solution {
    public int minEatingSpeed(int[] piles, int h) {
        int hi = 0;
        for (int p : piles) hi = Math.max(hi, p);
        for (int k = 1; k <= hi; k++) {
            long hours = 0;
            for (int p : piles) hours += (p + k - 1) / k;   // ceil
            if (hours <= h) return k;
        }
        return hi;
    }
}
```
```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        hi = max(piles)
        for k in range(1, hi + 1):
            hours = sum((p + k - 1) // k for p in piles)    # ceil
            if hours <= h:
                return k
        return hi
```

### Complexity
- **Time**: O(max(piles) · n) — up to `10^9 · 10^4` operations. **Will TLE badly.**
- **Space**: O(1).

### Verdict
Correct and demonstrates monotonicity, but the speed range is up to `10^9`, so a linear scan is hopeless. The monotonic false→true structure is exactly the invitation to binary search.

---

## Approach 2 — Binary search on the answer (optimal) ⭐

### Intuition
Replace the linear scan over `k` with a binary search over `[1, max(piles)]`. Define `feasible(k) = (hours(k) <= h)`. It's monotonic (false…false, true…true), so we search for the **leftmost** `k` where it's true.

We use the **converging template** `while (lo < hi)`:
- If `feasible(mid)` is true, the answer is `mid` or smaller → `hi = mid`.
- If false, we need to eat faster → `lo = mid + 1`.

When `lo == hi`, that's the smallest feasible speed.

### Algorithm
1. `lo = 1`, `hi = max(piles)`.
2. While `lo < hi`:
   - `mid = lo + (hi - lo) / 2`.
   - Compute `hours(mid) = Σ ceil(piles[i] / mid)`.
   - If `hours(mid) <= h` → `hi = mid` (this speed works; try slower).
   - Else → `lo = mid + 1` (too slow; speed up).
3. Return `lo`.

> ⚠️ Use a 64-bit accumulator for `hours`. With up to `10^4` piles each needing up to `10^9` hours at `k = 1`, the sum can reach `10^13`, which overflows 32-bit `int`.

### Dry run on `piles = [3,6,7,11]`, `h = 8`
```
max(piles) = 11 → lo=1, hi=11
  mid = 1 + (11-1)/2 = 6
    hours = ceil(3/6)+ceil(6/6)+ceil(7/6)+ceil(11/6) = 1+1+2+2 = 6 <= 8 → feasible → hi=6
lo=1, hi=6
  mid = 1 + (6-1)/2 = 3
    hours = 1+2+3+4 = 10 > 8 → not feasible → lo=4
lo=4, hi=6
  mid = 4 + (6-4)/2 = 5
    hours = ceil(3/5)+ceil(6/5)+ceil(7/5)+ceil(11/5) = 1+2+2+3 = 8 <= 8 → feasible → hi=5
lo=4, hi=5
  mid = 4 + (5-4)/2 = 4
    hours = ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 <= 8 → feasible → hi=4
lo=4, hi=4 → loop ends → return 4 ✅
```

### Code

```cpp
class Solution {
public:
    bool canFinish(vector<int>& piles, int k, int h) {
        long long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;   // ceil(p/k)
        return hours <= h;
    }
    int minEatingSpeed(vector<int>& piles, int h) {
        int lo = 1, hi = *max_element(piles.begin(), piles.end());
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (canFinish(piles, mid, h)) hi = mid;     // works → try slower
            else lo = mid + 1;                          // too slow → speed up
        }
        return lo;
    }
};
```
```java
class Solution {
    private boolean canFinish(int[] piles, int k, int h) {
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;   // ceil(p/k)
        return hours <= h;
    }
    public int minEatingSpeed(int[] piles, int h) {
        int lo = 1, hi = 0;
        for (int p : piles) hi = Math.max(hi, p);
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (canFinish(piles, mid, h)) hi = mid;     // works → try slower
            else lo = mid + 1;                          // too slow → speed up
        }
        return lo;
    }
}
```
```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def can_finish(k: int) -> bool:
            hours = sum((p + k - 1) // k for p in piles)  # ceil(p/k)
            return hours <= h

        lo, hi = 1, max(piles)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if can_finish(mid):
                hi = mid          # works → try slower
            else:
                lo = mid + 1      # too slow → speed up
        return lo
```

### Complexity
- **Time**: O(n · log(max(piles))) — each feasibility check is O(n), and we do O(log(max(piles))) of them. For the constraints, ~`10^4 · 30 ≈ 3·10^5` operations.
- **Space**: O(1).

### Verdict
**The optimal answer.** The pattern to internalize: *"minimize/maximize a value subject to a monotonic feasibility test → binary search the answer range, not the array."*

---

## ⚖️ Approach comparison

| Approach | Time | Space | Feasible for constraints | When to mention |
|----------|------|-------|--------------------------|-----------------|
| Linear scan over k | O(max(piles)·n) | O(1) | no (TLE) | only to establish monotonicity |
| Binary search on answer | **O(n·log(max(piles)))** | O(1) | yes | the optimal answer ⭐ |

The deciding insight: the answer space is huge (up to `10^9`) but **monotonic**, so we binary search it. Recognizing "smallest/largest X such that a monotonic condition holds" is the signal for this pattern.

---

## 🧪 Edge cases & pitfalls
- **`h == piles.length`** → exactly one hour per pile → answer is `max(piles)` (she must clear the biggest pile in one hour). Example 2.
- **Single pile** → answer is `ceil(piles[0] / h)`; the binary search still finds it.
- **Overflow pitfall** ⚠️ — the hour-sum can reach ~`10^13`. Use `long`/`long long` for the accumulator in C++ and Java. Python is immune but the logic is the same.
- **Ceiling pitfall** — compute `ceil(p / k)` as `(p + k - 1) / k` with integer division, not floating-point `math.ceil(p / k)`, which can misbehave on large values. (Python's `(p + k - 1) // k` is exact.)
- **Lower bound of 0** — never set `lo = 0`; speed 0 means she eats nothing and divides by zero. Start at `1`.
- **Template pitfall** — with `while (lo < hi)` you must set `hi = mid` (not `mid - 1`) on success, otherwise you can skip the true boundary.

---

## 🔗 Related problems
- **Capacity To Ship Packages Within D Days** (LC 1011) — same pattern: minimize capacity with a monotonic day-count test.
- **Split Array Largest Sum** (LC 410) — minimize the largest subarray sum; binary search on the answer.
- **Minimum Number of Days to Make m Bouquets** (LC 1482) — monotonic feasibility on days.
- **Find the Smallest Divisor Given a Threshold** (LC 1283) — nearly identical ceil-sum structure.

---

**→ Next:** [`04-Find-Minimum-Rotated-Sorted-Array.md`](./04-Find-Minimum-Rotated-Sorted-Array.md) | **→ Prev:** [`02-Search-2D-Matrix.md`](./02-Search-2D-Matrix.md) | [Problem set index](./00-Index.md)
