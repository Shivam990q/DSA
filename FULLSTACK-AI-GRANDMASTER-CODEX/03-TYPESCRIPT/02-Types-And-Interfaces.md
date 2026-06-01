# 🧩 Types & Interfaces

> *"Describe the shape of your data, and the compiler will defend it for you."*

This is the daily bread of TypeScript — the 90% you'll use constantly. Primitives, arrays, tuples, enums, the all-important **interfaces vs type aliases**, and the union/intersection operators that let you build precise types out of simple ones.

---

## I. PRIMITIVE & BASIC TYPES

```ts
let name: string = "Ada";
let age: number = 36;            // one type for ints and floats (like JS)
let active: boolean = true;
let nothing: null = null;
let notSet: undefined = undefined;
let big: bigint = 100n;
let id: symbol = Symbol("id");

// Type annotations are often unnecessary — inference handles them:
let city = "London";             // inferred as string
let count = 0;                   // inferred as number
city = 42;                       // ❌ error — city is string
```

### `any`, `unknown`, `never`, `void`
```ts
let a: any;          // disables checking — avoid
let u: unknown;      // safe unknown — must narrow before use

// void: a function that returns nothing meaningful
function log(msg: string): void { console.log(msg); }

// never: a value that never occurs (throws or loops forever)
function fail(msg: string): never { throw new Error(msg); }
function loop(): never { while (true) {} }
```
> `never` seems exotic but is genuinely useful for exhaustiveness checks (shown later) and for narrowing.

### Type inference — let TypeScript do the work
```ts
// ✅ DON'T annotate what TS can infer
const nums = [1, 2, 3];          // number[]
const user = { name: "Ada", age: 36 }; // { name: string; age: number }
const doubled = nums.map(n => n * 2);  // number[] — n inferred as number

// ✅ DO annotate function parameters, public APIs, and ambiguous values
function greet(name: string): string { return `Hi ${name}`; }
```
The rule of thumb: **annotate the boundaries (function params, return types of public APIs, external data), let inference handle the interior.**

---

## II. ARRAYS & TUPLES

### Arrays
```ts
let nums: number[] = [1, 2, 3];
let names: string[] = ["a", "b"];
let flags: Array<boolean> = [true, false]; // generic syntax — equivalent

let matrix: number[][] = [[1, 2], [3, 4]]; // 2D array
let mixed: (string | number)[] = [1, "two", 3]; // array of string OR number

// readonly arrays — can't be mutated
let frozen: readonly number[] = [1, 2, 3];
frozen.push(4);   // ❌ error — push doesn't exist on readonly array
```

### Tuples — fixed-length arrays with typed positions
```ts
let pair: [string, number] = ["Ada", 36];
pair[0].toUpperCase();   // ✅ TS knows [0] is string
pair[1].toFixed(2);      // ✅ TS knows [1] is number
let bad: [string, number] = [36, "Ada"];  // ❌ wrong order

// Named tuple elements (for readability)
let coord: [x: number, y: number] = [10, 20];

// React's useState returns a tuple — that's why this destructuring works:
// const [count, setCount] = useState(0);  → [number, (n: number) => void]

// Tuple with rest
let scores: [string, ...number[]] = ["Ada", 90, 85, 100];
```

---

## III. OBJECT TYPES

```ts
// Inline object type
let user: { name: string; age: number } = { name: "Ada", age: 36 };

// Optional properties with ?
let config: { host: string; port?: number } = { host: "localhost" };

// readonly properties
let point: { readonly x: number; readonly y: number } = { x: 1, y: 2 };
point.x = 5;   // ❌ error — readonly

// Index signatures — objects with dynamic keys
let scores: { [name: string]: number } = {};
scores["Ada"] = 90;
scores["Grace"] = 85;
```

---

## IV. INTERFACES vs TYPE ALIASES ⭐

Both describe the shape of data. They overlap heavily; knowing when to use which is a common interview topic.

### Interface
```ts
interface User {
  id: number;
  name: string;
  email?: string;            // optional
  readonly createdAt: Date;  // can't be reassigned after creation
  greet(): string;           // method
}

const ada: User = {
  id: 1,
  name: "Ada",
  createdAt: new Date(),
  greet() { return `Hi, ${this.name}`; },
};
```

### Type alias
```ts
type User = {
  id: number;
  name: string;
  email?: string;
};

// type can also alias ANYTHING, not just objects:
type ID = string | number;          // union
type Point = [number, number];      // tuple
type Handler = (e: Event) => void;  // function type
type Status = "on" | "off";         // literal union
```

### Interfaces can be extended and merged
```ts
// Extending
interface Animal { name: string; }
interface Dog extends Animal { breed: string; }
const d: Dog = { name: "Rex", breed: "Lab" };

// Declaration merging — same-name interfaces combine (types CANNOT do this)
interface Window { myAppConfig: string; }
interface Window { anotherThing: number; }
// Window now has both — useful for augmenting library/global types
```

### Types can do unions, intersections, and computed types interfaces can't
```ts
type Shape = Circle | Square;        // union — interfaces can't be unions
type Combined = A & B;               // intersection
type Keys = keyof User;              // computed from another type
type Pair<T> = [T, T];               // generic alias
```

### The practical guideline
| Use | When |
|-----|------|
| **`interface`** | Object shapes, especially public APIs and class contracts; when you want `extends` / declaration merging |
| **`type`** | Unions, intersections, tuples, function types, mapped/conditional types, or aliasing primitives |

> In practice: **default to `interface` for object shapes, reach for `type` when you need a union or something an interface can't express.** Either works for most objects — consistency within a codebase matters more than the choice.

---

## V. UNION & INTERSECTION TYPES

### Union (`|`) — "one of these"
```ts
type ID = string | number;
let id: ID = 123;
id = "abc";        // ✅ both allowed
id = true;         // ❌ not string or number

function format(value: string | number): string {
  // must NARROW before using type-specific methods
  if (typeof value === "string") return value.toUpperCase(); // value is string here
  return value.toFixed(2);                                   // value is number here
}
```

### Intersection (`&`) — "all of these combined"
```ts
interface HasName { name: string; }
interface HasAge { age: number; }

type Person = HasName & HasAge;     // must have BOTH
const p: Person = { name: "Ada", age: 36 };  // ✅
const q: Person = { name: "Ada" };           // ❌ missing age
```

### Literal types + unions = precise, self-documenting APIs
```ts
type Direction = "north" | "south" | "east" | "west";
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;

function move(dir: Direction): void { /* ... */ }
move("north");      // ✅
move("up");         // ❌ not a valid Direction — autocomplete even suggests the 4 options
```

### Discriminated unions ⭐ (a pattern you'll use constantly)
Give each member of a union a common literal "tag" property. TypeScript uses it to narrow automatically.

```ts
type Success = { status: "success"; data: string[] };
type Failure = { status: "error"; message: string };
type Result = Success | Failure;     // discriminated by `status`

function handle(result: Result): void {
  if (result.status === "success") {
    console.log(result.data);        // ✅ TS knows it's Success — data exists
  } else {
    console.log(result.message);     // ✅ TS knows it's Failure — message exists
  }
}
```

### Exhaustiveness checking with `never`
```ts
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "square": return shape.side ** 2;
    default:
      // if a new shape is added but not handled, this line errors at compile time
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}
```
> This is a power move: add a new variant to `Shape`, forget to handle it, and the compiler points right at the gap. Self-maintaining code.

---

## VI. ENUMS

Enums give names to a set of related constants.

```ts
enum Direction {
  North,   // 0
  South,   // 1
  East,    // 2
  West,    // 3
}
let d: Direction = Direction.North;
d === 0;   // true — numeric enums are number-backed by default

// String enums (clearer, preferred for most cases)
enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Banned = "BANNED",
}
let s: Status = Status.Active;   // "ACTIVE"
```

### The modern alternative: union of literals (often better)
```ts
// Instead of an enum, many teams prefer:
type Status = "active" | "inactive" | "banned";
const s: Status = "active";

// Or `as const` objects when you want runtime values too:
const Status = {
  Active: "active",
  Inactive: "inactive",
} as const;
type Status = typeof Status[keyof typeof Status]; // "active" | "inactive"
```
> ⚠️ Enums are *not* fully erased — they emit runtime code (unlike most TS, which vanishes). Numeric enums also allow surprising assignments. For simple cases, **a union of string literals is lighter and safer**. Use enums when you specifically want a named, importable runtime object.

---

## VII. TYPE NARROWING

TypeScript narrows a broad type to a specific one based on control flow. Learning the narrowing tools is essential.

```ts
function process(value: string | number | null) {
  if (value === null) return;              // null filtered out
  // value is string | number here

  if (typeof value === "string") {         // typeof guard
    return value.toUpperCase();            // string
  }
  return value.toFixed(2);                 // number
}

// instanceof for classes
function logError(e: Error | string) {
  if (e instanceof Error) console.log(e.message);
  else console.log(e);
}

// `in` operator for object shapes
type Fish = { swim(): void };
type Bird = { fly(): void };
function move(animal: Fish | Bird) {
  if ("swim" in animal) animal.swim();
  else animal.fly();
}

// Custom type guard (a function returning `x is Type`)
function isString(x: unknown): x is string {
  return typeof x === "string";
}
const val: unknown = "hi";
if (isString(val)) val.toUpperCase();      // ✅ narrowed by the guard
```

---

## VIII. TYPE ASSERTIONS & NON-NULL

```ts
// `as` assertion — "trust me, I know the type" (use sparingly)
const input = document.getElementById("name") as HTMLInputElement;
input.value;   // ✅ TS now treats it as an input element

// Non-null assertion ! — "this is definitely not null/undefined"
const el = document.querySelector(".btn")!;  // removes null from the type
el.addEventListener("click", () => {});

// ⚠️ Both are promises YOU make to the compiler. If you're wrong, it crashes
// at runtime with no warning. Prefer real narrowing (if-checks) where possible.
```

---

## IX. COMMON PITFALLS & GOTCHAS

**1. Over-annotating what TS already infers** — clutters code; trust inference for locals.

**2. Using `as` to silence errors instead of fixing the type**
```ts
const user = response as User;   // ❌ if response isn't a User, you'll crash later
```

**3. Forgetting to narrow a union before using member-specific methods**
```ts
function f(x: string | number) {
  return x.toUpperCase();   // ❌ number has no toUpperCase — narrow first
}
```

**4. Numeric enum surprises**
```ts
enum E { A, B }
const x: E = 99;   // ❌-ish: TS allows arbitrary numbers into numeric enums in some cases
// Prefer string enums or literal unions.
```

**5. `interface` vs `type` for unions** — interfaces can't express `A | B`; use `type`.

**6. Optional (`?`) vs `| undefined`** — subtly different: `?` means the key may be absent; `| undefined` means it must be present but can be `undefined`.

---

## X. KEY TAKEAWAYS

- Annotate **boundaries** (params, public return types, external data); let **inference** handle locals.
- **Arrays** (`T[]`) hold many of one type; **tuples** (`[string, number]`) have fixed length and per-position types (that's how `useState` destructuring is typed).
- Object types support **optional (`?`)**, **`readonly`**, and **index signatures**.
- **`interface`** is best for object shapes (supports `extends` and declaration merging); **`type`** can do everything an interface can for objects *plus* unions, intersections, tuples, and function types. Default to `interface` for objects, `type` when you need more.
- **Union (`|`)** = one of several; **intersection (`&`)** = all combined. **Literal unions** make precise, autocompleting APIs.
- **Discriminated unions ⭐** (a shared literal tag) let TypeScript narrow automatically — and `never` enables exhaustiveness checks.
- **Narrow** unions with `typeof`, `instanceof`, `in`, and custom `x is T` guards before using type-specific members.
- Prefer **string-literal unions** over enums for simple cases (lighter, fully erased, safer).

---

**← Prev:** [`01-Why-TypeScript-And-Setup.md`](./01-Why-TypeScript-And-Setup.md) | **→ Next:** [`03-Generics-And-Advanced-Types.md`](./03-Generics-And-Advanced-Types.md) | **Index:** [`00-Index.md`](./00-Index.md)
