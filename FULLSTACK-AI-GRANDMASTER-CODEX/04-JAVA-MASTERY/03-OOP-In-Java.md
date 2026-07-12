# ☕ 02 — Object-Oriented Programming in Java ⭐

> *"Objects let you model the world in code: a thing that knows something (state) and can do something (behavior). Master OOP and you stop writing scripts and start designing systems."*

**Prev:** [`02-Java-Fundamentals.md`](./02-Java-Fundamentals.md) · **Next:** [`04-Collections-Framework.md`](./04-Collections-Framework.md) · **Index:** [`01-Getting-Started.md`](./01-Getting-Started.md)

---

## I. CLASSES AND OBJECTS — THE CORE IDEA

A **class** is a blueprint. An **object** is a concrete thing built from that blueprint. The class `Car` describes what every car *has* (fields) and what every car *does* (methods); each actual car you make with `new Car()` is an object (an *instance*).

```java
// The blueprint
public class Car {
    // FIELDS (state) — what a car HAS
    String make;
    String model;
    int speed;

    // METHOD (behavior) — what a car DOES
    void accelerate(int amount) {
        speed += amount;
        System.out.println(make + " is now going " + speed + " km/h");
    }
}
```

```java
public class Main {
    public static void main(String[] args) {
        Car myCar = new Car();   // create an OBJECT (instance) from the blueprint
        myCar.make = "Toyota";   // set state
        myCar.model = "Corolla";
        myCar.accelerate(30);    // call behavior → "Toyota is now going 30 km/h"

        Car another = new Car(); // a SEPARATE object with its own state
        another.make = "Tesla";
        another.accelerate(100); // "Tesla is now going 100 km/h"
    }
}
```

Key mental model:

```
Class Car  (one blueprint)
   │
   ├──► myCar    {make:"Toyota", model:"Corolla", speed:30}   ← object 1, own state
   └──► another  {make:"Tesla",   model:null,     speed:100}  ← object 2, own state
```

> **`new` allocates on the heap.** `new Car()` reserves memory for a fresh object and returns a reference to it. `myCar` holds that reference. Two variables can point to the same object — then changes through one are visible through the other.

---

## II. CONSTRUCTORS — CONTROLLED CREATION

A **constructor** runs when you `new` an object. It initializes state. It has the same name as the class and no return type.

```java
public class Car {
    String make;
    String model;
    int speed;

    // Constructor — guarantees every Car starts in a valid state
    public Car(String make, String model) {
        this.make = make;        // 'this' distinguishes the field from the parameter
        this.model = model;
        this.speed = 0;          // sensible default
    }

    // Constructor OVERLOADING — multiple ways to build a Car
    public Car(String make) {
        this(make, "Unknown");   // 'this(...)' calls the other constructor — no duplication
    }
}
```

```java
Car a = new Car("Honda", "Civic");
Car b = new Car("Ford");          // model defaults to "Unknown"
```

> **The default constructor.** If you write *no* constructor, Java gives you a free no-argument one. The moment you write *any* constructor, that freebie disappears — so if you still want a no-arg constructor, write it explicitly.

> **`this`** refers to "the current object." Use it to disambiguate fields from parameters with the same name (`this.make = make`), or to call another constructor (`this(...)`).

---

## III. THE FOUR PILLARS OF OOP

OOP rests on four ideas: **Encapsulation, Inheritance, Polymorphism, Abstraction.** They are not trivia — they are the tools you use to keep large systems from collapsing under their own complexity.

---

### Pillar 1 — ENCAPSULATION: hide the data, expose a contract

Encapsulation means bundling data with the methods that operate on it, and **controlling access** so outside code cannot put your object into an invalid state. You make fields `private` and expose `public` methods (getters/setters) that enforce rules.

```java
public class BankAccount {
    private double balance;       // PRIVATE — no outside code can touch this directly
    private final String owner;   // final — set once, never changes

    public BankAccount(String owner, double initialBalance) {
        this.owner = owner;
        if (initialBalance < 0) throw new IllegalArgumentException("Cannot start negative");
        this.balance = initialBalance;
    }

    // Controlled access — the ONLY ways to change balance
    public void deposit(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Deposit must be positive");
        balance += amount;
    }

    public void withdraw(double amount) {
        if (amount <= 0) throw new IllegalArgumentException("Withdrawal must be positive");
        if (amount > balance) throw new IllegalStateException("Insufficient funds");
        balance -= amount;
    }

    // Read-only access (getter, no setter — balance can't be set arbitrarily)
    public double getBalance() { return balance; }
    public String getOwner()   { return owner; }
}
```

```java
public class Bank {
    public static void main(String[] args) {
        BankAccount acc = new BankAccount("Ada", 100);
        acc.deposit(50);
        acc.withdraw(30);
        System.out.println(acc.getBalance()); // 120.0

        // acc.balance = 1_000_000;  // COMPILE ERROR — balance is private. The invariant holds.
    }
}
```

**Why it matters:** without encapsulation, any code anywhere could set `balance = -999999`. With it, every change goes through a method that enforces the rules. The object can *never* be invalid. This is the foundation of safe, maintainable code.

#### Access modifiers — the visibility ladder

| Modifier | Same class | Same package | Subclass (other pkg) | Anywhere |
|----------|:----------:|:------------:|:--------------------:|:--------:|
| `private` | ✅ | ❌ | ❌ | ❌ |
| *(default / package-private)* | ✅ | ✅ | ❌ | ❌ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| `public` | ✅ | ✅ | ✅ | ✅ |

> **Default to `private`.** Make everything as private as possible and open it up only when there's a real need. The less your class exposes, the more freely you can change its internals later without breaking other code.

#### Records — encapsulation boilerplate, gone (Java 16+)

For immutable data carriers, a `record` generates the constructor, getters, `equals()`, `hashCode()`, and `toString()` for you.

```java
// One line replaces ~40 lines of boilerplate
public record Point(int x, int y) {}

public class RecordDemo {
    public static void main(String[] args) {
        Point p = new Point(3, 4);
        System.out.println(p.x());      // 3  (accessor)
        System.out.println(p);          // Point[x=3, y=4]  (auto toString)
        System.out.println(p.equals(new Point(3, 4))); // true (auto equals — by value)
    }
}
```

---

### Pillar 2 — INHERITANCE: reuse and specialize

Inheritance lets a class (the **subclass**/child) acquire the fields and methods of another (the **superclass**/parent) and then add or change behavior. It models an **"is-a"** relationship: a `Dog` *is an* `Animal`.

```java
public class Animal {
    protected String name;   // protected → visible to subclasses

    public Animal(String name) { this.name = name; }

    public void eat() { System.out.println(name + " is eating."); }
    public void makeSound() { System.out.println(name + " makes a sound."); }
}
```

```java
public class Dog extends Animal {   // Dog IS-A Animal
    public Dog(String name) {
        super(name);   // call the parent constructor FIRST
    }

    // Override: provide Dog-specific behavior
    @Override
    public void makeSound() { System.out.println(name + " barks: Woof!"); }

    // Add new behavior unique to Dog
    public void fetch() { System.out.println(name + " fetches the ball."); }
}
```

```java
public class Zoo {
    public static void main(String[] args) {
        Dog d = new Dog("Rex");
        d.eat();        // inherited from Animal → "Rex is eating."
        d.makeSound();  // overridden → "Rex barks: Woof!"
        d.fetch();      // Dog-only
    }
}
```

> **`super`** calls the parent: `super(name)` invokes the parent constructor (must be the first statement in the child constructor); `super.makeSound()` calls the parent's version of a method you've overridden.

> **`@Override` is your friend.** It's optional but always use it. It tells the compiler "I intend to override a parent method." If you typo the name or get the signature wrong, you get a compile error instead of a silent new method that never gets called.

#### Composition over inheritance — the senior engineer's default

Inheritance is powerful but **rigid**. Deep hierarchies (`A extends B extends C extends D`) become fragile: a change high up ripples everywhere. The widely-followed guideline is **"favor composition over inheritance."** Instead of a `Car` *being* an `Engine`, a `Car` *has* an `Engine`:

```java
// COMPOSITION: Car HAS-A Engine (flexible — swap engines, no inheritance chain)
public class Engine {
    public void start() { System.out.println("Engine roars to life."); }
}

public class Car {
    private final Engine engine;            // Car HAS an Engine
    public Car(Engine engine) { this.engine = engine; }
    public void start() { engine.start(); } // delegate
}
```

Use inheritance for genuine "is-a" relationships with shared behavior; use composition (has-a) for everything else. Java enforces one hard limit: **a class can extend only one class** (no multiple inheritance of classes) — composition has no such limit.

---

### Pillar 3 — POLYMORPHISM: one interface, many forms

Polymorphism ("many shapes") lets you treat different types through a common type, and the *right* method runs based on the actual object at runtime. This is what makes code extensible: you write against the general type and add new specific types without touching existing code.

```java
public class Shape {
    public double area() { return 0; }
}

public class Circle extends Shape {
    private final double r;
    public Circle(double r) { this.r = r; }
    @Override public double area() { return Math.PI * r * r; }
}

public class Rectangle extends Shape {
    private final double w, h;
    public Rectangle(double w, double h) { this.w = w; this.h = h; }
    @Override public double area() { return w * h; }
}
```

```java
import java.util.List;

public class Drawing {
    public static void main(String[] args) {
        // A list of Shape can hold ANY subclass
        List<Shape> shapes = List.of(new Circle(2), new Rectangle(3, 4));

        double total = 0;
        for (Shape s : shapes) {
            total += s.area();   // calls Circle.area() or Rectangle.area() — chosen at RUNTIME
        }
        System.out.printf("Total area: %.2f%n", total); // 24.57
    }
}
```

This is **runtime polymorphism** (dynamic dispatch). The variable's type is `Shape`, but the JVM looks at the *actual object* and calls its override. Add a `Triangle` class tomorrow and the loop above works unchanged — that's the power.

Two flavors of polymorphism:

- **Overriding** (runtime): subclass replaces a parent method (shown above).
- **Overloading** (compile-time): same method name, different parameter lists — the compiler picks based on arguments.

```java
public class Calc {
    int add(int a, int b)        { return a + b; }       // overload 1
    double add(double a, double b) { return a + b; }     // overload 2
    int add(int a, int b, int c) { return a + b + c; }   // overload 3
}
```

#### Casting and `instanceof`

```java
public class Casting {
    public static void main(String[] args) {
        Shape s = new Circle(5);          // upcast (Circle → Shape): always safe, implicit

        // Pattern matching for instanceof (Java 16+) — check AND cast in one step
        if (s instanceof Circle c) {
            System.out.println("Radius via cast: works, area=" + c.area());
        }

        // Old style downcast — risky; ClassCastException if wrong
        if (s instanceof Rectangle) {
            Rectangle r = (Rectangle) s;  // would throw if s isn't actually a Rectangle
        }
    }
}
```

---

### Pillar 4 — ABSTRACTION: model the essential, hide the rest

Abstraction means exposing *what* something does while hiding *how*. You design with high-level concepts (`PaymentProcessor`, `Repository`) and defer the messy details to implementations. Java gives you two tools: **abstract classes** and **interfaces**.

```java
// Abstract class: a partial blueprint — cannot be instantiated directly
public abstract class Employee {
    protected String name;
    public Employee(String name) { this.name = name; }

    // Concrete method — shared by all employees
    public void clockIn() { System.out.println(name + " clocked in."); }

    // Abstract method — NO body. Every subclass MUST implement it.
    public abstract double calculatePay();
}
```

```java
public class SalariedEmployee extends Employee {
    private final double annualSalary;
    public SalariedEmployee(String name, double annualSalary) {
        super(name);
        this.annualSalary = annualSalary;
    }
    @Override public double calculatePay() { return annualSalary / 12; }
}

public class HourlyEmployee extends Employee {
    private final double rate, hours;
    public HourlyEmployee(String name, double rate, double hours) {
        super(name);
        this.rate = rate; this.hours = hours;
    }
    @Override public double calculatePay() { return rate * hours; }
}
```

```java
public class Payroll {
    public static void main(String[] args) {
        // Employee e = new Employee("X");  // COMPILE ERROR — abstract, can't instantiate
        Employee[] staff = {
            new SalariedEmployee("Ada", 120_000),
            new HourlyEmployee("Bob", 25, 160)
        };
        for (Employee e : staff) {
            e.clockIn();
            System.out.printf("%s pay: %.2f%n", e.name, e.calculatePay());
        }
    }
}
```

---

## IV. INTERFACES vs ABSTRACT CLASSES — THE BIG DECISION

This comes up constantly, in design and in interviews. Both define contracts; they differ in intent and capability.

An **interface** is a pure contract: "any class that implements me promises to provide these methods." A class can implement **many** interfaces (this is how Java gets multiple inheritance of *type*).

```java
public interface Drawable {
    void draw();                              // implicitly public abstract

    default void describe() {                 // default method (Java 8+) — optional override
        System.out.println("A drawable thing.");
    }

    static Drawable empty() {                 // static factory on the interface
        return () -> System.out.println("(nothing)");
    }
}

public interface Resizable {
    void resize(double factor);
}
```

```java
// A class can implement MULTIPLE interfaces — composition of capabilities
public class Icon implements Drawable, Resizable {
    private double size = 1.0;
    @Override public void draw()   { System.out.println("Drawing icon at size " + size); }
    @Override public void resize(double f) { size *= f; }
}
```

```java
public class App {
    public static void main(String[] args) {
        Icon icon = new Icon();
        icon.draw();
        icon.resize(2);
        icon.draw();
        icon.describe();     // inherited default method
    }
}
```

### The decision table

| Question | Abstract class | Interface |
|----------|----------------|-----------|
| Relationship | "is-a" (strong) | "can-do" / capability |
| How many can you have? | extend **one** | implement **many** |
| Instance fields (state) | ✅ yes | ❌ no (only `public static final` constants) |
| Constructors | ✅ yes | ❌ no |
| Method bodies | ✅ yes (concrete + abstract) | ✅ `default` & `static` methods (Java 8+); otherwise abstract |
| Access modifiers on methods | any | implicitly `public` |
| Primary purpose | share code among closely related types | define a contract many unrelated types can fulfill |

**Rule of thumb:**
- Reach for an **interface** by default — especially to define a capability (`Comparable`, `Runnable`, `Repository`). It keeps things flexible and a class can implement several.
- Reach for an **abstract class** when subclasses are genuinely related *and* you want to share **state or concrete implementation** among them.

```java
// Classic real-world interface: Comparable defines "natural ordering"
public class Version implements Comparable<Version> {
    final int major, minor;
    Version(int major, int minor) { this.major = major; this.minor = minor; }

    @Override public int compareTo(Version o) {
        if (this.major != o.major) return Integer.compare(this.major, o.major);
        return Integer.compare(this.minor, o.minor);
    }
    @Override public String toString() { return major + "." + minor; }

    public static void main(String[] args) {
        var list = new java.util.ArrayList<>(java.util.List.of(
            new Version(2, 1), new Version(1, 5), new Version(2, 0)));
        java.util.Collections.sort(list);   // uses compareTo
        System.out.println(list);            // [1.5, 2.0, 2.1]
    }
}
```

---

## V. `equals()`, `hashCode()`, AND `toString()` — THE OBJECT CONTRACT

Every class inherits these from `Object`. The defaults are often wrong for your needs, so you override them. Getting `equals`/`hashCode` right is **mandatory** if your objects go into a `HashSet` or `HashMap` (file 03).

```java
import java.util.Objects;

public class User {
    private final String email;
    private final String name;

    public User(String email, String name) { this.email = email; this.name = name; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;                       // same reference, fast path
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return email.equals(user.email);                  // two users are equal iff same email
    }

    @Override
    public int hashCode() {
        return Objects.hash(email);   // MUST be consistent with equals: equal objects → equal hash
    }

    @Override
    public String toString() {
        return "User{email='" + email + "', name='" + name + "'}";
    }
}
```

> **The cardinal rule:** if you override `equals()`, you **must** override `hashCode()`, and they must use the same fields. Equal objects must have equal hash codes. Violate this and your objects "disappear" in hash-based collections — they're stored under one hash and looked up under another. (A `record` does all of this correctly for free.)

---

## VI. `static` — CLASS-LEVEL MEMBERS

`static` members belong to the *class*, not to any instance. There's exactly one copy, shared by all.

```java
public class Counter {
    private static int totalCreated = 0;   // shared across ALL Counter objects
    private final int id;

    public Counter() {
        totalCreated++;          // increment the shared counter
        this.id = totalCreated;  // each instance gets its own id
    }

    public static int getTotalCreated() { return totalCreated; } // static method
    public int getId() { return id; }

    public static void main(String[] args) {
        new Counter(); new Counter(); Counter c = new Counter();
        System.out.println(c.getId());                 // 3
        System.out.println(Counter.getTotalCreated()); // 3 — called on the CLASS, not an instance
    }
}
```

> **Gotcha — static methods can't use instance state.** A `static` method has no `this`, so it cannot read non-static fields directly. `main` is static, which is exactly why helper methods called from `main` are often static too.

---

## VII. A COHESIVE EXAMPLE — A SMALL DOMAIN MODEL

Pulling the pillars together into something that looks like real code:

```java
import java.util.ArrayList;
import java.util.List;

// Abstraction: a contract for anything that can be charged
interface Billable {
    double monthlyCost();
}

// Encapsulation + base behavior
abstract class Subscription implements Billable {
    private final String customer;     // private state
    protected Subscription(String customer) { this.customer = customer; }
    public String getCustomer() { return customer; }
    public abstract String tier();     // each subclass names its tier
}

// Inheritance + polymorphism
class BasicPlan extends Subscription {
    BasicPlan(String customer) { super(customer); }
    @Override public double monthlyCost() { return 9.99; }
    @Override public String tier() { return "Basic"; }
}

class ProPlan extends Subscription {
    private final int seats;
    ProPlan(String customer, int seats) { super(customer); this.seats = seats; }
    @Override public double monthlyCost() { return 29.99 + seats * 5; }
    @Override public String tier() { return "Pro (" + seats + " seats)"; }
}

public class BillingSystem {
    public static void main(String[] args) {
        List<Subscription> subs = new ArrayList<>();
        subs.add(new BasicPlan("Ada"));
        subs.add(new ProPlan("Bob", 3));

        double revenue = 0;
        for (Subscription s : subs) {            // polymorphism in action
            System.out.printf("%s — %s — $%.2f/mo%n", s.getCustomer(), s.tier(), s.monthlyCost());
            revenue += s.monthlyCost();
        }
        System.out.printf("Total MRR: $%.2f%n", revenue);
    }
}
```

This tiny system is **open for extension, closed for modification**: add a `EnterprisePlan` and the billing loop needs zero changes. That property — the Open/Closed Principle — is a direct payoff of polymorphism and abstraction.

---

## VIII. COMMON PITFALLS

| Pitfall | Why it bites | Fix |
|---------|--------------|-----|
| Public fields | Anyone can corrupt state | `private` fields + methods |
| Overriding `equals` but not `hashCode` | Objects vanish in HashMap/HashSet | Override both, same fields (or use `record`) |
| Deep inheritance chains | Fragile, hard to change | Favor composition (has-a) |
| Forgetting `@Override` | Silent typo creates a new method | Always annotate overrides |
| Calling overridable methods in a constructor | Subclass override runs before its fields are set | Don't; or make such methods `final`/`private` |
| Confusing overloading and overriding | Wrong method runs | Overload = compile-time by params; override = runtime by type |
| Instantiating abstract class / interface | Compile error | Instantiate a concrete subclass/impl |
| Mutable objects shared via getters | Caller mutates your internals | Return copies or immutable views |

---

## 🧠 KEY TAKEAWAYS

- A **class** is a blueprint; an **object** is an instance with its own state. **Constructors** guarantee objects start valid; `this` and `super` connect a class to itself and its parent.
- **Encapsulation:** make fields `private`, expose controlled methods, and your object can never enter an invalid state. Default everything to `private`.
- **Inheritance** models "is-a" and shares behavior, but **favor composition (has-a)** to avoid fragile hierarchies. Java allows extending only one class.
- **Polymorphism** lets one reference type drive many concrete behaviors chosen at runtime — the key to extensible, open/closed code.
- **Abstraction** via abstract classes and interfaces hides *how* behind *what*. Prefer **interfaces** for capabilities (implement many); use **abstract classes** to share state/code among related types.
- Override **`equals`/`hashCode` together** or your objects break in hash collections. `record`s give you correct data classes for free.

---

**Prev:** [`02-Java-Fundamentals.md`](./02-Java-Fundamentals.md) · **Next:** [`04-Collections-Framework.md`](./04-Collections-Framework.md) · **Index:** [`01-Getting-Started.md`](./01-Getting-Started.md)
