# ⚛️ 01 — React Fundamentals & JSX

> *"The DOM is slow to touch and easy to corrupt. React's bet: let you describe what the UI should look like, and let a diffing engine figure out the minimal changes. You declare the destination; React drives."*

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-Components-And-Props.md`](./02-Components-And-Props.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT REACT ACTUALLY IS

React is a **JavaScript library for building user interfaces** out of **components** — reusable, self-contained pieces of UI. It was created at Facebook (2013) to solve one problem: keeping a complex, fast-changing UI in sync with fast-changing data without the code collapsing into spaghetti.

The single idea that defines React:

```
UI = f(state)
```

Your UI is a **pure function of your application's state**. You never write "find this `<div>` and change its text." Instead you write "given this state, here is what the screen should look like," and React makes the real screen match. When state changes, React re-runs your function and updates the DOM for you.

Contrast with the old way (imperative DOM manipulation):

```js
// IMPERATIVE (vanilla JS / jQuery) — you micromanage every DOM mutation.
// As the app grows, these manual updates multiply and drift out of sync.
const button = document.querySelector('#like');
let likes = 0;
button.addEventListener('click', () => {
  likes++;
  document.querySelector('#count').textContent = likes;   // you, by hand
  if (likes > 10) button.classList.add('hot');            // you, by hand
});
```

```jsx
// DECLARATIVE (React) — you describe the result for any state. React syncs the DOM.
function LikeButton() {
  const [likes, setLikes] = useState(0);
  return (
    <button className={likes > 10 ? 'hot' : ''} onClick={() => setLikes(likes + 1)}>
      {likes} likes
    </button>
  );
}
```

You stopped saying *how* to update the DOM and started saying *what* it should be. That shift is the whole game.

> **Gotcha — React is a library, not a framework.** It does rendering. It does *not* (by itself) give you routing, data fetching, or a build system. You assemble those (React Router, TanStack Query, Vite). Next.js bundles them into a framework. Knowing this boundary keeps your mental model honest.

---

## II. THE VIRTUAL DOM & RECONCILIATION

Touching the real DOM is expensive. Layout, paint, and reflow are slow, and doing many small updates thrashes the browser. React's solution is the **Virtual DOM (VDOM)**: a lightweight JavaScript object tree that mirrors the real DOM.

The cycle:

```
1. State changes.
2. React re-runs your component → produces a NEW virtual DOM tree.
3. React DIFFS the new tree against the previous one ("reconciliation").
4. React computes the MINIMAL set of real-DOM operations needed.
5. React commits ONLY those operations to the real DOM.
```

```
   State change
        │
        ▼
  New VDOM tree  ──────►  diff  ──────►  Old VDOM tree
        │                  │
        │            minimal changes
        ▼                  ▼
   (kept in memory)   commit to REAL DOM (the only slow part, minimized)
```

Because the diff happens on plain JS objects in memory, it's fast. The only expensive operations — real DOM mutations — are reduced to the bare minimum.

**Reconciliation heuristics** (how the diff stays cheap):

- **Different element types → throw away and rebuild.** `<div>` replaced by `<span>` means React destroys the old subtree and builds a new one. It doesn't try to morph one into the other.
- **Same type → keep the node, update changed attributes.** A `<div className="a">` becoming `<div className="b">` just patches the class.
- **Lists are matched by `key`** (see Section VII) — this is why keys matter so much.

> **Gotcha — the VDOM is not "fast" by magic.** It is a tradeoff: you spend a little CPU diffing in JS to *avoid* expensive, redundant DOM work. For most apps that's a huge win. It does not make a poorly-written component free — Section 08 is about avoiding wasted diffs entirely.

---

## III. JSX — JAVASCRIPT THAT LOOKS LIKE HTML

**JSX** is a syntax extension that lets you write HTML-like markup inside JavaScript. It is not HTML, and it is not a string — it's syntactic sugar that a compiler (Babel/SWC, built into Vite) transforms into function calls.

```jsx
// What you write:
const element = <h1 className="title">Hello</h1>;

// What it compiles to (roughly):
const element = React.createElement('h1', { className: 'title' }, 'Hello');

// Which produces a plain object (a "React element"):
// { type: 'h1', props: { className: 'title', children: 'Hello' } }
```

So JSX is just a comfortable way to write `createElement` calls. That's why you can put JSX anywhere a value is allowed — it *is* a value (an object).

### Embedding expressions with `{ }`

Curly braces drop you back into JavaScript. Anything that is an **expression** (produces a value) goes inside.

```jsx
function Greeting() {
  const name = 'Ada';
  const user = { firstName: 'Grace', lastName: 'Hopper' };
  const hour = new Date().getHours();

  return (
    <div>
      <h1>Hello, {name}!</h1>                          {/* variable */}
      <p>2 + 2 = {2 + 2}</p>                            {/* arithmetic */}
      <p>{user.firstName} {user.lastName}</p>          {/* object access */}
      <p>{name.toUpperCase()}</p>                       {/* method call */}
      <p>{hour < 12 ? 'Good morning' : 'Good day'}</p>  {/* ternary */}
    </div>
  );
}
```

> **Gotcha — expressions only, not statements.** You can put `cond ? a : b` inside `{ }`, but not `if (cond) { ... }`. An `if` is a *statement*; JSX interpolation needs an *expression*. Use ternaries, `&&`, or compute the value before the `return`.

### JSX rules that trip up beginners

| Rule | Why | Example |
|------|-----|---------|
| One root element | A component returns a single element (a tree has one root) | Wrap siblings in a `<div>` or `<>…</>` |
| `className` not `class` | `class` is a reserved word in JS | `<div className="card">` |
| `htmlFor` not `for` | `for` is reserved | `<label htmlFor="email">` |
| camelCase event/attrs | JS convention | `onClick`, `tabIndex`, `onChange` |
| Close every tag | JSX is XML-strict | `<img />`, `<br />`, `<input />` |
| `{/* comment */}` | HTML comments don't work | `{/* like this */}` |
| `style` is an object | Not a CSS string | `style={{ color: 'red', fontSize: 14 }}` |

```jsx
function StyledCard() {
  return (
    <div style={{ padding: 16, border: '1px solid #ccc', borderRadius: 8 }}>
      {/* style takes an OBJECT: outer braces = JS, inner braces = object literal */}
      {/* CSS properties are camelCased: background-color → backgroundColor */}
      <label htmlFor="email">Email</label>
      <input id="email" type="email" />
      <img src="/logo.png" alt="logo" />   {/* self-closing, alt for accessibility */}
    </div>
  );
}
```

### Fragments — returning siblings without a wrapper `<div>`

When you need multiple top-level elements but don't want an extra DOM node, use a **Fragment**.

```jsx
import { Fragment } from 'react';

function Columns() {
  return (
    <>                          {/* shorthand fragment — renders no DOM node */}
      <td>Name</td>
      <td>Role</td>
    </>
  );
}

// Long form — needed when you must pass a key (e.g. in a list)
function List({ items }) {
  return items.map((item) => (
    <Fragment key={item.id}>
      <dt>{item.term}</dt>
      <dd>{item.definition}</dd>
    </Fragment>
  ));
}
```

> **Gotcha — "Adjacent JSX elements must be wrapped."** This error means you returned two sibling elements without a single parent. Wrap them in `<>...</>`. Use a real `<div>` only when you actually want a DOM node (e.g. for styling).

---

## IV. RENDERING REACT TO THE PAGE

A React app needs exactly one mount point. In your `index.html` there's a container, usually `<div id="root"></div>`. You tell React to take it over.

```jsx
// main.jsx — the bridge from "HTML page" to "React app"
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';

// 1. Find the container in the real DOM.
const container = document.getElementById('root');

// 2. Create a React "root" that manages everything inside that container.
const root = createRoot(container);

// 3. Render your top-level component into it.
root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

> **Gotcha — `createRoot` vs the old `ReactDOM.render`.** React 18+ uses `createRoot` (from `react-dom/client`), which enables concurrent features and automatic batching. The legacy `ReactDOM.render(<App/>, container)` is removed in React 19. If a tutorial uses `ReactDOM.render`, it's pre-2022 — use `createRoot`.

> **What is `StrictMode`?** A development-only wrapper that helps you catch bugs. It intentionally **double-invokes** components, effects, and state updaters in dev to surface impure code and missing effect cleanups. It renders nothing and disappears in production builds. If you see your `console.log` or effect run twice in dev — that's StrictMode, and it's a feature (Section 04 explains why).

---

## V. CONDITIONAL RENDERING

Because JSX is just values, you choose what to render with ordinary JavaScript.

```jsx
function Dashboard({ user, notifications }) {
  // 1. Early return — clean for whole-component branching
  if (!user) {
    return <LoginScreen />;
  }

  return (
    <div>
      {/* 2. Ternary — choose between two things */}
      {user.isAdmin ? <AdminPanel /> : <UserPanel />}

      {/* 3. Logical && — render something or nothing */}
      {notifications.length > 0 && (
        <span className="badge">{notifications.length}</span>
      )}

      {/* 4. Assign to a variable beforehand for complex cases */}
      {renderStatus(user.status)}
    </div>
  );
}

function renderStatus(status) {
  switch (status) {
    case 'online':  return <span className="green">●</span>;
    case 'away':    return <span className="yellow">●</span>;
    default:        return <span className="gray">●</span>;
  }
}
```

> **Gotcha — the `&&` zero trap.** `{count && <Badge />}` renders the *number* `0` to the screen when `count` is `0`, because `0` is falsy but still a renderable value. React renders `0` but not `false`/`null`/`undefined`. Fix it by forcing a boolean: `{count > 0 && <Badge />}` or `{!!count && <Badge />}`.

```jsx
function Cart({ items }) {
  return (
    <div>
      {items.length && <p>You have items</p>}     {/* BUG: shows "0" when empty */}
      {items.length > 0 && <p>You have items</p>} {/* CORRECT: shows nothing when empty */}
    </div>
  );
}
```

Returning `null` renders nothing — a valid way for a component to opt out:

```jsx
function Banner({ show, message }) {
  if (!show) return null;            // render nothing
  return <div className="banner">{message}</div>;
}
```

---

## VI. RENDERING LISTS WITH `.map()`

To render a collection, transform an array into an array of elements with `.map()`. React renders arrays of elements directly.

```jsx
function ProductList() {
  const products = [
    { id: 'p1', name: 'Keyboard', price: 49 },
    { id: 'p2', name: 'Mouse',    price: 25 },
    { id: 'p3', name: 'Monitor',  price: 199 },
  ];

  return (
    <ul>
      {products.map((product) => (
        <li key={product.id}>
          {product.name} — ${product.price}
        </li>
      ))}
    </ul>
  );
}
```

You can chain array methods — filter, then map — because it's all just JavaScript:

```jsx
function AffordableProducts({ products, budget }) {
  return (
    <ul>
      {products
        .filter((p) => p.price <= budget)   // keep only what fits the budget
        .map((p) => (
          <li key={p.id}>{p.name}</li>      // then render each survivor
        ))}
    </ul>
  );
}
```

---

## VII. KEYS — THE MOST MISUNDERSTOOD RULE IN REACT

When you render a list, React needs to match each rendered item to its data across re-renders. The **`key`** is that identity. It tells React "this element is the *same logical item* as before, even if it moved."

```jsx
// Each key must be UNIQUE among siblings and STABLE across renders.
{users.map((user) => <UserRow key={user.id} user={user} />)}
```

Why it matters — consider inserting an item at the top of a list:

```
Without stable keys (using index):        With stable keys (using id):
  Before: [A, B, C]                          Before: [A(id1), B(id2), C(id3)]
  Insert X at top                            Insert X(id0) at top
  After:  [X, A, B, C]                        After:  [X(id0), A(id1), B(id2), C(id3)]

  React (by index) thinks:                   React (by id) thinks:
   index0 changed A→X  (re-render)            id0 is NEW → insert one node
   index1 changed B→A  (re-render)            id1, id2, id3 UNCHANGED → keep them
   index2 changed C→B  (re-render)
   index3 is new C     (insert)               → 1 DOM insertion. Correct & fast.
  → 4 operations + state attached to the
    wrong rows. Slow & buggy.
```

> **Gotcha — never use the array index as a key when the list can reorder, filter, or have items inserted/removed.** Index-as-key causes subtle bugs: input values stick to the wrong rows, animations glitch, and component state gets misattached. Index is only safe for a static list that never changes order.

```jsx
// ❌ BAD — index breaks on reorder/insert/delete and corrupts per-item state
{todos.map((todo, index) => <TodoItem key={index} todo={todo} />)}

// ✅ GOOD — a stable, unique id from the data
{todos.map((todo) => <TodoItem key={todo.id} todo={todo} />)}

// If your data truly has no id, generate one when you CREATE the item
// (e.g. crypto.randomUUID()), not during render.
```

> **Gotcha — keys are not props.** A component cannot read its own `key`. `key` is a special instruction to React's reconciler. If you also need the value inside the component, pass it again as a normal prop: `<Item key={id} id={id} />`.

---

## VIII. A COMPLETE LITTLE COMPONENT

Everything above, combined into one self-contained component:

```jsx
import { useState } from 'react';

export default function TaskBoard() {
  const [tasks] = useState([
    { id: 't1', title: 'Learn JSX',        done: true  },
    { id: 't2', title: 'Understand keys',  done: true  },
    { id: 't3', title: 'Master hooks',     done: false },
  ]);

  const remaining = tasks.filter((t) => !t.done).length;

  return (
    <section style={{ maxWidth: 360, fontFamily: 'system-ui' }}>
      <h1>Task Board</h1>

      {/* Conditional: message changes with state */}
      {remaining === 0
        ? <p>🎉 All done!</p>
        : <p>{remaining} task{remaining > 1 ? 's' : ''} left</p>}

      {/* List with stable keys */}
      <ul>
        {tasks.map((task) => (
          <li key={task.id} style={{ textDecoration: task.done ? 'line-through' : 'none' }}>
            {task.done ? '✅' : '⬜'} {task.title}
          </li>
        ))}
      </ul>
    </section>
  );
}
```

---

## IX. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using `class` / `for` in JSX | Attribute ignored or warning | Use `className` / `htmlFor` |
| Returning multiple root elements | "Adjacent JSX elements must be wrapped" | Wrap in `<>...</>` |
| `if` statement inside `{ }` | Syntax error | Use a ternary, `&&`, or compute before `return` |
| `{count && <X/>}` with `count === 0` | A stray `0` appears on screen | Use `{count > 0 && <X/>}` |
| Index as `key` on a dynamic list | Wrong inputs/state stick to rows | Use a stable unique `id` |
| `style="color:red"` (string) | Error — style must be an object | `style={{ color: 'red' }}` |
| Forgetting `key` on `.map()` output | Console warning, subtle list bugs | Add `key={item.id}` |
| Using `ReactDOM.render` (React 18/19) | Deprecated / removed | Use `createRoot(...).render(...)` |
| Expecting JSX to be HTML | Confusion over attributes | JSX compiles to `createElement` — it's JS |
| Reading `this.props.key` | `undefined` | `key` isn't a readable prop; pass value separately |

---

## 🧠 KEY TAKEAWAYS

- React's core idea is **`UI = f(state)`**: you declare what the UI should be for a given state; React syncs the DOM.
- The **Virtual DOM** lets React diff in memory (**reconciliation**) and commit only the minimal real-DOM changes.
- **JSX is not HTML** — it compiles to `React.createElement` calls and produces plain objects. Use `{ }` for JavaScript **expressions**.
- A component returns **one root**; use **Fragments** (`<>...</>`) to group siblings without an extra DOM node.
- Render conditionally with ternaries and `&&` — but beware the **`0` trap** with `&&`.
- Render lists with `.map()`, and always give each item a **stable, unique `key`** (never the index for dynamic lists).
- Mount with **`createRoot(...).render(...)`**; `StrictMode` double-runs things in dev to catch bugs.

---

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-Components-And-Props.md`](./02-Components-And-Props.md) · **Index:** [`00-Index.md`](./00-Index.md)
