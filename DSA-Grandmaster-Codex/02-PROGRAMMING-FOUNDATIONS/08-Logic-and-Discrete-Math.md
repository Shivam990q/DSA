# 🧮 Logic & Discrete Math — The Crystalline Foundations

> *"All algorithms reduce to logic and counting. Master these and you master computation."*

---

## I. PROPOSITIONAL LOGIC

A **proposition** is a statement that is true or false.

### Connectives
- **AND** (∧): true iff both true
- **OR** (∨): true iff at least one true
- **NOT** (¬): inverts truth
- **IMPLIES** (→): false only when premise true and conclusion false
- **IFF** (↔): true iff both same truth value

### Truth tables
```
p | q | p∧q | p∨q | p→q | p↔q
T | T |  T  |  T  |  T  |  T
T | F |  F  |  T  |  F  |  F
F | T |  F  |  T  |  T  |  F
F | F |  F  |  F  |  T  |  T
```

### Key equivalences
- De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q
- Contrapositive: p → q ≡ ¬q → ¬p
- Implication: p → q ≡ ¬p ∨ q

---

## II. PREDICATE LOGIC

**Quantifiers**:
- ∀x P(x) — for all x, P(x) holds
- ∃x P(x) — there exists x such that P(x)

**Negation**:
- ¬∀x P(x) ≡ ∃x ¬P(x)
- ¬∃x P(x) ≡ ∀x ¬P(x)

**Order matters**:
- ∀x ∃y (y > x) — true on integers (y = x+1)
- ∃y ∀x (y > x) — false (no max integer)

---

## III. SETS

A **set** is an unordered collection of distinct elements.

- Notation: {1, 2, 3}, ∅ (empty)
- Operations: ∪ (union), ∩ (intersection), \ (difference), Δ (symmetric difference)
- Cardinality: |A|
- Power set: 2^A = {all subsets} — has 2^|A| elements

### Inclusion-Exclusion
|A ∪ B| = |A| + |B| − |A ∩ B|

### Cartesian product
A × B = {(a, b) : a ∈ A, b ∈ B}

---

## IV. RELATIONS

A **relation** R from A to B: a subset of A × B.

### Properties (relations on a set)
- **Reflexive**: ∀x: xRx
- **Symmetric**: ∀x,y: xRy → yRx
- **Antisymmetric**: ∀x,y: xRy ∧ yRx → x = y
- **Transitive**: ∀x,y,z: xRy ∧ yRz → xRz

### Equivalence relation = reflexive + symmetric + transitive
Partitions a set into equivalence classes.

### Partial order = reflexive + antisymmetric + transitive
Examples: ≤ on integers, ⊆ on sets

### Total order
Partial order + every two elements comparable.

---

## V. FUNCTIONS

A **function** f: A → B assigns each a ∈ A to one b ∈ B.

- **Injective** (1-1): different a's map to different b's
- **Surjective** (onto): every b is hit
- **Bijective**: both — has an inverse

|A| ≤ |B| iff there's an injection A → B.
|A| = |B| (finite) iff there's a bijection A → B.

---

## VI. INFINITE SETS (cardinality)

- ℕ (naturals), ℤ (integers), ℚ (rationals): all "**countably infinite**" (ℵ₀, same cardinality)
- ℝ (reals): "uncountable" (ℵ₁ or 2^ℵ₀)
- |ℝ| > |ℕ| (Cantor's diagonal argument)

This matters for theory of computation (the set of programs is countable, the set of functions is uncountable → some functions are uncomputable).

---

## VII. GRAPHS

A graph G = (V, E):
- V: vertices (nodes)
- E ⊆ V × V: edges (pairs)

### Types
- **Undirected**: edges are unordered pairs
- **Directed**: edges are ordered (source, target)
- **Weighted**: edges have weights
- **Simple**: no self-loops, no multi-edges
- **Multigraph**: multiple edges between same pair allowed

### Properties
- **Path**: sequence of vertices, consecutive ones connected
- **Cycle**: path that returns to start
- **Connected**: any two vertices have a path
- **Tree**: connected + acyclic; n nodes, n-1 edges
- **DAG**: directed acyclic graph

### Degree
- In undirected: degree(v) = number of edges touching v
- Sum of degrees = 2|E| (handshake lemma)

---

## VIII. TREES — THE FUNDAMENTAL STRUCTURE

A **tree** is a connected, acyclic graph.

### Equivalent characterizations (any one implies others, given n ≥ 1)
1. Connected and has n-1 edges
2. Connected and removing any edge disconnects it
3. Acyclic and adding any edge creates a cycle
4. Unique path between every pair of vertices

### Rooted tree
Pick one vertex as root. All edges directed away from root. Now we have parent/child/leaf concepts.

---

## IX. RECURRENCES

A **recurrence** defines a sequence in terms of earlier terms.

> Examples:
> - Fibonacci: F(n) = F(n-1) + F(n-2), F(0)=0, F(1)=1
> - Tower of Hanoi: T(n) = 2T(n-1) + 1, T(1) = 1

**Solving linear homogeneous recurrences with constant coefficients**:
- Find characteristic polynomial
- Find roots
- General solution = linear combination of `roots^n`
- Use initial conditions to fix constants

> Fibonacci characteristic: x² = x + 1 → x = (1±√5)/2
> Closed form: F(n) = (φⁿ − ψⁿ)/√5

---

## X. COMBINATORICS — COUNTING

### Sum rule
If task A can be done a ways, and task B can be done b ways, and they're disjoint: a + b ways for "A or B."

### Product rule
If task A: a ways, task B: b ways, independently: a × b ways for "A and B."

### Permutations
- n! arrangements of n distinct items
- nPr = n!/(n-r)! ordered arrangements of r items from n

### Combinations
- nCr = n!/(r!(n-r)!) unordered selections of r items from n

### With repetition
- Multisets of size r from n types: (n+r-1)Cr (stars and bars)
- Strings of length r over alphabet of size n: nʳ

### Bijection method
To count A, find a bijection A → B where |B| is known.

---

## XI. THE 12 EXERCISES

1. Prove De Morgan's laws via truth table.
2. Show that ∀x ∃y P(x,y) does not imply ∃y ∀x P(x,y).
3. Prove |power set of A| = 2^|A| by induction.
4. Show that the set of finite binary strings is countable.
5. Show that the set of all functions ℕ → {0,1} is uncountable (Cantor).
6. Define an equivalence relation on ℤ; describe its classes.
7. Count the number of distinct anagrams of "MISSISSIPPI."
8. How many ways to climb n stairs with steps {1, 2, 3}? Set up recurrence.
9. Prove the handshake lemma: in any graph, sum of degrees is even.
10. Show that every tree with ≥ 2 vertices has at least 2 leaves.
11. Solve recurrence T(n) = 2T(n-1) + 1, T(0)=0.
12. How many functions f: {1..n} → {1..k}? How many injective? How many surjective?

---

## XII. RECOMMENDED READING

- **Discrete Mathematics and Its Applications** (Rosen) — exhaustive textbook
- **Concrete Mathematics** (Knuth) — beautiful, deeper
- **A First Course in Logic** (Hedman)
- **Book of Proof** (Hammack) — free online, gentle introduction

---

**→ Next:** [`09-Abstraction-and-Decomposition.md`](./09-Abstraction-and-Decomposition.md)
