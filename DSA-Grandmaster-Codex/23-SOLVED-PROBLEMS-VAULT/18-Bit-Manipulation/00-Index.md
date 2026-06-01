# 🗂️ Bit Manipulation — Problem Set

> Each problem below is a **complete editorial**: full statement (platform-style) → every approach from the obvious counting/arithmetic method to the slick bit trick → intuition, algorithm, dry run, C++ & Java & Python code, complexity, edge cases, pitfalls, and related problems.

> **How to use**: open a problem, read ONLY the statement, attempt it cold (30–45 min). Then read the approaches in order — feel WHY each one improves on the last. These reward memorizing a handful of identities and then *seeing* where they apply. Re-derive the optimal from the key insight after 7 days.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Single Number](./01-Single-Number.md) | 136 | Easy | hash/sum → XOR fold |
| 02 | [Number of 1 Bits](./02-Number-of-1-Bits.md) | 191 | Easy | shift-and-test → `n & (n-1)` |
| 03 | [Counting Bits](./03-Counting-Bits.md) | 338 | Easy | per-number popcount → DP recurrences |
| 04 | [Reverse Bits](./04-Reverse-Bits.md) | 190 | Easy | bit-by-bit → byte-cached |
| 05 | [Missing Number](./05-Missing-Number.md) | 268 | Easy | sum formula → XOR fold |
| 06 | [Sum of Two Integers](./06-Sum-of-Two-Integers.md) | 371 | Medium | XOR sum + AND carry |
| 07 | [Reverse Integer](./07-Reverse-Integer.md) | 7 | Medium | pop/push digits with overflow guard |

---

## 🎯 The pattern family

**Bit manipulation** is about treating an integer as a vector of bits and exploiting the algebra of `AND`, `OR`, `XOR`, and shifts. Two identities carry most of these problems:

- **`a ^ a = 0` and `a ^ 0 = a`** (XOR cancels pairs). This collapses Single Number (one unpaired value survives) and Missing Number (XOR indices against values, the gap survives).
- **`n & (n - 1)` clears the lowest set bit.** This makes Number of 1 Bits run in "popcount" time and underlies the Counting Bits DP.

### The cheat sheet

| Trick | Effect |
|-------|--------|
| `x & 1` | parity (lowest bit) |
| `x >> 1` | divide by 2 (drop lowest bit) |
| `x << 1` | multiply by 2 |
| `x & (x - 1)` | clear the lowest set bit |
| `x & -x` | isolate the lowest set bit |
| `a ^ a = 0`, `a ^ 0 = a` | XOR cancels pairs |
| `a + b = (a ^ b) + ((a & b) << 1)` | sum = XOR (no-carry) + carry |

### The recurring shapes

- **XOR fold** over an array to cancel duplicates / find a gap (Single Number, Missing Number).
- **Bit loop** — process 32 bits, shifting in/out (Reverse Bits, Number of 1 Bits, Sum of Two Integers).
- **Bit DP** — define `bits[i]` from a smaller already-computed value using a one-bit relation (Counting Bits).
- **Digit pop/push with overflow guard** — Reverse Integer is "bit manipulation" by association but really decimal-digit surgery with a careful 32-bit bounds check.

### A note on languages

Python integers are **arbitrary precision** and have no fixed 32-bit width, so problems that rely on overflow wraparound (Sum of Two Integers, Reverse Bits) need explicit **masking** with `0xFFFFFFFF` and manual sign reinterpretation. Each affected editorial calls this out.

---

**→ Start:** [`01-Single-Number.md`](./01-Single-Number.md) | Back to [vault index](../00-Index.md)
