# Top K Frequent Elements

**Platform**: LeetCode 347 · **Difficulty**: Medium · **Topics**: Array, Hash Table, Heap, Bucket Sort, Quickselect · **Pattern**: Frequency + selection

---

## 📜 Problem Statement

Given an integer array `nums` and an integer `k`, return the `k` **most frequent** elements. You may return the answer in any order.

### Examples

**Example 1:**
```
Input:  nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
Explanation: 1 appears 3 times, 2 appears twice, 3 once. Top 2 → [1,2].
```

**Example 2:**
```
Input:  nums = [1], k = 1
Output: [1]
```

### Constraints
```
1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4
k is in the range [1, number of distinct elements]
It is guaranteed the answer is unique.
```

### Follow-up
Your algorithm's time complexity must be **better than O(n log n)**.

---

## 🧠 Understanding the problem

Two sub-tasks: (1) **count frequencies** — clearly a hash map, O(n); (2) **select the k largest** by frequency. The whole difficulty is step 2 and how fast we can do it. The follow-up bans full sorting (O(n log n)), nudging us toward a heap (O(n log k)) or bucket sort / quickselect (O(n)).

---

## Approach 1 — Count + sort

### Intuition
Count frequencies, sort the distinct elements by frequency descending, take the first k.

### Algorithm
1. Build `freq[value] = count`.
2. Sort distinct values by `freq` descending.
3. Return the first k.

### Code
```cpp
vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int,int> freq;
    for (int x : nums) freq[x]++;
    vector<pair<int,int>> v(freq.begin(), freq.end());
    sort(v.begin(), v.end(), [](auto& a, auto& b){ return a.second > b.second; });
    vector<int> res;
    for (int i = 0; i < k; i++) res.push_back(v[i].first);
    return res;
}
```
```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    List<Map.Entry<Integer, Integer>> v = new ArrayList<>(freq.entrySet());
    v.sort((a, b) -> b.getValue() - a.getValue());
    int[] res = new int[k];
    for (int i = 0; i < k; i++) res[i] = v.get(i).getKey();
    return res;
}
```
```python
from collections import Counter
def topKFrequent(nums, k):
    freq = Counter(nums)
    return [val for val, _ in sorted(freq.items(), key=lambda x: -x[1])[:k]]
```

### Complexity
- **Time**: O(n + m log m), m = distinct elements.
- **Space**: O(m).

### Verdict
Correct, but violates the follow-up's sub-O(n log n) requirement. Baseline.

---

## Approach 2 — Min-heap of size k

### Intuition
We don't need to sort everything — only keep the **k most frequent**. A min-heap of size k holds the current top-k by frequency; the smallest frequency sits at the top and gets evicted when something bigger arrives.

### Algorithm
1. Count frequencies.
2. For each `(value, freq)`: push onto a min-heap keyed by freq; if heap size > k, pop the smallest.
3. The heap's k entries are the answer.

### Code
```cpp
vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int,int> freq;
    for (int x : nums) freq[x]++;
    // min-heap by frequency
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    for (auto& [val, f] : freq) {
        pq.push({f, val});
        if (pq.size() > k) pq.pop();
    }
    vector<int> res;
    while (!pq.empty()) { res.push_back(pq.top().second); pq.pop(); }
    return res;
}
```
```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    // min-heap by frequency: [freq, val]
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
        pq.offer(new int[]{e.getValue(), e.getKey()});
        if (pq.size() > k) pq.poll();
    }
    int[] res = new int[pq.size()];
    int i = 0;
    while (!pq.isEmpty()) res[i++] = pq.poll()[1];
    return res;
}
```
```python
import heapq
from collections import Counter
def topKFrequent(nums, k):
    freq = Counter(nums)
    return [val for val, _ in heapq.nlargest(k, freq.items(), key=lambda x: x[1])]
```

### Complexity
- **Time**: O(n + m log k).
- **Space**: O(m + k).

### Verdict
Satisfies the follow-up when k ≪ m. A very common interview answer. But there's an even better O(n) approach.

---

## Approach 3 — Bucket sort (optimal, O(n)) ⭐

### Intuition
A frequency can be at most `n` (if all elements are equal). So create `n+1` buckets where `bucket[f]` holds all values that occur exactly `f` times. Then walk buckets from highest frequency down, collecting until we have k. No sorting, no heap — pure O(n).

### Algorithm
1. Count frequencies.
2. Create `buckets[0..n]`; place each value into `buckets[freq]`.
3. Iterate `f` from `n` down to `1`, appending values until we collected k.

### Dry run on `[1,1,1,2,2,3], k=2`
```
freq: {1:3, 2:2, 3:1}
buckets: index1=[3], index2=[2], index3=[1]
walk f=6..1:
  f=3 → [1] → res=[1]
  f=2 → [2] → res=[1,2] → size==k → stop
```

### Code
```cpp
vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int,int> freq;
    for (int x : nums) freq[x]++;
    int n = nums.size();
    vector<vector<int>> buckets(n + 1);
    for (auto& [val, f] : freq) buckets[f].push_back(val);
    vector<int> res;
    for (int f = n; f >= 1 && (int)res.size() < k; f--)
        for (int val : buckets[f]) {
            res.push_back(val);
            if ((int)res.size() == k) break;
        }
    return res;
}
```
```java
public int[] topKFrequent(int[] nums, int k) {
    Map<Integer, Integer> freq = new HashMap<>();
    for (int x : nums) freq.merge(x, 1, Integer::sum);
    int n = nums.length;
    List<Integer>[] buckets = new List[n + 1];
    for (Map.Entry<Integer, Integer> e : freq.entrySet()) {
        int f = e.getValue();
        if (buckets[f] == null) buckets[f] = new ArrayList<>();
        buckets[f].add(e.getKey());
    }
    int[] res = new int[k];
    int idx = 0;
    for (int f = n; f >= 1 && idx < k; f--) {
        if (buckets[f] == null) continue;
        for (int val : buckets[f]) {
            res[idx++] = val;
            if (idx == k) break;
        }
    }
    return res;
}
```
```python
from collections import Counter
def topKFrequent(nums, k):
    freq = Counter(nums)
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]
    for val, f in freq.items():
        buckets[f].append(val)
    res = []
    for f in range(n, 0, -1):
        for val in buckets[f]:
            res.append(val)
            if len(res) == k:
                return res
    return res
```

### Complexity
- **Time**: O(n).
- **Space**: O(n).

### Verdict
**The optimal answer.** Linear time, beats the follow-up bound cleanly. The key realization is that frequencies are bounded by `n`, so we can index by frequency.

---

## Approach 4 — Quickselect (O(n) average, in place-ish)

### Intuition
Treat the distinct `(value,freq)` pairs as an array and **partition** around a pivot frequency (like quicksort) so the top-k land on one side. Recurse only into the relevant side → O(m) average.

### Complexity
- **Time**: O(m) average, O(m²) worst.
- **Space**: O(m).

### Verdict
Elegant and interview-impressive, but the worst case and added complexity make bucket sort the safer optimal choice. Mention it as an alternative.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Meets follow-up? |
|----------|------|-------|------------------|
| Count + sort | O(n + m log m) | O(m) | ❌ |
| Min-heap (size k) | O(n + m log k) | O(m+k) | ✅ (k ≪ m) |
| Bucket sort | **O(n)** | O(n) | ✅ best ⭐ |
| Quickselect | O(m) avg | O(m) | ✅ avg |

---

## 🧪 Edge cases & pitfalls
- **k equals number of distinct elements** → return all distinct values.
- **All elements identical** → one bucket at frequency `n`.
- **Pitfall (heap)**: keep a *min*-heap of size k (not a max-heap of everything); evicting the smallest is what bounds it to O(log k).
- **Pitfall (bucket)**: bucket array must have size `n+1` since a frequency can equal `n`.

---

## 🔗 Related problems
- **Top K Frequent Words** (LC 692) — adds lexicographic tie-breaking.
- **Kth Largest Element in an Array** (LC 215) — quickselect / heap selection.
- **Sort Characters By Frequency** (LC 451) — bucket sort by frequency.

---

**→ Next:** [`06-Product-of-Array-Except-Self.md`](./06-Product-of-Array-Except-Self.md) | Prev: [`04-Group-Anagrams.md`](./04-Group-Anagrams.md) | [Index](./00-Index.md)
