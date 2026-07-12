# λ Lambda Calculus — The Essence of Computation

> *"Everything is a function. Functions take functions and return functions. From this alone, all of computation arises."*

---

## I. WHAT IT IS

The **lambda calculus** (Alonzo Church, 1930s) is the smallest possible programming language — and a complete model of computation. It has just **three** things:

```
1. Variables:      x
2. Abstraction:    λx. e        (a function of x with body e)
3. Application:    e1 e2        (apply function e1 to argument e2)
```

That's the *entire* language. No numbers, no booleans, no loops, no data structures — yet it's **Turing complete** (equivalent in power to a Turing machine, by the Church–Turing thesis). It proves that *functions alone are enough to express any computation.*

`λx. x` is the identity function ("take x, return x"). `λx. λy. x` takes two arguments and returns the first. Application `(λx. x) a` reduces to `a`.

---

## II. THE ONE COMPUTATION RULE: BETA REDUCTION

Computation in lambda calculus is **substitution**, called **beta reduction**: to apply a function to an argument, substitute the argument for the parameter in the body.

```
(λx. x + x) 5   →   5 + 5   →   10
   ^ substitute 5 for x in the body

(λx. λy. x) a b →   (λy. a) b   →   a
   ^ apply to a: substitute a for x        ^ apply to b: y unused, result is a
```

That single rule — substitute and simplify — *is* the whole evaluation mechanism. Running a lambda program means beta-reducing until you can't anymore (reaching "normal form"). This is the mathematical heart of what happens when a functional program executes.

---

## III. ENCODING EVERYTHING FROM NOTHING

The astonishing part: with only functions, you can build *all* the data and control you need.

### Booleans (Church encoding)
```
TRUE  = λx. λy. x      (pick the first)
FALSE = λx. λy. y      (pick the second)
IF    = λb. λt. λf. b t f   (a boolean IS its own if-then-else)
```
`IF TRUE a b` → `TRUE a b` → `a`. The boolean *chooses*.

### Numbers (Church numerals)
Represent `n` as "apply a function n times":
```
0 = λf. λx. x           (apply f zero times)
1 = λf. λx. f x         (once)
2 = λf. λx. f (f x)     (twice)
```
Arithmetic (successor, addition, multiplication) becomes function composition. Numbers *are* functions.

### Recursion (the Y combinator)
Even *recursion without names* is expressible via fixed-point combinators like the famous **Y combinator**:
```
Y = λf. (λx. f (x x)) (λx. f (x x))
```
`Y g` produces a fixed point of `g`, letting a function call "itself" without being named. This is deep magic — recursion emerging from pure substitution.

The lesson: functions are a *universal* substrate. Data, logic, and looping are all just functions in disguise.

---

## IV. WHY IT UNDERPINS REAL LANGUAGES

Lambda calculus isn't a curiosity — it's the theoretical core of functional programming:
- **Every functional language** (Haskell, Lisp, ML, and the functional subset of JS/Python) is essentially lambda calculus plus conveniences.
- **Closures** (see [`../01-LANGUAGE-FOUNDATIONS/04-Values-Bindings-and-Scope.md`](../01-LANGUAGE-FOUNDATIONS/04-Values-Bindings-and-Scope.md)) are lambda abstractions that capture their environment — the direct realization of `λ` in a real runtime.
- **First-class functions**, `map`/`filter`/`reduce`, currying — all come straight from this model.
- The name `lambda` (Python's `lambda`, JS arrow functions, `λ` in many languages) is a direct homage.

When you write `x => x * 2`, you are writing lambda calculus. Church's 1930s abstraction is running in your browser right now.

---

## V. TYPED LAMBDA CALCULUS — THE BRIDGE TO TYPES

Pure (untyped) lambda calculus allows nonsense like `x x` (applying something to itself) and non-terminating terms. Adding **types** (the *simply typed lambda calculus*) restricts terms to well-behaved ones and opens the door to the entire theory of type systems — and to the Curry–Howard correspondence (see [`03-Type-Theory.md`](./03-Type-Theory.md)), where typed lambda terms correspond exactly to logical proofs. The typed lambda calculus is the seed from which System F (parametric polymorphism), dependent types, and modern type theory all grow.

---

## VI. VARIANTS AND LEGACY

- **Untyped lambda calculus** — the original; models dynamically-typed functional computation.
- **Simply typed lambda calculus** — adds basic types; strongly normalizing (always terminates).
- **System F** — adds parametric polymorphism (generics); the theory behind Haskell/ML type systems.
- **Calculus of constructions** — dependent types; the basis of Coq and Lean (proof assistants).

From three symbols and one rule came functional programming, closures, type theory, and machine-checked mathematics. Lambda calculus is the "e = mc²" of computing — tiny, and world-altering.

---

## 📌 Key Takeaways
- Lambda calculus (Church, 1930s) is a **complete model of computation** with only variables, function abstraction (`λ`), and application.
- Its single rule, **beta reduction** (substitution), *is* evaluation.
- Booleans, numbers, and even **recursion** (Y combinator) can be built from functions alone — functions are a universal substrate.
- It's the theoretical core of **every functional language**; closures and arrow functions are lambda calculus made real.
- **Typed** lambda calculus seeds the entire theory of type systems and the Curry–Howard correspondence.

**Next:** [`02-Operational-and-Denotational-Semantics.md`](./02-Operational-and-Denotational-Semantics.md)
