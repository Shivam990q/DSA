# 🔤 Syntax vs Semantics

> *"'It compiles' means it is well-formed. It does not mean it is correct."*

---

## I. THE DISTINCTION

- **Syntax** = the *form*. Which strings of characters are grammatically legal.
- **Semantics** = the *meaning*. What a legal program actually computes.

A famous natural-language analogy (Chomsky): *"Colorless green ideas sleep furiously."* This sentence is **syntactically perfect** — noun, verb, adverb, all in order — but **semantically nonsense**. Programs can be exactly like this: legal but meaningless (or meaning something you didn't intend).

```python
# syntactically fine, semantically a disaster
balance = balance - amount   # forgot to check amount <= balance → negative balance
```

The compiler is happy. The bank is not.

---

## II. THE TWO KINDS OF SEMANTICS

Semantics itself splits in two:

### Static semantics (checked before running)
Rules verified at compile time *without executing* the program:
- **Type checking** — `"hello" + 5` may be illegal.
- **Scope/name resolution** — is `x` declared and visible here?
- **Definite assignment** — is a variable used before it's set? (Java, C# enforce this.)
- **Arity** — does this call pass the right number of arguments?

### Dynamic semantics (what happens at run time)
The actual behavior when executed:
- Evaluation order, effects, mutation
- What `a[i]` does when `i` is out of bounds (panic? UB? exception?)
- What arithmetic overflow does (wrap? trap? saturate?)

A program can pass static checks and still be dynamically wrong (logic bugs), or crash dynamically on inputs the types couldn't rule out (division by zero, null deref in languages that allow it).

---

## III. THE ERROR LADDER (when things get caught)

Errors are cheapest to fix the earlier they're caught:

```
1. Lexical error     illegal token          "3@x"          ← caught by lexer
2. Syntax error      bad grammar            "if x {"        ← caught by parser
3. Static-semantic   type/scope error       "1" + 2 (some langs) ← caught by type checker
4. Dynamic-semantic  runtime error          arr[999]        ← caught at run time (or not!)
5. Logic error       wrong result           computed tax wrong ← caught by tests / users
```

**The entire value proposition of static typing** is pushing errors *up* this ladder — from level 4/5 (runtime, users) to level 3 (compile time). That's why "if it compiles, it works" is *more* true in Rust/Haskell than in Python: their type systems catch more at level 3.

But note level 5: **no language catches logic errors.** A type system ensures you didn't add a string to an int; it cannot ensure you computed the *right* number. That's what tests, proofs, and thought are for.

---

## IV. WHY THE DISTINCTION MATTERS PRACTICALLY

1. **Debugging.** "Syntax error" and "wrong answer" are different worlds. Syntax errors are the parser's complaint; semantic bugs need reasoning about meaning.
2. **Undefined behavior.** In C, some *syntactically and statically valid* programs have *no defined dynamic semantics* (signed overflow, use-after-free). The compiler may do anything — this is the source of the scariest security bugs.
3. **Language power.** A more expressive *static semantics* (richer types) moves more bugs to compile time. This is the whole thrust of the type-systems section.

---

## V. SYNTACTIC SUGAR — SAME MEANING, NICER FORM

**Syntactic sugar** is syntax that adds no new semantics — it just reads better, and "desugars" into a more primitive form:

```python
# sugar
[x*x for x in nums if x > 0]
# desugars to
result = []
for x in nums:
    if x > 0:
        result.append(x*x)
```

```javascript
async function f() { const x = await g(); }
// desugars to promise .then() chains
```

Recognizing sugar is a superpower: it means fewer *fundamental* concepts than the surface suggests. A language may have 200 syntactic forms but 20 semantic primitives. Learn the primitives; the sugar is lookup.

---

## VI. THE GRANDMASTER LENS

When reading unfamiliar code, separate the two questions:
1. **"Is this legal, and what shape is it?"** (syntax — usually obvious)
2. **"What does this *do*, including on weird inputs?"** (semantics — where the depth is)

Beginners obsess over syntax ("what's the symbol for X?"). Experts have automated syntax and spend their attention entirely on semantics — meaning, effects, edge cases, and cost.

---

## 📌 Key Takeaways
- Syntax = form (legal?); semantics = meaning (what it does?).
- Semantics splits into **static** (compile-time checks) and **dynamic** (runtime behavior).
- The error ladder: static typing pushes errors from runtime/users up to compile time; no language catches logic errors.
- Syntactic sugar adds form, not meaning — learn the primitives beneath it.

**Next:** [`03-Grammars-and-Parsing.md`](./03-Grammars-and-Parsing.md)
