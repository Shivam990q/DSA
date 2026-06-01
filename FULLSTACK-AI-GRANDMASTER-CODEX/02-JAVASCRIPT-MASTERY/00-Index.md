# ⚡ JavaScript Mastery

> *"Frameworks change; fundamentals compound. Master JavaScript, not just React."*

The language of the web — and increasingly, of the server, the build tools, the desktop, and the edge. This section takes you from `let x = 5` to closures, the event loop, prototypes, and the advanced patterns that separate the people who *use* JavaScript from the people who *understand* it.

---

## 📚 Contents

1. [`01-JS-Fundamentals.md`](./01-JS-Fundamentals.md) — Variables (`let`/`const`/`var`), data types, operators, type coercion, truthy/falsy
2. [`02-Functions-And-Scope.md`](./02-Functions-And-Scope.md) — Declarations vs expressions, arrow functions, scope, hoisting, **closures ⭐**, IIFE
3. [`03-Objects-And-Arrays.md`](./03-Objects-And-Arrays.md) — Objects, arrays, destructuring, spread/rest, **`map`/`filter`/`reduce` ⭐**
4. [`04-The-This-Keyword-And-Prototypes.md`](./04-The-This-Keyword-And-Prototypes.md) — `this` binding, `call`/`apply`/`bind`, prototypal inheritance, classes
5. [`05-Asynchronous-JavaScript.md`](./05-Asynchronous-JavaScript.md) — Callbacks, **promises ⭐**, **async/await ⭐**, the event loop, microtasks/macrotasks, `fetch`
6. [`06-ES6-Plus-Features.md`](./06-ES6-Plus-Features.md) — Modules, template literals, default params, optional chaining, nullish coalescing, `Map`/`Set`, generators, iterators
7. [`07-The-DOM-And-Events.md`](./07-The-DOM-And-Events.md) — Selecting/manipulating the DOM, event listeners, delegation, bubbling/capturing
8. [`08-Advanced-JS-Patterns.md`](./08-Advanced-JS-Patterns.md) — Currying, debounce/throttle, memoization, the module pattern, interview questions

---

## 🧭 Recommended Learning Order

JavaScript is best learned **linearly first, then circularly**. Walk 01 → 08 in order — each file leans on the previous one. Then come back to the ⭐ files (closures, `reduce`, promises, async/await) and re-read them until they feel obvious. Those four concepts are where most "JavaScript is confusing" pain lives, and where most interview questions hide.

```
01 Fundamentals
   │  (you can now read any snippet)
02 Functions & Scope ──────► closures unlock everything
   │
03 Objects & Arrays ───────► reduce unlocks data transformation
   │
04 this & Prototypes ──────► how OOP works in JS
   │
05 Async ──────────────────► promises + event loop = real apps
   │
06 ES6+ ───────────────────► modern syntax you'll see everywhere
   │
07 DOM & Events ───────────► making pages interactive
   │
08 Advanced Patterns ──────► the senior-engineer toolkit
```

### How to study each file
- **Type the examples** into a browser console or a `.js` file run with Node. Reading code teaches you nothing; running and breaking it teaches you everything.
- **Predict before you run.** Guess the output, then check. Every wrong guess is a gap closed.
- **Re-read the "Common Pitfalls" sections.** They are the bugs you would otherwise ship.

---

## 🛠️ How to Run These Examples

You have three zero-setup options:

**1. Browser console** — open any browser, press `F12`, click *Console*, paste code, hit Enter.

**2. Node.js** — install [Node](https://nodejs.org), save code to `demo.js`, run:
```bash
node demo.js
```

**3. Online** — [PlayCode](https://playcode.io), [CodeSandbox](https://codesandbox.io), or the [MDN Playground](https://developer.mozilla.org/en-US/play).

Examples marked `// browser-only` use the DOM and must run in a browser. Everything else runs anywhere.

---

## 📌 Deep References
- **[MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)** — the canonical reference ⭐
- **[javascript.info](https://javascript.info)** — the best free deep-dive tutorial ⭐
- **[You Don't Know JS Yet](https://github.com/getify/You-Dont-Know-JS)** (Kyle Simpson) — for when you want to go to the metal
- **[ECMAScript spec](https://tc39.es/ecma262/)** — the law itself (advanced)

---

**→ Start:** [`01-JS-Fundamentals.md`](./01-JS-Fundamentals.md) | Back to [`../README.md`](../README.md)
