# 🔢 Generating Functions

> *"Turn a sequence into a function. Manipulate the function. Read off the sequence."*

---

## I. THE IDEA
An **ordinary generating function (OGF)** for a sequence (a₀, a₁, a₂, ...) is the formal power series:
```
A(x) = a₀ + a₁x + a₂x² + a₃x³ + ...
```
We manipulate A(x) algebraically; the coefficient of xⁿ recovers aₙ (written [xⁿ]A(x)).

---

## II. ESSENTIAL CLOSED FORMS
- 1/(1−x) = 1 + x + x² + x³ + ... (all 1s)
- 1/(1−x)² = Σ (n+1) xⁿ
- x/(1−x)² = Σ n xⁿ
- 1/(1−ax) = Σ aⁿ xⁿ
- (1+x)ⁿ = Σ C(n,k) xᵏ (binomial)
- 1/(1−x)^k = Σ C(n+k−1, k−1) xⁿ (stars and bars)
- eˣ = Σ xⁿ/n! (for **exponential** generating functions, EGF)

---

## III. SOLVING RECURRENCES WITH GFs
For aₙ = aₙ₋₁ + aₙ₋₂ (Fibonacci), a₀=0, a₁=1:
1. Multiply recurrence by xⁿ, sum over n.
2. Get A(x) = x / (1 − x − x²).
3. Partial fractions → closed form A(n) = (φⁿ − ψⁿ)/√5.

GFs systematically convert recurrences into closed forms.

---

## IV. COUNTING WITH GFs
GFs encode "choices" as polynomial factors:
- **Coin problem**: ways to make sum n with coins of denominations {1,2,5} = [xⁿ] in 1/((1−x)(1−x²)(1−x⁵)).
- **Bounded supplies**: factor (1 + x^v + x^(2v) + ... + x^(kv)) per item.
- **Partitions**: product over parts.

The **product of GFs = convolution of sequences** — and convolution is exactly what FFT/NTT computes fast (see [`05-FFT-NTT.md`](./05-FFT-NTT.md)).

---

## V. EXPONENTIAL GENERATING FUNCTIONS (EGF)
EGF: A(x) = Σ aₙ xⁿ/n!. Used for **labeled** structures (permutations, set partitions). Product of EGFs corresponds to combining labeled structures (exponential formula).

---

## VI. OPERATIONS DICTIONARY
| Sequence operation | GF operation |
|--------------------|--------------|
| Shift (aₙ → aₙ₋₁) | multiply by x |
| Partial sums | multiply by 1/(1−x) |
| Convolution (Σ aᵢbₙ₋ᵢ) | product A(x)·B(x) |
| aₙ → n·aₙ | x·A'(x) |

---

## VII. WHY IT MATTERS IN CP
- Derive closed forms / recurrences for counting problems
- Recognize that a counting answer = coefficient in a product → compute via FFT/NTT
- Linear recurrence + GF → matrix exponentiation or Kitamasa for the nth term

---

## VIII. PROBLEMS
- Coin change counting (LC 518) — implicitly a GF product
- Counting partitions / compositions
- Number of ways to form sums with constraints
- CF problems tagged "math" + "combinatorics" where the answer is a convolution
- [Project Euler](https://projecteuler.net) partition problems

---

## IX. NOTE
Generating functions are a Level 6-9 conceptual tool. You won't always compute with them explicitly, but recognizing "this count is a coefficient in a product" unlocks FFT-based solutions and elegant closed forms.

---

## X. RECOMMENDED READING
- **[generatingfunctionology](https://www2.math.upenn.edu/~wilf/gfology2.pdf)** by Herbert Wilf (free PDF) ⭐
- **Concrete Mathematics** (Knuth, Graham, Patashnik) — generating functions chapter

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | Full toolkit → [`11-COMPENDIUM-Math-Toolkit.md`](./11-COMPENDIUM-Math-Toolkit.md)
