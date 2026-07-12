# 🪄 Macros, Reflection, and DSLs

> *"The ultimate abstraction is a language that lets you grow the language."*

---

## I. MACROS — CODE THAT GENERATES CODE AT COMPILE TIME

A **macro** transforms source code *before* compilation. There are two very different kinds:

### Textual macros (crude) — C's preprocessor
```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
MAX(x, y)   // literally text-substituted before compilation
```
Simple string substitution, with no understanding of the language — hence the infamous footguns (`MAX(i++, j++)` evaluates arguments twice; missing parens break precedence). Powerful but dangerous.

### Syntactic (hygienic) macros — Lisp's superpower
In Lisp, **code is data** (both are lists — "homoiconicity"). Macros operate on the *syntax tree*, not text, so they're structurally aware and **hygienic** (they don't accidentally capture variables):
```lisp
(defmacro unless (condition body)
  `(if (not ,condition) ,body))     ; generates an if-expression
(unless (> x 10) (print "small"))   ; expands to (if (not (> x 10)) (print "small"))
```
Lisp macros are so powerful you can add new control structures, new syntax — effectively *extend the language itself*. This is why Lispers say Lisp is "programmable programming."

### Modern hygienic macros — Rust
```rust
println!("{} + {} = {}", a, b, a + b);   // println! is a macro, checked at compile time
#[derive(Debug, Clone)]                   // derive macros GENERATE trait implementations
struct Point { x: i32, y: i32 }
```
Rust's macros (`macro_rules!` and procedural macros) are hygienic and operate on token streams / the AST — generating boilerplate (serialization, trait impls) safely at compile time with zero runtime cost.

---

## II. REFLECTION — INSPECTING PROGRAMS AT RUN TIME

**Reflection** lets a program examine and modify its own structure *while running* — inspecting types, fields, and methods it didn't know about at compile time.

```java
// Java reflection: discover and invoke at runtime
Class<?> c = obj.getClass();
for (Field f : c.getDeclaredFields())
    System.out.println(f.getName() + " = " + f.get(obj));
Method m = c.getMethod("save");
m.invoke(obj);   // call a method chosen by name at runtime
```
```python
# Python's reflection is pervasive and easy
for name in dir(obj):
    print(name, getattr(obj, name))
```

Reflection powers the "magic" in frameworks:
- **Serialization** (JSON/XML) — inspect an object's fields to convert it automatically.
- **ORMs** (Hibernate, Django) — map class fields to database columns by inspection.
- **Dependency injection** (Spring) — discover and wire up components by their types/annotations.
- **Test frameworks** — find and run all methods named `test*` or annotated `@Test`.

Cost: reflection is **slower** (bypasses compile-time optimization), **less safe** (errors surface at runtime, not compile time), and defeats some static analysis. Use it where flexibility genuinely requires it.

---

## III. eval — THE ULTIMATE (AND DANGEROUS) META TOOL

Dynamic languages can execute strings as code at runtime:
```python
eval("2 + 3 * 4")          # 14
exec("x = 10")             # runs arbitrary code
```
Maximally flexible — and a **massive security hole** if fed untrusted input (arbitrary code execution). "`eval` is evil" is the standard warning. Legitimate uses (REPLs, template engines, config DSLs) exist but are narrow; never `eval` user input.

---

## IV. DOMAIN-SPECIFIC LANGUAGES (DSLs)

A **DSL** is a small language specialized for one domain — the ultimate application of metaprogramming. Two kinds:

### External DSLs — their own syntax, parsed by a tool
SQL, regex, HTML/CSS, Terraform, GraphQL, Makefiles. You write a real parser (see [`../05-COMPILERS-AND-INTERPRETERS/01-Lexing-and-Parsing.md`](../05-COMPILERS-AND-INTERPRETERS/01-Lexing-and-Parsing.md)).

### Internal (embedded) DSLs — a fluent API inside a host language
Built using the host language's features (macros, operator overloading, builders) so domain code reads naturally:
```ruby
# Ruby (RSpec) — reads like English, but it's just Ruby method calls
describe "Calculator" do
  it "adds numbers" do
    expect(add(2, 3)).to eq(5)
  end
end
```
```python
# Python (SQLAlchemy) — a query DSL embedded in Python
users.select().where(users.c.age > 18).order_by(users.c.name)
```
Internal DSLs leverage metaprogramming (method_missing, operator overloading, macros, builders) to make library code feel like a purpose-built language. React's JSX, testing frameworks, ORMs, and build tools are all DSLs.

---

## V. THE POWER/DANGER BALANCE

Metaprogramming is a superpower with a sharp edge:

**When it shines:** eliminating boilerplate (derive/codegen), building expressive DSLs, framework infrastructure (DI, ORMs, serialization), and adapting to data whose shape is unknown until runtime.

**When it hurts:** "magic" that's hard to debug (where did this method come from?), degraded performance (reflection/eval), weakened static analysis and tooling, and security holes (`eval`). Overused metaprogramming produces codebases where nothing is where it looks and errors are inscrutable.

**The rule:** prefer **compile-time** metaprogramming (macros, generics, codegen) over **run-time** (reflection, eval) when you can — it keeps safety and performance. And use the least powerful tool that solves the problem: a plain function beats a macro; a macro beats reflection; reflection beats `eval`.

---

## 📌 Key Takeaways
- **Macros** transform code before compilation: crude/textual (C preprocessor) vs hygienic/syntactic (Lisp, Rust) that safely extend the language.
- **Reflection** inspects/modifies program structure at runtime — powering serialization, ORMs, DI, and test frameworks, at a performance/safety cost.
- **`eval`** executes strings as code — maximally flexible, maximally dangerous (never on untrusted input).
- **DSLs** (external like SQL/regex; internal like RSpec/SQLAlchemy) are metaprogramming's ultimate application — languages tailored to a domain.
- Prefer **compile-time over run-time** metaprogramming, and the **least powerful tool** that works.

**Next:** [`../10-LANGUAGE-DESIGN/00-Index.md`](../10-LANGUAGE-DESIGN/00-Index.md)
