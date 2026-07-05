# 🔷 Polymorphism and Generics

> *"Write the algorithm once; run it on every type it makes sense for."*

**Polymorphism** (Greek: "many forms") means a single piece of code operating over multiple types. It's how we avoid writing `sortInts`, `sortStrings`, `sortFloats` separately. There are three distinct kinds — confusing them is a common source of muddled thinking.

---

## I. THE THREE KINDS OF POLYMORPHISM

### 1. Parametric polymorphism (generics)
The *same* code works for *any* type, uniformly, without knowing which. The type is a parameter.

```rust
fn first<T>(v: &Vec<T>) -> &T { &v[0] }   // works for Vec<i32>, Vec<String>, anything
```
```haskell
length :: [a] -> Int    -- 'a' is any type; length doesn't care what's in the list
```
```java
class Box<T> { private T value; T get() { return value; } }
```

The function is oblivious to `T` — it treats it as an opaque black box. This is the purest, safest form: "I don't care what type this is, I just move it around."

### 2. Ad-hoc polymorphism (overloading / type classes)
*Different* code for *different* types, selected by type. Same name, type-specific behavior.

```java
int    add(int a, int b)       { return a + b; }
String add(String a, String b) { return a + b; }   // overloading: same name, different impls
```
```haskell
class Show a where            -- a type class: "types that can be shown as text"
  show :: a -> String
instance Show Int  where show n = ...   -- Int's own implementation
instance Show Bool where show b = ...   -- Bool's own implementation
```

Type classes (Haskell), traits (Rust), and interfaces (Java/Go) are principled ad-hoc polymorphism: "any type that implements `Show` can be shown, each in its own way."

### 3. Subtype polymorphism (inheritance/interfaces)
Code written for a *supertype* works for any *subtype*. The OOP kind (see [`../02-PARADIGMS/02-Object-Oriented.md`](../02-PARADIGMS/02-Object-Oriented.md)).

```java
void render(Shape s) { s.draw(); }   // works for Circle, Square — any Shape subtype
```

---

## II. TWO WAYS TO IMPLEMENT GENERICS (a deep tradeoff)

When you write `Vec<T>`, how does the compiler make it work for every `T`? Two strategies with opposite tradeoffs:

### Monomorphization (C++, Rust)
The compiler generates a **separate specialized copy** for each concrete type used. `Vec<i32>` and `Vec<String>` become two distinct compiled types.
- ✅ **Zero runtime cost** — each copy is as fast as hand-written type-specific code; fully inlinable.
- ❌ **Code bloat** — bigger binaries; slower compiles (many copies).

### Type erasure (Java, Haskell)
Generic type info is **erased** after checking; one implementation handles all types, using boxing/pointers.
- ✅ **Small binaries, fast compiles** — one copy.
- ❌ **Runtime cost** — boxing, indirection; and lost type info (`List<Integer>` and `List<String>` are the same class at runtime — Java can't do `new T()` or `instanceof List<String>`).

This single decision explains many language quirks: why Rust generics are blazing fast but compile slowly, and why Java generics can't create arrays of `T` or inspect their type parameter at runtime.

---

## III. BOUNDED POLYMORPHISM — CONSTRAINTS ON TYPE PARAMETERS

Pure parametric polymorphism can't *do* anything to a `T` (it's opaque). Often you need to require capabilities:

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {   // T must be comparable
    let mut max = &list[0];
    for x in list { if x > max { max = x; } }    // '>' is allowed because T: PartialOrd
    max
}
```
```haskell
maximum :: Ord a => [a] -> a    -- 'Ord a' constrains 'a' to orderable types
```
```java
<T extends Comparable<T>> T max(List<T> list) { ... }
```

The **bound** (`T: PartialOrd`, `Ord a`, `extends Comparable`) says "T can be any type *that supports these operations*." This marries parametric polymorphism (works for many types) with ad-hoc (uses type-specific operations) — the most useful pattern in practice.

---

## IV. VARIANCE — THE SUBTLE PART

If `Cat` is a subtype of `Animal`, is `List<Cat>` a subtype of `List<Animal>`? The answer — **variance** — is subtle and a frequent source of bugs:

- **Covariant** — `List<Cat>` *is* a `List<Animal>` (safe for read-only). If you can only *take out*, it's fine.
- **Contravariant** — flips: a `Consumer<Animal>` can be used where a `Consumer<Cat>` is needed (safe for write-only).
- **Invariant** — no subtyping relationship (safe for read-write). Mutable `List<Cat>` is *not* a `List<Animal>`, because you could then insert a `Dog` into it.

```java
List<Cat> cats = ...;
List<Animal> animals = cats;   // ILLEGAL in Java (lists are invariant) — good!
// if it were allowed: animals.add(new Dog());  → cats now contains a Dog. Disaster.
```

Java uses wildcards (`? extends`, `? super`) and Scala/Kotlin use `out`/`in` annotations to control variance. The rule of thumb: **producers are covariant (`out`), consumers are contravariant (`in`), mutable containers are invariant.**

---

## V. THE PRAGMATIC SUMMARY

- Use **generics (parametric)** whenever your code doesn't care about the specific type — collections, containers, plumbing. Safest and most reusable.
- Use **traits/interfaces/type classes (ad-hoc)** to require capabilities (`Comparable`, `Serializable`, `Iterator`).
- Understand your language's **implementation** (monomorphization vs erasure) — it explains performance and limitations.
- Respect **variance** — it's why "obviously fine" subtyping is sometimes rejected (and rightly so).

---

## 📌 Key Takeaways
- Three kinds: **parametric** (generics, type-agnostic), **ad-hoc** (overloading/traits, type-specific), **subtype** (inheritance).
- Generics are implemented via **monomorphization** (fast, bloated — Rust/C++) or **type erasure** (small, boxed, lossy — Java).
- **Bounded polymorphism** (`T: Ord`) lets generic code use type-specific operations — the most practical pattern.
- **Variance** governs whether `List<Cat>` is a `List<Animal>`: producers covariant, consumers contravariant, mutable containers invariant.

**Next:** [`04-Advanced-Types.md`](./04-Advanced-Types.md)
