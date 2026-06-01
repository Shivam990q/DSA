# Task Scheduler

**Platform**: LeetCode 621 · **Difficulty**: Medium · **Topics**: Array, Hash Table, Greedy, Sorting, Heap (Priority Queue), Counting · **Pattern**: Greedy scheduling / max-heap simulation

---

## 📜 Problem Statement

You are given an array of CPU `tasks`, each labeled with a letter from `A` to `Z`, and an integer `n`. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of **at least** `n` intervals between two tasks with the **same** label.

Return the **minimum** number of CPU intervals required to complete all tasks.

### Examples

**Example 1:**
```
Input:  tasks = ["A","A","A","B","B","B"], n = 2
Output: 8

Explanation:
A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
After completing task A, you must wait two intervals before doing A again.
The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle.
By the 4th interval, you can do A again as 2 intervals have passed.
```

**Example 2:**
```
Input:  tasks = ["A","C","A","B","D","B"], n = 1
Output: 6

Explanation:
A possible sequence is: A -> B -> C -> D -> A -> B.
With a cooling interval of 1, you can repeat a task after just one other task.
```

**Example 3:**
```
Input:  tasks = ["A","A","A","B","B","B"], n = 3
Output: 10

Explanation:
A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.
There are only two types of tasks, A and B, which need to be separated by 3 intervals.
This leads to idling twice between repetitions.
```

### Constraints
```
1 <= tasks.length <= 10^4
0 <= n <= 100
tasks[i] is an uppercase English letter.
```

---

## 🧠 Understanding the problem

We schedule one task per interval, possibly idling, such that two identical tasks are at least `n` intervals apart, and we want to **minimize total intervals** (work + idle).

The crucial insight: **the most frequent task is the bottleneck.** Suppose task `A` occurs `maxCount` times. Between consecutive `A`s we need `n` other intervals. So `A` forces a skeleton of `(maxCount - 1)` blocks, each of length `(n + 1)` (one `A` plus `n` cooldown slots), followed by a final `A`. We then slot the other tasks into the cooldown gaps. Idle time appears only when there aren't enough other tasks to fill the gaps.

This yields a beautiful closed-form. Let `maxCount` be the highest frequency and `numMax` be how many tasks tie at that frequency. The answer is:

```
max( tasks.length , (maxCount - 1) * (n + 1) + numMax )
```

- `(maxCount - 1) * (n + 1)` builds the rigid frame from the most frequent task.
- `+ numMax` appends the final occurrence of every task tied for the max (they sit in the last block).
- `max(..., tasks.length)`: if there are *many distinct* tasks, the gaps fill completely and there's **no idle** — the answer is simply the number of tasks. The formula can never undercount below the total work.

A **max-heap simulation** reaches the same answer by literally playing out the schedule, which is more intuitive to derive even if the formula is faster.

---

## Approach 1 — Max-heap simulation (intuitive) ⭐

### Intuition
Greedy rule: **at each cycle of `n + 1` intervals, run the most frequent remaining tasks first.** A max-heap of remaining counts gives the most frequent task each pick. Process one full cooldown window `(n + 1)` slots at a time: pop up to `n + 1` distinct tasks, decrement each, and remember which ones still have remaining counts to push back after the window. Add idles only when the heap empties mid-window but tasks still remain.

### Algorithm
1. Count task frequencies; push all counts into a max-heap.
2. While the heap is non-empty:
   - For `i` in `0..n` (one window of size `n + 1`):
     - If heap non-empty, pop the largest count; if it's > 1, stash `count - 1` in a temp list.
     - Increment a `time` counter.
     - If heap is empty **and** the temp list is empty → all done, break out of the window early (no trailing idle).
   - Push every stashed count back into the heap.
3. Return `time`.

### Dry run on ["A","A","A","B","B","B"], n=2
```
counts: A=3, B=3 → heap {3,3}; window size n+1 = 3
Window 1: pop 3(A)→stash 2; pop 3(B)→stash 2; heap empty, but stash not empty → time +1 (idle). time=3
          push back {2,2}
Window 2: pop 2(A)→stash 1; pop 2(B)→stash 1; heap empty, stash not empty → idle. time=6
          push back {1,1}
Window 3: pop 1(A)→done; pop 1(B)→done; heap empty AND stash empty → break early. time=8
Result: 8 ✓
```

### Code
```cpp
int leastInterval(vector<char>& tasks, int n) {
    vector<int> cnt(26, 0);
    for (char t : tasks) cnt[t - 'A']++;
    priority_queue<int> maxHeap;                  // max-heap of counts
    for (int c : cnt) if (c > 0) maxHeap.push(c);

    int time = 0;
    while (!maxHeap.empty()) {
        vector<int> temp;
        for (int i = 0; i <= n; i++) {
            if (!maxHeap.empty()) {
                int c = maxHeap.top(); maxHeap.pop();
                if (c > 1) temp.push_back(c - 1);
            }
            time++;
            if (maxHeap.empty() && temp.empty()) break;   // no trailing idle
        }
        for (int c : temp) maxHeap.push(c);
    }
    return time;
}
```
```java
public int leastInterval(char[] tasks, int n) {
    int[] cnt = new int[26];
    for (char t : tasks) cnt[t - 'A']++;
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    for (int c : cnt) if (c > 0) maxHeap.offer(c);

    int time = 0;
    while (!maxHeap.isEmpty()) {
        List<Integer> temp = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            if (!maxHeap.isEmpty()) {
                int c = maxHeap.poll();
                if (c > 1) temp.add(c - 1);
            }
            time++;
            if (maxHeap.isEmpty() && temp.isEmpty()) break;   // no trailing idle
        }
        for (int c : temp) maxHeap.offer(c);
    }
    return time;
}
```
```python
import heapq
from collections import Counter

def leastInterval(tasks, n):
    cnt = Counter(tasks)
    max_heap = [-c for c in cnt.values()]    # negate for max-heap
    heapq.heapify(max_heap)

    time = 0
    while max_heap:
        temp = []
        for i in range(n + 1):
            if max_heap:
                c = -heapq.heappop(max_heap)
                if c > 1:
                    temp.append(-(c - 1))
            time += 1
            if not max_heap and not temp:
                break                         # no trailing idle
        for c in temp:
            heapq.heappush(max_heap, c)
    return time
```

### Complexity
- **Time**: O(T) where T = total intervals returned, with heap ops bounded by the 26-letter alphabet (O(log 26) = O(1)). Effectively O(tasks.length).
- **Space**: O(1) — the heap holds at most 26 entries.

### Verdict
The most *teachable* solution: it literally simulates the greedy schedule, so it's easy to convince yourself it's optimal. Slightly more code than the formula, but the reasoning is transparent.

---

## Approach 2 — Greedy closed-form formula (optimal) ⭐⭐

### Intuition
Skip the simulation. The most frequent task builds a rigid frame of `(maxCount - 1)` rows of width `(n + 1)`; the last row holds every task tied for the maximum frequency. If other tasks overflow the idle gaps, there's no idle at all and the answer is just the task count.

```
Frame for ["A","A","A","B","B","B"], n=2 (maxCount=3, numMax=2):
Row 1: A B _
Row 2: A B _
Last : A B          ← numMax = 2 tasks tie for the max
length = (3-1)*(2+1) + 2 = 8
```

### Algorithm
1. Count frequencies.
2. `maxCount` = the highest frequency; `numMax` = how many tasks have that frequency.
3. `slots = (maxCount - 1) * (n + 1) + numMax`.
4. Return `max(tasks.length, slots)`.

### Dry run
```
["A","A","A","B","B","B"], n=3:
maxCount=3, numMax=2
slots = (3-1)*(3+1) + 2 = 2*4 + 2 = 10
max(6, 10) = 10 ✓  (Example 3)

["A","C","A","B","D","B"], n=1:
counts A=2,B=2,C=1,D=1 → maxCount=2, numMax=2
slots = (2-1)*(1+1) + 2 = 2 + 2 = 4
max(6, 4) = 6 ✓  (Example 2: enough distinct tasks → no idle)
```

### Code
```cpp
int leastInterval(vector<char>& tasks, int n) {
    vector<int> cnt(26, 0);
    for (char t : tasks) cnt[t - 'A']++;
    int maxCount = *max_element(cnt.begin(), cnt.end());
    int numMax = count(cnt.begin(), cnt.end(), maxCount);
    int slots = (maxCount - 1) * (n + 1) + numMax;
    return max((int)tasks.size(), slots);
}
```
```java
public int leastInterval(char[] tasks, int n) {
    int[] cnt = new int[26];
    for (char t : tasks) cnt[t - 'A']++;
    int maxCount = 0;
    for (int c : cnt) maxCount = Math.max(maxCount, c);
    int numMax = 0;
    for (int c : cnt) if (c == maxCount) numMax++;
    int slots = (maxCount - 1) * (n + 1) + numMax;
    return Math.max(tasks.length, slots);
}
```
```python
from collections import Counter

def leastInterval(tasks, n):
    cnt = Counter(tasks)
    max_count = max(cnt.values())
    num_max = sum(1 for v in cnt.values() if v == max_count)
    slots = (max_count - 1) * (n + 1) + num_max
    return max(len(tasks), slots)
```

### Complexity
- **Time**: O(N) to count (N = tasks.length); the frequency table is fixed at 26.
- **Space**: O(1).

### Verdict
**The optimal answer.** O(N) time, O(1) space, no heap needed. The only "cost" is that you must derive (and trust) the formula. The two terms — frame plus tail, floored by total work — capture every case.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Max-heap simulation | O(T) ≈ O(N) | O(1) (≤26) | easy to reason about; plays out the schedule ⭐ |
| Greedy formula | **O(N)** | **O(1)** | no heap; derive once and reuse ⭐⭐ |

Both are linear. The heap simulation is the **intuition builder** and generalizes if the rules change (e.g., per-task cooldowns); the formula is the **tightest** solution when the rules are exactly as stated.

---

## 🧪 Edge cases & pitfalls
- **n = 0**: no cooldown → never idle → answer is `tasks.length`. The formula gives `(maxCount-1)*1 + numMax ≤ N`, and the `max` clamps to `N`.
- **Many distinct tasks**: when distinct tasks ≥ the frame width, gaps fill completely and the answer equals `tasks.length` (Example 2). The `max(...)` term handles this.
- **Single task type**: `["A","A","A"]`, n=2 → `(3-1)*3 + 1 = 7` (A _ _ A _ _ A).
- **Ties for the max frequency**: `numMax` counts *all* tasks at the top frequency; they all occupy the final block. Forgetting `numMax` (using 1) undercounts.
- **Pitfall — off-by-one in the window**: the cooldown window is `n + 1` slots (the task itself plus `n` gaps), not `n`. Looping `i` from `0` to `n` inclusive is `n + 1` iterations.
- **Pitfall — trailing idle**: in the simulation, do not count idle intervals after the *last* real task. Break the window early once the heap and the stash are both empty.
- **Pitfall (Python)**: negate counts for the max-heap, and negate back when reading.

---

## 🔗 Related problems
- **Reorganize String** (LC 767) — same "spread out the most frequent" idea via a max-heap on characters.
- **Rearrange String k Distance Apart** (LC 358) — generalized cooldown with a queue + heap.
- **Last Stone Weight** (LC 1046) — another max-heap simulation. *(file 02)*
- **Distant Barcodes** (LC 1054) — interleave by frequency with a heap.

---

**→ Next:** [`06-Design-Twitter.md`](./06-Design-Twitter.md) | **← Prev:** [`04-Kth-Largest-Element-In-Array.md`](./04-Kth-Largest-Element-In-Array.md) | Back to [`00-Index.md`](./00-Index.md)
