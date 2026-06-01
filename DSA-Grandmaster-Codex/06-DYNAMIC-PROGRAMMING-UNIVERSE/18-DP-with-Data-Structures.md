# 🧬 DP with Data Structures

> *"When a DP transition queries a range of previous states, a data structure makes it fast."*

---

## I. THE IDEA
Many DPs have transitions like:
```
dp[i] = (best / sum) over j in some RANGE of (dp[j] + f(i, j))
```
A linear scan of the range makes this O(n²). A **data structure** that supports range queries turns it into O(n log n).

---

## II. THE TOOLBOX

### Prefix sums (range-sum transitions) → O(1) per transition
When `dp[i] = Σ dp[j]` over a contiguous range, maintain a running prefix sum.
- Example: counting-paths DPs, "ways to reach with sum in window."

### Fenwick (BIT) / Segment Tree by VALUE → O(log n) per transition
When the transition is "best dp[j] among j with value < a[i]" (not index range).
- **LIS in O(n log n)**: coordinate-compress values; segment tree stores max dp over value ranges; query max over values < a[i], then update.
- **Count of smaller/greater with DP**.

### Segment Tree by INDEX → range max/min/sum of dp
When `dp[i] = max(dp[j]) + c` over an index window or arbitrary range.

### Monotonic deque → sliding-window min/max
When the range is a fixed sliding window [i−k, i−1]. O(n). (See [`15-DP-Optimizations.md`](./15-DP-Optimizations.md).)

### Multiset / ordered set → nearest / kth element transitions
When you need "closest previous value" or order statistics among prior states.

### Convex Hull Trick / Li Chao → linear-function transitions
When `dp[i] = min(m[j]·x[i] + b[j])`. (See [`15-DP-Optimizations.md`](./15-DP-Optimizations.md).)

---

## III. WORKED EXAMPLE: LIS in O(n log n) via Segment Tree
```
1. Compress values of a[] to ranks 1..n.
2. Segment tree over ranks storing max LIS length.
3. For each element (left to right):
     best = query max over ranks [1, rank(a[i]) - 1]
     dp[i] = best + 1
     update segment tree at rank(a[i]) with dp[i]
4. Answer = global max.
```
This generalizes to LIS variants with extra constraints (where patience-sorting doesn't directly apply).

---

## IV. WORKED EXAMPLE: Counting DP with prefix sums
"Number of ways to reach state i = sum of ways over a range of previous states" → maintain a prefix-sum array of dp so each transition is O(1).
- Example: New 21 Game (LC 837), some path-counting DPs.

---

## V. RECOGNITION ⭐
The signal: your DP recurrence has **"over all j with (some range condition)"** in it. Ask:
- Range over INDEX? → segment tree / BIT / sliding-window deque / prefix sum
- Range over VALUE? → coordinate-compress + segment tree / BIT by value
- "Linear function of i"? → CHT / Li Chao
- Fixed sliding window? → monotonic deque

---

## VI. COMPLEXITY
- O(n²) → O(n log n) with a tree/BIT.
- O(n²) → O(n) with prefix sums or monotonic deque (when applicable).

---

## VII. PROBLEMS
- LIS variants (300, and harder constrained versions)
- Number of Longest Increasing Subsequence (673) — with counts in a BIT
- Constrained Subsequence Sum (1425) — deque
- New 21 Game (837) — prefix sums
- Russian Doll Envelopes (354) — sort + LIS (BIT/patience)
- CF problems "dp + data structures"

---

## VIII. NOTE
This is where DP meets the Data Structures Universe. Mastering both unlocks the hardest DP problems on [Codeforces](https://codeforces.com) and in senior FAANG interviews.

Cross-reference: [`../04-DATA-STRUCTURES-UNIVERSE/26-Segment-Tree.md`](../04-DATA-STRUCTURES-UNIVERSE/26-Segment-Tree.md), [`../04-DATA-STRUCTURES-UNIVERSE/COMPENDIUM-Heaps-And-Range.md`](../04-DATA-STRUCTURES-UNIVERSE/COMPENDIUM-Heaps-And-Range.md)

---

**→ Next:** [`19-DP-Cheatsheet.md`](./19-DP-Cheatsheet.md) (see [`COMPENDIUM-Classical-DP.md`](./COMPENDIUM-Classical-DP.md) §19-20)
