# ⚛️ TypeScript with React

> *"This is where you'll actually write most of your TypeScript. Props, state, hooks, events — typed."*

React + TypeScript is the dominant frontend combination today. This file shows how to type the things you touch every day: **component props**, **state**, **hooks** (`useState`, `useReducer`, `useRef`, `useContext`, custom hooks), and **DOM/form events**. The patterns here build directly on generics (file 03) — React's hooks are generic functions.

> This file teaches *typing* React, not React itself. The full React section is [`../05-REACT/`](../05-REACT/). File extensions: use `.tsx` for files containing JSX, `.ts` for everything else.

---

## I. TYPING COMPONENT PROPS

Props are just an object, so you type them with an `interface` (or `type`). This is the most common TypeScript you'll write in React.

```tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "primary" | "secondary";   // optional, with a literal union
  disabled?: boolean;
}

function Button({ label, onClick, variant = "primary", disabled = false }: ButtonProps) {
  return (
    <button className={variant} onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
}

// Usage — fully checked:
<Button label="Save" onClick={() => save()} />              // ✅
<Button label="Delete" onClick={handleDelete} variant="secondary" />  // ✅
<Button label="X" />                                        // ❌ missing onClick
<Button label="X" onClick={fn} variant="danger" />          // ❌ invalid variant
```

### Typing `children`
```tsx
import { ReactNode } from "react";

interface CardProps {
  title: string;
  children: ReactNode;        // ReactNode = anything renderable (jsx, string, number, null...)
}

function Card({ title, children }: CardProps) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
}

<Card title="Profile">
  <p>Any JSX goes here</p>      {/* ✅ children */}
</Card>
```

### Props with functions, objects, and arrays
```tsx
interface User { id: number; name: string; }

interface UserListProps {
  users: User[];                            // array of objects
  onSelect: (user: User) => void;           // callback receiving a User
  renderItem?: (user: User) => ReactNode;   // optional render prop
}

function UserList({ users, onSelect, renderItem }: UserListProps) {
  return (
    <ul>
      {users.map(user => (
        <li key={user.id} onClick={() => onSelect(user)}>
          {renderItem ? renderItem(user) : user.name}
        </li>
      ))}
    </ul>
  );
}
```

> **Note on `React.FC`:** you may see `const C: React.FC<Props> = (props) => {...}`. It works, but the modern community preference is to type the props argument directly (as above) — it's simpler and avoids some historical `children` quirks.

---

## II. TYPING `useState`

`useState` is generic. Most of the time inference is enough; annotate when the initial value doesn't tell the whole story.

```tsx
import { useState } from "react";

// Inferred from the initial value — no annotation needed
const [count, setCount] = useState(0);          // count: number
const [name, setName] = useState("");           // name: string
const [active, setActive] = useState(false);    // active: boolean

setCount(5);          // ✅
setCount("5");        // ❌ string not assignable to number

// Explicit type when initial value is null/empty (inference can't tell)
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);     // would infer never[] otherwise
const [status, setStatus] = useState<"idle" | "loading" | "done">("idle");

// Functional updates are typed too
setCount(prev => prev + 1);   // prev: number
```

> ⚠️ `useState([])` infers `never[]` — you can never add anything to it. Always annotate empty-array and `null` initial states: `useState<string[]>([])`, `useState<User | null>(null)`.

---

## III. TYPING EVENTS

React wraps DOM events in `SyntheticEvent` types. The trick is matching the right event type to the element.

```tsx
// Click events
function handleClick(e: React.MouseEvent<HTMLButtonElement>) {
  e.preventDefault();
  console.log(e.currentTarget);   // typed as HTMLButtonElement
}

// Input change events — the daily one
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);    // string, fully typed
}

// Form submit
function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
}

// Keyboard
function handleKey(e: React.KeyboardEvent<HTMLInputElement>) {
  if (e.key === "Enter") submit();
}

function SearchForm() {
  const [query, setQuery] = useState("");
  return (
    <form onSubmit={handleSubmit}>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}   // e inferred — often no annotation needed
        onKeyDown={handleKey}
      />
    </form>
  );
}
```

### Common event type reference
| Event | Type |
|-------|------|
| Button/div click | `React.MouseEvent<HTMLButtonElement>` |
| Input change | `React.ChangeEvent<HTMLInputElement>` |
| Textarea change | `React.ChangeEvent<HTMLTextAreaElement>` |
| Select change | `React.ChangeEvent<HTMLSelectElement>` |
| Form submit | `React.FormEvent<HTMLFormElement>` |
| Key press | `React.KeyboardEvent<HTMLInputElement>` |
| Focus/blur | `React.FocusEvent<HTMLInputElement>` |

> **Tip:** when you write the handler *inline* (`onChange={e => ...}`), React infers `e` for you — no annotation needed. You only annotate when the handler is a *separate named function*.

---

## IV. TYPING `useRef`

`useRef` has two distinct uses, typed differently.

```tsx
import { useRef, useEffect } from "react";

// 1. DOM element refs — initialize with null, type the element
function TextInput() {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();    // ?. because current is HTMLInputElement | null
  }, []);

  return <input ref={inputRef} />;
}

// 2. Mutable value refs (not attached to DOM) — like an instance variable
function Timer() {
  const intervalRef = useRef<number | null>(null);   // holds a timer id

  const start = () => {
    intervalRef.current = window.setInterval(() => console.log("tick"), 1000);
  };
  const stop = () => {
    if (intervalRef.current !== null) clearInterval(intervalRef.current);
  };
  return <button onClick={start}>Start</button>;
}
```

---

## V. TYPING `useReducer`

`useReducer` shines with TypeScript because the action types become a discriminated union (file 02) — giving you exhaustive, autocompleted action handling.

```tsx
import { useReducer } from "react";

interface State {
  count: number;
  step: number;
}

// Discriminated union of actions
type Action =
  | { type: "increment" }
  | { type: "decrement" }
  | { type: "setStep"; payload: number }
  | { type: "reset" };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "increment": return { ...state, count: state.count + state.step };
    case "decrement": return { ...state, count: state.count - state.step };
    case "setStep":   return { ...state, step: action.payload };  // ✅ payload typed as number
    case "reset":     return { count: 0, step: 1 };
    default:
      const _exhaustive: never = action;   // compile error if an action is unhandled
      return state;
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, step: 1 });
  return (
    <>
      <p>{state.count}</p>
      <button onClick={() => dispatch({ type: "increment" })}>+</button>
      <button onClick={() => dispatch({ type: "setStep", payload: 5 })}>Step 5</button>
      <button onClick={() => dispatch({ type: "setStep" })}>           {/* ❌ missing payload */}
    </>
  );
}
```

---

## VI. TYPING `useContext`

```tsx
import { createContext, useContext, useState, ReactNode } from "react";

interface AuthContextType {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

// Create with a typed default (null + a guard is a common safe pattern)
const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const login = (u: User) => setUser(u);
  const logout = () => setUser(null);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// A custom hook that guarantees the context exists (no null checks everywhere)
export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;   // narrowed to AuthContextType — non-null
}

// Usage — fully typed, no null handling needed at call sites
function Profile() {
  const { user, logout } = useAuth();
  return <div>{user?.name} <button onClick={logout}>Logout</button></div>;
}
```

---

## VII. TYPING CUSTOM HOOKS

Custom hooks are just functions — type their arguments and return value. Returning a **tuple** mirrors `useState`; returning an **object** is clearer for many values.

```tsx
import { useState, useCallback } from "react";

// A generic, reusable hook — works with any value type
function useToggle(initial = false): [boolean, () => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  return [value, toggle];   // tuple, like useState
}
const [isOpen, toggleOpen] = useToggle();   // [boolean, () => void]

// A generic data-fetching hook
interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

function useFetch<T>(url: string): FetchState<T> {
  const [state, setState] = useState<FetchState<T>>({
    data: null, loading: true, error: null,
  });

  useEffect(() => {
    let cancelled = false;
    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json() as Promise<T>;
      })
      .then(data => { if (!cancelled) setState({ data, loading: false, error: null }); })
      .catch(err => { if (!cancelled) setState({ data: null, loading: false, error: err.message }); });
    return () => { cancelled = true; };
  }, [url]);

  return state;
}

// Usage — the generic flows through, so `data` is fully typed
function UserProfile({ id }: { id: number }) {
  const { data, loading, error } = useFetch<User>(`/api/users/${id}`);
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;
  return <h1>{data?.name}</h1>;   // data is User | null
}
```

---

## VIII. GENERIC COMPONENTS

Components can be generic too — essential for reusable lists, tables, and selects.

```tsx
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => ReactNode;
  keyExtractor: (item: T) => string | number;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map(item => <li key={keyExtractor(item)}>{renderItem(item)}</li>)}
    </ul>
  );
}

// Usage — T is inferred from `items`, and renderItem's param is typed accordingly
<List
  items={users}                              // User[]
  keyExtractor={(u) => u.id}                 // u: User
  renderItem={(u) => <span>{u.name}</span>}  // u: User — fully typed
/>
```

---

## IX. COMMON PITFALLS & GOTCHAS

**1. `useState([])` or `useState(null)` without a type**
```tsx
const [items, setItems] = useState([]);          // ❌ never[] — can't add items
const [items, setItems] = useState<Item[]>([]);  // ✅
const [user, setUser] = useState<User | null>(null); // ✅
```

**2. Over-annotating inline event handlers** — `onChange={e => ...}` infers `e`; you rarely need `React.ChangeEvent<...>` inline.

**3. Using `any` for props to "move fast"** — you lose every benefit; props are the easiest, highest-value thing to type.

**4. `createContext()` with no type** — leads to `undefined`-not-handled errors. Type it `<T | null>` and guard in a custom hook (section VI).

**5. Forgetting `?.` on refs** — `ref.current` is `T | null` until mounted; use optional chaining.

**6. Typing children by hand** — use `ReactNode`, not `JSX.Element` (which is too narrow — it rejects strings, arrays, and null).

**7. Confusing `e.target` and `e.currentTarget`** — `currentTarget` is reliably the element the handler is attached to (and best-typed); `target` is whatever was actually clicked.

---

## X. KEY TAKEAWAYS

- Type **props** with an `interface`; type the destructured argument directly rather than reaching for `React.FC`. Use `ReactNode` for `children`.
- **`useState`** infers from its initial value — but annotate when starting from `null` or `[]` (`useState<User | null>(null)`, `useState<string[]>([])`) to avoid `never`.
- Match **event types** to elements (`React.ChangeEvent<HTMLInputElement>`, `React.FormEvent<HTMLFormElement>`...). Inline handlers infer the event; named handlers need the annotation.
- **`useRef`** is `useRef<HTMLInputElement>(null)` for DOM refs (mind the `?.`) and `useRef<T>(initial)` for mutable values.
- **`useReducer`** pairs beautifully with a **discriminated-union** action type, giving exhaustive, autocompleted, payload-checked actions.
- **`useContext`** should be typed `<T | null>` and wrapped in a **custom hook that throws if missing**, so call sites get a non-null, fully typed value.
- **Custom hooks and components can be generic** — let the type flow from arguments (`useFetch<User>`, `<List items={users} />`) for reusable, fully typed building blocks.

---

**← Prev:** [`03-Generics-And-Advanced-Types.md`](./03-Generics-And-Advanced-Types.md) | **→ Next section:** [`../05-REACT/00-Index.md`](../05-REACT/00-Index.md) — React *(coming in this codex)* | **Index:** [`00-Index.md`](./00-Index.md)
