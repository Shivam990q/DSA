# 🧬 SOS DP (Sum Over Subsets)

> *"For every mask, aggregate over all its submasks — in O(n·2ⁿ), not O(3ⁿ)."*

---

## I. THE PROBLEM
Given f(mask) for all masks, compute:
```
g(mask) = Σ over all submasks s of mask: f(s)
```
- Naive (enumerate submasks of each mask): O(3ⁿ).
- **SOS DP**: O(n · 2ⁿ).

---

## II. THE ALGORITHM ⭐
Process one bit at a time. For each bit i, add the contribution from masks that have bit i, pulling from the version without bit i.
```cpp
// g initialized to f
for (int i = 0; i < n; i++)
    for (int mask = 0; mask < (1 << n); mask++)
        if (mask & (1 << i))
            g[mask] += g[mask ^ (1 << i)];
```
After processing all n bits, `g[mask]` = sum of f over all submasks of mask.

**Why it works**: it's a "subset-sum convolution" performed dimension by dimension (like an n-dimensional prefix sum over the hypercube).

---

## III. THE DUAL: SUM OVER SUPERSETS
To compute, for each mask, the sum of f over all **supersets**:
```cpp
for (int i = 0; i < n; i++)
    for (int mask = 0; mask < (1 << n); mask++)
        if (!(mask & (1 << i)))
            g[mask] += g[mask ^ (1 << i)];
```

---

## IV. APPLICATIONS
1. **Count pairs (i,j) with a[i] & a[j] == a[i]** (subset relationships)
2. **Subset-sum convolutions** (combine two functions over subsets)
3. **Bitmask DP transitions** that aggregate over submasks
4. **Counting / inclusion-exclusion over subsets**
5. **Maximum/sum over all submasks** of each mask
6. AND/OR convolutions (closely related)

---

## V. RELATED: BITWISE CONVOLUTIONS
- **OR convolution**: c[k] = Σ over i|j==k of a[i]·b[j] → use SOS (superset/subset zeta + Möbius transforms).
- **AND convolution**: dual of OR.
- **XOR convolution**: **FWHT** (Fast Walsh-Hadamard Transform), O(n·2ⁿ).

These are the "subset/bitwise FFT" analogs.

---

## VI. COMPLEXITY
O(n · 2ⁿ) time, O(2ⁿ) space. Feasible for n ≤ ~20-22.

---

## VII. WHEN TO USE
- You have values indexed by bitmasks and need "for each mask, aggregate over submasks/supersets."
- Bitmask DP where the transition would otherwise enumerate submasks (O(3ⁿ)).

---

## VIII. PROBLEMS
- Compatible Numbers (CF) — for each a[i], does a submask exist in the array?
- Counting subset/superset relationships
- CF problems tagged "bitmasks" + "dp" with subset aggregation
- Subset-sum convolution problems

---

## IX. NOTE
SOS DP is a slick Level 6-7 technique. The four-line loop is deceptively powerful — it's an n-dimensional prefix sum over the subset lattice.

---

**→ Next:** [`17-Profile-DP.md`](./17-Profile-DP.md)
