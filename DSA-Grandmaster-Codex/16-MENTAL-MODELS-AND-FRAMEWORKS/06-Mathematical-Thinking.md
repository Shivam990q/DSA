# ➗ Mathematical Thinking

> *"Many problems have closed-form, formulaic, or structurally elegant solutions hiding behind the noise."*

---

## THE WORLDVIEW
Before brute-forcing, ask: "Is there a formula? A pattern? A mathematical structure?"

## THE TRIGGERS
- Counting problems ("how many ways")
- Modular arithmetic ("mod 10⁹+7")
- Number theory (divisibility, primes, GCD)
- Combinatorics (selections, arrangements)
- Probability / expected value
- Large constraints (n ≤ 10¹⁸ → must be formula/log)

## KEY TOOLS
- **Sums**: 1+2+...+n = n(n+1)/2
- **Combinatorics**: nCr, Catalan, stars-and-bars
- **Modular**: inverse, fast exponentiation
- **Number theory**: GCD, sieve, totient
- **Linear algebra**: matrix exponentiation for recurrences
- **Probability**: linearity of expectation

## THE POWER MOVE: LINEARITY OF EXPECTATION
E[X+Y] = E[X] + E[Y], always. Break complex expectations into simple indicator variables.

## MANIFESTATIONS
- Counting paths via combinations (grid paths = C(m+n, m))
- Fibonacci in O(log n) via matrix exponentiation
- Counting with inclusion-exclusion
- Expected value via indicators

## THE SMALL-CASE METHOD
Compute n=1,2,3,4,5 by hand. Find the pattern/formula. (Often reveals the closed form.)

## EXERCISE
Find the math:
1. Number of ways to climb n stairs (1 or 2 steps) → Fibonacci
2. Number of paths in m×n grid → C(m+n, m)
3. Expected number of comparisons in random quicksort → O(n log n) via linearity
4. Sum of first n cubes → (n(n+1)/2)²

---

**→ Next:** [`07-Optimization-Thinking.md`](./07-Optimization-Thinking.md) | Deep dive: [`../09-MATHEMATICS-UNIVERSE/00-Index.md`](../09-MATHEMATICS-UNIVERSE/00-Index.md)
