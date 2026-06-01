# 🔷 TypeScript

> *"JavaScript that scales. TypeScript catches at compile time the bugs JavaScript hands you at 3am in production."*

TypeScript is JavaScript with a **static type system** bolted on top. You write types; the TypeScript compiler checks them and then erases them, emitting plain JavaScript that runs anywhere. The payoff: bugs caught before you run the code, fearless refactoring, and an editor that actually understands your program.

This section assumes you've worked through [`../02-JAVASCRIPT-MASTERY/`](../02-JAVASCRIPT-MASTERY/00-Index.md) — TypeScript only makes sense once JavaScript does.

---

## 📚 Contents

1. [`01-Why-TypeScript-And-Setup.md`](./01-Why-TypeScript-And-Setup.md) — What TS solves, installing, `tsconfig.json`, the compilation model
2. [`02-Types-And-Interfaces.md`](./02-Types-And-Interfaces.md) — Primitives, arrays, tuples, enums, interfaces vs types, union/intersection
3. [`03-Generics-And-Advanced-Types.md`](./03-Generics-And-Advanced-Types.md) — **Generics ⭐**, utility types (`Partial`/`Pick`/`Omit`/`Record`), conditional & mapped types
4. [`04-TypeScript-With-React.md`](./04-TypeScript-With-React.md) — Typing props, state, hooks, and events in React

---

## 🧭 Recommended Learning Order

Walk 01 → 04 in order. The first two files give you everything you need for 90% of day-to-day TypeScript. File 03 (**generics**) is the conceptual leap that unlocks reusable, library-grade code — give it real time. File 04 ties it all to React, where most TypeScript is actually written today.

```
01 Why & Setup ──────► get the compiler running, understand the model
   │
02 Types & Interfaces ► describe the shape of your data (the daily 90%)
   │
03 Generics ⭐ ───────► reusable types; the senior-level leap
   │
04 TS + React ───────► where you'll actually use all of it
```

### How to study
- **Use the [TypeScript Playground](https://www.typescriptlang.org/play)** — it shows compiler errors and the emitted JavaScript live, side by side. Paste every example.
- **Read the red squiggles.** TypeScript's error messages are verbose but precise. Learning to decode them *is* learning TypeScript.
- **Let inference do the work.** The goal isn't to annotate everything — it's to annotate the boundaries and let TypeScript figure out the rest.

---

## 🛠️ Quick Start

```bash
# Install TypeScript globally (or per-project as a dev dependency)
npm install -g typescript

# Compile a file
tsc hello.ts          # produces hello.js

# Or run TS directly without compiling (great for scripts)
npx tsx hello.ts      # via the `tsx` runner
```
```ts
// hello.ts
const greeting: string = "Hello, TypeScript";
console.log(greeting);
```

Zero-install alternative: the **[TypeScript Playground](https://www.typescriptlang.org/play)** runs entirely in your browser.

---

## 🌟 Why It's Worth It

```ts
// JavaScript: this bug ships to production
function getDiscount(price, percent) {
  return price - price * percent;
}
getDiscount(100, "20");   // "100-2000" worth of nonsense, no warning

// TypeScript: the bug never compiles
function getDiscount(price: number, percent: number): number {
  return price - price * percent;
}
getDiscount(100, "20");
//                ^^^^ Error: Argument of type 'string' is not assignable to 'number'
```

---

## 📌 Deep References
- **[TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)** — the official, well-written guide ⭐
- **[TypeScript Playground](https://www.typescriptlang.org/play)** — experiment with instant feedback ⭐
- **[Type Challenges](https://github.com/type-challenges/type-challenges)** — puzzles to master the type system
- **[Total TypeScript](https://www.totaltypescript.com)** (Matt Pocock) — advanced patterns
- **[React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app)** — for file 04

---

**→ Start:** [`01-Why-TypeScript-And-Setup.md`](./01-Why-TypeScript-And-Setup.md) | Back to [`../README.md`](../README.md)
