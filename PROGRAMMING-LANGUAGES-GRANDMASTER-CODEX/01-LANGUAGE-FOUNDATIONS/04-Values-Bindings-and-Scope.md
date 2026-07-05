# 🏷️ Values, Bindings, and Scope

> *"A variable is not a box. It is a binding — a temporary marriage between a name and a value."*

---

## I. VALUES vs VARIABLES vs BINDINGS

Three distinct ideas beginners blur:

- A **value** is a piece of data that exists: `42`, `"hi"`, `[1,2,3]`, a function.
- A **name** (identifier) is a symbol in source text: `x`, `count`, `add`.
- A **binding** connects a name to a value in some context (an *environment*).

```python
x = 42        # bind name 'x' to the value 42
x = "hello"   # rebind 'x' to a new value (in Python, names are just labels)
```

The **environment** is a mapping from names to values (or to storage locations). Executing code is largely *creating, looking up, and destroying bindings* in environments.

---

## II. THE TWO MODELS: NAMES-AS-LABELS vs BOXES

Languages differ fundamentally in what a variable *is*:

### Value semantics ("boxes")
The variable *is* the storage; assignment *copies*.
```c
int a = 5;
int b = a;   // b is a COPY; changing b never touches a
```
C, C++ (for value types), Rust (for `Copy` types), Go structs.

### Reference semantics ("labels")
The variable is a *name pointing at* a value; assignment copies the *pointer*.
```python
a = [1, 2, 3]
b = a          # b points at the SAME list
b.append(4)    # a is now [1,2,3,4] too!  ← the classic surprise
```
Python, JavaScript, Java (for objects), Ruby.

**This single distinction causes more beginner bugs than any other.** Always ask of a new language: *"Does assignment copy the value or the reference?"* (It's often *both*, depending on the type — Java copies primitives, references objects.)

---

## III. SCOPE — THE RULEBOOK FOR NAME LOOKUP

**Scope** is the region of a program where a binding is visible. When you write `x`, scope rules decide *which* `x`.

### Lexical (static) scope — the modern default
A name refers to the binding in the *nearest enclosing block in the source text*. You can determine it by reading the code, without running it.

```javascript
let x = "global";
function outer() {
  let x = "outer";
  function inner() { return x; }  // 'x' = "outer" (nearest enclosing text)
  return inner();
}
outer();  // "outer"
```

### Dynamic scope — the historical alternative
A name refers to the *most recent binding on the call stack at runtime*. Determined by *who called you*, not where you're written. Rare today (old Lisps, Bash variables, Emacs Lisp) because it makes code hard to reason about.

```
# In a dynamically-scoped language, inner() would see the caller's x,
# not the lexically-enclosing x. Almost always confusing → abandoned.
```

**Lexical scope won** because it makes functions self-contained: you can understand a function by reading it, not by tracing every possible caller.

---

## IV. CLOSURES — SCOPE THAT OUTLIVES ITS FRAME

A **closure** is a function bundled with the environment where it was *defined*. Because of lexical scope, an inner function "captures" the variables it uses — and they survive even after the outer function returns.

```javascript
function makeCounter() {
  let count = 0;                 // local to makeCounter
  return function () {           // this inner function CLOSES OVER count
    count += 1;
    return count;
  };
}
const c = makeCounter();
c(); // 1
c(); // 2  ← 'count' lived on, captured by the closure
```

`count` should have died when `makeCounter` returned — but the returned function still references it, so the runtime keeps it alive. That captured environment *is* the closure.

Closures are the foundation of:
- Callbacks and event handlers (they remember their context)
- Data privacy (the module pattern — `count` is inaccessible except through `c`)
- Functional patterns (currying, partial application)
- The way `async` state is preserved across `await`

> You do not truly understand closures until you've implemented one. In an interpreter, a closure is literally a pair: `(the function's AST, a pointer to the defining environment)`. See [`../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md`](../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md).

---

## V. LIFETIME — WHEN A BINDING LIVES AND DIES

**Scope** is *where* a name is visible (a source-text region). **Lifetime** is *when* the underlying value exists (a runtime duration). They're related but distinct:

- A local variable's scope is its block; its lifetime is normally its stack frame.
- A closure-captured variable's lifetime *exceeds* its original frame.
- A heap value's lifetime lasts until it's freed (manually in C, by GC in Java, by ownership rules in Rust).

Rust makes lifetimes *explicit and checked* — the borrow checker proves no reference outlives the value it points to. This is Rust's superpower and its learning curve. (See [`../04-MEMORY-AND-RUNTIME/03-Ownership-and-Borrowing.md`](../04-MEMORY-AND-RUNTIME/03-Ownership-and-Borrowing.md).)

---

## VI. SHADOWING, HOISTING, AND OTHER SCOPE GOTCHAS

- **Shadowing** — an inner binding hides an outer one of the same name. Legal in most languages; sometimes intentional (Rust encourages it), sometimes a bug.
- **Hoisting** (JavaScript) — `var` declarations are conceptually moved to the top of their function, so `var` can be *used before its line*. `let`/`const` are hoisted but stay in a "temporal dead zone" and error if used early. A frequent source of confusion.
- **Block vs function scope** — `let`/`const` are block-scoped `{...}`; old `var` is function-scoped. Choosing wrong causes leaked loop variables.

---

## 📌 Key Takeaways
- Distinguish **value**, **name**, and **binding**; execution is managing bindings in environments.
- The deepest split: **value semantics (copy)** vs **reference semantics (alias)** — source of the #1 beginner bug.
- **Lexical scope** (by source text) beat dynamic scope (by call stack) because it makes code readable.
- A **closure** = function + captured defining environment; it keeps variables alive past their frame.
- **Scope** (where visible) ≠ **lifetime** (when it exists); Rust checks lifetimes explicitly.

**Next:** [`05-Expressions-Statements-and-Control.md`](./05-Expressions-Statements-and-Control.md)
