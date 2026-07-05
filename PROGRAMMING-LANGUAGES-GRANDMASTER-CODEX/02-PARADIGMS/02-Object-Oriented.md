# 🧩 Object-Oriented Programming

> *"Don't ask for data and act on it. Ask the object to act. Bundle state with the behavior that guards it."*

---

## I. THE CORE IDEA

**Object-oriented programming (OOP)** structures a program as a collection of **objects** — bundles of *state* (data/fields) and *behavior* (methods) that interact by sending each other messages (calling methods). The organizing insight: **keep data and the code that operates on it together**, and hide the data behind a controlled interface.

```java
class BankAccount {
    private double balance;              // hidden state

    public void deposit(double amount) { // behavior that guards the state
        if (amount <= 0) throw new IllegalArgumentException();
        balance += amount;
    }
    public double getBalance() { return balance; }
}
```

No one can set `balance` to a negative number directly — they must go through `deposit`, which enforces the rule. State and its guardians live together.

---

## II. THE FOUR PILLARS

### 1. Encapsulation
Hide internal state; expose a controlled interface. The object protects its own **invariants** (rules that must always hold, like "balance ≥ 0"). Callers depend on *what* it does, not *how*. This is the most important pillar — the others are secondary.

### 2. Abstraction
Model the essential features, ignore the irrelevant. A `Car` exposes `drive()` and `brake()`; you don't touch the pistons. Abstraction manages complexity by hiding detail behind a clean interface.

### 3. Inheritance
A class can extend another, reusing and specializing its behavior.
```java
class SavingsAccount extends BankAccount {
    void addInterest() { deposit(getBalance() * 0.03); }
}
```
Inheritance models "is-a" relationships — a `SavingsAccount` *is a* `BankAccount`. **But it's the most abused pillar** (see section IV).

### 4. Polymorphism
One interface, many implementations. Code written against a general type works with any specific subtype.
```java
void report(BankAccount acc) { print(acc.getBalance()); }
// works for BankAccount, SavingsAccount, CheckingAccount — any subtype
```
This is **subtype polymorphism** (dynamic dispatch): the actual method called is chosen at runtime based on the object's real type. It's what makes OOP extensible — add a new subtype without touching existing code.

---

## III. HOW POLYMORPHISM ACTUALLY WORKS (the vtable)

Under the hood, dynamic dispatch is usually a **virtual method table (vtable)**: each object carries a hidden pointer to a table of function pointers for its class. Calling `acc.getBalance()` means "look up `getBalance` in the object's vtable and call it." This is one pointer indirection — cheap, but not free (it can prevent inlining and hurt CPU branch prediction). Knowing this explains why virtual calls cost slightly more than direct calls, and why languages like C++ make `virtual` opt-in.

---

## IV. THE GREAT DEBATE: INHERITANCE VS COMPOSITION

Inheritance was OOP's headline feature — and its biggest mistake when overused.

**Problems with deep inheritance:**
- **Fragile base class** — changing a parent breaks distant children.
- **The diamond problem** — multiple inheritance creates ambiguity (C++'s pain; Java banned it for classes).
- **Tight coupling** — subclasses depend intimately on parent internals.
- **Rigid taxonomies** — real domains rarely form clean trees ("a Square is-a Rectangle" breaks — see the Liskov Substitution Principle).

**The modern consensus: "favor composition over inheritance."** Instead of *being* a thing, *have* a thing:
```java
// Instead of: class Car extends Engine  (a car is NOT an engine)
class Car {
    private Engine engine;   // a car HAS an engine  ← composition
    void start() { engine.ignite(); }
}
```
Go and Rust *have no inheritance at all* — they use composition + interfaces/traits. Their success proved inheritance was never essential to OOP; encapsulation and polymorphism were the real value.

---

## V. SOLID — THE OOP DESIGN PRINCIPLES

Five principles for maintainable OO code:
- **S**ingle Responsibility — a class should have one reason to change.
- **O**pen/Closed — open for extension, closed for modification.
- **L**iskov Substitution — subtypes must be usable anywhere their base type is.
- **I**nterface Segregation — many small interfaces beat one fat one.
- **D**ependency Inversion — depend on abstractions, not concretions.

These aren't laws; they're heuristics against the failure modes OOP tends toward (rigidity, coupling, fragility).

---

## VI. STRENGTHS, WEAKNESSES, AND WHEN TO USE IT

**Strengths:** excellent for **domain modeling** (entities with identity and behavior), large team codebases (clear ownership boundaries), GUIs, and systems with many similar-but-varying entities.

**Weaknesses:** encourages hidden mutable state (the thing FP warns against); deep hierarchies get brittle; can add ceremony for simple tasks; poor fit for data-transformation pipelines (functional wins there).

**When to reach for it:** modeling a business domain with entities and invariants (orders, users, accounts), building extensible frameworks where plugins implement interfaces, and any time "bundle this data with its rules" is the natural decomposition.

---

## 📌 Key Takeaways
- OOP bundles **state + behavior** into objects and hides state behind interfaces.
- Four pillars: **encapsulation** (the key one), abstraction, inheritance, polymorphism.
- Polymorphism is usually implemented via a **vtable** (one indirection, small cost).
- **Favor composition over inheritance** — Go and Rust prove inheritance is optional.
- **SOLID** principles guard against OOP's failure modes.

**Next:** [`03-Functional.md`](./03-Functional.md)
