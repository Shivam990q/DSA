# Linked List Cycle

**Platform**: LeetCode 141 · **Difficulty**: Easy · **Topics**: Linked List, Two Pointers, Hash Table · **Pattern**: Floyd's tortoise & hare

---

## 📜 Problem Statement

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. **Note that `pos` is not passed as a parameter.**

Return `true` *if there is a cycle in the linked list. Otherwise, return* `false`.

### Examples

**Example 1:**
```
Input:  head = [3, 2, 0, -4], pos = 1
Output: true
Explanation: There is a cycle, where the tail connects to the 1st node (0-indexed).
```

**Example 2:**
```
Input:  head = [1, 2], pos = 0
Output: true
Explanation: There is a cycle, where the tail connects to the 0th node.
```

**Example 3:**
```
Input:  head = [1], pos = -1
Output: false
Explanation: There is no cycle.
```

### Constraints
```
The number of the nodes in the list is in the range [0, 10^4].
-10^5 <= Node.val <= 10^5
pos is -1 or a valid index in the linked-list.
```

**Follow-up:** Can you solve it using O(1) (i.e. constant) memory?

---

## 🧠 Understanding the problem

A "cycle" means following `next` repeatedly never reaches null — you loop forever inside some suffix of the list. We must decide *yes/no* whether such a loop exists.

The naive mental model is "walk until null → no cycle; but if there's a cycle, walking never terminates." So the challenge is detecting the loop **without running forever** and ideally without extra memory (the follow-up).

Two clean ideas:
1. **Remember every node you've visited.** If you ever arrive at a node you've already seen, that's the cycle. Costs O(n) memory.
2. **Two runners at different speeds.** On a circular track, a faster runner eventually laps a slower one. If `next` ever leads to null, no track — no cycle. This is O(1) memory and is the intended answer.

---

## Approach 1 — Hash set of visited nodes

### Intuition
Walk the list node by node, recording each node's identity (the pointer/reference itself, not its value — values can repeat). The first time you revisit a node, you've closed a loop. If you reach null, the walk terminated, so there is no cycle.

### Algorithm
1. Create an empty set `seen`.
2. Walk `cur` from `head`:
   - If `cur` is null → return `false`.
   - If `cur` is already in `seen` → return `true`.
   - Insert `cur` into `seen`; advance `cur = cur.next`.

### Dry run on `[3, 2, 0, -4]` with tail linking back to node `2` (index 1)
```
cur=3  → not seen → add {3}
cur=2  → not seen → add {3,2}
cur=0  → not seen → add {3,2,0}
cur=-4 → not seen → add {3,2,0,-4}
cur=2  → ALREADY in set → return true ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    bool hasCycle(ListNode *head) {
        unordered_set<ListNode*> seen;
        for (ListNode* cur = head; cur; cur = cur->next) {
            if (seen.count(cur)) return true;
            seen.insert(cur);
        }
        return false;
    }
};
```

**Java**
```java
public class Solution {
    public boolean hasCycle(ListNode head) {
        Set<ListNode> seen = new HashSet<>();
        for (ListNode cur = head; cur != null; cur = cur.next) {
            if (!seen.add(cur)) return true;  // add returns false if already present
        }
        return false;
    }
}
```

**Python**
```python
class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        seen = set()
        cur = head
        while cur:
            if cur in seen:
                return True
            seen.add(cur)
            cur = cur.next
        return False
```

### Complexity
- **Time**: O(n) — each node inspected once before either revisiting or hitting null.
- **Space**: O(n) — the set may hold every node.

### Verdict
Simple and bulletproof. The downside is O(n) memory, which fails the follow-up. Good as the first thing you say before optimizing.

---

## Approach 2 — Floyd's tortoise & hare (optimal) ⭐

### Intuition
Send two pointers from the head: `slow` advances one node per step, `fast` advances two. If there is no cycle, `fast` reaches the end (null) and we stop. If there *is* a cycle, both pointers eventually enter the loop, and since `fast` gains one node on `slow` every step, the gap closes by one each iteration — they are guaranteed to land on the same node. It's the classic "two runners on a circular track" argument: the faster one always catches the slower one.

### Algorithm
1. Set `slow = head`, `fast = head`.
2. While `fast` and `fast.next` are non-null:
   - `slow = slow.next` (one step).
   - `fast = fast.next.next` (two steps).
   - If `slow == fast` → return `true`.
3. `fast` hit null → return `false`.

### Why are they guaranteed to meet?
Once both are inside the cycle of length `L`, consider the distance from `fast` to `slow` measured *forward around the loop*. Each step, `slow` moves +1 and `fast` moves +2, so that distance shrinks by exactly 1 (mod L) per step. A non-negative integer distance that decreases by 1 each step must hit 0 — that's the meeting. It can never "jump over" because the change is exactly 1.

### Dry run on `[1, 2, 3, 4]` with tail linking back to node `2` (index 1)
```
List:  1 → 2 → 3 → 4 ┐
                 ↑─────┘  (4.next = 2)

start: slow=1 fast=1
step1: slow=2 fast=3        (2 != 3)
step2: slow=3 fast=2        fast: 3→4→2   (3 != 2)
step3: slow=4 fast=4        fast: 2→3→4   slow==fast=4 → return true ✅
```

Dry run with no cycle `[1, 2, 3]`:
```
start: slow=1 fast=1
step1: slow=2 fast=3
loop check: fast.next == null → exit → return false ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    bool hasCycle(ListNode *head) {
        ListNode *slow = head, *fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) return true;
        }
        return false;
    }
};
```

**Java**
```java
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}
```

**Python**
```python
class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
```

### Complexity
- **Time**: O(n) — before meeting, the pointers traverse at most O(n) nodes (slow makes ≤ n steps).
- **Space**: O(1) — two pointers. Satisfies the follow-up.

### Verdict
The textbook optimal answer. Constant memory, linear time. The same machinery extends to *finding* the cycle's entrance (LC 142) and to Find the Duplicate Number (LC 287).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Hash set | O(n) | O(n) | simplest to reason about; fails the O(1) follow-up |
| Floyd fast/slow | O(n) | **O(1)** | optimal; the intended answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Empty list** (`head == null`) → the `while` guard is false immediately → `false`.
- **Single node, no self-loop** → `fast.next` is null → `false`.
- **Single node with self-loop** (`head.next == head`) → after one step `slow == fast` → `true`.
- **Pitfall — checking `slow == fast` before moving**: if you compare them while both still equal `head`, you falsely report a cycle on step zero. Move first, then compare.
- **Pitfall — wrong loop guard**: you must check both `fast` and `fast.next` before doing `fast.next.next`, or you'll dereference null.
- **Pitfall — comparing values not identity**: in the hash-set approach, store the node reference, not `node.val` (values can repeat without a cycle).

---

## 🔗 Related problems
- **Linked List Cycle II** (LC 142) — return the node where the cycle begins (Floyd + a second walk from head).
- **Find the Duplicate Number** (LC 287) — array reinterpreted as a linked list; same Floyd detection. See [`08-Find-The-Duplicate-Number.md`](./08-Find-The-Duplicate-Number.md).
- **Happy Number** (LC 202) — cycle detection on a number-transformation sequence.
- **Middle of the Linked List** (LC 876) — fast/slow to find the midpoint.

---

**→ Next:** [`04-Reorder-List.md`](./04-Reorder-List.md) | **← Prev:** [`02-Merge-Two-Sorted-Lists.md`](./02-Merge-Two-Sorted-Lists.md) | Back to [`00-Index.md`](./00-Index.md)
