# 🔺 Type Theory — Programs as Proofs

> *"A type is a proposition. A program of that type is a proof of the proposition. This is not an analogy — it is an identity."*

---

## I. WHAT TYPE THEORY IS

**Type theory** is the mathematical study of type systems — and an alternative foundation for *all* of mathematics (rivaling set theory). It began with Bertrand Russell (to fix paradoxes in logic) and grew, through Church's typed lambda calculus and Per Martin-Löf's work, into the foundation of modern programming-language theory and proof assistants. It answers: what *is* a type, formally, and what can types guarantee?

---

## II. THE CURRY–HOWARD CORRESPONDENCE — THE GREAT IDEA

Independently discovered by Haskell Curry and William Howard, this is one of the most profound insights in all of science:

> **Types are propositions. Programs are proofs. Type-checking is proof-checking.**

The correspondence is exact:

| Logic | Programming |
|-------|-------------|
| proposition | type |
| proof of a proposition | program (term) of that type |
| implication `A → B` | function type `A → B` |
| conjunction `A ∧ B` | product type (pair/struct) `(A, B)` |
| disjunction `A ∨ B` | sum type (enum) `Either A B` |
| true | the unit type `()` |
| false | the empty type (no values) |
| proof normalization | program evaluation |

**Concretely:** a function `f : A → B` is *literally a proof* that "if you give me evidence of A, I can produce evidence of B" — i.e., a proof that A implies B. Writing a well-typed program *is* constructing a proof. Running it *is* simplifying the proof.

```
A function of type   (A → B) → (B → C) → (A → C)
is a PROOF of the logical statement:
   (A implies B) and (B implies C) implies (A implies C)   [transitivity!]
```
That function *is* function composition. Composition is the proof of transitivity of implication. Programs and proofs are the same thing.

---

## III. WHY THIS ISN'T JUST Beautiful — IT'S POWERFUL

If types are propositions and programs are proofs, then a **sufficiently powerful type system is a proof assistant**, and a well-typed program is a **machine-checked proof of its own correctness.**

- **Dependent types** (types that depend on values — see [`../03-TYPE-SYSTEMS/04-Advanced-Types.md`](../03-TYPE-SYSTEMS/04-Advanced-Types.md)) can express *arbitrary* propositions: "this list is sorted," "this function returns a prime," "these matrix dimensions match." Providing a program of that type *proves* the property.
- **Proof assistants** — Coq, Lean, Agda, Idris — exploit exactly this. Mathematicians now use them to verify theorems (the Four Color Theorem, the Kepler conjecture were formally verified). Engineers use them to build **provably correct software**: CompCert (a verified C compiler with no miscompilation bugs), seL4 (a formally verified OS kernel).
- **Lean** is now used by working mathematicians (e.g., Terence Tao) to formalize cutting-edge mathematics with machine-checked certainty.

The dream: software whose correctness is *proven*, not merely tested. Type theory is the road there.

---

## IV. THE HIERARCHY OF TYPE-THEORETIC POWER

```
Simply typed λ-calculus   → basic types; provably terminating
        │  add polymorphism
System F                  → generics/parametric polymorphism (Haskell/ML core)
        │  add type operators
System Fω                 → higher-kinded types (Functor, Monad)
        │  add types depending on values
Dependent type theory     → full proofs; Coq, Agda, Idris, Lean
```

This "lambda cube" (Barendregt) organizes type systems by which forms of abstraction they allow. Real languages sit at various points: Java/Go near the bottom, Haskell high up (System Fω-ish), Idris/Agda/Lean at the dependent-type summit.

---

## V. "PROPOSITIONS AS TYPES" IN EVERYDAY CODE

You benefit from Curry–Howard even without proof assistants:
- **"Make illegal states unrepresentable"** is Curry–Howard thinking: encode a property in the type so the *only* way to construct a value is to satisfy the property. A `NonEmptyList` type is a *proof* the list is non-empty — no runtime check needed.
- **`Option`/`Result`** force you to "prove" you've handled absence/failure before proceeding.
- **The typestate pattern** — encode a protocol (e.g., "file must be opened before read") in types so misuse won't compile.
- Every time the compiler rejects your code, it's saying *"your proof is incomplete."* Reframing type errors as "failed proofs" makes them feel less like nagging and more like a collaborator catching a genuine gap in your reasoning.

---

## VI. THE HORIZON

Type theory is where programming languages, logic, and mathematics converge. Its trajectory:
- **Gradual/refinement types** bringing lightweight proofs to mainstream languages (LiquidHaskell, F*, TypeScript's ever-richer types).
- **Dependent types** slowly becoming practical (Idris, Lean 4 as a general-purpose language).
- **Verified systems software** (compilers, kernels, cryptography) proven correct via these foundations.
- **AI + proof assistants** — automated theorem proving accelerating with machine learning.

The endpoint is a world where "it compiles" can mean "it is *proven* correct." Type theory is the mathematics making that possible.

---

## 📌 Key Takeaways
- **Type theory** studies type systems and serves as a foundation of mathematics itself.
- The **Curry–Howard correspondence** is an *identity*: types = propositions, programs = proofs, type-checking = proof-checking.
- Function composition is the proof of transitivity; every well-typed program is a proof of something.
- Powerful (dependent) type systems become **proof assistants** — Coq, Agda, Lean, Idris — enabling provably correct software (CompCert, seL4) and verified mathematics.
- You use Curry–Howard daily via "make illegal states unrepresentable," `Option`/`Result`, and typestate — a type error is a *failed proof*.

**Next:** [`../09-METAPROGRAMMING/00-Index.md`](../09-METAPROGRAMMING/00-Index.md)
