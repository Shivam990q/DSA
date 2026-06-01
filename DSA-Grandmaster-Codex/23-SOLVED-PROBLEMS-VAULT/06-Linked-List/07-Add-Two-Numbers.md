# Add Two Numbers

**Platform**: LeetCode 2 · **Difficulty**: Medium · **Topics**: Linked List, Math, Recursion · **Pattern**: Digit-by-digit addition with carry + dummy node

---

## 📜 Problem Statement

You are given two **non-empty** linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

### Examples

**Example 1:**
```
Input:  l1 = [2, 4, 3], l2 = [5, 6, 4]
Output: [7, 0, 8]
Explanation: 342 + 465 = 807.
```

**Example 2:**
```
Input:  l1 = [0], l2 = [0]
Output: [0]
```

**Example 3:**
```
Input:  l1 = [9, 9, 9, 9, 9, 9, 9], l2 = [9, 9, 9, 9]
Output: [8, 9, 9, 9, 0, 0, 0, 1]
Explanation: 9999999 + 9999 = 10009998.
```

### Constraints
```
The number of nodes in each linked list is in the range [1, 100].
0 <= Node.val <= 9
It is guaranteed that the list represents a number that does not have leading zeros.
```

---

## 🧠 Understanding the problem

The lists store digits **least-significant first**. That detail is a gift: it lines the lists up exactly the way we add by hand — start at the ones place, add, carry into the tens place, and so on. So we walk both lists front-to-front, and the result list is also built least-significant first.

We cannot just convert each list to an integer and add (well, we can in this constrained version, but the lists can be up to 100 digits long, which overflows 64-bit integers — and that defeats the purpose). The robust solution is grade-school addition: at each position, `digit = (a + b + carry) % 10`, `carry = (a + b + carry) / 10`.

Three details to get right:
- Lists may differ in length → treat a missing digit as 0.
- A final carry after both lists end produces a brand-new most-significant digit (Example 3).
- A **dummy head** makes building the result list painless.

---

## Approach 1 — Elementary addition with carry (optimal) ⭐

### Intuition
Mirror long addition. Keep a running `carry`. Loop while there is anything left to add — either list still has nodes, or the carry is non-zero. Each iteration emits one result digit.

### Algorithm
1. Create `dummy`; set `tail = dummy`, `carry = 0`.
2. While `l1` or `l2` is non-null, or `carry != 0`:
   - `sum = carry + (l1 ? l1.val : 0) + (l2 ? l2.val : 0)`.
   - `carry = sum / 10`.
   - Append `new ListNode(sum % 10)` to `tail`; advance `tail`.
   - Advance `l1` and `l2` if non-null.
3. Return `dummy.next`.

### Dry run on `l1 = [2, 4, 3]` (342), `l2 = [5, 6, 4]` (465)
```
carry=0
pos0: 2 + 5 + 0 = 7  → digit 7, carry 0   result: 7
pos1: 4 + 6 + 0 = 10 → digit 0, carry 1   result: 7 → 0
pos2: 3 + 4 + 1 = 8  → digit 8, carry 0   result: 7 → 0 → 8
both lists null, carry 0 → stop
result: [7, 0, 8]  (=807) ✅
```

Dry run showing the final carry, `l1 = [9, 9]` (99), `l2 = [1]` (1):
```
pos0: 9 + 1 + 0 = 10 → digit 0, carry 1   result: 0
pos1: 9 + 0 + 1 = 10 → digit 0, carry 1   result: 0 → 0
pos2: 0 + 0 + 1 = 1  → digit 1, carry 0   result: 0 → 0 → 1
result: [0, 0, 1]  (=100) ✅  ← extra node created by trailing carry
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode dummy(0);
        ListNode* tail = &dummy;
        int carry = 0;
        while (l1 || l2 || carry) {
            int sum = carry + (l1 ? l1->val : 0) + (l2 ? l2->val : 0);
            carry = sum / 10;
            tail->next = new ListNode(sum % 10);
            tail = tail->next;
            if (l1) l1 = l1->next;
            if (l2) l2 = l2->next;
        }
        return dummy.next;
    }
};
```

**Java**
```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        int carry = 0;
        while (l1 != null || l2 != null || carry != 0) {
            int sum = carry + (l1 != null ? l1.val : 0) + (l2 != null ? l2.val : 0);
            carry = sum / 10;
            tail.next = new ListNode(sum % 10);
            tail = tail.next;
            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode(0)
        tail = dummy
        carry = 0
        while l1 or l2 or carry:
            total = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
            carry, digit = divmod(total, 10)
            tail.next = ListNode(digit)
            tail = tail.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return dummy.next
```

### Complexity
- **Time**: O(max(n, m)) — one pass over the longer list (plus possibly one extra node for the carry).
- **Space**: O(max(n, m)) for the result list (O(1) auxiliary beyond the output).

### Verdict
The canonical solution. The single loop condition `l1 || l2 || carry` elegantly folds three concerns — unequal lengths and the trailing carry — into one. This is what you write.

---

## Approach 2 — Recursion

### Intuition
The same addition expressed recursively: compute the current digit and carry, then recurse on the rest of both lists plus the carry. The recursion bottoms out when both lists are exhausted and there's no carry.

### Algorithm
1. Define `add(l1, l2, carry)`:
   - If `l1`, `l2`, and `carry` are all empty/zero → return null.
   - `sum = carry + (l1 ? l1.val : 0) + (l2 ? l2.val : 0)`.
   - Create `node = new ListNode(sum % 10)`.
   - `node.next = add(l1?.next, l2?.next, sum / 10)`.
   - Return `node`.
2. Call `add(l1, l2, 0)`.

### Dry run on `l1 = [5]`, `l2 = [5]`
```
add([5],[5],0): sum=10 → node(0), recurse add(null,null,1)
  add(null,null,1): sum=1 → node(1), recurse add(null,null,0)
    add(null,null,0): all empty → return null
  ⇒ node(1) → null
⇒ node(0) → node(1)
result: [0, 1]  (=10) ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        return add(l1, l2, 0);
    }
private:
    ListNode* add(ListNode* l1, ListNode* l2, int carry) {
        if (!l1 && !l2 && carry == 0) return nullptr;
        int sum = carry + (l1 ? l1->val : 0) + (l2 ? l2->val : 0);
        ListNode* node = new ListNode(sum % 10);
        node->next = add(l1 ? l1->next : nullptr,
                         l2 ? l2->next : nullptr,
                         sum / 10);
        return node;
    }
};
```

**Java**
```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        return add(l1, l2, 0);
    }
    private ListNode add(ListNode l1, ListNode l2, int carry) {
        if (l1 == null && l2 == null && carry == 0) return null;
        int sum = carry + (l1 != null ? l1.val : 0) + (l2 != null ? l2.val : 0);
        ListNode node = new ListNode(sum % 10);
        node.next = add(l1 != null ? l1.next : null,
                        l2 != null ? l2.next : null,
                        sum / 10);
        return node;
    }
}
```

**Python**
```python
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        def add(a, b, carry):
            if not a and not b and carry == 0:
                return None
            total = carry + (a.val if a else 0) + (b.val if b else 0)
            node = ListNode(total % 10)
            node.next = add(a.next if a else None,
                            b.next if b else None,
                            total // 10)
            return node
        return add(l1, l2, 0)
```

### Complexity
- **Time**: O(max(n, m)).
- **Space**: O(max(n, m)) recursion stack (plus the output list).

### Verdict
A tidy expression of the same logic. The recursion stack adds space cost, so the iterative version is preferred in practice, but the recursive form reads beautifully and is good to know.

---

## ⚖️ Approach comparison

| Approach | Time | Aux Space | Notes |
|----------|------|-----------|-------|
| Iterative carry | O(max(n,m)) | **O(1)** | default optimal answer ⭐ |
| Recursive carry | O(max(n,m)) | O(max(n,m)) stack | clean, but extra stack |

> **Why not convert to integers?** With up to 100 digits, the numbers far exceed 64-bit range. Big-integer types would work but obscure the intended digit-and-carry technique and aren't available cleanly in C++.

---

## 🧪 Edge cases & pitfalls
- **Different lengths** → the `(l ? l.val : 0)` guard treats the shorter list's missing digits as 0.
- **Trailing carry** → `9999999 + 9999` needs an extra leading node; the `|| carry` in the loop condition (or the recursion's `carry == 0` base check) creates it.
- **Both inputs `[0]`** → one iteration emits `0`, carry becomes 0 → result `[0]`. ✅
- **Pitfall — stopping when one list ends**: looping only `while (l1 && l2)` drops the longer list's remaining digits. Loop while *either* has nodes.
- **Pitfall — forgetting the final carry**: ending the loop on lists-empty alone loses the most-significant digit of Example 3.
- **Pitfall — advancing a null pointer**: guard each advance with `if (l1)` / `if (l2)`.

---

## 🔗 Related problems
- **Add Two Numbers II** (LC 445) — digits stored **most-significant first**; reverse the lists or use stacks.
- **Multiply Strings** (LC 43) — grade-school multiplication with carries on strings.
- **Plus One** (LC 66) — increment a digit array with carry propagation.
- **Merge Two Sorted Lists** (LC 21) — also builds a result with a dummy head. See [`02-Merge-Two-Sorted-Lists.md`](./02-Merge-Two-Sorted-Lists.md).

---

**→ Next:** [`08-Find-The-Duplicate-Number.md`](./08-Find-The-Duplicate-Number.md) | **← Prev:** [`06-Copy-List-With-Random-Pointer.md`](./06-Copy-List-With-Random-Pointer.md) | Back to [`00-Index.md`](./00-Index.md)
