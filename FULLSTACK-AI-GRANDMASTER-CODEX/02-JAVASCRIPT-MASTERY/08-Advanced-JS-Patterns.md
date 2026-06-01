# 🧙 Advanced JavaScript Patterns

> *"These are the techniques that show up in senior interviews and in the source code of every library you admire."*

You now know the language. This file is the toolkit that separates competent from senior: **currying**, **debounce/throttle**, **memoization**, the **module pattern**, and the interview questions that test whether you really understand closures, `this`, and the event loop. Every pattern here is built on the fundamentals from files 02–06 — especially closures.

---

## I. CURRYING

**Currying** transforms a function of many arguments into a chain of functions each taking one argument. It enables partial application — locking in some arguments now, supplying the rest later.

```js
// Normal function
function add(a, b, c) { return a + b + c; }
add(1, 2, 3);   // 6

// Curried version
function addCurried(a) {
  return function (b) {
    return function (c) {
      return a + b + c;
    };
  };
}
addCurried(1)(2)(3);   // 6

// Arrow form (concise)
const addC = a => b => c => a + b + c;
addC(1)(2)(3);   // 6
```

### Partial application — the practical payoff
```js
const add = a => b => a + b;
const add10 = add(10);     // lock in a=10, get a reusable function
add10(5);    // 15
add10(20);   // 30

// Real-world: build specialized functions from a general one
const log = level => message => console.log(`[${level}] ${message}`);
const logError = log("ERROR");
const logInfo = log("INFO");
logError("Database down");   // [ERROR] Database down
logInfo("Server started");   // [INFO] Server started
```

### A generic `curry` utility (interview favorite)
```js
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {        // enough args? call it
      return fn.apply(this, args);
    }
    // otherwise return a function that collects more
    return (...next) => curried.apply(this, [...args, ...next]);
  };
}

const sum = (a, b, c) => a + b + c;
const curriedSum = curry(sum);
curriedSum(1)(2)(3);      // 6
curriedSum(1, 2)(3);      // 6
curriedSum(1)(2, 3);      // 6
curriedSum(1, 2, 3);      // 6  — all equivalent
```
> Currying relies on **closures** (each returned function remembers earlier args) and `fn.length` (the declared parameter count). Libraries like Lodash/Ramda lean on it heavily for composable, point-free code.

---

## II. DEBOUNCE & THROTTLE

Both limit how often a function runs in response to rapid-fire events (typing, scrolling, resizing). They solve different problems.

### Debounce — "wait until the user stops"
Runs the function only after a quiet period with no new calls. Perfect for search-as-you-type and validating input.

```js
function debounce(fn, delay) {
  let timerId;
  return function (...args) {
    clearTimeout(timerId);                   // cancel the pending call
    timerId = setTimeout(() => fn.apply(this, args), delay); // reschedule
  };
}

// Usage: only search 300ms after the user stops typing
const search = debounce((query) => {
  console.log("Searching for:", query);      // hits the API
}, 300);

input.addEventListener("input", (e) => search(e.target.value));
// Typing "hello" fires 5 input events but only ONE search, after the pause.
```

```
input events: h  e  l  l  o
                              └── 300ms quiet ──► search("hello") runs ONCE
```

### Throttle — "at most once every N ms"
Runs the function at a steady maximum rate, ignoring extra calls in between. Perfect for scroll/resize/mousemove handlers.

```js
function throttle(fn, limit) {
  let waiting = false;
  return function (...args) {
    if (waiting) return;                     // in cooldown — ignore
    fn.apply(this, args);                    // run now
    waiting = true;
    setTimeout(() => { waiting = false; }, limit); // open the gate after limit
  };
}

// Usage: handle scroll at most every 200ms
const onScroll = throttle(() => {
  console.log("scroll position:", window.scrollY);
}, 200);
window.addEventListener("scroll", onScroll);
```

```
scroll events: ▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮  (fired constantly)
throttled:     ▮     ▮     ▮      (runs every 200ms max)
```

### When to use which
| Scenario | Use |
|----------|-----|
| Search box, autosave, validating input | **Debounce** (act after they stop) |
| Scroll position, window resize, mousemove, infinite scroll | **Throttle** (steady cadence) |
| Button double-click prevention | **Throttle** with `{ leading: true }` (or `once`) |

> Both are closures: the returned function remembers `timerId`/`waiting` across calls. This is *the* classic "implement debounce from scratch" interview question — practice writing both from memory.

---

## III. MEMOIZATION

**Memoization** caches a function's results by its arguments, so repeated calls with the same input return instantly. It trades memory for speed and only works for **pure** functions (same input → same output, no side effects).

```js
function memoize(fn) {
  const cache = new Map();                   // closure-held cache
  return function (...args) {
    const key = JSON.stringify(args);        // simple key (see caveat below)
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const slowSquare = (n) => {
  for (let i = 0; i < 1e8; i++) {}           // simulate expensive work
  return n * n;
};
const fastSquare = memoize(slowSquare);
fastSquare(5);   // slow first time → 25
fastSquare(5);   // instant (cached) → 25
```

### Memoization shines on recursive problems
```js
// Naive Fibonacci — O(2^n), recomputes the same values exponentially
function fib(n) {
  return n < 2 ? n : fib(n - 1) + fib(n - 2);
}
// fib(40) ≈ 1+ billion calls 😱

// Memoized — O(n), each value computed once
const memoFib = memoize(function fib(n) {
  return n < 2 ? n : memoFib(n - 1) + memoFib(n - 2);
});
memoFib(40);    // instant
memoFib(100);   // still instant (within Number precision)
```
> ⚠️ The `JSON.stringify` key works for simple arguments but fails for functions, circular structures, or when key order matters. For single-primitive-arg functions, use the arg directly as the `Map` key. This is the same caching trick React's `useMemo`/`useCallback` apply to render performance.

---

## IV. THE MODULE PATTERN

Before ES modules, the **module pattern** used an IIFE + closure to create private state and a public interface. You'll still see it in older code and library bundles — and the concept (encapsulation via closures) is timeless.

```js
const Counter = (function () {
  // ---- private (closure) ----
  let count = 0;
  function validate(n) { return typeof n === "number"; }

  // ---- public interface ----
  return {
    increment() { count++; return count; },
    decrement() { count--; return count; },
    reset() { count = 0; },
    get value() { return count; },
  };
})();

Counter.increment();   // 1
Counter.increment();   // 2
Counter.value;         // 2
Counter.count;         // undefined — truly private
```

### The revealing module pattern (define privately, reveal selectively)
```js
const UserService = (function () {
  let users = [];                            // private state

  function add(user) { users.push(user); }
  function getAll() { return [...users]; }   // return a copy, protect internals
  function count() { return users.length; }

  return { add, getAll, count };             // reveal only these
})();

UserService.add({ name: "Ada" });
UserService.count();    // 1
UserService.users;      // undefined — encapsulated
```
> Modern equivalent: an ES module (file 06) where un-exported variables are automatically private. Same goal — encapsulation — different mechanism.

---

## V. FUNCTION COMPOSITION & PIPELINES

Combine small functions into bigger ones — the functional-programming counterpart to OOP.

```js
// compose: right-to-left (math style: compose(f, g)(x) = f(g(x)))
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

// pipe: left-to-right (reads like a pipeline)
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const trim = s => s.trim();
const lower = s => s.toLowerCase();
const exclaim = s => s + "!";

const shout = pipe(trim, lower, exclaim);
shout("  Hello  ");      // "hello!"

const shout2 = compose(exclaim, lower, trim);
shout2("  Hello  ");     // "hello!" (same result, reversed order)
```

---

## VI. OTHER PATTERNS WORTH KNOWING

### Singleton (one shared instance)
```js
const Config = (function () {
  let instance;
  function create() { return { apiUrl: "https://api.io", version: "1.0" }; }
  return { getInstance() { return instance || (instance = create()); } };
})();
Config.getInstance() === Config.getInstance();   // true — same object
```

### Observer / pub-sub (event emitter)
```js
function createEmitter() {
  const listeners = {};
  return {
    on(event, cb) { (listeners[event] ||= []).push(cb); },
    emit(event, data) { (listeners[event] || []).forEach(cb => cb(data)); },
    off(event, cb) {
      listeners[event] = (listeners[event] || []).filter(l => l !== cb);
    },
  };
}
const bus = createEmitter();
bus.on("login", user => console.log(`${user} logged in`));
bus.emit("login", "Ada");   // "Ada logged in"
```

### Factory function
```js
function createUser(name, role = "user") {
  return {
    name,
    role,
    isAdmin() { return this.role === "admin"; },
  };
}
const admin = createUser("Ada", "admin");
admin.isAdmin();   // true
```

---

## VII. COMMON INTERVIEW QUESTIONS (with answers)

**Q1: What's the output?**
```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);
}
// → 3, 3, 3.  `var` shares one binding; by the time callbacks run, i is 3.
// Fix: use `let`, or an IIFE to capture each value. (See file 02.)
```

**Q2: Explain the output order.**
```js
console.log(1);
setTimeout(() => console.log(2), 0);
Promise.resolve().then(() => console.log(3));
console.log(4);
// → 1, 4, 3, 2.  Sync first (1,4), then microtasks/promises (3),
//   then macrotasks/timers (2). (See file 05, event loop.)
```

**Q3: What does this print, and why?**
```js
const obj = {
  name: "Codex",
  greet: function () { return this.name; },
  greetArrow: () => this.name,
};
obj.greet();      // "Codex" — regular method, `this` is obj
obj.greetArrow(); // undefined — arrow captured outer `this`, not obj
// (See file 04, `this` binding.)
```

**Q4: Implement debounce.** → Section II above. Be ready to write it from scratch.

**Q5: Difference between `==` and `===`?** → `==` coerces types before comparing; `===` doesn't. Always use `===`. (File 01.)

**Q6: What is a closure, and give a real use?** → A function that retains access to its birth scope's variables. Used for private state, memoization caches, debounce timers, function factories. (File 02.)

**Q7: `null` vs `undefined`?** → `undefined` = system "no value yet"; `null` = deliberate "no value." `typeof null === "object"` (historic bug). (File 01.)

**Q8: Deep vs shallow copy?** → Shallow copies the top level (`{...obj}`); nested objects stay shared. Deep copy with `structuredClone`. (File 03.)

**Q9: Flatten an array (without `.flat`).**
```js
const flatten = arr =>
  arr.reduce((acc, x) => acc.concat(Array.isArray(x) ? flatten(x) : x), []);
flatten([1, [2, [3, [4]]]]);   // [1, 2, 3, 4]
```

**Q10: Implement `Promise.all`.**
```js
function promiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let done = 0;
    if (promises.length === 0) return resolve(results);
    promises.forEach((p, i) => {
      Promise.resolve(p).then(val => {
        results[i] = val;               // preserve order
        if (++done === promises.length) resolve(results);
      }, reject);                        // reject on first failure
    });
  });
}
```

---

## VIII. KEY TAKEAWAYS

- **Currying** turns `f(a,b,c)` into `f(a)(b)(c)`, enabling partial application and composable, reusable functions. Built on closures.
- **Debounce** waits until activity stops (search, autosave); **throttle** runs at a steady max rate (scroll, resize). Both are closures and classic interview questions — write them from memory.
- **Memoization** caches results of pure functions by argument; it turns exponential recursion (naive Fibonacci) into linear time. It's what `useMemo` does for React.
- The **module pattern** (IIFE + closure) creates private state and a public interface — the pre-ESM ancestor of today's modules.
- **Composition/`pipe`** combines small functions into pipelines — the functional alternative to inheritance.
- The senior-level interview themes are all here: **closures, `this`, the event loop, coercion, copying** — and they trace straight back to files 01–05.

---

**← Prev:** [`07-The-DOM-And-Events.md`](./07-The-DOM-And-Events.md) | **→ Next:** [`../03-TYPESCRIPT/00-Index.md`](../03-TYPESCRIPT/00-Index.md) | **Index:** [`00-Index.md`](./00-Index.md)
