# LRU Cache

**Platform**: LeetCode 146 · **Difficulty**: Medium · **Topics**: Hash Table, Linked List, Design, Doubly Linked List · **Pattern**: Hash map + doubly linked list

---

## 📜 Problem Statement

Design a data structure that follows the constraints of a **Least Recently Used (LRU) cache**.

Implement the `LRUCache` class:

- `LRUCache(int capacity)` Initialize the LRU cache with **positive** size `capacity`.
- `int get(int key)` Return the value of the `key` if the key exists, otherwise return `-1`.
- `void put(int key, int value)` Update the value of the `key` if the `key` exists. Otherwise, add the `key-value` pair to the cache. If the number of keys exceeds the `capacity` from this operation, **evict** the least recently used key.

The functions `get` and `put` must each run in **O(1)** average time complexity.

### Examples

**Example 1:**
```
Input:
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1,1], [2,2], [1], [3,3], [2], [4,4], [1], [3], [4]]
Output:
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation:
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1, cache is {2=2, 1=1} (1 now most recent)
lRUCache.put(3, 3); // evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // evicts key 1, cache is {3=3, 4=4}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4
```

### Constraints
```
1 <= capacity <= 3000
0 <= key <= 10^4
0 <= value <= 10^5
At most 2 * 10^5 calls will be made to get and put.
```

---

## 🧠 Understanding the problem

An LRU cache must answer two questions in O(1):
1. **Where is the value for this key?** → a **hash map** keyed by `key` gives O(1) lookup.
2. **Which key is least recently used right now?** → we need an ordering by recency that supports O(1) "move this to most-recent" and O(1) "remove the least-recent."

A plain array/list can't reorder in O(1). The structure that can splice a node out and re-insert it at an end in O(1) — *given a pointer to the node* — is a **doubly linked list**. The map stores `key → node pointer`, so we always have that pointer.

The design: a doubly linked list ordered most-recent → least-recent. We use two sentinel nodes, `head` and `tail`, so insertion/removal never touch null and need no edge-case branches. Convention used here: **insert at the front (right after `head`) = most recently used; evict from the back (right before `tail`) = least recently used.**

Every `get` or `put` that touches a key moves that node to the front. When size exceeds capacity, drop the node before `tail`.

---

## Approach 1 — Hash map + doubly linked list (optimal) ⭐

### Intuition
Combine the strengths: the map for O(1) addressing, the DLL for O(1) recency reordering. Two private helpers do all the pointer work: `remove(node)` unlinks a node, `insertFront(node)` places it right after `head`. Then:
- `get(key)`: miss → `-1`; hit → `remove` then `insertFront` (mark most-recent), return value.
- `put(key, value)`: if key exists, update + move to front; else insert a new node at front and store in map; if over capacity, evict the node before `tail` and erase it from the map.

### Algorithm
1. **Init**: `head` and `tail` sentinels linked together (`head.next = tail`, `tail.prev = head`). Empty map. Store `capacity`.
2. **`remove(node)`**: `node.prev.next = node.next; node.next.prev = node.prev`.
3. **`insertFront(node)`**: splice `node` between `head` and `head.next`.
4. **`get(key)`**: if not in map → `-1`. Else `node = map[key]`, `remove(node)`, `insertFront(node)`, return `node.val`.
5. **`put(key, value)`**: if key in map → `remove` old node (and free it). Create node, `insertFront`, `map[key] = node`. If `map.size() > capacity` → `lru = tail.prev`, `remove(lru)`, `map.erase(lru.key)` (free it).

### Dry run (capacity = 2)
```
DLL shown head ⇄ ... ⇄ tail  (front = most recent)

put(1,1): insert 1 → head ⇄ 1 ⇄ tail              map{1}
put(2,2): insert 2 → head ⇄ 2 ⇄ 1 ⇄ tail          map{1,2}
get(1):   hit, move 1 to front
          head ⇄ 1 ⇄ 2 ⇄ tail   return 1          (2 is now LRU)
put(3,3): new key, size would be 3 > 2
          insert 3 → head ⇄ 3 ⇄ 1 ⇄ 2 ⇄ tail
          evict tail.prev = 2 → head ⇄ 3 ⇄ 1 ⇄ tail  map{1,3}
get(2):   miss → return -1
put(4,4): insert 4, evict LRU = 1
          head ⇄ 4 ⇄ 3 ⇄ tail   map{3,4}
get(1):   miss → -1
get(3):   hit → 3 (move to front)
get(4):   hit → 4
```

### Code

**C++**
```cpp
class LRUCache {
    struct Node {
        int key, val;
        Node *prev, *next;
        Node(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}
    };
    unordered_map<int, Node*> mp;
    Node *head, *tail;   // sentinels: head=most recent side, tail=LRU side
    int cap;

    void remove(Node* n) {
        n->prev->next = n->next;
        n->next->prev = n->prev;
    }
    void insertFront(Node* n) {
        n->next = head->next;
        n->prev = head;
        head->next->prev = n;
        head->next = n;
    }
public:
    LRUCache(int capacity) : cap(capacity) {
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head->next = tail;
        tail->prev = head;
    }
    int get(int key) {
        if (!mp.count(key)) return -1;
        Node* n = mp[key];
        remove(n);
        insertFront(n);
        return n->val;
    }
    void put(int key, int value) {
        if (mp.count(key)) {
            Node* old = mp[key];
            remove(old);
            delete old;
        }
        Node* n = new Node(key, value);
        insertFront(n);
        mp[key] = n;
        if ((int)mp.size() > cap) {
            Node* lru = tail->prev;
            remove(lru);
            mp.erase(lru->key);
            delete lru;
        }
    }
};
```

**Java**
```java
class LRUCache {
    class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }
    private final Map<Integer, Node> mp = new HashMap<>();
    private final Node head, tail;   // sentinels
    private final int cap;

    private void remove(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }
    private void insertFront(Node n) {
        n.next = head.next;
        n.prev = head;
        head.next.prev = n;
        head.next = n;
    }
    public LRUCache(int capacity) {
        cap = capacity;
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    public int get(int key) {
        if (!mp.containsKey(key)) return -1;
        Node n = mp.get(key);
        remove(n);
        insertFront(n);
        return n.val;
    }
    public void put(int key, int value) {
        if (mp.containsKey(key)) {
            remove(mp.get(key));
        }
        Node n = new Node(key, value);
        insertFront(n);
        mp.put(key, n);
        if (mp.size() > cap) {
            Node lru = tail.prev;
            remove(lru);
            mp.remove(lru.key);
        }
    }
}
```

**Python**
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.mp = {}
        self.head = Node()   # most-recent side
        self.tail = Node()   # LRU side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, n: Node) -> None:
        n.prev.next = n.next
        n.next.prev = n.prev

    def _insert_front(self, n: Node) -> None:
        n.next = self.head.next
        n.prev = self.head
        self.head.next.prev = n
        self.head.next = n

    def get(self, key: int) -> int:
        if key not in self.mp:
            return -1
        n = self.mp[key]
        self._remove(n)
        self._insert_front(n)
        return n.val

    def put(self, key: int, value: int) -> None:
        if key in self.mp:
            self._remove(self.mp[key])
        n = Node(key, value)
        self._insert_front(n)
        self.mp[key] = n
        if len(self.mp) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.mp[lru.key]
```

### Complexity
- **Time**: O(1) average for both `get` and `put` — map lookup is O(1) average, and DLL splices are O(1) worst case.
- **Space**: O(capacity) — at most `capacity` nodes plus the map and two sentinels.

### Verdict
The textbook design and the answer interviewers expect. The two sentinels remove all null checks; the two helpers (`remove`, `insertFront`) keep the logic DRY. Master this — it's the foundation for LFU Cache and many design questions.

---

## Approach 2 — Built-in ordered map (language shortcut)

### Intuition
Some languages ship an insertion-ordered map that does the DLL bookkeeping for you. Java's `LinkedHashMap` even has a built-in access-order mode and an overridable eviction hook. Python's `OrderedDict` offers `move_to_end` and `popitem`. C++ has no standard equivalent, so we fall back to the manual implementation above.

### Algorithm (Java `LinkedHashMap` with access order)
1. Construct `LinkedHashMap` with `accessOrder = true`.
2. Override `removeEldestEntry` to return `size() > capacity` (auto-evicts on insert).
3. `get`: return value or `-1`. `put`: `put` into the map.

### Code

**C++** *(no standard ordered-by-use map — reuse the manual DLL solution from Approach 1)*
```cpp
// C++'s STL has no insertion/access-ordered hash map equivalent to
// LinkedHashMap / OrderedDict. The idiomatic O(1) solution in C++ IS the
// hash map + doubly linked list from Approach 1. (One alternative is to
// combine std::list<pair<int,int>> with an unordered_map<int, list iterator>.)
class LRUCache {
    list<pair<int,int>> dll;                                  // front = most recent
    unordered_map<int, list<pair<int,int>>::iterator> mp;
    int cap;
public:
    LRUCache(int capacity) : cap(capacity) {}
    int get(int key) {
        auto it = mp.find(key);
        if (it == mp.end()) return -1;
        dll.splice(dll.begin(), dll, it->second);  // move node to front, O(1)
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = mp.find(key);
        if (it != mp.end()) {
            it->second->second = value;
            dll.splice(dll.begin(), dll, it->second);
            return;
        }
        if ((int)dll.size() == cap) {
            int lruKey = dll.back().first;
            dll.pop_back();
            mp.erase(lruKey);
        }
        dll.push_front({key, value});
        mp[key] = dll.begin();
    }
};
```

**Java**
```java
class LRUCache {
    private final LinkedHashMap<Integer, Integer> map;
    public LRUCache(int capacity) {
        // accessOrder = true → most-recently-accessed moves to the end
        map = new LinkedHashMap<>(capacity, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
                return size() > capacity;
            }
        };
    }
    public int get(int key) {
        return map.getOrDefault(key, -1);
    }
    public void put(int key, int value) {
        map.put(key, value);
    }
}
```

**Python**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # mark most recently used
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)   # evict least recently used
```

### Complexity
- **Time**: O(1) average per operation — the library maintains the linked structure internally.
- **Space**: O(capacity).

### Verdict
Concise and production-friendly, but in an interview you should be ready to explain (or implement) what the library does under the hood — which is exactly Approach 1. Lead with the manual DLL design to prove you understand the mechanism, then mention the shortcut.

---

## ⚖️ Approach comparison

| Approach | get / put | Space | Notes |
|----------|-----------|-------|-------|
| Hash map + DLL (manual) | O(1) | O(capacity) | the expected, language-agnostic answer ⭐ |
| Built-in ordered map | O(1) | O(capacity) | concise; hides the mechanism; no C++ stdlib equivalent |

---

## 🧪 Edge cases & pitfalls
- **Updating an existing key** must refresh its recency *and* its value — don't just overwrite the value without moving it to the front.
- **Capacity 1** → every `put` of a new key evicts the previous one. Sentinels keep this correct.
- **`get` on a present key counts as a use** → it must move the node to the front, or recency tracking is wrong.
- **Pitfall — evicting before/after insert order**: insert the new node first, then check `size > cap` and evict. If you evict first you might wrongly drop a node when updating an existing key.
- **Pitfall — forgetting to erase the evicted key from the map**: removing the DLL node but leaving the map entry leaks memory and corrupts future lookups.
- **Pitfall — no sentinels**: without `head`/`tail` dummies you must special-case empty list, single node, and head/tail removal — a bug factory. Always use two sentinels.
- **Pitfall (Java `LinkedHashMap`) — forgetting `accessOrder = true`**: without it, `get` doesn't update recency and you implement FIFO, not LRU.

---

## 🔗 Related problems
- **LFU Cache** (LC 460) — evict least *frequently* used; combines a frequency map with per-frequency DLLs.
- **Design Linked List** (LC 707) — practice raw doubly-linked-list pointer surgery.
- **All O`one Data Structure** (LC 432) — another hash-map + DLL design.
- **Insert Delete GetRandom O(1)** (LC 380) — hash map + array design.

---

**→ Next:** [`10-Merge-K-Sorted-Lists.md`](./10-Merge-K-Sorted-Lists.md) | **← Prev:** [`08-Find-The-Duplicate-Number.md`](./08-Find-The-Duplicate-Number.md) | Back to [`00-Index.md`](./00-Index.md)
