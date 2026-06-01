# 🗂️ Greedy — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute force to the optimal greedy → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. The hard part of greedy is **proving** the local choice is globally optimal; every editorial walks through that argument. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Maximum Subarray](./01-Maximum-Subarray.md) | 53 | Medium | brute → divide & conquer → Kadane (greedy/DP) |
| 02 | [Jump Game](./02-Jump-Game.md) | 55 | Medium | backtracking → DP → greedy reach |
| 03 | [Jump Game II](./03-Jump-Game-II.md) | 45 | Medium | DP → greedy BFS-by-levels |
| 04 | [Gas Station](./04-Gas-Station.md) | 134 | Medium | brute → one-pass greedy |
| 05 | [Hand of Straights](./05-Hand-of-Straights.md) | 846 | Medium | sorted-map greedy → ordered count |
| 06 | [Merge Triplets to Form Target](./06-Merge-Triplets-To-Form-Target.md) | 1899 | Medium | greedy filter + flag |
| 07 | [Partition Labels](./07-Partition-Labels.md) | 763 | Medium | last-index greedy sweep |
| 08 | [Valid Parenthesis String](./08-Valid-Parenthesis-String.md) | 678 | Medium | DP → two-pass → range `[lo,hi]` greedy |

---

## 🎯 The pattern family

**Greedy** means we build the answer by repeatedly making the choice that looks best *right now*, never reconsidering. It is the fastest family of algorithms — usually a single linear pass — but the danger is that a locally optimal move can lock you out of the global optimum. So a greedy solution is only as good as its **proof**.

The recurring shapes in this set:

- **Running-state scan** (carry one or two scalars across the array): Maximum Subarray (`cur` running sum), Jump Game (`reach`), Jump Game II (`curEnd`/`farthest`), Gas Station (`tank`/`total`). The greedy is "extend while it helps, reset/advance when it can't."
- **Sort-then-consume**: Hand of Straights — always start a group from the smallest remaining card. Sorting exposes the forced choice.
- **Exchange / range tracking**: Valid Parenthesis String tracks an *interval* of possible open-paren counts; Merge Triplets keeps a boolean per target slot. The state is richer than one number but the pass is still single.
- **Last-occurrence sweep**: Partition Labels extends a window to the farthest last-index of any letter seen, cutting when the cursor catches the boundary.

### How to prove a greedy is correct

Three standard arguments show up again and again:

1. **Exchange argument** — assume an optimal solution differs from the greedy choice; show you can swap in the greedy choice without making the answer worse. (Hand of Straights, interval scheduling.)
2. **Stay-ahead** — show the greedy is always at least as far along as any other strategy after every step. (Jump Game II reaches index `i` in no more jumps than any alternative.)
3. **Invariant / impossibility** — prove that once a quantity goes bad, no earlier starting point could have helped, so skipping ahead is safe. (Gas Station: if the tank empties between `start` and `i`, no station in that range can be the answer.)

If you can't produce one of these, be suspicious — the problem may actually need DP. The bridge problem here is **Maximum Subarray**, which can be read as either greedy (discard a negative prefix) or 1D DP (`dp[i] = max(nums[i], dp[i-1]+nums[i])`); seeing both views is the whole point.

---

**→ Start:** [`01-Maximum-Subarray.md`](./01-Maximum-Subarray.md) | Back to [vault index](../00-Index.md)
