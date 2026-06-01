# Median of Two Sorted Arrays

**Platform**: LeetCode 4 · **Difficulty**: Hard · **Topics**: Array, Binary Search, Divide and Conquer · **Pattern**: Binary search on a partition

---

## 📜 Problem Statement

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the **median** of the two sorted arrays.

The overall run time complexity should be **O(log (m+n))**.

### Examples

**Example 1:**
```
Input:  nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

**Example 2:**
```
Input:  nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

**Example 3:**
```
Input:  nums1 = [], nums2 = [1]
Output: 1.00000
Explanation: only one element; it is the median.
```

### Constraints
```
nums1.length == m
nums2.length == n
0 <= m <= 1000
0 <= n <= 1000
1 <= m + n <= 2000
-10^6 <= nums1[i], nums2[i] <= 10^6
```

---

## 🧠 Understanding the problem

The **median** of a combined collection of `m + n` numbers is the value that splits the sorted union into two equal halves:

- If `m + n` is **odd**, it's the single middle element.
- If `m + n` is **even**, it's the average of the two middle elements.

The naive idea is to merge both arrays and look at the middle, but the problem demands **O(log(m+n))**, which forbids building the full merged array (that's O(m+n)). So we need a logarithmic idea.

The key reframing: **we don't need to merge — we only need a correct partition.** Imagine cutting the combined sorted array into a **left part** and a **right part** of equal size (left gets the extra element when the total is odd). If we knew where to cut each individual array so the pieces line up, the median would come from the four elements *around the cut*:

```
left part                 |  right part
... maxLeft1, maxLeft2     |  minRight1, minRight2 ...
```

A partition is **correct** when every element on the left is `<=` every element on the right. Because each array is already sorted, that reduces to just two cross-checks:

```
maxLeft1 <= minRight2   AND   maxLeft2 <= minRight1
```

Here's the leap: **if I choose how many elements of `nums1` go to the left (call it `i`), then the count from `nums2` is forced** — it must be `half - i` so the left part has exactly half the total. So there is only **one free variable**, `i`, and it ranges over `[0, m]`. We **binary search `i`** to find the partition that satisfies the cross-check. That's O(log m), and by always binary-searching the **smaller** array, it's O(log(min(m, n))) ⊆ O(log(m+n)).

---

## Approach 1 — Merge fully, then take the middle (baseline)

### Intuition
Merge the two sorted arrays into one (like the merge step of merge sort), then read off the median by index.

### Algorithm
1. Two-pointer merge `nums1` and `nums2` into `merged`.
2. If `m + n` is odd → return `merged[(m+n)/2]`.
3. Else → return the average of `merged[(m+n)/2 - 1]` and `merged[(m+n)/2]`.

### Code

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size(), n = nums2.size();
        vector<int> merged;
        merged.reserve(m + n);
        int i = 0, j = 0;
        while (i < m && j < n)
            merged.push_back(nums1[i] <= nums2[j] ? nums1[i++] : nums2[j++]);
        while (i < m) merged.push_back(nums1[i++]);
        while (j < n) merged.push_back(nums2[j++]);
        int total = m + n;
        if (total % 2) return merged[total / 2];
        return (merged[total / 2 - 1] + merged[total / 2]) / 2.0;
    }
};
```
```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length, n = nums2.length;
        int[] merged = new int[m + n];
        int i = 0, j = 0, k = 0;
        while (i < m && j < n)
            merged[k++] = (nums1[i] <= nums2[j]) ? nums1[i++] : nums2[j++];
        while (i < m) merged[k++] = nums1[i++];
        while (j < n) merged[k++] = nums2[j++];
        int total = m + n;
        if (total % 2 == 1) return merged[total / 2];
        return (merged[total / 2 - 1] + merged[total / 2]) / 2.0;
    }
}
```
```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = []
        i = j = 0
        m, n = len(nums1), len(nums2)
        while i < m and j < n:
            if nums1[i] <= nums2[j]:
                merged.append(nums1[i]); i += 1
            else:
                merged.append(nums2[j]); j += 1
        merged.extend(nums1[i:])
        merged.extend(nums2[j:])
        total = m + n
        if total % 2:
            return merged[total // 2]
        return (merged[total // 2 - 1] + merged[total // 2]) / 2.0
```

### Complexity
- **Time**: O(m + n) — builds the whole merged array.
- **Space**: O(m + n) for the merged array.

### Verdict
Correct and easy to reason about, but it **violates the required O(log(m+n))**. It's a great correctness oracle to test the optimal solution against, and many interviewers accept it as a warm-up before asking for the log solution.

---

## Approach 2 — Merge halfway (no extra array)

### Intuition
We don't need the whole merged array — only the element(s) at the middle. Walk the merge `(m+n)/2 + 1` steps, remembering the last two values seen. This removes the O(m+n) space but is still O(m+n) time.

### Algorithm
1. Advance two pointers as in a merge, counting steps up to `(m+n)/2`.
2. Track `prev` and `curr` (the values at the two central positions).
3. Combine them based on parity of `m + n`.

### Code

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size(), n = nums2.size(), total = m + n;
        int i = 0, j = 0;
        int prev = 0, curr = 0;
        for (int count = 0; count <= total / 2; count++) {
            prev = curr;
            if (i < m && (j >= n || nums1[i] <= nums2[j])) curr = nums1[i++];
            else curr = nums2[j++];
        }
        if (total % 2) return curr;
        return (prev + curr) / 2.0;
    }
};
```
```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length, n = nums2.length, total = m + n;
        int i = 0, j = 0, prev = 0, curr = 0;
        for (int count = 0; count <= total / 2; count++) {
            prev = curr;
            if (i < m && (j >= n || nums1[i] <= nums2[j])) curr = nums1[i++];
            else curr = nums2[j++];
        }
        if (total % 2 == 1) return curr;
        return (prev + curr) / 2.0;
    }
}
```
```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        m, n = len(nums1), len(nums2)
        total = m + n
        i = j = 0
        prev = curr = 0
        for _ in range(total // 2 + 1):
            prev = curr
            if i < m and (j >= n or nums1[i] <= nums2[j]):
                curr = nums1[i]; i += 1
            else:
                curr = nums2[j]; j += 1
        if total % 2:
            return curr
        return (prev + curr) / 2.0
```

### Complexity
- **Time**: O(m + n) — still linear (we walk halfway).
- **Space**: O(1) — no merged array.

### Verdict
Better space, same time class. Still **doesn't meet O(log(m+n))**, but it's a clean intermediate step that shows we only care about the middle elements — which motivates the partition idea.

---

## Approach 3 — Partition binary search (optimal) ⭐

### Intuition
Binary search the cut position `i` in the **smaller** array. The cut in the other array is forced to `j = half - i` so the combined left part holds exactly `half = (m + n + 1) / 2` elements (the `+1` puts the extra element on the left for odd totals, which lets us handle both parities uniformly).

Define the four boundary values around the cuts, using `±∞` sentinels when a cut sits at an array edge:
```
Aleft  = (i == 0) ? -inf : A[i-1]      Aright = (i == m) ? +inf : A[i]
Bleft  = (j == 0) ? -inf : B[j-1]      Bright = (j == n) ? +inf : B[j]
```
The partition is correct when `Aleft <= Bright` **and** `Bleft <= Aright`. If `Aleft > Bright`, we took too many from A → move the cut left (`hi = i - 1`). If `Bleft > Aright`, we took too few from A → move right (`lo = i + 1`).

Once correct:
- **Odd total** → median = `max(Aleft, Bleft)` (the largest element on the left).
- **Even total** → median = `(max(Aleft, Bleft) + min(Aright, Bright)) / 2`.

### Algorithm
1. Ensure `A` is the smaller array (swap if needed) so we binary search the shorter one.
2. `half = (m + n + 1) / 2`; `lo = 0`, `hi = m`.
3. While `lo <= hi`:
   - `i = (lo + hi) / 2`, `j = half - i`.
   - Compute the four boundary values with sentinels.
   - If `Aleft <= Bright && Bleft <= Aright` → correct partition; return median by parity.
   - Else if `Aleft > Bright` → `hi = i - 1`.
   - Else → `lo = i + 1`.

### Dry run on `A = [1,3]` (smaller), `B = [2]`
```
m = 2, n = 1, total = 3 (odd), half = (2+1+1)/2 = 2
lo=0, hi=2
  i = (0+2)/2 = 1, j = half - i = 2 - 1 = 1
    Aleft  = A[0] = 1     Aright = A[1] = 3
    Bleft  = B[0] = 2     Bright = (j==n=1) → +inf
    check: Aleft(1) <= Bright(+inf) ✅  AND  Bleft(2) <= Aright(3) ✅  → correct!
  odd total → median = max(Aleft, Bleft) = max(1, 2) = 2 ✅
```

A second dry run on `A = [1,2]`, `B = [3,4]` (already smaller-or-equal, no swap needed since equal size):
```
m = 2, n = 2, total = 4 (even), half = (2+2+1)/2 = 2
lo=0, hi=2
  i = 1, j = 1
    Aleft = A[0] = 1   Aright = A[1] = 2
    Bleft = B[0] = 3   Bright = B[1] = 4
    check: Aleft(1) <= Bright(4) ✅  AND  Bleft(3) <= Aright(2)? ❌  (3 > 2)
    Bleft > Aright → took too few from A → lo = i + 1 = 2
  i = 2, j = 0
    Aleft = A[1] = 2   Aright = (i==m=2) → +inf
    Bleft = (j==0) → -inf   Bright = B[0] = 3
    check: Aleft(2) <= Bright(3) ✅  AND  Bleft(-inf) <= Aright(+inf) ✅ → correct!
  even total → (max(Aleft,Bleft) + min(Aright,Bright)) / 2
             = (max(2,-inf) + min(+inf,3)) / 2 = (2 + 3) / 2 = 2.5 ✅
```

### Code

```cpp
class Solution {
public:
    double findMedianSortedArrays(vector<int>& A, vector<int>& B) {
        if (A.size() > B.size()) swap(A, B);          // binary search the smaller
        int m = A.size(), n = B.size();
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            int i = (lo + hi) / 2;                    // cut in A
            int j = half - i;                         // cut in B
            int Aleft  = (i == 0) ? INT_MIN : A[i-1];
            int Aright = (i == m) ? INT_MAX : A[i];
            int Bleft  = (j == 0) ? INT_MIN : B[j-1];
            int Bright = (j == n) ? INT_MAX : B[j];
            if (Aleft <= Bright && Bleft <= Aright) {
                if ((m + n) % 2) return max(Aleft, Bleft);
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2.0;
            } else if (Aleft > Bright) {
                hi = i - 1;                           // too many from A → cut left
            } else {
                lo = i + 1;                           // too few from A → cut right
            }
        }
        return 0.0;                                   // unreachable for valid input
    }
};
```
```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int[] A = nums1, B = nums2;
        if (A.length > B.length) { int[] t = A; A = B; B = t; }  // search smaller
        int m = A.length, n = B.length;
        int half = (m + n + 1) / 2;
        int lo = 0, hi = m;
        while (lo <= hi) {
            int i = (lo + hi) / 2;                   // cut in A
            int j = half - i;                        // cut in B
            int Aleft  = (i == 0) ? Integer.MIN_VALUE : A[i-1];
            int Aright = (i == m) ? Integer.MAX_VALUE : A[i];
            int Bleft  = (j == 0) ? Integer.MIN_VALUE : B[j-1];
            int Bright = (j == n) ? Integer.MAX_VALUE : B[j];
            if (Aleft <= Bright && Bleft <= Aright) {
                if ((m + n) % 2 == 1) return Math.max(Aleft, Bleft);
                return (Math.max(Aleft, Bleft) + Math.min(Aright, Bright)) / 2.0;
            } else if (Aleft > Bright) {
                hi = i - 1;
            } else {
                lo = i + 1;
            }
        }
        return 0.0;
    }
}
```
```python
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        if len(A) > len(B):
            A, B = B, A                              # binary search the smaller
        m, n = len(A), len(B)
        half = (m + n + 1) // 2
        lo, hi = 0, m
        while lo <= hi:
            i = (lo + hi) // 2                       # cut in A
            j = half - i                             # cut in B
            Aleft  = float('-inf') if i == 0 else A[i-1]
            Aright = float('inf')  if i == m else A[i]
            Bleft  = float('-inf') if j == 0 else B[j-1]
            Bright = float('inf')  if j == n else B[j]
            if Aleft <= Bright and Bleft <= Aright:
                if (m + n) % 2:
                    return max(Aleft, Bleft)
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2.0
            elif Aleft > Bright:
                hi = i - 1                           # too many from A → cut left
            else:
                lo = i + 1                           # too few from A → cut right
        return 0.0
```

### Complexity
- **Time**: O(log(min(m, n))) — we binary search only the smaller array's cut position. This is within O(log(m+n)).
- **Space**: O(1).

### Verdict
**The optimal answer** and the one the problem demands. It's the hardest binary search in this set because you search over *partitions*, not values. The two ideas to lock in: (1) fixing `i` forces `j = half - i`, and (2) correctness reduces to two cross-checks with `±∞` sentinels at the edges.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Meets O(log(m+n)) | When to mention |
|----------|------|-------|-------------------|-----------------|
| Full merge | O(m+n) | O(m+n) | no | warm-up / correctness oracle |
| Merge halfway | O(m+n) | O(1) | no | shows only the middle matters |
| Partition binary search | **O(log(min(m,n)))** | O(1) | yes | the required optimal answer ⭐ |

The progression mirrors the insight chain: *merge everything → realize you only need the middle → realize you only need the right partition, which you can binary search.*

---

## 🧪 Edge cases & pitfalls
- **One array empty** (`A = []`) → after the swap `A` is the smaller (possibly empty), `m = 0`, the loop runs once with `i = 0`, and the sentinels make the answer come entirely from `B`. Handled.
- **All of one array below the other** (`A = [1,2]`, `B = [10,20]`) → the binary search drives the cut to an edge; `±∞` sentinels keep the comparisons valid.
- **Odd vs even total** → `half = (m + n + 1) / 2` puts the extra element on the left for odd totals, so odd uses `max(Aleft, Bleft)` and even averages across the cut. Getting this `+1` right is the crux.
- **Pitfall — not searching the smaller array**: `j = half - i` can go out of bounds if `A` is the larger array. Always swap so `m <= n`.
- **Pitfall — overflow / sentinels**: use `INT_MIN`/`INT_MAX` (C++), `Integer.MIN_VALUE`/`MAX_VALUE` (Java), `±inf` (Python) for out-of-range cuts. Don't read `A[-1]` or `A[m]`.
- **Pitfall — integer division for the average**: return a `double` (`/ 2.0`), not integer division, or even-length medians like `2.5` will truncate to `2`.
- **Pitfall — `while (lo <= hi)` vs `< `**: here we use `<=` because `i` can legitimately equal `0` or `m` (a cut at either edge), and we must allow `hi` to reach those.

---

## 🔗 Related problems
- **Median of Two Sorted Arrays** generalization → **Kth Smallest Element in Two Sorted Arrays** — the same partition idea for an arbitrary `k`.
- **Find K-th Smallest Pair Distance** (LC 719) — binary search on the answer with a counting check.
- **Merge Sorted Array** (LC 88) — the linear merge underlying Approaches 1 and 2.
- **Kth Smallest Element in a Sorted Matrix** (LC 378) — partition / binary-search-on-value cousin.

---

**→ Prev:** [`06-Time-Based-Key-Value-Store.md`](./06-Time-Based-Key-Value-Store.md) | [Problem set index](./00-Index.md)
