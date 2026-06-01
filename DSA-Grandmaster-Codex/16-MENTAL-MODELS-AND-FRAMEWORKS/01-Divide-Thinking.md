# ✂️ Divide Thinking

> *"Break the giant into ants. Solve the ants. Reassemble the giant."*

---

## THE WORLDVIEW
Every complex problem is the combination of solutions to simpler problems. Divide thinking asks: *"How can I split this?"*

## THE TRIGGERS
- "Can I split the input in half?"
- "Can I separate into independent cases?"
- "Can I solve subproblem A and B separately, then merge?"
- Recursion tree with branching

## MANIFESTATIONS
- Merge sort, quick sort (divide array)
- Binary search (divide search space)
- FFT (divide polynomial by even/odd coefficients)
- Strassen (divide matrix into quadrants)
- Closest pair of points (divide plane)
- Divide & conquer DP

## THE TEMPLATE
```
solve(problem):
    if small enough: solve directly (base case)
    split problem into subproblems
    solve each subproblem recursively
    combine sub-solutions into the full solution
```

## THE MASTER THEOREM CONNECTION
T(n) = a·T(n/b) + f(n). The recursion tree has log_b(n) levels. Divide thinking's cost is determined by how much work the "combine" step does.

## WHEN TO USE
- Subproblems are independent (no overlap → use DP instead if overlapping)
- Combine step is cheap
- Natural recursive structure

## EXERCISE
For each, find the divide:
1. Count inversions in an array → (merge sort)
2. Find the kth smallest element → (quickselect)
3. Multiply two large numbers → (Karatsuba)
4. Find majority element → (divide and count)

---

**→ Next:** [`02-Recursive-Thinking.md`](./02-Recursive-Thinking.md) | Full reference: [`13-COMPENDIUM-Mental-Models.md`](./13-COMPENDIUM-Mental-Models.md)
