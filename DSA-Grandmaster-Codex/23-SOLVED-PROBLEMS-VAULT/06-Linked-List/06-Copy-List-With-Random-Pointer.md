# Copy List With Random Pointer

**Platform**: LeetCode 138 · **Difficulty**: Medium · **Topics**: Linked List, Hash Table · **Pattern**: Deep copy via mapping / node interleaving

---

## 📜 Problem Statement

A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list, or `null`.

Construct a **deep copy** of the list. The deep copy should consist of exactly `n` **brand new** nodes, where each new node has its value set to the value of its corresponding original node. Both the `next` and `random` pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. **None of the pointers in the new list should point to nodes in the original list.**

For example, if there are two nodes `X` and `Y` in the original list, where `X.random --> Y`, then for the corresponding two nodes `x` and `y` in the copied list, `x.random --> y`.

Return *the head of the copied linked list*.

The linked list is represented in the input/output as a list of `n` nodes. Each node is represented as a pair of `[val, random_index]` where `random_index` is the index of the node (range from `0` to `n-1`) that the `random` pointer points to, or `null` if it does not point to any node.

### Examples

**Example 1:**
```
Input:  head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]
```

**Example 2:**
```
Input:  head = [[1,1],[2,1]]
Output: [[1,1],[2,1]]
```

**Example 3:**
```
Input:  head = [[3,null],[3,0],[3,null]]
Output: [[3,null],[3,0],[3,null]]
```

### Constraints
```
0 <= n <= 1000
-10^4 <= Node.val <= 10^4
Node.random is null or points to some node in the linked list.
```

---

## 🧠 The node

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

---

## 🧠 Understanding the problem

A plain linked-list copy is trivial: walk forward, allocate a new node per original, link them. The `random` pointer breaks that simplicity because when we're copying node `X`, the clone of `X.random` **may not exist yet** (it could be a node further ahead we haven't reached).

So the heart of the problem is: *given an original node, instantly find its clone*. There are two ways to maintain that original→clone correspondence:

1. **A hash map** `original → clone`. Build all clones first (or lazily), then wire up `next` and `random` using map lookups. O(n) time, O(n) space.
2. **Interleave clones into the original list** so each original node `X` is immediately followed by its clone `X'`. Then `X'.random = X.random.next` — the clone of any node is always the node right after it. This needs no map → O(1) extra space.

Both are O(n) time. The interleaving approach is the "wow" optimization interviewers love.

---

## Approach 1 — Hash map (two passes) ⭐

### Intuition
First pass: create a clone for every original node and remember the pairing in a map. Second pass: now that every clone exists, set each clone's `next` and `random` by looking up the clones of the originals' `next` and `random`.

### Algorithm
1. If `head` is null, return null.
2. Pass 1: for each `cur` in the original, create `clone[cur] = new Node(cur.val)`.
3. Pass 2: for each `cur`, set `clone[cur].next = clone[cur.next]` and `clone[cur].random = clone[cur.random]` (a null key maps to null).
4. Return `clone[head]`.

### Dry run on `[[7,null],[13,0]]`
```
originals: A(7), B(13) with B.random → A

Pass 1 (create clones):
  clone[A] = a(7)
  clone[B] = b(13)

Pass 2 (wire pointers):
  a.next = clone[A.next] = clone[B] = b
  a.random = clone[null] = null
  b.next = clone[B.next] = clone[null] = null
  b.random = clone[B.random] = clone[A] = a
result: a(7) → b(13),  b.random → a  ✅ (all new nodes)
```

### Code

**C++**
```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) return nullptr;
        unordered_map<Node*, Node*> clone;
        for (Node* cur = head; cur; cur = cur->next)
            clone[cur] = new Node(cur->val);
        for (Node* cur = head; cur; cur = cur->next) {
            clone[cur]->next   = clone[cur->next];    // null → null via default
            clone[cur]->random = clone[cur->random];
        }
        return clone[head];
    }
};
```
> Note: `clone[nullptr]` default-constructs to `nullptr` in `unordered_map`, so null next/random map correctly.

**Java**
```java
class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) return null;
        Map<Node, Node> clone = new HashMap<>();
        for (Node cur = head; cur != null; cur = cur.next)
            clone.put(cur, new Node(cur.val));
        for (Node cur = head; cur != null; cur = cur.next) {
            clone.get(cur).next   = clone.get(cur.next);    // missing key → null
            clone.get(cur).random = clone.get(cur.random);
        }
        return clone.get(head);
    }
}
```

**Python**
```python
class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head:
            return None
        clone = {}
        cur = head
        while cur:
            clone[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur:
            clone[cur].next = clone.get(cur.next)      # None → None
            clone[cur].random = clone.get(cur.random)
            cur = cur.next
        return clone[head]
```

### Complexity
- **Time**: O(n) — two passes.
- **Space**: O(n) — the map stores one entry per node.

### Verdict
The go-to answer: easy to reason about and hard to get wrong. The `.get()` / default-null behavior cleanly handles null `next`/`random`. Present this first.

> **Variant — one-pass map with default lookups.** You can collapse it into a single pass using a helper that returns the existing clone or lazily creates one. Same O(n)/O(n) bounds, slightly trickier to write.

---

## Approach 2 — Interleaving (O(1) extra space) ⭐⭐

### Intuition
Weave each clone directly behind its original: `A → A' → B → B' → C → C' → …`. Now the clone of *any* original node `X` is simply `X.next`. That gives us a map "for free" embedded in the list structure:
- `X'.random = X.random.next` (the clone of `X.random` sits right after it).

Finally, unweave the two lists to restore the original and extract the copy.

### Algorithm
1. **Interleave**: for each original `cur`, insert `clone = new Node(cur.val)` between `cur` and `cur.next`. Advance `cur = clone.next`.
2. **Assign randoms**: for each original `cur` (step 2 at a time), if `cur.random` is non-null, set `cur.next.random = cur.random.next`.
3. **Separate**: split the interleaved list back into the original and the copy. Restore each original's `next` and link the clones together.

### Dry run on `A(7) → B(13)` where `B.random → A`
```
Step 1 — interleave:
  A → A' → B → B'    (A'=7, B'=13)

Step 2 — randoms:
  A.random = null → skip
  B.random = A → B'.random = A.random.next = A.next = A'   ✅

Step 3 — separate:
  original: A → B          (restored)
  copy:     A' → B'   with B'.random → A'
result: deep copy A'(7) → B'(13), B'.random → A' ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        if (!head) return nullptr;

        // 1. interleave clones: A -> A' -> B -> B' -> ...
        for (Node* cur = head; cur; cur = cur->next->next) {
            Node* clone = new Node(cur->val);
            clone->next = cur->next;
            cur->next = clone;
        }

        // 2. assign random pointers
        for (Node* cur = head; cur; cur = cur->next->next) {
            if (cur->random) cur->next->random = cur->random->next;
        }

        // 3. separate the two lists
        Node* dummy = new Node(0);
        Node* copyTail = dummy;
        for (Node* cur = head; cur; cur = cur->next) {
            Node* clone = cur->next;
            cur->next = clone->next;          // restore original
            copyTail->next = clone;           // build copy
            copyTail = clone;
        }
        Node* res = dummy->next;
        delete dummy;
        return res;
    }
};
```

**Java**
```java
class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) return null;

        // 1. interleave clones: A -> A' -> B -> B' -> ...
        for (Node cur = head; cur != null; cur = cur.next.next) {
            Node clone = new Node(cur.val);
            clone.next = cur.next;
            cur.next = clone;
        }

        // 2. assign random pointers
        for (Node cur = head; cur != null; cur = cur.next.next) {
            if (cur.random != null) cur.next.random = cur.random.next;
        }

        // 3. separate the two lists
        Node dummy = new Node(0);
        Node copyTail = dummy;
        for (Node cur = head; cur != null; cur = cur.next) {
            Node clone = cur.next;
            cur.next = clone.next;            // restore original
            copyTail.next = clone;            // build copy
            copyTail = clone;
        }
        return dummy.next;
    }
}
```

**Python**
```python
class Solution:
    def copyRandomList(self, head: 'Node') -> 'Node':
        if not head:
            return None

        # 1. interleave clones: A -> A' -> B -> B' -> ...
        cur = head
        while cur:
            clone = Node(cur.val)
            clone.next = cur.next
            cur.next = clone
            cur = clone.next

        # 2. assign random pointers
        cur = head
        while cur:
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next

        # 3. separate the two lists
        dummy = Node(0)
        copy_tail = dummy
        cur = head
        while cur:
            clone = cur.next
            cur.next = clone.next      # restore original
            copy_tail.next = clone     # build copy
            copy_tail = clone
            cur = cur.next
        return dummy.next
```

### Complexity
- **Time**: O(n) — three linear passes.
- **Space**: O(1) extra — beyond the `n` clone nodes we must allocate, no auxiliary structure.

### Verdict
The space-optimal answer. The "clone lives right behind the original" insight is the kind of pointer trick that distinguishes strong candidates. The bookkeeping (restoring the original list) is where bugs hide — practice the separation step until it's automatic.

---

## ⚖️ Approach comparison

| Approach | Time | Extra Space | Notes |
|----------|------|-------------|-------|
| Hash map | O(n) | O(n) | simplest; default-null lookups handle edges ⭐ |
| Interleaving | O(n) | **O(1)** | space-optimal; trickier separation step ⭐⭐ |

Both allocate `n` new nodes (unavoidable for a deep copy). The difference is only the auxiliary map.

---

## 🧪 Edge cases & pitfalls
- **Empty list** → return null right away.
- **`random` points to self** → handled automatically: in the map version `clone[cur->random]` is `clone[cur]`; in interleaving, `cur.next.random = cur.random.next = cur.next`.
- **`random` is null** → map lookup defaults to null; interleaving guards with `if (cur.random)`.
- **Duplicate values** → never key the map on `val`; key on the node identity, or values collide.
- **Pitfall — not restoring the original list (interleaving)**: leaving the lists interleaved both corrupts the input and produces a wrong copy. The separation pass is mandatory.
- **Pitfall (C++) — `clone[cur->next]` when `cur->next` is null**: `unordered_map::operator[]` value-initializes a missing key to `nullptr`, which is exactly what we want, but be aware it *inserts* a `{nullptr → nullptr}` entry. It's harmless here.

---

## 🔗 Related problems
- **Clone Graph** (LC 133) — deep copy with arbitrary edges; same original→clone map idea.
- **Copy List with Random Pointer** is itself a stepping stone to graph-cloning problems.
- **Linked List Cycle** (LC 141) — also relies on node identity, not value. See [`03-Linked-List-Cycle.md`](./03-Linked-List-Cycle.md).

---

**→ Next:** [`07-Add-Two-Numbers.md`](./07-Add-Two-Numbers.md) | **← Prev:** [`05-Remove-Nth-Node-From-End.md`](./05-Remove-Nth-Node-From-End.md) | Back to [`00-Index.md`](./00-Index.md)
