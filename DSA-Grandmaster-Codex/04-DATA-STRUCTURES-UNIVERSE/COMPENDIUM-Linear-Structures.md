# 📚 Linear Structures Compendium

> Compact reference for: Strings, Linked Lists, Stacks, Queues, Deques.

---

## 02 — STRINGS

### Concept
Sequence of characters. Often immutable in modern languages (Python, Java strings).

### Key operations & complexity
| Operation                  | C++ string | Python str | Java String |
|----------------------------|------------|------------|-------------|
| Length                     | O(1)       | O(1)       | O(1)        |
| Indexed access             | O(1)       | O(1)       | O(1)        |
| Concatenation              | O(n+m)     | O(n+m)     | O(n+m) → use StringBuilder for repeated concats |
| Substring                  | O(n)       | O(n)       | O(n)        |
| Find/index                 | O(nm)      | O(nm) avg  | O(nm)       |
| Replace                    | O(nm)      | O(nm)      | O(nm)       |
| Split                      | O(n)       | O(n)       | O(n)        |

### Patterns
- Use **StringBuilder** in Java/Python `''.join(...)` for repeated concatenation.
- Convert to char array for in-place mutation in Java.
- For pattern matching, learn **KMP, Z-algorithm, Rabin-Karp**.

### Top problems
1. Reverse string
2. Valid palindrome
3. Longest substring without repeating characters
4. Longest palindromic substring
5. Group anagrams
6. Implement strStr
7. Longest common prefix
8. Roman to integer / Integer to roman
9. ZigZag conversion
10. Multiply strings

### Deeper deep dive
See [Universe 08: Strings](../08-STRING-UNIVERSE/00-Index.md).

---

## 03 — LINKED LISTS

### Concept
Each node holds data + pointer to next (and possibly prev).

```cpp
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v) : val(v), next(nullptr) {}
};
```

### Variants
- **Singly linked**: `next` only
- **Doubly linked**: `prev` + `next` (e.g., `std::list`)
- **Circular**: tail.next == head

### Complexities
| Op                    | Singly  | Doubly | Notes                   |
|-----------------------|---------|--------|-------------------------|
| Access by index       | O(n)    | O(n)   | NO random access        |
| Insert at head        | O(1)    | O(1)   |                         |
| Insert at tail        | O(n)    | O(1)†  | †with tail pointer      |
| Insert at known node  | O(1)    | O(1)   | given node ref          |
| Delete known node     | O(1)†   | O(1)   | †with prev or trick     |
| Search                | O(n)    | O(n)   |                         |

### Why NOT to use them (vs arrays)
- 2-4× slower per operation due to **cache misses** (each node a pointer chase)
- Higher memory overhead (each node has 8-16 byte pointer)
- No SIMD vectorization possible

### Why TO use them
- O(1) insert/delete at known position
- Lock-free concurrent versions exist
- Foundation of LRU cache (DLL + hashmap)

### Critical patterns
1. **Slow & fast pointer** (cycle detection, midpoint, kth-from-end)
2. **In-place reversal** (recursive or iterative)
3. **Merge two sorted lists**
4. **Dummy head node** (simplifies edge cases)

### Top problems
1. Reverse linked list (iterative & recursive)
2. Detect cycle (Floyd's tortoise/hare)
3. Find cycle start (Floyd's stage 2)
4. Middle of linked list (slow/fast)
5. Merge two sorted lists
6. Remove Nth node from end
7. Add two numbers (digits as list)
8. Palindrome linked list
9. Reorder list
10. Copy list with random pointer
11. LRU cache
12. Reverse k-group

---

## 04 — STACKS

### Concept
LIFO (Last In First Out). Operations: push, pop, top, empty.

### Implementation
```cpp
stack<int> s;
s.push(1); s.push(2); s.top() == 2; s.pop();
// or vector
vector<int> stk;
stk.push_back(1); int top = stk.back(); stk.pop_back();
```

### Killer pattern: **Monotonic Stack**

When you need "next greater element," "next smaller element," "stock span," "histogram rectangle," etc.

```cpp
// Next greater to the right (O(n)):
vector<int> nge(n, -1);
stack<int> stk;  // indices, values strictly decreasing from bottom
for (int i = 0; i < n; i++) {
    while (!stk.empty() && a[stk.top()] < a[i]) {
        nge[stk.top()] = a[i];
        stk.pop();
    }
    stk.push(i);
}
```

### Top problems
1. Valid parentheses
2. Min stack (O(1) min query)
3. Daily temperatures
4. Next greater element I, II, III
5. Largest rectangle in histogram (CLASSIC)
6. Maximal rectangle (2D)
7. Trapping rain water (also two pointer)
8. Stock span
9. Asteroid collision
10. Decode string
11. Sum of subarray minimums
12. 132 pattern
13. Implement queue using stacks
14. Evaluate reverse polish notation
15. Basic calculator

---

## 05 — QUEUES

### Concept
FIFO (First In First Out). Operations: enqueue, dequeue, front, empty.

### Implementations
- **Array-based**: circular buffer
- **Linked list**: head + tail pointers
- **Two stacks** (interview classic)

```cpp
queue<int> q;
q.push(1); q.push(2); q.front() == 1; q.pop();
```

### Use cases
- BFS (level-order traversal)
- Task scheduling
- Stream processing buffer

### Top problems
1. Implement queue using arrays
2. Implement queue using stacks
3. Implement stack using queues
4. Number of recent calls
5. Design circular queue
6. Moving average from data stream

---

## 06 — DEQUES

### Concept
Double-ended queue. O(1) push/pop at **both** ends.

```cpp
deque<int> dq;
dq.push_back(1); dq.push_front(0);
dq.pop_back(); dq.pop_front();
```

Implementation: typically a circular buffer of fixed-size chunks linked together.

### Killer pattern: **Monotonic Deque** (sliding window max/min)

```cpp
// Sliding window maximum (O(n)):
deque<int> dq;  // indices, values decreasing from front
vector<int> result;
for (int i = 0; i < n; i++) {
    while (!dq.empty() && a[dq.back()] < a[i]) dq.pop_back();
    dq.push_back(i);
    if (dq.front() <= i - k) dq.pop_front();
    if (i >= k - 1) result.push_back(a[dq.front()]);
}
```

### Top problems
1. Sliding window maximum (LC 239)
2. Constrained subsequence sum (LC 1425)
3. Shortest subarray with sum at least K (LC 862)
4. First negative number in window (GFG)
5. Longest subarray with sum ≤ k

---

**→ Next:** [`07-Hash-Tables.md`](./07-Hash-Tables.md)
