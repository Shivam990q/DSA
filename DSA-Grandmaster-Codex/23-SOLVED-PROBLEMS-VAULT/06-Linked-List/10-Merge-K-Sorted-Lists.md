# Merge K Sorted Lists

**Platform**: LeetCode 23 · **Difficulty**: Hard · **Topics**: Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort · **Pattern**: Min-heap over heads / divide & conquer pairwise merge

---

## 📜 Problem Statement

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

*Merge all the linked-lists into one sorted linked-list and return it.*

### Examples

**Example 1:**
```
Input:  lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6
```

**Example 2:**
```
Input:  lists = []
Output: []
```

**Example 3:**
```
Input:  lists = [[]]
Output: []
```

### Constraints
```
k == lists.length
0 <= k <= 10^4
0 <= lists[i].length <= 500
-10^4 <= lists[i][j] <= 10^4
lists[i] is sorted in ascending order.
The sum of lists[i].length will not exceed 10^4.
```

---

## 🧠 Understanding the problem

We already know how to merge **two** sorted lists in O(n + m) (see [`02-Merge-Two-Sorted-Lists.md`](./02-Merge-Two-Sorted-Lists.md)). The new twist is `k` lists at once. Let `N` be the total number of nodes across all lists.

The naive idea — repeatedly merge list 0 with list 1, then with list 2, … — works but is slow: the accumulated list gets re-traversed every merge, giving O(N·k). We want to avoid re-scanning the big merged prefix `k` times.

Two efficient strategies, both O(N log k):
1. **Min-heap of the current heads.** The smallest unplaced node is always the minimum among the `k` current heads. A heap surfaces that minimum in O(log k); pop it, append it, push its successor. Each of the `N` nodes is pushed/popped once → O(N log k).
2. **Divide & conquer.** Pair up the lists and merge them two at a time, halving the number of lists each round. After ⌈log₂ k⌉ rounds we have one list. Each round touches all `N` nodes once → O(N log k).

Both hit the same bound; the heap is more intuitive, divide & conquer uses no extra structure.

---

## Approach 1 — Sequential merge (warm-up, suboptimal)

### Intuition
Fold the array: keep a running merged list and merge each new list into it. Simple, but the running list is re-walked on every merge.

### Algorithm
1. `result = null`.
2. For each list `l` in `lists`: `result = mergeTwo(result, l)`.
3. Return `result`.

### Dry run on `[[1,4,5],[1,3,4],[2,6]]`
```
result = []          merge with [1,4,5] → [1,4,5]
merge [1,4,5] + [1,3,4] → [1,1,3,4,4,5]
merge [1,1,3,4,4,5] + [2,6] → [1,1,2,3,4,4,5,6] ✅
(notice the 6-node prefix gets walked again in the last merge)
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        ListNode* result = nullptr;
        for (ListNode* l : lists) result = mergeTwo(result, l);
        return result;
    }
private:
    ListNode* mergeTwo(ListNode* a, ListNode* b) {
        ListNode dummy(0);
        ListNode* tail = &dummy;
        while (a && b) {
            if (a->val <= b->val) { tail->next = a; a = a->next; }
            else                  { tail->next = b; b = b->next; }
            tail = tail->next;
        }
        tail->next = a ? a : b;
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        ListNode result = null;
        for (ListNode l : lists) result = mergeTwo(result, l);
        return result;
    }
    private ListNode mergeTwo(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (a != null && b != null) {
            if (a.val <= b.val) { tail.next = a; a = a.next; }
            else                { tail.next = b; b = b.next; }
            tail = tail.next;
        }
        tail.next = (a != null) ? a : b;
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        result = None
        for l in lists:
            result = self._merge_two(result, l)
        return result

    def _merge_two(self, a: ListNode, b: ListNode) -> ListNode:
        dummy = ListNode(0)
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a if a else b
        return dummy.next
```

### Complexity
- **Time**: O(N·k) — at merge step `i`, the running list has up to ~`i/k · N` nodes and we re-walk it.
- **Space**: O(1) (reusing nodes).

### Verdict
Correct and easy, but the repeated re-traversal of the growing prefix makes it the slow option. State it, then optimize.

---

## Approach 2 — Min-heap of current heads (optimal) ⭐

### Intuition
At any moment, the global next-smallest node is the minimum of the `k` lists' current heads. Maintain those heads in a min-heap keyed by value. Pop the smallest, splice it onto the result, and push that node's successor (if any). Repeat until the heap empties.

### Algorithm
1. Push the head of every non-null list into a min-heap (ordered by `val`).
2. With a `dummy`/`tail`:
   - While the heap is non-empty: pop the min node `n`, append to `tail`, advance `tail`. If `n.next` exists, push it.
3. Return `dummy.next`.

> In Python, push tuples `(val, index, node)` — the `index` tiebreaker prevents comparing `ListNode` objects when values tie.

### Dry run on `[[1,4,5],[1,3,4],[2,6]]`
```
heap (by val): {1a, 1b, 2}
pop 1a → result:1a, push 4(from list0)   heap{1b,2,4}
pop 1b → result:1a,1b, push 3            heap{2,3,4}
pop 2  → +2, push 6                      heap{3,4,6}
pop 3  → +3, push 4                      heap{4,4,6}
pop 4  → +4, push 5                      heap{4,5,6}
pop 4  → +4 (list1 exhausted)            heap{5,6}
pop 5  → +5 (list0 exhausted)            heap{6}
pop 6  → +6 (list2 exhausted)            heap{}
result: 1->1->2->3->4->4->5->6 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        auto cmp = [](ListNode* a, ListNode* b) { return a->val > b->val; };  // min-heap
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> pq(cmp);
        for (ListNode* l : lists)
            if (l) pq.push(l);

        ListNode dummy(0);
        ListNode* tail = &dummy;
        while (!pq.empty()) {
            ListNode* n = pq.top(); pq.pop();
            tail->next = n;
            tail = n;
            if (n->next) pq.push(n->next);
        }
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
        for (ListNode l : lists)
            if (l != null) pq.offer(l);

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!pq.isEmpty()) {
            ListNode n = pq.poll();
            tail.next = n;
            tail = n;
            if (n.next != null) pq.offer(n.next);
        }
        return dummy.next;
    }
}
```

**Python**
```python
import heapq

class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        heap = []
        for i, l in enumerate(lists):
            if l:
                heapq.heappush(heap, (l.val, i, l))  # i breaks ties; nodes never compared

        dummy = ListNode(0)
        tail = dummy
        while heap:
            val, i, n = heapq.heappop(heap)
            tail.next = n
            tail = n
            if n.next:
                heapq.heappush(heap, (n.next.val, i, n.next))
        return dummy.next
```

### Complexity
- **Time**: O(N log k) — each of `N` nodes is pushed and popped once; heap operations cost O(log k) since the heap holds at most `k` nodes.
- **Space**: O(k) — the heap stores one node per active list.

### Verdict
The most intuitive optimal solution. The heap size stays at `k`, so the log factor is `log k`, not `log N`. The Python tuple-with-index trick is essential to avoid "unorderable ListNode" errors on value ties.

---

## Approach 3 — Divide & conquer (pairwise merge)

### Intuition
Like merge sort's merge phase: merge lists in pairs so the count halves each round (k → k/2 → k/4 → … → 1). Crucially, every node is touched exactly once per round and there are ⌈log₂ k⌉ rounds → O(N log k), with **no auxiliary heap**.

### Algorithm
1. If `lists` is empty, return null.
2. While more than one list remains:
   - Merge `lists[i]` with `lists[i + interval]` for `i = 0, 2·interval, 4·interval, …`.
   - Double the `interval`.
3. Return `lists[0]`.

(Equivalently, recurse: split the array in half, merge each half, then merge the two results.)

### Dry run on `[A, B, C, D]` (4 lists)
```
Round 1 (pair up):  merge(A,B)=AB,  merge(C,D)=CD     → [AB, CD]
Round 2:            merge(AB,CD)=ABCD                 → [ABCD]
2 rounds = ⌈log2 4⌉; each round walks all N nodes once → O(N log k) ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.empty()) return nullptr;
        int interval = 1, n = lists.size();
        while (interval < n) {
            for (int i = 0; i + interval < n; i += interval * 2)
                lists[i] = mergeTwo(lists[i], lists[i + interval]);
            interval *= 2;
        }
        return lists[0];
    }
private:
    ListNode* mergeTwo(ListNode* a, ListNode* b) {
        ListNode dummy(0);
        ListNode* tail = &dummy;
        while (a && b) {
            if (a->val <= b->val) { tail->next = a; a = a->next; }
            else                  { tail->next = b; b = b->next; }
            tail = tail->next;
        }
        tail->next = a ? a : b;
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode mergeKLists(ListNode[] lists) {
        if (lists.length == 0) return null;
        int interval = 1, n = lists.length;
        while (interval < n) {
            for (int i = 0; i + interval < n; i += interval * 2)
                lists[i] = mergeTwo(lists[i], lists[i + interval]);
            interval *= 2;
        }
        return lists[0];
    }
    private ListNode mergeTwo(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (a != null && b != null) {
            if (a.val <= b.val) { tail.next = a; a = a.next; }
            else                { tail.next = b; b = b.next; }
            tail = tail.next;
        }
        tail.next = (a != null) ? a : b;
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        if not lists:
            return None
        interval, n = 1, len(lists)
        while interval < n:
            for i in range(0, n - interval, interval * 2):
                lists[i] = self._merge_two(lists[i], lists[i + interval])
            interval *= 2
        return lists[0]

    def _merge_two(self, a: ListNode, b: ListNode) -> ListNode:
        dummy = ListNode(0)
        tail = dummy
        while a and b:
            if a.val <= b.val:
                tail.next, a = a, a.next
            else:
                tail.next, b = b, b.next
            tail = tail.next
        tail.next = a if a else b
        return dummy.next
```

### Complexity
- **Time**: O(N log k) — ⌈log₂ k⌉ rounds, each merging a total of `N` nodes.
- **Space**: O(1) for the iterative version (O(log k) recursion stack if written recursively).

### Verdict
Equally optimal and often the fastest in practice because it avoids heap overhead and pointer chasing. No comparator subtleties. A great answer to pair with the heap solution when asked "any other way?"

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Sequential merge | O(N·k) | O(1) | simple; re-walks the growing prefix |
| Min-heap | O(N log k) | O(k) | most intuitive optimal ⭐ |
| Divide & conquer | O(N log k) | O(1) iter / O(log k) rec | no heap; often fastest in practice |

Here `N` = total nodes, `k` = number of lists.

---

## 🧪 Edge cases & pitfalls
- **Empty input** (`lists = []`) → return null. The heap stays empty; divide & conquer guards with the `if empty` check.
- **List of empty lists** (`[[]]`, `[[], []]`) → no nodes are ever pushed/merged → null.
- **Some lists empty, some not** → skip null heads when seeding the heap; `mergeTwo` handles null operands.
- **Pitfall (Python heap) — comparing nodes**: pushing `(val, node)` crashes when two `val`s tie because Python then compares `node` objects. Add a unique tiebreaker like the list index: `(val, i, node)`.
- **Pitfall (C++ heap) — wrong comparator direction**: `a->val > b->val` yields a **min**-heap with `priority_queue`. Getting it backwards merges in descending order.
- **Pitfall (divide & conquer) — loop bound**: the inner loop must use `i + interval < n` so you never merge a list with a non-existent partner; the unpaired tail list simply carries to the next round.

---

## 🔗 Related problems
- **Merge Two Sorted Lists** (LC 21) — the merge subroutine all three approaches rely on. See [`02-Merge-Two-Sorted-Lists.md`](./02-Merge-Two-Sorted-Lists.md).
- **Sort List** (LC 148) — merge sort on a single linked list.
- **Kth Smallest Element in a Sorted Matrix** (LC 378) — heap over `k` sorted rows, same idea.
- **Find K Pairs with Smallest Sums** (LC 373) — heap merge over multiple sequences.

---

**→ Next:** [`11-Reverse-Nodes-In-K-Group.md`](./11-Reverse-Nodes-In-K-Group.md) | **← Prev:** [`09-LRU-Cache.md`](./09-LRU-Cache.md) | Back to [`00-Index.md`](./00-Index.md)
