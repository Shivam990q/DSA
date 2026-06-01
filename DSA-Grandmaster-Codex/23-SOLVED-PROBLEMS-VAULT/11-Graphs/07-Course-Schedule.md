# Course Schedule

**Platform**: LeetCode 207 · **Difficulty**: Medium · **Topics**: DFS, BFS, Graph, Topological Sort · **Pattern**: Cycle detection in a directed graph

---

## 📜 Problem Statement

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

- For example, the pair `[0, 1]` indicates that to take course `0` you have to first take course `1`.

Return `true` if you can finish all courses. Otherwise, return `false`.

### Examples

**Example 1:**
```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are 2 courses. To take course 1 you should have
finished course 0. So it is possible.
```

**Example 2:**
```
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: To take course 1 you need course 0, and to take course 0
you need course 1. That is a cycle — impossible.
```

**Example 3:**
```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: true
Explanation: A valid order is 0 → 1 → 2 → 3 (3 depends on both 1 and 2).
```

### Constraints
```
1 <= numCourses <= 2000
0 <= prerequisites.length <= 5000
prerequisites[i].length == 2
0 <= ai, bi < numCourses
All the pairs prerequisites[i] are unique.
```

---

## 🧠 Understanding the problem

Model courses as nodes and each prerequisite `[a, b]` as a **directed edge `b → a`** (take `b`, then you can take `a`). You can finish all courses **if and only if** this directed graph has **no cycle**. A cycle means a set of courses each waiting on another in a loop — you could never start any of them.

So the problem is pure **cycle detection in a directed graph**. Two standard tools:

- **Kahn's algorithm (BFS topological sort)**: repeatedly remove nodes with in-degree 0. If you remove all `numCourses` nodes, the graph is acyclic; if some remain stuck (all in a cycle), it is not.
- **DFS with three colors**: track nodes currently on the recursion stack. Reaching a node that is already on the stack means a back-edge → cycle.

Constraints are small (≤ 2000 nodes, ≤ 5000 edges), so either O(V + E) approach is comfortable.

---

## Approach 1 — Kahn's algorithm / BFS topological sort (recommended) ⭐

### Intuition
A course with **no remaining prerequisites** (in-degree 0) can be taken now. Take it, then "release" its dependents by decrementing their in-degrees; any that drop to 0 become takeable. If we manage to take every course this way, there is no cycle.

### Algorithm
1. Build an adjacency list `adj` and an `indeg` array. For each `[a, b]`: add edge `b → a`, `indeg[a]++`.
2. Push all nodes with `indeg == 0` into a queue.
3. `taken = 0`. While the queue is non-empty:
   - Pop `u`, `taken++`.
   - For each `v` in `adj[u]`: decrement `indeg[v]`; if it hits 0, enqueue `v`.
4. Return `taken == numCourses`.

### Dry run on Example 3 (`edges 0→1, 0→2, 1→3, 2→3`)
```
indeg: 0:0, 1:1, 2:1, 3:2.
queue=[0]. taken=0.
Pop 0 → taken=1. release 1 (indeg 0 → enqueue), 2 (indeg 0 → enqueue).
Pop 1 → taken=2. release 3 (indeg 1).
Pop 2 → taken=3. release 3 (indeg 0 → enqueue).
Pop 3 → taken=4.
taken == 4 == numCourses → true.
```

### Code

```cpp
class Solution {
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        vector<vector<int>> adj(numCourses);
        vector<int> indeg(numCourses, 0);
        for (auto& p : prerequisites) {
            adj[p[1]].push_back(p[0]);
            indeg[p[0]]++;
        }
        queue<int> q;
        for (int i = 0; i < numCourses; i++)
            if (indeg[i] == 0) q.push(i);
        int taken = 0;
        while (!q.empty()) {
            int u = q.front(); q.pop();
            taken++;
            for (int v : adj[u])
                if (--indeg[v] == 0) q.push(v);
        }
        return taken == numCourses;
    }
};
```
```java
class Solution {
    public boolean canFinish(int numCourses, int[][] prerequisites) {
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
        int taken = 0;
        while (!q.isEmpty()) {
            int u = q.poll();
            taken++;
            for (int v : adj.get(u))
                if (--indeg[v] == 0) q.offer(v);
        }
        return taken == numCourses;
    }
}
```
```python
from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indeg[a] += 1
        q = deque(i for i in range(numCourses) if indeg[i] == 0)
        taken = 0
        while q:
            u = q.popleft()
            taken += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return taken == numCourses
```

### Complexity
- **Time**: O(V + E) — each node and edge processed once.
- **Space**: O(V + E) for the adjacency list, in-degree array, and queue.

---

## Approach 2 — DFS cycle detection (three-color)

### Intuition
Walk the graph with DFS. Color each node: `0` unvisited, `1` in the current recursion path, `2` fully processed. If DFS reaches a node colored `1`, we have looped back onto the current path → a cycle exists.

### Algorithm
1. Build the adjacency list (`b → a`).
2. `state[i]` all start at `0`.
3. `dfs(u)`:
   - If `state[u] == 1` → cycle → return `false`.
   - If `state[u] == 2` → already safe → return `true`.
   - Set `state[u] = 1`; recurse into all neighbors; if any returns `false`, propagate `false`.
   - Set `state[u] = 2`; return `true`.
4. Run `dfs` from every node; if any reports a cycle, return `false`.

### Dry run on Example 2 (`edges 0→1, 1→0`)
```
dfs(0): state[0]=1. neighbor 1.
  dfs(1): state[1]=1. neighbor 0.
    dfs(0): state[0]==1 → cycle → false.
  returns false.
returns false → overall false.
```

### Code

```cpp
class Solution {
    vector<vector<int>> adj;
    vector<int> state;
    bool dfs(int u) {
        if (state[u] == 1) return false;   // on current path → cycle
        if (state[u] == 2) return true;    // already proven safe
        state[u] = 1;
        for (int v : adj[u])
            if (!dfs(v)) return false;
        state[u] = 2;
        return true;
    }
public:
    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        adj.assign(numCourses, {});
        state.assign(numCourses, 0);
        for (auto& p : prerequisites) adj[p[1]].push_back(p[0]);
        for (int i = 0; i < numCourses; i++)
            if (!dfs(i)) return false;
        return true;
    }
};
```
```java
class Solution {
    private List<List<Integer>> adj;
    private int[] state;

    public boolean canFinish(int numCourses, int[][] prerequisites) {
        adj = new ArrayList<>();
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        state = new int[numCourses];
        for (int[] p : prerequisites) adj.get(p[1]).add(p[0]);
        for (int i = 0; i < numCourses; i++)
            if (!dfs(i)) return false;
        return true;
    }

    private boolean dfs(int u) {
        if (state[u] == 1) return false;
        if (state[u] == 2) return true;
        state[u] = 1;
        for (int v : adj.get(u))
            if (!dfs(v)) return false;
        state[u] = 2;
        return true;
    }
}
```
```python
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            adj[b].append(a)
        state = [0] * numCourses  # 0 unvisited, 1 on path, 2 done

        def dfs(u):
            if state[u] == 1:
                return False
            if state[u] == 2:
                return True
            state[u] = 1
            for v in adj[u]:
                if not dfs(v):
                    return False
            state[u] = 2
            return True

        return all(dfs(i) for i in range(numCourses))
```

### Complexity
- **Time**: O(V + E).
- **Space**: O(V + E) for the graph plus O(V) recursion stack.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Kahn's BFS | O(V+E) | O(V+E) | iterative, no recursion; also yields an order ⭐ |
| DFS 3-color | O(V+E) | O(V+E) | concise; watch recursion depth (up to 2000) |

Both detect cycles in linear time. Kahn's doubles as a topological-sort generator (used directly in Course Schedule II), while DFS is shorter to write. The three-color invariant — "gray means on the current stack" — is the crux of DFS correctness.

---

## 🧪 Edge cases & pitfalls
- **No prerequisites** → always `true` (every course has in-degree 0).
- **Self-dependency** `[x, x]` → an immediate cycle → `false` (constraints here forbid duplicate pairs but not all variants do).
- **Disconnected components** — both algorithms must start from *every* node, not just node 0.
- **Edge direction** — `[a, b]` means `b → a`. Reversing it flips prerequisites and silently breaks the answer.
- **Counting with `taken`** in Kahn's: comparing against `numCourses` is what detects a leftover cycle.

---

## 🔗 Related problems
- **Course Schedule II** (LC 210) — same graph, but return an actual valid ordering.
- **Alien Dictionary** (LC 269) — build the precedence graph, then topological sort.
- **Find Eventual Safe States** (LC 802) — DFS color-based cycle reasoning.
- **Minimum Height Trees** (LC 310) — peel leaves like Kahn's algorithm.

---

**→ Next:** [`08-Course-Schedule-II.md`](./08-Course-Schedule-II.md) | **← Prev:** [`06-Surrounded-Regions.md`](./06-Surrounded-Regions.md) | [Problem set index](./00-Index.md)
