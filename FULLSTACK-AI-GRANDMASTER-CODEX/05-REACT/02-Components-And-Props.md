# ⚛️ 02 — Components & Props

> *"A component is a function that takes data and returns UI. Props are how a parent hands data down. Get composition right and your app becomes a tree of small, honest functions instead of one tangled monolith."*

**Prev:** [`01-React-Fundamentals-And-JSX.md`](./01-React-Fundamentals-And-JSX.md) · **Next:** [`03-State-And-Events.md`](./03-State-And-Events.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT A COMPONENT IS

A **component** is a JavaScript function that returns JSX. That's the entire definition. It takes input (props), and returns a description of UI.

```jsx
// A component is just a function that returns JSX.
function Welcome() {
  return <h1>Welcome!</h1>;
}

// Use it like an HTML tag. React calls the function and renders what it returns.
function App() {
  return (
    <div>
      <Welcome />
      <Welcome />   {/* reusable — render it as many times as you like */}
    </div>
  );
}
```

> **Gotcha — component names MUST start with a capital letter.** `<welcome />` is treated by React as a built-in HTML tag (and ignored/empty); `<Welcome />` is treated as your component. This capitalization rule is how JSX distinguishes "DOM element" from "your component." Always `PascalCase`.

### Function components vs class components

Modern React is written with **function components + hooks**. **Class components** are legacy — you'll encounter them in old codebases, but write new code as functions.

```jsx
// ✅ MODERN — function component (what you write today)
function Profile({ name }) {
  return <p>{name}</p>;
}

// 🕰️ LEGACY — class component (recognize it, don't write it)
import { Component } from 'react';
class ProfileClass extends Component {
  render() {
    return <p>{this.props.name}</p>;
  }
}
```

| Aspect | Function component | Class component |
|--------|-------------------|-----------------|
| Syntax | Plain function | `class extends Component` |
| State | `useState` hook | `this.state` / `this.setState` |
| Side effects | `useEffect` hook | Lifecycle methods (`componentDidMount`…) |
| `this` | None (no confusion) | Bound `this` everywhere |
| Reuse logic | Custom hooks | HOCs / render props (clunky) |
| React's direction | The future | Maintenance only |

---

## II. PROPS — PASSING DATA DOWN

**Props** (properties) are the arguments you pass to a component. They flow **one way**: from parent to child. The parent owns the data; the child receives a read-only copy.

```jsx
// Parent passes props as attributes.
function App() {
  return <UserCard name="Ada Lovelace" role="Engineer" age={36} verified={true} />;
}

// Child receives a single `props` object.
function UserCard(props) {
  return (
    <div className="card">
      <h2>{props.name}</h2>
      <p>{props.role}, {props.age}</p>
      {props.verified && <span>✔ verified</span>}
    </div>
  );
}
```

### Destructuring props (the idiomatic style)

Almost everyone destructures props in the parameter list — it's cleaner and documents what the component expects.

```jsx
// Destructure right in the signature. Now `name`, `role`, etc. are local variables.
function UserCard({ name, role, age, verified }) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <p>{role}, {age}</p>
      {verified && <span>✔ verified</span>}
    </div>
  );
}
```

### Passing different value types

```jsx
function Demo() {
  return (
    <Widget
      title="Hello"                 // string → quotes
      count={42}                    // number → braces
      active={true}                 // boolean → braces (or just `active` for true)
      tags={['a', 'b', 'c']}        // array → braces
      user={{ id: 1, name: 'Ada' }} // object → braces (note double braces)
      onSave={() => console.log('saved')} // function → braces
    />
  );
}
```

> **Gotcha — `count="42"` vs `count={42}`.** `count="42"` passes the **string** `"42"`; `count={42}` passes the **number** `42`. `"42" + 1` is `"421"`, but `42 + 1` is `43`. Use braces for anything that isn't a literal string.

### Props are READ-ONLY

A component must never modify its own props. Props are an input contract; mutating them breaks React's data flow and causes bugs that are nearly impossible to trace.

```jsx
function BadComponent({ user }) {
  user.name = 'changed';   // ❌ NEVER mutate props — corrupts the parent's data
  return <p>{user.name}</p>;
}

// If a child needs to "change" something, the PARENT owns the state and passes
// down a callback. The child requests a change; the parent performs it.
function GoodComponent({ user, onRename }) {
  return <button onClick={() => onRename('new name')}>{user.name}</button>;
}
```

---

## III. THE `children` PROP — COMPOSITION'S SECRET WEAPON

Whatever you nest *between* a component's opening and closing tags arrives as a special prop called **`children`**. This is the foundation of composition.

```jsx
// Card doesn't know or care what's inside it. It just provides the frame.
function Card({ children }) {
  return <div className="card" style={{ padding: 16, border: '1px solid #ddd' }}>
    {children}
  </div>;
}

// The parent decides the contents. Card wraps ANY UI.
function App() {
  return (
    <>
      <Card>
        <h2>Profile</h2>
        <p>Name: Ada</p>
      </Card>

      <Card>
        <img src="/chart.png" alt="sales" />
        <button>Export</button>
      </Card>
    </>
  );
}
```

This is **composition over configuration**. Instead of giving `Card` 20 props for every possible variation, you let the parent pass arbitrary children. The same `Card` renders a profile, a chart, or anything else.

### Named "slots" via props

When you need multiple distinct regions, pass JSX through named props:

```jsx
function Layout({ header, sidebar, children }) {
  return (
    <div className="layout">
      <header>{header}</header>
      <div className="body">
        <aside>{sidebar}</aside>
        <main>{children}</main>   {/* default slot */}
      </div>
    </div>
  );
}

function App() {
  return (
    <Layout
      header={<h1>Dashboard</h1>}
      sidebar={<nav>...</nav>}
    >
      <p>Main content goes here.</p>   {/* becomes `children` */}
    </Layout>
  );
}
```

> **JSX is a value.** Because a React element is just an object, you can store it in a variable, pass it as a prop, or put it in an array. `header={<h1>Dashboard</h1>}` passes a *piece of UI* as a prop. This unlocks extremely flexible APIs.

---

## IV. COMPOSITION — BUILDING UIs FROM SMALL PIECES

Real UIs are **trees of components**. You decompose a screen into named pieces and compose them back together. Each piece is small, testable, and reusable.

```jsx
// A page composed from focused components.
function ProductPage({ product }) {
  return (
    <Page>
      <Breadcrumbs items={product.path} />
      <ProductHero product={product} />
      <div className="columns">
        <ProductDescription text={product.description} />
        <BuyBox price={product.price} stock={product.stock} />
      </div>
      <Reviews productId={product.id} />
    </Page>
  );
}
```

The art is choosing component boundaries. A good guideline: **a component should do one thing**. If a component is hard to name, it's probably doing too much.

> **Rule of thumb — extract a component when:** (1) a chunk of JSX repeats, (2) a chunk has its own state/logic, or (3) a function is getting too long to read at a glance. Don't pre-extract; let duplication or complexity pull components out of you.

---

## V. PROP DRILLING — AND WHY IT'S A SMELL (AT SCALE)

**Prop drilling** is passing a prop through many intermediate components that don't use it, just to reach a deep child.

```jsx
// `user` is needed only by Avatar, but every layer must forward it. Tedious + fragile.
function App() {
  const user = { name: 'Ada', avatar: '/ada.png' };
  return <Page user={user} />;
}
function Page({ user })   { return <Header user={user} />; }      // doesn't use user
function Header({ user }) { return <Nav user={user} />; }         // doesn't use user
function Nav({ user })    { return <Avatar user={user} />; }      // doesn't use user
function Avatar({ user }) { return <img src={user.avatar} alt={user.name} />; } // finally uses it
```

For one or two levels, drilling is fine — it's explicit and easy to follow. When a prop tunnels through five layers, it becomes noise: every refactor touches files that don't care about the data.

**Solutions** (covered later):
- **Composition** — pass the deep component as `children` so intermediate layers don't see the prop (often the simplest fix).
- **Context** — for truly global-ish data (theme, current user, locale). See [`05-Context-And-State-Management.md`](./05-Context-And-State-Management.md).
- **State libraries** — Redux/Zustand for large shared state.

```jsx
// Composition fix: App injects Avatar directly; Page/Header/Nav just render children.
function App() {
  const user = { name: 'Ada', avatar: '/ada.png' };
  return (
    <Page>
      <Header>
        <Nav>
          <Avatar user={user} />   {/* assembled at the top, no drilling */}
        </Nav>
      </Header>
    </Page>
  );
}
function Page({ children })   { return <div>{children}</div>; }
function Header({ children }) { return <header>{children}</header>; }
function Nav({ children })    { return <nav>{children}</nav>; }
```

---

## VI. DEFAULT PROP VALUES

Give props sensible defaults so callers can omit them. The modern way is **default parameter values** in the destructuring.

```jsx
// Defaults via destructuring — clean and colocated.
function Button({ label = 'Click me', variant = 'primary', disabled = false }) {
  return (
    <button className={`btn btn-${variant}`} disabled={disabled}>
      {label}
    </button>
  );
}

<Button />                              // → "Click me", primary
<Button label="Save" variant="ghost" />// → "Save", ghost
```

> **Gotcha — the legacy `Component.defaultProps`.** Class components and old function components used a static `defaultProps` object. For function components this is **deprecated** in React 19 — use default parameters instead. If you see `MyComponent.defaultProps = {...}` in old code, that's the pattern being replaced.

### The rest/spread pattern for "pass-through" props

Collect extra props with rest syntax and spread them onto an element — great for wrapper components that should accept any standard DOM attribute.

```jsx
// Pull out the props you handle; forward the rest to the <button>.
function IconButton({ icon, ...rest }) {
  return (
    <button {...rest}>      {/* onClick, aria-label, disabled, type… all flow through */}
      <span className="icon">{icon}</span>
    </button>
  );
}

<IconButton icon="🔍" onClick={search} aria-label="Search" disabled={loading} />
```

> **Gotcha — spreading unknown props onto DOM elements.** `{...rest}` is powerful but can leak invalid attributes onto the DOM (React warns about unknown HTML attributes). Only spread onto a real DOM element when you intend to forward standard attributes; otherwise destructure explicitly.

---

## VII. TYPING PROPS — PropTypes vs TypeScript

Props are an implicit contract. Making that contract explicit catches bugs and documents the component.

### PropTypes (runtime checks, plain JS)

```jsx
import PropTypes from 'prop-types';   // npm install prop-types

function UserCard({ name, age, verified }) {
  return <div>{name} ({age}) {verified && '✔'}</div>;
}

// Validated at RUNTIME in development; logs a console warning on mismatch.
UserCard.propTypes = {
  name: PropTypes.string.isRequired,
  age: PropTypes.number,
  verified: PropTypes.bool,
};
```

### TypeScript (compile-time checks — strongly preferred)

```tsx
// Errors caught at COMPILE time, with autocomplete in your editor. The modern standard.
type UserCardProps = {
  name: string;
  age?: number;          // optional
  verified?: boolean;
  onSelect?: (id: string) => void;   // function props are typed too
};

function UserCard({ name, age, verified }: UserCardProps) {
  return <div>{name}{age ? ` (${age})` : ''} {verified && '✔'}</div>;
}
```

| | PropTypes | TypeScript |
|---|-----------|------------|
| When checked | Runtime (dev only) | Compile time |
| Editor autocomplete | No | Yes |
| Setup | `npm i prop-types` | TS toolchain |
| Industry trend | Fading | Standard for new projects |

> **Recommendation.** Use **TypeScript** for any non-trivial project — it catches prop mistakes before the app runs and powers autocomplete. See [`../03-TYPESCRIPT/04-TypeScript-With-React.md`](../03-TYPESCRIPT/04-TypeScript-With-React.md). Use PropTypes only in plain-JS codebases that can't adopt TS.

---

## VIII. A COMPLETE EXAMPLE — COMPOSING A SMALL UI

```jsx
// Reusable presentational components, composed into a feature.

function Badge({ children, color = 'gray' }) {
  return <span className={`badge badge-${color}`}>{children}</span>;
}

function Card({ title, children }) {
  return (
    <div className="card">
      {title && <h3 className="card-title">{title}</h3>}
      <div className="card-body">{children}</div>
    </div>
  );
}

function UserCard({ user, onMessage }) {
  const { name, role, online } = user;
  return (
    <Card title={name}>
      <p>{role}</p>
      <Badge color={online ? 'green' : 'gray'}>
        {online ? 'Online' : 'Offline'}
      </Badge>
      <button onClick={() => onMessage(user.id)}>Message</button>
    </Card>
  );
}

export default function Team() {
  const team = [
    { id: 'u1', name: 'Ada',   role: 'Engineer', online: true  },
    { id: 'u2', name: 'Grace', role: 'Admiral',  online: false },
  ];
  const handleMessage = (id) => console.log('Message', id);

  return (
    <div className="team">
      {team.map((member) => (
        <UserCard key={member.id} user={member} onMessage={handleMessage} />
      ))}
    </div>
  );
}
```

Notice the layering: `Badge` and `Card` are dumb/reusable; `UserCard` composes them with data; `Team` owns the list and the callback. Data flows down via props, events flow up via callbacks.

---

## IX. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Lowercase component name | Renders nothing / treated as HTML tag | Use `PascalCase` |
| Mutating props | Bugs, stale parent data | Treat props as read-only; lift state, use callbacks |
| `prop="42"` when you meant a number | String math bugs (`"42"+1`) | Use braces: `prop={42}` |
| Forgetting `children` exists | Building rigid configure-everything APIs | Accept and render `{children}` |
| Deep prop drilling | Many files forward unused props | Composition, then Context |
| `defaultProps` on function component | Deprecated warning (React 19) | Default parameters in destructuring |
| Spreading `{...rest}` onto DOM blindly | "Unknown attribute" warnings | Forward only intended attributes |
| Returning props mutated/derived in place | Hard-to-trace data flow | Compute locally; never write to props |
| No prop typing on a shared component | Misuse caught only at runtime | TypeScript (preferred) or PropTypes |

---

## 🧠 KEY TAKEAWAYS

- A **component** is a function that returns JSX; its name must be **capitalized**. Write **function components**, not classes.
- **Props** flow **one way** (parent → child) and are **read-only**. To change parent data, pass a **callback** down.
- The **`children`** prop captures nested JSX — the basis of **composition over configuration**.
- Compose UIs as **trees of small, single-purpose components**; extract when JSX repeats or grows complex.
- **Prop drilling** is fine for a level or two; fix deep drilling with **composition**, then **Context**, then state libraries.
- Provide **default values** via destructuring defaults; use **rest/spread** to forward pass-through props (carefully).
- Make the props contract explicit with **TypeScript** (preferred) or PropTypes.

---

**Prev:** [`01-React-Fundamentals-And-JSX.md`](./01-React-Fundamentals-And-JSX.md) · **Next:** [`03-State-And-Events.md`](./03-State-And-Events.md) · **Index:** [`00-Index.md`](./00-Index.md)
