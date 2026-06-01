# ⚛️ React

> *"React isn't a framework you memorize — it's a mental model you adopt. UI is a function of state. Change the state, and the UI re-derives itself. Internalize that one sentence and everything else is detail."*

> **Section 05 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module takes you from your first JSX expression to architecting a performant, well-structured single-page application with routing, data fetching, and production-grade patterns.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- The **mental model**: UI as a pure function of state, the virtual DOM, and reconciliation
- **JSX** — what it compiles to, and how to wield expressions, fragments, lists, and keys
- **Components and props** — composition, `children`, and the patterns that scale
- **State and events** — `useState`, immutability, batching, and lifting state up
- **Hooks, deeply** — `useEffect`, `useRef`, `useMemo`, `useCallback`, `useReducer`, and custom hooks
- **Context** and an honest map of the **state-management** landscape (Redux Toolkit, Zustand, server state)
- **Forms** — controlled vs uncontrolled, validation, and React Hook Form
- **Data fetching** — effects, race conditions, `AbortController`, and TanStack Query
- **Performance** — what causes re-renders, how to stop the wasteful ones, code splitting, profiling
- **Patterns** — composition, container/presentational, compound components, render props, error boundaries, portals, folder structure
- **Routing** — React Router v6+, nested routes, params, loaders, and protected routes
- **Testing & TypeScript** — React Testing Library, Jest/Vitest, and fully typed components, hooks, and events

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file assumes the ones before it. The ⭐ files are the highest-leverage — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here | — |
| 01 | [`01-React-Fundamentals-And-JSX.md`](./01-React-Fundamentals-And-JSX.md) | What React is, the virtual DOM, reconciliation, JSX, rendering, `createRoot`, conditionals, lists & keys | Core |
| 02 | [`02-Components-And-Props.md`](./02-Components-And-Props.md) | Function components, props, `children`, composition, prop drilling, defaults, PropTypes/TS | ⭐ |
| 03 | [`03-State-And-Events.md`](./03-State-And-Events.md) | `useState`, events, controlled updates, immutability, batching, lifting state up | ⭐ |
| 04 | [`04-Hooks-Deep-Dive.md`](./04-Hooks-Deep-Dive.md) | Rules of hooks, `useEffect`, `useRef`, `useMemo`, `useCallback`, `useReducer`, custom hooks | ⭐⭐ |
| 05 | [`05-Context-And-State-Management.md`](./05-Context-And-State-Management.md) | `useContext`, Context patterns, Redux Toolkit, Zustand, server vs client state | ⭐ |
| 06 | [`06-Forms-And-Controlled-Components.md`](./06-Forms-And-Controlled-Components.md) | Controlled vs uncontrolled, multi-field forms, validation, React Hook Form | Core |
| 07 | [`07-Data-Fetching-And-Effects.md`](./07-Data-Fetching-And-Effects.md) | Fetching in effects, loading/error states, race conditions, `AbortController`, TanStack Query | ⭐ |
| 08 | [`08-Performance-Optimization.md`](./08-Performance-Optimization.md) | Re-render causes, `React.memo`, memo hooks, key stability, lazy/Suspense, profiling | ⭐ |
| 09 | [`09-React-Patterns-And-Best-Practices.md`](./09-React-Patterns-And-Best-Practices.md) | Composition, custom hooks, container/presentational, compound components, render props, error boundaries, portals, folder structure, interview Qs | ⭐ |
| 10 | [`10-Routing-With-React-Router.md`](./10-Routing-With-React-Router.md) | React Router v6+, nested routes, params, navigation, loaders/actions, protected routes | Core |
| 11 | [`11-Testing-And-TypeScript-React.md`](./11-Testing-And-TypeScript-React.md) | React Testing Library, Jest/Vitest, testing hooks/async, TypeScript with React (props/hooks/events/generics), a11y testing | ⭐ |

---

## 🗺️ COMPLETE REACT ROADMAP (coverage checklist)

> A [roadmap.sh](https://roadmap.sh/react)-style exhaustive checklist of **every** React concept worth knowing, each mapped to the file that covers it. If you can tick every box, you know React. Nothing here is left to "you'll pick it up later" — it's all in this section.

### 🧱 Core Foundations

- [x] What React is / library vs framework — **01**
- [x] Virtual DOM, the diffing algorithm & reconciliation — **01**
- [x] `UI = f(state)` declarative mental model — **01**
- [x] JSX deeply (compiles to `createElement`, expressions, rules) — **01**
- [x] Fragments (`<>…</>`) — **01**
- [x] `createRoot` / mounting / `StrictMode` — **01**
- [x] Conditional rendering (ternary, `&&`, early return, the `0` trap) — **01**
- [x] Lists, `.map()`, and **keys** (stable identity, index pitfall) — **01**
- [x] Function components (and recognizing legacy class components) — **02**
- [x] Props, destructuring, one-way data flow, read-only props — **02**
- [x] The `children` prop & composition / named slots — **02**
- [x] Prop drilling (and how to avoid it) — **02**
- [x] Default props (default parameters) & rest/spread pass-through — **02**

### 🎛️ State, Events & Data Flow

- [x] `useState`, lazy init, async/batched updates — **03**
- [x] Functional updates (`setX(prev => …)`) — **03**
- [x] Event handling & SyntheticEvent, `preventDefault` — **03**
- [x] Immutability (objects/arrays, mutating-method traps) — **03**
- [x] Automatic batching (React 18) — **03**
- [x] Lifting state up / single source of truth / derived state — **03**

### 🪝 Hooks (the complete set)

- [x] Rules of Hooks & the call-order secret — **04**
- [x] `useState` (deep notes) — **04**
- [x] `useEffect` (deps, cleanup, lifecycle mapping, stale closures) — **04** · effects-focused deep dive in **07**
- [x] `useRef` (DOM refs + mutable boxes) — **04**
- [x] `useMemo` (memoize values, referential stability) — **04** / **08**
- [x] `useCallback` (memoize functions) — **04** / **08**
- [x] `useReducer` (reducer pattern) — **04**
- [x] `useContext` — **04** (intro) / **05** (full)
- [x] `useLayoutEffect` (sync, pre-paint) — **04**
- [x] `useId` (SSR-safe unique ids) — **04** / **11**
- [x] `useTransition` (non-urgent updates) — **04** / **08**
- [x] `useDeferredValue` (deferred rendering) — **04** / **08**
- [x] `useImperativeHandle` (+ `forwardRef`) — **04**
- [x] `useDebugValue` — **04**
- [x] `useSyncExternalStore` (external store subscriptions) — **05**
- [x] Custom hooks (extracting reusable logic) — **04** / **09**

### 🌐 Context & State Management

- [x] `useContext` + Context patterns (provider, split contexts) — **05**
- [x] Context performance pitfalls & fixes — **05**
- [x] **Redux Toolkit** (slices, store, `useSelector`/`useDispatch`, RTK Query) — **05**
- [x] **Zustand** (minimal store) — **05**
- [x] **Jotai** (atomic state) — **05**
- [x] Server state vs client state distinction — **05** / **07**
- [x] **TanStack Query (React Query)** overview — **05** / deep in **07**

### 📝 Forms

- [x] Controlled vs uncontrolled components — **06**
- [x] Multi-field forms & single change handler — **06**
- [x] Validation (manual + schema) — **06**
- [x] `<textarea>`, `<select>`, checkboxes, radios, file inputs — **06**
- [x] **React Hook Form** — **06**
- [x] **Zod** schema validation + resolver — **06**

### 🔌 Data Fetching & Effects

- [x] Fetching in `useEffect`, loading/error states — **07**
- [x] Race conditions & `AbortController` — **07**
- [x] The "ignore" flag cleanup pattern — **07**
- [x] **TanStack Query** deep (caching, mutations, invalidation, pagination) — **07**
- [x] `use()` hook for reading promises (React 19) — **07**
- [x] Suspense for data fetching (concept) — **07** / **08**

### ⚡ Performance

- [x] What causes re-renders — **08**
- [x] `React.memo` — **08**
- [x] `useMemo` / `useCallback` for performance — **08**
- [x] Key stability & list performance — **08**
- [x] Code splitting, `React.lazy`, `Suspense` — **08**
- [x] The Profiler & measuring renders — **08**
- [x] List virtualization (windowing) — **08**
- [x] Concurrent rendering, `useTransition`, `useDeferredValue` — **08**

### 🧩 Patterns & Architecture

- [x] Composition patterns — **09**
- [x] Custom hook patterns — **09**
- [x] Container / presentational — **09**
- [x] Compound components — **09**
- [x] Render props vs hooks — **09**
- [x] Higher-Order Components (HOCs) — **09**
- [x] **Error Boundaries** — **09**
- [x] **Portals** (`createPortal`) — **09**
- [x] Folder structure & project organization — **09**
- [x] Interview questions — **09**

### 🧭 Routing

- [x] React Router v6+ setup & `<Routes>`/`<Route>` — **10**
- [x] Nested routes & `<Outlet>` — **10**
- [x] URL params, query params, `useParams`/`useSearchParams` — **10**
- [x] Navigation: `<Link>`, `<NavLink>`, `useNavigate` — **10**
- [x] Loaders & actions (data router) — **10**
- [x] Protected / private routes — **10**
- [x] Lazy routes & code splitting — **10**

### 🧪 Testing & TypeScript

- [x] React Testing Library (queries, user-event) — **11**
- [x] Jest vs Vitest — **11**
- [x] Testing async, hooks, context — **11**
- [x] Mocking fetch / modules — **11**
- [x] Accessibility testing — **11**
- [x] TypeScript: typing props, state, events — **11**
- [x] TypeScript: typing hooks, refs, generics, context — **11**

### 🎨 Styling (mapped throughout)

- [x] Inline styles & `className` — **01**
- [x] CSS Modules — **09** (styling section)
- [x] styled-components / CSS-in-JS — **09**
- [x] Tailwind CSS with React — **09**

### 🚀 Modern React (18 & 19)

- [x] Automatic batching — **03**
- [x] Concurrent rendering & transitions — **08**
- [x] `Suspense` & lazy loading — **08**
- [x] `use()` hook — **07**
- [x] Actions & `useActionState` / `useOptimistic` / `useFormStatus` — **06**
- [x] Server Components & SSR concepts (pointer to Next.js) — **08** / [`../06-NEXTJS/`](../06-NEXTJS/)
- [x] Accessibility (a11y) fundamentals — **02** / **06** / **11**

> **Legend:** numbers are the topic files in this folder (e.g. **04** = `04-Hooks-Deep-Dive.md`). A concept listed under two files means it's introduced in the first and treated in depth in the second.

---

## 🛠️ SETUP — A WORKING REACT PROJECT

React is a **library**, not a runtime. You need **Node.js** installed (Node 18+ recommended) and a build tool that bundles your JSX/modules for the browser.

### Verify Node

```bash
node -v    # should print v18.x or newer
npm -v     # comes with Node
```

If you don't have Node, install the LTS from [nodejs.org](https://nodejs.org), or use a version manager like `nvm` / `fnm`.

### The modern default: Vite

[Vite](https://vite.dev) is the recommended way to start a client-side React app today. It's fast, has a great dev server with hot-module reload, and minimal config.

```bash
# Scaffold a new React project (you'll be prompted to pick a framework + variant)
npm create vite@latest my-react-app

# Or skip the prompts: choose React + JavaScript
npm create vite@latest my-react-app -- --template react

# React + TypeScript (recommended once you've done Section 03)
npm create vite@latest my-react-app -- --template react-ts

cd my-react-app
npm install        # install dependencies
npm run dev        # start the dev server → http://localhost:5173
```

The key files in a fresh Vite project:

```
my-react-app/
├── index.html          ← the single HTML page; has <div id="root"></div>
├── package.json        ← scripts + dependencies
├── vite.config.js      ← build config
└── src/
    ├── main.jsx        ← entry point: mounts React into #root
    ├── App.jsx         ← your root component
    └── index.css       ← styles
```

### The older default: Create React App (CRA)

You'll still see **Create React App** in tutorials and older codebases:

```bash
npx create-react-app my-app
cd my-app
npm start            # dev server → http://localhost:3000
```

> **Gotcha — CRA is effectively deprecated.** The React team no longer recommends CRA for new projects; it's slow and unmaintained. Prefer **Vite** for client-only SPAs, or a framework like **Next.js** (see [`../06-NEXTJS/`](../06-NEXTJS/)) when you need server-side rendering, routing, and data fetching built-in. CRA is documented here only so you recognize it.

### Hello, React

```jsx
// src/main.jsx — the entry point
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './index.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

```jsx
// src/App.jsx — your first component
export default function App() {
  return <h1>Welcome to React.</h1>;
}
```

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Build, don't read.** Keep `npm run dev` running and paste every example into a live component. Watch it render.
2. **Break things on purpose.** Forget a key, mutate state directly, leave out a dependency. Read the warning React prints. The warnings are a curriculum.
3. **Open React DevTools.** Install the [React Developer Tools](https://react.dev/learn/react-developer-tools) browser extension early. You'll inspect the component tree, props, state, and (in file 08) profile renders.
4. **Master the model before the ecosystem.** Don't reach for Redux/Zustand/React Query until you've felt the pain they solve. Files 01–04 are the foundation everything else stands on.
5. **JavaScript first.** React is "just JavaScript." If closures, `map`/`filter`, destructuring, spread, and `async/await` feel shaky, revisit [`../02-JAVASCRIPT-MASTERY/`](../02-JAVASCRIPT-MASTERY/) — it pays off tenfold here.

---

## 🔗 RELATED SECTIONS

- **Prerequisite:** [`02-JAVASCRIPT-MASTERY`](../02-JAVASCRIPT-MASTERY/) — React is JavaScript; closures and array methods are non-negotiable.
- **Strongly recommended:** [`03-TYPESCRIPT`](../03-TYPESCRIPT/) — typed props and hooks catch a whole class of bugs. See its `04-TypeScript-With-React.md`.
- **Next:** [`06-NEXTJS`](../06-NEXTJS/) — the production React framework: routing, SSR/SSG, server components, and full-stack data.
- **Backend pairing:** [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/) and [`10-MERN-STACK`](../10-MERN-STACK/) — where the data your components fetch comes from.

---

## 📖 DEEP REFERENCES

- **[react.dev](https://react.dev)** — the official docs. The *Learn* and *Reference* sections are excellent and current. When in doubt, this is the source of truth.
- **[react.dev/reference/react](https://react.dev/reference/react)** — the complete hooks and API reference.
- **[React Router docs](https://reactrouter.com)** — for Section 10.
- **[TanStack Query docs](https://tanstack.com/query)** — for server-state management in Sections 05 & 07.
- **[Redux Toolkit](https://redux-toolkit.js.org)**, **[Zustand](https://zustand.docs.pmnd.rs)**, and **[Jotai](https://jotai.org)** — for Section 05.
- **[React Hook Form](https://react-hook-form.com)** and **[Zod](https://zod.dev)** — for forms & validation in Section 06.
- **[Testing Library](https://testing-library.com/docs/react-testing-library/intro)** and **[Vitest](https://vitest.dev)** — for testing in Section 11.

---

**→ Begin:** [`01-React-Fundamentals-And-JSX.md`](./01-React-Fundamentals-And-JSX.md) | Back to [`../README.md`](../README.md)
