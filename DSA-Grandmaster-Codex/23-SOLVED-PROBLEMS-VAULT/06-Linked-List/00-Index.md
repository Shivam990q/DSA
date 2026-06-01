# 🗂️ Linked List — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to optimal → intuition, algorithm, dry run, C++ / Java / Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Reverse Linked List](./01-Reverse-Linked-List.md) | 206 | Easy | iterative 3-pointer → recursion |
| 02 | [Merge Two Sorted Lists](./02-Merge-Two-Sorted-Lists.md) | 21 | Easy | dummy-node splice → recursion |
| 03 | [Linked List Cycle](./03-Linked-List-Cycle.md) | 141 | Easy | hash set → Floyd fast/slow |
| 04 | [Reorder List](./04-Reorder-List.md) | 143 | Medium | array buffer → mid+reverse+merge |
| 05 | [Remove Nth Node From End](./05-Remove-Nth-Node-From-End.md) | 19 | Medium | two-pass length → one-pass gap |
| 06 | [Copy List With Random Pointer](./06-Copy-List-With-Random-Pointer.md) | 138 | Medium | hash map → O(1) interleaving |
| 07 | [Add Two Numbers](./07-Add-Two-Numbers.md) | 2 | Medium | digit-by-digit carry |
| 08 | [Find the Duplicate Number](./08-Find-The-Duplicate-Number.md) | 287 | Medium | sort/set → negate → Floyd / binary search |
| 09 | [LRU Cache](./09-LRU-Cache.md) | 146 | Medium | hash map + doubly linked list |
| 10 | [Merge K Sorted Lists](./10-Merge-K-Sorted-Lists.md) | 23 | Hard | sequential → min-heap → divide & conquer |
| 11 | [Reverse Nodes in K-Group](./11-Reverse-Nodes-In-K-Group.md) | 25 | Hard | recursion → iterative O(1) |

---

## 🧩 The `ListNode` definition

Every singly-linked problem in this set uses the same node. Memorize all three so you never waste interview time re-typing it.

**C++**
```cpp
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};
```

**Java**
```java
public class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}
```

**Python**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

Two problems use a richer node. **Copy List With Random Pointer (LC 138)** adds a `random` pointer:

```cpp
class Node {
public:
    int val;
    Node* next;
    Node* random;
    Node(int _val) : val(_val), next(nullptr), random(nullptr) {}
};
```
```java
class Node {
    int val;
    Node next;
    Node random;
    public Node(int val) { this.val = val; this.next = null; this.random = null; }
}
```
```python
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random
```

And **Find the Duplicate Number (LC 287)** is an *array* problem that secretly is a linked-list cycle problem — the array indices form an implicit linked list (`i → nums[i]`).

---

## 🎯 The pattern family

Linked lists reward a small toolkit of reusable maneuvers. Almost every problem here is a combination of these:

- **Dummy / sentinel head** — a fake node before `head` so the "delete the head" or "build a new list" cases need no special branch. Used in Merge Two Lists, Add Two Numbers, Remove Nth Node, Merge K Lists.
- **In-place reversal (3-pointer `prev / cur / next`)** — the single most reused subroutine. Reverse Linked List, Reorder List, Reverse K-Group all hinge on it.
- **Fast & slow pointers (Floyd)** — detect cycles, find the middle, find the cycle entrance, find a back-from-end position. Linked List Cycle, Reorder List, Remove Nth Node, Find the Duplicate Number.
- **Two pointers with a fixed gap** — to locate "the n-th node from the end" in one pass. Remove Nth Node.
- **Hash map for structure** — when nodes carry extra pointers or you need O(1) keyed access. Copy List With Random Pointer, LRU Cache, Linked List Cycle (set variant).
- **Heap / divide & conquer over k lists** — Merge K Sorted Lists.

> The mental model: a linked list is *pointers you re-thread*. Draw the boxes-and-arrows on paper, move three pointers slowly, and almost every "tricky" problem becomes mechanical. Always ask: *"what does each pointer point to right now, and what is the LAST node whose `next` I still need?"*

---

**→ Start:** [`01-Reverse-Linked-List.md`](./01-Reverse-Linked-List.md) | Back to [vault index](../00-Index.md)
