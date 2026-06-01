# 🔧 Functions, Scope & Closures

> *"A closure is a function that remembers where it was born."*

Functions are the heart of JavaScript — it is, after all, a language where functions are *values* you can pass around, return, and store. This file covers how to define them, how scope decides what they can see, why hoisting sometimes lets you call them before they're written, and the single most important concept in the language: **closures ⭐**.

---

## I. FUNCTIONS ARE FIRST-CLASS VALUES

In JavaScript, a function is just another value. You can assign it to a variable, pass it as an argument, return it from another function, and store it in arrays or objects. This is what makes functional patterns (file 08) possible.

```js
// Store a function in a variable
const greet = function (name) { return `Hi, ${name}`; };

// Pass a function as an argument (a "callback")
[1, 2, 3].forEach(function (n) { console.log(n); });

// Return a function from a function
function multiplier(factor) {
  return function (x) { return x * factor; };
}
const double = multiplier(2);
console.log(double(5)); // 10

// Store functions in a data structure
const ops = {
  add: (a, b) => a + b,
  sub: (a, b) => a - b,
};
console.log(ops.add(2, 3)); // 5
```

---

## II. WAYS TO DEFINE A FUNCTION

### Function declaration
```js
function add(a, b) {
  return a + b;
}
```
- Has a name.
- Is **hoisted** (you can call it before its definition — see section IV).

### Function expression
```js
const add = function (a, b) {
  return a + b;
};
```
- Assigned to a variable.
- **Not** hoisted as a callable — the variable follows normal declaration rules.

### Named function expression (useful for recursion + stack traces)
```js
const factorial = function fac(n) {
  return n <= 1 ? 1 : n * fac(n - 1); // can call itself by inner name
};
```

### Arrow function (ES6)
```js
const add = (a, b) => a + b;          // implicit return
const square = x => x * x;            // one param: parens optional
const greet = () => "hello";          // no params: parens required
const make = () => ({ ok: true });    // return an object literal: wrap in ()
const sum = (a, b) => {               // block body needs explicit return
  const total = a + b;
  return total;
};
```

Arrow functions are not just shorter — they differ in two important ways:
1. **No own `this`** — they inherit `this` from the enclosing scope (covered in depth in file 04). This makes them ideal for callbacks.
2. **No `arguments` object** — use rest parameters `(...args)` instead.

```js
// Why arrows shine in callbacks:
class Timer {
  constructor() {
    this.seconds = 0;
    setInterval(() => {
      this.seconds++;        // `this` correctly refers to the Timer instance
    }, 1000);
  }
}
// With a regular function() here, `this` would be wrong (undefined/window).
```

---

## III. PARAMETERS & ARGUMENTS

### Default parameters
```js
function greet(name = "stranger", greeting = "Hello") {
  return `${greeting}, ${name}!`;
}
greet();                    // "Hello, stranger!"
greet("Ada");               // "Hello, Ada!"
greet("Ada", "Welcome");    // "Welcome, Ada!"
greet(undefined, "Hi");     // "Hi, stranger!"  ← undefined triggers default
```

### Rest parameters — gather extra args into an array
```js
function sum(...numbers) {     // numbers is a real array
  return numbers.reduce((acc, n) => acc + n, 0);
}
sum(1, 2, 3, 4);   // 10
sum();             // 0

function logFirst(first, ...rest) {
  console.log("first:", first);  // 1
  console.log("rest:", rest);    // [2, 3, 4]
}
logFirst(1, 2, 3, 4);
```

### The `arguments` object (legacy — regular functions only)
```js
function old() {
  // `arguments` is array-LIKE (has length, indices) but NOT a real array
  console.log(arguments.length);
  return Array.from(arguments).reduce((a, b) => a + b, 0);
}
old(1, 2, 3); // 6
```
> Prefer rest parameters (`...args`). They give you a real array, work in arrow functions, and are clearer.

---

## IV. SCOPE — WHERE A VARIABLE LIVES

**Scope** is the set of rules that decides which variables you can access at a given point in code. JavaScript has three scope levels:

```
┌─ Global scope ─────────────────────────────┐
│  const APP = "codex";                       │
│                                             │
│  ┌─ Function scope ───────────────────────┐ │
│  │  function outer() {                     │ │
│  │    const a = 1;                         │ │
│  │    ┌─ Block scope ──────────────────┐   │ │
│  │    │  if (true) {                    │   │ │
│  │    │    let b = 2;  // only here     │   │ │
│  │    │  }                              │   │ │
│  │    └─────────────────────────────────┘  │ │
│  │  }                                       │ │
│  └──────────────────────────────────────────┘│
└──────────────────────────────────────────────┘
```

### Lexical scope — inner can see outer, not vice versa
```js
const a = "global";

function outer() {
  const b = "outer";

  function inner() {
    const c = "inner";
    console.log(a, b, c); // ✅ "global outer inner" — sees all enclosing scopes
  }

  inner();
  console.log(c); // ❌ ReferenceError — can't see into inner
}
outer();
```

Scope is **lexical** (a.k.a. *static*): determined by *where you write the code*, not by where/how it is called. This is the foundation closures are built on.

### The scope chain
When you reference a variable, JavaScript looks in the current scope, then the enclosing scope, then the next one out, all the way to global. First match wins. If nothing matches: `ReferenceError`.

```js
const x = "global";
function a() {
  const x = "a";
  function b() {
    console.log(x); // "a" — found in nearest enclosing scope, stops looking
  }
  b();
}
a();
```

---

## V. HOISTING — WHY YOU CAN SOMETIMES USE THINGS EARLY

**Hoisting** is JavaScript's behavior of processing declarations before executing code. Conceptually, declarations are "moved to the top" of their scope. But the details differ by declaration type.

### Function declarations: fully hoisted
```js
console.log(add(2, 3)); // ✅ 5 — works before the definition!

function add(a, b) {
  return a + b;
}
```

### `var`: hoisted but initialized to `undefined`
```js
console.log(x); // undefined — NOT a ReferenceError, but no value yet
var x = 5;
console.log(x); // 5

// What the engine effectively sees:
// var x;          ← declaration hoisted
// console.log(x); // undefined
// x = 5;          ← assignment stays put
```

### `let` / `const`: hoisted but in the "Temporal Dead Zone"
```js
console.log(y); // ❌ ReferenceError: Cannot access 'y' before initialization
let y = 5;
```
`let` and `const` *are* hoisted, but you cannot touch them until the declaration line runs. The gap between scope-entry and declaration is the **Temporal Dead Zone (TDZ)**. This is a feature: it catches "used before defined" bugs that `var` silently allowed.

### Function expressions are NOT callable when hoisted
```js
console.log(fn);   // undefined (var hoisting) — it's not a function yet
console.log(fn()); // ❌ TypeError: fn is not a function
var fn = function () { return 1; };
```

> **Mental model:** function declarations are fully ready before any code runs. `var` exists-but-empty. `let`/`const` exist-but-locked until their line. This is why function declarations are convenient for top-level helpers but `const fn = ...` is preferred for predictability.

---

## VI. CLOSURES ⭐ (THE MOST IMPORTANT CONCEPT)

A **closure** is a function bundled together with references to the variables from the scope where it was *created*. Because of lexical scope, an inner function "remembers" the outer variables even after the outer function has returned.

> **One-line definition:** *A closure is a function that retains access to its birth scope's variables, even after that scope has finished executing.*

### The canonical example
```js
function makeCounter() {
  let count = 0;            // private variable

  return function () {      // this inner function is a closure
    count++;                // it "closes over" count
    return count;
  };
}

const counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
console.log(counter()); // 3

const counter2 = makeCounter(); // a SEPARATE count
console.log(counter2()); // 1   ← independent state
```

`makeCounter` has returned and exited — yet `count` lives on, because the returned function holds a reference to it. Each call to `makeCounter` creates a brand-new `count`. **The closure is the mechanism behind private state in JavaScript.**

### Why the `var` loop bug happens (and `let` fixes it)
```js
// THE BUG
const fns = [];
for (var i = 0; i < 3; i++) {
  fns.push(() => i);     // all three close over the SAME i
}
console.log(fns.map(f => f())); // [3, 3, 3]
// By the time the functions run, the single shared `i` is 3.

// THE FIX: let creates a new binding per iteration
const fns2 = [];
for (let j = 0; j < 3; j++) {
  fns2.push(() => j);    // each closes over its OWN j
}
console.log(fns2.map(f => f())); // [0, 1, 2]

// THE OLD-SCHOOL FIX (pre-let): an IIFE to capture each value
const fns3 = [];
for (var k = 0; k < 3; k++) {
  fns3.push(((captured) => () => captured)(k));
}
console.log(fns3.map(f => f())); // [0, 1, 2]
```

### Practical uses of closures

**1. Data privacy / encapsulation**
```js
function createBankAccount(initial) {
  let balance = initial;       // no one outside can touch this directly

  return {
    deposit(amount) { balance += amount; return balance; },
    withdraw(amount) {
      if (amount > balance) throw new Error("Insufficient funds");
      balance -= amount;
      return balance;
    },
    getBalance() { return balance; },
  };
}

const acct = createBankAccount(100);
acct.deposit(50);     // 150
acct.withdraw(30);    // 120
acct.getBalance();    // 120
acct.balance;         // undefined — truly private
```

**2. Function factories**
```js
function makeMultiplier(factor) {
  return x => x * factor;       // closes over factor
}
const triple = makeMultiplier(3);
const tenX = makeMultiplier(10);
triple(5);  // 15
tenX(5);    // 50
```

**3. Memoization (caching) — closures hold the cache**
```js
function memoize(fn) {
  const cache = new Map();      // private cache, lives in the closure
  return function (n) {
    if (cache.has(n)) return cache.get(n);
    const result = fn(n);
    cache.set(n, result);
    return result;
  };
}
const slowSquare = n => { /* imagine expensive work */ return n * n; };
const fastSquare = memoize(slowSquare);
fastSquare(4); // computes → 16
fastSquare(4); // cached → 16 (no recompute)
```
(More on memoization, currying, debounce, and throttle in file 08 — all powered by closures.)

> 🧠 **Where you've already used closures without knowing:** every callback passed to `setTimeout`, every event handler that references an outer variable, every React `useState` updater. Closures are everywhere.

---

## VII. IIFE — IMMEDIATELY INVOKED FUNCTION EXPRESSION

An IIFE is a function that runs the instant it is defined. Before ES6 modules and block scoping, it was the primary way to create a private scope and avoid polluting the global namespace.

```js
(function () {
  const secret = "hidden";       // not visible outside
  console.log("runs immediately");
})();

// Arrow version
(() => {
  console.log("also runs immediately");
})();

// Returning a value
const config = (function () {
  const apiKey = "abc123";       // private
  return { getKey: () => apiKey };
})();
config.getKey(); // "abc123"
```

### Why the wrapping parentheses?
```js
function () {}();   // ❌ SyntaxError — parsed as a declaration
(function () {})(); // ✅ the () turns it into an expression, then we call it
```

### The classic IIFE use case (now mostly replaced by modules)
```js
// Avoiding global pollution in the script-tag era
var MyLibrary = (function () {
  var privateState = 0;          // not on the global object
  function privateHelper() { return privateState; }
  return {
    increment: function () { privateState++; },
    get: privateHelper,
  };
})();
```
Today, ES modules (file 06) give each file its own scope, so IIFEs are less needed — but you'll still see them in older code, bundled libraries, and the occasional `(async () => { await ... })()` to use `await` at the top level.

---

## VIII. COMMON PITFALLS & GOTCHAS

**1. The `var` loop closure trap** — already shown; use `let`.

**2. Losing `this` by extracting a method (fixed by arrows — preview of file 04)**
```js
const obj = {
  name: "Codex",
  regular() { return this.name; },
};
const fn = obj.regular;
fn(); // undefined or error — `this` is lost. Arrow methods or .bind() fix it.
```

**3. Creating functions in a loop (memory)**
```js
// Each iteration creates a new function — usually fine, but be aware
// in hot loops. Define once outside if the function doesn't need loop state.
```

**4. Forgetting arrow functions can't be `new`-ed or used as constructors**
```js
const Foo = () => {};
new Foo(); // ❌ TypeError: Foo is not a constructor
```

**5. Hoisting confusion**
```js
greet();                  // ✅ works (declaration hoisted)
function greet() {}

sayHi();                  // ❌ TypeError (expression not hoisted as function)
const sayHi = () => {};
```

---

## IX. KEY TAKEAWAYS

- Functions are **first-class values**: assignable, passable, returnable, storable.
- **Declarations** are hoisted and callable early; **expressions** and **arrow functions** are not.
- **Arrow functions** have no own `this` and no `arguments` — perfect for callbacks, wrong for object methods that need `this` and for constructors.
- **Scope is lexical** — determined by where code is *written*. Inner scopes see outer variables; not the reverse.
- **Hoisting**: function declarations are fully ready; `var` is `undefined`-until-assigned; `let`/`const` are locked in the **Temporal Dead Zone** until their line runs.
- A **closure ⭐** is a function that remembers its birth scope's variables even after that scope returns. It powers private state, factories, memoization, and nearly every callback you write.
- The `var`-in-a-loop bug exists because `var` shares one binding; `let` creates a fresh binding per iteration.
- **IIFEs** run immediately and create a private scope — historically used to avoid globals, now largely replaced by ES modules.

---

**← Prev:** [`01-JS-Fundamentals.md`](./01-JS-Fundamentals.md) | **→ Next:** [`03-Objects-And-Arrays.md`](./03-Objects-And-Arrays.md) | **Index:** [`00-Index.md`](./00-Index.md)
