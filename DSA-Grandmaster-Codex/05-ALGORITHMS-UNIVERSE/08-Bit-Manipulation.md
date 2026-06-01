# 🎯 Bit Manipulation

> *"Numbers are sets of bits. Master the bits, master a hidden layer of speed."*

---

## I. THE OPERATORS
- `&` AND, `|` OR, `^` XOR, `~` NOT, `<<` left shift, `>>` right shift

---

## II. THE ESSENTIAL TRICKS ⭐
```cpp
n & (1 << i)        // is bit i set?
n | (1 << i)        // set bit i
n & ~(1 << i)       // clear bit i
n ^ (1 << i)        // toggle bit i
n & -n              // lowest set bit (isolate)
n & (n - 1)         // clear lowest set bit
n | (n + 1)         // set lowest clear bit
__builtin_popcount(n)   // count set bits (popcountll for long long)
__builtin_ctz(n)        // count trailing zeros
__builtin_clz(n)        // count leading zeros
__lg(n)                 // floor(log2(n)) = index of highest set bit
n && !(n & (n - 1))     // is n a power of two?
```

---

## III. XOR — THE MAGIC OPERATOR ⭐
- `a ^ a = 0`, `a ^ 0 = a`, XOR is associative & commutative.
- **Single Number (LC 136)**: XOR all → duplicates cancel, the unique survives.
- **Missing Number (LC 268)**: XOR indices and values.
- **Two unique numbers (LC 260)**: XOR all → split by a differing bit.
- **XOR of a range [0..n]**: closed form by n mod 4.

---

## IV. SUBSET ENUMERATION VIA BITMASKS
- Iterate all 2ⁿ subsets: `for (int mask = 0; mask < (1<<n); mask++)`.
- Iterate all submasks of a mask: `for (int s = mask; s; s = (s-1) & mask)` (total O(3ⁿ) over all masks).
- Powers **bitmask DP** (see [`../06-DYNAMIC-PROGRAMMING-UNIVERSE/12-Bitmask-DP.md`](../06-DYNAMIC-PROGRAMMING-UNIVERSE/12-Bitmask-DP.md)) and **SOS DP**.

---

## V. BITSET (O(n/64) speedup)
`std::bitset<N>` packs bits into machine words → set operations (AND/OR/XOR/count) run ~64× faster. Used to speed up DP (subset-sum), reachability (transitive closure), and string matching by a constant 64×.

---

## VI. COMMON APPLICATIONS
- **State compression** (small sets as integers) → bitmask DP
- **Fast set operations** (union/intersection via | and &)
- **Parity / counting** problems
- **XOR basis** (linear algebra over GF(2), max XOR subset) — see [`../09-MATHEMATICS-UNIVERSE/04-Linear-Algebra.md`](../09-MATHEMATICS-UNIVERSE/04-Linear-Algebra.md)
- **Binary trie** for max-XOR queries — see [`../08-STRING-UNIVERSE/13-Trie-Applications.md`](../08-STRING-UNIVERSE/13-Trie-Applications.md)
- **Gray code**, **subset sum via bitset**

---

## VII. GOTCHAS ⭐
- `1 << 31` overflows `int` (use `1LL << k` for ≥ 32-bit shifts).
- Shifting by ≥ width is **undefined behavior** in C/C++.
- Negative numbers + right shift: arithmetic vs logical — be careful.
- Operator precedence: `&`, `|`, `^` are LOWER than `==` — parenthesize! (`(n & 1) == 0`, not `n & 1 == 0`).

---

## VIII. PROBLEMS
- Single Number I/II/III (136, 137, 260)
- Number of 1 Bits (191), Counting Bits (338), Reverse Bits (190)
- Missing Number (268), Power of Two/Four (231, 342)
- Sum of Two Integers without + (371)
- Subsets via bitmask (78), Maximum XOR (421)
- Bitwise AND of Numbers Range (201), Gray Code (89)
- [CSES](https://cses.fi/problemset/) bit problems, CF tagged "bitmasks"

---

**→ Next:** Randomized, approximation, online & all advanced paradigms → [`COMPENDIUM-Advanced-Algorithms.md`](./COMPENDIUM-Advanced-Algorithms.md) · deeper: [`../11-ADVANCED-PARADIGMS-UNIVERSE/08-COMPENDIUM-Advanced.md`](../11-ADVANCED-PARADIGMS-UNIVERSE/08-COMPENDIUM-Advanced.md)
