# 🔮 Logic and Declarative Programming

> *"Stop telling the machine how. Tell it what — and let it figure out how."*

---

## I. THE DECLARATIVE IDEA

**Declarative programming** describes *what* you want, not *how* to compute it. You specify the desired result or the rules of the domain; the language's engine determines the steps.

Contrast:
```sql
-- DECLARATIVE (SQL): describe the result
SELECT name FROM users WHERE age > 18 ORDER BY name;
```
```python
# IMPERATIVE: spell out every step
result = []
for u in users:
    if u.age > 18: result.append(u.name)
result.sort()
```

The SQL says nothing about loops, indexes, or sorting algorithms. The **query planner** decides whether to scan, use an index, or hash-join — often better than you would. That separation of *intent* from *execution strategy* is the essence of declarative programming.

**Declarative languages you already use:** SQL (data), HTML/CSS (documents/layout), regular expressions (text patterns), Makefiles (build rules), Terraform (infrastructure), and configuration in general.

---

## II. LOGIC PROGRAMMING — THE PUREST DECLARATIVE FORM

**Logic programming** takes declarativeness to its logical extreme: you state **facts** and **rules**, then ask **questions**, and an inference engine *searches* for answers using formal logic. Prolog is the canonical example.

```prolog
% FACTS
parent(tom, bob).
parent(bob, ann).
parent(bob, pat).

% RULE: X is a grandparent of Z if X is a parent of Y and Y is a parent of Z
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% QUERY
?- grandparent(tom, Who).
Who = ann ;
Who = pat.
```

You never wrote a loop or a search. You declared *what a grandparent is*, and the engine **searched** the space of facts to satisfy the query. This is a radically different mental model: programming as *declaring truths* and *asking questions*.

---

## III. HOW THE ENGINE WORKS: UNIFICATION + BACKTRACKING

Two mechanisms power logic programming:

1. **Unification** — pattern-matching that solves for variables. `grandparent(tom, Who)` unifies `X=tom`, then tries to satisfy `parent(tom, Y), parent(Y, Z)`, binding `Y` and `Z` to make the facts true.

2. **Backtracking search** — when one path fails, the engine *rewinds* and tries another. It systematically explores all ways to satisfy the goals. (The `;` above asks "any more solutions?" — the engine backtracks to find `pat` after `ann`.)

This built-in search is why logic programming shines for **constraint satisfaction, parsing, theorem proving, expert systems, and puzzles** — problems that are naturally "find values satisfying these rules."

---

## IV. CONSTRAINT PROGRAMMING

A close cousin: **constraint programming** and **constraint logic programming**. You declare variables, their domains, and constraints among them; a solver finds assignments that satisfy all constraints.

```
# Sudoku, declaratively:
# variables: 81 cells, each in 1..9
# constraints: each row, column, and box has all distinct values
# → hand it to a solver; it fills the grid. You wrote NO solving algorithm.
```

Modern **SAT/SMT solvers** (Z3, MiniSat) are the industrial heirs of this idea — they power program verification, chip design, and scheduling. You encode your problem as logical constraints; the solver does the heavy search.

---

## V. WHY DECLARATIVE MATTERS (even if you never write Prolog)

1. **You already live in it.** SQL, regex, CSS, build systems, IaC — declarative is everywhere in real engineering.
2. **It separates intent from optimization.** The engine can improve execution (better query plans, better solvers) without you rewriting anything. Your SQL from 2005 runs faster on a modern database — the *what* was future-proof.
3. **It shrinks code.** Declaring the *what* is often an order of magnitude shorter than coding the *how*.
4. **It's the shape of the future.** Much of "AI-assisted" and high-level tooling is about declaring intent and letting systems synthesize the how.

**The tradeoff:** you give up fine control over execution. When the query planner or solver makes a bad choice, debugging is harder — you're one level removed from the mechanics. Declarative is a trade of control for concision and adaptability.

---

## VI. THE MENTAL SHIFT

Imperative asks: *"What steps produce the answer?"*
Declarative asks: *"What is true about the answer?"*

Learning to think declaratively — even inside an imperative language — makes you write better SQL, cleaner configuration, and more maintainable rule systems. When you catch yourself hand-coding a search that a solver or query could express, you've found a place declarative thinking pays off.

---

## 📌 Key Takeaways
- **Declarative** = describe *what* (the result/rules); the engine decides *how*. SQL, regex, HTML, IaC.
- **Logic programming** (Prolog) states facts + rules, then searches for answers via **unification + backtracking**.
- **Constraint programming** and modern **SAT/SMT solvers** industrialize "declare constraints, let the solver search."
- Declarative trades execution control for concision, adaptability, and future-proofing.

**Next:** [`05-Concurrent-and-Reactive.md`](./05-Concurrent-and-Reactive.md)
