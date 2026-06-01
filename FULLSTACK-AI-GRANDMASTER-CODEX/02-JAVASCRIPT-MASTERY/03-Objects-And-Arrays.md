# 📦 Objects & Arrays

> *"90% of real JavaScript is reshaping data: objects in, objects out."*

Objects and arrays are how you model the world in JavaScript — a user is an object, a list of users is an array. This file covers building and reading them, the destructuring/spread/rest syntax that makes modern JS concise, and the array methods (`map`, `filter`, `reduce ⭐`) that replace nearly every `for` loop you'd otherwise write.

---

## I. OBJECTS — KEY/VALUE COLLECTIONS

An object maps **string (or symbol) keys** to values of any type.

```js
const user = {
  name: "Ada",
  age: 36,
  isAdmin: true,
  greet() { return `Hi, I'm ${this.name}`; },  // method shorthand
  "favorite color": "teal",                     // keys with spaces need quotes
};
```

### Reading and writing properties
```js
user.name              // "Ada"           — dot notation
user["name"]           // "Ada"           — bracket notation
user["favorite color"] // "teal"          — bracket required for odd keys

const key = "age";
user[key]              // 36              — dynamic key (dot can't do this)

user.email = "ada@x.io";   // add a new property
user.age = 37;             // update
delete user.isAdmin;       // remove
```

### Checking for properties
```js
"name" in user             // true  — own or inherited
user.hasOwnProperty("name")// true  — own only
user.missing === undefined // true  — but careful: a key set to undefined also matches
Object.hasOwn(user, "name")// true  — modern, preferred over hasOwnProperty
```

### Computed property names & shorthand
```js
const field = "score";
const value = 99;

const record = {
  [field]: value,   // computed key → { score: 99 }
};

const name = "Grace", age = 45;
const person = { name, age }; // shorthand for { name: name, age: age }
```

### Iterating over objects
```js
const obj = { a: 1, b: 2, c: 3 };

Object.keys(obj);     // ["a", "b", "c"]
Object.values(obj);   // [1, 2, 3]
Object.entries(obj);  // [["a", 1], ["b", 2], ["c", 3]]

for (const [key, val] of Object.entries(obj)) {
  console.log(`${key} = ${val}`);
}

// Build an object back from entries
Object.fromEntries([["x", 1], ["y", 2]]); // { x: 1, y: 2 }
```

### Useful Object static methods
```js
Object.assign({}, obj, { d: 4 });  // merge (shallow) → { a:1, b:2, c:3, d:4 }
Object.freeze(obj);                // make immutable (shallow)
Object.isFrozen(obj);              // true
const copy = structuredClone(obj); // deep clone (modern browsers/Node 17+)
```

---

## II. REFERENCE vs VALUE (the bug that bites everyone)

Primitives are copied **by value**. Objects and arrays are copied **by reference** — the variable holds a pointer, not the data.

```js
// Primitives: independent copies
let a = 1;
let b = a;
b = 2;
console.log(a, b); // 1 2 — a is untouched

// Objects: shared reference
const obj1 = { count: 1 };
const obj2 = obj1;       // both point at the SAME object
obj2.count = 99;
console.log(obj1.count); // 99 — surprise! they're the same object

// Equality compares references, not contents
{ a: 1 } === { a: 1 }    // false — two different objects
const x = { a: 1 };
x === x                  // true — same reference
```

### Shallow vs deep copy
```js
const original = { name: "Ada", address: { city: "London" } };

// Shallow copy — top level is copied, nested objects are still shared
const shallow = { ...original };
shallow.name = "Grace";              // ✅ doesn't affect original
shallow.address.city = "Paris";      // ⚠️ DOES affect original.address.city!

// Deep copy — fully independent
const deep = structuredClone(original);
deep.address.city = "Berlin";        // ✅ original is safe
```

> 🐛 The shallow-copy nested-mutation bug is one of the most common in React state and Redux. When in doubt about nesting, `structuredClone` or copy each level explicitly.

---

## III. ARRAYS — ORDERED COLLECTIONS

Arrays are objects with integer keys and a `length`. They hold any mix of types.

```js
const nums = [1, 2, 3, 4, 5];
const mixed = [1, "two", true, null, { a: 1 }, [1, 2]];

nums.length    // 5
nums[0]        // 1
nums[nums.length - 1] // 5 — last element
nums.at(-1)    // 5 — modern: negative indexing
```

### Mutating methods (change the original array)
```js
const arr = [1, 2, 3];
arr.push(4);        // add to end       → [1,2,3,4]   returns new length
arr.pop();          // remove from end  → [1,2,3]     returns removed item
arr.unshift(0);     // add to front     → [0,1,2,3]
arr.shift();        // remove from front→ [1,2,3]
arr.splice(1, 1);   // remove at index  → [1,3]       (start, deleteCount)
arr.splice(1, 0, 9);// insert at index  → [1,9,3]
arr.reverse();      // → [3,9,1]
arr.sort();         // → sorted in place
```

### Non-mutating methods (return a NEW array — prefer these)
```js
const arr = [1, 2, 3];
const more   = arr.concat([4, 5]);  // [1,2,3,4,5]  (arr unchanged)
const part   = arr.slice(1, 3);     // [2,3]        (start, end-exclusive)
const joined = arr.join("-");       // "1-2-3"
const spread = [...arr, 4];         // [1,2,3,4]    (spread copy)
```

### ⚠️ The `sort` gotcha (lexicographic by default)
```js
[10, 1, 2, 20, 3].sort();             // [1, 10, 2, 20, 3] — sorted as STRINGS!
[10, 1, 2, 20, 3].sort((a, b) => a - b); // [1, 2, 3, 10, 20] — numeric, correct
[10, 1, 2, 20, 3].sort((a, b) => b - a); // [20, 10, 3, 2, 1] — descending
```
> Always pass a comparator to `sort` for numbers. `a - b` ascending, `b - a` descending. The comparator returns negative (a first), positive (b first), or 0 (keep order).

### Searching
```js
const arr = [10, 20, 30, 20];
arr.indexOf(20)             // 1   (first match, or -1)
arr.lastIndexOf(20)         // 3
arr.includes(30)            // true
arr.find(x => x > 15)       // 20  (first element matching predicate)
arr.findIndex(x => x > 15)  // 1
arr.some(x => x > 25)       // true  (at least one matches)
arr.every(x => x > 5)       // true  (all match)
```

---

## IV. DESTRUCTURING — UNPACK WITH STYLE

Destructuring pulls values out of arrays/objects into variables in one line.

### Array destructuring
```js
const [first, second, third] = [1, 2, 3];
// first = 1, second = 2, third = 3

const [a, , c] = [1, 2, 3];        // skip with a hole → a=1, c=3
const [head, ...tail] = [1, 2, 3]; // head=1, tail=[2,3]
const [x = 10, y = 20] = [1];      // defaults → x=1, y=20

// Swap without a temp variable
let p = 1, q = 2;
[p, q] = [q, p];                   // p=2, q=1
```

### Object destructuring
```js
const user = { name: "Ada", age: 36, role: "admin" };

const { name, age } = user;        // name="Ada", age=36
const { role: title } = user;      // rename → title="admin"
const { country = "UK" } = user;   // default → country="UK" (key absent)
const { name: n, ...rest } = user; // n="Ada", rest={age:36, role:"admin"}
```

### Destructuring in function parameters (extremely common)
```js
// Instead of accessing props.name, props.age repeatedly:
function greet({ name, age = 0 }) {
  return `${name} is ${age}`;
}
greet({ name: "Ada", age: 36 }); // "Ada is 36"
greet({ name: "Grace" });        // "Grace is 0"

// Nested destructuring
const config = { db: { host: "localhost", port: 5432 } };
const { db: { host, port } } = config; // host="localhost", port=5432
```

> This is exactly how React components read their props: `function Button({ label, onClick }) { ... }`.

---

## V. SPREAD & REST — `...` IN TWO ROLES

The `...` operator does two opposite things depending on context.

### Spread — expand an iterable into individual elements
```js
// In arrays
const a = [1, 2], b = [3, 4];
const combined = [...a, ...b];        // [1,2,3,4]
const copy = [...a];                  // shallow copy
const withExtra = [0, ...a, 5];       // [0,1,2,5]

// In objects (merge / clone / override)
const base = { a: 1, b: 2 };
const merged = { ...base, b: 99, c: 3 }; // {a:1, b:99, c:3} — later wins
const clone = { ...base };               // shallow clone

// In function calls (expand array into arguments)
const nums = [5, 1, 8, 3];
Math.max(...nums);                    // 8
const str = "hi";
[...str];                             // ["h", "i"] — strings are iterable
```

### Rest — gather multiple elements into one
```js
// In function parameters (see file 02)
function sum(...nums) { return nums.reduce((a, b) => a + b, 0); }

// In destructuring
const [first, ...others] = [1, 2, 3, 4]; // first=1, others=[2,3,4]
const { id, ...data } = { id: 1, x: 2, y: 3 }; // id=1, data={x:2,y:3}
```

> **Memory aid:** spread *spreads things out* (right-hand side / arguments). Rest *gathers the rest* (left-hand side / parameters).

---

## VI. THE BIG THREE: map / filter / reduce ⭐

These three methods replace the vast majority of `for` loops in modern JavaScript. They are **non-mutating** (return new arrays/values) and **chainable**. Learning to think in terms of these is a major step toward fluency.

### `map` — transform every element (n in → n out)
```js
const nums = [1, 2, 3, 4];

const doubled = nums.map(n => n * 2);          // [2, 4, 6, 8]
const strings = nums.map(n => `#${n}`);        // ["#1","#2","#3","#4"]

// Real-world: reshape objects
const users = [{ id: 1, name: "Ada" }, { id: 2, name: "Grace" }];
const names = users.map(u => u.name);          // ["Ada", "Grace"]
const options = users.map(u => ({ value: u.id, label: u.name }));

// The callback also gets index and the whole array
nums.map((n, i) => `${i}:${n}`);               // ["0:1","1:2","2:3","3:4"]
```
> `map` always returns an array of the **same length**. If you find yourself returning nothing for some elements, you want `filter` (or `reduce`).

### `filter` — keep elements that pass a test (n in → ≤n out)
```js
const nums = [1, 2, 3, 4, 5, 6];

const evens = nums.filter(n => n % 2 === 0);   // [2, 4, 6]
const big = nums.filter(n => n > 3);           // [4, 5, 6]

// Real-world
const users = [
  { name: "Ada", active: true },
  { name: "Grace", active: false },
  { name: "Linus", active: true },
];
const activeUsers = users.filter(u => u.active);     // Ada, Linus

// Remove falsy values (common idiom)
[0, 1, "", "hi", null, 5].filter(Boolean);     // [1, "hi", 5]
```

### `reduce` ⭐ — fold an array into a single value (n in → 1 out)
`reduce` is the most powerful and most feared. It walks the array carrying an **accumulator**, applying your function at each step. `map` and `filter` can both be written in terms of `reduce`.

```js
// Signature: arr.reduce((accumulator, current) => newAccumulator, initialValue)

// Sum
const total = [1, 2, 3, 4].reduce((acc, n) => acc + n, 0); // 10
// Step-by-step: acc=0,n=1→1 | acc=1,n=2→3 | acc=3,n=3→6 | acc=6,n=4→10

// Max
const max = [3, 7, 2, 9, 4].reduce((acc, n) => Math.max(acc, n), -Infinity); // 9

// Count occurrences → frequency map
const fruits = ["apple", "banana", "apple", "cherry", "banana", "apple"];
const counts = fruits.reduce((acc, fruit) => {
  acc[fruit] = (acc[fruit] || 0) + 1;
  return acc;
}, {});
// { apple: 3, banana: 2, cherry: 1 }

// Group by a property
const people = [
  { name: "Ada", dept: "eng" },
  { name: "Grace", dept: "eng" },
  { name: "Linus", dept: "ops" },
];
const byDept = people.reduce((acc, p) => {
  (acc[p.dept] ||= []).push(p.name);   // ||= creates the array if missing
  return acc;
}, {});
// { eng: ["Ada", "Grace"], ops: ["Linus"] }

// Flatten one level
const nested = [[1, 2], [3, 4], [5]];
const flat = nested.reduce((acc, arr) => acc.concat(arr), []); // [1,2,3,4,5]
```

> ⚠️ **Always pass the initial value** (the second argument). Without it, `reduce` uses the first element as the seed and starts at index 1 — which breaks on empty arrays (`TypeError`) and behaves differently than you expect.

### Chaining the big three (the payoff)
```js
const orders = [
  { item: "book", price: 12, qty: 2 },
  { item: "pen", price: 1, qty: 10 },
  { item: "laptop", price: 999, qty: 1 },
  { item: "eraser", price: 0.5, qty: 4 },
];

// Total revenue from orders over $5, in one readable pipeline:
const revenue = orders
  .filter(o => o.price > 5)              // keep book & laptop
  .map(o => o.price * o.qty)             // [24, 999]
  .reduce((sum, total) => sum + total, 0); // 1023

console.log(revenue); // 1023
```
This declarative pipeline says *what* you want, not *how* to loop. It's the heartbeat of modern JS data work.

### Other essential iteration methods
```js
[1, 2, 3].forEach(n => console.log(n));   // side effects only, returns undefined
[[1, 2], [3, 4]].flat();                  // [1,2,3,4] — flatten one level
[1, 2, 3].flatMap(n => [n, n * 10]);      // [1,10,2,20,3,30] — map then flat
Array.from({ length: 3 }, (_, i) => i);   // [0, 1, 2] — generate
Array(5).fill(0);                         // [0,0,0,0,0]
```

---

## VII. COMMON PITFALLS & GOTCHAS

**1. Mutating when you meant to copy**
```js
const sorted = arr.sort();   // ⚠️ also mutates arr! sort is in-place
const safe = [...arr].sort((a, b) => a - b); // copy first
```

**2. `forEach` can't be broken or chained**
```js
[1, 2, 3].forEach(n => { if (n === 2) return; }); // `return` only skips, can't break
// Use a for...of loop with break, or .some()/.find() to stop early.
```

**3. Shallow copy on nested data**
```js
const copy = { ...original };  // nested objects are still shared references
```

**4. `reduce` without an initial value on an empty array**
```js
[].reduce((a, b) => a + b);     // ❌ TypeError: Reduce of empty array with no initial value
[].reduce((a, b) => a + b, 0);  // ✅ 0
```

**5. Sparse arrays / holes behave oddly**
```js
[1, , 3].map(x => x * 2);   // [2, <hole>, 6] — map skips holes
```

**6. Comparing arrays/objects with `===`**
```js
[1, 2] === [1, 2];          // false — different references
JSON.stringify([1,2]) === JSON.stringify([1,2]); // true (cheap deep-equal hack)
```

---

## VIII. KEY TAKEAWAYS

- Objects map keys to values; access with `.key` or `["key"]` (brackets for dynamic/odd keys).
- Objects and arrays are held **by reference** — assignment shares, it doesn't copy. `===` compares references.
- **Shallow copy** (`{...obj}`, `[...arr]`) copies the top level only; nested objects stay shared. Use `structuredClone` for deep copies.
- **Destructuring** unpacks arrays/objects into variables, including in function parameters (how React reads props).
- `...` is **spread** (expand) on the right/in calls, and **rest** (gather) on the left/in parameters.
- **`map`** transforms (same length), **`filter`** selects (≤ length), **`reduce ⭐`** folds to a single value (any shape). Chain them for declarative data pipelines.
- Always pass `reduce` an **initial value**; always pass `sort` a **comparator** for numbers.
- Prefer **non-mutating** methods (`map`, `filter`, `slice`, `concat`, spread) over mutating ones (`push`, `splice`, `sort`, `reverse`) when working with shared state.

---

**← Prev:** [`02-Functions-And-Scope.md`](./02-Functions-And-Scope.md) | **→ Next:** [`04-The-This-Keyword-And-Prototypes.md`](./04-The-This-Keyword-And-Prototypes.md) | **Index:** [`00-Index.md`](./00-Index.md)
