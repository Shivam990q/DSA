# 🌐 Graph Thinking

> *"Everything is a graph if you squint. Objects are vertices. Relationships are edges."*

---

## THE WORLDVIEW
Any problem about discrete objects with relationships is a graph problem. The skill: SEE the hidden graph.

## THE TRIGGERS
- Things connected to other things
- States that transition to other states
- Dependencies, prerequisites, hierarchies
- Networks, friends, paths, flows

## THE MODELING SKILL
Ask:
1. **What are the vertices?** (the objects/states)
2. **What are the edges?** (the relationships/transitions)
3. **Directed or undirected? Weighted?**

## HIDDEN GRAPHS — EXAMPLES
| Problem            | Vertices       | Edges                  |
|--------------------|----------------|------------------------|
| Word Ladder        | words          | 1-letter changes       |
| Course Schedule    | courses        | prerequisites          |
| Sliding Puzzle     | board states   | single moves           |
| Currency Arbitrage | currencies     | exchange rates (log)   |
| Number of Islands  | grid cells     | adjacent land          |

## MANIFESTATIONS
- BFS (shortest path unweighted)
- DFS (components, cycles)
- Dijkstra/Bellman-Ford (weighted shortest path)
- Topological sort (dependencies)
- Union-Find (connectivity)
- MST (minimum connection cost)
- Flow (capacity/matching)

## THE STATE-GRAPH INSIGHT
Many non-graph problems become graphs when you treat *states* as vertices and *transitions* as edges. (Sliding puzzle, BFS on configurations.)

## EXERCISE
Model as a graph:
1. "Minimum moves for knight to reach target" → vertices = cells, edges = knight moves
2. "Can tasks be ordered given dependencies?" → topological sort
3. "Detect arbitrage in currency exchange" → negative cycle (Bellman-Ford on log rates)

---

**→ Next:** [`04-DP-Thinking.md`](./04-DP-Thinking.md) | Deep dive: [`../07-GRAPH-THEORY-UNIVERSE/00-Index.md`](../07-GRAPH-THEORY-UNIVERSE/00-Index.md)
