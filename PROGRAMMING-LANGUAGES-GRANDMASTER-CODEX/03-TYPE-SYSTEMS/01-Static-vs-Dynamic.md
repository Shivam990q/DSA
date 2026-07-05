# ⚖️ Static vs Dynamic Typing

> *"Static typing catches your typos at compile time. Dynamic typing catches them in production."* — the tribal joke that contains a real tradeoff

---

## I. TWO INDEPENDENT AXES (not one)

People say "typed vs untyped" as if it's one dimension. It's **two**:

### Axis 1: WHEN are types checked?
- **Static typing** — at **compile time**, before the program runs. The compiler knows every variable's type. (Rust, Java, Haskell, Go, C, TypeScript.)
- **Dynamic typing** — at **run time**, as values flow. Variables hold any type; the check happens when an operation executes. (Python, Ruby, JavaScript, Lisp.)

### Axis 2: HOW strictly are types enforced?
- **Strong typing** — no silent, surprising coercions. You can't secretly add a string to a number without an explicit conversion.
- **Weak typing** — implicit coercions happen freely, sometimes bizarrely.

These are **orthogonal**. The four corners:

| | Strong | Weak |
|---|--------|------|
| **Static** | Rust, Haskell, Java | C, C++ (implicit conversions) |
| **Dynamic** | Python, Ruby | JavaScript, PHP, Perl |

**Python is strongly, dynamically typed** — `"1" + 2` raises a `TypeError` (strong: no silent coercion) but only *at runtime* (dynamic). **JavaScript is weakly, dynamically typed** — `"1" + 2` silently gives `"12"` (weak coercion) at runtime. This distinction resolves endless confusion.

---

## II. THE WEAK-TYPING HALL OF SHAME

Weak typing's implicit coercions produce genuinely surprising results:

```javascript
// JavaScript
[] + []        // ""      (arrays coerced to empty strings)
[] + {}        // "[object Object]"
"5" - 1        // 4       (- coerces to number)
"5" + 1        // "51"    (+ prefers string concat)
true + true    // 2       (booleans → numbers)
0 == "0"       // true    (coercion), but 0 === "0" is false (no coercion)
```

These aren't bugs in JS — they're the *defined* behavior of weak coercion. But they cause real defects, which is why TypeScript (static + stronger) and `===` (strict equality) exist as guardrails.

---

## III. THE CASE FOR STATIC TYPING

1. **Bugs caught before running.** Type errors, typos in field names, wrong argument counts, forgotten cases — caught at compile time, not by a user.
2. **Documentation that can't lie.** `fn transfer(from: Account, to: Account, amount: Money)` tells you everything, and the compiler *enforces* it stays true.
3. **Fearless refactoring.** Rename a field, change a signature — the compiler lists every place that breaks. Refactoring a large dynamically-typed codebase is terrifying by comparison.
4. **Superb tooling.** Autocomplete, go-to-definition, and inline errors all rely on the compiler knowing types.
5. **Performance.** Known types let the compiler generate efficient machine code (no runtime type tags to check).

## IV. THE CASE FOR DYNAMIC TYPING

1. **Speed of writing.** No type annotations, no fighting the checker; prototype fast.
2. **Flexibility.** Duck typing ("if it walks like a duck...") — a function works with anything that has the right methods, no declared interface needed.
3. **Metaprogramming.** Easy to build objects, add methods, and handle data whose shape you don't know until runtime (JSON, plugins).
4. **Gentle learning curve.** Beginners aren't blocked by type errors while learning logic.

---

## V. WHY THE INDUSTRY IS DRIFTING TOWARD STATIC

The last decade's clear trend: **add static types to dynamic languages.**
- **TypeScript** wraps JavaScript — now dominant in serious frontend work.
- **Python type hints** (`def f(x: int) -> str`) + **mypy**/**pyright** — increasingly standard in large codebases.
- **Ruby's Sorbet**, **PHP's type declarations** — same story.

Why? Because at **scale** (big codebases, big teams, long lifespans), the cost of runtime type bugs and un-refactorable code dwarfs the cost of writing annotations. Dynamic typing wins for scripts and prototypes; static typing wins for systems that must live and grow. The tooling improvements (inference — see file 02) also erased much of static typing's verbosity tax.

---

## VI. TYPE SOUNDNESS — THE PROMISE (AND WHEN IT BREAKS)

A type system is **sound** if "well-typed programs cannot go wrong" — a program that type-checks *cannot* exhibit the type errors the system rules out. Haskell and Rust have (largely) sound type systems.

But soundness has escape hatches and holes in real languages:
- **Java's `null`** — `String s` can be `null`, and `s.length()` compiles but crashes. Null defeats the type system (the "billion-dollar mistake").
- **TypeScript's `any`** — an explicit "turn off checking here" that punches a hole in soundness for pragmatism.
- **Type casts** — `(Dog) animal` tells the compiler "trust me," moving the check to runtime.

Knowing where your language's type system is *unsound* tells you exactly where runtime type bugs can still hide. Modern languages fight this: Rust and Kotlin encode nullability *in the type* (`Option<T>`, `String?`), making "might be absent" a compile-time concern.

---

## 📌 Key Takeaways
- Two axes: **static/dynamic** (when checked) and **strong/weak** (how strictly). They're independent.
- Python = strong + dynamic; JavaScript = weak + dynamic; Rust/Haskell = strong + static.
- Static: bugs caught early, honest docs, fearless refactoring, better tooling, speed. Dynamic: fast to write, flexible, metaprogramming-friendly.
- The industry is adding static types to dynamic languages (TypeScript, Python hints) — static wins at scale.
- **Soundness** = well-typed programs can't go wrong; `null`, `any`, and casts are the holes to watch.

**Next:** [`02-Type-Inference.md`](./02-Type-Inference.md)
