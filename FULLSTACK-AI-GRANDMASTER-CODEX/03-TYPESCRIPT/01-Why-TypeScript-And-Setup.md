# 🔷 Why TypeScript & Setup

> *"Types are documentation that can't go stale, and tests you don't have to write."*

Before learning the syntax, understand *why* TypeScript exists, what problems it solves, and how it actually works — because TypeScript is unusual: it's a language that compiles to *another language you already know*, and then disappears entirely at runtime.

---

## I. WHAT PROBLEM DOES TYPESCRIPT SOLVE?

JavaScript is dynamically typed: a variable's type is only known at runtime, and type errors blow up *while the program runs* — often in production, often far from the actual mistake.

```js
// Plain JavaScript — all of these are silent bugs until they explode
function getUserName(user) {
  return user.name.toUpperCase();
}

getUserName({ name: "Ada" });   // "ADA" ✅
getUserName({ username: "Ada" });// 💥 TypeError: Cannot read 'toUpperCase' of undefined
getUserName(null);               // 💥 crash
getUserName("Ada");              // 💥 "Ada".name is undefined
```
Nothing warned you. The bug surfaces only when that exact call happens, maybe months later.

TypeScript adds a **static type system**: you declare the shapes your code expects, and a **compiler checks them before the code ever runs**.

```ts
interface User {
  name: string;
}

function getUserName(user: User): string {
  return user.name.toUpperCase();
}

getUserName({ name: "Ada" });    // ✅ ok
getUserName({ username: "Ada" });// ❌ compile error: 'username' not assignable to 'User'
getUserName(null);               // ❌ compile error: null not assignable to 'User'
getUserName("Ada");              // ❌ compile error: string not assignable to 'User'
```
The bugs are caught at your desk, in your editor, with a red squiggle — not in production.

### The concrete benefits
- **Catch bugs early** — type errors surface at compile time, not runtime.
- **Better tooling** — autocomplete, go-to-definition, inline docs, and safe rename across the whole codebase.
- **Fearless refactoring** — change a type and the compiler shows you every spot that needs updating.
- **Self-documenting code** — the types *are* the documentation, and they can't drift out of date.
- **Scales to large teams/codebases** — the bigger the project, the more TypeScript pays off.

### The honest tradeoffs
- **A build step** — `.ts` must be compiled to `.js` (or run with a TS-aware runner).
- **A learning curve** — generics and advanced types take time.
- **Some verbosity** — though inference removes most of it.
- **Types are not runtime guarantees** — they vanish after compilation (more on this below).

---

## II. HOW TYPESCRIPT WORKS — THE MENTAL MODEL

This is the single most important thing to understand:

> **TypeScript is JavaScript + types, and the types are *erased* during compilation. At runtime, there is no TypeScript — only plain JavaScript.**

```ts
// What you write (TypeScript)
function add(a: number, b: number): number {
  return a + b;
}
const result: number = add(2, 3);
```
```js
// What actually runs (compiled JavaScript) — types are GONE
function add(a, b) {
  return a + b;
}
const result = add(2, 3);
```

### The two phases
```
┌──────────────┐   tsc (type check    ┌──────────────┐   node / browser
│  your .ts    │   + strip types)     │  plain .js   │   runs this
│  code        │ ───────────────────► │  output      │ ──────────────►
└──────────────┘                      └──────────────┘
   COMPILE TIME                          RUN TIME
   (types exist,                         (types gone,
    errors reported)                      pure JS)
```

### The crucial consequence: types can't validate runtime data
Because types disappear, they cannot check data that arrives *at runtime* — API responses, user input, `JSON.parse` results. TypeScript trusts your annotations.

```ts
// This compiles fine, but if the API lies, it crashes at runtime
const user = await fetch("/api/user").then(r => r.json()) as User;
user.name.toUpperCase();   // 💥 at runtime if the API didn't send a `name`
```
> For runtime validation of external data, use a schema library like **[Zod](https://zod.dev)** alongside TypeScript. Types guard your code; Zod guards your boundaries.

---

## III. INSTALLING & COMPILING

### Install
```bash
# Per-project (recommended — pins the version)
npm install --save-dev typescript

# Global (handy for quick experiments)
npm install -g typescript

# Check the version
npx tsc --version
```

### Compile a file
```ts
// hello.ts
const message: string = "Hello, TypeScript!";
console.log(message);
```
```bash
npx tsc hello.ts        # emits hello.js next to it
node hello.js           # run the output
```

### Watch mode (recompile on save)
```bash
npx tsc --watch         # or: npx tsc -w
```

### Run TypeScript directly (no manual compile)
```bash
npx tsx hello.ts        # tsx: fast, zero-config TS runner
# or the older: npx ts-node hello.ts
```

---

## IV. `tsconfig.json` — THE PROJECT'S BRAIN

A `tsconfig.json` at the project root configures how `tsc` behaves. Generate a commented starter with:
```bash
npx tsc --init
```

A sensible modern config:
```jsonc
{
  "compilerOptions": {
    /* What JS version to emit and which built-in APIs to assume */
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],

    /* Module system */
    "module": "ESNext",
    "moduleResolution": "Bundler",   // or "NodeNext" for Node projects

    /* Output */
    "outDir": "./dist",              // where .js files go
    "rootDir": "./src",              // where .ts files live
    "sourceMap": true,               // .map files for debugging TS in the browser

    /* TYPE-CHECKING STRICTNESS — turn it all on */
    "strict": true,                  // ⭐ the master switch (see below)
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,

    /* Interop & quality of life */
    "esModuleInterop": true,
    "skipLibCheck": true,            // skip type-checking node_modules .d.ts (faster)
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### The most important option: `"strict": true` ⭐
`strict` is a bundle of safety flags. **Always turn it on for new projects** — it's the difference between TypeScript actually protecting you and merely decorating your code. It enables, among others:

- **`strictNullChecks`** — `null` and `undefined` must be handled explicitly (the single biggest win).
- **`noImplicitAny`** — you can't accidentally leave something untyped (an implicit `any` silently disables checking).
- **`strictFunctionTypes`**, **`strictBindCallApply`**, and more.

```ts
// With strictNullChecks ON:
function firstChar(s: string) {
  return s[0].toUpperCase();
}
let name: string | null = getName();
firstChar(name);   // ❌ error: 'name' is possibly null — you MUST handle it
if (name) firstChar(name);  // ✅ narrowed to string inside the guard
```

### `any` vs `unknown` — the escape hatches
```ts
let a: any;        // ❌ disables all checking — "trust me", the bug magnet. Avoid.
a.foo.bar.baz();   // compiles, crashes at runtime — any defeats the point of TS

let u: unknown;    // ✅ the SAFE "I don't know the type yet"
u.toUpperCase();   // ❌ error — must narrow first
if (typeof u === "string") u.toUpperCase(); // ✅ now allowed
```
> Prefer `unknown` over `any` for values of uncertain type (like `JSON.parse` output). `unknown` forces you to check before use; `any` silently throws away all safety.

---

## V. A FIRST REAL TASTE

```ts
// types describe intent; the compiler enforces it
type Status = "active" | "inactive" | "banned";   // union of literals

interface User {
  id: number;
  name: string;
  email: string;
  status: Status;
  lastLogin?: Date;              // ? = optional
}

function activate(user: User): User {
  return { ...user, status: "active" };
}

const ada: User = {
  id: 1,
  name: "Ada",
  email: "ada@x.io",
  status: "inactive",
};

activate(ada);                   // ✅
activate({ id: 2, name: "G" });  // ❌ missing email & status — caught now
const bad: Status = "deleted";   // ❌ not one of the allowed literals
```
Everything above is covered in depth in the next files — but notice how much the compiler already protects, before a single line runs.

---

## VI. COMMON PITFALLS & GOTCHAS

**1. Expecting types to exist at runtime**
```ts
if (typeof value === "User") {}   // ❌ "User" isn't a runtime value; types are erased
// Use a runtime check on a property, or a validation library.
```

**2. Reaching for `any` to silence errors**
```ts
const data: any = fetchStuff();   // ❌ you just turned TypeScript off for `data`
// Use `unknown` and narrow, or define the real type.
```

**3. Not enabling `strict`** — without it, `null` bugs and implicit `any` sail right through. Turn it on from day one.

**4. Casting with `as` to force-fit shapes**
```ts
const user = {} as User;          // ❌ lies to the compiler; crashes later
// `as` should be rare and deliberate, not a way to dodge real errors.
```

**5. Confusing compile errors with runtime errors** — TypeScript errors stop the *build* (or just warn in some setups); they don't appear when the JS runs.

---

## VII. KEY TAKEAWAYS

- TypeScript is **JavaScript + a static type system**; the compiler (`tsc`) **checks types, then erases them**, emitting plain JavaScript.
- Benefits: **early bug detection, great tooling, safe refactoring, self-documenting code** — and the value grows with project size.
- **Types don't exist at runtime.** They can't validate API responses or user input — use a schema library (Zod) at your boundaries for that.
- Configure projects with **`tsconfig.json`**; the most important setting is **`"strict": true`** — always enable it.
- Prefer **`unknown`** over **`any`** for uncertain values: `unknown` forces a check, `any` disables all safety.
- Compile with `tsc` (or `tsc --watch`), or run directly with `tsx`/`ts-node`.

---

**← Prev:** [`00-Index.md`](./00-Index.md) | **→ Next:** [`02-Types-And-Interfaces.md`](./02-Types-And-Interfaces.md) | **Index:** [`00-Index.md`](./00-Index.md)
