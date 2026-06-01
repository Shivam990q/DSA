# ⚛️ 04 — Hooks Deep Dive ⭐

> *"Hooks are how a function component grows a memory and a connection to the outside world. They look like magic until you learn the one secret: React identifies each hook by the ORDER it's called. Everything else follows from that."*

**Prev:** [`03-State-And-Events.md`](./03-State-And-Events.md) · **Next:** [`05-Context-And-State-Management.md`](./05-Context-And-State-Management.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT HOOKS ARE & THE RULES THAT GOVERN THEM

A **hook** is a function whose name starts with `use` that lets a function component "hook into" React features — state, lifecycle, context, refs. Before hooks (2019), only class components could hold state or run side effects. Hooks brought those powers to functions and made logic reusable.

### Why the rules exist — the order secret

React does **not** know which `useState` is which by name. It tracks them by **call order**. On the first render, React creates a list: hook #1, hook #2, hook #3. On every later render, it expects the **exact same sequence**. If the order changes between renders, React hands hook #2's state to hook #3 — chaos.

```
Render 1:  useState('a')  useState('b')  useEffect(...)
            slot 0          slot 1          slot 2
Render 2:  useState('a')  useState('b')  useEffect(...)
            slot 0          slot 1          slot 2   ← order matches → correct

If render 2 SKIPS the first hook (e.g. behind an if):
Render 2:  useState('b')  useEffect(...)
            slot 0          slot 1   ← 'b' now reads slot 0's value → BROKEN
```

### The Two Rules of Hooks

```jsx
function Component({ condition }) {
  // ✅ RULE 1: Only call hooks at the TOP LEVEL.
  //    Never inside conditions, loops, nested functions, or after an early return.
  const [a, setA] = useState(0);
  const [b, setB] = useState(0);

  // ❌ VIOLATION — conditional hook changes call order between renders
  // if (condition) {
  //   const [c, setC] = useState(0);
  // }

  // ❌ VIOLATION — early return BEFORE a hook makes later hooks conditional
  // if (!a) return null;
  // const [d, setD] = useState(0);

  // ✅ RULE 2: Only call hooks from React FUNCTIONS — components or custom hooks.
  //    Not from regular functions, event handlers, or class components.

  return null;
}
```

> **Gotcha — "Rendered fewer/more hooks than during the previous render."** This runtime error means you broke Rule 1: a hook ran conditionally. The fix is always the same — move the hook above any condition/return, and put the *condition inside the hook* instead (e.g. inside the effect body).

> **Tooling:** install the `eslint-plugin-react-hooks` lint plugin. It catches rule violations and missing effect dependencies automatically. Vite's React template includes it. Trust its warnings.

---

## II. `useState` — RECAP & DEEPER NOTES

Covered in file 03; here are the deeper points that matter for the rest of this file.

```jsx
const [state, setState] = useState(initial);
```

- **Initial value is read once.** On re-renders, the `initial` argument is ignored — React returns the stored value.
- **Lazy initialization** avoids recomputing an expensive initial value every render:

```jsx
// ❌ readFromStorage() runs on EVERY render (its return value is just ignored after mount)
const [data, setData] = useState(readFromStorage());

// ✅ React calls the function only ONCE, on mount
const [data, setData] = useState(() => readFromStorage());
```

- **Setting state to the same value bails out.** If you `setState(x)` with a value `Object.is`-equal to the current one, React skips the re-render. (For objects, "same value" means same reference.)
- **Each call to a component has its own independent state.** Two `<Counter />` instances don't share state — state is per-instance.

---

## III. `useEffect` — SYNCHRONIZING WITH THE OUTSIDE WORLD

Rendering should be **pure**: given props/state, return JSX, no side effects. But real apps must talk to the world — fetch data, set timers, subscribe to events, manipulate the DOM directly. `useEffect` is where those **side effects** live. It runs **after** React commits the render to the screen.

```jsx
import { useEffect } from 'react';

useEffect(() => {
  // effect body: runs AFTER render is painted
  // ...do the side effect...

  return () => {
    // OPTIONAL cleanup: runs before the effect re-runs, and on unmount
  };
}, [/* dependency array */]);
```

### The dependency array — the heart of `useEffect`

The second argument controls **when** the effect re-runs:

| Dependency array | When the effect runs |
|------------------|----------------------|
| *omitted* | After **every** render (rarely what you want) |
| `[]` (empty) | **Once**, after the first render (on mount) only |
| `[a, b]` | On mount, then whenever `a` or `b` changed since last render |

```jsx
useEffect(() => { console.log('every render'); });           // no array
useEffect(() => { console.log('mount only'); }, []);          // empty array
useEffect(() => { console.log('when userId changes'); }, [userId]); // deps
```

React compares each dependency to its previous value with `Object.is` (a shallow, reference-based check). If any differ, the effect re-runs (after running the previous effect's cleanup first).

### Cleanup — preventing leaks and stale subscriptions

The function you **return** from an effect is its cleanup. React runs it (1) before re-running the effect, and (2) when the component unmounts. Use it to undo whatever the effect set up.

```jsx
function Clock() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date()), 1000); // set up
    return () => clearInterval(id);                          // tear down
    // Without cleanup, every re-mount adds another interval → leak + flicker.
  }, []);

  return <p>{time.toLocaleTimeString()}</p>;
}
```

```jsx
function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', onResize);          // subscribe
    return () => window.removeEventListener('resize', onResize); // unsubscribe
  }, []);

  return <p>Width: {width}px</p>;
}
```

### Mapping class lifecycle → effects

If you know class components, here's the translation. Function components don't have lifecycle *methods*; they have effects that *synchronize*.

| Class lifecycle | `useEffect` equivalent |
|-----------------|------------------------|
| `componentDidMount` | `useEffect(() => {...}, [])` |
| `componentDidUpdate` | `useEffect(() => {...}, [deps])` |
| `componentWillUnmount` | the **cleanup** return: `useEffect(() => { return () => {...} }, [])` |
| `DidMount` + `DidUpdate` together | `useEffect(() => {...})` (no array) |

> **Mental model shift.** Don't think "run on mount / update / unmount." Think **"keep this external thing in sync with this state."** List everything the effect reads in the deps, add cleanup, and let React run it whenever needed. Effects are about *synchronization*, not *lifecycle timing*.

### Common `useEffect` mistakes

> **Gotcha — the stale closure / missing dependency.** An effect "captures" the props and state from the render it was created in. If you omit a dependency the effect uses, it keeps reading the **stale** value from an old render. The ESLint rule flags this. The fix is to honestly list all dependencies — or restructure so you don't need the stale value (functional updates, `useReducer`, refs).

```jsx
function Poller({ userId }) {
  const [data, setData] = useState(null);

  // ❌ Missing `userId` in deps: if userId changes, this keeps polling the OLD id.
  // useEffect(() => {
  //   const id = setInterval(() => fetchUser(userId).then(setData), 5000);
  //   return () => clearInterval(id);
  // }, []);

  // ✅ Declare userId; effect re-subscribes when it changes.
  useEffect(() => {
    const id = setInterval(() => fetchUser(userId).then(setData), 5000);
    return () => clearInterval(id);
  }, [userId]);

  return <pre>{JSON.stringify(data)}</pre>;
}
```

> **Gotcha — the infinite loop.** An effect that sets state it also depends on re-runs forever: render → effect → setState → render → effect → … Break the cycle: remove the dependency, use a functional update, or guard the update with a condition.

> **Gotcha — object/array dependencies.** `[]`, `{}` literals are a new reference every render, so an effect depending on one runs every time. Memoize the value (`useMemo`) or depend on the primitive fields you actually use.

> **Gotcha — effects run twice in dev (StrictMode).** React 18 StrictMode mounts → unmounts → remounts every component once in development to surface missing cleanup. If your effect breaks when run twice, it has a cleanup bug. This does **not** happen in production. Write effects that are safe to run, clean up, and re-run.

> **You often don't need an effect.** Effects are for *external* systems. You do **not** need an effect to: transform data for rendering (compute it during render), respond to a user event (do it in the handler), or reset state when a prop changes (use a `key`). Reaching for `useEffect` to sync one piece of state to another is usually a smell.

---

## IV. `useRef` — A MUTABLE BOX THAT SURVIVES RENDERS

`useRef` gives you an object `{ current: value }` that:
1. **persists across renders** (like state), but
2. **does NOT trigger a re-render when you change `.current`** (unlike state).

Two main uses: **referencing DOM nodes**, and **storing mutable values** that shouldn't cause renders.

### Use 1 — accessing a DOM node

```jsx
import { useRef } from 'react';

function SearchBox() {
  const inputRef = useRef(null);   // will hold the <input> DOM node

  function focusInput() {
    inputRef.current.focus();      // imperative DOM access — escape hatch
  }

  return (
    <>
      <input ref={inputRef} />     {/* React assigns the node to inputRef.current */}
      <button onClick={focusInput}>Focus the input</button>
    </>
  );
}
```

### Use 2 — a mutable value that isn't UI

```jsx
function Stopwatch() {
  const [elapsed, setElapsed] = useState(0);
  const intervalRef = useRef(null);     // hold the timer id between renders
  const startTimeRef = useRef(0);

  function start() {
    if (intervalRef.current) return;    // already running
    startTimeRef.current = Date.now() - elapsed;
    intervalRef.current = setInterval(() => {
      setElapsed(Date.now() - startTimeRef.current);
    }, 10);
  }

  function stop() {
    clearInterval(intervalRef.current);
    intervalRef.current = null;
  }

  return (
    <div>
      <p>{(elapsed / 1000).toFixed(2)}s</p>
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </div>
  );
}
```

| | `useState` | `useRef` |
|---|-----------|----------|
| Survives re-renders | Yes | Yes |
| Changing it re-renders | **Yes** | **No** |
| Read latest value synchronously | No (next render) | **Yes** (`.current`) |
| Use for | UI data | DOM nodes, timer ids, "instance variables", previous values |

> **Gotcha — don't read/write `ref.current` during render.** Refs are for effects and event handlers. Reading or mutating `.current` while rendering makes render impure and the output unpredictable. Keep render pure; touch refs in handlers/effects.

> **Gotcha — a ref change won't update the screen.** If you mutate `ref.current` expecting the UI to react, nothing happens — that's the whole point of a ref. If the value drives UI, it belongs in state.

---

## V. `useMemo` — CACHING EXPENSIVE COMPUTATIONS

`useMemo` **memoizes** (caches) the result of a calculation, recomputing only when its dependencies change. It's a performance tool — use it when a computation is genuinely expensive or when you need a **stable reference**.

```jsx
import { useMemo } from 'react';

function ProductTable({ products, filterText }) {
  // Without useMemo, this O(n) (or worse) filter+sort runs on EVERY render,
  // even when only an unrelated piece of state changed.
  const visible = useMemo(() => {
    console.log('recomputing list…');
    return products
      .filter((p) => p.name.includes(filterText))
      .sort((a, b) => a.price - b.price);
  }, [products, filterText]);   // recompute only when these change

  return <ul>{visible.map((p) => <li key={p.id}>{p.name}</li>)}</ul>;
}
```

The second crucial use: **referential stability**. Objects/arrays created during render are new each time. If you pass one to a memoized child or use it as an effect dependency, memoize it so its identity is stable.

```jsx
// Stable object identity so the child / effect doesn't see a "new" value every render.
const options = useMemo(() => ({ sort: 'price', limit: 20 }), []);
```

> **Gotcha — don't memoize everything.** `useMemo` has its own cost (the deps comparison + cache). For cheap computations (`a + b`, mapping a tiny array) it's pure overhead and noise. Reach for it when you've measured a real cost or you need stable identity. Premature memoization makes code harder to read for no gain.

---

## VI. `useCallback` — STABLE FUNCTION IDENTITY

Every render creates **new** function objects. Usually harmless — but if you pass a function to a `React.memo`-wrapped child, or use it as an effect dependency, a new identity each render defeats the optimization. `useCallback` memoizes the *function itself*.

```jsx
import { useCallback } from 'react';

function Parent({ items }) {
  const [count, setCount] = useState(0);

  // ❌ New function every render → memoized <List> re-renders even when items didn't change.
  // const handleSelect = (id) => console.log(id);

  // ✅ Same function identity across renders (deps empty here) → <List> can skip re-rendering.
  const handleSelect = useCallback((id) => {
    console.log('selected', id);
  }, []);   // list deps; here it depends on nothing

  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <List items={items} onSelect={handleSelect} />
    </>
  );
}

const List = React.memo(function List({ items, onSelect }) {
  console.log('List render');
  return items.map((i) => <button key={i.id} onClick={() => onSelect(i.id)}>{i.name}</button>);
});
```

`useCallback(fn, deps)` is exactly `useMemo(() => fn, deps)` — it memoizes a function instead of a computed value.

> **Gotcha — `useCallback` is pointless without a reason for stability.** It only helps when the function's *identity* matters: it's passed to a memoized child, or it's a dependency of another hook. Wrapping every handler in `useCallback` for a component that doesn't memoize its children adds overhead and clutter for zero benefit.

> **The trio's relationship:** `React.memo` skips re-rendering a child when its props are unchanged by reference. For that to work, object/array/function props must keep stable identities — which is what `useMemo` and `useCallback` provide. They're a team; using one without the others is often useless.

---

## VII. `useReducer` — STATE LOGIC AS A REDUCER

When state is complex — multiple sub-values that change together, or the next state depends intricately on the previous one and an action — `useReducer` is cleaner than juggling many `useState`s. It centralizes update logic in one pure **reducer** function.

```jsx
import { useReducer } from 'react';

// A reducer: (currentState, action) => newState. Pure — no side effects.
function cartReducer(state, action) {
  switch (action.type) {
    case 'add':
      return { ...state, items: [...state.items, action.item], count: state.count + 1 };
    case 'remove':
      return {
        ...state,
        items: state.items.filter((i) => i.id !== action.id),
        count: state.count - 1,
      };
    case 'clear':
      return { items: [], count: 0 };
    default:
      throw new Error(`Unknown action: ${action.type}`);
  }
}

function Cart() {
  const [state, dispatch] = useReducer(cartReducer, { items: [], count: 0 });

  return (
    <div>
      <p>{state.count} items</p>
      <button onClick={() => dispatch({ type: 'add', item: { id: Date.now(), name: 'X' } })}>
        Add
      </button>
      <button onClick={() => dispatch({ type: 'clear' })}>Clear</button>
    </div>
  );
}
```

```jsx
const [state, dispatch] = useReducer(reducer, initialState);
//     ▲        ▲                     ▲        ▲
//     │        │                     │        └─ starting state
//     │        │                     └─ (state, action) => newState (pure)
//     │        └─ call dispatch(action) to trigger an update
//     └─ current state
```

| Use `useState` when… | Use `useReducer` when… |
|----------------------|------------------------|
| State is simple (a few independent values) | State is complex / many fields change together |
| Updates are straightforward | Update logic is involved and worth centralizing |
| Few transitions | Many distinct action types |
| — | You want to unit-test update logic in isolation (reducer is pure) |
| — | Next state depends heavily on previous state + an action |

> **Why reducers scale.** The reducer is a **pure function** you can test without React. All transitions live in one place, so the logic is auditable. This is the same model Redux uses — learn it here and Redux Toolkit (file 05) is familiar.

---

## VIII. CUSTOM HOOKS — REUSING STATEFUL LOGIC

A **custom hook** is a function that starts with `use` and calls other hooks. It lets you extract and reuse stateful logic between components — the killer feature hooks unlocked. It returns whatever you want (values, setters, functions).

```jsx
// A reusable "is this on/off" hook.
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  const toggle = useCallback(() => setOn((v) => !v), []);
  return [on, toggle];
}

// Two components share the logic, NOT the state — each call gets its own state.
function Modal() {
  const [isOpen, toggleOpen] = useToggle();
  return <button onClick={toggleOpen}>{isOpen ? 'Close' : 'Open'}</button>;
}
```

### A practical custom hook: `useLocalStorage`

```jsx
function useLocalStorage(key, initialValue) {
  // Lazy init: read from storage once on mount.
  const [value, setValue] = useState(() => {
    const stored = localStorage.getItem(key);
    return stored !== null ? JSON.parse(stored) : initialValue;
  });

  // Keep storage in sync whenever value (or key) changes.
  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];   // same shape as useState — feels native
}

// Usage — persists across page reloads automatically.
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Theme: {theme}
    </button>
  );
}
```

### Another: `useFetch` (preview of file 07)

```jsx
function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const controller = new AbortController();    // cancel on cleanup
    setLoading(true);
    setError(null);

    fetch(url, { signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setData)
      .catch((err) => { if (err.name !== 'AbortError') setError(err); })
      .finally(() => setLoading(false));

    return () => controller.abort();             // cleanup: cancel in-flight request
  }, [url]);

  return { data, loading, error };
}

function Profile({ userId }) {
  const { data, loading, error } = useFetch(`/api/users/${userId}`);
  if (loading) return <p>Loading…</p>;
  if (error)   return <p>Error: {error.message}</p>;
  return <h1>{data.name}</h1>;
}
```

> **Custom hooks share logic, not state.** Each component that calls `useToggle()` gets its own independent `on` value. A custom hook is a recipe, not a shared store. To share *state* across components, use Context or a store (file 05).

> **Naming matters.** A custom hook **must** start with `use` — that's how the linter knows to apply the Rules of Hooks to it, and how readers know it may call hooks internally. A function that calls hooks but isn't named `use…` will break the lint checks.

---

## IX. OTHER HOOKS WORTH KNOWING

```jsx
// useContext — read a context value (full treatment in file 05)
const theme = useContext(ThemeContext);

// useLayoutEffect — like useEffect but fires SYNCHRONOUSLY after DOM mutation,
// BEFORE the browser paints. Use ONLY when you must measure/adjust layout to avoid
// a visible flicker. It blocks paint, so prefer useEffect unless you have that need.
useLayoutEffect(() => {
  const { height } = ref.current.getBoundingClientRect();
  setHeight(height);
}, []);

// useId — generate stable unique ids (great for linking <label> and inputs, SSR-safe)
function Field() {
  const id = useId();
  return <><label htmlFor={id}>Name</label><input id={id} /></>;
}

// useTransition / useDeferredValue (React 18) — mark updates as non-urgent so typing
// stays responsive while an expensive list re-renders in the background.
const [isPending, startTransition] = useTransition();
startTransition(() => setQuery(input));   // low-priority update
```

| Hook | One-line purpose |
|------|------------------|
| `useState` | Local component state |
| `useEffect` | Synchronize with external systems (after paint) |
| `useLayoutEffect` | Same, but before paint — for layout measurement |
| `useRef` | Mutable value / DOM handle that doesn't re-render |
| `useMemo` | Cache an expensive computed value |
| `useCallback` | Cache a function's identity |
| `useReducer` | Complex state via a pure reducer |
| `useContext` | Read shared context (file 05) |
| `useId` | Stable unique ids (accessibility, SSR) |
| `useTransition` | Mark state updates as low-priority |

---

## X. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Hook inside `if`/loop/after return | "Rendered fewer/more hooks…" crash | Call hooks at top level only |
| Missing effect dependency | Stale values, bugs the linter warns about | List all deps honestly; restructure if needed |
| Effect sets state it depends on | Infinite render loop | Functional update, guard, or drop the dep |
| Object/array literal in deps | Effect/memo runs every render | `useMemo` the value or depend on primitives |
| Expecting `ref.current` change to re-render | UI doesn't update | If it's UI, use state, not a ref |
| Reading `ref.current` during render | Impure render, flaky output | Touch refs in handlers/effects only |
| `useMemo`/`useCallback` everywhere | Slower, noisier code | Use only for real cost or stable identity |
| `useCallback` with no memoized consumer | Zero benefit, extra code | Remove it unless a memo child/dep needs it |
| Custom hook not named `use…` | Lint can't enforce rules | Prefix with `use` |
| Surprised effect runs twice in dev | StrictMode double-invoke | Ensure cleanup is correct; it's dev-only |
| Using an effect to derive render data | Extra renders, bugs | Compute during render instead |

---

## 🧠 KEY TAKEAWAYS

- React identifies hooks by **call order** — so always call them at the **top level**, never conditionally, and only from components/custom hooks.
- `useEffect` runs side effects **after paint**; the **dependency array** controls when, and the **returned cleanup** undoes setup. Think *synchronization*, not lifecycle.
- The biggest effect bugs are the **stale closure** (missing deps), the **infinite loop** (setting depended-on state), and **unstable object/array deps**.
- `useRef` is a mutable box that **persists without re-rendering** — for DOM nodes and instance-like values. Don't touch it during render.
- `useMemo` caches a **value**, `useCallback` caches a **function**; both exist for performance and **referential stability**, and pair with `React.memo`. Don't over-apply them.
- `useReducer` centralizes complex state in a **pure reducer** — testable, scalable, and the foundation of Redux.
- **Custom hooks** (`use…`) extract and reuse stateful logic; they share **logic, not state**.
- Install `eslint-plugin-react-hooks` and trust its warnings — it enforces the rules and dependency completeness for you.

---

**Prev:** [`03-State-And-Events.md`](./03-State-And-Events.md) · **Next:** [`05-Context-And-State-Management.md`](./05-Context-And-State-Management.md) · **Index:** [`00-Index.md`](./00-Index.md)
