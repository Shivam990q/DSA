# Reorder List

**Platform**: LeetCode 143 · **Difficulty**: Medium · **Topics**: Linked List, Two Pointers, Stack, Recursion · **Pattern**: Find middle + reverse + merge

---

## 📜 Problem Statement

You are given the head of a singly linked-list. The list can be represented as:

```
L0 → L1 → … → Ln-1 → Ln
```

*Reorder the list to be on the following form:*

```
L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …
```

You may **not** modify the values in the list's nodes. Only nodes themselves may be changed.

### Examples

**Example 1:**
```
Input:  head = [1, 2, 3, 4]
Output: [1, 4, 2, 3]
```

**Example 2:**
```
Input:  head = [1, 2, 3, 4, 5]
Output: [1, 5, 2, 4, 3]
```

**Example 3:**
```
Input:  head = [1]
Output: [1]
```

### Constraints
```
The number of nodes in the list is in the range [1, 5 * 10^4].
1 <= Node.val <= 1000
```

---

## 🧠 Understanding the problem

Read the target pattern carefully: we interleave the list from **both ends inward** — first node, last node, second node, second-to-last node, and so on. Equivalently, take the second half of the list, reverse it, and zip it into the first half.

Since we cannot move values (only re-thread pointers), and we'd like O(1) space, the clean decomposition is three well-known subroutines we already own:

1. **Find the middle** (fast/slow pointers) → splits the list into a first half and second half.
2. **Reverse the second half** (3-pointer reversal).
3. **Merge the two halves alternately** (zip them: one from the front, one from the reversed back).

Each piece is a primitive you've practiced; the whole problem is just composing them. The only subtlety is choosing the middle split so that for even and odd lengths the first half is the same length or one longer than the second.

---

## Approach 1 — Array / deque buffer (warm-up)

### Intuition
If we dump all nodes into an array, we have random access. Then we use two indices walking inward from both ends, re-linking `front → back → front+1 → back-1 → …`. Simple, but costs O(n) extra space.

### Algorithm
1. Push every node into a vector `nodes`.
2. Set `i = 0`, `j = nodes.size() - 1`.
3. While `i < j`:
   - `nodes[i].next = nodes[j]`; `i++`.
   - If `i == j` break.
   - `nodes[j].next = nodes[i]`; `j--`.
4. `nodes[i].next = null` to terminate.

### Dry run on `[1, 2, 3, 4]`
```
nodes = [1,2,3,4]   i=0 j=3
1.next=4  i=1
4.next=2  j=2
i(1) < j(2): 2.next=3  i=2
i==j → break
2.next... wait i==j=2 → set nodes[2].next=null → 3.next=null
result: 1->4->2->3 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    void reorderList(ListNode* head) {
        if (!head || !head->next) return;
        vector<ListNode*> nodes;
        for (ListNode* cur = head; cur; cur = cur->next) nodes.push_back(cur);
        int i = 0, j = (int)nodes.size() - 1;
        while (i < j) {
            nodes[i]->next = nodes[j];
            i++;
            if (i == j) break;
            nodes[j]->next = nodes[i];
            j--;
        }
        nodes[i]->next = nullptr;
    }
};
```

**Java**
```java
class Solution {
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) return;
        List<ListNode> nodes = new ArrayList<>();
        for (ListNode cur = head; cur != null; cur = cur.next) nodes.add(cur);
        int i = 0, j = nodes.size() - 1;
        while (i < j) {
            nodes.get(i).next = nodes.get(j);
            i++;
            if (i == j) break;
            nodes.get(j).next = nodes.get(i);
            j--;
        }
        nodes.get(i).next = null;
    }
}
```

**Python**
```python
class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head or not head.next:
            return
        nodes = []
        cur = head
        while cur:
            nodes.append(cur)
            cur = cur.next
        i, j = 0, len(nodes) - 1
        while i < j:
            nodes[i].next = nodes[j]
            i += 1
            if i == j:
                break
            nodes[j].next = nodes[i]
            j -= 1
        nodes[i].next = None
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) for the node array.

### Verdict
Correct and easy to get right under pressure, but the O(n) buffer is unnecessary. Mention it, then improve to O(1) space.

---

## Approach 2 — Middle + reverse + merge (optimal) ⭐

### Intuition
We never need random access if we physically reverse the back half. Steps:
- Use fast/slow to find the middle so we can cut the list into two halves.
- Reverse the second half in place.
- Walk both halves simultaneously, splicing one node from each alternately.

For `[1,2,3,4,5]`: first half `1→2→3`, second half reversed `5→4`. Zipping gives `1→5→2→4→3`.

### Algorithm
1. **Find middle**: `slow = fast = head`; while `fast.next && fast.next.next`, advance `slow` by 1 and `fast` by 2. Now `slow` is the end of the first half.
2. **Split & reverse**: `second = slow.next`; `slow.next = null`. Reverse `second` into `prev`.
3. **Merge alternately**: with `first = head` and `second = prev`, repeatedly splice `first → second → first.next → …`.

### Dry run on `[1, 2, 3, 4, 5]`
```
Find middle: slow stops at 3
  first half:  1 → 2 → 3
  slow.next=null cuts it; second = 4 → 5

Reverse second half: 5 → 4

Merge:
  first=1 second=5
    n1 = 2 (first.next), n2 = 4 (second.next)
    1.next = 5; 5.next = 2     → 1 → 5 → 2 ...
    first = 2; second = 4
  first=2 second=4
    n1 = 3, n2 = null
    2.next = 4; 4.next = 3     → 1 → 5 → 2 → 4 → 3
    first = 3; second = null → stop
result: 1 → 5 → 2 → 4 → 3 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    void reorderList(ListNode* head) {
        if (!head || !head->next) return;

        // 1. find the end of the first half
        ListNode *slow = head, *fast = head;
        while (fast->next && fast->next->next) {
            slow = slow->next;
            fast = fast->next->next;
        }

        // 2. reverse the second half
        ListNode* second = slow->next;
        slow->next = nullptr;
        ListNode* prev = nullptr;
        while (second) {
            ListNode* nxt = second->next;
            second->next = prev;
            prev = second;
            second = nxt;
        }

        // 3. merge the two halves alternately
        ListNode* first = head;
        second = prev;
        while (second) {
            ListNode* n1 = first->next;
            ListNode* n2 = second->next;
            first->next = second;
            second->next = n1;
            first = n1;
            second = n2;
        }
    }
};
```

**Java**
```java
class Solution {
    public void reorderList(ListNode head) {
        if (head == null || head.next == null) return;

        // 1. find the end of the first half
        ListNode slow = head, fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        // 2. reverse the second half
        ListNode second = slow.next;
        slow.next = null;
        ListNode prev = null;
        while (second != null) {
            ListNode nxt = second.next;
            second.next = prev;
            prev = second;
            second = nxt;
        }

        // 3. merge the two halves alternately
        ListNode first = head;
        second = prev;
        while (second != null) {
            ListNode n1 = first.next;
            ListNode n2 = second.next;
            first.next = second;
            second.next = n1;
            first = n1;
            second = n2;
        }
    }
}
```

**Python**
```python
class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head or not head.next:
            return

        # 1. find the end of the first half
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. reverse the second half
        second = slow.next
        slow.next = None
        prev = None
        while second:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt

        # 3. merge the two halves alternately
        first, second = head, prev
        while second:
            n1, n2 = first.next, second.next
            first.next = second
            second.next = n1
            first, second = n1, n2
```

### Complexity
- **Time**: O(n) — three linear passes (find middle, reverse, merge).
- **Space**: O(1) — only a handful of pointers; the reversal is in place.

### Verdict
The optimal answer and a beautiful demonstration of *composing primitives*. If you can confidently write "find middle," "reverse," and "merge" separately, this problem is free.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Array buffer | O(n) | O(n) | easiest to get correct; wasteful memory |
| Middle + reverse + merge | O(n) | **O(1)** | optimal; the expected answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **One or two nodes** → already in final form; the early `return` (and the loops) leave them unchanged.
- **Even vs odd length** → the `fast.next && fast.next.next` guard makes the first half length ⌈n/2⌉, so the second (reversed) half is never longer. The merge naturally terminates when `second` runs out.
- **Pitfall — not cutting the first half**: if you forget `slow.next = null`, the reversed second half still links back into the first half, creating a cycle during the merge.
- **Pitfall — wrong middle for even length**: using `while (fast && fast->next)` instead of `while (fast->next && fast->next->next)` puts `slow` one node too far, mis-splitting the halves. Use the `next/next.next` guard so `slow` ends at the *last node of the first half*.
- **Pitfall — losing `next` during the merge**: save both `n1` and `n2` before re-pointing, exactly like in-place reversal.

---

## 🔗 Related problems
- **Reverse Linked List** (LC 206) — the reversal subroutine. See [`01-Reverse-Linked-List.md`](./01-Reverse-Linked-List.md).
- **Middle of the Linked List** (LC 876) — the find-middle subroutine.
- **Merge Two Sorted Lists** (LC 21) — the alternate-merge idea. See [`02-Merge-Two-Sorted-Lists.md`](./02-Merge-Two-Sorted-Lists.md).
- **Palindrome Linked List** (LC 234) — same find-middle + reverse-half technique.

---

**→ Next:** [`05-Remove-Nth-Node-From-End.md`](./05-Remove-Nth-Node-From-End.md) | **← Prev:** [`03-Linked-List-Cycle.md`](./03-Linked-List-Cycle.md) | Back to [`00-Index.md`](./00-Index.md)
