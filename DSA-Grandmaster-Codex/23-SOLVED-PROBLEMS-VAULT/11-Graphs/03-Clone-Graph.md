# Clone Graph

**Platform**: LeetCode 133 · **Difficulty**: Medium · **Topics**: Hash Table, DFS, BFS, Graph · **Pattern**: Graph traversal with a visited→clone map

---

## 📜 Problem Statement

Given a reference of a node in a **connected** undirected graph, return a **deep copy** (clone) of the graph.

Each node in the graph contains a value (`int`) and a list (`List[Node]`) of its neighbors.

```
class Node {
    public int val;
    public List<Node> neighbors;
}
```

**Test case format**: For simplicity, each node's value is the same as the node's index (1-indexed). The graph is represented in the test using an adjacency list. The given node is always the first node with `val = 1`.

You must return the **copy of the given node** as a reference to the cloned graph.

### Examples

**Example 1:**
```
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]
Explanation:
Node 1's neighbors are 2 and 4.
Node 2's neighbors are 1 and 3.
Node 3's neighbors are 2 and 4.
Node 4's neighbors are 1 and 3.
```

**Example 2:**
```
Input: adjList = [[]]
Output: [[]]
Explanation: There is a single node with no neighbors.
```

**Example 3:**
```
Input: adjList = []
Output: []
Explanation: The graph is empty (the given node is null).
```

### Constraints
```
The number of nodes in the graph is in the range [0, 100].
1 <= Node.val <= 100
Node.val is unique for each node.
There are no repeated edges and no self-loops in the graph.
The Graph is connected and all nodes can be visited starting from the given node.
```

---

## 🧠 Understanding the problem

We must build a brand-new graph that is structurally identical to the input but shares **no node objects** with it. The challenge is cycles: the graph is undirected, so node 1 points to node 2 and node 2 points back to node 1. A naive recursion that clones a node and then recurses into every neighbor would loop forever.

The fix is a **visited map** `original → clone`. Before cloning a node's neighbors, we record its clone in the map. When traversal revisits a node (which it will, because of cycles), we return the already-created clone instead of making a new one. This map does double duty: it prevents infinite loops *and* guarantees each original node maps to exactly one clone, preserving shared references.

So this is a standard DFS/BFS traversal where "process a node" means "allocate its clone and wire up its neighbor list."

---

## Approach 1 — DFS with hash map (recommended) ⭐

### Intuition
Recurse through the graph. The first time you see a node, create its clone and store it in the map *before* recursing into neighbors (so a cycle back to this node finds the clone already present). Then clone each neighbor and append it to the current clone's neighbor list.

### Algorithm
1. Keep a map `seen: original → clone`.
2. `clone(node)`:
   - If `node` is null → return null.
   - If `node` already in `seen` → return `seen[node]`.
   - Create `copy = new Node(node.val)`; put `seen[node] = copy`.
   - For each neighbor `nb`: `copy.neighbors.push(clone(nb))`.
   - Return `copy`.
3. Return `clone(start)`.

### Dry run on Example 1 (`1—2—3—4—1`, a 4-cycle with chords)
```
clone(1): create 1'. seen={1:1'}. neighbors of 1 = [2,4].
  clone(2): create 2'. seen={1:1',2:2'}. neighbors of 2 = [1,3].
    clone(1): 1 in seen → return 1'.        (cycle handled)
    clone(3): create 3'. neighbors=[2,4].
      clone(2): in seen → return 2'.
      clone(4): create 4'. neighbors=[1,3].
        clone(1): return 1'.  clone(3): return 3'.
      4'.neighbors=[1',3']. return 4'.
    3'.neighbors=[2',4']. return 3'.
  2'.neighbors=[1',3']. return 2'.
  clone(4): in seen → return 4'.
1'.neighbors=[2',4']. return 1'.
```

### Code

```cpp
/*
// Definition for a Node.
class Node {
public:
    int val;
    vector<Node*> neighbors;
    Node() { val = 0; neighbors = vector<Node*>(); }
    Node(int _val) { val = _val; neighbors = vector<Node*>(); }
    Node(int _val, vector<Node*> _neighbors) { val = _val; neighbors = _neighbors; }
};
*/
class Solution {
public:
    Node* cloneGraph(Node* node) {
        unordered_map<Node*, Node*> seen;
        return clone(node, seen);
    }
private:
    Node* clone(Node* node, unordered_map<Node*, Node*>& seen) {
        if (!node) return nullptr;
        if (seen.count(node)) return seen[node];
        Node* copy = new Node(node->val);
        seen[node] = copy;
        for (Node* nb : node->neighbors)
            copy->neighbors.push_back(clone(nb, seen));
        return copy;
    }
};
```
```java
/*
// Definition for a Node.
class Node {
    public int val;
    public List<Node> neighbors;
    public Node() { val = 0; neighbors = new ArrayList<Node>(); }
    public Node(int _val) { val = _val; neighbors = new ArrayList<Node>(); }
    public Node(int _val, ArrayList<Node> _neighbors) { val = _val; neighbors = _neighbors; }
}
*/
class Solution {
    public Node cloneGraph(Node node) {
        return clone(node, new HashMap<>());
    }

    private Node clone(Node node, Map<Node, Node> seen) {
        if (node == null) return null;
        if (seen.containsKey(node)) return seen.get(node);
        Node copy = new Node(node.val);
        seen.put(node, copy);
        for (Node nb : node.neighbors)
            copy.neighbors.add(clone(nb, seen));
        return copy;
    }
}
```
```python
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        seen = {}

        def clone(n):
            if not n:
                return None
            if n in seen:
                return seen[n]
            copy = Node(n.val)
            seen[n] = copy
            for nb in n.neighbors:
                copy.neighbors.append(clone(nb))
            return copy

        return clone(node)
```

### Complexity
- **Time**: O(V + E) — each node created once, each edge traversed once.
- **Space**: O(V) for the map plus O(V) recursion stack.

---

## Approach 2 — BFS with hash map

### Intuition
Same map, but explore iteratively with a queue. Create the start's clone first, then for each dequeued original node, clone any not-yet-seen neighbor and link clones. Avoids recursion depth issues on long chains.

### Algorithm
1. If `node` is null → return null.
2. Create the clone of `node`; store in `seen`; enqueue `node`.
3. While the queue is non-empty:
   - Pop `cur`.
   - For each neighbor `nb`:
     - If `nb` not in `seen` → create its clone, store, enqueue `nb`.
     - Append `seen[nb]` to `seen[cur].neighbors`.
4. Return `seen[node]`.

### Dry run on Example 1 (start node 1)
```
seen={1:1'}, queue=[1].
Pop 1: neighbors [2,4].
   2 new → 2', enqueue; link 1'->2'.
   4 new → 4', enqueue; link 1'->4'.
Pop 2: neighbors [1,3].
   1 seen; link 2'->1'.
   3 new → 3', enqueue; link 2'->3'.
Pop 4: neighbors [1,3]; both seen; link 4'->1', 4'->3'.
Pop 3: neighbors [2,4]; both seen; link 3'->2', 3'->4'.
Return 1'.
```

### Code

```cpp
class Solution {
public:
    Node* cloneGraph(Node* node) {
        if (!node) return nullptr;
        unordered_map<Node*, Node*> seen;
        seen[node] = new Node(node->val);
        queue<Node*> q;
        q.push(node);
        while (!q.empty()) {
            Node* cur = q.front(); q.pop();
            for (Node* nb : cur->neighbors) {
                if (!seen.count(nb)) {
                    seen[nb] = new Node(nb->val);
                    q.push(nb);
                }
                seen[cur]->neighbors.push_back(seen[nb]);
            }
        }
        return seen[node];
    }
};
```
```java
class Solution {
    public Node cloneGraph(Node node) {
        if (node == null) return null;
        Map<Node, Node> seen = new HashMap<>();
        seen.put(node, new Node(node.val));
        Queue<Node> q = new LinkedList<>();
        q.offer(node);
        while (!q.isEmpty()) {
            Node cur = q.poll();
            for (Node nb : cur.neighbors) {
                if (!seen.containsKey(nb)) {
                    seen.put(nb, new Node(nb.val));
                    q.offer(nb);
                }
                seen.get(cur).neighbors.add(seen.get(nb));
            }
        }
        return seen.get(node);
    }
}
```
```python
from collections import deque

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None
        seen = {node: Node(node.val)}
        q = deque([node])
        while q:
            cur = q.popleft()
            for nb in cur.neighbors:
                if nb not in seen:
                    seen[nb] = Node(nb.val)
                    q.append(nb)
                seen[cur].neighbors.append(seen[nb])
        return seen[node]
```

### Complexity
- **Time**: O(V + E).
- **Space**: O(V) for the map and queue.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| DFS + map | O(V+E) | O(V) | shortest code; map prevents cycles ⭐ |
| BFS + map | O(V+E) | O(V) | no recursion; identical correctness |

Both rely on the same insight (the `original → clone` map). Pick whichever traversal you are more comfortable writing; correctness hinges on inserting into the map **before** exploring neighbors.

---

## 🧪 Edge cases & pitfalls
- **Empty graph** (`node == null`) → return null. Easy to forget; both versions guard it.
- **Single node, no neighbors** → clone with an empty neighbor list.
- **Self reference via cycles** — the whole point of the map; without it you recurse/enqueue forever.
- **Inserting into the map too late** (after the neighbor loop) reintroduces infinite recursion. Insert the clone *before* recursing.
- **Returning a node by value instead of the cloned reference** — the answer must be the clone of the *given* node.

---

## 🔗 Related problems
- **Copy List with Random Pointer** (LC 138) — same `original → copy` map trick on a linked list.
- **Clone N-ary Tree** (LC 1490) — tree version, no cycle handling needed.
- **Number of Connected Components** (LC 323) — traversal with a visited set.
- **Course Schedule** (LC 207) — adjacency-list traversal of a directed graph.

---

**→ Next:** [`04-Rotting-Oranges.md`](./04-Rotting-Oranges.md) | **← Prev:** [`02-Max-Area-of-Island.md`](./02-Max-Area-of-Island.md) | [Problem set index](./00-Index.md)
