# 🦀 Ownership and Borrowing

> *"What if the compiler could prove your memory is safe — with no garbage collector and no runtime cost at all?"*

Rust's ownership system is the most important language innovation of the last two decades: **memory safety without garbage collection**, enforced entirely at compile time. This file explains how — the concepts generalize far beyond Rust.

---

## I. THE THREE RULES OF OWNERSHIP

Rust's model rests on three deceptively simple rules:

1. **Each value has exactly one owner** (a variable).
2. **There can be only one owner at a time.**
3. **When the owner goes out of scope, the value is dropped (freed).**

```rust
{
    let s = String::from("hello");   // s OWNS the heap string
    // ... use s ...
}   // s goes out of scope → the string is freed HERE, automatically, deterministically
```

No `free`, no garbage collector, no reference counting. The compiler inserts the cleanup at exactly the right spot because it *knows* when the owner dies. This is RAII (Resource Acquisition Is Initialization), enforced by the type system.

---

## II. MOVE SEMANTICS — TRANSFERRING OWNERSHIP

Assigning or passing a value **moves** ownership. The old binding becomes invalid — so two variables can never both think they own (and must free) the same data.

```rust
let s1 = String::from("hi");
let s2 = s1;          // ownership MOVES from s1 to s2
println!("{}", s1);   // ❌ COMPILE ERROR: s1 was moved, it's no longer valid
```

This single rule *statically eliminates* the double-free bug: since only one owner exists, only one `free` ever happens. It also prevents use-after-free: you can't use `s1` after moving it away.

(Small `Copy` types like integers are copied instead of moved — copying an `i32` is trivial and has no heap resource to double-free.)

---

## III. BORROWING — ACCESS WITHOUT OWNERSHIP

Moving everything would be painful — you'd lose access constantly. So Rust lets you **borrow** a reference without taking ownership:

```rust
fn len(s: &String) -> usize { s.len() }   // borrows s, doesn't own it

let s = String::from("hello");
let n = len(&s);      // lend s to len()
println!("{}", s);    // ✅ still valid — len() only borrowed it
```

Borrowing follows **the borrowing rules**, enforced at compile time:

> At any given time, you may have **either**
> - **any number of immutable references** (`&T`), **or**
> - **exactly one mutable reference** (`&mut T`)
> — **but not both.**

```rust
let mut v = vec![1, 2, 3];
let r1 = &v;          // immutable borrow
let r2 = &v;          // another immutable borrow — fine, both can read
let r3 = &mut v;      // ❌ ERROR: can't borrow mutably while immutable borrows exist
```

This is "shared XOR mutable": data can be *shared* (many readers) or *mutable* (one writer), never both at once.

---

## IV. WHY THIS IS PROFOUND: DATA RACES BECOME IMPOSSIBLE

The borrowing rules don't just prevent memory bugs — they prevent **data races** *at compile time*. A data race requires: two threads, accessing the same data, at least one writing, without synchronization. But "shared XOR mutable" makes "two accessors where one writes" *impossible to even express* without explicit synchronization types.

This is Rust's famous **"fearless concurrency"**: if concurrent code compiles, it's free of data races. The same rules that manage single-threaded memory also guarantee thread safety. One elegant idea solves two of the hardest problems in systems programming simultaneously.

---

## V. LIFETIMES — PROVING REFERENCES DON'T DANGLE

The last piece: how does the compiler ensure a borrowed reference never outlives the data it points to? **Lifetimes** — annotations (usually inferred) that let the compiler prove a reference is valid for its entire use.

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}   // the 'a says: the returned reference lives as long as BOTH inputs
```

The **borrow checker** uses lifetimes to reject any program where a reference could outlive its referent (a dangling pointer). This is the source of Rust's learning curve — "fighting the borrow checker" — but what you're really doing is *proving your program is memory-safe*, and once it compiles, it is.

```rust
fn dangle() -> &String {
    let s = String::from("boom");
    &s      // ❌ ERROR: returns a reference to s, but s is dropped when the function ends
}
```
In C, this compiles and returns a dangling pointer (undefined behavior). In Rust, it simply won't build.

---

## VI. THE BROADER LESSON

Ownership is an **affine type system** (values used at most once — see [`../03-TYPE-SYSTEMS/04-Advanced-Types.md`](../03-TYPE-SYSTEMS/04-Advanced-Types.md)) applied to memory. Its impact:
- **Memory safety + thread safety** with **zero runtime cost** — no GC, no pauses, C-level performance.
- The ideas are spreading: C++ smart pointers and move semantics, Swift's ownership work, and static analyzers all borrow from this model.
- The cost is real: a steeper learning curve and some patterns (doubly-linked lists, graphs) that fight the model and need escape hatches (`Rc`, `RefCell`, `unsafe`).

Rust proved you don't have to choose between safety and performance — you can have both, paid for at *compile time* with programmer effort rather than at *run time* with a collector. That's why it's the first language in decades to seriously challenge C/C++ for systems programming, and why the Linux kernel, Windows, and Android now include Rust.

---

## 📌 Key Takeaways
- **Ownership**: one owner per value; value freed deterministically when the owner leaves scope (no GC, no `free`).
- **Move semantics** eliminate double-free and use-after-free at compile time.
- **Borrowing** allows access without ownership under "shared XOR mutable": many readers OR one writer, never both.
- Those rules make **data races impossible** to compile → "fearless concurrency."
- **Lifetimes** + the borrow checker prove references never dangle — the source of both Rust's difficulty and its safety.
- Ownership = affine typing on memory → safety + speed with zero runtime cost.

**Next:** [`../05-COMPILERS-AND-INTERPRETERS/00-Index.md`](../05-COMPILERS-AND-INTERPRETERS/00-Index.md)
