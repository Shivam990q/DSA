# 📖 IOI "Aliens" and the Birth of the Aliens Trick

> *"One problem at IOI 2016 gave its name to an entire optimization technique."*

---

## I. THE PROBLEM (IOI 2016 "Aliens")
- **Setup**: photograph points on a grid using at most k square photos; minimize total area covered.
- **The constraint**: "at most k" photos is the troublemaker.

---

## II. THE NAIVE DP
- `dp[i][j]` = min cost covering first i points with j photos.
- O(n²k) — too slow for large n, k.

---

## III. THE ALIENS TRICK (Lagrangian Relaxation)
**The insight**: instead of fixing exactly k photos, add a penalty λ per photo and DROP the "exactly k" constraint.

- Solve `dp'[i]` = min(cost + λ × photos_used) WITHOUT the count constraint. This is faster (often O(n log n) with CHT).
- The number of photos used decreases as λ increases (monotonic!).
- **Binary search on λ** until the optimal uses exactly k photos.

**Result**: O(n log n log(maxCost)) instead of O(n²k).

---

## IV. WHEN THE ALIENS TRICK APPLIES
- "Exactly k" partition / selection problems
- The cost function (as a function of k) is CONVEX
- Removing the "k" constraint makes the problem much easier
- The number of items used is monotonic in the Lagrange multiplier λ

---

## V. THE GENERAL TEMPLATE
```
function solve(lambda):
    # DP without the "exactly k" constraint,
    # but each "use" costs an extra lambda.
    # Returns (optimal cost, count of items used)

binary search lambda:
    if count(lambda) > k: increase lambda (penalize more)
    else: decrease lambda
until count == k
adjust final answer by subtracting lambda*k
```

---

## VI. THE BROADER LESSON
The Aliens trick exemplifies a deep idea: **relaxing a hard constraint with a penalty (Lagrangian relaxation)** is a general optimization technique from continuous optimization, adapted to discrete DP.

This is how research-level ideas flow into competitive programming.

---

## VII. WHERE IT'S USED
- "Exactly k segments" partition problems
- "Exactly k edges" in trees
- Many "with exactly k operations" CP problems

---

## VIII. PREREQUISITES TO UNDERSTAND IT
- Convex Hull Trick (for the inner DP)
- Convexity of the cost function
- Binary search on real/integer λ

Study at Level 7 (Elite CP).

---

**→ Next:** [`05-CF-Greatest-Hits.md`](./05-CF-Greatest-Hits.md)
