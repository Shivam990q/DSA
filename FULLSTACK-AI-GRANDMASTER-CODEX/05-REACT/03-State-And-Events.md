# ⚛️ 03 — State & Events

> *"Props come from above and you can't change them. State is yours — it's the memory a component keeps between renders. Change state and React re-renders. That single rule is how a static function becomes a living UI."*

**Prev:** [`02-Components-And-Props.md`](./02-Components-And-Props.md) · **Next:** [`04-Hooks-Deep-Dive.md`](./04-Hooks-Deep-Dive.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT STATE IS, AND WHY PLAIN VARIABLES FAIL

**State** is data that a component remembers across renders and that, when changed, triggers a re-render. Without it, your UI is frozen.

Why can't you just use a regular variable? Because a component is a function — every render runs it from scratch, and local variables are reborn each time. And even if you mutate a variable, React has no idea it changed, so nothing re-renders.

```jsx
// ❌ BROKEN — a plain variable doesn't survive re-renders and doesn't trigger them.
function BrokenCounter() {
  let count = 0;                                  // reset to 0 on EVERY render
  return (
    <button onClick={() => { count++; console.log(count); }}>
      {count}                                     {/* always shows 0 on screen */}
    </button>
  );
}
```

`count++` increments the variable and logs `1, 2, 3...`, but the screen stays `0` because (a) React never re-renders, and (b) even if it did, `count` would reset to `0`. State fixes both: it persists, and updating it schedules a re-render.

```jsx
import { useState } from 'react';

// ✅ WORKS — useState persists the value and re-renders on change.
function Counter() {
  const [count, setCount] = useState(0);          // [current value, setter]
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## II. `useState` — THE FUNDAMENTAL HOOK

`useState` returns a pair: the **current value** and a **setter function**. Calling the setter with a new value tells React "this changed — re-render with the new value."

```jsx
const [value, setValue] = useState(initialValue);
//     ▲        ▲                    ▲
//     │        │                    └─ used ONLY on the first render
//     │        └─ call this to update value (and trigger a re-render)
//     └─ current value for THIS render
```

```jsx
function Examples() {
  const [count, setCount]   = useState(0);          // number
  const [name, setName]     = useState('');         // string
  const [isOpen, setIsOpen] = useState(false);      // boolean
  const [items, setItems]   = useState([]);         // array
  const [user, setUser]     = useState({ name: '', age: 0 }); // object

  // Lazy initial state: pass a FUNCTION when the initial value is expensive to compute.
  // React calls it once, on mount, instead of every render.
  const [data, setData] = useState(() => expensiveCompute());

  return null;
}
```

> **Gotcha — state updates are asynchronous (batched).** After `setCount(count + 1)`, `count` does **not** change on the next line — it still holds the value for the current render. The new value appears on the *next* render. Don't read state right after setting it expecting the new value.

```jsx
function Logger() {
  const [count, setCount] = useState(0);
  function handleClick() {
    setCount(count + 1);
    console.log(count);   // logs the OLD value — the update hasn't applied yet
  }
  return <button onClick={handleClick}>{count}</button>;
}
```

### Functional updates — when the new value depends on the old

If you update based on the previous value (especially multiple times, or inside async code), pass a **function** to the setter. React calls it with the latest queued value.

```jsx
function Counter() {
  const [count, setCount] = useState(0);

  function addThree() {
    // ❌ All three read the SAME stale `count` from this render → net effect: +1
    // setCount(count + 1);
    // setCount(count + 1);
    // setCount(count + 1);

    // ✅ Functional updates queue correctly off the latest value → net effect: +3
    setCount((c) => c + 1);
    setCount((c) => c + 1);
    setCount((c) => c + 1);
  }

  return <button onClick={addThree}>{count}</button>;
}
```

> **Rule:** if your next state is computed from the current state, use the updater function `setX(prev => ...)`. It's always correct, even across batches and async boundaries.

---

## III. HANDLING EVENTS

React events look like DOM events but are camelCased and take a **function** (not a string). React wraps native events in a cross-browser **SyntheticEvent** with the same API (`e.target`, `e.preventDefault()`, etc.).

```jsx
function EventBasics() {
  // Pass a function reference — do NOT call it.
  function handleClick(e) {
    console.log('clicked', e.target);
  }

  return (
    <div>
      <button onClick={handleClick}>Reference (correct)</button>

      {/* Inline arrow — needed when you pass arguments */}
      <button onClick={() => handleClick('hi')}>Inline arrow</button>

      {/* ❌ WRONG — this CALLS handleClick during render, not on click */}
      {/* <button onClick={handleClick()}>Bug</button> */}
    </div>
  );
}
```

> **Gotcha — `onClick={handler}` vs `onClick={handler()}`.** The first passes the function so React calls it on click. The second **calls it immediately during render** and passes whatever it returns — a classic bug that fires handlers on mount and creates infinite loops with state setters.

### Common events and the event object

```jsx
function Form() {
  function handleSubmit(e) {
    e.preventDefault();          // stop the browser's default page reload
    console.log('submitted');
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        onChange={(e) => console.log(e.target.value)}   // fires on every keystroke
        onFocus={() => console.log('focused')}
        onBlur={() => console.log('left field')}
        onKeyDown={(e) => { if (e.key === 'Enter') console.log('enter'); }}
      />
      <button type="submit">Go</button>
    </form>
  );
}
```

> **Gotcha — always `e.preventDefault()` on form submit.** By default, submitting a form reloads the page (a relic of pre-SPA web). In React you almost always want to handle it in JS, so prevent the default.

---

## IV. UPDATING STATE THE RIGHT WAY — IMMUTABILITY

React decides whether to re-render by comparing the **reference** (identity) of state, not its deep contents. If you mutate an object/array in place, the reference is unchanged, so React thinks nothing happened — your UI won't update.

**The rule: never mutate state. Always create a new object/array.**

```jsx
function Mutations() {
  const [user, setUser] = useState({ name: 'Ada', age: 36 });
  const [items, setItems] = useState(['a', 'b']);

  // ❌ MUTATION — same reference, React may not re-render
  function badUpdate() {
    user.age = 37;          // mutating in place
    setUser(user);          // same object → React sees no change
    items.push('c');        // mutating the array
    setItems(items);        // same array → no re-render
  }

  // ✅ IMMUTABLE — new references, React re-renders
  function goodUpdate() {
    setUser({ ...user, age: 37 });      // spread old, override age → NEW object
    setItems([...items, 'c']);          // spread old, append → NEW array
  }

  return null;
}
```

### Immutable update cheatsheet

```jsx
// OBJECTS
setUser({ ...user, age: 37 });                       // update one field
setUser({ ...user, address: { ...user.address, city: 'NYC' } }); // nested update

// ARRAYS — use methods that RETURN a new array; avoid push/splice/sort-in-place
setItems([...items, newItem]);                       // add to end
setItems([newItem, ...items]);                       // add to start
setItems(items.filter((x) => x.id !== id));          // remove by id
setItems(items.map((x) => x.id === id ? { ...x, done: true } : x)); // update one
setItems([...items].sort());                         // copy THEN sort (sort mutates!)
```

> **Gotcha — `.sort()`, `.reverse()`, `.splice()` mutate in place.** These array methods modify the original array. Copy first: `[...items].sort(...)`. Prefer the non-mutating methods (`map`, `filter`, `concat`, `slice`, plus the newer `toSorted`, `toReversed`).

```jsx
// A practical todo updater — all immutable.
function Todos() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn state', done: false },
  ]);

  const add = (text) =>
    setTodos((prev) => [...prev, { id: Date.now(), text, done: false }]);

  const toggle = (id) =>
    setTodos((prev) => prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));

  const remove = (id) =>
    setTodos((prev) => prev.filter((t) => t.id !== id));

  return (
    <ul>
      {todos.map((t) => (
        <li key={t.id}>
          <input type="checkbox" checked={t.done} onChange={() => toggle(t.id)} />
          {t.text}
          <button onClick={() => remove(t.id)}>✕</button>
        </li>
      ))}
    </ul>
  );
}
```

---

## V. BATCHING — MULTIPLE UPDATES, ONE RENDER

React **batches** state updates that happen in the same event handler into a single re-render for performance. Three `setX` calls in one click cause **one** render, not three.

```jsx
function Batching() {
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);

  function handleClick() {
    setA((x) => x + 1);
    setB((x) => x + 1);
    setA((x) => x + 1);
    // React 18+ batches ALL of these → exactly ONE re-render with a=2, b=1.
  }

  // This component renders once per click, not three times.
  console.log('render');
  return <button onClick={handleClick}>{a} / {b}</button>;
}
```

> **Note — React 18 automatic batching.** Older React only batched inside React event handlers. React 18+ batches everywhere — including inside `setTimeout`, promises, and native event handlers — thanks to `createRoot`. This is one reason `createRoot` matters (file 01). You rarely need to think about it; just know multiple sets collapse into one render.

---

## VI. LIFTING STATE UP

When two components need to share or sync state, you can't store it in either one. You **lift it up** to their nearest common parent, then pass the value down as props and changes up as callbacks. This keeps a **single source of truth**.

The pattern in three steps:
1. Move the state to the closest common ancestor.
2. Pass the value **down** as a prop.
3. Pass a setter/handler **down** so children can request changes.

```jsx
// Two inputs that must stay in sync (e.g. Celsius ↔ a shared temperature).
// State lives in the PARENT; children are controlled by it.

function TemperatureInput({ label, value, onChange }) {
  return (
    <label>
      {label}:
      <input value={value} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}

function Calculator() {
  const [celsius, setCelsius] = useState('');           // single source of truth

  const fahrenheit = celsius === '' ? '' : (Number(celsius) * 9) / 5 + 32;

  return (
    <div>
      <TemperatureInput label="Celsius" value={celsius} onChange={setCelsius} />
      <TemperatureInput
        label="Fahrenheit"
        value={fahrenheit}
        onChange={(f) => setCelsius(((Number(f) - 32) * 5) / 9)}
      />
      {Number(celsius) >= 100 && <p>The water would boil. 💧→💨</p>}
    </div>
  );
}
```

Both inputs read from and write to one piece of parent state, so they can never disagree.

> **Where should state live?** Put state in the **lowest common ancestor** of all components that need it. Too high and you re-render too much and drill too far; too low and siblings can't share it. When sharing crosses many layers or the whole app, reach for Context or a state library (file 05).

### Data down, events up — the core data flow

```
        ┌─────────────────────┐
        │   Parent (owns state)│
        └─────────┬───────────┘
       props ↓    │    ↑ callbacks (events)
        ┌─────────▼───────────┐
        │       Child         │
        └─────────────────────┘

  Data flows DOWN as props.   Changes flow UP as function calls.
  The owner of the state is the only one who mutates it.
```

---

## VII. A COMPLETE EXAMPLE — A SHOPPING CART COUNTER

Everything together: state, events, immutability, derived values, lifting state up.

```jsx
import { useState } from 'react';

function ProductRow({ product, quantity, onChange }) {
  return (
    <div className="row">
      <span>{product.name} (${product.price})</span>
      <button onClick={() => onChange(product.id, Math.max(0, quantity - 1))}>−</button>
      <span>{quantity}</span>
      <button onClick={() => onChange(product.id, quantity + 1)}>+</button>
    </div>
  );
}

export default function Cart() {
  const products = [
    { id: 'p1', name: 'Coffee', price: 4 },
    { id: 'p2', name: 'Bagel',  price: 3 },
  ];

  // State: a map of productId → quantity. Lives here so the total can be derived.
  const [quantities, setQuantities] = useState({ p1: 0, p2: 0 });

  // Immutable update of one entry.
  const setQty = (id, qty) =>
    setQuantities((prev) => ({ ...prev, [id]: qty }));

  // DERIVED value — computed during render, not stored in state.
  const total = products.reduce((sum, p) => sum + p.price * quantities[p.id], 0);

  return (
    <div>
      {products.map((p) => (
        <ProductRow
          key={p.id}
          product={p}
          quantity={quantities[p.id]}
          onChange={setQty}
        />
      ))}
      <hr />
      <strong>Total: ${total}</strong>
    </div>
  );
}
```

> **Don't store what you can derive.** `total` is computed from `quantities` on every render — it is **not** its own state. Storing derived data in state is a top source of bugs (the two values drift out of sync). Keep the minimal state; compute the rest.

---

## VIII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Plain variable instead of state | UI never updates | Use `useState` |
| Reading state right after `setState` | Sees the old value | Updates apply next render; use the new value in JSX |
| `setCount(count+1)` ×3 | Increments by 1, not 3 | Functional update `setCount(c => c + 1)` |
| Mutating state object/array | No re-render | Create new object/array (spread, `map`, `filter`) |
| `.sort()`/`.push()` on state array | Mutation bug | Copy first: `[...arr].sort()` |
| `onClick={handler()}` | Fires on render / infinite loop | `onClick={handler}` or `onClick={() => handler(arg)}` |
| Forgetting `e.preventDefault()` on submit | Page reloads | Call `e.preventDefault()` |
| Storing derived data in state | Values drift out of sync | Compute it during render |
| Duplicating shared state in two siblings | They disagree | Lift state to common parent |
| Initial state recomputed each render | Wasted work | Lazy init: `useState(() => compute())` |

---

## 🧠 KEY TAKEAWAYS

- **State** is per-component memory that persists across renders; changing it triggers a re-render. Plain variables can't do this.
- `useState` returns `[value, setter]`; the initial value is used only on the first render (use a function for **lazy init**).
- State updates are **asynchronous and batched** — the new value shows up on the next render, not the next line.
- When the next value depends on the previous, use the **functional updater**: `setX(prev => ...)`.
- **Never mutate state.** Create new objects/arrays with spread, `map`, `filter`. Beware in-place methods like `sort`/`push`/`splice`.
- Events are camelCased and take a **function reference**; `handler` not `handler()`. Call `e.preventDefault()` on form submit.
- Share state by **lifting it up** to the nearest common parent: **data flows down (props), events flow up (callbacks)**.
- Keep state **minimal** — derive everything you can during render instead of storing it.

---

**Prev:** [`02-Components-And-Props.md`](./02-Components-And-Props.md) · **Next:** [`04-Hooks-Deep-Dive.md`](./04-Hooks-Deep-Dive.md) · **Index:** [`00-Index.md`](./00-Index.md)
