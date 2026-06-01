# 🔢 Sorting Algorithms

> *"Sorting is the most-studied problem in computer science. Master it, master order itself."*

---

## I. THE SORTING ZOO

| Algorithm        | Best     | Avg      | Worst    | Space  | Stable | In-place | Notes                        |
|------------------|----------|----------|----------|--------|--------|----------|------------------------------|
| Bubble           | O(n)     | O(n²)    | O(n²)    | O(1)   | Yes    | Yes      | Educational only             |
| Selection        | O(n²)    | O(n²)    | O(n²)    | O(1)   | No     | Yes      | Educational only             |
| Insertion        | O(n)     | O(n²)    | O(n²)    | O(1)   | Yes    | Yes      | Great for nearly-sorted      |
| Merge            | O(nlogn) | O(nlogn) | O(nlogn) | O(n)   | Yes    | No       | External sorting; LL-friendly|
| Quick            | O(nlogn) | O(nlogn) | O(n²)    | O(logn)| No     | Yes      | Cache-friendly; standard sort|
| Heap             | O(nlogn) | O(nlogn) | O(nlogn) | O(1)   | No     | Yes      | Worst-case guarantee         |
| Counting         | O(n+k)   | O(n+k)   | O(n+k)   | O(k)   | Yes    | No       | Bounded integers             |
| Radix            | O(d(n+k))| O(d(n+k))| O(d(n+k))| O(n+k) | Yes    | No       | Integers / strings           |
| Bucket           | O(n+k)   | O(n+k)   | O(n²)    | O(n+k) | Yes    | No       | Uniform distribution         |
| TimSort          | O(n)     | O(nlogn) | O(nlogn) | O(n)   | Yes    | No       | Python's sort, Java's sort   |
| IntroSort        | O(nlogn) | O(nlogn) | O(nlogn) | O(logn)| No     | Yes      | C++ std::sort                |

---

## II. THE LOWER BOUND

**Theorem**: any **comparison-based** sort requires Ω(n log n) comparisons in the worst case.

**Proof sketch**: a comparison sort produces a binary decision tree. The tree must distinguish all n! permutations. Tree of height h has ≤ 2^h leaves. So h ≥ log₂(n!) = Θ(n log n). □

→ Comparison sorts cannot beat n log n.
→ Non-comparison sorts (counting, radix, bucket) beat it for restricted inputs.

---

## III. THE THREE MUST-IMPLEMENT FROM SCRATCH

### Merge Sort
```cpp
void merge(vector<int>& a, int l, int m, int r) {
    vector<int> tmp(r - l + 1);
    int i = l, j = m + 1, k = 0;
    while (i <= m && j <= r) tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    while (i <= m) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int x = 0; x < tmp.size(); x++) a[l + x] = tmp[x];
}

void mergeSort(vector<int>& a, int l, int r) {
    if (l >= r) return;
    int m = (l + r) / 2;
    mergeSort(a, l, m);
    mergeSort(a, m + 1, r);
    merge(a, l, m, r);
}
```

### Quick Sort
```cpp
int partition(vector<int>& a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo - 1;
    for (int j = lo; j < hi; j++) {
        if (a[j] <= pivot) swap(a[++i], a[j]);
    }
    swap(a[++i], a[hi]);
    return i;
}

void quickSort(vector<int>& a, int lo, int hi) {
    if (lo < hi) {
        int p = partition(a, lo, hi);
        quickSort(a, lo, p - 1);
        quickSort(a, p + 1, hi);
    }
}
```

For better practical performance: random pivot + 3-way partition.

### Heap Sort
```cpp
void heapify(vector<int>& a, int n, int i) {
    int largest = i, l = 2*i + 1, r = 2*i + 2;
    if (l < n && a[l] > a[largest]) largest = l;
    if (r < n && a[r] > a[largest]) largest = r;
    if (largest != i) { swap(a[i], a[largest]); heapify(a, n, largest); }
}

void heapSort(vector<int>& a) {
    int n = a.size();
    for (int i = n / 2 - 1; i >= 0; i--) heapify(a, n, i);
    for (int i = n - 1; i > 0; i--) {
        swap(a[0], a[i]);
        heapify(a, i, 0);
    }
}
```

---

## IV. NON-COMPARISON SORTS

### Counting Sort — O(n + k)
For integers in [0, k]. Count occurrences; reconstruct.

### Radix Sort — O(d × (n + k))
Sort by each digit (LSD or MSD). With counting sort as subroutine, overall O(n) when d, k constant.

### Bucket Sort — O(n + k) average
Partition into k buckets; sort each (with insertion sort or recursively); concatenate.

---

## V. TIMSORT (Python's & Java's standard)

Hybrid of merge sort and insertion sort. Identifies "runs" of already-sorted segments, merges intelligently.

- O(n) on already-sorted data
- O(n log n) worst case
- Stable
- Used in Python's `list.sort` / `sorted`, Java's `Arrays.sort` (for Object types)

---

## VI. INTROSORT (C++ std::sort)

Quicksort with fallback to heap sort if recursion depth exceeds 2 log n. Avoids quicksort's worst case.

---

## VII. CUSTOM COMPARATORS

```cpp
sort(a.begin(), a.end(), [](int x, int y) { return abs(x) < abs(y); });

// Sort by frequency, then by value
sort(a.begin(), a.end(), [&](int x, int y) {
    if (freq[x] != freq[y]) return freq[x] > freq[y];  // higher freq first
    return x < y;  // tie: smaller value first
});
```

---

## VIII. SORTING-ENABLED PATTERNS

### Pattern 1: **Sort then linear scan**
Many problems become O(n) after O(n log n) sorting.

### Pattern 2: **Sort intervals**
Schedule problems, merge intervals, etc.

### Pattern 3: **Sort by custom key**
"Sort employees by salary descending, then by name."

### Pattern 4: **Sorting + two pointers**
3-sum, 4-sum, container with most water (variant).

### Pattern 5: **Counting sort indirectly** (bucketing)
Top-K frequent: bucket by frequency.

---

## IX. PROBLEMS

1. Sort 0s, 1s, 2s (Dutch flag)
2. Inversions in array (merge sort, O(n log n))
3. Count smaller numbers after self
4. Reverse pairs
5. Merge sorted arrays
6. Maximum gap (bucket sort)
7. Wiggle sort I, II
8. K closest points to origin (quickselect, O(n) avg)
9. Kth largest element (quickselect)
10. Top K frequent elements
11. Sort characters by frequency
12. Custom sort string
13. Largest number (custom comparator)
14. Reorganize string
15. Sort an array (LC 912)

---

## X. WHEN TO PICK WHICH

- Small n (< 50): insertion sort (low constants)
- General purpose: built-in (TimSort or IntroSort)
- Integers in known small range: counting sort
- Need stable sort: merge sort or TimSort
- Memory-constrained: heap sort or quicksort
- External (data > RAM): merge sort variants

---

## XI. PARALLEL SORTING

- Parallel merge sort
- Bitonic sort (for GPUs)
- Sample sort (for distributed)
- TeraSort (for MapReduce)

For Level 8 / production. See the parallel section in [`COMPENDIUM-Advanced-Algorithms.md`](./COMPENDIUM-Advanced-Algorithms.md) (§13) and [`../11-ADVANCED-PARADIGMS-UNIVERSE/08-COMPENDIUM-Advanced.md`](../11-ADVANCED-PARADIGMS-UNIVERSE/08-COMPENDIUM-Advanced.md) (§05).

---

**→ Next:** [`03-Divide-And-Conquer.md`](./03-Divide-And-Conquer.md)
