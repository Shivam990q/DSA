# Reconstruct Itinerary

**Platform**: LeetCode 332 · **Difficulty**: Hard · **Topics**: Graph, DFS, Eulerian Circuit/Path · **Pattern**: Hierholzer's Eulerian path

---

## 📜 Problem Statement

You are given a list of airline `tickets` where `tickets[i] = [fromi, toi]` represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.

All of the tickets belong to a man who departs from `"JFK"`, thus, the itinerary must begin with `"JFK"`. If there are multiple valid itineraries, you should return the itinerary that has the **smallest lexical order** when read as a single string.

- For example, the itinerary `["JFK", "LGA"]` has a smaller lexical order than `["JFK", "LGB"]`.

You may assume all tickets form **at least one** valid itinerary. You must use **all** the tickets once and only once.

### Examples

**Example 1:**
```
Input: tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
Output: ["JFK","MUC","LHR","SFO","SJC"]
```

**Example 2:**
```
Input: tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
Output: ["JFK","ATL","JFK","SFO","ATL","SFO"]
Explanation: Another possible reconstruction is
["JFK","SFO","ATL","JFK","ATL","SFO"] but it is larger in lexical order.
```

**Example 3:**
```
Input: tickets = [["JFK","KUL"],["JFK","NRT"],["NRT","JFK"]]
Output: ["JFK","NRT","JFK","KUL"]
Explanation: You must take NRT first (to use that return ticket) before KUL,
even though "KUL" < "NRT", otherwise you'd strand the NRT->JFK ticket.
```

### Constraints
```
1 <= tickets.length <= 300
tickets[i].length == 2
fromi.length == 3
toi.length == 3
fromi and toi consist of uppercase English letters.
fromi != toi
```

---

## 🧠 Understanding the problem

Each ticket is a **directed edge** that must be used **exactly once**. Visiting every edge exactly once is precisely an **Eulerian path**. The problem guarantees at least one valid Eulerian path starting at "JFK", and asks for the lexicographically smallest one.

A naive greedy "always fly to the smallest next airport" fails — Example 3 shows that flying to "KUL" first (smaller than "NRT") strands the "NRT→JFK" ticket. We need an algorithm that produces a valid Eulerian path while preferring small airports *without* getting stuck.

**Hierholzer's algorithm** does exactly this. Walk forward, always taking the smallest available outgoing edge. When you reach a vertex with no remaining edges (a dead end), you "retreat" it onto the answer in **post-order**. Reversing the post-order yields a valid Eulerian path. The key insight: a dead-end vertex must be the *last* airport in the remaining itinerary, so prepending it (via reverse of post-order) is always correct. Sorting neighbors ascending makes the result lexicographically smallest.

---

## Approach 1 — Hierholzer's algorithm, iterative with a stack (recommended) ⭐

### Intuition
Keep airports sorted so we always try the smallest next hop. Use an explicit stack as the current path. If the top airport still has unused tickets, follow the smallest one (push the destination). If it has none left, it is a dead end — pop it into the route. Reverse the route at the end.

### Algorithm
1. Build `adj[from]` as a sorted structure of destinations (so we can pop the smallest in O(1) or O(log)).
2. Stack `st = ["JFK"]`; empty `route`.
3. While the stack is non-empty:
   - Let `u = st.top()`. If `adj[u]` still has a destination, pop its smallest `v` and push `v`.
   - Else (dead end), pop `u` from the stack and append to `route`.
4. Reverse `route` and return it.

### Dry run on Example 3 (`JFK→KUL, JFK→NRT, NRT→JFK`)
```
adj: JFK:[KUL,NRT] (sorted), NRT:[JFK].
stack=[JFK].
top JFK has dests → take KUL? smallest is KUL. push KUL. stack=[JFK,KUL].
top KUL no dests → pop to route. route=[KUL]. stack=[JFK].
top JFK has NRT → push NRT. stack=[JFK,NRT].
top NRT has JFK → push JFK. stack=[JFK,NRT,JFK].
top JFK no dests → pop. route=[KUL,JFK]. stack=[JFK,NRT].
top NRT no dests → pop. route=[KUL,JFK,NRT]. stack=[JFK].
top JFK no dests → pop. route=[KUL,JFK,NRT,JFK].
reverse → [JFK,NRT,JFK,KUL]. ✓
```

### Code

```cpp
class Solution {
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string, multiset<string>> adj;
        for (auto& t : tickets) adj[t[0]].insert(t[1]);
        vector<string> route;
        stack<string> st;
        st.push("JFK");
        while (!st.empty()) {
            string u = st.top();
            if (!adj[u].empty()) {
                string v = *adj[u].begin();
                adj[u].erase(adj[u].begin());
                st.push(v);
            } else {
                route.push_back(u);
                st.pop();
            }
        }
        reverse(route.begin(), route.end());
        return route;
    }
};
```
```java
class Solution {
    public List<String> findItinerary(List<List<String>> tickets) {
        Map<String, PriorityQueue<String>> adj = new HashMap<>();
        for (List<String> t : tickets)
            adj.computeIfAbsent(t.get(0), x -> new PriorityQueue<>()).offer(t.get(1));
        LinkedList<String> route = new LinkedList<>();
        Deque<String> st = new ArrayDeque<>();
        st.push("JFK");
        while (!st.isEmpty()) {
            String u = st.peek();
            PriorityQueue<String> dests = adj.get(u);
            if (dests != null && !dests.isEmpty()) {
                st.push(dests.poll());
            } else {
                route.addFirst(u);   // prepend == reverse of post-order
                st.pop();
            }
        }
        return route;
    }
}
```
```python
import heapq

class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adj = {}
        for a, b in tickets:
            adj.setdefault(a, []).append(b)
        for a in adj:
            heapq.heapify(adj[a])      # min-heap → smallest destination first

        route = []
        stack = ["JFK"]
        while stack:
            u = stack[-1]
            if adj.get(u):
                stack.append(heapq.heappop(adj[u]))
            else:
                route.append(stack.pop())
        return route[::-1]
```

### Complexity
- **Time**: O(E log E) — each edge handled once; the sorted structure (multiset / priority queue) costs log per operation.
- **Space**: O(E) for the adjacency structure, stack, and route.

---

## Approach 2 — Hierholzer's algorithm, recursive DFS

### Intuition
The same post-order idea expressed with recursion. Recurse into the smallest available destination repeatedly until stuck, then append the current airport to the route. Reverse at the end.

### Algorithm
1. Build sorted adjacency lists.
2. `dfs(u)`: while `adj[u]` has a destination, remove the smallest `v` and `dfs(v)`. After the loop, append `u` to `route`.
3. Call `dfs("JFK")`, then reverse `route`.

> Note: removing the smallest from the front of a sorted list is O(n); using an index pointer or a deque avoids that cost. The version below sorts in reverse and pops from the back for O(1) removal.

### Dry run on Example 1 (`JFK→MUC→LHR→SFO→SJC`, a single chain)
```
dfs(JFK): take MUC → dfs(MUC): take LHR → dfs(LHR): take SFO →
  dfs(SFO): take SJC → dfs(SJC): no dests → route=[SJC].
  back in SFO → route=[SJC,SFO]. ... → route=[SJC,SFO,LHR,MUC,JFK].
reverse → [JFK,MUC,LHR,SFO,SJC]. ✓
```

### Code

```cpp
class Solution {
    unordered_map<string, vector<string>> adj;
    vector<string> route;
    void dfs(const string& u) {
        while (!adj[u].empty()) {
            string v = adj[u].back();   // smallest, since sorted descending
            adj[u].pop_back();
            dfs(v);
        }
        route.push_back(u);
    }
public:
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        for (auto& t : tickets) adj[t[0]].push_back(t[1]);
        for (auto& [k, v] : adj) sort(v.rbegin(), v.rend());  // descending
        dfs("JFK");
        reverse(route.begin(), route.end());
        return route;
    }
};
```
```java
class Solution {
    private Map<String, List<String>> adj = new HashMap<>();
    private LinkedList<String> route = new LinkedList<>();

    public List<String> findItinerary(List<List<String>> tickets) {
        for (List<String> t : tickets)
            adj.computeIfAbsent(t.get(0), x -> new ArrayList<>()).add(t.get(1));
        for (List<String> dests : adj.values())
            dests.sort(Collections.reverseOrder());  // descending → pop from end
        dfs("JFK");
        return route;
    }

    private void dfs(String u) {
        List<String> dests = adj.get(u);
        while (dests != null && !dests.isEmpty()) {
            String v = dests.remove(dests.size() - 1);  // smallest remaining
            dfs(v);
        }
        route.addFirst(u);   // prepend == reverse of post-order
    }
}
```
```python
class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adj = {}
        for a, b in tickets:
            adj.setdefault(a, []).append(b)
        for a in adj:
            adj[a].sort(reverse=True)   # descending → pop() gives smallest

        route = []

        def dfs(u):
            dests = adj.get(u)
            while dests:
                dfs(dests.pop())        # pop() removes the smallest remaining
            route.append(u)

        dfs("JFK")
        return route[::-1]
```

### Complexity
- **Time**: O(E log E) — sorting the adjacency lists dominates.
- **Space**: O(E) for the adjacency lists plus O(E) recursion depth.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Hierholzer iterative (stack) | O(E log E) | O(E) | no recursion; multiset/heap for smallest edge ⭐ |
| Hierholzer recursive (DFS) | O(E log E) | O(E) | concise; sort descending + pop back for O(1) removal |

Both implement the same Eulerian-path algorithm. The crucial idea — append a vertex to the route only when it has no unused edges (post-order), then reverse — is what makes the greedy "smallest first" choice safe.

---

## 🧪 Edge cases & pitfalls
- **Why post-order works**: a dead-end vertex can only be the final airport of the remaining trip. Appending dead-ends and reversing guarantees a valid Eulerian path even when the greedy smallest choice would otherwise strand edges (Example 3).
- **Lexical order**: neighbors must be consumed smallest-first. With a multiset/min-heap pop the front; with a list sorted descending pop the back.
- **Removing the front of a plain sorted list is O(n)** — sort descending and pop the back, or use an index pointer, to keep it efficient.
- **Multi-edges allowed**: the same `from→to` ticket can appear multiple times; a multiset / list (not a set) is required.
- **All tickets must be used** — the route length is always `tickets.length + 1`.

---

## 🔗 Related problems
- **Cracking the Safe** (LC 753) — Eulerian circuit over de Bruijn sequences.
- **Valid Arrangement of Pairs** (LC 2097) — Eulerian path with degree-based start selection.
- **Course Schedule II** (LC 210) — different ordering (topological vs Eulerian).
- **Word Ladder** (LC 127) — also a path-construction problem, but shortest-path flavored.

---

**→ Next:** [`06-Min-Cost-Make-Network-Connected.md`](./06-Min-Cost-Make-Network-Connected.md) | **← Prev:** [`04-Swim-In-Rising-Water.md`](./04-Swim-In-Rising-Water.md) | [Problem set index](./00-Index.md)
