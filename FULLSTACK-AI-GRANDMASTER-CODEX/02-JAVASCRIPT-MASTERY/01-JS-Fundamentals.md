# 🧱 JavaScript Fundamentals

> *"You can't reason about a program until you can reason about a single value."*

This is the bedrock: how JavaScript stores values, names them, combines them, and — crucially — how it *coerces* them when you least expect it. Master this and the famous "JavaScript is weird" moments stop being mysteries and become predictable rules.

---

## I. WHAT IS JAVASCRIPT?

JavaScript is a **dynamically typed**, **interpreted (then JIT-compiled)**, **single-threaded**, **multi-paradigm** language. Unpacking that:

- **Dynamically typed** — a variable's type is decided at runtime, not declared up front. The same variable can hold a number, then a string.
- **JIT-compiled** — engines like V8 (Chrome, Node) compile hot code paths to machine code on the fly. It's fast.
- **Single-threaded** — one call stack, one thing at a time (concurrency comes from the event loop — see file 05).
- **Multi-paradigm** — it supports functional, object-oriented, and imperative styles.

```js
let x = 42;        // x is a number now
x = "hello";       // ...and a string now. Totally legal.
x = [1, 2, 3];     // ...and an array now.
console.log(typeof x); // "object" (arrays are objects)
```

> ⚠️ This flexibility is power *and* footgun. TypeScript (section 03) exists largely to put guardrails on it.

---

## II. VARIABLES: `let`, `const`, `var`

There are three ways to declare a variable. In modern code you use `const` by default, `let` when you must reassign, and `var` essentially never.

### `const` — a binding that can't be reassigned
```js
const PI = 3.14159;
PI = 3;            // ❌ TypeError: Assignment to constant variable.

const user = { name: "Ada" };
user.name = "Grace";   // ✅ ALLOWED — the object is mutable, the *binding* is not
user = {};             // ❌ TypeError — you can't rebind `user`
```
`const` means **the variable name always points at the same value**. If that value is an object or array, its *contents* can still change. `const` is about the binding, not deep immutability.

### `let` — a reassignable binding
```js
let count = 0;
count = count + 1;   // ✅ fine
count += 1;          // ✅ fine
```

### `var` — the legacy declaration (avoid)
`var` behaves differently in two important ways: it is **function-scoped** (not block-scoped) and it is **hoisted and initialized to `undefined`**.

```js
function demo() {
  if (true) {
    var a = 1;   // function-scoped: escapes the block
    let b = 2;   // block-scoped: trapped in the if
  }
  console.log(a); // 1   ← var leaked out
  console.log(b); // ❌ ReferenceError: b is not defined
}
demo();
```

### The scoping difference, visualized
```js
// var: one shared binding across the loop (classic bug)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log("var:", i), 10);
}
// prints: var: 3, var: 3, var: 3

// let: a fresh binding each iteration (what you actually want)
for (let j = 0; j < 3; j++) {
  setTimeout(() => console.log("let:", j), 10);
}
// prints: let: 0, let: 1, let: 2
```
This single example is one of the most common interview questions in existence. The reason it works is closures — covered in file 02. For now, internalize: **`let` gives each loop iteration its own variable; `var` shares one.**

### The rule of thumb
| Use | When |
|-----|------|
| `const` | Default. 90% of declarations. |
| `let` | When you genuinely reassign (counters, accumulators, loop indices). |
| `var` | Never, in new code. Know it only to read old code. |

---

## III. THE DATA TYPES

JavaScript has **7 primitive types** and **1 object type**.

### Primitives (immutable, copied by value)
```js
const num    = 42;            // number  (one type for ints AND floats)
const big    = 9007199254740993n; // bigint  (arbitrary-precision integers, note the n)
const str    = "hello";       // string
const bool   = true;          // boolean
const nope   = undefined;     // undefined (a variable that hasn't been assigned)
const empty  = null;          // null      (intentional "no value")
const sym    = Symbol("id");  // symbol    (unique identifier)
```

### Objects (mutable, copied by reference)
```js
const obj   = { a: 1 };        // object
const arr   = [1, 2, 3];       // array (a kind of object)
const fn    = () => {};        // function (a callable object)
const date  = new Date();      // also objects
```

### `typeof` — your inspection tool
```js
typeof 42            // "number"
typeof 42n           // "bigint"
typeof "hi"          // "string"
typeof true          // "boolean"
typeof undefined     // "undefined"
typeof Symbol()      // "symbol"
typeof {}            // "object"
typeof []            // "object"   ← arrays report as object!
typeof null          // "object"   ← the famous historical bug
typeof function(){}  // "function" ← functions get their own label
```

> 🐛 **`typeof null === "object"`** is a bug from 1995 that can never be fixed without breaking the web. To check for null, compare directly: `value === null`. To check for arrays, use `Array.isArray(value)`.

### Number: one type, some sharp edges
JavaScript numbers are 64-bit IEEE-754 floats. There is no separate integer type (until `bigint`).
```js
0.1 + 0.2            // 0.30000000000000004  ← floating point, not a JS bug
0.1 + 0.2 === 0.3    // false
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON  // true ← the correct way to compare

Number.MAX_SAFE_INTEGER  // 9007199254740991 (2^53 - 1)
9007199254740991 + 1     // 9007199254740992
9007199254740991 + 2     // 9007199254740992  ← precision lost! use bigint

10 / 0               // Infinity
-10 / 0              // -Infinity
0 / 0                // NaN  ("Not a Number")
typeof NaN           // "number"  (yes, really)
NaN === NaN          // false ← NaN is not equal to itself
Number.isNaN(NaN)    // true  ← the reliable check
```

### `null` vs `undefined`
Both mean "no value," but with different intent:
- **`undefined`** — the system's "nothing here yet." A declared-but-unassigned variable, a missing object property, a function with no `return`.
- **`null`** — *your* "nothing here, on purpose." You assign it deliberately.

```js
let a;
console.log(a);              // undefined — never assigned

const obj = {};
console.log(obj.missing);   // undefined — no such key

function f() {}
console.log(f());           // undefined — no return

let chosen = null;          // "deliberately empty for now"
```

---

## IV. OPERATORS

### Arithmetic
```js
5 + 2    // 7
5 - 2    // 3
5 * 2    // 10
5 / 2    // 2.5   (no integer division — always float)
5 % 2    // 1     (remainder / modulo)
5 ** 2   // 25    (exponentiation)

// Increment / decrement
let n = 5;
n++;     // n is now 6 (returns old value 5 if used in expression)
++n;     // n is now 7 (returns new value 7)
```

### String concatenation with `+` (and the coercion trap)
```js
"a" + "b"      // "ab"
"1" + 1        // "11"   ← number coerced to string
1 + "1"        // "11"   ← same
1 + 1 + "1"    // "21"   ← left-to-right: (1+1) then +"1"
"1" + 1 + 1    // "111"  ← once a string, stays a string
```

### Comparison: `==` vs `===` (THE big one)
```js
// === : strict equality — NO type coercion. Use this.
1 === 1        // true
1 === "1"      // false  (different types)
null === undefined  // false

// == : loose equality — coerces types first. Avoid this.
1 == "1"       // true   ← string coerced to number
0 == false     // true
"" == false    // true
null == undefined   // true   (the one useful case)
[] == false    // true   ← 🤯 array coerces to "" coerces to 0
```

> ✅ **Rule: always use `===` and `!==`.** The only common exception is `value == null`, which neatly checks "is it `null` OR `undefined`" in one shot.

### Logical operators (and their return values)
```js
true && false    // false
true || false    // true
!true            // false

// CRUCIAL: && and || return one of the OPERANDS, not a boolean
"a" && "b"       // "b"   (&& returns the last truthy, or first falsy)
"" && "b"        // ""    (short-circuits at the falsy value)
"a" || "b"       // "a"   (|| returns the first truthy)
"" || "default"  // "default"  ← classic "fallback value" idiom
0 || "fallback"  // "fallback"
```

This is why you see `const name = userInput || "Anonymous";` everywhere. (But see the nullish coalescing operator `??` in file 06 — it's often the safer choice.)

### Ternary — inline if/else
```js
const age = 20;
const status = age >= 18 ? "adult" : "minor";  // "adult"
```

---

## V. TYPE COERCION — THE RULES BEHIND THE WEIRDNESS

Coercion is JavaScript automatically converting a value from one type to another. There are two kinds: **implicit** (the engine does it) and **explicit** (you do it). Understanding the implicit rules removes 90% of "WAT" moments.

### Explicit conversion (do this on purpose)
```js
// To number
Number("42")     // 42
Number("42px")   // NaN
Number("")       // 0
Number(true)     // 1
Number(null)     // 0
Number(undefined)// NaN
parseInt("42px", 10) // 42  (parses leading digits, base 10)
parseFloat("3.14abc")// 3.14
+"42"            // 42   (unary plus = quick Number())

// To string
String(42)       // "42"
String(null)     // "null"
String([1,2,3])  // "1,2,3"
(42).toString()  // "42"
`${42}`          // "42"  (template literal)

// To boolean
Boolean(1)       // true
Boolean(0)       // false
!!"hello"        // true  (double-bang = quick Boolean())
```

### Implicit coercion (the engine doing it for you)
```js
// + with a string => string concatenation
1 + "2"          // "12"

// other math operators => numeric coercion
"5" - 2          // 3
"5" * "2"        // 10
"abc" - 1        // NaN

// comparison with == triggers coercion
"5" == 5         // true
```

### The mental model for `+`
> If **either** operand of `+` is a string, JavaScript does string concatenation. Otherwise it does numeric addition. Every other arithmetic operator (`-`, `*`, `/`, `%`) always coerces to number.

---

## VI. TRUTHY AND FALSY

In any boolean context (`if`, `while`, `&&`, `||`, ternary), JavaScript coerces the value to a boolean. There are exactly **8 falsy values**. Memorize them — everything else is truthy.

### The complete falsy list
```js
false
0
-0
0n        // bigint zero
""        // empty string (also '' and ``)
null
undefined
NaN
```

### Everything else is truthy — including these surprises
```js
if ("false") {}   // runs! non-empty string is truthy
if ("0") {}       // runs! it's a non-empty string
if ([]) {}        // runs! empty array is truthy (it's an object)
if ({}) {}        // runs! empty object is truthy
if (" ") {}       // runs! a space is a non-empty string
if (-1) {}        // runs! only ZERO is falsy, not negatives
if (Infinity) {}  // runs!
```

### Practical use
```js
const username = "";
if (username) {
  console.log(`Hello, ${username}`);
} else {
  console.log("Please enter a name"); // ← this runs, "" is falsy
}

// Guarding against missing values
function greet(name) {
  name = name || "stranger";   // if name is falsy, use default
  return `Hello, ${name}`;
}
greet();        // "Hello, stranger"
greet("Ada");   // "Hello, Ada"
greet("");      // "Hello, stranger"  ← careful: "" is falsy!
greet(0);       // "Hello, stranger"  ← 0 is falsy too!
```

> ⚠️ The `||` fallback trips people up when `0` or `""` are *valid* values. For "only fall back on null/undefined," use `??` (nullish coalescing, file 06): `name ?? "stranger"`.

---

## VII. COMMON PITFALLS & GOTCHAS

**1. Comparing with `==` instead of `===`**
```js
if (x == null) { /* OK idiom: catches null AND undefined */ }
if (x == 0)    { /* BUG MAGNET: "" == 0, [] == 0, false == 0 all true */ }
```

**2. Thinking `const` means immutable**
```js
const arr = [1, 2, 3];
arr.push(4);     // ✅ works — mutating contents is fine
arr = [];        // ❌ error — rebinding is not
// For real immutability: Object.freeze(arr)
```

**3. Floating-point equality**
```js
if (total === 0.3) {}  // may never be true if total = 0.1 + 0.2
// Compare with tolerance, or work in integer cents.
```

**4. `NaN` comparisons**
```js
if (result === NaN) {}        // ❌ always false
if (Number.isNaN(result)) {}  // ✅ correct
```

**5. Number precision with large integers**
```js
const id = 9007199254740993;   // silently becomes ...992
const id2 = 9007199254740993n; // ✅ use bigint for IDs beyond 2^53
```

**6. Implicit string concatenation in math**
```js
const a = "5";
const total = a + 3;   // "53" not 8 — coerce first: Number(a) + 3
```

---

## VIII. KEY TAKEAWAYS

- JavaScript is **dynamically typed**: variables hold any type, decided at runtime.
- **`const` by default, `let` when you reassign, never `var`.** `const` blocks rebinding, not mutation.
- There are **7 primitives** (number, bigint, string, boolean, undefined, null, symbol) + **objects** (which include arrays and functions).
- `typeof null` is `"object"` (a permanent bug); use `=== null` and `Array.isArray()`.
- Numbers are 64-bit floats: `0.1 + 0.2 !== 0.3`, and integers above `2^53` lose precision (use `bigint`).
- **Always use `===`/`!==`.** The lone exception is `x == null` to catch null+undefined together.
- `&&` and `||` **return operands, not booleans**, and short-circuit — the basis of the `x || default` idiom.
- There are exactly **8 falsy values**: `false, 0, -0, 0n, "", null, undefined, NaN`. Everything else (including `[]`, `{}`, `"0"`, `"false"`) is truthy.
- Coercion rule for `+`: if either side is a string, it concatenates; every other math operator coerces to number.

---

**← Prev:** [`00-Index.md`](./00-Index.md) | **→ Next:** [`02-Functions-And-Scope.md`](./02-Functions-And-Scope.md) | **Index:** [`00-Index.md`](./00-Index.md)
