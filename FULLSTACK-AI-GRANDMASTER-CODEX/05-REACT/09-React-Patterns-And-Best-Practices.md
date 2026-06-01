# ⚛️ 09 — React Patterns & Best Practices ⭐

> *"Patterns are crystallized experience — the shapes good React code keeps converging on. Learn them not as rules to apply everywhere, but as tools with a problem each one solves. The mark of seniority is knowing which problem you actually have."*

**Prev:** [`08-Performance-Optimization.md`](./08-Performance-Optimization.md) · **Next:** [`10-Routing-With-React-Router.md`](./10-Routing-With-React-Router.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. COMPOSITION OVER CONFIGURATION (THE FOUNDATIONAL PATTERN)

The single most important React pattern: build flexible components by accepting **`children`** and JSX props, not by piling on configuration booleans. We met this in file 02; here it's the lens for everything else.

```jsx
// ❌ CONFIGURATION — a new prop for every variation. Grows endlessly, hard to extend.
<Dialog
  title="Delete?"
  showIcon
  iconType="warning"
  primaryLabel="Delete"
  secondaryLabel="Cancel"
  showSecondary
/>

// ✅ COMPOSITION — the caller assembles the pieces. Infinitely flexible, no prop explosion.
<Dialog>
  <Dialog.Header><WarningIcon /> Delete?</Dialog.Header>
  <Dialog.Body>This cannot be undone.</Dialog.Body>
  <Dialog.Footer>
    <Button onClick={onCancel}>Cancel</Button>
    <Button variant="danger" onClick={onDelete}>Delete</Button>
  </Dialog.Footer>
</Dialog>
```

> **Heuristic — when you're tempted to add the 6th boolean prop, switch to composition.** A pile of `showX`/`hideY`/`enableZ` props is a smell. Let the consumer compose the variations with children instead.

---

## II. CONTAINER / PRESENTATIONAL (SMART vs DUMB)

Separate components that **fetch/own data and logic** (containers) from those that **just render props** (presentational). Presentational components are reusable, trivially testable, and easy to preview in isolation (Storybook).

```jsx
// PRESENTATIONAL — pure: data in (props), UI out. No fetching, no global state.
function UserCard({ user, onMessage }) {
  return (
    <div className="card">
      <h3>{user.name}</h3>
      <button onClick={() => onMessage(user.id)}>Message</button>
    </div>
  );
}

// CONTAINER — owns data + behavior, renders the presentational component.
function UserCardContainer({ userId }) {
  const { data: user, isPending } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  const handleMessage = (id) => openChat(id);

  if (isPending) return <CardSkeleton />;
  return <UserCard user={user} onMessage={handleMessage} />;
}
```

> **Modern nuance.** Hooks blurred this line — a custom hook (`useUser(id)`) often replaces a separate container component, putting data logic *inside* the component while staying testable. Treat container/presentational as a *guideline for separation of concerns*, not a mandatory two-file rule. The goal is: **keep rendering pure and put effects/data behind a hook**.

---

## III. CUSTOM HOOKS — THE PRIMARY REUSE MECHANISM

From file 04: a custom hook (`use…`) extracts stateful logic so multiple components share the **logic** (not the state). This is React's answer to the old HOC/render-prop reuse problems — cleaner and composable.

```jsx
// Reusable behavior: track an element's hover state.
function useHover() {
  const [hovering, setHovering] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;
    const onEnter = () => setHovering(true);
    const onLeave = () => setHovering(false);
    node.addEventListener('mouseenter', onEnter);
    node.addEventListener('mouseleave', onLeave);
    return () => {
      node.removeEventListener('mouseenter', onEnter);
      node.removeEventListener('mouseleave', onLeave);
    };
  }, []);

  return [ref, hovering];
}

function Card() {
  const [ref, hovering] = useHover();
  return <div ref={ref}>{hovering ? '👋 Hi!' : 'Hover me'}</div>;
}
```

> **Hooks compose.** A custom hook can call other custom hooks: `useUserDashboard` might call `useUser`, `useTheme`, and `usePermissions`. This composition — small hooks built into bigger ones — is how mature React apps organize logic.

---

## IV. COMPOUND COMPONENTS

**Compound components** are a set of components that work together and share implicit state via context, exposing a flexible, declarative API. Think `<select>` + `<option>`, or the `<Dialog>` above. The parent holds state; children read it through context.

```jsx
import { createContext, useContext, useState } from 'react';

const TabsContext = createContext(null);

function Tabs({ children, defaultTab }) {
  const [active, setActive] = useState(defaultTab);
  return <TabsContext.Provider value={{ active, setActive }}>{children}</TabsContext.Provider>;
}

function TabList({ children }) {
  return <div className="tab-list" role="tablist">{children}</div>;
}

function Tab({ id, children }) {
  const { active, setActive } = useContext(TabsContext);
  return (
    <button role="tab" aria-selected={active === id}
            className={active === id ? 'tab active' : 'tab'}
            onClick={() => setActive(id)}>
      {children}
    </button>
  );
}

function TabPanel({ id, children }) {
  const { active } = useContext(TabsContext);
  return active === id ? <div role="tabpanel">{children}</div> : null;
}

// Attach children as properties for a clean namespace: <Tabs.Tab/>, <Tabs.Panel/>.
Tabs.List = TabList;
Tabs.Tab = Tab;
Tabs.Panel = TabPanel;

// Usage — declarative, flexible, the state is invisible to the caller.
function Settings() {
  return (
    <Tabs defaultTab="general">
      <Tabs.List>
        <Tabs.Tab id="general">General</Tabs.Tab>
        <Tabs.Tab id="billing">Billing</Tabs.Tab>
      </Tabs.List>
      <Tabs.Panel id="general">General settings…</Tabs.Panel>
      <Tabs.Panel id="billing">Billing settings…</Tabs.Panel>
    </Tabs>
  );
}
```

> **Why compound components are great APIs.** The consumer arranges the pieces freely (reorder tabs, add custom markup between them) without you predicting every layout via props. The shared state stays an implementation detail. This is the pattern behind most good headless UI libraries (Radix, Headless UI).

---

## V. RENDER PROPS vs HOCs vs HOOKS — THE EVOLUTION

Before hooks, two patterns shared logic. Know them — you'll meet them in older code and libraries — but reach for **hooks** in new code.

### Render props — a prop that's a function returning UI

```jsx
// The component manages state and CALLS children as a function with that state.
function MouseTracker({ children }) {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  return (
    <div onMouseMove={(e) => setPos({ x: e.clientX, y: e.clientY })}>
      {children(pos)}   {/* children is a function: (pos) => JSX */}
    </div>
  );
}

// Usage:
<MouseTracker>
  {({ x, y }) => <p>Mouse at {x}, {y}</p>}
</MouseTracker>
```

### Higher-Order Component (HOC) — a function that wraps a component

```jsx
// Takes a component, returns an enhanced one. (React Router/Redux used these.)
function withLoading(Component) {
  return function WithLoading({ isLoading, ...props }) {
    if (isLoading) return <Spinner />;
    return <Component {...props} />;
  };
}

const UserListWithLoading = withLoading(UserList);
```

### The hook version (preferred today)

```jsx
function useMousePosition() {
  const [pos, setPos] = useState({ x: 0, y: 0 });
  useEffect(() => {
    const onMove = (e) => setPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', onMove);
    return () => window.removeEventListener('mousemove', onMove);
  }, []);
  return pos;
}

function Component() {
  const { x, y } = useMousePosition();   // no wrapper components, no "JSX pyramid"
  return <p>{x}, {y}</p>;
}
```

| Pattern | Pros | Cons | Today |
|---------|------|------|-------|
| Render props | Flexible, explicit | "Wrapper hell" nesting, verbose | Rare; sometimes for headless UI |
| HOC | Composable, pre-hooks standard | Prop collisions, indirection, hard to type | Legacy; you'll read it |
| **Custom hook** | Clean, composable, no wrappers | Must follow Rules of Hooks | **Default** |

> **Gotcha — HOC pitfalls.** HOCs can silently collide on prop names, swallow refs (need `forwardRef`), and stack into deep, hard-to-debug trees. Hooks avoid all of this. Convert HOC logic to hooks when you can.

---

## VI. ERROR BOUNDARIES — CATCHING RENDER CRASHES

By default, a JavaScript error during rendering **unmounts the entire React tree** — a blank white screen. An **Error Boundary** catches errors in its subtree and renders a fallback instead, containing the blast radius.

```jsx
import { Component } from 'react';

// Error boundaries MUST be class components — there's no hook equivalent yet.
class ErrorBoundary extends Component {
  state = { hasError: false, error: null };

  // Render the fallback on the next render after a child throws.
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  // Side effect: log the error to a reporting service (Sentry, etc.).
  componentDidCatch(error, info) {
    console.error('Caught by boundary:', error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? <p role="alert">Something went wrong.</p>;
    }
    return this.props.children;
  }
}

// Usage — wrap risky regions; place several so one crash doesn't blank the app.
function App() {
  return (
    <ErrorBoundary fallback={<AppCrash />}>
      <Header />
      <ErrorBoundary fallback={<WidgetError />}>
        <FlakyWidget />   {/* if this throws, only the widget shows the fallback */}
      </ErrorBoundary>
    </ErrorBoundary>
  );
}
```

> **Gotcha — error boundaries DON'T catch everything.** They catch errors during **rendering, lifecycle methods, and constructors** of their children. They do **not** catch: event handlers (use try/catch there), async code (`setTimeout`, promises), SSR errors, or errors in the boundary itself. For event/async errors, handle them where they happen and set error state manually.

> **Practical advice.** Use the maintained `react-error-boundary` package for a hook-friendly API (`useErrorBoundary`, reset keys) instead of hand-writing the class each time. Place boundaries at route level and around independently-failing widgets.

---

## VII. PORTALS — RENDERING OUTSIDE THE PARENT DOM

A **portal** renders children into a **different DOM node**, outside the parent's hierarchy — while keeping them in the React tree (so context, state, and events still work). Essential for modals, tooltips, and toasts that must escape parent `overflow: hidden` or `z-index` traps.

```jsx
import { createPortal } from 'react-dom';

function Modal({ open, onClose, children }) {
  if (!open) return null;
  // Render into document.body instead of wherever <Modal> sits in the tree.
  return createPortal(
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>   {/* don't close on inner click */}
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>,
    document.body   // the target DOM node
  );
}

function Page() {
  const [open, setOpen] = useState(false);
  return (
    <div style={{ overflow: 'hidden' }}>   {/* would clip a normal child — portal escapes it */}
      <button onClick={() => setOpen(true)}>Open modal</button>
      <Modal open={open} onClose={() => setOpen(false)}>
        <h2>Hello from a portal</h2>
      </Modal>
    </div>
  );
}
```

> **Gotcha — events bubble through the React tree, not the DOM tree.** A click inside a portal bubbles to its React **parent**, even though the DOM node lives in `document.body`. This is usually what you want (handlers keep working), but it surprises people debugging event propagation. Remember: portals move the DOM, not the React parent-child relationship.

> **Accessibility for modals:** trap focus inside, return focus on close, close on `Escape`, and add `role="dialog"` + `aria-modal="true"`. Hand-rolling this correctly is hard — prefer Radix/Headless UI dialogs in production.

---

## VIII. STYLING REACT — THE OPTIONS

There's no single "React way" to style; here are the mainstream approaches with their tradeoffs.

### CSS Modules — scoped, plain CSS

```jsx
// Button.module.css → class names are hashed/scoped to this file, no global clashes.
import styles from './Button.module.css';

function Button({ children }) {
  return <button className={styles.primary}>{children}</button>;
  // styles.primary becomes something like "Button_primary__a1b2c"
}
```

```css
/* Button.module.css */
.primary { background: rebeccapurple; color: white; padding: 8px 16px; }
```

### styled-components (CSS-in-JS)

```jsx
import styled from 'styled-components';   // npm install styled-components

// Styles live in JS, scoped automatically, with props-driven dynamic styling.
const Button = styled.button`
  background: ${(props) => (props.$primary ? 'rebeccapurple' : 'gray')};
  color: white;
  padding: 8px 16px;
  &:hover { opacity: 0.9; }
`;

<Button $primary>Save</Button>
```

### Tailwind CSS — utility classes

```jsx
// Compose styles from atomic utility classes directly in className. npm + config setup.
function Button({ children }) {
  return (
    <button className="bg-purple-700 text-white px-4 py-2 rounded hover:opacity-90">
      {children}
    </button>
  );
}
```

| Approach | Scoping | Dynamic styles | Runtime cost | Notes |
|----------|---------|----------------|--------------|-------|
| Plain CSS / global | none (global) | hard | none | clashes at scale |
| **CSS Modules** | per-file (build) | via class toggling | none | simple, safe default |
| **styled-components** | automatic | excellent (props) | small runtime | colocated, dynamic; CSS-in-JS |
| **Tailwind** | utility (no naming) | via conditional classes | none (build) | fast to write, verbose markup |
| Inline `style={{}}` | element-only | easy | re-created each render | no pseudo/media; use sparingly |

> **Pragmatic guidance.** **Tailwind** dominates new projects for speed and consistency; **CSS Modules** is a great zero-dependency default; **styled-components** suits design systems needing heavy prop-driven theming. There's no wrong answer — pick one per project and stay consistent. For conditional classes, the `clsx`/`classnames` helper keeps `className` readable.

```jsx
import clsx from 'clsx';   // tidy conditional class names
<button className={clsx('btn', { 'btn-active': isActive, 'btn-disabled': disabled })} />
```

---

## IX. FOLDER STRUCTURE & PROJECT ORGANIZATION

Two common structures. Start simple; adopt feature-based as the app grows.

```
# Small app — group by TYPE
src/
├── components/      # reusable UI (Button, Card, Modal)
├── pages/           # route-level screens
├── hooks/           # custom hooks (useAuth, useFetch)
├── context/         # context providers
├── services/        # API clients
├── utils/           # pure helpers
└── App.jsx

# Larger app — group by FEATURE (scales better)
src/
├── features/
│   ├── auth/        # everything auth: components, hooks, api, slice, types
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api.js
│   │   └── authSlice.js
│   └── cart/
├── components/      # truly shared/generic UI
├── lib/             # shared utilities, API setup
└── App.jsx
```

> **Principle — colocate by change, not by type.** Files that change together should live together. Feature folders mean adding/removing a feature touches one directory, not five. The type-based layout is fine for small apps but spreads a single feature across `components/`, `hooks/`, `services/`, etc., as it grows.

### General best-practices checklist

- **One component, one job.** If it's hard to name, it's doing too much — split it.
- **Keep render pure.** No fetching/mutation during render; effects and handlers do side effects.
- **Derive, don't duplicate.** Compute from state; don't store derived values (file 03).
- **Lift state only as high as needed** (file 03); colocate otherwise (file 08).
- **Name custom hooks `use…`** and keep them focused.
- **Type your props** (TypeScript, file 11).
- **Stable keys**, never index for dynamic lists (file 01/08).
- **Accessibility is not optional**: semantic elements, labels, `alt`, keyboard support.

---

## X. INTERVIEW QUESTIONS (RAPID REVIEW)

> Short, honest answers to the React questions that come up most. Each links back to the file with the full story.

- **What's the virtual DOM and reconciliation?** An in-memory tree React diffs against the previous one to compute minimal real-DOM changes. (file 01)
- **Why keys?** Stable identity for list items so React reuses nodes/state across reorders; never use index for dynamic lists. (file 01/08)
- **`useState` vs `useReducer`?** `useState` for simple/independent values; `useReducer` for complex transitions centralized in a pure reducer. (file 04)
- **What does `useEffect`'s dependency array do?** Controls when the effect re-runs; cleanup runs before re-run and on unmount; omitting deps you read causes stale closures. (file 04/07)
- **`React.memo`/`useMemo`/`useCallback` — when?** To skip re-renders / cache values / stabilize function identity — only for expensive or frequently-rendered cases; they're a team. (file 04/08)
- **Controlled vs uncontrolled?** React state owns the value vs the DOM owns it (read via ref). Controlled is the default. (file 06)
- **How do you fetch data and avoid race conditions?** Handle loading/error, use an `ignore` flag or `AbortController`; prefer TanStack Query in real apps. (file 07)
- **Context vs Redux?** Context transports a value (no selectors); Redux/Zustand are stores with selector-based subscriptions for large/fast-changing state. (file 05)
- **What's an error boundary and what can't it catch?** A class component that catches render-phase errors; not event handlers or async. (this file)
- **Why do effects run twice in dev?** StrictMode double-invokes to surface missing cleanup; dev-only. (file 04)
- **Prop drilling fixes?** Composition (`children`), then Context, then a store. (file 02/05)
- **What are React 18/19 features?** Automatic batching, concurrent rendering, `useTransition`/`useDeferredValue`, Suspense for data, `use()`, Actions. (file 03/06/07/08)

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Config-prop explosion | Unmaintainable component API | Composition / compound components |
| HOC prop collisions / ref loss | Mysterious overrides, broken refs | Prefer custom hooks; `forwardRef` if needed |
| No error boundaries | One crash blanks the whole app | Wrap routes/widgets in boundaries |
| Expecting boundaries to catch events/async | Errors slip through | try/catch in handlers; manual error state |
| Modal clipped by `overflow:hidden` | Modal cut off / behind content | `createPortal` to `document.body` |
| Confused by portal event bubbling | Handlers fire "unexpectedly" | Events follow the React tree, not DOM |
| Mixing styling approaches | Inconsistent, bloated CSS | Pick one per project |
| Type-based folders at scale | Features spread across dirs | Group by feature |
| God components | Hard to test/reuse | One responsibility; extract |
| Reaching for HOC/render props in new code | Wrapper hell | Use hooks |

---

## 🧠 KEY TAKEAWAYS

- **Composition over configuration** is the root pattern: accept `children`/JSX rather than endless config props.
- **Container/presentational** separates data/logic from pure rendering; **custom hooks** are the modern way to achieve that separation and reuse logic.
- **Compound components** share implicit state via context for flexible, declarative APIs (`<Tabs.Tab/>`).
- **Render props** and **HOCs** are legacy reuse patterns — recognize them, but use **hooks** in new code.
- **Error boundaries** (class components) catch **render-phase** crashes and show a fallback; they do **not** catch event-handler or async errors.
- **Portals** (`createPortal`) render into another DOM node (modals/tooltips) while staying in the React tree — events bubble through the React parent.
- Styling has several valid options — **CSS Modules**, **styled-components**, **Tailwind** — pick one per project and stay consistent.
- Organize **by feature** as apps grow (colocate what changes together); keep components single-purpose, render pure, props typed, and accessibility built in.

---

**Prev:** [`08-Performance-Optimization.md`](./08-Performance-Optimization.md) · **Next:** [`10-Routing-With-React-Router.md`](./10-Routing-With-React-Router.md) · **Index:** [`00-Index.md`](./00-Index.md)
