# 🔍 Searching Algorithms

> *"To search is to bisect ignorance."*

---

## I. LINEAR SEARCH — O(n)

The brute force. Examine each element until target found.

```cpp
int linearSearch(vector<int>& a, int x) {
    for (int i = 0; i < a.size(); i++)
        if (a[i] == x) return i;
    return -1;
}
```

When to use: unsorted, small data, or single search.

---

## II. BINARY SEARCH — O(log n)

For **sorted** arrays.

### Classic
```cpp
int binarySearch(vector<int>& a, int x) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;  // avoid overflow
        if (a[mid] == x) return mid;
        else if (a[mid] < x) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}
```

### Lower bound (first index where a[i] ≥ x)
```cpp
int lowerBound(vector<int>& a, int x) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

### Upper bound (first index where a[i] > x)
```cpp
int upperBound(vector<int>& a, int x) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
```

### C++ STL
- `lower_bound(a.begin(), a.end(), x)`
- `upper_bound(a.begin(), a.end(), x)`
- `binary_search(a.begin(), a.end(), x)` (returns bool)

---

## III. BINARY SEARCH ON ANSWER

The most powerful pattern. When you have a **monotonic predicate** `feasible(x)`:

```cpp
int searchAnswer() {
    int lo = MIN_X, hi = MAX_X;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (feasible(mid)) hi = mid;     // smallest feasible
        else lo = mid + 1;
    }
    return lo;
}
```

### Examples
- **Koko eating bananas (LC 875)**: smallest k such that she can finish in H hours.
- **Capacity to ship (LC 1011)**: smallest capacity such that all packages ship in D days.
- **Aggressive cows**: maximum minimum distance.
- **Allocate minimum pages**.
- **Median of two sorted arrays** (with smart bisection).

---

## IV. TERNARY SEARCH — O(log n)

For **unimodal** functions (one peak / one valley) on continuous or discrete domain.

```cpp
double ternarySearch(double lo, double hi, function<double(double)> f) {
    for (int iter = 0; iter < 200; iter++) {
        double m1 = lo + (hi - lo) / 3;
        double m2 = hi - (hi - lo) / 3;
        if (f(m1) < f(m2)) lo = m1;
        else hi = m2;
    }
    return (lo + hi) / 2;
}
```

### Use case
Maximize a downward parabola on a range; minimize convex function.

---

## V. EXPONENTIAL / GALLOPING SEARCH — O(log p) where p is target position

For unbounded sorted streams or when target is near start.

```
Step 1: find range [2^(k-1), 2^k] containing target by doubling
Step 2: binary search within that range
```

---

## VI. INTERPOLATION SEARCH — O(log log n) for uniform distribution

Linearly interpolate the next probe rather than midpoint.

For uniformly distributed sorted data, much faster than binary search. For adversarial data, can degrade to O(n).

```cpp
int pos = lo + ((double)(x - a[lo]) / (a[hi] - a[lo])) * (hi - lo);
```

---

## VII. JUMP SEARCH — O(√n)

Jump in steps of √n; once you overshoot, linear-search backward. Useful when binary search is too random-access (some external storage).

---

## VIII. SEARCH IN ROTATED SORTED ARRAY

Two-step BS:
1. Find pivot (rotation point).
2. BS in the appropriate half.

Or: smart unified BS that handles both cases.

```cpp
int search(vector<int>& a, int target) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {  // left half sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {  // right half sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}
```

---

## IX. PROBLEMS

1. Binary search (LC 704)
2. Search insert position (LC 35)
3. First & last position (LC 34)
4. Search in rotated sorted array (LC 33, 81)
5. Find minimum in rotated array (LC 153, 154)
6. Find peak element (LC 162)
7. Median of two sorted arrays (LC 4) ⭐
8. Capacity to ship (LC 1011)
9. Koko eating bananas (LC 875)
10. Split array largest sum (LC 410)
11. Aggressive cows ([SPOJ](https://www.spoj.com))
12. Allocate min pages (GFG)
13. Find Kth missing positive (LC 1539)
14. Search a 2D matrix I, II (LC 74, 240)
15. Minimum days to make M bouquets (LC 1482)
16. Find smallest divisor (LC 1283)
17. Painter's partition problem
18. Magnetic force between balls (LC 1552)
19. Swim in rising water (LC 778) — BS + DSU/BFS
20. Online median

---

**→ Next:** [`02-Sorting.md`](./02-Sorting.md)
