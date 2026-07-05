# 🧿 Advanced Types — The Frontier

> *"Make illegal states unrepresentable. If the type can't express the bug, the bug can't exist."*

The frontier of type systems is about **encoding more of your program's correctness into types** — so the compiler proves properties you'd otherwise test for (or ship as bugs).

---

## I. ALGEBRAIC DATA TYPES (ADTs) — THE WORKHORSE

The most important idea in modern typed languages. Types built by combining others with **AND** and **OR**:

### Product types (AND) — "a struct has all of these"
```rust
struct Point { x: f64, y: f64 }   // a Point has an x AND a y
```
Called "product" because the number of possible values is the *product* of the fields' possibilities.

### Sum types (OR) — "a value is one of these" (a.k.a. tagged unions, enums)
```rust
enum Shape {
    Circle { radius: f64 },              // it's a Circle OR
    Rectangle { width: f64, height: f64 },  // a Rectangle OR
    Triangle { base: f64, height: f64 },    // a Triangle
}
```
Called "sum" because the possible values are the *sum* of the variants'. Sum types are what most mainstream languages historically *lacked* — and their absence forced people to fake it with nullable fields, type tags, and inheritance.

### The killer combination: sums + pattern matching + exhaustiveness
```rust
fn area(s: Shape) -> f64 {
    match s {
        Shape::Circle { radius } => 3.14159 * radius * radius,
        Shape::Rectangle { width, height } => width * height,
        Shape::Triangle { base, height } => 0.5 * base * height,
    }   // if you forget a variant, THIS DOESN'T COMPILE
}
```
Add a new `Shape` variant and the compiler flags *every* `match` that forgot to handle it. A whole class of "forgot that case" bugs becomes impossible.

---

## II. OPTION / RESULT — KILLING NULL AND EXCEPTIONS

The most valuable application of sum types: making **absence** and **failure** explicit in the type.

```rust
enum Option<T> { Some(T), None }          // a value that might be absent
enum Result<T, E> { Ok(T), Err(E) }       // a computation that might fail
```

Instead of `null` (which lurks in *every* reference type and crashes when dereferenced), a possibly-absent value has type `Option<T>` — and the compiler *forces* you to handle the `None` case before using the value:

```rust
match find_user(id) {
    Some(user) => greet(user),
    None => show_login(),        // you CANNOT forget this — it won't compile otherwise
}
```

This is how Rust, Haskell, Swift, and Kotlin *eliminate the null-pointer exception* — Tony Hoare's self-described "billion-dollar mistake." Absence and failure are no longer invisible landmines; they're visible in the type and enforced by the checker. Errors-as-values (`Result`) similarly make failure explicit without the hidden control flow of exceptions.

---

## III. GENERIC ADTs — COMPOSING THE IDEAS

ADTs + generics = expressive, safe data modeling:
```haskell
data Tree a = Leaf | Node (Tree a) a (Tree a)   -- a binary tree of any type 'a'
data Either a b = Left a | Right b               -- one of two types
data List a = Nil | Cons a (List a)              -- a linked list, from scratch
```
`Tree a` is a binary tree over any element type, defined in one line, with pattern matching and exhaustiveness for free. This is why functional languages express data structures so tersely and safely.

---

## IV. DEPENDENT TYPES — TYPES THAT DEPEND ON VALUES

The research frontier (Idris, Agda, Coq, Lean). Here **types can depend on values**, letting you encode arbitrarily precise properties:

```idris
-- A vector whose LENGTH is part of its type
append : Vect n a -> Vect m a -> Vect (n + m) a
--                                    ^^^^^ the result length is PROVEN to be n+m
```

With dependent types you can express "a sorted list," "a non-empty list," "a matrix multiplication where dimensions match," or "this function returns a prime number" — all checked at compile time. The type system becomes a full **proof assistant**; a well-typed program is a *machine-checked mathematical proof* of its own correctness (the Curry–Howard correspondence — see [`../08-SEMANTICS-AND-THEORY/03-Type-Theory.md`](../08-SEMANTICS-AND-THEORY/03-Type-Theory.md)).

The cost: writing proofs is hard, and full dependent typing hasn't reached the mainstream — yet. It powers verified software (CompCert, a formally-verified C compiler) and proof assistants that mathematicians now use to verify theorems.

---

## V. LINEAR AND AFFINE TYPES — TRACKING USAGE

Types that constrain *how many times* a value is used:
- **Linear types** — must be used *exactly once*.
- **Affine types** — used *at most once*.

Rust's **ownership** is essentially an affine type system: a value has one owner; moving it makes the source unusable. This lets the compiler prove memory safety (no use-after-free, no double-free) *without a garbage collector* — the core of Rust's achievement (see [`../04-MEMORY-AND-RUNTIME/03-Ownership-and-Borrowing.md`](../04-MEMORY-AND-RUNTIME/03-Ownership-and-Borrowing.md)). Linear types are also used to manage file handles, network sockets, and other resources that must be released exactly once.

---

## VI. GRADUAL TYPING — MIXING STATIC AND DYNAMIC

**Gradual typing** lets static and dynamic typing coexist in one program: annotate the parts you want checked, leave the rest dynamic, and migrate incrementally. This is exactly what **TypeScript** (over JavaScript) and **Python type hints + mypy** do.

```typescript
function add(a: number, b: number): number { return a + b; }  // statically checked
let data: any = fetchWhatever();   // 'any' opts out — dynamic here
```

Gradual typing is the pragmatic bridge that let millions of dynamic-language codebases gain static safety *without a rewrite* — a huge part of why TypeScript conquered frontend development.

---

## VII. OTHER FRONTIER FEATURES (briefly)
- **Refinement types** — a type plus a predicate: `{x: Int | x > 0}` (positive integers). (LiquidHaskell, F*.)
- **Higher-kinded types** — abstract over type constructors, not just types (`Functor f`). Enables writing code generic over `Option`, `List`, `Future` uniformly.
- **Phantom types** — type parameters used only for compile-time tagging (e.g., units: `Meters` vs `Feet`), never stored — preventing "mixed up the units" bugs at zero runtime cost.

---

## 📌 Key Takeaways
- **Algebraic data types** = products (AND/structs) + sums (OR/enums); with pattern matching + exhaustiveness they make "forgot a case" bugs impossible.
- **Option/Result** encode absence and failure in the type, killing null-pointer exceptions and hidden error flow.
- **Dependent types** let types depend on values → the type system becomes a proof assistant (Curry–Howard).
- **Linear/affine types** track usage; Rust's ownership is affine typing → memory safety without GC.
- **Gradual typing** (TypeScript, mypy) mixes static and dynamic, enabling incremental adoption.
- Overarching goal: **make illegal states unrepresentable.**

**Next:** [`../04-MEMORY-AND-RUNTIME/00-Index.md`](../04-MEMORY-AND-RUNTIME/00-Index.md)
