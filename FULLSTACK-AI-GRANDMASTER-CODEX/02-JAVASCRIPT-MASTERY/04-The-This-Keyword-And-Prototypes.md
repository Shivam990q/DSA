# 🎯 The `this` Keyword & Prototypes

> *"`this` is not where the function lives. It's how the function is called."*

`this` and prototypes are the two concepts that make people say "JavaScript's OOP is weird." It isn't — it's just *different*. Once you learn the four rules of `this` binding and the idea of the prototype chain, classes become a thin layer of sugar over a simple, elegant model.

---

## I. WHAT IS `this`?

`this` is a special keyword that refers to an object — but **which** object is decided at **call time**, not when the function is written. The same function can have different `this` values depending on how you call it.

> **The golden rule:** to find `this`, don't look at where the function is *defined* — look at how it's *called*.

There are four binding rules, checked in priority order. Learn these and `this` is never mysterious again.

---

## II. THE FOUR BINDING RULES

### Rule 1: Default binding (a plain function call)
```js
function show() {
  console.log(this);
}
show();   // global object (window in browser, global in Node) — or undefined in strict mode
```
In strict mode (`"use strict"`, and inside ES modules/classes), a plain call sets `this` to `undefined`.

### Rule 2: Implicit binding (called as a method)
```js
const user = {
  name: "Ada",
  greet() {
    return `Hi, I'm ${this.name}`;  // `this` is the object left of the dot
  },
};
user.greet();   // "Hi, I'm Ada" — `this` is `user`

// The "left of the dot" rule:
const obj = { x: 10, getX() { return this.x; } };
obj.getX();     // 10 — obj is left of the dot
```

### The implicit binding LOSS trap ⚠️
```js
const user = {
  name: "Ada",
  greet() { return `Hi, ${this.name}`; },
};

const fn = user.greet;   // extracted — no object attached anymore
fn();                    // "Hi, undefined" — `this` lost (default binding)

// Same trap with callbacks:
setTimeout(user.greet, 100); // `this` is lost — greet called without `user.`
setTimeout(() => user.greet(), 100); // ✅ fixed: arrow preserves the call form
setTimeout(user.greet.bind(user), 100); // ✅ fixed: bind locks `this`
```

### Rule 3: Explicit binding (`call`, `apply`, `bind`)
You can force `this` to be whatever you want.

```js
function introduce(greeting, punctuation) {
  return `${greeting}, I'm ${this.name}${punctuation}`;
}
const person = { name: "Grace" };

// call — pass `this`, then args one by one
introduce.call(person, "Hello", "!");      // "Hello, I'm Grace!"

// apply — pass `this`, then args as an ARRAY
introduce.apply(person, ["Hi", "."]);      // "Hi, I'm Grace."

// bind — returns a NEW function with `this` permanently locked
const boundIntro = introduce.bind(person);
boundIntro("Hey", "?");                    // "Hey, I'm Grace?"
```

> **Memory aid:** **c**all = **c**omma-separated args. **a**pply = **a**rray of args. **bind** = **b**ind for later (returns a new function instead of calling now).

### Rule 4: `new` binding (constructor call)
```js
function User(name) {
  // `new` creates a fresh object and binds `this` to it
  this.name = name;
  // implicitly returns `this`
}
const u = new User("Ada");
u.name;   // "Ada"
```

### Bonus: arrow functions ignore all four rules
Arrow functions have **no own `this`**. They capture `this` from the enclosing lexical scope at definition time. `call`/`apply`/`bind` cannot change it.

```js
const obj = {
  name: "Codex",
  regularMethod() {
    // `this` is obj here ✅
    const arrow = () => this.name;  // arrow captures obj's `this`
    return arrow();
  },
  arrowMethod: () => this.name,     // ⚠️ `this` is the OUTER scope, NOT obj
};
obj.regularMethod(); // "Codex"  ✅
obj.arrowMethod();   // undefined ❌ — arrow captured the module/global `this`
```

> ✅ Use arrow functions for **callbacks inside methods** (they inherit the right `this`). Use regular functions/methods for **object methods** (so `this` is the object).

### The priority order (highest wins)
```
new binding  >  explicit (bind/call/apply)  >  implicit (obj.method())  >  default
```

---

## III. PROTOTYPES — JAVASCRIPT'S INHERITANCE MODEL

Unlike class-based languages, JavaScript uses **prototypal inheritance**. Every object has a hidden link to another object — its **prototype**. When you access a property that doesn't exist on an object, JavaScript walks up this **prototype chain** until it finds it (or hits `null`).

```js
const animal = {
  eats: true,
  walk() { return "walking"; },
};

const rabbit = {
  jumps: true,
  __proto__: animal,   // rabbit's prototype is animal (demo syntax)
};

rabbit.jumps   // true   — own property
rabbit.eats    // true   — inherited from animal via the chain
rabbit.walk()  // "walking" — inherited method
```

### The prototype chain, visualized
```
rabbit ──▶ animal ──▶ Object.prototype ──▶ null
{jumps}    {eats,walk}  {toString,hasOwnProperty,...}

Looking up rabbit.eats:
  1. on rabbit?         no
  2. on animal?         YES → return true (stop)

Looking up rabbit.toString:
  1. on rabbit?         no
  2. on animal?         no
  3. on Object.prototype? YES → return the function
```

### Inspecting and setting prototypes (modern API)
```js
const proto = { hello() { return "hi"; } };
const obj = Object.create(proto);  // create obj with proto as its prototype
obj.hello();                       // "hi" — inherited

Object.getPrototypeOf(obj) === proto;  // true
obj.hasOwnProperty("hello");           // false — it's inherited, not own
"hello" in obj;                        // true — own OR inherited
```

### Constructor functions + `.prototype` (the pre-class pattern)
```js
function Animal(name) {
  this.name = name;                // own (instance) property
}
// Methods go on the prototype — SHARED by all instances (memory-efficient)
Animal.prototype.speak = function () {
  return `${this.name} makes a sound`;
};

const dog = new Animal("Rex");
dog.speak();                       // "Rex makes a sound"
dog.hasOwnProperty("name");        // true  — own
dog.hasOwnProperty("speak");       // false — on the prototype
```
> Methods live on `.prototype` so all instances **share one copy** rather than each carrying its own. This is exactly what `class` does under the hood.

---

## IV. CLASSES — SUGAR OVER PROTOTYPES

ES6 `class` syntax is cleaner to read but compiles down to the prototype machinery above. There is no separate "class system" — it's the same prototypes, nicer syntax.

```js
class Animal {
  constructor(name) {
    this.name = name;              // instance property
  }
  speak() {                        // goes on Animal.prototype automatically
    return `${this.name} makes a sound`;
  }
  static create(name) {            // static: called on the class, not instances
    return new Animal(name);
  }
}

const a = new Animal("Rex");
a.speak();              // "Rex makes a sound"
Animal.create("Bella"); // static method on the class itself

// Proof it's still prototypes:
typeof Animal;                            // "function"
Object.getPrototypeOf(a) === Animal.prototype; // true
```

### Inheritance with `extends` and `super`
```js
class Animal {
  constructor(name) { this.name = name; }
  speak() { return `${this.name} makes a sound`; }
}

class Dog extends Animal {
  constructor(name, breed) {
    super(name);                   // MUST call super() before using `this`
    this.breed = breed;
  }
  speak() {                        // override
    return `${super.speak()} — specifically, a bark`; // super calls parent's version
  }
}

const d = new Dog("Rex", "Lab");
d.speak();   // "Rex makes a sound — specifically, a bark"
d instanceof Dog;     // true
d instanceof Animal;  // true — inheritance chain
```

### Getters, setters, and private fields (`#`)
```js
class Temperature {
  #celsius = 0;                    // # = truly private (not accessible outside)

  get celsius() { return this.#celsius; }
  set celsius(value) {
    if (value < -273.15) throw new Error("Below absolute zero");
    this.#celsius = value;
  }
  get fahrenheit() { return this.#celsius * 9 / 5 + 32; }
  set fahrenheit(value) { this.#celsius = (value - 32) * 5 / 9; }
}

const t = new Temperature();
t.celsius = 25;        // uses the setter (validates)
t.fahrenheit;          // 77 — computed getter
t.fahrenheit = 212;    // uses the setter
t.celsius;             // 100
t.#celsius;            // ❌ SyntaxError — private field, no outside access
```

### Static members and fields
```js
class Counter {
  static count = 0;                // shared across all (class-level) 
  #id;
  constructor() {
    Counter.count++;
    this.#id = Counter.count;
  }
  get id() { return this.#id; }
}
new Counter(); new Counter();
Counter.count;   // 2
```

---

## V. PUTTING `this` AND CLASSES TOGETHER

The `this`-loss trap appears constantly with class methods used as callbacks:

```js
class Button {
  constructor(label) {
    this.label = label;
  }
  // ❌ regular method: `this` is lost when passed as a handler
  handleClickBad() {
    console.log(`Clicked ${this.label}`); // `this` undefined when detached
  }
  // ✅ arrow class field: `this` is bound to the instance permanently
  handleClickGood = () => {
    console.log(`Clicked ${this.label}`);
  };
}

const btn = new Button("Save");
const bad = btn.handleClickBad;
// bad();  // 💥 error — this.label fails

const good = btn.handleClickGood;
good();    // ✅ "Clicked Save" — arrow field captured `this`

// Or bind in the constructor (the classic React pattern):
class Button2 {
  constructor(label) {
    this.label = label;
    this.handleClick = this.handleClick.bind(this);
  }
  handleClick() { console.log(this.label); }
}
```

---

## VI. COMMON PITFALLS & GOTCHAS

**1. Losing `this` by detaching a method** — the #1 issue. Use arrow class fields or `.bind()`.

**2. Using an arrow function as an object method**
```js
const obj = { name: "x", get: () => this.name }; // ❌ `this` is not obj
```

**3. Forgetting `super()` in a subclass constructor**
```js
class B extends A {
  constructor() { this.x = 1; } // ❌ ReferenceError — must call super() first
}
```

**4. Forgetting `new`**
```js
function User(n) { this.name = n; }
const u = User("Ada");   // ❌ no `new` — `this` is global; u is undefined
const u2 = new User("Ada"); // ✅
// (Classes throw a clear error if called without `new` — another reason to use them.)
```

**5. Putting methods inside the constructor (wastes memory)**
```js
class Bad {
  constructor() {
    this.method = function () {}; // new copy per instance — avoid
  }
}
// Prefer defining methods in the class body (they go on the prototype, shared).
```

**6. Modifying built-in prototypes (don't)**
```js
Array.prototype.last = function () { return this[this.length - 1]; };
// Works, but pollutes ALL arrays globally and can break other code. Avoid.
```

---

## VII. KEY TAKEAWAYS

- `this` is determined by **how a function is called**, not where it's defined.
- The four rules, by priority: **`new`** > **explicit (`bind`/`call`/`apply`)** > **implicit (`obj.method()`)** > **default (`undefined`/global)**.
- `call`/`apply` invoke immediately (comma args / array args); `bind` returns a new function with `this` locked.
- **Arrow functions have no own `this`** — they capture it lexically. Great for callbacks, wrong for object methods and constructors.
- JavaScript uses **prototypal inheritance**: property lookups walk the **prototype chain** until found or `null`.
- Methods live on `.prototype` so all instances **share one copy**.
- `class` is **syntactic sugar** over prototypes — `extends`/`super` for inheritance, `#field` for true privacy, `static` for class-level members, getters/setters for computed properties.
- The "lost `this`" trap (detached method as callback) is solved with **arrow class fields** or **`.bind(this)`**.

---

**← Prev:** [`03-Objects-And-Arrays.md`](./03-Objects-And-Arrays.md) | **→ Next:** [`05-Asynchronous-JavaScript.md`](./05-Asynchronous-JavaScript.md) | **Index:** [`00-Index.md`](./00-Index.md)
