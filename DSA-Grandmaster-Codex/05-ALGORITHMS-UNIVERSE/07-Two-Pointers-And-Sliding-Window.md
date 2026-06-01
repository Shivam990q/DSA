# 🎯 Two Pointers & Sliding Window

> *"Two indices, moving with purpose, turn O(n²) into O(n)."*

---

## I. TWO POINTERS (opposite ends)
For sorted arrays / palindromes / pair problems: start at both ends, move inward based on a condition.
```cpp
int l = 0, r = n - 1;
while (l < r) {
    if (a[l] + a[r] == target) { /* found */ l++; r--; }
    else if (a[l] + a[r] < target) l++;   // need bigger
    else r--;                              // need smaller
}
```
- **Why it works**: sortedness gives monotonicity — moving a pointer provably can't skip a valid answer.

---

## II. TWO POINTERS (same direction = sliding window)
A window [l, r] expands by moving r; shrinks by moving l when a constraint is violated.
```cpp
int l = 0;
for (int r = 0; r < n; r++) {
    add(a[r]);                       // expand
    while (windowInvalid()) remove(a[l++]);  // shrink until valid
    ans = max(ans, r - l + 1);       // record (size / sum / count)
}
```

---

## III. FIXED vs VARIABLE WINDOW
- **Fixed size k**: slide a window of constant width (e.g., max sum of k consecutive). Add a[r], remove a[r-k].
- **Variable size**: grow/shrink based on a constraint (e.g., longest substring with ≤ k distinct).

---

## IV. THE MONOTONICITY REQUIREMENT ⭐
Sliding window works **only when the validity predicate is monotonic** in window size: once a window is invalid, extending it further (without shrinking) keeps it invalid. This lets `l` only move forward. If not monotonic, sliding window fails (need different approach).

---

## V. THE "AT MOST K" TRICK
For "exactly K" problems, compute **atMost(K) − atMost(K−1)**. Counting windows with "exactly K distinct" directly is awkward; "at most" is a clean sliding window.
- Subarrays with K Different Integers (LC 992), Count Nice Subarrays (LC 1248).

---

## VI. CLASSIC PROBLEMS
### Two pointers (opposite)
- Two Sum II (167), 3Sum (15), Container With Most Water (11), Trapping Rain Water (42), Valid Palindrome (125), Sort Colors (75)

### Sliding window (variable)
- Longest Substring Without Repeating (3) ⭐
- Minimum Window Substring (76) ⭐⭐
- Longest Repeating Character Replacement (424)
- Longest Substring with At Most K Distinct (340)
- Minimum Size Subarray Sum (209)
- Fruit Into Baskets (904), Permutation in String (567), Find All Anagrams (438)

### Fixed window
- Maximum Average Subarray (643), Sliding Window Maximum (239 — uses monotonic deque)

---

## VII. THE DECISION GUIDE
| Signal | Technique |
|--------|-----------|
| sorted array + pair/triplet | two pointers (opposite) |
| "contiguous subarray/substring with constraint" | sliding window |
| "longest/shortest window such that..." | variable window |
| "window of size exactly k" | fixed window |
| "exactly K distinct/odd/..." | atMost(K) − atMost(K−1) |
| window max/min | monotonic deque (see [`COMPENDIUM-Advanced-Algorithms.md`](./COMPENDIUM-Advanced-Algorithms.md) §07) |

---

## VIII. COMPLEXITY
O(n) — each pointer traverses the array at most once. The inner `while` doesn't make it O(n²) because `l` only moves forward total n times.

---

## IX. PROBLEMS
LC 3, 11, 15, 16, 26, 27, 42, 75, 76, 125, 167, 209, 239, 340, 424, 438, 567, 643, 713, 904, 992, 1004, 1248, 1493

---

**→ Next:** [`08-Bit-Manipulation.md`](./08-Bit-Manipulation.md) | All paradigms → [`COMPENDIUM-Advanced-Algorithms.md`](./COMPENDIUM-Advanced-Algorithms.md)
