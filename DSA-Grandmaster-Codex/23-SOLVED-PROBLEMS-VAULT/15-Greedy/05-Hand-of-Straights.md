# Hand of Straights

**Platform**: LeetCode 846 · **Difficulty**: Medium · **Topics**: Array, Hash Table, Greedy, Sorting · **Pattern**: Sorted-count greedy consumption

---

## 📜 Problem Statement

Alice has some number of cards and she wants to rearrange the cards into groups so that each group is of size `groupSize`, and consists of `groupSize` **consecutive** cards.

Given an integer array `hand` where `hand[i]` is the value written on the `i`-th card and an integer `groupSize`, return `true` if she can rearrange the cards, or `false` otherwise.

### Examples

**Example 1:**
```
Input:  hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
Output: true
Explanation: Alice's hand can be rearranged as [1,2,3],[2,3,4],[6,7,8].
```

**Example 2:**
```
Input:  hand = [1,2,3,4,5], groupSize = 4
Output: false
Explanation: Alice's hand can't be rearranged into groups of 4.
```

**Example 3:**
```
Input:  hand = [1,1,2,2,3,3], groupSize = 3
Output: true
Explanation: Two groups [1,2,3] and [1,2,3] use all six cards.
```

### Constraints
```
1 <= hand.length <= 10^4
0 <= hand[i] <= 10^9
1 <= groupSize <= hand.length
```

> This problem is identical to LC 1296 "Divide Array in Sets of K Consecutive Numbers".

---

## 🧠 Understanding the problem

We must tile all cards into runs of `groupSize` consecutive integers. First, an obvious necessary condition: `hand.length` must be divisible by `groupSize`, otherwise the groups can't partition the hand.

The key greedy observation: consider the **smallest** card value present, say `m`. There is no card smaller than `m`, so `m` cannot be the 2nd, 3rd, … element of any consecutive run — it **must** be the start of a group `[m, m+1, …, m+groupSize-1]`. If we have `c` copies of `m`, then we need `c` groups all starting at `m`, which forces `c` copies each of `m+1, m+2, …`. Consume them. Repeat with the new smallest remaining value. If at any point the required next consecutive card isn't available in sufficient quantity, it's impossible.

Sorting (or a sorted map of counts) gives us "smallest available" cheaply.

---

## Approach 1 — Sorted hash map / TreeMap greedy (optimal) ⭐

### Intuition
Count each value. Process values in increasing order. For the current smallest value with positive count `c`, it must anchor `c` groups, so subtract `c` from each of `value, value+1, …, value+groupSize-1`. If any of those falls short, return `false`.

### Algorithm
1. If `n % groupSize != 0` → `false`.
2. Build a count map; iterate keys in **sorted** order.
3. For each `card` with `cnt[card] = c > 0`:
   - For `k` in `0..groupSize-1`: if `cnt[card+k] < c` → `false`; else `cnt[card+k] -= c`.
4. Return `true`.

### Dry run on `hand=[1,2,3,6,2,3,4,7,8], groupSize=3`
```
counts: 1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1   (n=9 divisible by 3 ✓)
card=1 c=1: need 1,2,3 → cnt→ 1:0,2:1,3:1
card=2 c=1: need 2,3,4 → cnt→ 2:0,3:0,4:0
card=6 c=1: need 6,7,8 → cnt→ 6:0,7:0,8:0
all consumed → true
```

### Code
```cpp
bool isNStraightHand(vector<int>& hand, int groupSize) {
    if (hand.size() % groupSize != 0) return false;
    map<int,int> cnt;                  // ordered map → ascending keys
    for (int c : hand) cnt[c]++;
    for (auto& [card, _] : cnt) {
        int c = cnt[card];
        if (c > 0) {
            for (int k = 0; k < groupSize; k++) {
                if (cnt[card + k] < c) return false;
                cnt[card + k] -= c;
            }
        }
    }
    return true;
}
```
```java
public boolean isNStraightHand(int[] hand, int groupSize) {
    if (hand.length % groupSize != 0) return false;
    TreeMap<Integer,Integer> cnt = new TreeMap<>();
    for (int c : hand) cnt.merge(c, 1, Integer::sum);
    for (int card : cnt.keySet()) {
        int c = cnt.get(card);
        if (c > 0) {
            for (int k = 0; k < groupSize; k++) {
                int need = card + k;
                if (cnt.getOrDefault(need, 0) < c) return false;
                cnt.put(need, cnt.get(need) - c);
            }
        }
    }
    return true;
}
```
```python
from collections import Counter
def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False
    cnt = Counter(hand)
    for card in sorted(cnt):
        c = cnt[card]
        if c > 0:
            for k in range(groupSize):
                if cnt[card + k] < c:
                    return False
                cnt[card + k] -= c
    return True
```

### Complexity
- **Time**: O(n log n) — sorting / ordered-map traversal dominates; the inner loop does O(n·groupSize / groupSize) = O(n) total consumption work amortized, but the ordered structure costs the log factor.
- **Space**: O(n) for the count map.

### Verdict
**Optimal and clean.** The "smallest card must start a group" argument is the whole proof; an ordered map makes it almost transcribe itself.

---

## Approach 2 — Min-heap greedy

### Intuition
Same logic, but use a **min-heap** of distinct values plus a count map. Repeatedly pop the smallest, and build a group upward. Useful when you want to avoid a full ordered map and prefer a priority queue.

### Algorithm
1. Divisibility check.
2. Count values; push distinct values into a min-heap.
3. While the heap isn't empty: peek the smallest `start`; for `k` in `0..groupSize-1`, the value `start+k` must exist with count > 0 — decrement it; if it hits zero it must be the current heap minimum (else there's a gap), so pop it.

### Dry run on `hand=[1,1,2,2,3,3], groupSize=3`
```
counts 1:2,2:2,3:2 ; heap [1,2,3]
start=1: consume 1,2,3 → counts 1:1,2:1,3:1 (none hit 0)
start=1 again: consume 1,2,3 → counts 0,0,0; pop 1, then 2, then 3
heap empty → true
```

### Code
```cpp
bool isNStraightHand(vector<int>& hand, int groupSize) {
    if (hand.size() % groupSize != 0) return false;
    unordered_map<int,int> cnt;
    for (int c : hand) cnt[c]++;
    priority_queue<int, vector<int>, greater<int>> pq;
    for (auto& [v, _] : cnt) pq.push(v);
    while (!pq.empty()) {
        int start = pq.top();
        for (int k = 0; k < groupSize; k++) {
            int v = start + k;
            if (cnt[v] == 0) return false;
            cnt[v]--;
            if (cnt[v] == 0) {
                if (v != pq.top()) return false;  // a gap remains below
                pq.pop();
            }
        }
    }
    return true;
}
```
```java
public boolean isNStraightHand(int[] hand, int groupSize) {
    if (hand.length % groupSize != 0) return false;
    Map<Integer,Integer> cnt = new HashMap<>();
    for (int c : hand) cnt.merge(c, 1, Integer::sum);
    PriorityQueue<Integer> pq = new PriorityQueue<>(cnt.keySet());
    while (!pq.isEmpty()) {
        int start = pq.peek();
        for (int k = 0; k < groupSize; k++) {
            int v = start + k;
            int have = cnt.getOrDefault(v, 0);
            if (have == 0) return false;
            cnt.put(v, have - 1);
            if (have - 1 == 0) {
                if (v != pq.peek()) return false;
                pq.poll();
            }
        }
    }
    return true;
}
```
```python
import heapq
from collections import Counter
def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False
    cnt = Counter(hand)
    heap = list(cnt.keys())
    heapq.heapify(heap)
    while heap:
        start = heap[0]
        for k in range(groupSize):
            v = start + k
            if cnt[v] == 0:
                return False
            cnt[v] -= 1
            if cnt[v] == 0:
                if v != heap[0]:
                    return False
                heapq.heappop(heap)
    return True
```

### Complexity
- **Time**: O(n log n).
- **Space**: O(n).

### Verdict
Equivalent complexity; nice when a heap is the natural tool. The TreeMap version is usually shorter, so use that unless a heap is required.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Sorted map greedy | **O(n log n)** | O(n) | shortest, clearest ⭐ |
| Min-heap greedy | O(n log n) | O(n) | handy if you prefer a PQ |

Both rest on the same proof; they differ only in how they fetch "the smallest remaining value."

---

## 🧪 Edge cases & pitfalls
- **`n % groupSize != 0`** → immediate `false`. Always check first.
- **`groupSize == 1`** → every single card is its own group → always `true`.
- **Large values up to 10^9** → can't use a fixed array indexed by value; a hash/tree map is required.
- **Duplicates** → handled by counts; multiple copies of the smallest force multiple parallel groups.
- **Pitfall**: in the heap version, popping a value whose count hits zero but isn't the current minimum signals a hole below it (impossible to fill later) → must return `false`.
- **Pitfall**: mutating counts while iterating a `map` is fine because we only read forward keys, but don't erase keys mid-iteration.

---

## 🔗 Related problems
- **Divide Array in Sets of K Consecutive Numbers** (LC 1296) — the same problem, different wording.
- **Split Array into Consecutive Subsequences** (LC 659) — greedy with "extend vs start" choice.
- **Rearrange String k Distance Apart** (LC 358) — heap-based greedy scheduling.
- **Task Scheduler** (LC 621) — greedy on frequency counts.

---

**→ Next:** [`06-Merge-Triplets-To-Form-Target.md`](./06-Merge-Triplets-To-Form-Target.md) | **Prev:** [`04-Gas-Station.md`](./04-Gas-Station.md) | [Problem set index](./00-Index.md)
