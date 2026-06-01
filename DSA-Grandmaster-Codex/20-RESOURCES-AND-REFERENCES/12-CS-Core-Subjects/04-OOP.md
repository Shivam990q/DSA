# 🧩 OOP — Interview Prep

> Object-Oriented Programming concepts are asked in nearly every interview, often tied to language specifics (C++/Java/Python).

---

## THE 4 PILLARS ⭐
1. **Encapsulation** — bundling data + methods; hiding internal state (private fields, getters/setters)
2. **Abstraction** — exposing only essential features, hiding complexity (abstract classes, interfaces)
3. **Inheritance** — a class derives properties from another (code reuse, "is-a" relationship)
4. **Polymorphism** — same interface, different behavior:
   - **Compile-time** (overloading)
   - **Runtime** (overriding, virtual functions)

---

## CORE CONCEPTS
- Class vs Object
- Constructor / Destructor (and types: default, parameterized, copy)
- `this` pointer / `self`
- Access modifiers (public, private, protected)
- Static members
- Abstract class vs Interface
- Virtual functions, vtables (C++)
- Method overloading vs overriding
- Composition vs Inheritance ("has-a" vs "is-a")
- Multiple inheritance + diamond problem
- Operator overloading (C++)

---

## DESIGN PRINCIPLES (SOLID) ⭐
- **S**ingle Responsibility — one reason to change
- **O**pen/Closed — open for extension, closed for modification
- **L**iskov Substitution — subtypes substitutable for base types
- **I**nterface Segregation — many specific interfaces > one general
- **D**ependency Inversion — depend on abstractions, not concretions

Plus: **DRY** (Don't Repeat Yourself), **KISS**, **YAGNI**, composition over inheritance.

---

## DESIGN PATTERNS (know the common ones)
- **Creational**: Singleton, Factory, Builder, Prototype
- **Structural**: Adapter, Decorator, Facade, Proxy, Composite
- **Behavioral**: Observer, Strategy, Iterator, Command, State

(Reference: "Design Patterns" by Gang of Four; [refactoring.guru](https://refactoring.guru) for visuals)

---

## THE TOP 20 INTERVIEW QUESTIONS
1. What are the 4 pillars of OOP? (with examples)
2. Abstraction vs Encapsulation?
3. Overloading vs Overriding?
4. Abstract class vs Interface?
5. What is a virtual function? How do vtables work?
6. Composition vs Inheritance?
7. What is the diamond problem? How is it resolved?
8. Static vs instance methods?
9. What is a copy constructor? Shallow vs deep copy?
10. Explain SOLID principles.
11. What is the Singleton pattern? When to use?
12. What is the Factory pattern?
13. What is the Observer pattern?
14. Constructor vs destructor?
15. Can you override a static method?
16. What is polymorphism — give a real example?
17. What are access modifiers?
18. final/sealed keyword purpose?
19. Association vs Aggregation vs Composition?
20. Why prefer composition over inheritance?

---

## RESOURCES
### YouTube
- **[Gate Smashers](https://www.youtube.com/@GateSmashers)** — OOP concepts
- Language-specific channels (Java: Telusko; C++: CodeBeauty)

### Written
- **[GeeksforGeeks](https://www.geeksforgeeks.org)** — OOP concepts + interview questions ⭐
- **refactoring.guru** — design patterns (visual, excellent)

### Books
- **Head First Object-Oriented Analysis and Design**
- **Design Patterns** (Gang of Four)
- **Clean Code** (Robert Martin) — for principles

---

## LOW-LEVEL DESIGN (LLD) — the OOP application
Senior interviews ask you to DESIGN with OOP:
- Design a parking lot
- Design a vending machine
- Design an elevator system
- Design a library management system
- Design tic-tac-toe / chess

Practice: identify classes, relationships, apply SOLID + patterns.

---

## PREP PLAN (3 days)
- Day 1: 4 pillars + core concepts
- Day 2: SOLID + design patterns
- Day 3: LLD practice (parking lot, etc.) + revise top 20

---

**→ Next:** [`05-Aptitude-And-Reasoning.md`](./05-Aptitude-And-Reasoning.md)
