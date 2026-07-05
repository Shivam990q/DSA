# 🧭 The Polyglot Mindset

> *"Learn languages in families, not in isolation. The tenth language in a family takes a day."*

---

## I. WHY MOST PEOPLE LEARN LANGUAGES SLOWLY

They treat each language as a fresh island: relearn loops, relearn functions, relearn "how do I print." This is exhausting and never ends, because syntax is infinite and arbitrary.

The grandmaster does the opposite. They carry a **mental template of "what a language has"** and, for each new language, simply *fill in the blanks*. Learning becomes a lookup, not a rediscovery.

---

## II. THE UNIVERSAL LANGUAGE TEMPLATE

When you meet any language, answer these in order. This is your intake checklist:

```
1. TYPING     static or dynamic? inferred or annotated? strong or weak?
2. MEMORY     manual, GC, or ownership? values or references by default?
3. PARADIGM   imperative? OOP? functional? multi-paradigm? what's idiomatic?
4. FUNCTIONS  first-class? closures? higher-order? how are they declared?
5. DATA       what are the built-in collections? records/structs? enums/unions?
6. ERRORS     exceptions? error values? Option/Result? panics?
7. CONCURRENCY  threads? async? goroutines? actors? none?
8. MODULES    how is code organized, imported, and packaged?
9. TOOLING    build tool, package manager, formatter, test runner, REPL?
10. IDIOM     what does "good code" look like here? (read the std lib)
```

Fill those ten in and you can write competent code the same day. Everything else is vocabulary you pick up as you go.

---

## III. THE LANGUAGE FAMILIES

Languages cluster into families that share ancestry and ideas. Learn one member well and the family opens up:

| Family | Members | Shared DNA |
|--------|---------|-----------|
| **C family** | C, C++, Java, C#, JavaScript, Go, Rust | curly braces, `if/for/while`, similar operators |
| **ML family** | Standard ML, OCaml, F#, (Rust's types), Haskell-adjacent | type inference, pattern matching, algebraic data types |
| **Lisp family** | Common Lisp, Scheme, Clojure, Racket | code-as-data, macros, s-expressions, REPL-driven |
| **Scripting** | Python, Ruby, Perl, PHP, Lua | dynamic typing, quick to write, GC, batteries included |
| **Logic** | Prolog, Datalog, miniKanren | you state facts and rules; the engine searches |
| **Array** | APL, J, K, (NumPy-style) | whole-array operations, terse, data-parallel |

Cross-family transfer is where the growth is. A C programmer learning Haskell doesn't just learn a language — they *rewire how they think* (immutability, purity, types-as-proofs). That rewiring is the whole point of Perlis's quote.

---

## IV. THE 3-DAY PROTOCOL FOR A NEW LANGUAGE

**Day 1 — the template.** Answer the 10 template questions from the official docs. Write "hello world," a function, a loop, a collection transform, and error handling. Get the toolchain running (build, run, test).

**Day 2 — the idiom.** Read real code: the standard library, a popular small library. Notice *how they do things*. Rewrite one small program you know well (e.g., a to-do CLI) idiomatically.

**Day 3 — the edges.** Learn what this language does *differently* from ones you know. Rust's borrow checker. Go's goroutines. Python's decorators. Haskell's laziness. This is where the language's soul is.

After three focused days you are not an expert — but you are *dangerous*, and expertise is now just reps.

---

## V. WHAT TRANSFERS AND WHAT DOESN'T

**Transfers everywhere (learn once):**
- Control flow, functions, recursion
- Data structures and algorithms (that's the sibling codex)
- Naming, decomposition, testing discipline
- The concept of types, scope, memory

**Does NOT transfer (relearn each time):**
- Exact syntax and operators
- The standard library's shape and names
- Idioms and community conventions
- The specific tradeoffs (what's cheap vs expensive here)

Invest heavily in the transferable layer. It compounds across every language for the rest of your career.

---

## VI. THE POLYGLOT'S DISCIPLINE

- **Depth in one, breadth in many.** Master one language completely (know its runtime, its spec). Then breadth becomes cheap.
- **Read specs, not just tutorials.** The spec is the truth; tutorials are one person's summary.
- **Implement to understand.** You don't understand closures until you've implemented them (see the compilers section).
- **Judge by fit, not fashion.** The best language is the one that fits the problem, the team, and the constraints.

---

## 📌 Key Takeaways
- Carry a 10-point template and *fill in the blanks* for each new language.
- Learn languages in **families**; cross-family learning rewires your thinking.
- The 3-day protocol: template → idiom → edges.
- Invest in the transferable layer (concepts); it compounds forever.

**Next:** [`03-Language-Tradeoffs.md`](./03-Language-Tradeoffs.md)
