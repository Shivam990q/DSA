# Merge Two Sorted Lists

**Platform**: LeetCode 21 · **Difficulty**: Easy · **Topics**: Linked List, Recursion · **Pattern**: Dummy-node splice / two-pointer merge

---

## 📜 Problem Statement

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one **sorted** list. The list should be made by splicing together the nodes of the first two lists.

Return *the head of the merged linked list*.

### Examples

**Example 1:**
```
Input:  list1 = [1, 2, 4], list2 = [1, 3, 4]
Output: [1, 1, 2, 3, 4, 4]
```

**Example 2:**
```
Input:  list1 = [], list2 = []
Output: []
```

**Example 3:**
```
Input:  list1 = [], list2 = [0]
Output: [0]
```

### Constraints
```
The number of nodes in both lists is in the range [0, 50].
-100 <= Node.val <= 100
Both list1 and list2 are sorted in non-decreasing order.
```

---

## 🧠 Understanding the problem

This is the **merge step of merge sort**, applied to linked lists. Because both inputs are already sorted, the smallest unplaced node is always at one of the two current heads. So we repeatedly compare the two heads, pick the smaller, and append it to our growing result.

Two things make linked lists nicer than arrays here: we don't need to shift elements, and we can **reuse the existing nodes** (the problem explicitly says splice them together — no new node allocation required). We only re-thread `next` pointers.

The recurring annoyance in list building is the *first* node: until we've appended something, we have no "tail" to attach to. The **dummy head** trick eliminates that special case — we start with a throwaway node, always attach to its tail, and return `dummy.next` at the end.

---

## Approach 1 — Iterative merge with a dummy head (optimal) ⭐

### Intuition
Keep a `tail` pointer to the last node of the result so far, starting at a dummy node. At each step, whichever of `list1`/`list2` has the smaller head gets spliced onto `tail`, and that list advances. When one list runs out, the other is already sorted, so just attach the entire remainder in O(1).

### Algorithm
1. Create `dummy`; set `tail = dummy`.
2. While both `list1` and `list2` are non-null:
   - If `list1.val <= list2.val`: `tail.next = list1`; advance `list1`.
   - Else: `tail.next = list2`; advance `list2`.
   - Advance `tail = tail.next`.
3. Attach the leftover: `tail.next = list1 != null ? list1 : list2`.
4. Return `dummy.next`.

> Using `<=` (not `<`) keeps the merge **stable** and handles equal values correctly.

### Dry run on `list1 = [1, 2, 4]`, `list2 = [1, 3, 4]`
```
dummy → ?    tail=dummy

1 vs 1: 1<=1 → take list1(1)   tail=1   list1=[2,4]
        result: 1
2 vs 1: 2>1  → take list2(1)   tail=1   list2=[3,4]
        result: 1 -> 1
2 vs 3: 2<=3 → take list1(2)   tail=2   list1=[4]
        result: 1 -> 1 -> 2
4 vs 3: 4>3  → take list2(3)   tail=3   list2=[4]
        result: 1 -> 1 -> 2 -> 3
4 vs 4: 4<=4 → take list1(4)   tail=4   list1=[]
        result: 1 -> 1 -> 2 -> 3 -> 4
list1 empty → attach list2 remainder [4]
        result: 1 -> 1 -> 2 -> 3 -> 4 -> 4 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        ListNode dummy(0);
        ListNode* tail = &dummy;
        while (list1 && list2) {
            if (list1->val <= list2->val) {
                tail->next = list1;
                list1 = list1->next;
            } else {
                tail->next = list2;
                list2 = list2->next;
            }
            tail = tail->next;
        }
        tail->next = list1 ? list1 : list2;  // attach the rest
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (list1 != null && list2 != null) {
            if (list1.val <= list2.val) {
                tail.next = list1;
                list1 = list1.next;
            } else {
                tail.next = list2;
                list2 = list2.next;
            }
            tail = tail.next;
        }
        tail.next = (list1 != null) ? list1 : list2;  // attach the rest
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        dummy = ListNode(0)
        tail = dummy
        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        tail.next = list1 if list1 else list2  # attach the rest
        return dummy.next
```

### Complexity
- **Time**: O(n + m) — each node from both lists is visited once.
- **Space**: O(1) — we reuse existing nodes; only a dummy and a tail pointer are allocated.

### Verdict
The standard answer: constant extra space, single pass, easy to reason about. The dummy node is the key idiom — internalize it, it appears in half the problems in this set.

---

## Approach 2 — Recursion

### Intuition
The merged list's head is the smaller of the two heads. Whatever that is, its `next` should be the merge of "the rest of that list" with "the other whole list." That recursive definition writes itself.

### Algorithm
1. If `list1` is null, return `list2`. If `list2` is null, return `list1`. (Base cases.)
2. If `list1.val <= list2.val`:
   - `list1.next = merge(list1.next, list2)`; return `list1`.
3. Else:
   - `list2.next = merge(list1, list2.next)`; return `list2`.

### Dry run on `list1 = [1, 4]`, `list2 = [2]`
```
merge([1,4], [2]): 1<=2 → 1.next = merge([4], [2]); return 1
  merge([4], [2]): 4>2  → 2.next = merge([4], []); return 2
    merge([4], []): list2 null → return [4]
  ⇒ 2.next = 4 → returns 2->4
⇒ 1.next = 2->4 → returns 1->2->4 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* list1, ListNode* list2) {
        if (!list1) return list2;
        if (!list2) return list1;
        if (list1->val <= list2->val) {
            list1->next = mergeTwoLists(list1->next, list2);
            return list1;
        } else {
            list2->next = mergeTwoLists(list1, list2->next);
            return list2;
        }
    }
};
```

**Java**
```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        if (list1 == null) return list2;
        if (list2 == null) return list1;
        if (list1.val <= list2.val) {
            list1.next = mergeTwoLists(list1.next, list2);
            return list1;
        } else {
            list2.next = mergeTwoLists(list1, list2.next);
            return list2;
        }
    }
}
```

**Python**
```python
class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

### Complexity
- **Time**: O(n + m).
- **Space**: O(n + m) — recursion depth equals the total number of nodes.

### Verdict
Clean and expressive. The trade-off is the call-stack space. For the tiny constraints here (≤ 50 nodes each) it's perfectly fine, but the iterative version generalizes better and is the one to reach for inside Merge K Sorted Lists.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Iterative + dummy | O(n + m) | **O(1)** | default optimal answer ⭐ |
| Recursive | O(n + m) | O(n + m) stack | elegant; stack cost on long lists |

---

## 🧪 Edge cases & pitfalls
- **Both lists empty** → loop never runs; `dummy.next` is null. ✅
- **One list empty** → the leftover-attach step (or recursion base case) handles it.
- **Duplicate values across lists** → `<=` keeps them in a sensible, stable order.
- **Pitfall — `<` vs `<=`**: both produce a sorted list, but `<=` preserves stability (nodes from `list1` come before equal nodes from `list2`). Use `<=`.
- **Pitfall — forgetting the leftover attach**: if you stop at the `while` loop and don't splice the remaining list, you truncate the result.
- **Pitfall — returning `dummy` instead of `dummy.next`**: that prepends a bogus `0` node.

---

## 🔗 Related problems
- **Merge K Sorted Lists** (LC 23) — generalizes this to `k` lists with a heap or divide & conquer. See [`10-Merge-K-Sorted-Lists.md`](./10-Merge-K-Sorted-Lists.md).
- **Merge Sorted Array** (LC 88) — same merge logic on arrays, merged in place from the back.
- **Sort List** (LC 148) — merge sort on a linked list; this is its merge subroutine.
- **Add Two Numbers** (LC 2) — also builds a result list with a dummy head. See [`07-Add-Two-Numbers.md`](./07-Add-Two-Numbers.md).

---

**→ Next:** [`03-Linked-List-Cycle.md`](./03-Linked-List-Cycle.md) | **← Prev:** [`01-Reverse-Linked-List.md`](./01-Reverse-Linked-List.md) | Back to [`00-Index.md`](./00-Index.md)
