# Kth Largest Element in a Stream

**Platform**: LeetCode 703 · **Difficulty**: Easy · **Topics**: Tree, Design, BST, Heap (Priority Queue), Data Stream · **Pattern**: Min-heap of size K

---

## 📜 Problem Statement

You are part of a university admissions office and need to keep track of the `kth` highest test score from applicants in real time. This arises frequently in competitive gaming where you want to display the `kth` highest score in real time.

Implement a class to find the `kth` largest element in a stream. Note that it is the `kth` largest element **in the sorted order**, not the `kth` distinct element.

Implement the `KthLargest` class:

- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)` Appends the integer `val` to the stream and returns the element representing the `kth` largest element in the stream.

### Examples

**Example 1:**
```
Input:
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]

Output:
[null, 4, 5, 5, 8, 8]

Explanation:
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3);   // returns 4  → stream sorted desc: [8,5,4,3,2], 3rd largest = 4
kthLargest.add(5);   // returns 5  → [8,5,5,4,3,2], 3rd largest = 5
kthLargest.add(10);  // returns 5  → [10,8,5,5,4,3,2], 3rd largest = 5
kthLargest.add(9);   // returns 8  → [10,9,8,5,5,4,3,2], 3rd largest = 8
kthLargest.add(4);   // returns 8  → [10,9,8,5,5,4,4,3,2], 3rd largest = 8
```

**Example 2:**
```
Input:
["KthLargest", "add", "add"]
[[1, []], [-3], [-2]]

Output:
[null, -3, -2]

Explanation:
k = 1 means we always want the single largest element.
After add(-3): largest is -3. After add(-2): largest is -2.
```

**Example 3:**
```
Input:
["KthLargest", "add", "add", "add"]
[[2, [0]], [-1], [3], [5]]

Output:
[null, -1, 0, 3]

Explanation:
k = 2. After add(-1): [0,-1], 2nd largest = -1.
After add(3): [3,0,-1], 2nd largest = 0.
After add(5): [5,3,0,-1], 2nd largest = 3.
```

### Constraints
```
0 <= nums.length <= 10^4
1 <= k <= nums.length + 1
-10^4 <= nums[i] <= 10^4
-10^4 <= val <= 10^4
At most 10^4 calls will be made to add.
It is guaranteed that there will be at least k elements in the array when you search for the kth element.
```

---

## 🧠 Understanding the problem

We need the **k-th largest** value after each insertion — and we get up to 10⁴ insertions. The naive "re-sort after every add" works but is wasteful: we re-order the whole stream just to read one position.

The key observation: to know the k-th largest, **we don't need the whole sorted order — we only need the k largest elements**, and among *those* the smallest one is the answer. Anything ranked beyond k is irrelevant and can be thrown away.

That's a perfect job for a **min-heap of size k**. We keep exactly the k largest elements seen so far. The heap's root (its minimum) is the smallest of those k — which is precisely the k-th largest overall. When a new value arrives, push it; if the heap now holds k+1 elements, pop the smallest to drop back to size k. The root is then the updated answer.

---

## Approach 1 — Re-sort after each add (baseline)

### Intuition
Literal reading: maintain the full list, and after each `add`, sort it descending and read index `k-1`.

### Algorithm
1. Store all stream values in a list.
2. On `add(val)`: append `val`, sort the list descending, return element at index `k-1`.

### Dry run on k=3, nums=[4,5,8,2], add(3)
```
list = [4,5,8,2,3] → sort desc → [8,5,4,3,2]
index k-1 = 2 → value 4 → return 4
```

### Code
```cpp
class KthLargest {
    vector<int> v;
    int k;
public:
    KthLargest(int k, vector<int>& nums) : v(nums), k(k) {}
    int add(int val) {
        v.push_back(val);
        sort(v.begin(), v.end(), greater<int>());
        return v[k - 1];
    }
};
```
```java
class KthLargest {
    private List<Integer> v = new ArrayList<>();
    private int k;

    public KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) v.add(x);
    }
    public int add(int val) {
        v.add(val);
        v.sort(Collections.reverseOrder());
        return v.get(k - 1);
    }
}
```
```python
class KthLargest:
    def __init__(self, k: int, nums):
        self.k = k
        self.v = list(nums)

    def add(self, val: int) -> int:
        self.v.append(val)
        self.v.sort(reverse=True)
        return self.v[self.k - 1]
```

### Complexity
- **Time**: O(n log n) per `add`, so up to O(m · n log n) across m calls — wasteful.
- **Space**: O(n) for the full list.

### Verdict
Correct but it sorts the entire stream on every insertion just to read one position. We never need ranks beyond k, so most of that sorting is thrown away. The size-k heap fixes exactly this.

---

## Approach 2 — Min-heap of size k (optimal) ⭐

### Intuition
Keep only the **k largest elements** in a min-heap. The root is the smallest of those k = the k-th largest overall. Each `add` is O(log k): push, and if the heap exceeds size k, pop the smallest (it can never be the k-th largest, since k larger values exist).

### Algorithm
1. In the constructor, push every initial number through the same `add` logic so the heap ends up holding the k largest, capped at size k.
2. `add(val)`:
   - Push `val`.
   - If heap size > k, pop the minimum.
   - Return the heap's root (minimum) — the k-th largest.

### Dry run on k=3, nums=[4,5,8,2]
```
init pushes: 4 → [4]; 5 → [4,5]; 8 → [4,5,8]; 2 → push→[2,4,5,8] size4>3 → pop 2 → [4,5,8]
heap (min-heap) root = 4

add(3):  push 3 → {3,4,5,8} size4>3 → pop min 3 → {4,5,8} → root 4 → return 4
add(5):  push 5 → {4,5,5,8} → pop 4 → {5,5,8} → root 5 → return 5
add(10): push 10 → {5,5,8,10} → pop 5 → {5,8,10} → root 5 → return 5
add(9):  push 9 → {5,8,9,10} → pop 5 → {8,9,10} → root 8 → return 8
add(4):  push 4 → {4,8,9,10} → pop 4 → {8,9,10} → root 8 → return 8
```
Matches the expected output `[4, 5, 5, 8, 8]`.

### Code
```cpp
class KthLargest {
    priority_queue<int, vector<int>, greater<int>> minHeap;   // min-heap
    int k;
public:
    KthLargest(int k, vector<int>& nums) : k(k) {
        for (int x : nums) add(x);
    }
    int add(int val) {
        minHeap.push(val);
        if ((int)minHeap.size() > k) minHeap.pop();
        return minHeap.top();
    }
};
```
```java
class KthLargest {
    private PriorityQueue<Integer> minHeap;   // min-heap (Java default)
    private int k;

    public KthLargest(int k, int[] nums) {
        this.k = k;
        minHeap = new PriorityQueue<>();
        for (int x : nums) add(x);
    }
    public int add(int val) {
        minHeap.offer(val);
        if (minHeap.size() > k) minHeap.poll();
        return minHeap.peek();
    }
}
```
```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums):
        self.k = k
        self.heap = nums[:]            # copy
        heapq.heapify(self.heap)       # O(n) build
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

### Complexity
- **Time**: constructor O(n log k) (or O(n) heapify + trimming). Each `add` O(log k).
- **Space**: O(k) — the heap never exceeds k elements.

### Verdict
**The optimal answer.** Bounded memory and O(log k) per insertion regardless of how big the stream grows. The "keep only the k largest, the root is the answer" framing is the canonical size-k-heap pattern.

---

## ⚖️ Approach comparison

| Approach | add time | Space | Notes |
|----------|----------|-------|-------|
| Re-sort each add | O(n log n) | O(n) | sorts the whole stream every call |
| Min-heap of size k | **O(log k)** | **O(k)** | keep only the k largest ⭐ |

The heap wins decisively when k ≪ n: it ignores the (n − k) smaller elements entirely instead of repeatedly sorting them.

---

## 🧪 Edge cases & pitfalls
- **Empty initial `nums`**: the heap starts empty; early `add` calls fill it. The guarantee that ≥ k elements exist before a meaningful query means the root is valid when read.
- **k = 1**: a size-1 min-heap just tracks the running maximum.
- **Duplicates count**: the problem asks for the k-th largest in sorted order, *not* k-th distinct. The heap naturally keeps duplicates, so `[8,5,5,4]` with k=3 correctly yields 5.
- **Negative values**: no special handling — the heap orders them like any integer.
- **Pitfall — using a max-heap**: a max-heap would need to pop k−1 elements to read the k-th largest on every query. A **min-heap of size k** gives it directly at the root. Pick the right polarity.
- **Pitfall (Python)**: remember `heapq` is min-only — which is exactly what we want here, so *no* negation. Don't reflexively negate values.

---

## 🔗 Related problems
- **Kth Largest Element in an Array** (LC 215) — same k-th-largest target on a static array; quickselect becomes available. *(file 04)*
- **K Closest Points to Origin** (LC 973) — size-k *max*-heap variant. *(file 03)*
- **Top K Frequent Elements** (LC 347) — size-k heap keyed by frequency.
- **Find Median from Data Stream** (LC 295) — the two-heap escalation of streaming order statistics. *(file 07)*

---

**→ Next:** [`02-Last-Stone-Weight.md`](./02-Last-Stone-Weight.md) | Back to [`00-Index.md`](./00-Index.md)
