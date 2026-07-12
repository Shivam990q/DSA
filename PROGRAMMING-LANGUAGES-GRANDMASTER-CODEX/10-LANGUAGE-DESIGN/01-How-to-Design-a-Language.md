# 🎨 How to Design a Language

> *"Every feature you add is a feature every user must learn, every tool must support, and you must maintain forever. Add slowly."*

---

## I. START WITH PURPOSE

Every good language begins with a **clear purpose and audience**. The purpose determines every subsequent tradeoff (recall the [dials](../00-PHILOSOPHY-AND-DOCTRINE/03-Language-Tradeoffs.md)):

- **C** — a portable assembler for OS development → chose control over safety.
- **Go** — productivity for large teams at Google → chose simplicity over expressiveness.
- **Rust** — safe systems programming → chose safety+control over ease of learning.
- **SQL** — querying relational data → chose declarative over imperative.

Ask first: *Who is this for? What problem does it solve better than existing languages? What will I deliberately NOT support?* A language that tries to be everything to everyone becomes C++ — powerful and overwhelming. Focus is a feature.

---

## II. THE DESIGN DECISIONS (the checklist)

Designing a language means answering, deliberately, the eternal questions from [`../00-PHILOSOPHY-AND-DOCTRINE/01-Why-Languages-Exist.md`](../00-PHILOSOPHY-AND-DOCTRINE/01-Why-Languages-Exist.md):

1. **Typing** — static or dynamic? Inferred or annotated? How strong? Nullable?
2. **Memory** — manual, GC, or ownership? Value or reference semantics?
3. **Paradigm** — what's idiomatic? What does "good code" look like?
4. **Syntax** — braces or indentation? Expression- or statement-oriented? Familiar (C-like) or novel?
5. **Error handling** — exceptions, error values, `Option`/`Result`, panics?
6. **Concurrency** — threads, async, actors, CSP, none?
7. **Effects & mutation** — immutable by default? Pure? Controlled effects?
8. **Metaprogramming** — macros? reflection? none (for simplicity)?
9. **Module system** — how is code organized, imported, versioned?
10. **Tooling** — build, package manager, formatter, REPL (often decisive for adoption!).

Each answer places your language in the design space. Consistency among the answers is what makes a language feel *coherent* rather than bolted-together.

---

## III. SYNTAX DESIGN PRINCIPLES

Syntax is "skin," but skin matters for adoption and error-proneness:

- **Familiarity lowers the barrier.** C-like syntax (`{}`, `if`, `for`) means millions already half-know your language. Radical novelty (APL, Lisp parens) raises the wall.
- **Readability over writability.** Code is read far more than written. Optimize for the reader (Python's whitespace, Go's `gofmt`).
- **Unambiguous grammar.** Avoid ambiguity (dangling else); design so the parser has one clear tree (see [`../01-LANGUAGE-FOUNDATIONS/03-Grammars-and-Parsing.md`](../01-LANGUAGE-FOUNDATIONS/03-Grammars-and-Parsing.md)).
- **Consistency.** Similar things should look similar; the "principle of least surprise." Irregular special cases are cognitive tax.
- **One obvious way** (Python) vs **many ways** (Perl) — a philosophy choice with big maintainability consequences.

---

## IV. LEARN FROM CLASSIC MISTAKES

Great design is often knowing what *not* to do:

- **`null`** — Tony Hoare's "billion-dollar mistake." Prefer `Option`/`Maybe` and encode absence in types (see [`../03-TYPE-SYSTEMS/04-Advanced-Types.md`](../03-TYPE-SYSTEMS/04-Advanced-Types.md)). Rust, Kotlin, Swift learned this.
- **Weak implicit coercion** — JavaScript's `[] + {}` chaos. Be explicit about conversions.
- **Two things that do the same thing** — `==` vs `===`, `null` vs `undefined`. Every duplication is confusion.
- **Overpowered features** — unrestricted `goto`, unrestricted operator overloading, unrestricted macros → unreadable code. Constrain power.
- **Ignoring tooling** — a great language with bad build/package tooling loses to a mediocre one with `cargo`/`npm`. Tooling is part of the language's success.
- **Breaking changes** — Python 2→3 took a decade. Backward compatibility vs progress is a brutal tradeoff (C++ chose compatibility → complexity; Python chose progress → pain).

---

## V. THE FEATURE-CREEP TRAP

The hardest discipline: **saying no.** Every feature interacts with every other feature (combinatorial complexity), must be documented, supported by tools, and maintained indefinitely. Go's success came largely from *refusing* features (no inheritance, no generics for a decade, no exceptions). The mantra: *"It's easier to add a feature later than to remove one."* Start minimal; let real usage reveal what's genuinely needed. A small, coherent language beats a large, incoherent one.

---

## VI. THE PATH FROM DESIGN TO REALITY

A language isn't real until it runs. The implementation path (built in the next file):
```
1. Define the grammar (BNF)          — what's legal
2. Write the lexer                   — text → tokens
3. Write the parser                  — tokens → AST
4. (Optional) semantic analysis      — scope + type checking
5. Write an interpreter OR compiler  — execute or translate the AST
6. Build the tooling                 — REPL, formatter, package manager
7. Write the spec + docs             — pin down semantics
```

Start with a tree-walking interpreter (simplest — see [`../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md`](../05-COMPILERS-AND-INTERPRETERS/04-Interpreters-VMs-and-JIT.md)); optimize to bytecode/VM/JIT later if needed. The next file builds a complete working language this way.

---

## 📌 Key Takeaways
- Start with a **clear purpose and audience** — it dictates every tradeoff; focus is a feature.
- Deliberately answer the ~10 design decisions (typing, memory, paradigm, syntax, errors, concurrency, effects, meta, modules, **tooling**); coherence among them is key.
- Syntax: favor **familiarity, readability, unambiguity, consistency**.
- Avoid classic mistakes: `null`, weak coercion, redundant features, overpowered features, and neglected tooling.
- Resist **feature creep** — it's easier to add than remove; small and coherent wins.
- A language is real only when it runs: grammar → lexer → parser → (checker) → interpreter/compiler → tooling.

**Next:** [`02-Build-Your-Own-Language.md`](./02-Build-Your-Own-Language.md)
