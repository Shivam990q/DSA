# Reverse Linked List

**Platform**: LeetCode 206 · **Difficulty**: Easy · **Topics**: Linked List, Recursion · **Pattern**: In-place 3-pointer reversal

---

## 📜 Problem Statement

Given the `head` of a singly linked list, reverse the list, and return *the reversed list*.

### Examples

**Example 1:**
```
Input:  head = [1, 2, 3, 4, 5]
Output: [5, 4, 3, 2, 1]
```

**Example 2:**
```
Input:  head = [1, 2]
Output: [2, 1]
```

**Example 3:**
```
Input:  head = []
Output: []
```

### Constraints
```
The number of nodes in the list is in the range [0, 5000].
-5000 <= Node.val <= 5000
```

**Follow-up:** A linked list can be reversed either iteratively or recursively. Could you implement both?

---

## 🧠 Understanding the problem

Reversing a singly linked list means that the node that *was* last becomes the new head, and every `next` pointer flips to point at what used to be its predecessor. We are not allowed to read the list backwards (singly linked — there are no `prev` pointers), so we cannot "walk to the end and come back." Instead we must physically re-thread the `next` pointers as we go.

The one trap that catches everyone: the moment you set `cur->next = prev`, you have **destroyed the link to the rest of the list**. So before you overwrite `cur->next`, you must save it. That single observation — *save the next node first* — is the whole problem.

We want this in O(1) extra space if possible, which rules out copying values into an array and rebuilding. The classic solution carries exactly three references: the node behind us (`prev`), the node we're on (`cur`/`head`), and the node ahead (`next`).

---

## Approach 1 — Iterative three-pointer reversal (optimal) ⭐

### Intuition
Imagine standing on each node in turn. For the current node, you want its arrow to point **backwards** to the node you just came from. You keep a `prev` pointer for "the node I came from." But flipping `cur->next` to `prev` loses the forward link, so you stash `cur->next` in a temporary `next` before flipping. Then everybody shuffles one step forward: `prev` becomes `cur`, `cur` becomes the saved `next`.

When `cur` falls off the end (becomes null), `prev` is sitting on the old last node — which is exactly the new head.

### Algorithm
1. Initialize `prev = null`, `cur = head`.
2. While `cur` is not null:
   - Save `next = cur->next`.
   - Re-point `cur->next = prev`.
   - Advance `prev = cur`.
   - Advance `cur = next`.
3. Return `prev` (the new head).

### Dry run on `[1, 2, 3]`
```
start:  prev=null  cur=1->2->3

iter 1: next=2
        1.next=null            (1 now points back to nothing)
        prev=1                 cur=2
        state: 1   2->3

iter 2: next=3
        2.next=1               (2 now points to 1)
        prev=2                 cur=3
        state: 2->1   3

iter 3: next=null
        3.next=2               (3 now points to 2)
        prev=3                 cur=null
        state: 3->2->1

cur==null → return prev = 3  →  list is 3->2->1 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* prev = nullptr;
        ListNode* cur = head;
        while (cur) {
            ListNode* next = cur->next;  // save the rest of the list
            cur->next = prev;            // flip the pointer
            prev = cur;                  // advance prev
            cur = next;                  // advance cur
        }
        return prev;
    }
};
```

**Java**
```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode cur = head;
        while (cur != null) {
            ListNode next = cur.next;  // save the rest of the list
            cur.next = prev;           // flip the pointer
            prev = cur;                // advance prev
            cur = next;                // advance cur
        }
        return prev;
    }
}
```

**Python**
```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        cur = head
        while cur:
            nxt = cur.next   # save the rest of the list
            cur.next = prev  # flip the pointer
            prev = cur       # advance prev
            cur = nxt        # advance cur
        return prev
```

### Complexity
- **Time**: O(n) — each node visited exactly once.
- **Space**: O(1) — only three pointers, regardless of list size.

### Verdict
The canonical answer. Constant space, single pass, no recursion depth worries. This is what you write first in an interview.

---

## Approach 2 — Recursion

### Intuition
Trust recursion to reverse everything *after* the head. Suppose `reverseList(head->next)` correctly returns the new head of the reversed tail. After that call, `head->next` is still pointing at the node that is now the **last** node of the reversed tail. So to attach `head` to the end, we do `head->next->next = head` (make the old second node point back to `head`), then sever `head->next` to null so `head` becomes the new tail.

### Algorithm
1. Base case: if `head` is null or `head->next` is null, return `head` (empty or single node is its own reverse).
2. Recurse: `newHead = reverseList(head->next)`.
3. `head->next->next = head` — the next node now points back to us.
4. `head->next = null` — we are the new tail.
5. Return `newHead` (unchanged all the way up the stack).

### Dry run on `[1, 2, 3]`
```
reverseList(1) → reverseList(2) → reverseList(3)
  reverseList(3): head.next is null → return 3   (newHead = 3)

back in reverseList(2): head=2, head.next=3
  3.next = 2     → 3->2
  2.next = null  → 2 is tail
  return 3

back in reverseList(1): head=1, head.next=2
  2.next = 1     → 2->1
  1.next = null  → 1 is tail
  return 3

final: 3->2->1 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if (!head || !head->next) return head;
        ListNode* newHead = reverseList(head->next);
        head->next->next = head;  // tail node points back to head
        head->next = nullptr;     // head becomes the new tail
        return newHead;
    }
};
```

**Java**
```java
class Solution {
    public ListNode reverseList(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode newHead = reverseList(head.next);
        head.next.next = head;  // tail node points back to head
        head.next = null;       // head becomes the new tail
        return newHead;
    }
}
```

**Python**
```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head or not head.next:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head  # tail node points back to head
        head.next = None       # head becomes the new tail
        return new_head
```

### Complexity
- **Time**: O(n) — one call per node.
- **Space**: O(n) — recursion stack depth equals the list length (up to 5000 frames here, which is safe, but on a 10⁶-node list this would stack-overflow).

### Verdict
Elegant and great for demonstrating recursive reasoning, but the O(n) stack is a real downside on long lists. Prefer the iterative version in production; mention recursion as the "could you also..." follow-up.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Iterative 3-pointer | O(n) | **O(1)** | the default optimal answer ⭐ |
| Recursive | O(n) | O(n) stack | elegant, but risks stack overflow on long lists |

Both are O(n) time. The only differentiator is space: the iterative version is strictly better. The recursive version is worth knowing because the "reverse the tail, then fix up the link" idea reappears in harder problems (Reverse Nodes in K-Group).

---

## 🧪 Edge cases & pitfalls
- **Empty list** (`head == null`) → both approaches return null immediately.
- **Single node** → reverse of itself; loop runs once / recursion hits base case.
- **Pitfall — losing the rest of the list**: if you write `cur->next = prev` *before* saving `cur->next`, you orphan everything ahead. Always save `next` first.
- **Pitfall — returning `head` instead of `prev`**: after the loop, `head`/`cur` is null. The new head is `prev`. Returning the wrong variable gives an empty list.
- **Pitfall (recursion) — forgetting `head->next = null`**: omit it and the original head still points forward, creating a 2-node cycle (`1 ⇄ 2`).

---

## 🔗 Related problems
- **Reverse Linked List II** (LC 92) — reverse only the sublist between positions `left` and `right`.
- **Reverse Nodes in K-Group** (LC 25) — repeatedly reverse fixed-size chunks. See [`11-Reverse-Nodes-In-K-Group.md`](./11-Reverse-Nodes-In-K-Group.md).
- **Reorder List** (LC 143) — uses reversal of the second half. See [`04-Reorder-List.md`](./04-Reorder-List.md).
- **Palindrome Linked List** (LC 234) — reverse half the list and compare.

---

**→ Next:** [`02-Merge-Two-Sorted-Lists.md`](./02-Merge-Two-Sorted-Lists.md) | Back to [`00-Index.md`](./00-Index.md)
