# Last Stone Weight

**Platform**: LeetCode 1046 · **Difficulty**: Easy · **Topics**: Array, Heap (Priority Queue) · **Pattern**: Max-heap simulation

---

## 📜 Problem Statement

You are given an array of integers `stones` where `stones[i]` is the weight of the `ith` stone.

We are playing a game with the stones. On each turn, we choose the **heaviest two stones** and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:

- If `x == y`, both stones are destroyed, and
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

At the end of the game, there is **at most one** stone left.

Return the weight of the last remaining stone. If there are no stones left, return `0`.

### Examples

**Example 1:**
```
Input:  stones = [2,7,4,1,8,1]
Output: 1

Explanation:
We combine 7 and 8 to get 1, so the array converts to [2,4,1,1,1].
We combine 2 and 4 to get 2, so the array converts to [2,1,1,1].
We combine 2 and 1 to get 1, so the array converts to [1,1,1].
We combine 1 and 1 to get 0, so the array converts to [1].
That's the value of the last stone.
```

**Example 2:**
```
Input:  stones = [1]
Output: 1

Explanation: Only one stone — nothing to smash, return it.
```

**Example 3:**
```
Input:  stones = [3,3]
Output: 0

Explanation: 3 and 3 smash to 0; both destroyed, nothing left → 0.
```

### Constraints
```
1 <= stones.length <= 30
1 <= stones[i] <= 1000
```

---

## 🧠 Understanding the problem

Every turn needs the **two heaviest** stones currently present, and a smash may put a *new* stone (`y - x`) back into the pile. So the set of stones is constantly changing, and we always need quick access to the current maximum.

That "repeatedly grab the largest, sometimes insert a new one" loop is the textbook signal for a **max-heap**. Pop the two largest, compute the difference, and if it's positive, push it back. Repeat until 0 or 1 stones remain.

The constraints are tiny (≤ 30 stones, weights ≤ 1000), so even a re-sort-every-round approach passes — but the heap version is the clean, scalable answer and the one expected for the topic.

---

## Approach 1 — Sort every round (baseline)

### Intuition
Keep the stones in a list. Each round, sort it, take the two largest from the end, smash, and push back the difference if non-zero.

### Algorithm
1. While more than one stone remains:
   - Sort the list ascending.
   - Pop the last two (`y`, then `x`, with `y ≥ x`).
   - If `y - x > 0`, append `y - x`.
2. Return the single remaining stone, or 0 if empty.

### Dry run on [2,7,4,1,8,1]
```
sort → [1,1,2,4,7,8]; pop 8,7 → diff 1 → [1,1,2,4,1]
sort → [1,1,1,2,4]; pop 4,2 → diff 2 → [1,1,1,2]
sort → [1,1,1,2]; pop 2,1 → diff 1 → [1,1,1]
sort → [1,1,1]; pop 1,1 → diff 0 → [1]
one stone left → return 1
```

### Code
```cpp
int lastStoneWeight(vector<int>& stones) {
    while (stones.size() > 1) {
        sort(stones.begin(), stones.end());
        int y = stones.back(); stones.pop_back();
        int x = stones.back(); stones.pop_back();
        if (y - x > 0) stones.push_back(y - x);
    }
    return stones.empty() ? 0 : stones[0];
}
```
```java
public int lastStoneWeight(int[] stones) {
    List<Integer> list = new ArrayList<>();
    for (int s : stones) list.add(s);
    while (list.size() > 1) {
        Collections.sort(list);
        int y = list.remove(list.size() - 1);
        int x = list.remove(list.size() - 1);
        if (y - x > 0) list.add(y - x);
    }
    return list.isEmpty() ? 0 : list.get(0);
}
```
```python
def lastStoneWeight(stones):
    stones = list(stones)
    while len(stones) > 1:
        stones.sort()
        y = stones.pop()
        x = stones.pop()
        if y - x > 0:
            stones.append(y - x)
    return stones[0] if stones else 0
```

### Complexity
- **Time**: O(n² log n) worst case — up to n rounds, each sorting O(n log n).
- **Space**: O(1) extra (in place) / O(n) for the working list.

### Verdict
Fine for n ≤ 30, but it re-sorts the whole pile every round just to find the top two. A heap maintains the order incrementally.

---

## Approach 2 — Max-heap simulation (optimal) ⭐

### Intuition
A **max-heap** hands us the heaviest stone in O(1) and lets us remove it in O(log n). Pop twice for the two heaviest; if they differ, push the difference back. The heap reorganizes itself in O(log n) instead of a full O(n log n) re-sort each round.

### Algorithm
1. Build a max-heap from all stones.
2. While the heap has more than one stone:
   - Pop `y` (largest), pop `x` (second largest).
   - If `y != x`, push `y - x`.
3. Return the heap's top if non-empty, else 0.

### Dry run on [2,7,4,1,8,1]
```
max-heap top order: 8,7,4,2,1,1
pop 8, pop 7 → 8≠7 → push 1   → heap {4,2,1,1,1}
pop 4, pop 2 → 4≠2 → push 2   → heap {2,1,1,1}
pop 2, pop 1 → 2≠1 → push 1   → heap {1,1,1}
pop 1, pop 1 → equal → push nothing → heap {1}
size 1 → return 1
```

### Code
```cpp
int lastStoneWeight(vector<int>& stones) {
    priority_queue<int> maxHeap(stones.begin(), stones.end());  // max-heap
    while (maxHeap.size() > 1) {
        int y = maxHeap.top(); maxHeap.pop();
        int x = maxHeap.top(); maxHeap.pop();
        if (y != x) maxHeap.push(y - x);
    }
    return maxHeap.empty() ? 0 : maxHeap.top();
}
```
```java
public int lastStoneWeight(int[] stones) {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    for (int s : stones) maxHeap.offer(s);
    while (maxHeap.size() > 1) {
        int y = maxHeap.poll();
        int x = maxHeap.poll();
        if (y != x) maxHeap.offer(y - x);
    }
    return maxHeap.isEmpty() ? 0 : maxHeap.peek();
}
```
```python
import heapq

def lastStoneWeight(stones):
    heap = [-s for s in stones]      # negate for a max-heap
    heapq.heapify(heap)
    while len(heap) > 1:
        y = -heapq.heappop(heap)     # largest
        x = -heapq.heappop(heap)     # second largest
        if y != x:
            heapq.heappush(heap, -(y - x))
    return -heap[0] if heap else 0
```

### Complexity
- **Time**: O(n log n) — building the heap is O(n), and each of up to n−1 rounds does O(log n) pops/pushes.
- **Space**: O(n) for the heap.

### Verdict
**The optimal answer.** Incrementally maintains the max instead of re-sorting. The clean "pop two, push difference" loop is the canonical max-heap simulation.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Sort each round | O(n² log n) | O(n) | re-sorts the whole pile every round |
| Max-heap | **O(n log n)** | O(n) | maintains the max incrementally ⭐ |

Both pass the small constraints, but the heap is the scalable, idiomatic solution and the one the topic is teaching.

---

## 🧪 Edge cases & pitfalls
- **Single stone**: loop never runs; return it directly.
- **Two equal stones**: smash to 0, heap empties → return 0 (Example 3).
- **All stones eventually cancel**: heap becomes empty → return 0.
- **Equal-weight smash pushes nothing**: only push when `y != x`; pushing a 0 would be harmless to the answer but pollutes the heap and weights are ≥ 1, so guard it.
- **Pitfall (C++)**: `priority_queue<int>` is already a max-heap — do **not** add `greater<int>` (that would make it a min-heap and break the logic).
- **Pitfall (Python)**: `heapq` is min-only, so negate on the way in *and* on the way out. Forgetting one negation silently smashes the *lightest* stones.
- **Pitfall**: reading `top()`/`peek()` without checking emptiness after the loop — return 0 when empty.

---

## 🔗 Related problems
- **Kth Largest Element in a Stream** (LC 703) — heap that always exposes an order statistic. *(file 01)*
- **Last Stone Weight II** (LC 1049) — the deceptively different DP/partition version (subset-sum), *not* a heap problem.
- **Maximum Performance of a Team** (LC 1383) — greedy + min-heap of size k.
- **IPO** (LC 502) — two heaps to greedily pick the most profitable affordable project.

---

**→ Next:** [`03-K-Closest-Points.md`](./03-K-Closest-Points.md) | **← Prev:** [`01-Kth-Largest-In-Stream.md`](./01-Kth-Largest-In-Stream.md) | Back to [`00-Index.md`](./00-Index.md)
