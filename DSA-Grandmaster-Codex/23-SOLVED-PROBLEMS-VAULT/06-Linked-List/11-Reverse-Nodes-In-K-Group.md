# Reverse Nodes in K-Group

**Platform**: LeetCode 25 · **Difficulty**: Hard · **Topics**: Linked List, Recursion · **Pattern**: Grouped in-place reversal

---

## 📜 Problem Statement

Given the `head` of a linked list, reverse the nodes of the list `k` at a time, and return *the modified list*.

`k` is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k` then left-out nodes, in the end, should remain as it is.

You may **not** alter the values in the list's nodes, only nodes themselves may be changed.

### Examples

**Example 1:**
```
Input:  head = [1, 2, 3, 4, 5], k = 2
Output: [2, 1, 4, 3, 5]
```

**Example 2:**
```
Input:  head = [1, 2, 3, 4, 5], k = 3
Output: [3, 2, 1, 4, 5]
```

**Example 3:**
```
Input:  head = [1, 2, 3, 4, 5], k = 1
Output: [1, 2, 3, 4, 5]
```

### Constraints
```
The number of nodes in the list is n.
1 <= k <= n <= 5000
0 <= Node.val <= 1000
```

**Follow-up:** Can you solve the problem in O(1) extra memory space?

---

## 🧠 Understanding the problem

This is "Reverse Linked List" (LC 206) applied to fixed-size chunks, with one strict rule: a chunk is reversed **only if it has a full `k` nodes**. The final partial chunk (fewer than `k` nodes) stays untouched.

So the work splits into two responsibilities:
1. **Detect** whether the next `k` nodes exist. If not, leave the rest alone.
2. **Reverse exactly `k` nodes**, then stitch the reversed block between the previous block's tail and the next block's start.

The connection bookkeeping is the delicate part. After reversing a group, its original *head* becomes the group's *tail*, and that tail must point to whatever the next group resolves to. A **dummy node** before `head` gives us a stable "previous group tail" to anchor the first connection, eliminating the special case for the very first group.

The follow-up asks for O(1) extra space, which means an iterative solution (recursion costs O(n/k) stack frames).

---

## Approach 1 — Recursion

### Intuition
Process one group at a time. First check there are `k` nodes ahead; if not, return `head` unchanged (this is the leftover tail). Otherwise, recursively reverse *everything after* this group, then reverse this group's `k` nodes and attach the reversed-rest to the new tail.

### Algorithm
1. Walk `k` nodes from `head`. If you hit null before `k` → fewer than `k` remain → return `head` as-is.
2. Let `node` be the (k+1)-th node. Recurse: `prev = reverseKGroup(node, k)` — the head of the already-reversed remainder.
3. Reverse this group's `k` nodes, threading each onto `prev` (so the group's original head ends up pointing into the reversed remainder).
4. Return the new group head (the k-th original node).

### Dry run on `[1, 2, 3, 4, 5]`, `k = 2`
```
reverseKGroup(1, 2):
  check 2 nodes ahead: 1,2 exist → node = 3
  prev = reverseKGroup(3, 2):
      check: 3,4 exist → node = 5
      prev = reverseKGroup(5, 2):
          check: 5 then null → fewer than 2 → return 5
      reverse [3,4] onto prev=5:
          3.next=5→prev=3 ; 4.next=3→prev=4   group head = 4 → 4->3->5
      return 4   (so 3->5, and 4 heads it: 4->3->5)
  reverse [1,2] onto prev=4:
      1.next=4→prev=1 ; 2.next=1→prev=2        group head = 2 → 2->1->4->3->5
  return 2
result: 2 -> 1 -> 4 -> 3 -> 5 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        // 1. check there are at least k nodes
        ListNode* node = head;
        for (int i = 0; i < k; i++) {
            if (!node) return head;   // fewer than k → leave as-is
            node = node->next;
        }
        // 2. reverse the rest first
        ListNode* prev = reverseKGroup(node, k);
        // 3. reverse this group of k, threading onto prev
        ListNode* cur = head;
        for (int i = 0; i < k; i++) {
            ListNode* nxt = cur->next;
            cur->next = prev;
            prev = cur;
            cur = nxt;
        }
        return prev;  // new head of this group
    }
};
```

**Java**
```java
class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        // 1. check there are at least k nodes
        ListNode node = head;
        for (int i = 0; i < k; i++) {
            if (node == null) return head;   // fewer than k → leave as-is
            node = node.next;
        }
        // 2. reverse the rest first
        ListNode prev = reverseKGroup(node, k);
        // 3. reverse this group of k, threading onto prev
        ListNode cur = head;
        for (int i = 0; i < k; i++) {
            ListNode nxt = cur.next;
            cur.next = prev;
            prev = cur;
            cur = nxt;
        }
        return prev;  // new head of this group
    }
}
```

**Python**
```python
class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        # 1. check there are at least k nodes
        node = head
        for _ in range(k):
            if not node:
                return head          # fewer than k → leave as-is
            node = node.next
        # 2. reverse the rest first
        prev = self.reverseKGroup(node, k)
        # 3. reverse this group of k, threading onto prev
        cur = head
        for _ in range(k):
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        return prev                  # new head of this group
```

### Complexity
- **Time**: O(n) — each node is visited a constant number of times (once to count, once to reverse).
- **Space**: O(n / k) — one recursion frame per group.

### Verdict
The cleanest to write and reason about. The "reverse the rest, then prepend this group" structure mirrors recursive list reversal. Downside: the recursion stack is O(n/k), so it doesn't satisfy the O(1) follow-up.

---

## Approach 2 — Iterative with a dummy node (O(1) space) ⭐

### Intuition
Process groups left to right, anchored by a `groupPrev` pointer (initially the dummy) that always points to the node *before* the current group. For each group:
- Confirm `k` nodes exist by walking from `groupPrev` (find the `kth` node).
- Reverse the `k` nodes in place.
- Re-stitch: `groupPrev.next` should point to the new group head (the old `kth` node); the old group head becomes the new tail and must point to the next group's first node.
- Advance `groupPrev` to the group's new tail (the old group head).

No recursion → O(1) extra space.

### Algorithm
1. `dummy.next = head`; `groupPrev = dummy`.
2. Loop:
   - Find `kth = groupPrev` advanced `k` steps. If `kth` is null → fewer than `k` remain → break.
   - `groupNext = kth.next`.
   - Reverse the group: set `prev = groupNext`, `cur = groupPrev.next`; repeatedly move `cur` onto `prev` until `cur == groupNext`.
   - Now the old group head is `groupPrev.next`. Save it as the new tail; set `groupPrev.next = kth` (new head); advance `groupPrev = newTail`.
3. Return `dummy.next`.

### Dry run on `[1, 2, 3, 4, 5]`, `k = 3`
```
dummy → 1 → 2 → 3 → 4 → 5    groupPrev = dummy

Group 1: kth = node 3 (3 steps from dummy). groupNext = 4.
  Reverse 1,2,3 with prev starting at groupNext=4:
    1.next=4  prev=1
    2.next=1  prev=2
    3.next=2  prev=3
  old head = 1 (= groupPrev.next). newTail = 1.
  groupPrev.next = kth = 3  →  dummy → 3 → 2 → 1 → 4 → 5
  groupPrev = 1 (the new tail)

Group 2: walk k=3 from groupPrev(1): 1→4→5→null  kth = null → break

result: 3 → 2 → 1 → 4 → 5 ✅  (leftover 4,5 untouched)
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* reverseKGroup(ListNode* head, int k) {
        ListNode dummy(0);
        dummy.next = head;
        ListNode* groupPrev = &dummy;

        while (true) {
            // find the k-th node from groupPrev
            ListNode* kth = groupPrev;
            for (int i = 0; i < k && kth; i++) kth = kth->next;
            if (!kth) break;                 // fewer than k remain

            ListNode* groupNext = kth->next;

            // reverse the group [groupPrev.next .. kth]
            ListNode* prev = groupNext;
            ListNode* cur = groupPrev->next;
            while (cur != groupNext) {
                ListNode* nxt = cur->next;
                cur->next = prev;
                prev = cur;
                cur = nxt;
            }

            // re-stitch
            ListNode* newTail = groupPrev->next;  // old head, now tail
            groupPrev->next = kth;                // kth is the new head
            groupPrev = newTail;
        }
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode dummy = new ListNode(0);
        dummy.next = head;
        ListNode groupPrev = dummy;

        while (true) {
            // find the k-th node from groupPrev
            ListNode kth = groupPrev;
            for (int i = 0; i < k && kth != null; i++) kth = kth.next;
            if (kth == null) break;          // fewer than k remain

            ListNode groupNext = kth.next;

            // reverse the group [groupPrev.next .. kth]
            ListNode prev = groupNext;
            ListNode cur = groupPrev.next;
            while (cur != groupNext) {
                ListNode nxt = cur.next;
                cur.next = prev;
                prev = cur;
                cur = nxt;
            }

            // re-stitch
            ListNode newTail = groupPrev.next;   // old head, now tail
            groupPrev.next = kth;                // kth is the new head
            groupPrev = newTail;
        }
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def reverseKGroup(self, head: ListNode, k: int) -> ListNode:
        dummy = ListNode(0)
        dummy.next = head
        group_prev = dummy

        while True:
            # find the k-th node from group_prev
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    break
            if not kth:
                return dummy.next        # fewer than k remain

            group_next = kth.next

            # reverse the group [group_prev.next .. kth]
            prev, cur = group_next, group_prev.next
            while cur != group_next:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt

            # re-stitch
            new_tail = group_prev.next   # old head, now tail
            group_prev.next = kth        # kth is the new head
            group_prev = new_tail
```

### Complexity
- **Time**: O(n) — each node is counted once and reversed once.
- **Space**: O(1) — only a fixed set of pointers; satisfies the follow-up.

### Verdict
The space-optimal answer and the one to deliver for the follow-up. The trick that makes it clean: initializing `prev = groupNext` so the reversed group's tail *already* points at the next group, then just resetting `groupPrev.next = kth`. Trace the re-stitch on paper once and it becomes mechanical.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Recursive | O(n) | O(n/k) stack | cleanest to write; fails O(1) follow-up |
| Iterative + dummy | O(n) | **O(1)** | optimal; the expected follow-up answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **`k = 1`** → every "group" is a single node; reversing one node is a no-op → list unchanged. Both approaches handle it.
- **`n` not divisible by `k`** → the final short group is detected by the "is there a k-th node?" check and left untouched (Examples 2 reverses `1,2,3` but leaves `4,5`).
- **`k = n`** → the whole list reverses exactly once.
- **Pitfall — reversing a partial last group**: you must verify `k` full nodes *before* touching them. Reverse-then-check would corrupt the leftover tail.
- **Pitfall — broken stitches**: after reversing, three links matter — `groupPrev.next` → new head, old head → next group, and `groupPrev` advances to the old head. Drop any one and the list fragments or cycles.
- **Pitfall (iterative) — `prev` initialization**: start `prev = groupNext` (not null) so the group's new tail links to the next group automatically. Starting at null would terminate the list early.
- **Pitfall — counting from the wrong anchor**: count the `k`-th node starting from `groupPrev`, so `kth` lands on the last node of the current group (and `groupPrev.next` is the current group's first node).

---

## 🔗 Related problems
- **Reverse Linked List** (LC 206) — the core reversal this generalizes. See [`01-Reverse-Linked-List.md`](./01-Reverse-Linked-List.md).
- **Reverse Linked List II** (LC 92) — reverse a single sublist between two positions.
- **Swap Nodes in Pairs** (LC 24) — exactly this problem with `k = 2`.
- **Rotate List** (LC 61) — another re-threading problem using length and a pointer offset.

---

**→ Next topic:** [`../07-Trees/00-Index.md`](../07-Trees/00-Index.md) | Back to [`00-Index.md`](./00-Index.md) | **← Prev:** [`10-Merge-K-Sorted-Lists.md`](./10-Merge-K-Sorted-Lists.md)
