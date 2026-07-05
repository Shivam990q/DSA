# 🔎 Type Inference

> *"The best of both worlds: the safety of static types with the brevity of dynamic ones — the compiler figures out the types you didn't write."*

---

## I. THE IDEA

**Type inference** lets you omit type annotations while the compiler *deduces* them from context. You get full static checking without the verbosity.

```rust
let x = 5;              // compiler infers x: i32
let name = "Ada";       // infers name: &str
let nums = vec![1,2,3]; // infers nums: Vec<i32>
let doubled = nums.iter().map(|n| n * 2).collect::<Vec<_>>();  // inferred throughout
```

Compare the bad old days of explicit everything:
```java
// Java before 'var' (pre-10)
HashMap<String, List<Integer>> map = new HashMap<String, List<Integer>>();
// Java 10+ with inference
var map = new HashMap<String, List<Integer>>();
```

Inference is why modern statically-typed languages (Rust, Kotlin, Swift, Scala, Haskell, modern Java/C++) feel almost as light as Python while retaining full compile-time safety.

---

## II. LOCAL vs GLOBAL INFERENCE

- **Local inference** (Java `var`, C++ `auto`, C# `var`) — infers within a single statement/expression, usually from the right-hand side. Function signatures still need annotations. Simple, predictable.
- **Global / whole-program inference** (Haskell, ML, OCaml) — can infer the types of *entire functions* with no annotations at all, using the famous **Hindley–Milner** algorithm.

```haskell
-- No annotations anywhere. Haskell infers:  add :: Num a => a -> a -> a
add x y = x + y
```

Most mainstream languages deliberately choose *local* inference and require annotations on function boundaries — because full-program inference can produce confusing errors and slow compiles, and because signatures serve as documentation.

---

## III. HINDLEY–MILNER — HOW GLOBAL INFERENCE WORKS

The classic algorithm (Algorithm W) behind ML and Haskell. Conceptually three steps:

1. **Assign type variables.** Every unknown gets a placeholder: `x : a`, `y : b`, result `: c`.
2. **Generate constraints.** Each use of the value imposes equations. `x + y` (with numeric `+`) forces `a = b` and both numeric; the result forces `c = a`.
3. **Unify.** Solve the constraint equations, substituting until every variable is pinned down or shown to be genuinely general.

```
add x y = x + y
  x : a, y : b, (+) : Num t => t -> t -> t
  constraints: a = t, b = t, result = t
  solution: a = b = result = t, with Num t
  ⇒ add :: Num a => a -> a -> a     (works for any numeric type)
```

The magic: it finds the **most general type** (principal type) that works — automatically producing generic code. This is *parametric polymorphism for free* (see file 03).

---

## IV. WHERE INFERENCE STOPS (and you must annotate)

Inference isn't omniscient. You still annotate when:
- **Function signatures** (in most languages) — for documentation and to localize errors.
- **Ambiguity** — `let x = "42".parse()` in Rust: parse into *what*? You must say `let x: i32 = ...`.
- **Empty collections** — `let v = Vec::new();` — of what element type? Annotate or let later use pin it.
- **Recursion and complex generics** — inference may need a hint to converge.
- **Overloaded literals** — is `1` an `i32`, `f64`, or `u8`? Context or annotation decides.

A good rule: **annotate public/function boundaries; let inference handle the local plumbing.** Signatures are contracts and docs; internals are noise best inferred.

---

## V. THE TRADEOFFS

**Benefits:** less boilerplate, DRY (types not repeated), easier refactoring (change a type in one place), keeps code readable.

**Costs:**
- **Worse error messages** — an error's *cause* and its *reported location* can be far apart, because the checker only discovers the conflict late in unification. Haskell's "cannot match `a` with `b`" errors are infamous.
- **Reduced local readability** — `let x = foo()` hides `x`'s type; you rely on the editor to show it.
- **Slower compiles** for whole-program inference.

The modern sweet spot — local inference + mandatory signatures — deliberately captures most of the benefit while avoiding most of the cost.

---

## 📌 Key Takeaways
- Type inference deduces types you didn't write: static safety with dynamic-like brevity.
- **Local** inference (Java `var`, C++ `auto`) works per-statement; **global** inference (Haskell/ML via **Hindley–Milner**) can type whole functions with no annotations.
- HM works by assigning type variables, generating constraints, and **unifying** to the most general type.
- Annotate function boundaries and ambiguous cases; let inference handle local plumbing.
- Cost of powerful inference: confusing errors and lower local readability.

**Next:** [`03-Polymorphism-and-Generics.md`](./03-Polymorphism-and-Generics.md)
