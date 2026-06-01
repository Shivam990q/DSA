# 🌀 Recursive Thinking

> *"A problem's solution often contains the solution to a smaller version of itself."*

---

## THE WORLDVIEW
See self-similarity. When a problem at size n can be expressed using the answer at size n-1 (or n/2), you're thinking recursively.

## THE TRIGGERS
- "What if the input were one element smaller?"
- Trees, lists, self-similar structures
- "Try a choice, recurse, undo" (backtracking)
- Nested / fractal structure

## THE LEAP OF FAITH
When writing recursion, TRUST that the recursive call works for smaller inputs. Don't trace 5 levels deep. State the contract: "f(n) returns X, given f(n-1) returns X for size n-1."

## MANIFESTATIONS
- Tree traversals
- Backtracking (subsets, permutations, N-queens)
- Divide and conquer
- DP (memoized recursion)
- Recursive descent parsing

## THE THREE PARTS
1. **Base case**: smallest input solved directly
2. **Recursive case**: solve via smaller subproblem
3. **Combination**: merge sub-results

## RECURSION → DP
When recursion has overlapping subproblems, memoize → top-down DP. When you can order subproblems, tabulate → bottom-up DP.

## EXERCISE
Express recursively:
1. Factorial, Fibonacci, GCD
2. Tree height, tree diameter
3. All subsets, all permutations
4. Tower of Hanoi

---

**→ Next:** [`03-Graph-Thinking.md`](./03-Graph-Thinking.md) | Deep dive: [`../02-PROGRAMMING-FOUNDATIONS/04-Recursion-Thinking.md`](../02-PROGRAMMING-FOUNDATIONS/04-Recursion-Thinking.md)
