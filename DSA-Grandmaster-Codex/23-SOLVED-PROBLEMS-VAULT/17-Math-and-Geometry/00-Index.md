# 🗂️ Math & Geometry — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from brute simulation to the clever in-place / numeric trick → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. These problems reward **clean index arithmetic** and **spotting the pattern over brute simulation**. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Rotate Image](./01-Rotate-Image.md) | 48 | Medium | extra matrix → transpose + reverse → 4-way cycle |
| 02 | [Spiral Matrix](./02-Spiral-Matrix.md) | 54 | Medium | four shrinking boundaries |
| 03 | [Set Matrix Zeroes](./03-Set-Matrix-Zeroes.md) | 73 | Medium | extra sets → O(m+n) → first row/col markers |
| 04 | [Pow(x, n)](./04-Pow-X-N.md) | 50 | Medium | naive loop → fast exponentiation |
| 05 | [Multiply Strings](./05-Multiply-Strings.md) | 43 | Medium | schoolbook digit convolution |
| 06 | [Happy Number](./06-Happy-Number.md) | 202 | Easy | hash-set cycle → Floyd fast/slow |
| 07 | [Plus One](./07-Plus-One.md) | 66 | Easy | digit carry from the right |
| 08 | [Detect Squares](./08-Detect-Squares.md) | 2013 | Medium | point-count map + diagonal scan |

---

## 🎯 The pattern family

This bucket mixes two flavors that share a mindset: **don't simulate when you can reason**.

**Matrix manipulation** (Rotate Image, Spiral Matrix, Set Matrix Zeroes) is about **index discipline**. The recurring tools:

- **Transpose + reverse** to rotate without a second matrix (`(i,j) → (j,i)`, then flip rows).
- **Boundary shrinking** to traverse in a spiral (`top/bottom/left/right` pointers contract after each side).
- **In-place markers**: reuse the matrix's own first row and column as scratch space to hit O(1) extra space (Set Matrix Zeroes).

**Number tricks** (Pow, Multiply Strings, Happy Number, Plus One, Detect Squares) reward **mathematical structure**:

- **Fast exponentiation** halves the exponent (`x^n = (x^2)^{n/2}`) for O(log n) — the same binary-decomposition idea appears in modular exponentiation and matrix power.
- **Positional arithmetic**: digit `i × j` lands at result positions `i+j` and `i+j+1` (Multiply Strings); carry propagates right-to-left (Plus One).
- **Cycle detection**: a process that either terminates or loops is a job for a hash set or Floyd's tortoise-and-hare (Happy Number) — the very same trick as Linked List Cycle.
- **Counting with a hash map**: Detect Squares stores point frequencies and multiplies counts of the other two corners.

### The meta-lesson

Brute force here usually means "build a whole new structure" or "simulate every step." The optimal almost always either **edits in place using the structure you already have** or **replaces O(n) work with an O(log n) / O(1) formula**. Train yourself to ask: *can I avoid the extra array? can I avoid the loop with math?*

---

**→ Start:** [`01-Rotate-Image.md`](./01-Rotate-Image.md) | Back to [vault index](../00-Index.md)
