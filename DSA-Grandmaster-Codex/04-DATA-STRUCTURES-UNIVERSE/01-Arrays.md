# 🪨 Arrays — The Atomic Data Structure

> *"Every advanced data structure is, at the bottom, an array dressed up."*

---

## I. WHAT IS AN ARRAY?

A **contiguous block of memory** holding fixed-type elements, accessed by index in O(1).

```
Index:  0    1    2    3    4
Array: [10] [20] [30] [40] [50]
Addr:  100  104  108  112  116    (assuming 4-byte ints)
```

`a[i]` = memory at address `base + i × sizeof(element)` → constant-time access.

---

## II. STATIC vs DYNAMIC

### Static array (C-style, fixed size)
- Size known at compile time (or stack-allocated at function entry)
- Cannot grow
- Fastest: zero overhead

```c
int a[100];     // C, fixed
```

### Dynamic array (vector / list / ArrayList)
- Resizable
- Stores capacity + size + pointer to data
- Amortized O(1) push_back via doubling

```cpp
vector<int> v;          // C++ STL
v.push_back(5);         // O(1) amortized
v[i] = 7;               // O(1)
```

```python
a = []                  # Python list (dynamic array)
a.append(5)             # O(1) amortized
a[i] = 7                # O(1)
```

---

## III. AMORTIZED ANALYSIS OF DYNAMIC ARRAY

When a dynamic array runs out of capacity, it allocates a new block (typically 2× size), copies, frees the old.

- Most pushes: O(1)
- Resize push: O(n) (copy)
- Total cost over n pushes: O(n) (geometric series)
- **Amortized**: O(1) per push.

This is **why Python's `list.append` and C++ `vector::push_back` are O(1) amortized despite occasional O(n) ops.**

---

## IV. OPERATIONS COMPLEXITY

| Operation               | Static | Dynamic | Notes                               |
|-------------------------|--------|---------|-------------------------------------|
| Access `a[i]`           | O(1)   | O(1)    |                                     |
| Update `a[i] = x`       | O(1)   | O(1)    |                                     |
| Push back               | N/A    | O(1) amortized | occasional resize             |
| Pop back                | N/A    | O(1)    |                                     |
| Push/pop front          | O(n)   | O(n)    | shifts all elements (use deque!)    |
| Insert at index k       | O(n)   | O(n)    | shifts                              |
| Delete at index k       | O(n)   | O(n)    | shifts                              |
| Search (unsorted)       | O(n)   | O(n)    |                                     |
| Search (sorted)         | O(log n) | O(log n) | binary search                  |
| Sort                    | O(n log n) | O(n log n) | comparison-based sort         |

---

## V. MEMORY LAYOUT & CACHE

Arrays are **cache-friendly**: iterating sequentially reads cache lines efficiently.

```cpp
for (int i = 0; i < n; i++) sum += a[i];   // CACHE-FRIENDLY
```

Linked lists are NOT cache-friendly (each node is a pointer chase).

**Implication**: even when both have the same Big-O, an array implementation can be 5-20× faster.

---

## VI. MULTI-DIMENSIONAL ARRAYS

### True 2D (contiguous)
```cpp
int a[N][M];  // n*m contiguous ints
```
Layout: row-major in C/C++/Java. `a[i][j]` at `base + (i*M + j) * sizeof(int)`.

### Array of arrays (jagged)
```cpp
vector<vector<int>> a(n);  // each row is a separate dynamic array
```
Each row is independently allocated; rows can have different lengths.

**Performance**: contiguous 2D is cache-friendlier; jagged is more flexible.

### Iteration order matters
```cpp
// FAST (row-major iteration on row-major storage)
for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        sum += a[i][j];

// SLOW (column-major iteration on row-major storage — cache misses)
for (int j = 0; j < m; j++)
    for (int i = 0; i < n; i++)
        sum += a[i][j];
```

For n=m=1000, column-major can be 5-10× slower than row-major.

---

## VII. ESSENTIAL OPERATIONS PATTERNS

### Pattern 1: **Two pointers**
```cpp
int l = 0, r = n - 1;
while (l < r) { /* ... */ l++; r--; }
```

### Pattern 2: **Sliding window**
```cpp
int l = 0;
for (int r = 0; r < n; r++) {
    // expand window
    while (window_invalid()) shrink_window(l++);
    record(l, r);
}
```

### Pattern 3: **Prefix sum**
```cpp
vector<long long> P(n + 1, 0);
for (int i = 0; i < n; i++) P[i+1] = P[i] + a[i];
// range sum [l, r]: P[r+1] - P[l]
```

### Pattern 4: **Difference array** (range updates, point queries)
```cpp
vector<long long> D(n + 1, 0);
// add x to range [l, r]:
D[l] += x;
D[r+1] -= x;
// final array: prefix sum of D
```

### Pattern 5: **In-place reverse**
```cpp
void reverse(vector<int>& a) {
    int l = 0, r = a.size() - 1;
    while (l < r) swap(a[l++], a[r--]);
}
```

### Pattern 6: **Rotate**
```cpp
void rotate(vector<int>& a, int k) {
    k %= a.size();
    reverse(a.begin(), a.end());
    reverse(a.begin(), a.begin() + k);
    reverse(a.begin() + k, a.end());
}
```

---

## VIII. INTERVIEW PROBLEMS (TOP 30)

1. Two Sum
2. Best Time to Buy and Sell Stock
3. Maximum Subarray (Kadane)
4. Container With Most Water
5. Trapping Rain Water
6. 3Sum
7. 4Sum
8. Move Zeroes
9. Remove Duplicates from Sorted Array
10. Sort Colors (Dutch flag)
11. Merge Intervals
12. Insert Interval
13. Spiral Matrix
14. Set Matrix Zeroes
15. Rotate Image (matrix rotation)
16. Search a 2D Matrix
17. Word Search
18. Maximum Product Subarray
19. Find Minimum in Rotated Sorted Array
20. Search in Rotated Sorted Array
21. Median of Two Sorted Arrays
22. First Missing Positive
23. Subarray Sum Equals K
24. Longest Consecutive Sequence
25. Product of Array Except Self
26. Maximum Sum Circular Subarray
27. Find Pivot Index
28. Find All Duplicates in an Array
29. Set Mismatch
30. Largest Number

---

## IX. ARRAY TRICKS (THE CRAFT)

### Trick 1: Negate to mark visited
For arrays of positive integers, negating `a[abs(a[i]) - 1]` marks index as visited. (Used in finding duplicates.)

### Trick 2: XOR cancellation
`a ^ a = 0`, `a ^ 0 = a`. Find single non-duplicate element by XORing all.

### Trick 3: Cycle finding in array (Floyd's)
For arrays where `a[i]` is in [0, n-1], treat as a function; find cycle with slow/fast pointers.

### Trick 4: In-place hash by index
For "find missing in 1..n," use the array itself as a hash by negating or swapping.

### Trick 5: Boyer-Moore voting
For finding majority element (appears >n/2 times) in O(n) time and O(1) space.

---

## X. PYTHON / JAVA / C++ SPECIFICS

### Python list
- Dynamic array of `PyObject*` pointers
- `.append`: O(1) amortized
- `arr[i]`: O(1) but with object overhead
- Slicing `arr[l:r]`: O(r-l), creates new list

### Java
- `int[]` for primitives (contiguous memory)
- `Integer[]` for boxed (each int is heap-allocated)
- `ArrayList<Integer>` is `Integer[]` underneath
- For perf: prefer `int[]` if possible

### C++
- `int a[N]`: C-style, stack
- `vector<int>`: dynamic, heap-allocated, cache-friendly
- `array<int, N>`: fixed-size, stack, modern wrapper

---

## XI. TEMPLATES

Reusable array patterns (prefix sum, difference array, two pointers, sliding window, rotate, in-place reverse) are all implemented in Section VII above. For the broader CP template library (segment tree, BIT, DSU, etc.), see [`../19-TEMPLATES-AND-IMPLEMENTATIONS/`](../19-TEMPLATES-AND-IMPLEMENTATIONS/).

---

## XII. RECOMMENDED PROBLEMS

- [LeetCode](https://leetcode.com) Top 100 Liked → 30+ array problems
- Striver A2Z Array Track
- [CSES](https://cses.fi/problemset/) "Sorting and Searching" section

---

**→ Next:** Strings, Linked Lists, Stacks, Queues, Deques → [`COMPENDIUM-Linear-Structures.md`](./COMPENDIUM-Linear-Structures.md)
