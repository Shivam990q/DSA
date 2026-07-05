# λ Functional Programming

> *"A program is a composition of pure functions. Data goes in, data comes out, and nothing is disturbed in between."*

---

## I. THE CORE IDEA

**Functional programming (FP)** treats computation as the **evaluation of mathematical functions** and avoids changing state and mutable data. A function, in the mathematical sense, maps inputs to outputs — nothing more. Given the same input, it *always* returns the same output and *changes nothing else in the world*.

```haskell
double x = x * 2          -- a pure function: same input → same output, no effects
result = map double [1,2,3]   -- [2,4,6]; the original list is untouched
```

Instead of *commanding* the machine step by step (imperative), you *describe* the result as a transformation of data through functions.

---

## II. PURITY AND SIDE EFFECTS

A **pure function**:
1. **Deterministic** — same inputs always give the same output.
2. **No side effects** — doesn't mutate external state, do I/O, or depend on anything but its arguments.

```python
# PURE
def add(a, b): return a + b

# IMPURE — depends on and changes external state
total = 0
def add_to_total(x):
    global total
    total += x          # side effect: mutates 'total'
    return total
```

Purity is the source of FP's benefits:
- **Referential transparency** — you can replace any call with its result without changing behavior. This makes code trivially easy to reason about, test, and cache (memoize).
- **Fearless concurrency** — pure functions can't race, because they share no mutable state.
- **Composability** — pure functions snap together like Lego.

Of course, a program that does *nothing* to the world is useless — you need I/O eventually. FP languages **push effects to the edges** and keep the core pure. Haskell famously isolates effects in the *IO monad*, making "this function touches the outside world" visible in its type.

---

## III. FIRST-CLASS AND HIGHER-ORDER FUNCTIONS

In FP, functions are **first-class values** — you can store them in variables, pass them as arguments, and return them from other functions, just like numbers.

A **higher-order function** takes or returns functions. The famous trio:
```python
map(f, xs)       # apply f to every element:  [f(x) for x in xs]
filter(p, xs)    # keep elements where p is true
reduce(g, xs)    # fold the list into one value (sum, product, max...)
```
These three replace most hand-written loops with declarative transformations. `sum = reduce(add, nums, 0)` says *what* you want (fold with addition) without an index, a bounds check, or an off-by-one bug.

---

## IV. IMMUTABILITY

FP data is **immutable** — you never modify a value; you create a *new* value.

```clojure
(def a [1 2 3])
(def b (conj a 4))   ; b is [1 2 3 4]; a is STILL [1 2 3]
```

This sounds wasteful, but FP languages use **persistent data structures** that share unchanged parts structurally, so "copying" a big map to change one key is O(log n), not O(n). Immutability eliminates whole bug categories (aliasing surprises, data races) and makes time-travel debugging and undo trivial.

---

## V. THE FP TOOLKIT (concepts that recur)

- **Recursion over loops** — no mutable loop counter, so iteration is recursion (with tail-call optimization to stay cheap).
- **Pattern matching** — destructure data by shape (see [`../03-TYPE-SYSTEMS/04-Advanced-Types.md`](../03-TYPE-SYSTEMS/04-Advanced-Types.md)).
- **Currying & partial application** — `add(3)(4)`: a function of many args becomes a chain of one-arg functions, enabling reuse.
- **Function composition** — `(f ∘ g)(x) = f(g(x))`: build big transformations from small ones.
- **Algebraic data types** — model data as "sums and products" (`Option`, `Result`, `Either`).
- **Monads** — a structured way to sequence computations *with context* (effects, optionality, async). Famously "hard to explain," but operationally: a monad is a type with `flatMap`/`bind` that lets you chain operations while threading context. `Promise.then` in JS is a monad in disguise.

---

## VI. FP HAS QUIETLY WON (in every language)

You don't need Haskell to program functionally. FP ideas have flooded mainstream languages:
- **JavaScript/Python** — `map`/`filter`/`reduce`, arrow functions, immutability libraries.
- **Java 8+** — lambdas, `Stream` API, `Optional`.
- **Rust** — iterators, `Option`/`Result`, pattern matching, immutability by default.
- **React** — pure components, immutable state, "UI = f(state)" is a functional idea.

The pragmatic modern style: **write pure functions by default, isolate side effects, prefer immutability, and use `map`/`filter`/`reduce` over manual loops** — regardless of your language.

---

## VII. STRENGTHS, WEAKNESSES, WHEN TO USE

**Strengths:** data-transformation pipelines, concurrency (no shared mutable state), correctness-critical code (easy to reason about and test), and anything where "input → output" is the natural shape.

**Weaknesses:** can be slower/allocation-heavy (immutability); some algorithms are naturally stateful and awkward in pure FP; the learning curve for monads and category-theory vocabulary; interfacing with an inherently effectful world needs discipline.

**When to reach for it:** data processing, business logic, anything concurrent, and the *core* of almost any system (keep it pure, push effects to the edges).

---

## 📌 Key Takeaways
- FP = computation as evaluation of **pure functions**; avoid mutation and side effects.
- **Purity** gives referential transparency, fearless concurrency, and composability; push effects to the edges.
- Functions are **first-class**; **higher-order** functions (`map`/`filter`/`reduce`) replace loops.
- **Immutability** + persistent data structures eliminate aliasing and race bugs cheaply.
- FP ideas have won everywhere — use them in any language: pure by default, effects at the edges.

**Next:** [`04-Logic-and-Declarative.md`](./04-Logic-and-Declarative.md)
