# ⚛️ 05 — Context & State Management ⭐

> *"Most 'we need Redux' moments are really 'we never learned to lift state and compose components' moments. Learn the built-in tools first; reach for a library only when the pain is real and named. Then pick the smallest tool that kills the pain."*

**Prev:** [`04-Hooks-Deep-Dive.md`](./04-Hooks-Deep-Dive.md) · **Next:** [`06-Forms-And-Controlled-Components.md`](./06-Forms-And-Controlled-Components.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE PROBLEM CONTEXT SOLVES

In file 02 you met **prop drilling**: forwarding a prop through layers of components that don't use it, just to reach a deep child. For one or two levels it's fine. For "global-ish" data — the current user, theme, locale, auth token — that nearly every component needs, drilling becomes unbearable noise.

**Context** lets a parent broadcast a value to its entire subtree, and any descendant can read it directly — no forwarding through the middle.

```
Prop drilling:                          Context:
  App ─user→ Page ─user→ Nav ─user→        App
                              Avatar         │  <UserContext.Provider value={user}>
  (every layer forwards user)               Page
                                             Nav
                                              Avatar ──reads── useContext(UserContext)
                                             (middle layers know nothing)
```

> **Context is not a state manager.** It's a *transport* — a way to pass a value down without drilling. The state still lives in some component (usually via `useState`/`useReducer`). Context just makes that value readable anywhere below. Confusing "Context" with "Redux replacement" is the #1 misconception.

---

## II. `useContext` — THE THREE STEPS

Using context is always the same three steps: **create**, **provide**, **consume**.

```jsx
import { createContext, useContext, useState } from 'react';

// 1. CREATE — define the context (optionally a default used when no Provider is found).
const ThemeContext = createContext('light');

// 2. PROVIDE — wrap a subtree and supply the value.
function App() {
  const [theme, setTheme] = useState('dark');
  return (
    <ThemeContext.Provider value={theme}>
      <Toolbar />
      <button onClick={() => setTheme((t) => (t === 'dark' ? 'light' : 'dark'))}>
        Toggle theme
      </button>
    </ThemeContext.Provider>
  );
}

// (middle component — doesn't touch theme at all)
function Toolbar() {
  return <ThemedButton />;
}

// 3. CONSUME — read the nearest Provider's value with useContext.
function ThemedButton() {
  const theme = useContext(ThemeContext);   // "dark"
  return <button className={`btn-${theme}`}>I'm {theme}</button>;
}
```

> **Gotcha — the default value is only used with NO Provider.** `createContext('light')` sets a fallback for components rendered *outside* any matching Provider. Once a Provider wraps the tree, its `value` wins. The default is mostly useful for testing components in isolation and for catching "forgot the Provider" mistakes.

### Providing more than a value: state + updaters together

Usually you provide both the data and the functions to change it, bundled in an object.

```jsx
import { createContext, useContext, useState, useMemo } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  const login = (credentials) => setUser({ name: credentials.name });
  const logout = () => setUser(null);

  // Memoize so consumers don't re-render just because AuthProvider re-rendered
  // and created a brand-new object identity (see Section IV).
  const value = useMemo(() => ({ user, login, logout }), [user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// A custom hook makes consuming clean AND guards against missing Provider.
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (ctx === null) {
    throw new Error('useAuth must be used within an <AuthProvider>');
  }
  return ctx;
}

// Anywhere in the tree:
function ProfileMenu() {
  const { user, logout } = useAuth();
  if (!user) return <a href="/login">Sign in</a>;
  return <button onClick={logout}>Sign out {user.name}</button>;
}
```

> **Pattern — wrap context in a custom hook.** Exposing `useAuth()` instead of making every component import `AuthContext` + `useContext` gives you one place to add the "missing Provider" check, hides the implementation, and reads beautifully. Do this for every context you create.

---

## III. CONTEXT + REDUCER — A MINI REDUX, BUILT IN

Combine `useReducer` (centralized update logic from file 04) with Context (transport) and you get a surprisingly capable global store with **zero dependencies**.

```jsx
import { createContext, useContext, useReducer } from 'react';

const CartContext = createContext(null);

function cartReducer(state, action) {
  switch (action.type) {
    case 'add':    return { ...state, items: [...state.items, action.item] };
    case 'remove': return { ...state, items: state.items.filter((i) => i.id !== action.id) };
    case 'clear':  return { ...state, items: [] };
    default:       throw new Error(`Unknown action: ${action.type}`);
  }
}

export function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [] });
  // Provide BOTH state and dispatch. dispatch identity is stable across renders.
  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error('useCart must be used within <CartProvider>');
  return ctx;
}

// Consumer:
function AddToCart({ product }) {
  const { dispatch } = useCart();
  return <button onClick={() => dispatch({ type: 'add', item: product })}>Add</button>;
}
```

> **Tip — split state and dispatch into two contexts.** Components that only `dispatch` don't care about state changes. If you put `dispatch` in its own context, those components won't re-render when `state` changes. This is a free, real performance win for larger apps.

---

## IV. CONTEXT PERFORMANCE — THE PITFALL EVERYONE HITS

**Every component that calls `useContext(X)` re-renders whenever `X`'s value changes by reference** — even if it only uses a small slice of that value. Two traps follow.

### Trap 1 — a new object value every render

```jsx
// ❌ BAD — value={{...}} creates a NEW object on every AuthProvider render.
// Every consumer re-renders every time, even if user didn't change.
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  return (
    <AuthContext.Provider value={{ user, setUser }}>  {/* new object each render */}
      {children}
    </AuthContext.Provider>
  );
}

// ✅ GOOD — memoize the value object so its identity is stable.
function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const value = useMemo(() => ({ user, setUser }), [user]);  // stable until user changes
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
```

### Trap 2 — one giant context for unrelated data

If theme, user, cart, and locale all live in one context, changing the theme re-renders every consumer of *any* of those. **Split into focused contexts** so unrelated changes don't cascade.

```jsx
// ❌ One mega-context — a theme toggle re-renders cart consumers.
<AppContext.Provider value={{ theme, user, cart, locale }}>

// ✅ Focused contexts — changes are isolated to the relevant consumers.
<ThemeContext.Provider value={theme}>
  <UserContext.Provider value={user}>
    <CartContext.Provider value={cart}>{children}</CartContext.Provider>
  </UserContext.Provider>
</ThemeContext.Provider>
```

| Symptom | Cause | Fix |
|---------|-------|-----|
| All consumers re-render constantly | New `value` object each render | `useMemo` the value |
| Unrelated components re-render | One context holds everything | Split into focused contexts |
| Dispatch-only components re-render | State + dispatch in same context | Separate state and dispatch contexts |

> **When Context isn't enough.** Context has no built-in selector ("re-render me only when `user.name` changes"). For frequently-changing, finely-sliced global state, a dedicated library (Zustand/Redux) with selector-based subscriptions avoids the re-render storms Context can cause. That's the real reason to graduate to a library — not "Context is bad."

---

## V. THE STATE MANAGEMENT LANDSCAPE — A HONEST MAP

Before picking a library, classify your state. **Most "state management" pain is mixing two very different kinds of state.**

| Kind | Examples | Lives where | Tool |
|------|----------|-------------|------|
| **Local UI state** | input value, modal open, hover | `useState` in the component | built-in |
| **Shared client state** | theme, auth user, cart, sidebar | lifted state / Context / store | Context, Zustand, Redux |
| **Server state** | data fetched from an API | a cache synced with the server | **TanStack Query**, RTK Query |
| **URL state** | current route, filters in query string | the URL | React Router (file 10) |
| **Form state** | field values, validation, dirty/touched | form library | React Hook Form (file 06) |

> **The single most important insight in this file:** **server state is not client state.** Data from an API is a *cache* of something that lives elsewhere; it goes stale, needs refetching, deduping, and revalidation. Trying to manage it with Redux/`useState` means reinventing caching badly. Use a server-state library (TanStack Query) for it and your "global state" problem usually shrinks to almost nothing.

### Decision guide

```
Is it server data (from an API)?  ──► TanStack Query / RTK Query (file 07)
Is it in the URL?                 ──► React Router (file 10)
Is it one component's UI detail?  ──► useState
Is it shared by a few components? ──► lift state up, or Context
Is it shared app-wide & changes a lot, with many slices?
                                   ──► Zustand (simple) / Redux Toolkit (large, structured)
```

---

## VI. REDUX TOOLKIT (RTK) — THE STRUCTURED STANDARD

**Redux** is a predictable, centralized store: one global state object, changed only by dispatching **actions** to pure **reducers**. Classic Redux was famously boilerplate-heavy. **Redux Toolkit (RTK)** is the official, modern way — it slashes boilerplate and is the only Redux you should write today.

```bash
npm install @reduxjs/toolkit react-redux
```

### A "slice" — state + reducers + actions in one place

```js
// features/counter/counterSlice.js
import { createSlice } from '@reduxjs/toolkit';

const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    // RTK uses Immer under the hood, so you can "mutate" draft state safely —
    // Immer produces a correct immutable update for you.
    increment: (state) => { state.value += 1; },
    decrement: (state) => { state.value -= 1; },
    addBy:     (state, action) => { state.value += action.payload; },
  },
});

export const { increment, decrement, addBy } = counterSlice.actions; // auto-generated
export default counterSlice.reducer;
```

### The store

```js
// app/store.js
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,    // state.counter
    // ...other slices
  },
  // configureStore auto-wires Redux DevTools + sensible middleware.
});
```

### Wire it up & use it

```jsx
// main.jsx
import { Provider } from 'react-redux';
import { store } from './app/store';

createRoot(document.getElementById('root')).render(
  <Provider store={store}>
    <App />
  </Provider>
);
```

```jsx
// Any component — read with useSelector, change with useDispatch.
import { useSelector, useDispatch } from 'react-redux';
import { increment, addBy } from './features/counter/counterSlice';

function Counter() {
  const value = useSelector((state) => state.counter.value); // subscribe to a SLICE
  const dispatch = useDispatch();
  return (
    <div>
      <span>{value}</span>
      <button onClick={() => dispatch(increment())}>+1</button>
      <button onClick={() => dispatch(addBy(5))}>+5</button>
    </div>
  );
}
```

> **Why `useSelector` matters for performance.** A component re-renders only when the *specific* slice it selects changes (compared with `Object.is`). This selector-based subscription is what Context lacks — it's why Redux scales to large, fast-changing global state without re-render storms. Keep selectors narrow (`state.counter.value`, not the whole `state`).

### Async with `createAsyncThunk`

```js
import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';

export const fetchUser = createAsyncThunk('user/fetch', async (id) => {
  const res = await fetch(`/api/users/${id}`);
  return res.json();   // becomes action.payload on success
});

const userSlice = createSlice({
  name: 'user',
  initialState: { data: null, status: 'idle' },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUser.pending,   (s) => { s.status = 'loading'; })
      .addCase(fetchUser.fulfilled, (s, a) => { s.status = 'done'; s.data = a.payload; })
      .addCase(fetchUser.rejected,  (s) => { s.status = 'error'; });
  },
});
export default userSlice.reducer;
```

> **RTK Query** (built into Redux Toolkit) handles server state — fetching, caching, invalidation — declaratively, similar to TanStack Query. If you're already on Redux, prefer RTK Query over hand-written thunks for data fetching.

> **Gotcha — don't put server data in Redux by hand.** Hand-managing loading/error/cache in slices is exactly the reinvention TanStack Query/RTK Query exist to prevent. Reserve plain Redux slices for genuine *client* state.

---

## VII. ZUSTAND — MINIMAL GLOBAL STATE

**Zustand** ("state" in German) is a tiny store with almost no boilerplate, no Provider required, and selector-based subscriptions. For most apps that just need some shared client state, it's the sweet spot.

```bash
npm install zustand
```

```js
// store/useBearStore.js
import { create } from 'zustand';

// The store is a hook. State + actions live together.
export const useBearStore = create((set) => ({
  bears: 0,
  increase: () => set((state) => ({ bears: state.bears + 1 })),
  reset: () => set({ bears: 0 }),
}));
```

```jsx
// No <Provider> needed. Select exactly the slice you need.
function BearCounter() {
  const bears = useBearStore((state) => state.bears);     // re-renders only when bears changes
  return <h1>{bears} bears</h1>;
}

function Controls() {
  const increase = useBearStore((state) => state.increase); // select just the action
  return <button onClick={increase}>one up</button>;
}
```

> **Why Zustand wins for many teams:** the selector (`(state) => state.bears`) means a component re-renders only when *its* slice changes — Context's biggest weakness, solved, with a fraction of Redux's ceremony. No actions/reducers/dispatch vocabulary, no Provider. Add middleware for persistence (`persist`) or devtools when needed.

```js
// Persisting to localStorage with middleware:
import { persist } from 'zustand/middleware';

export const useSettings = create(
  persist(
    (set) => ({ theme: 'light', setTheme: (t) => set({ theme: t }) }),
    { name: 'settings' }  // localStorage key
  )
);
```

---

## VIII. JOTAI — ATOMIC STATE

**Jotai** takes a different model: state is built from tiny independent **atoms**. You compose atoms instead of slicing one big store. It feels like `useState`, but the state is shareable and can be derived.

```bash
npm install jotai
```

```jsx
import { atom, useAtom } from 'jotai';

// An atom is a unit of state. Define it once, use it anywhere.
const countAtom = atom(0);

// A DERIVED atom — recomputed automatically from other atoms.
const doubledAtom = atom((get) => get(countAtom) * 2);

function Counter() {
  const [count, setCount] = useAtom(countAtom);   // like useState, but shared globally
  const [doubled] = useAtom(doubledAtom);          // read-only derived value
  return (
    <div>
      <p>{count} (doubled: {doubled})</p>
      <button onClick={() => setCount((c) => c + 1)}>+</button>
    </div>
  );
}
```

> **When Jotai fits:** apps with lots of small, interrelated pieces of state where a single big store feels wrong. Atoms avoid the "select a slice of one giant object" model entirely — each atom is its own subscription, so updates are naturally granular.

### Library comparison

| Library | Model | Boilerplate | Provider? | Selectors | Best for |
|---------|-------|-------------|-----------|-----------|----------|
| **Context + useReducer** | built-in transport + reducer | low | yes | no (whole value) | small shared state, no deps |
| **Redux Toolkit** | single store, actions/reducers | medium | yes | yes (`useSelector`) | large apps, strict structure, teams, devtools |
| **Zustand** | hook-based store | very low | no | yes | most "I just need shared state" cases |
| **Jotai** | atomic, bottom-up | very low | optional | per-atom | many small/derived pieces of state |

> **My pragmatic default:** built-in (`useState` + lift + Context) until it hurts → **Zustand** for client state → **TanStack Query** for server state. Redux Toolkit when you specifically want its structure, middleware ecosystem, and time-travel devtools (common on large teams). There's no universally "correct" pick — match the tool to the team and the kind of state.

---

## IX. `useSyncExternalStore` — SUBSCRIBING TO EXTERNAL STORES

React 18 added `useSyncExternalStore` for safely reading from stores **outside** React (your own pub/sub, browser APIs, a vanilla store). Libraries like Zustand and Redux use it internally — you rarely call it directly, but knowing it exists demystifies how those libraries stay in sync with concurrent rendering.

```jsx
import { useSyncExternalStore } from 'react';

// Subscribe to the browser's online/offline status (an "external store").
function useOnlineStatus() {
  return useSyncExternalStore(
    (callback) => {                       // subscribe
      window.addEventListener('online', callback);
      window.addEventListener('offline', callback);
      return () => {
        window.removeEventListener('online', callback);
        window.removeEventListener('offline', callback);
      };
    },
    () => navigator.onLine,               // getSnapshot (client)
    () => true                            // getServerSnapshot (SSR fallback)
  );
}

function StatusBar() {
  const isOnline = useOnlineStatus();
  return <span>{isOnline ? '🟢 Online' : '🔴 Offline'}</span>;
}
```

---

## X. SERVER STATE PREVIEW — TANSTACK QUERY

We go deep in file 07, but it belongs on the state-management map. **TanStack Query (React Query)** manages *server state* — it fetches, caches, dedupes, and revalidates data, handling loading/error/stale automatically.

```bash
npm install @tanstack/react-query
```

```jsx
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Users />
    </QueryClientProvider>
  );
}

function Users() {
  // One hook gives you data + loading + error + caching + background refetch.
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],                                  // cache key
    queryFn: () => fetch('/api/users').then((r) => r.json()),
  });

  if (isLoading) return <p>Loading…</p>;
  if (error)     return <p>Error loading users</p>;
  return <ul>{data.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

> **The mindset shift:** with TanStack Query you stop *storing* server data in global state and start *querying* it by key. Caching, deduping, and refetching are handled. After adopting it, most apps discover they need almost no global client state at all — which is the whole point of separating the two. Full treatment in [`07-Data-Fetching-And-Effects.md`](./07-Data-Fetching-And-Effects.md).

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Treating Context as a state manager | Surprise re-renders, no selectors | Context transports; pair with state, or use a store |
| Inline `value={{...}}` on Provider | All consumers re-render every render | `useMemo` the value object |
| One mega-context for everything | Unrelated updates cascade | Split into focused contexts |
| Reading context without Provider | Get the default value silently | Throw in a custom `useX()` guard |
| Server data in Redux/`useState` | Reinventing caching, stale bugs | TanStack Query / RTK Query |
| Reaching for Redux on day one | Boilerplate for a tiny app | Built-ins → Zustand → Redux only if needed |
| Selecting the whole store | Component re-renders on any change | Narrow selectors (`s => s.counter.value`) |
| Classic Redux (`createStore`, hand reducers) | Massive boilerplate | Redux **Toolkit** (`createSlice`/`configureStore`) |
| Mutating state outside RTK | Broken updates | Only "mutate" inside RTK reducers (Immer); else stay immutable |

---

## 🧠 KEY TAKEAWAYS

- **Context is a transport, not a state manager** — it passes a value down a subtree so you can stop prop drilling. State still lives in a component.
- Use it in three steps: **create → provide → consume**, and wrap consumption in a **custom `useX()` hook** with a missing-Provider guard.
- Context's big pitfalls are an **unmemoized value object** (memoize it) and **one giant context** (split into focused ones); Context has **no selectors**.
- **Classify your state**: local UI, shared client, **server**, URL, and form state are different problems with different tools. The key insight: **server state ≠ client state**.
- **Redux Toolkit** is the modern, low-boilerplate Redux — `createSlice` + `configureStore` + `useSelector`/`useDispatch`, with selector-based subscriptions that scale.
- **Zustand** is minimal global state with selectors and no Provider — the pragmatic default for shared client state. **Jotai** offers an atomic model for many small/derived pieces.
- **TanStack Query / RTK Query** own server state (caching, dedupe, revalidation) — adopt them and your global client state usually shrinks dramatically.
- Pragmatic ladder: **built-ins → Zustand → Redux Toolkit (if structure needed)**, plus **TanStack Query** for server data.

---

**Prev:** [`04-Hooks-Deep-Dive.md`](./04-Hooks-Deep-Dive.md) · **Next:** [`06-Forms-And-Controlled-Components.md`](./06-Forms-And-Controlled-Components.md) · **Index:** [`00-Index.md`](./00-Index.md)
