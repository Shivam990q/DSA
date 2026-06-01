# Course Schedule II

**Platform**: LeetCode 210 · **Difficulty**: Medium · **Topics**: DFS, BFS, Graph, Topological Sort · **Pattern**: Topological ordering of a DAG

---

## 📜 Problem Statement

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

- For example, the pair `[0, 1]` indicates that to take course `0` you have to first take course `1`.

Return *the ordering of courses you should take to finish all courses*. If there are many valid answers, return **any** of them. If it is impossible to finish all courses, return **an empty array**.

### Examples

**Example 1:**
```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: To take course 1 you must first take course 0, so the order is [0,1].
```

**Example 2:**
```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,1,2,3]
Explanation: [0,2,1,3] is also valid. Course 0 first; courses 1 and 2 next;
course 3 last (it needs both 1 and 2).
```

**Example 3:**
```
Input: numCourses = 1, prerequisites = []
Output: [0]
```

### Constraints
```
1 <= numCourses <= 2000
0 <= prerequisites.length <= numCourses * (numCourses - 1)
prerequisites[i].length == 2
0 <= ai, bi < numCourses
ai != bi
All the pairs [ai, bi] are distinct.
```

---

## 🧠 Understanding the problem

This is **Course Schedule** (LC 207) but instead of just answering "is it possible?", we must produce **one valid topological order** — a linear ordering of the nodes such that every edge `b → a` puts `b` before `a`. If a cycle exists, no ordering is possible and we return `[]`.

Same two engines apply:

- **Kahn's algorithm** builds the order *forward*: it appends a node the moment all its prerequisites are satisfied. If it cannot append all `numCourses` nodes, a cycle blocked it → return `[]`.
- **DFS post-order** builds the order *backward*: a node is appended after all its descendants are processed; reversing the post-order gives a topological order. A cycle is detected with the three-color trick.

We again model `[a, b]` as the directed edge `b → a`.

---

## Approach 1 — Kahn's algorithm / BFS (recommended) ⭐

### Intuition
Record the order in which courses become takeable. Start with all in-degree-0 courses, append each as it is removed, and release its dependents. The append sequence is a valid order. If the sequence does not cover every course, a cycle exists.

### Algorithm
1. Build `adj` and `indeg`. For each `[a, b]`: edge `b → a`, `indeg[a]++`.
2. Enqueue all nodes with `indeg == 0`.
3. While the queue is non-empty: pop `u`, append `u` to `order`, decrement neighbors' in-degrees, enqueue any that hit 0.
4. Return `order` if `order.size() == numCourses`, else `[]`.

### Dry run on Example 2 (`0→1, 0→2, 1→3, 2→3`)
```
indeg: 0:0, 1:1, 2:1, 3:2. queue=[0].
Pop 0 → order=[0]. release 1,2 → both indeg 0 → enqueue.
Pop 1 → order=[0,1]. release 3 → indeg 1.
Pop 2 → order=[0,1,2]. release 3 → indeg 0 → enqueue.
Pop 3 → order=[0,1,2,3].
size 4 == numCourses → return [0,1,2,3].
```

### Code

```cpp
class Solution {
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> indeg(numCourses, 0);
        for (auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            indeg[p[0]]++;
        }
        queue<int> q;
        for (int i = 0; i < numCourses; i++)
            if (indeg[i] == 0) q.push(i);
        vector<int> order;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            order.push_back(u);
            for (int v : adj[u])
                if (--indeg[v] == 0) q.push(v);
        }
        return (int)order.size() == numCourses ? order : vector<int>{};
    }
};
```
```java
class Solution {
    public int[] findOrder(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        int[] indeg = new int[numCourses];
        for (int[] p : prerequisites) {
            adj.get(p[1]).add(p[0]);
            indeg[p[0]]++;
        }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++)
            if (indeg[i] == 0) q.offer(i);
        int[] order = new int[numCourses];
        int idx = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            order[idx++] = u;
            for (int v : adj.get(u))
                if (--indeg[v] == 0) q.offer(v);
        }
        return idx == numCourses ? order : new int[0];
    }
}
```
```python
from collections import deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == numCourses else []
```

### Complexity
- **Time**: O(V + E).
- **Space**: O(V + E).

---

## Approach 2 — DFS post-order (with cycle detection)

### Intuition
In a DAG, if you append a node **after** visiting all nodes it points to, you get a reverse topological order; reversing it yields a valid order. Detect cycles with the three-color state so an impossible input returns `[]`.

### Algorithm
1. Build the adjacency list (`b → a`).
2. `state[i]`: `0` unvisited, `1` on the current path, `2` done.
3. `dfs(u)`:
   - If `state[u] == 1` → cycle → signal failure.
   - If `state[u] == 2` → return.
   - Mark `1`; recurse all neighbors; mark `2`; push `u` to `order`.
4. After visiting every node, if no cycle, reverse `order` and return it; otherwise return `[]`.

### Dry run on Example 1 (`edge 0→1`)
```
dfs(0): state[0]=1. neighbor 1.
  dfs(1): state[1]=1. no neighbors. state[1]=2. order=[1].
state[0]=2. order=[1,0].
reverse → [0,1].
```

### Code

```cpp
class Solution {
    vector<vector<int>> adj;
    vector<int> state, order;
    bool cyclic = false;
    void dfs(int u) {
        if (state[u] == 1) { cyclic = true; return; }
        if (state[u] == 2) return;
        state[u] = 1;
        for (int v : adj[u]) {
            dfs(v);
            if (cyclic) return;
        }
        state[u] = 2;
        order.push_back(u);
    }
public:
    vector<int> findOrder(int numCourses, vector<vector<int>>& prerequisites) {
        adj.assign(numCourses, {});
        state.assign(numCourses, 0);
        for (auto& p : prerequisites) adj[p[1]].push_back(p[0]);
        for (int i = 0; i < numCourses; i++) {
            dfs(i);
            if (cyclic) return {};
        }
        reverse(order.begin(), order.end());
        return order;
    }
};
```
```java
class Solution {
    private List<List<Integer>> adj;
    private int[] state;
    private List<Integer> order;
    private boolean cyclic;

    public int[] findOrder(int numCourses, int[][] prerequisites) {
        adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        state = new int[numCourses];
        order = new ArrayList<>();
        cyclic = false;
        for (int[] p : prerequisites) adj.get(p[1]).add(p[0]);
        for (int i = 0; i < numCourses; i++) {
            dfs(i);
            if (cyclic) return new int[0];
        }
        Collections.reverse(order);
        int[] res = new int[numCourses];
        for (int i = 0; i < numCourses; i++) res[i] = order.get(i);
        return res;
    }

    private void dfs(int u) {
        if (state[u] == 1) { cyclic = true; return; }
        if (state[u] == 2) return;
        state[u] = 1;
        for (int v : adj.get(u)) {
            dfs(v);
            if (cyclic) return;
        }
        state[u] = 2;
        order.add(u);
    }
}
```
```python
class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            adj[b].append(a)
        state = [0] * numCourses  # 0 unvisited, 1 on path, 2 done
        order = []
        self.cyclic = False

        def dfs(u):
            if state[u] == 1:
                self.cyclic = True
                return
            if state[u] == 2:
                return
            state[u] = 1
            for v in adj[u]:
                dfs(v)
                if self.cyclic:
                    return
            state[u] = 2
            order.append(u)

        for i in range(numCourses):
            dfs(i)
            if self.cyclic:
                return []
        order.reverse()
        return order
```

### Complexity
- **Time**: O(V + E).
- **Space**: O(V + E) plus O(V) recursion.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Order produced | Notes |
|----------|------|-------|----------------|-------|
| Kahn's BFS | O(V+E) | O(V+E) | forward (append on release) | iterative; cycle check via count ⭐ |
| DFS post-order | O(V+E) | O(V+E) | reversed post-order | concise; needs 3-color cycle guard |

Both yield a valid (not necessarily identical) topological order. Kahn's is preferred when you want to avoid recursion and get cycle detection "for free" via the size check.

---

## 🧪 Edge cases & pitfalls
- **No prerequisites** → any permutation is valid; both produce `[0, 1, ..., n-1]` or similar.
- **Cycle present** → must return `[]`, not a partial order. The size check (Kahn) or `cyclic` flag (DFS) handles this.
- **DFS without cycle detection** would emit a bogus order on cyclic input. The three-color guard is mandatory here.
- **Forgetting to reverse** the DFS post-order gives the *reverse* topological order — a subtle, common bug.
- **Edge direction** — `[a, b]` ⇒ `b → a`.

---

## 🔗 Related problems
- **Course Schedule** (LC 207) — feasibility only (no order needed).
- **Alien Dictionary** (LC 269) — derive ordering constraints, then topologically sort.
- **Sequence Reconstruction** (LC 444) — check whether a unique topological order exists.
- **Parallel Courses** (LC 1136) — topological "levels" = minimum semesters.

---

**→ Next:** [`09-Number-of-Connected-Components.md`](./09-Number-of-Connected-Components.md) | **← Prev:** [`07-Course-Schedule.md`](./07-Course-Schedule.md) | [Problem set index](./00-Index.md)
