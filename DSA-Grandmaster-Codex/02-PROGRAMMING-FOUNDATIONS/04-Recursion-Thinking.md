# 🌀 Recursion Thinking — The Self-Similar Mind

> *"To understand recursion, you must first understand recursion."*

---

## I. THE ESSENCE

Recursion = **a function defined in terms of itself**, on smaller subproblems.

Three required components:
1. **Base case** — a stop condition (smallest subproblem solved directly)
2. **Recursive case** — solve via smaller subproblem(s)
3. **Combination** — combine subproblem solutions into the current solution

```python
def factorial(n):
    if n == 0: return 1                  # base case
    return n * factorial(n - 1)          # recursive case + combination
```

---

## II. THE INDUCTION VIEW

Recursion = **mathematical induction in code form**.

To prove `P(n)` holds:
- Base: prove `P(0)` (or `P(1)`).
- Inductive step: assume `P(k)`, prove `P(k+1)`.

To write recursion:
- Base case: solve smallest input.
- Recursive case: assume `f(smaller)` works, write `f(n)` using it.

**This means**: while writing recursion, **trust** the recursive call. Don't dive into implementation; trust the contract.

---

## III. THE LEAP OF FAITH

When you write:
```python
def fibonacci(n):
    if n <= 1: return n
    return fibonacci(n-1) + fibonacci(n-2)
```

You **trust** that `fibonacci(n-1)` returns the correct (n-1)th Fibonacci. You **trust** that `fibonacci(n-2)` returns the correct (n-2)th. You add them. You're done.

You don't trace 5 levels deep. You **trust the contract**.

This is the recursion **leap of faith**. It is the single most important mindset shift in this skill.

---

## IV. RECURSION TREES

Visualize recursion as a tree:

```
                fib(5)
              /       \
         fib(4)       fib(3)
         /    \        /    \
     fib(3) fib(2)  fib(2) fib(1)
     /  \    / \    / \
  fib(2) ... ... ...
```

**Insight**: same subproblems appear multiple times! → memoize → O(2ⁿ) becomes O(n).

This is **the discovery of dynamic programming**. You're already doing it in your head.

---

## V. THE CALL STACK

Each function call adds a **stack frame**:
```
[fib(2)]
[fib(3)]
[fib(4)]
[fib(5)]
[main]
```

When `fib(2)` returns, its frame pops. Each frame holds local variables + return address.

**Stack overflow**: too-deep recursion exhausts stack memory. Default stack: ~1-8 MB. Each frame: ~50-200 bytes. → recursion depth limit ~50K-100K.

If your recursion is `O(n)` deep with n = 10⁶, stack overflows. Convert to iteration with explicit stack.

---

## VI. RECURSIVE PATTERNS

### Pattern A: **Reduce-by-One**
`f(n) = g(f(n-1), n)`
> Examples: factorial, sum 1..n, reverse string

### Pattern B: **Divide-and-Conquer**
`f(n) = combine(f(n/2), f(n/2))`
> Examples: merge sort, quick sort, binary search

### Pattern C: **Multiple Recursion**
`f(n) = combine(f(n-1), f(n-2), ...)`
> Examples: fibonacci, climbing stairs

### Pattern D: **Tree Recursion**
`f(node) = combine(f(node.left), f(node.right), node.val)`
> Examples: tree height, tree diameter, max path sum

### Pattern E: **Backtracking**
`f(state) = for each choice c: try c; recurse; undo c`
> Examples: N-queens, sudoku, permutations

---

## VII. WRITING RECURSION — A PROCEDURE

1. **Define the contract** — "What does my function compute?"
2. **Identify base case(s)** — when input is smallest, what's the answer?
3. **Identify recursive case** — assume smaller works; build current using it
4. **Verify by trace** — trace small inputs by hand
5. **Test edge cases** — n=0, n=1, single-element

---

## VIII. RECURSION VS ITERATION

|              | Recursion             | Iteration             |
|--------------|-----------------------|-----------------------|
| Readability  | Often higher (especially trees, DP) | Usually higher for sequences |
| Performance  | Function call overhead | Tighter inner loop  |
| Memory       | O(depth) stack space   | O(1) usually        |
| When to use  | Trees, divide-conquer, backtrack | Sequences, simple counting |

**Conversion**: any recursive can become iterative with an explicit stack. Tail recursion can become a simple loop.

---

## IX. TAIL RECURSION

A recursive call is **tail-recursive** if it's the *last* operation in the function (no further work after the call):

```python
# Tail-recursive
def factorial_tail(n, acc=1):
    if n == 0: return acc
    return factorial_tail(n - 1, acc * n)

# NOT tail-recursive (multiplication after the call)
def factorial(n):
    if n == 0: return 1
    return n * factorial(n - 1)
```

Some compilers (Scheme, Haskell, sometimes C++ with -O2) optimize tail calls into loops, eliminating stack growth. Python and Java do *not*.

---

## X. COMMON BUGS

1. **Missing base case** → infinite recursion → stack overflow
2. **Wrong base case** → wrong answer for smallest inputs
3. **Not making progress toward base** → infinite recursion
4. **Off-by-one in recursive call** → subtle wrong answers
5. **Mutating shared state** → unpredictable results

---

## XI. RECURSION → DP

When recursion has **overlapping subproblems**, memoize:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)
```

This is **top-down DP** = recursion + memoization.

**Bottom-up DP** = explicit table, fill in topological order. Same complexity, no recursion overhead.

---

## XII. RECURSION → BACKTRACKING

Backtracking is recursion with **state mutation + undo**:

```python
def backtrack(state):
    if is_solution(state):
        record(state)
        return
    for choice in valid_choices(state):
        make_choice(state, choice)
        backtrack(state)
        undo_choice(state, choice)
```

The "undo" is critical. Without it, branches contaminate each other.

---

## XIII. THE 30 RECURSION DRILLS

Until each is "Stage 4" (you can teach it):
1. Factorial
2. Fibonacci
3. Power
4. Sum 1..n
5. Reverse string
6. Reverse number
7. GCD (Euclidean)
8. Tower of Hanoi
9. Print all subsets
10. Print all permutations
11. Print all combinations of size k
12. Climbing stairs
13. Generate parentheses
14. Word break (return all sentences)
15. N-queens
16. Sudoku solver
17. Knight's tour
18. Tree height
19. Tree mirror (invert)
20. LCA in binary tree
21. Path sum
22. Merge sort
23. Quick sort
24. Binary search
25. K-th smallest in BST (with state)
26. Diameter of binary tree
27. Maximum path sum (binary tree)
28. Print path from root to leaf with sum k
29. Generate all paths in DAG
30. Robot in grid (count unique paths with obstacles)

---

## XIV. THE FINAL TRUTH

> **"Recursion is not a coding technique.  
>  It is a way of seeing.  
>  When you see a problem and notice it contains a smaller version of itself —  
>  you have seen recursively.  
>  The code is just transcription."**

---

**→ Next:** [`05-State-Modeling.md`](./05-State-Modeling.md)
