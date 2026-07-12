# 📖 Operational and Denotational Semantics

> *"A language spec that says 'the compiler decides' isn't a spec. Formal semantics pins meaning down mathematically."*

How do we define, *precisely and unambiguously*, what a program means? Three main approaches, two of which we detail here.

---

## I. WHY FORMAL SEMANTICS?

Natural-language specs are ambiguous ("evaluates the operands" — in which order?). Ambiguity causes:
- **Compiler disagreements** — the same program behaves differently on GCC vs Clang.
- **Security holes** — undefined behavior optimized unpredictably.
- **Impossibility of proof** — you can't prove a compiler correct against a vague spec.

**Formal semantics** gives meaning mathematically, enabling verified compilers (CompCert), sound type systems, and precise language standards. There are three classic styles: **operational**, **denotational**, and **axiomatic**.

---

## II. OPERATIONAL SEMANTICS — MEANING AS EXECUTION STEPS

Defines meaning by specifying **how a program executes** on an abstract machine, via inference rules. It's the most intuitive and closest to implementation. Two flavors:

### Small-step (structural) — one tiny step at a time
Describes single reduction steps: `e → e'` ("e steps to e'").
```
        e1 → e1'
   ─────────────────      (evaluate the left operand first)
   e1 + e2 → e1' + e2

   ──────────────────     (when both are values, add them)
   n1 + n2 → (n1 plus n2)
```
Reading top-to-bottom: "IF the premise (above the line) holds, THEN the conclusion (below) holds." Evaluating `(1+2)+3` proceeds: `(1+2)+3 → 3+3 → 6`, each `→` justified by a rule. Small-step captures the *whole trajectory* of execution — ideal for reasoning about concurrency and non-termination.

### Big-step (natural) — straight to the final result
Describes the final value: `e ⇓ v` ("e evaluates to v").
```
   e1 ⇓ n1    e2 ⇓ n2
   ──────────────────
   e1 + e2 ⇓ (n1 plus n2)
```
Big-step is more compact for defining interpreters (it *is*, essentially, a recursive interpreter written as rules) but hides intermediate steps and struggles with non-terminating programs.

**Operational semantics is what real language specs mostly use** — it directly guides implementers and is the basis for proving properties like type soundness ("well-typed programs don't get stuck").

---

## III. DENOTATIONAL SEMANTICS — MEANING AS MATHEMATICAL OBJECTS

Defines meaning by mapping each program to a **mathematical object** it *denotes* — typically a function from inputs to outputs. Notation: `⟦e⟧` = "the meaning of e."

```
⟦5⟧            = 5                         (the number 5)
⟦e1 + e2⟧      = ⟦e1⟧ + ⟦e2⟧               (meaning of a sum = sum of meanings)
⟦λx. e⟧        = a mathematical function
```

The key principle is **compositionality**: the meaning of a whole is built from the meanings of its parts. A program *is* a mathematical function; two programs are equivalent iff they denote the *same* function — a clean, implementation-independent notion of equivalence.

Denotational semantics is more abstract and powerful for **proofs and reasoning about equivalence**, but requires sophisticated math (domain theory, to handle recursion and non-termination via least fixed points). It's favored by theorists; operational is favored by implementers. They're two lenses on the same truth, and a language is well-defined when they *agree*.

---

## IV. AXIOMATIC SEMANTICS — MEANING AS WHAT YOU CAN PROVE

The third style defines meaning through **logical assertions about program state**, using **Hoare triples**:

```
{P} C {Q}
```
"If precondition **P** holds before executing command **C**, then postcondition **Q** holds after (if C terminates)." Example:
```
{x = 5}  x := x + 1  {x = 6}
```
Axiomatic semantics underpins **program verification** and tools like **Hoare logic** and **separation logic** (for reasoning about heap/pointers). It's less about "what a program computes" and more about "what properties we can *prove* it satisfies" — the foundation of formal verification, loop invariants, and tools like Dafny and Frama-C.

---

## V. HOW THEY RELATE AND WHY YOU CARE

| Style | Defines meaning as... | Best for | Used by |
|-------|----------------------|----------|---------|
| **Operational** | steps of execution | implementing, type soundness proofs | most language specs |
| **Denotational** | mathematical objects (functions) | equivalence, deep reasoning | theorists, domain theory |
| **Axiomatic** | provable pre/postconditions | verification, correctness proofs | formal methods, verifiers |

**Why an engineer should care:**
- **Undefined behavior** exists because C's semantics deliberately leaves gaps — knowing this is knowing where your dragons live.
- **Verified compilers** (CompCert, CakeML) are proven correct against formal semantics — no miscompilation bugs, ever.
- **Loop invariants and pre/postconditions** (axiomatic thinking) make you reason correctly about tricky code even without formal tools.
- When two compilers disagree, the answer is "what does the *spec's semantics* say?"

---

## 📌 Key Takeaways
- Formal semantics gives programs **precise mathematical meaning**, enabling verified compilers, sound types, and unambiguous specs.
- **Operational** semantics = execution steps (small-step: `e → e'`; big-step: `e ⇓ v`); intuitive, implementation-guiding, used by most specs.
- **Denotational** semantics = programs as mathematical objects (`⟦e⟧`), compositional; powerful for equivalence and proofs.
- **Axiomatic** semantics = Hoare triples `{P} C {Q}`; the basis of program verification and loop-invariant reasoning.
- Engineers benefit: understanding undefined behavior, verified compilers, and correctness reasoning.

**Next:** [`03-Type-Theory.md`](./03-Type-Theory.md)
