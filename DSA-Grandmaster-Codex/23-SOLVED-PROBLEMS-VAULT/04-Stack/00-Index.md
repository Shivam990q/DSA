# 🗂️ Stack — Problem Set

> Each problem is a complete editorial: full statement → every approach → C++ & Python code, complexity, edge cases.

---

## 📋 Problems

| # | Problem | LC # | Difficulty | Core Approaches |
|---|---------|------|------------|-----------------|
| 01 | [Valid Parentheses](./01-Valid-Parentheses.md) | 20 | Easy | stack matching |
| 02 | [Min Stack](./02-Min-Stack.md) | 155 | Medium | auxiliary min-stack / pairs |
| 03 | [Evaluate Reverse Polish Notation](./03-Evaluate-RPN.md) | 150 | Medium | operand stack |
| 04 | [Generate Parentheses](./04-Generate-Parentheses.md) | 22 | Medium | backtracking (stack-like) |
| 05 | [Daily Temperatures](./05-Daily-Temperatures.md) | 739 | Medium | monotonic stack |
| 06 | [Car Fleet](./06-Car-Fleet.md) | 853 | Medium | sort + stack/greedy |
| 07 | [Largest Rectangle in Histogram](./07-Largest-Rectangle-Histogram.md) | 84 | Hard | monotonic increasing stack |

---

## 🎯 The pattern family

**Stack** = LIFO. Two killer patterns:
- **Matching/nesting**: parentheses, tags, expressions → push openers, pop on closers.
- **Monotonic stack**: maintain increasing/decreasing order → "next greater/smaller" in O(n).

---

**→ Start:** [`01-Valid-Parentheses.md`](./01-Valid-Parentheses.md) | Back to [vault index](../00-Index.md)
