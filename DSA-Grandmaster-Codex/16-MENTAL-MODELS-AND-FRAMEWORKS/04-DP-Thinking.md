# 🧬 DP Thinking

> *"Future decisions depend only on a finite state — the rest of history is irrelevant."*

---

## THE WORLDVIEW
A problem is DP when (1) it has optimal substructure and (2) overlapping subproblems. The art is finding the minimal STATE.

## THE TRIGGERS
- "Number of ways to..."
- "Min/max cost/length/sum..."
- "Longest/shortest..."
- "Can we transform A to B?"
- Constraints hinting O(n²) or O(n·k)

## THE STATE QUESTION
"What's the smallest piece of information that determines all future decisions?" That's your state.

## THE 5-STEP FRAMEWORK
1. Define state: dp[...] = ?
2. Define transition: dp[...] depends on which smaller states?
3. Define base case
4. Determine computation order
5. Locate the answer

## MANIFESTATIONS
- 1D (climbing stairs, house robber)
- 2D (grid paths, LCS, edit distance)
- Knapsack (subset selection)
- Interval (burst balloons, matrix chain)
- Tree (subtree aggregates)
- Bitmask (TSP, subset states)
- Digit (counting in ranges)

## THE INSIGHT
DP = memoized recursion + topological order. If you can write the recursion AND it repeats subproblems, you have DP.

## EXERCISE
Find the state:
1. Edit distance → (i, j) positions in two strings
2. Coin change → (amount remaining)
3. TSP → (visited set, current city)
4. Stock with cooldown → (day, holding?, cooldown?)

---

**→ Next:** [`05-Greedy-Thinking.md`](./05-Greedy-Thinking.md) | Deep dive: [`../06-DYNAMIC-PROGRAMMING-UNIVERSE/00-Index.md`](../06-DYNAMIC-PROGRAMMING-UNIVERSE/00-Index.md)
