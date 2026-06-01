# 🧬 Generics & Advanced Types

> *"Generics are to types what functions are to values: parameters that let you write something once and reuse it everywhere."*

This is the conceptual leap from "I can annotate my variables" to "I can write reusable, library-grade types." We cover **generics ⭐**, the built-in **utility types** you'll use weekly (`Partial`, `Pick`, `Omit`, `Record`...), and the machinery behind them: **conditional** and **mapped** types. Take your time here — this is where TypeScript becomes powerful.

---

## I. GENERICS ⭐ — TYPE PARAMETERS

A generic is a **type variable**: a placeholder for a type that gets filled in when the code is used. It lets one function or type work with many types while staying fully type-safe.

### The problem generics solve
```ts
// Without generics — you either lose type info...
function identityAny(x: any): any { return x; }
const a = identityAny(5);     // a is `any` — type info LOST, no safety

// ...or you duplicate code per type (absurd)
function identityNum(x: number): number { return x; }
function identityStr(x: string): string { return x; }
```

### The generic solution
```ts
function identity<T>(x: T): T {   // T is a type parameter
  return x;
}

const n = identity<number>(5);    // T = number → n is number
const s = identity("hello");      // T inferred as string → s is string
const arr = identity([1, 2, 3]);  // T inferred as number[]
```
`<T>` declares a type variable. The caller (or inference) decides what `T` is, and the return type tracks it exactly. **One function, full type safety, any type.**

### Generic functions in the wild
```ts
// A type-safe "first element"
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}
first([1, 2, 3]);        // number | undefined
first(["a", "b"]);       // string | undefined

// Multiple type parameters
function pair<K, V>(key: K, value: V): [K, V] {
  return [key, value];
}
pair("age", 36);         // [string, number]

// Generic with a default
function makeArray<T = string>(...items: T[]): T[] {
  return items;
}
```

### Generic constraints with `extends`
Often you need `T` to have certain properties. Constrain it.

```ts
// T must have a `.length` property
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}
longest("hello", "hi");      // ✅ strings have length
longest([1, 2, 3], [1]);     // ✅ arrays have length
longest(10, 20);             // ❌ numbers have no length

// Constrain a key to be a real key of an object (very common)
function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
const user = { name: "Ada", age: 36 };
getProp(user, "name");   // string  — TS knows the exact return type
getProp(user, "age");    // number
getProp(user, "email");  // ❌ "email" is not a key of user
```
> `K extends keyof T` is the single most useful generic constraint — it powers type-safe property access across the ecosystem.

### Generic interfaces & classes
```ts
// Generic interface
interface Box<T> {
  value: T;
  getValue(): T;
}
const numBox: Box<number> = { value: 5, getValue() { return this.value; } };

// Generic class — a type-safe stack
class Stack<T> {
  private items: T[] = [];
  push(item: T): void { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
  peek(): T | undefined { return this.items[this.items.length - 1]; }
  get size(): number { return this.items.length; }
}

const numbers = new Stack<number>();
numbers.push(1);
numbers.push(2);
numbers.pop();      // number | undefined
numbers.push("x");  // ❌ not a number

// A reusable API-response wrapper (real-world)
interface ApiResponse<T> {
  data: T;
  status: number;
  error: string | null;
}
type UserResponse = ApiResponse<User>;
type UserListResponse = ApiResponse<User[]>;
```

---

## II. `keyof`, `typeof`, AND INDEXED ACCESS

These operators extract type information from existing types — the building blocks of advanced types.

```ts
// keyof — union of an object type's keys
interface User { id: number; name: string; email: string; }
type UserKeys = keyof User;          // "id" | "name" | "email"

// typeof — get the TYPE of a runtime value
const config = { host: "localhost", port: 5432 };
type Config = typeof config;         // { host: string; port: number }

// Indexed access — look up a property's type
type NameType = User["name"];        // string
type IdOrName = User["id" | "name"]; // number | string

// Combine them: get the type of array elements
const roles = ["admin", "user", "guest"] as const;
type Role = typeof roles[number];    // "admin" | "user" | "guest"
```
> `as const` + `typeof x[number]` is the idiomatic way to derive a literal union from an array of values — no enum needed.

---

## III. UTILITY TYPES (THE WEEKLY TOOLKIT)

TypeScript ships built-in generic types that transform other types. These save enormous boilerplate.

### `Partial<T>` — all properties optional
```ts
interface User { id: number; name: string; email: string; }

// Perfect for update functions where you only send changed fields
function updateUser(id: number, changes: Partial<User>): void { /* ... */ }
updateUser(1, { name: "Grace" });          // ✅ only name
updateUser(1, { email: "g@x.io", id: 2 }); // ✅ any subset
```

### `Required<T>` — all properties required (the opposite)
```ts
interface Config { host?: string; port?: number; }
type FullConfig = Required<Config>;   // { host: string; port: number }
```

### `Readonly<T>` — all properties readonly
```ts
type FrozenUser = Readonly<User>;
const u: FrozenUser = { id: 1, name: "Ada", email: "a@x.io" };
u.name = "Grace";   // ❌ cannot assign to readonly property
```

### `Pick<T, Keys>` — keep only some properties
```ts
type UserPreview = Pick<User, "id" | "name">;   // { id: number; name: string }
```

### `Omit<T, Keys>` — remove some properties
```ts
type UserWithoutEmail = Omit<User, "email">;    // { id: number; name: string }

// Classic use: a "create" type that omits the server-generated id
type NewUser = Omit<User, "id">;                // { name: string; email: string }
function createUser(data: NewUser): User { /* server assigns id */ }
```

### `Record<Keys, Type>` — build an object type from keys + value type
```ts
type Role = "admin" | "user" | "guest";
type Permissions = Record<Role, boolean>;
const perms: Permissions = { admin: true, user: true, guest: false }; // all keys required

// Dictionary of anything
type ScoreBoard = Record<string, number>;
const scores: ScoreBoard = { ada: 90, grace: 85 };
```

### `Exclude`, `Extract`, `NonNullable` — union surgery
```ts
type T = "a" | "b" | "c";
type WithoutA = Exclude<T, "a">;          // "b" | "c"
type OnlyA = Extract<T, "a" | "x">;       // "a"

type Maybe = string | null | undefined;
type Definite = NonNullable<Maybe>;       // string
```

### `ReturnType`, `Parameters`, `Awaited` — extract from functions/promises
```ts
function makeUser(name: string, age: number) {
  return { name, age, createdAt: new Date() };
}
type User = ReturnType<typeof makeUser>;  // { name: string; age: number; createdAt: Date }
type Args = Parameters<typeof makeUser>;  // [name: string, age: number]

type P = Promise<string>;
type Resolved = Awaited<P>;               // string — unwraps the promise
```

### Combining utility types (real-world power)
```ts
interface User { id: number; name: string; email: string; password: string; }

// A safe-to-send-to-client user: drop password, make all optional for patching
type PublicUser = Omit<User, "password">;
type UserPatch = Partial<Omit<User, "id">>;

// A form's initial values: everything optional
type UserForm = Partial<Pick<User, "name" | "email">>;
```

---

## IV. MAPPED TYPES — TRANSFORM EVERY PROPERTY

Mapped types let you create a new type by transforming each property of an existing one. They're how the utility types above are *implemented*.

```ts
// The pattern: { [K in keyof T]: ... }

// Reimplement Readonly
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};

// Reimplement Partial
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};

// Make everything nullable
type Nullable<T> = {
  [K in keyof T]: T[K] | null;
};

interface User { id: number; name: string; }
type NullableUser = Nullable<User>;   // { id: number | null; name: string | null }
```

### Key remapping with `as`
```ts
// Generate getter method names from properties
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
interface Person { name: string; age: number; }
type PersonGetters = Getters<Person>;
// { getName: () => string; getAge: () => number }
```
> The `` `get${...}` `` syntax is a **template literal type** — string manipulation at the type level. `Capitalize`, `Uppercase`, `Lowercase`, and `Uncapitalize` are built-in.

### Mapping modifiers (`+`/`-`)
```ts
// Remove readonly and optional from all properties
type Mutable<T> = {
  -readonly [K in keyof T]-?: T[K];
};
```

---

## V. CONDITIONAL TYPES — TYPE-LEVEL IF/ELSE

A conditional type chooses between two types based on a condition: `T extends U ? X : Y`.

```ts
type IsString<T> = T extends string ? "yes" : "no";
type A = IsString<string>;   // "yes"
type B = IsString<number>;   // "no"

// Practical: unwrap an array element type
type ElementType<T> = T extends (infer U)[] ? U : T;
type E1 = ElementType<number[]>;   // number
type E2 = ElementType<string>;     // string (not an array → itself)
```

### The `infer` keyword — extract a type from within another
```ts
// Pull the resolved type out of a Promise
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;
type R1 = UnwrapPromise<Promise<number>>;  // number
type R2 = UnwrapPromise<string>;           // string

// Pull the return type out of a function (this is how ReturnType works)
type MyReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type Ret = MyReturnType<() => User>;       // User
```

### Distributive conditional types
When the checked type is a union, the condition distributes over each member:
```ts
type ToArray<T> = T extends any ? T[] : never;
type Arrs = ToArray<string | number>;   // string[] | number[]  (distributed)
```

---

## VI. A FULL WORKED EXAMPLE — TYPE-SAFE EVENT EMITTER

Tying generics, mapped types, and constraints together into something you'd actually ship:

```ts
// Define the events and their payload types in one place
interface EventMap {
  login: { userId: number };
  logout: { userId: number; reason: string };
  message: { text: string };
}

class TypedEmitter<Events extends Record<string, any>> {
  private handlers: { [K in keyof Events]?: ((payload: Events[K]) => void)[] } = {};

  on<K extends keyof Events>(event: K, handler: (payload: Events[K]) => void): void {
    (this.handlers[event] ??= []).push(handler);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    this.handlers[event]?.forEach(h => h(payload));
  }
}

const emitter = new TypedEmitter<EventMap>();

emitter.on("login", (p) => console.log(p.userId));        // ✅ p is { userId: number }
emitter.on("logout", (p) => console.log(p.reason));       // ✅ p has reason
emitter.emit("login", { userId: 1 });                     // ✅
emitter.emit("login", { text: "hi" });                    // ❌ wrong payload shape
emitter.emit("unknown", {});                              // ❌ not a known event
```
Every event name autocompletes, every payload is checked against its declared shape, and adding an event to `EventMap` instantly updates the whole API. This is the kind of leverage generics give you.

---

## VII. COMMON PITFALLS & GOTCHAS

**1. Overusing generics where a concrete type would do** — generics earn their keep with *reuse*; don't add `<T>` to a one-off function.

**2. Forgetting constraints, then trying to use properties**
```ts
function len<T>(x: T) { return x.length; }            // ❌ T might not have length
function len<T extends { length: number }>(x: T) { return x.length; } // ✅
```

**3. `any` leaking through a generic**
```ts
function bad<T>(x: T): any { return x; }   // the `any` return throws away T's safety
```

**4. Confusing `extends` in generics (constraint) with `extends` in conditionals (test)** — same keyword, two roles: `<T extends X>` constrains; `T extends X ? A : B` tests.

**5. Reimplementing built-ins** — before writing a mapped type, check if `Partial`/`Pick`/`Omit`/`Record`/`ReturnType` already does it.

---

## VIII. KEY TAKEAWAYS

- **Generics ⭐** are type parameters (`<T>`) — they let one function/class/interface work with many types while preserving full type safety. Inference usually fills `T` in for you.
- **Constrain** generics with `extends` (`T extends { length: number }`, `K extends keyof T`) to safely use properties; `K extends keyof T` is the workhorse for type-safe property access.
- `keyof` (keys as a union), `typeof` (value → type), and indexed access (`T["key"]`) extract type info from existing types.
- **Utility types** — `Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Record`, `Exclude`/`Extract`, `NonNullable`, `ReturnType`/`Parameters`/`Awaited` — eliminate boilerplate. Learn `Partial`, `Pick`, `Omit`, and `Record` cold.
- **Mapped types** (`{ [K in keyof T]: ... }`) transform every property; they're how utility types are built, and support key remapping with `as` + template literal types.
- **Conditional types** (`T extends U ? X : Y`) plus **`infer`** do type-level logic and extraction — the basis of `ReturnType`, `Awaited`, and friends.
- Reach for generics when you need **reuse**; prefer concrete types for one-offs.

---

**← Prev:** [`02-Types-And-Interfaces.md`](./02-Types-And-Interfaces.md) | **→ Next:** [`04-TypeScript-With-React.md`](./04-TypeScript-With-React.md) | **Index:** [`00-Index.md`](./00-Index.md)
