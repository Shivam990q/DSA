# Remove Nth Node From End of List

**Platform**: LeetCode 19 · **Difficulty**: Medium · **Topics**: Linked List, Two Pointers · **Pattern**: Two pointers with a fixed gap + dummy node

---

## 📜 Problem Statement

Given the `head` of a linked list, remove the `n`-th node from the end of the list and return its head.

### Examples

**Example 1:**
```
Input:  head = [1, 2, 3, 4, 5], n = 2
Output: [1, 2, 3, 5]
Explanation: The 2nd node from the end is the node with value 4; remove it.
```

**Example 2:**
```
Input:  head = [1], n = 1
Output: []
```

**Example 3:**
```
Input:  head = [1, 2], n = 1
Output: [1]
```

### Constraints
```
The number of nodes in the list is sz.
1 <= sz <= 30
1 <= n <= sz
```

**Follow-up:** Could you do this in one pass?

---

## 🧠 Understanding the problem

"`n`-th from the end" is awkward because singly linked lists only let us walk **forward**. If we knew the length `L`, the target would be the `(L - n)`-th node from the front (0-indexed), and we'd stop one node *before* it to splice it out.

To delete a node in a singly linked list we need a handle on its **predecessor**, so we can set `predecessor.next = target.next`. The pesky case is deleting the head itself (when `n == L`) — there's no predecessor. The **dummy node** placed before `head` gives every real node, including the head, a predecessor, erasing that special case.

The follow-up asks for one pass. The trick: launch a `fast` pointer `n` steps ahead of a `slow` pointer, then move both together. When `fast` reaches the end, `slow` is exactly `n` nodes from the end — sitting on the predecessor if we offset things by one with the dummy.

---

## Approach 1 — Two passes (compute length, then delete)

### Intuition
First pass measures the length `L`. The node to remove is at index `L - n` from the front. Walk a second time to the node *before* it (index `L - n - 1`, which is why the dummy helps) and unlink.

### Algorithm
1. Create `dummy` with `dummy.next = head`.
2. Pass 1: count nodes → `L`.
3. Pass 2: from `dummy`, take `L - n` steps to reach the predecessor.
4. `prev.next = prev.next.next`.
5. Return `dummy.next`.

### Dry run on `[1, 2, 3, 4, 5]`, `n = 2`
```
L = 5. Target from front = L - n = 3 (value 4). Predecessor index from dummy = 3.
dummy → 1 → 2 → 3 → 4 → 5
walk 3 steps from dummy: dummy→1→2→3, prev = node(3)
prev.next = prev.next.next  → 3.next = 5
result: 1 → 2 → 3 → 5 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0);
        dummy.next = head;
        int len = 0;
        for (ListNode* cur = head; cur; cur = cur->next) len++;
        ListNode* prev = &dummy;
        for (int i = 0; i < len - n; i++) prev = prev->next;
        prev->next = prev->next->next;
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        int len = 0;
        for (ListNode cur = head; cur != null; cur = cur.next) len++;
        ListNode prev = dummy;
        for (int i = 0; i < len - n; i++) prev = prev.next;
        prev.next = prev.next.next;
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)
        length = 0
        cur = head
        while cur:
            length += 1
            cur = cur.next
        prev = dummy
        for _ in range(length - n):
            prev = prev.next
        prev.next = prev.next.next
        return dummy.next
```

### Complexity
- **Time**: O(L) — two linear passes, still O(n) overall.
- **Space**: O(1).

### Verdict
Perfectly correct and arguably the clearest to explain. The only knock is it reads the list twice; the follow-up wants a single pass.

---

## Approach 2 — One pass, two pointers with a fixed gap (optimal) ⭐

### Intuition
Put `fast` `n + 1` steps ahead of `slow` (the `+1` so `slow` lands on the *predecessor*, thanks to the dummy). Then advance both one step at a time. When `fast` falls off the end (becomes null), `slow` is exactly one node before the target. Unlink and done — one traversal.

### Algorithm
1. Create `dummy` with `dummy.next = head`. Set `fast = slow = dummy`.
2. Advance `fast` by `n + 1` steps.
3. While `fast` is not null: advance both `fast` and `slow`.
4. `slow.next = slow.next.next`.
5. Return `dummy.next`.

### Dry run on `[1, 2, 3, 4, 5]`, `n = 2`
```
dummy → 1 → 2 → 3 → 4 → 5
fast = slow = dummy

advance fast by n+1 = 3:  fast = node(3)
move both until fast == null:
  fast=4 slow=1
  fast=5 slow=2
  fast=null slow=3   ← stop
slow = node(3). slow.next = node(4).next = node(5)
result: 1 → 2 → 3 → 5 ✅
```

Dry run on `[1]`, `n = 1` (removing the head):
```
dummy → 1
advance fast by 2: fast = null (dummy→1→null)
loop doesn't run; slow = dummy
slow.next = slow.next.next → dummy.next = null
result: [] ✅   (dummy node made the head-deletion trivial)
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode *fast = &dummy, *slow = &dummy;
        for (int i = 0; i <= n; i++) fast = fast->next;  // n+1 steps ahead
        while (fast) {
            fast = fast->next;
            slow = slow->next;
        }
        slow->next = slow->next->next;
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode fast = dummy, slow = dummy;
        for (int i = 0; i <= n; i++) fast = fast.next;  // n+1 steps ahead
        while (fast != null) {
            fast = fast.next;
            slow = slow.next;
        }
        slow.next = slow.next.next;
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)
        fast = slow = dummy
        for _ in range(n + 1):       # n+1 steps ahead
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next = slow.next.next
        return dummy.next
```

### Complexity
- **Time**: O(L) — a single traversal.
- **Space**: O(1).

### Verdict
The intended optimal solution. The `n + 1` gap plus the dummy node is the elegant part: it makes "remove the head" and "remove a middle node" the exact same code path.

---

## ⚖️ Approach comparison

| Approach | Passes | Time | Space | Notes |
|----------|--------|------|-------|-------|
| Length then delete | 2 | O(L) | O(1) | clearest to explain |
| Two-pointer gap | 1 | O(L) | O(1) | satisfies the one-pass follow-up ⭐ |

Both are linear and constant space; the difference is whether you touch the list once or twice. In an interview, lead with the two-pass to show understanding, then deliver the one-pass for the follow-up.

---

## 🧪 Edge cases & pitfalls
- **Remove the head** (`n == L`) → the dummy node provides a predecessor so no special case is needed.
- **Single-node list** (`[1], n = 1`) → result is empty; dummy makes this clean.
- **Pitfall — off-by-one on the gap**: advancing `fast` by `n` instead of `n + 1` leaves `slow` *on* the target rather than its predecessor, deleting the wrong node. Use `n + 1`.
- **Pitfall — no dummy node**: deleting the head then needs a separate branch; easy to get wrong. The dummy removes it.
- **Pitfall — assuming `n` could exceed length**: constraints guarantee `1 <= n <= sz`, so we don't need to validate, but the dummy still protects the head case.

---

## 🔗 Related problems
- **Middle of the Linked List** (LC 876) — same "two pointers, one faster" idea to find a positional node.
- **Linked List Cycle** (LC 141) — fast/slow pointers. See [`03-Linked-List-Cycle.md`](./03-Linked-List-Cycle.md).
- **Delete Node in a Linked List** (LC 237) — deletion given only the node itself (copy-next trick).
- **Remove Linked List Elements** (LC 203) — delete by value using a dummy node.

---

**→ Next:** [`06-Copy-List-With-Random-Pointer.md`](./06-Copy-List-With-Random-Pointer.md) | **← Prev:** [`04-Reorder-List.md`](./04-Reorder-List.md) | Back to [`00-Index.md`](./00-Index.md)
