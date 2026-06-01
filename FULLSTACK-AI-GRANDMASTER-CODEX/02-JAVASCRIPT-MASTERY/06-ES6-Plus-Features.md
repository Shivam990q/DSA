# 🚀 ES6+ Modern Features

> *"ES6 (2015) split JavaScript into 'before' and 'after.' Everything since has made it sharper."*

ECMAScript 2015 (ES6) and the yearly releases after it transformed JavaScript from a quirky scripting language into a serious, ergonomic one. This file is your tour of the modern syntax you'll see in every codebase: modules, template literals, optional chaining, nullish coalescing, `Map`/`Set`, generators, and iterators.

---

## I. MODULES — `import` / `export`

Before modules, JavaScript files shared everything through global variables (chaos). ES modules give each file its own scope and an explicit interface: you choose what to `export`, and other files `import` it.

### Named exports (many per file)
```js
// math.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export function sub(a, b) { return a - b; }

// or export at the bottom:
const mul = (a, b) => a * b;
export { mul };
```
```js
// main.js
import { PI, add, sub } from "./math.js";
add(2, 3);   // 5

import { add as plus } from "./math.js";  // rename on import
import * as math from "./math.js";        // import everything as a namespace
math.PI;     // 3.14159
```

### Default export (one per file)
```js
// User.js
export default class User {
  constructor(name) { this.name = name; }
}

// main.js — no braces, you choose the name
import User from "./User.js";
import Whatever from "./User.js";  // default imports can be named anything

// Mix default + named
import User, { PI, add } from "./somefile.js";
```

### Dynamic import (load on demand — code splitting)
```js
button.addEventListener("click", async () => {
  const { heavyChart } = await import("./charts.js"); // loaded only when needed
  heavyChart();
});
```

> **CommonJS vs ESM:** older Node code uses `require()` / `module.exports` (CommonJS). Modern code uses `import`/`export` (ES modules). In Node, ESM needs `"type": "module"` in `package.json` or a `.mjs` extension. Bundlers (Vite, webpack) handle ESM in the browser. Prefer ESM in new projects.

---

## II. TEMPLATE LITERALS

Backtick strings with interpolation and multi-line support.

```js
const name = "Ada", age = 36;

// Interpolation with ${...}
const msg = `${name} is ${age} years old`;       // "Ada is 36 years old"
const calc = `Next year: ${age + 1}`;            // "Next year: 37"

// Multi-line — no more \n concatenation
const html = `
  <div>
    <h1>${name}</h1>
    <p>Age: ${age}</p>
  </div>
`;

// Any expression works inside ${}
const items = ["a", "b", "c"];
const list = `You have ${items.length} item${items.length === 1 ? "" : "s"}`;
```

### Tagged templates (advanced)
A function can process a template literal — used by libraries like styled-components and for safe escaping.
```js
function highlight(strings, ...values) {
  return strings.reduce((out, str, i) =>
    `${out}${str}${values[i] ? `<b>${values[i]}</b>` : ""}`, "");
}
const name = "Ada";
highlight`Hello ${name}, welcome!`; // "Hello <b>Ada</b>, welcome!"
```

---

## III. DEFAULT, REST & SPREAD (recap + nuance)

```js
// Default parameters
function connect(host = "localhost", port = 5432, opts = {}) {
  return `${host}:${port}`;
}
connect();                 // "localhost:5432"
connect("db.io");          // "db.io:5432"

// Defaults can reference earlier params
function rect(w, h = w) { return w * h; }
rect(5);    // 25 (square)

// Rest gathers (file 02), spread expands (file 03)
const merge = (...arrays) => [].concat(...arrays);
merge([1, 2], [3], [4, 5]);  // [1,2,3,4,5]
```

---

## IV. OPTIONAL CHAINING `?.`

Safely access deeply nested properties that might not exist — no more `a && a.b && a.b.c`.

```js
const user = {
  name: "Ada",
  address: { city: "London" },
};

// Without optional chaining (verbose, error-prone)
const zip1 = user && user.address && user.address.zip; // undefined

// With optional chaining (clean)
const zip2 = user?.address?.zip;        // undefined — no error
const city = user?.address?.city;       // "London"
const missing = user?.contact?.email;   // undefined (contact doesn't exist)

// Works with method calls — only calls if it exists
user.greet?.();              // undefined if greet isn't a function (no crash)
api.onSuccess?.(data);       // call the callback only if provided

// Works with dynamic/array access
const first = data?.items?.[0];   // safe even if items is undefined
```
> `?.` short-circuits: the moment it hits `null`/`undefined`, it stops and returns `undefined` instead of throwing `Cannot read property 'x' of undefined`.

---

## V. NULLISH COALESCING `??`

Provide a fallback **only** when a value is `null` or `undefined` — unlike `||`, which falls back on *any* falsy value.

```js
// The problem with ||
const count = 0;
const a = count || 10;    // 10  ❌ — 0 is valid but falsy!
const b = count ?? 10;    // 0   ✅ — only null/undefined trigger fallback

const name = "";
name || "Anon";           // "Anon" ❌ — empty string is valid but falsy
name ?? "Anon";           // ""     ✅ — keeps the empty string

// When you DO want any-falsy fallback, || is still right:
const displayName = userInput || "Guest"; // treat "" and 0 as "no input"
```

### `??` vs `||` cheat sheet
| Value | `x || "fb"` | `x ?? "fb"` |
|-------|-------------|-------------|
| `0` | `"fb"` | `0` |
| `""` | `"fb"` | `""` |
| `false` | `"fb"` | `false` |
| `null` | `"fb"` | `"fb"` |
| `undefined` | `"fb"` | `"fb"` |

### Combine with optional chaining (the modern idiom)
```js
const port = config?.server?.port ?? 3000;  // deep-safe read + sensible default
```

### Logical assignment operators
```js
let a = null;
a ??= 5;       // assign only if a is null/undefined → a = 5
let b = 0;
b ||= 10;      // assign if b is falsy → b = 10
let c = 1;
c &&= 2;       // assign if c is truthy → c = 2
```

---

## VI. `Map` AND `Set`

### `Map` — keyed collection with ANY key type
Plain objects only allow string/symbol keys and carry a prototype. `Map` allows *any* key (objects, functions, numbers), preserves insertion order, and has a clean API.

```js
const map = new Map();
map.set("name", "Ada");
map.set(42, "the answer");
const objKey = { id: 1 };
map.set(objKey, "object as key!");   // ✅ objects as keys — impossible with {}

map.get("name");      // "Ada"
map.get(objKey);      // "object as key!"
map.has(42);          // true
map.size;             // 3
map.delete("name");

// Iterate (insertion order guaranteed)
for (const [key, value] of map) {
  console.log(key, value);
}
map.forEach((value, key) => console.log(key, value));

// Init from entries / convert to array
const m = new Map([["a", 1], ["b", 2]]);
[...m.keys()];     // ["a", "b"]
[...m.values()];   // [1, 2]
[...m.entries()];  // [["a",1],["b",2]]
```

**Map vs Object — when to use which:**
| Need | Use |
|------|-----|
| Non-string keys, frequent add/remove, size, ordered iteration | `Map` |
| Fixed structure, JSON serialization, method definitions | Object |

### `Set` — collection of unique values
```js
const set = new Set([1, 2, 2, 3, 3, 3]);
set;            // Set(3) {1, 2, 3} — duplicates removed automatically
set.add(4);
set.has(2);     // true
set.delete(1);
set.size;       // 3

// THE most common use: dedupe an array
const unique = [...new Set([1, 1, 2, 3, 3])];  // [1, 2, 3]

// Set operations
const a = new Set([1, 2, 3]), b = new Set([2, 3, 4]);
const intersection = [...a].filter(x => b.has(x)); // [2, 3]
const union = [...new Set([...a, ...b])];          // [1, 2, 3, 4]
const difference = [...a].filter(x => !b.has(x));  // [1]
```

> `WeakMap`/`WeakSet` exist too: keys must be objects and are held weakly (garbage-collected when nothing else references them). Useful for caching metadata without causing memory leaks.

---

## VII. ITERATORS & GENERATORS

### The iterator protocol
An object is **iterable** if it has a `Symbol.iterator` method returning an object with a `next()` that yields `{ value, done }`. Arrays, strings, `Map`, and `Set` are all built-in iterables — which is why `for...of` and spread work on them.

```js
const arr = [10, 20, 30];
const it = arr[Symbol.iterator]();
it.next();   // { value: 10, done: false }
it.next();   // { value: 20, done: false }
it.next();   // { value: 30, done: false }
it.next();   // { value: undefined, done: true }
```

### Making your own iterable
```js
const range = {
  from: 1,
  to: 5,
  [Symbol.iterator]() {
    let current = this.from;
    const last = this.to;
    return {
      next() {
        return current <= last
          ? { value: current++, done: false }
          : { value: undefined, done: true };
      },
    };
  },
};
[...range];               // [1, 2, 3, 4, 5]
for (const n of range) console.log(n); // 1 2 3 4 5
```

### Generators — iterators made easy with `function*` and `yield`
A generator function pauses at each `yield` and resumes when you ask for the next value. It's the simplest way to create custom iterables and to model lazy/infinite sequences.

```js
function* counter() {
  yield 1;
  yield 2;
  yield 3;
}
const gen = counter();
gen.next();   // { value: 1, done: false }
gen.next();   // { value: 2, done: false }
gen.next();   // { value: 3, done: false }
gen.next();   // { value: undefined, done: true }

[...counter()];  // [1, 2, 3] — generators are iterable

// Rewrite the range as a generator (much shorter)
function* range(from, to) {
  for (let i = from; i <= to; i++) yield i;
}
[...range(1, 5)];   // [1, 2, 3, 4, 5]

// Infinite sequences — lazy, only computes what you take
function* naturals() {
  let n = 1;
  while (true) yield n++;
}
const nats = naturals();
nats.next().value;  // 1
nats.next().value;  // 2
// never runs out of memory — values produced on demand

// Generators can receive values via next(arg) and delegate with yield*
function* fib() {
  let [a, b] = [0, 1];
  while (true) { yield a; [a, b] = [b, a + b]; }
}
const f = fib();
[f.next().value, f.next().value, f.next().value, f.next().value]; // [0,1,1,2]
```

> Generators power async iteration (`for await...of`), data streaming, and state machines. They're niche day-to-day but elegant when you need lazy evaluation.

---

## VIII. OTHER MODERN ESSENTIALS

```js
// String methods
"  hi  ".trim();              // "hi"
"abc".padStart(5, "0");       // "00abc"
"5".padEnd(3, "*");           // "5**"
"hello".includes("ell");      // true
"hello".startsWith("he");     // true
"a,b,c".replaceAll(",", "-"); // "a-b-c"

// Numeric separators & methods
const billion = 1_000_000_000;     // underscores for readability
Number.isInteger(5);               // true
(3.14159).toFixed(2);              // "3.14"

// Object/array shortcuts
Object.fromEntries([["a", 1]]);    // { a: 1 }
[1, 2, 3].at(-1);                  // 3 (negative indexing)
["a","b","c"].at(-2);              // "b"

// Array grouping (newer)
const nums = [1, 2, 3, 4, 5];
// Object.groupBy(nums, n => n % 2 ? "odd" : "even"); // {odd:[1,3,5], even:[2,4]}
```

---

## IX. COMMON PITFALLS & GOTCHAS

**1. `||` where you needed `??`**
```js
const timeout = config.timeout || 3000;  // ❌ a valid timeout of 0 becomes 3000
const timeout = config.timeout ?? 3000;  // ✅
```

**2. Mixing `??` with `||`/`&&` without parentheses**
```js
a ?? b || c;     // ❌ SyntaxError — must disambiguate
(a ?? b) || c;   // ✅
```

**3. Forgetting file extensions in browser ESM imports**
```js
import { x } from "./util";     // ❌ in raw browser ESM
import { x } from "./util.js";  // ✅ (bundlers are more lenient)
```

**4. Treating `Map`/`Set` like arrays**
```js
const s = new Set([1, 2, 3]);
s[0];          // ❌ undefined — no index access
[...s][0];     // ✅ convert first
s.map(...);    // ❌ no map on Set — spread to array first
```

**5. Optional chaining hides bugs if overused** — only use it where a value is *genuinely* optional, not to paper over a data-shape mistake.

---

## X. KEY TAKEAWAYS

- **Modules** (`import`/`export`) give each file its own scope: named exports (many) vs default export (one); `import()` loads code on demand.
- **Template literals** (backticks) do interpolation `${...}` and multi-line strings.
- **Optional chaining `?.`** safely reads nested properties/methods, returning `undefined` instead of throwing.
- **Nullish coalescing `??`** falls back only on `null`/`undefined` (unlike `||`, which falls back on any falsy value). Combine: `a?.b ?? default`.
- **`Map`** allows any key type, ordered iteration, and `size`; **`Set`** stores unique values (the go-to for deduping: `[...new Set(arr)]`).
- **Iterators** make objects work with `for...of` and spread; **generators** (`function*`/`yield`) are the easy way to build them and to model lazy/infinite sequences.
- Logical assignment (`??=`, `||=`, `&&=`), numeric separators (`1_000`), and `.at(-1)` are small modern wins worth knowing.

---

**← Prev:** [`05-Asynchronous-JavaScript.md`](./05-Asynchronous-JavaScript.md) | **→ Next:** [`07-The-DOM-And-Events.md`](./07-The-DOM-And-Events.md) | **Index:** [`00-Index.md`](./00-Index.md)
