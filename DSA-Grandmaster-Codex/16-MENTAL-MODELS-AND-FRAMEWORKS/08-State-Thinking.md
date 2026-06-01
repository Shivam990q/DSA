# 🎚️ State Thinking

> *"The system at any moment is fully described by its state. Find the minimal sufficient state."*

---

## THE WORLDVIEW
Many problems reduce to: "What's the minimal information needed to determine future behavior?" That's the state.

## THE TRIGGERS
- DP problems (state = subproblem identifier)
- BFS/DFS on configurations (state = node)
- Simulations (state = variables describing "where I am")
- Game positions

## THE MARKOV PROPERTY
Good state design satisfies: the future depends only on the current state, not the path taken to reach it.

## THE QUESTIONS
1. What's varying as decisions are made?
2. What can I drop (redundant info)?
3. What can I compress (sets → bitmasks, coordinates → indices)?
4. What are the transitions between states?

## STATE EXAMPLES
| Problem              | State                          |
|----------------------|--------------------------------|
| Climbing stairs      | current step                   |
| Knapsack             | (item index, capacity left)    |
| TSP                  | (visited bitmask, current city)|
| Edit distance        | (i, j) positions               |
| Stock with cooldown  | (day, holding?, cooldown?)     |
| 8-puzzle             | board configuration            |

## STATE COMPRESSION TECHNIQUES
- Drop dimensions derivable from others
- Bitmask for small sets (n ≤ 20)
- Coordinate compression for sparse large values
- Hash for arbitrary complex states
- Rolling arrays when only recent states matter

## THE TRAP
- Over-stating: extra dimensions → exponential blowup
- Under-stating: missing info → wrong answer

## EXERCISE
Design minimal state:
1. Longest increasing path in matrix → (cell)
2. Paint house (no adjacent same color) → (house, last color)
3. Dice rolls to reach target → (rolls used, sum)
4. Word break → (start index)

---

**→ Next:** [`09-Systems-Thinking.md`](./09-Systems-Thinking.md) | Deep dive: [`../03-PROBLEM-SOLVING-FOUNDATIONS/07-State-Design.md`](../03-PROBLEM-SOLVING-FOUNDATIONS/07-State-Design.md)
