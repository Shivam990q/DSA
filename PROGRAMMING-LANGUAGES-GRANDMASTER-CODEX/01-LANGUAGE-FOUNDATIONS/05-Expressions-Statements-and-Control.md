# 🔀 Expressions, Statements, and Control Flow

> *"An expression asks a question and gets an answer. A statement issues a command and changes the world."*

---

## I. THE FUNDAMENTAL DUALITY

- An **expression** *evaluates to a value*: `3 + 4`, `f(x)`, `a > b`, `[1,2,3]`.
- A **statement** *performs an action* (an effect): `x = 5`, `return`, `if (...) {...}`, `while (...) {...}`.

The litmus test: **can you put it on the right side of an assignment?** If yes, it's an expression.

```python
y = (3 + 4)        # ok: 3+4 is an expression
y = (while True: pass)   # error: a while loop is a statement, has no value
```

---

## II. EXPRESSION-ORIENTED vs STATEMENT-ORIENTED LANGUAGES

A deep design choice:

### Statement-oriented (C, Java, Python)
`if`, loops, and blocks are *statements* — they don't produce values. You need a separate ternary `?:` operator to get a value from a condition.
```java
int max = (a > b) ? a : b;   // ternary needed; 'if' has no value
```

### Expression-oriented (Rust, Haskell, Scala, Ruby, Kotlin)
Almost *everything* is an expression, including `if`, `match`, and blocks. They evaluate to values, so no separate ternary is needed.
```rust
let max = if a > b { a } else { b };   // 'if' IS an expression
let x = { let t = compute(); t * 2 };  // a block evaluates to its last expression
```

Expression-orientation is cleaner and composes better — fewer special cases, everything nests. It pairs naturally with functional style. This is why newer languages (Rust, Kotlin, Scala) lean expression-oriented.

---

## III. EVALUATION ORDER AND STRATEGY

*When* and *whether* sub-expressions get evaluated is a semantics decision with real consequences:

### Strict (eager) evaluation — the default almost everywhere
Arguments are evaluated *before* the call.
```python
f(g(), h())   # g() and h() both run before f is called
```

### Lazy (non-strict) evaluation — Haskell's signature
Expressions evaluate *only when their value is actually needed*.
```haskell
take 5 [1..]   -- [1..] is an INFINITE list, but laziness means
               -- only the first 5 are ever computed → [1,2,3,4,5]
```
Laziness enables infinite data structures and can avoid wasted work, but makes time/space behavior harder to predict (space leaks).

### Short-circuit evaluation — the pragmatic middle
`&&` and `||` evaluate the right side *only if needed*:
```javascript
if (user != null && user.isActive) { ... }
//  ↑ if user is null, user.isActive is never evaluated → no crash
```
This is *sequencing* baked into operators. Relying on it is idiomatic and safe.

### Argument evaluation order (a real footgun)
`f(a(), b())` — does `a()` or `b()` run first? Java says left-to-right; **C/C++ leave it unspecified**, so `f(i++, i++)` is a bug that behaves differently across compilers. Know your language's rule.

---

## IV. THE CONTROL-FLOW PRIMITIVES

All control flow is built from a small set of primitives:

| Primitive | Purpose | Forms |
|-----------|---------|-------|
| **Sequence** | do this, then that | `;`, newlines, blocks |
| **Selection** | choose a path | `if/else`, `switch`, `match`, guards |
| **Iteration** | repeat | `for`, `while`, `do-while`, comprehensions |
| **Recursion** | repeat via self-call | function calling itself |
| **Non-local jumps** | abrupt transfer | `return`, `break`, `continue`, `goto`, exceptions |

**Structured programming** (Dijkstra, "Go To Statement Considered Harmful", 1968) established that sequence + selection + iteration suffice for any program — `goto` is unnecessary and harmful. This is why modern languages restrict or ban `goto`.

---

## V. PATTERN MATCHING — SELECTION EVOLVED

Modern languages replace long `if/else` chains with **pattern matching** — selection that also *destructures*:

```rust
match shape {
    Circle { radius }        => 3.14 * radius * radius,
    Rectangle { w, h }       => w * h,
    Triangle { base, height} => 0.5 * base * height,
}
```

Pattern matching is checked for **exhaustiveness** by the compiler: if you forget a case, it won't compile. This turns a whole class of "forgot to handle that" runtime bugs into compile errors. It pairs with algebraic data types (see [`../03-TYPE-SYSTEMS/04-Advanced-Types.md`](../03-TYPE-SYSTEMS/04-Advanced-Types.md)).

---

## VI. RECURSION AND ITERATION ARE DUAL

Any loop can be written as recursion and vice versa:

```python
# iterative
def fact(n):
    r = 1
    for i in range(1, n+1): r *= i
    return r

# recursive
def fact(n):
    return 1 if n == 0 else n * fact(n-1)
```

- **Imperative languages** prefer loops (cheap, no stack growth).
- **Functional languages** prefer recursion (no mutation needed).

The catch: naive recursion grows the call stack → stack overflow for deep inputs. **Tail-call optimization (TCO)** fixes this: if the recursive call is the *last* thing a function does, the compiler reuses the stack frame, making recursion as cheap as a loop. Scheme, Haskell, and functional languages guarantee TCO; Java and Python deliberately do *not* (Python caps recursion ~1000 deep). Knowing whether your language has TCO tells you whether deep recursion is safe.

---

## 📌 Key Takeaways
- **Expressions** produce values; **statements** produce effects. Test: can it go on the RHS of `=`?
- **Expression-oriented** languages (Rust, Kotlin, Haskell) make `if`/`match`/blocks yield values — cleaner composition.
- Evaluation may be **strict** (default), **lazy** (Haskell), or **short-circuit** (`&&`/`||`); argument order can be unspecified (C).
- Control flow = sequence + selection + iteration + recursion + jumps; structured programming showed the first three suffice.
- **Pattern matching** adds exhaustiveness checking; **tail-call optimization** makes recursion as cheap as looping.

**Next:** [`../02-PARADIGMS/00-Index.md`](../02-PARADIGMS/00-Index.md)
