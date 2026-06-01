# 🔢 Algebraic Thinking

> *"Structure imposes constraints. Equations express constraints. Solving is manipulating algebra."*

---

## THE WORLDVIEW
Many problems hide algebraic structure: symmetries, invariants, group/monoid properties, linear relations. Exploit them.

## THE TRIGGERS
- Symmetries in the problem
- Invariants preserved by operations
- Group structure (games, transformations)
- Linear systems / matrix relations
- Associativity (enables segment trees, sparse tables)

## KEY CONCEPTS
- **Monoid**: associative operation + identity (enables segment trees: sum, min, max, gcd, matrix product)
- **Group**: monoid + inverses (enables prefix-sum-style differences)
- **Invariant**: quantity preserved by operations (parity, GCD, XOR sum)
- **Linear recurrence**: solvable via matrix exponentiation

## MANIFESTATIONS
- Matrix exponentiation for linear recurrences (Fibonacci in O(log n))
- XOR invariants in Nim/games (Sprague-Grundy)
- Parity arguments for impossibility proofs
- Segment trees require associative operations
- Möbius inversion (algebraic number theory)
- Gaussian elimination (linear systems, XOR basis)

## THE INVARIANT POWER MOVE
When operations are allowed, ask: "What algebraic quantity is preserved?" If source and target differ in that invariant, the transformation is impossible.

## THE ASSOCIATIVITY INSIGHT
A range query DS (segment tree, sparse table) works iff the operation is associative. Sum, min, max, gcd, matrix product all qualify. This is why "range gcd query" works but "range mode query" needs different tools.

## EXERCISE
1. Why can a segment tree do range-GCD but not range-mode easily?
2. Nim: when does the second player win? → XOR of pile sizes = 0
3. Fibonacci via matrix: [[1,1],[1,0]]^n
4. Can you reach board state B from A by allowed swaps? → check permutation parity invariant

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | [`13-COMPENDIUM-Mental-Models.md`](./13-COMPENDIUM-Mental-Models.md)
