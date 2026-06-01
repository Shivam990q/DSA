# ⚛️ 08 — Performance Optimization ⭐

> *"The fastest render is the one that never happens. React performance is mostly about not re-rendering, not re-computing, and not shipping code the user doesn't need yet. Measure first — most apps are fast enough, and premature memoization is its own kind of slow."*

**Prev:** [`07-Data-Fetching-And-Effects.md`](./07-Data-Fetching-And-Effects.md) · **Next:** [`09-React-Patterns-And-Best-Practices.md`](./09-React-Patterns-And-Best-Practices.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. FIRST PRINCIPLE — WHAT CAUSES A RE-RENDER

To optimize renders you must know exactly what triggers them. A component re-renders when **any** of these happens:

1. Its **state** changes (`setState`).
2. Its **parent** re-renders (by default, children re-render too — regardless of props).
3. Its **context** value changes (if it consumes that context).

```jsx
function Parent() {
  const [count, setCount] = useState(0);
  console.log('Parent render');
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <Child />   {/* Child re-renders on EVERY click — even though it takes no props */}
    </div>
  );
}

function Child() {
  console.log('Child render');   // logs on every parent render
  return <p>I am a child</p>;
}
```

> **Gotcha — "re-render" ≠ "DOM update."** A re-render means React **re-runs your function and re-diffs**. If the output is identical, the *real DOM* isn't touched — the diff is cheap. So most re-renders are harmless. You optimize the ones that are *expensive* (big trees, heavy computation) or *frequent* (typing, scrolling, animations). Don't chase render-count vanity.

> **Myth — "state changes only re-render the changed component."** No: by default a parent's re-render cascades to **all** descendants. Stopping that cascade (when worthwhile) is what `React.memo` is for (Section III).

---

## II. THE CHEAPEST WINS — STRUCTURE BEFORE MEMOIZATION

Before reaching for any memo API, fix the structure. These cost nothing and often eliminate the problem.

### Win 1 — move state down (colocation)

If only a small part of the tree uses some state, push the state into a small component so changing it re-renders only that subtree.

```jsx
// ❌ Search state at the top re-renders the WHOLE page on every keystroke.
function Page() {
  const [query, setQuery] = useState('');
  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ExpensiveDashboard />   {/* re-renders on every keystroke for no reason */}
      <Results query={query} />
    </>
  );
}

// ✅ Isolate the state in a small component. The dashboard never re-renders while typing.
function Page() {
  return (
    <>
      <SearchSection />        {/* owns the query state internally */}
      <ExpensiveDashboard />
    </>
  );
}
```

### Win 2 — lift content up via `children` (pass JSX through)

A component that re-renders does **not** re-render JSX it received as `children` — those elements were created by the parent and keep their identity.

```jsx
// ColorPicker re-renders on color change, but <ExpensiveTree/> (passed as children)
// was created by App and is NOT re-rendered. Free optimization, no memo needed.
function App() {
  return (
    <ColorPicker>
      <ExpensiveTree />
    </ColorPicker>
  );
}

function ColorPicker({ children }) {
  const [color, setColor] = useState('red');
  return (
    <div style={{ borderColor: color }}>
      <input value={color} onChange={(e) => setColor(e.target.value)} />
      {children}   {/* identity stable across ColorPicker's re-renders */}
    </div>
  );
}
```

> **Reach for structure first.** "Move state down" and "pass children through" solve a huge share of perf issues with zero memoization and zero added complexity. Memo APIs are the *second* resort, not the first.

---

## III. `React.memo` — SKIP RE-RENDERS ON UNCHANGED PROPS

`React.memo` wraps a component so it **re-renders only when its props change** (shallow comparison). It breaks the "parent re-render cascades to child" default.

```jsx
import { memo } from 'react';

// Now Child re-renders only when its props change by shallow comparison.
const Child = memo(function Child({ label }) {
  console.log('Child render');
  return <p>{label}</p>;
});

function Parent() {
  const [count, setCount] = useState(0);
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <Child label="static" />   {/* prop never changes → Child does NOT re-render */}
    </>
  );
}
```

### The catch — referential equality

`React.memo` compares props **shallowly** (`Object.is`). Object, array, and function props created during render are **new every time**, so memo sees "changed" and re-renders anyway. This is where `useMemo`/`useCallback` come in — to keep those props' identities stable.

```jsx
const Child = memo(function Child({ config, onClick }) { /* ... */ });

function Parent() {
  const [count, setCount] = useState(0);

  // ❌ New object + new function every render → memo is DEFEATED, Child always re-renders.
  // return <Child config={{ a: 1 }} onClick={() => doThing()} />;

  // ✅ Stable identities → memo works, Child skips re-renders.
  const config = useMemo(() => ({ a: 1 }), []);
  const onClick = useCallback(() => doThing(), []);
  return (
    <>
      <button onClick={() => setCount(count + 1)}>{count}</button>
      <Child config={config} onClick={onClick} />
    </>
  );
}
```

> **The trio is a team (from file 04).** `React.memo` only pays off when **all** non-primitive props are stabilized with `useMemo`/`useCallback`. Memoizing the child but passing it a fresh object every render does nothing. Either stabilize every prop or don't bother memoizing the child.

> **Gotcha — don't `memo` everything.** Each `memo` adds a props comparison on every render. For cheap components rendered a few times, that comparison can cost more than the re-render it prevents. Apply `memo` to components that are **expensive** or render **often in lists** — and measure.

---

## IV. `useMemo` & `useCallback` FOR PERFORMANCE

Covered as concepts in file 04; here's the performance lens.

```jsx
function Analytics({ rows, filter }) {
  // Expensive derived computation — memoize so it only reruns when inputs change.
  const summary = useMemo(() => {
    return rows
      .filter((r) => r.region === filter)
      .reduce((acc, r) => acc + r.amount, 0);   // imagine this is heavy
  }, [rows, filter]);

  return <p>Total: {summary}</p>;
}
```

Two legitimate reasons to memoize:
1. **Expensive computation** — avoid redoing heavy work each render.
2. **Referential stability** — keep an object/array/function identity stable for a `memo` child or a hook dependency.

If neither applies, memoizing is **net negative**: it adds a dependency check and cache, makes code noisier, and can hide bugs. The React team's guidance: write it plainly first; add memoization when a measurement shows a real cost.

> **The future — React Compiler.** React's new compiler (React 19+, opt-in/experimental) auto-memoizes components and values at build time, aiming to make most manual `useMemo`/`useCallback`/`memo` unnecessary. It's worth watching; until it's standard in your stack, the rules above still apply.

---

## V. KEY STABILITY (REVISITED FOR PERFORMANCE)

From file 01: keys give list items identity. For performance, **stable keys let React reuse DOM nodes and component state** across reorders instead of destroying and rebuilding them.

```jsx
// ❌ index keys: insert at top → React thinks every item "changed" → rebuilds + remounts,
//    losing each row's internal state (focus, input text, animation).
{items.map((item, i) => <Row key={i} item={item} />)}

// ✅ stable id keys: insert at top → React inserts ONE node, keeps the rest (and their state).
{items.map((item) => <Row key={item.id} item={item} />)}
```

> **Keys are a performance tool, not just a warning silencer.** Bad keys cause unnecessary unmount/remount cycles — the most expensive kind of DOM work — and reset component state on every list change. Stable, unique keys are one of the highest-leverage perf habits.

---

## VI. CODE SPLITTING — SHIP LESS JAVASCRIPT

A big reason apps feel slow is a huge JS bundle the browser must download and parse before anything is interactive. **Code splitting** breaks the bundle into chunks loaded on demand. React does this with `lazy` + `Suspense`.

```jsx
import { lazy, Suspense } from 'react';

// Each lazy component becomes its own chunk, fetched only when first rendered.
const Dashboard = lazy(() => import('./Dashboard'));   // dynamic import()
const Settings  = lazy(() => import('./Settings'));

function App() {
  const [tab, setTab] = useState('dashboard');
  return (
    <Suspense fallback={<Spinner />}>   {/* shown while the chunk downloads */}
      {tab === 'dashboard' ? <Dashboard /> : <Settings />}
    </Suspense>
  );
}
```

Where to split:
- **Per route** — the biggest win; users only download the page they visit (file 10 shows lazy routes).
- **Heavy components** — charts, editors, maps, modals that aren't needed on first paint.
- **Below-the-fold / behind interaction** — load when revealed.

> **Gotcha — `lazy` needs a `Suspense` boundary above it.** A lazy component throws a promise while loading; the nearest `<Suspense>` catches it and shows the fallback. No boundary → error. Place `Suspense` at a sensible level (per route, or around the lazy region) so the fallback area makes sense.

> **Gotcha — `import()` returns a module with a default export.** `lazy(() => import('./X'))` expects `./X` to `export default` the component. For named exports, map it: `lazy(() => import('./X').then(m => ({ default: m.Named })))`.

---

## VII. SUSPENSE — DECLARATIVE LOADING UI

`Suspense` lets you declare a loading fallback for a region while something inside it isn't ready — whether that's a lazy chunk (above) or data (file 07, React 19 `use()`/`useSuspenseQuery`).

```jsx
<Suspense fallback={<PageSkeleton />}>
  <Profile />          {/* suspends on lazy load or data fetch */}
  <Suspense fallback={<FeedSkeleton />}>
    <Feed />           {/* nested boundary: Feed can load independently of Profile */}
  </Suspense>
</Suspense>
```

> **Nest boundaries to control granularity.** One boundary at the top means the whole region waits for the slowest child. Nested boundaries let fast parts show immediately while slow parts keep their own fallback. This is how you avoid an all-or-nothing loading screen.

---

## VIII. CONCURRENT FEATURES — `useTransition` & `useDeferredValue`

React 18's **concurrent rendering** lets React interrupt a long render to handle something more urgent (like a keystroke). You opt in by marking some updates as **non-urgent**.

### `useTransition` — mark an update as low-priority

```jsx
import { useState, useTransition } from 'react';

function SearchableList({ allItems }) {
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  function handleChange(e) {
    setQuery(e.target.value);                  // URGENT — keep the input responsive
    startTransition(() => {
      // Low-priority: filtering 10k items can be interrupted by more typing.
      setFiltered(allItems.filter((i) => i.includes(e.target.value)));
    });
  }

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending && <span>updating…</span>}    {/* show the list is catching up */}
      <List items={filtered} />
    </>
  );
}
```

### `useDeferredValue` — defer a value's effect on an expensive child

```jsx
function Search({ query }) {
  // deferredQuery "lags behind" query during heavy renders, keeping input snappy.
  const deferredQuery = useDeferredValue(query);
  const results = useMemo(() => expensiveFilter(deferredQuery), [deferredQuery]);
  return <Results items={results} />;
}
```

| Tool | You have… | Use it to… |
|------|-----------|-----------|
| `useTransition` | a state **setter** to call | wrap the non-urgent `setState` so urgent updates win |
| `useDeferredValue` | a **value** (e.g. a prop) | render an expensive child off a deferred copy of the value |

> **When these help.** They shine when an **expensive render** (huge list, complex viz) would otherwise block typing/clicking. They don't make the work faster — they make the UI *feel* responsive by letting urgent updates jump the queue. For genuinely huge lists, also virtualize (next section).

---

## IX. LIST VIRTUALIZATION (WINDOWING)

Rendering 10,000 rows creates 10,000 DOM nodes — slow to mount and scroll. **Virtualization** renders only the rows visible in the viewport (plus a small buffer), recycling them as you scroll.

```jsx
// Using @tanstack/react-virtual (headless virtualization).
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

function BigList({ rows }) {
  const parentRef = useRef(null);
  const virtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 35,        // estimated row height in px
    overscan: 5,                   // render a few extra rows above/below
  });

  return (
    <div ref={parentRef} style={{ height: 400, overflow: 'auto' }}>
      <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
        {virtualizer.getVirtualItems().map((vRow) => (   // only the visible rows
          <div
            key={vRow.key}
            style={{ position: 'absolute', top: 0, transform: `translateY(${vRow.start}px)`,
                     height: vRow.size, width: '100%' }}
          >
            {rows[vRow.index].name}
          </div>
        ))}
      </div>
    </div>
  );
}
```

> **When to virtualize:** long lists/tables/grids (hundreds to thousands of rows), chat logs, infinite feeds. Below ~100 simple rows it's usually unnecessary complexity. Libraries: `@tanstack/react-virtual`, `react-window`, `react-virtuoso`.

---

## X. MEASURE — THE PROFILER & TOOLS

**Never optimize by guessing.** Measure, change, measure again.

- **React DevTools Profiler** — record an interaction; it shows which components rendered, how long each took, and **why** they rendered (enable "Record why each component rendered"). This tells you exactly where the wasted renders are.
- **`<Profiler>` API** — programmatic timing in code:

```jsx
import { Profiler } from 'react';

function onRender(id, phase, actualDuration) {
  // phase: "mount" | "update"; actualDuration: ms spent rendering this commit
  console.log(`${id} (${phase}) took ${actualDuration.toFixed(2)}ms`);
}

<Profiler id="Sidebar" onRender={onRender}>
  <Sidebar />
</Profiler>
```

- **Browser tools** — Lighthouse (bundle size, Core Web Vitals: LCP/INP/CLS), the Network tab (chunk sizes), and your bundler's analyzer (`rollup-plugin-visualizer` for Vite) to find oversized dependencies.

> **The optimization loop:** (1) measure with the Profiler/Lighthouse, (2) find the *actual* bottleneck, (3) apply the cheapest fix (structure → keys → memo → split → virtualize), (4) measure again to confirm. Optimizing un-measured code wastes effort and adds complexity for nothing.

### A quick triage table

| Symptom | Likely cause | First fix |
|---------|--------------|-----------|
| Typing lags | Heavy tree re-renders per keystroke | Move state down; `useTransition`/`useDeferredValue` |
| Whole page re-renders on small change | State too high / context too broad | Colocate state; split context; `children` pass-through |
| List janky on scroll/reorder | Index keys / too many nodes | Stable keys; virtualize |
| Slow first load | Huge JS bundle | Route-based code splitting (`lazy`) |
| Memo child still re-renders | New object/function props | `useMemo`/`useCallback` the props |
| Expensive recompute each render | Unmemoized derivation | `useMemo` it |

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Optimizing without measuring | Wasted effort, complex code | Profile first |
| `memo` child with fresh object/fn props | memo does nothing | Stabilize props with `useMemo`/`useCallback` |
| `useMemo`/`useCallback` everywhere | Slower, noisier code | Use for real cost / stable identity only |
| Index keys on dynamic lists | Remounts, lost state, jank | Stable unique `id` keys |
| State too high in the tree | Over-rendering | Colocate; pass `children` through |
| One broad context | Unrelated re-renders | Split contexts (file 05) |
| `lazy` without `Suspense` | Crash on load | Wrap in `<Suspense fallback>` |
| `lazy` of a named export | "undefined is not a component" | Map to `{ default: m.Named }` |
| Rendering thousands of rows | Slow mount/scroll | Virtualize |
| Expecting concurrent hooks to speed work | Same total work | They reprioritize, not accelerate; also virtualize |

---

## 🧠 KEY TAKEAWAYS

- A component re-renders on **state change, parent re-render, or consumed-context change**; a re-render is **not** automatically a DOM update — optimize the **expensive** and **frequent** ones.
- Try **structure first**: **move state down** (colocate) and **pass JSX as `children`** — both stop re-renders for free.
- **`React.memo`** skips re-renders when props are shallow-equal — but only works if object/array/function props are **stabilized** with `useMemo`/`useCallback`. The trio is a team.
- Memoize for two reasons only: **expensive computation** or **referential stability**. Otherwise it's net-negative overhead.
- **Stable keys** are a real performance tool — they let React reuse DOM and component state instead of remounting.
- **Code splitting** (`lazy` + `Suspense`), especially **per route**, ships less JS and speeds first load; nest **Suspense** boundaries for granular loading.
- **`useTransition`/`useDeferredValue`** keep the UI responsive by reprioritizing expensive renders; **virtualize** very long lists.
- **Always measure** with the **React DevTools Profiler** and Lighthouse, then apply the cheapest fix and measure again.

---

**Prev:** [`07-Data-Fetching-And-Effects.md`](./07-Data-Fetching-And-Effects.md) · **Next:** [`09-React-Patterns-And-Best-Practices.md`](./09-React-Patterns-And-Best-Practices.md) · **Index:** [`00-Index.md`](./00-Index.md)
