# 🎲 Probabilistic Thinking

> *"When determinism is hard, randomness is a tool. When worst case is rare, expected case is what matters."*

---

## THE WORLDVIEW
Randomness can simplify algorithms, break adversarial symmetry, and provide bounded-error answers fast.

## THE TRIGGERS
- "Adversarial worst case is rare in practice"
- "Use randomness to break symmetry / avoid worst case"
- "Approximate with bounded error is acceptable"
- Expected value / probability problems

## TWO FLAVORS
- **Las Vegas**: always correct, runtime is random (randomized quicksort)
- **Monte Carlo**: bounded runtime, small error probability (Miller-Rabin)

## KEY TOOLS
- **Linearity of expectation**: E[X+Y] = E[X]+E[Y], always
- **Indicator variables**: X_i = 1 if event i; E[count] = Σ P(event i)
- **Markov's inequality**: P(X ≥ a) ≤ E[X]/a
- **Chernoff bounds**: tight concentration for sums of independent variables
- **Union bound**: P(A∪B) ≤ P(A) + P(B)

## MANIFESTATIONS
- Randomized quicksort (random pivot avoids O(n²))
- Treap, skip list (random balancing)
- Miller-Rabin (probabilistic primality)
- Reservoir sampling (uniform from stream)
- Bloom filter, HyperLogLog, Count-Min (probabilistic DS)
- Karger's min cut

## THE POWER MOVE
For expected-value problems, decompose into indicator variables and use linearity. This turns hard expectations into sums of simple probabilities.

## EXERCISE
1. Expected comparisons in randomized quicksort → O(n log n) via P(i,j compared) = 2/(j−i+1)
2. Expected number of fixed points in a random permutation → 1 (linearity)
3. Why does a random pivot make quicksort's O(n²) worst case astronomically unlikely?
4. Coupon collector: expected draws to collect all n coupons → n·H(n) ≈ n ln n

---

**→ Next:** [`11-Geometric-Thinking.md`](./11-Geometric-Thinking.md)
