# ⚛️ 11 — Testing & TypeScript with React ⭐

> *"Tests are how you sleep at night; types are how you avoid the bug before it's even written. Test what the user experiences, not how the component is built — and let the type system document and enforce every contract. Together they turn 'I think it works' into 'I know it works.'"*

**Prev:** [`10-Routing-With-React-Router.md`](./10-Routing-With-React-Router.md) · **Next:** [`../06-NEXTJS/00-Index.md`](../06-NEXTJS/00-Index.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE TESTING PHILOSOPHY — TEST BEHAVIOR, NOT INTERNALS

The guiding principle, from Testing Library's author:

> *"The more your tests resemble the way your software is used, the more confidence they give you."*

This means: **test what the user sees and does** — text on screen, clicking buttons, filling inputs — **not** implementation details like state variables, prop names, or which hooks ran. Tests coupled to internals break on every refactor even when the app still works; tests coupled to behavior survive refactors and catch real regressions.

```
❌ Implementation testing:  "after click, this.state.count === 1"
✅ Behavior testing:        "after the user clicks +, the screen shows 1"
```

| Test type | What it checks | Tool | How many |
|-----------|----------------|------|----------|
| **Unit** | a pure function / hook in isolation | Vitest/Jest | many |
| **Component / integration** | a component renders & responds to interaction | RTL + Vitest/Jest | most of your effort |
| **E2E** | the whole app in a real browser | Playwright / Cypress | a few critical flows |

> **Where to invest:** the "testing trophy" (Kent C. Dodds) puts the bulk of effort on **integration/component** tests — they give the most confidence per line. A few E2E tests cover critical paths (login, checkout); unit tests cover tricky pure logic.

---

## II. THE TOOLS — VITEST vs JEST, AND RTL

- **Test runner** — runs tests, gives `describe/it/expect`, mocking, coverage. **Jest** (long-standing, CRA default) or **Vitest** (Vite-native, faster, Jest-compatible API). For a Vite app, **Vitest** is the natural choice.
- **React Testing Library (RTL)** — renders components into a test DOM and queries them the way a user/screen-reader would. It does *not* let you reach into internals — by design.
- **`@testing-library/user-event`** — simulates realistic user interactions (typing, clicking, tabbing) more faithfully than firing raw events.
- **jsdom** — a headless DOM implementation so tests run in Node without a real browser.

```bash
# Vitest setup for a Vite React project
npm install -D vitest @testing-library/react @testing-library/user-event \
  @testing-library/jest-dom jsdom
```

```js
// vite.config.js — enable Vitest with a jsdom environment
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,            // use describe/it/expect without importing
    environment: 'jsdom',     // browser-like DOM
    setupFiles: './src/test/setup.js',
  },
});
```

```js
// src/test/setup.js — adds matchers like toBeInTheDocument()
import '@testing-library/jest-dom';
```

> **Vitest vs Jest API.** They're near-identical (`describe`, `it`, `expect`, `vi`/`jest` for mocks). Vitest uses `vi.fn()` where Jest uses `jest.fn()`. Code and RTL usage are otherwise the same, so examples below work in both with that one swap.

---

## III. YOUR FIRST COMPONENT TEST

```jsx
// Counter.jsx
import { useState } from 'react';
export function Counter() {
  const [count, setCount] = useState(0);
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>Increment</button>
    </div>
  );
}
```

```jsx
// Counter.test.jsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Counter } from './Counter';

describe('Counter', () => {
  it('starts at 0 and increments on click', async () => {
    const user = userEvent.setup();
    render(<Counter />);                       // render into the test DOM

    // Query like a user: find by visible text / accessible role.
    expect(screen.getByText('Count: 0')).toBeInTheDocument();

    const button = screen.getByRole('button', { name: /increment/i });
    await user.click(button);                  // simulate a real click (await it!)

    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });
});
```

Notice: no mention of `useState` or `count`. The test reads like a user story — render, see "Count: 0", click "Increment", see "Count: 1". Refactor the component's internals freely; this test still passes.

---

## IV. QUERIES — HOW TO FIND ELEMENTS (THE RIGHT WAY)

RTL queries have a **priority order** that nudges you toward accessible markup. Prefer the top of this list.

```jsx
// 1. getByRole — BEST. How assistive tech finds things. Covers most elements.
screen.getByRole('button', { name: /submit/i });
screen.getByRole('heading', { level: 1 });
screen.getByRole('textbox', { name: /email/i });   // an <input> with an associated label

// 2. getByLabelText — form fields by their <label> (accessibility-driven).
screen.getByLabelText('Password');

// 3. getByPlaceholderText / getByText — when role/label don't fit.
screen.getByText(/welcome back/i);

// 4. getByTestId — LAST resort, when nothing user-visible identifies it.
screen.getByTestId('chart-canvas');   // needs data-testid="chart-canvas"
```

### The three query variants — `getBy` vs `queryBy` vs `findBy`

| Variant | Returns | Not found | Use when |
|---------|---------|-----------|----------|
| `getBy…` | element | **throws** | element should exist now |
| `queryBy…` | element or `null` | returns `null` | asserting something is **absent** |
| `findBy…` | **Promise** of element | rejects after timeout | element appears **asynchronously** |

```jsx
// Assert absence — must use queryBy (getBy would throw).
expect(screen.queryByText('Error')).not.toBeInTheDocument();

// Wait for async appearance — findBy retries until it shows up (or times out).
expect(await screen.findByText('Loaded!')).toBeInTheDocument();
```

> **Gotcha — `getBy` throws when missing.** Use `queryBy` for "should NOT be there" assertions and `findBy` (awaited) for "will appear later." Using `getBy` for an absent element throws instead of failing the assertion cleanly; using it for async content fails because it doesn't wait.

> **Gotcha — prefer `getByRole`.** If you can't query a button by its accessible name, a screen reader probably can't use it either — so RTL's query difficulty is *also an accessibility signal*. Reaching for `getByTestId` constantly is a hint your markup isn't accessible.

---

## V. TESTING INTERACTIONS, FORMS, AND ASYNC

```jsx
// A login form that calls onSubmit with the entered values.
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { LoginForm } from './LoginForm';

it('submits the entered credentials', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();                       // mock callback (jest.fn() in Jest)
  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'ada@example.com');
  await user.type(screen.getByLabelText(/password/i), 'secret123');
  await user.click(screen.getByRole('button', { name: /log in/i }));

  expect(onSubmit).toHaveBeenCalledWith({ email: 'ada@example.com', password: 'secret123' });
});
```

### Testing async data (with a mocked fetch)

```jsx
import { render, screen, waitFor } from '@testing-library/react';
import { vi, beforeEach, afterEach } from 'vitest';
import { UserProfile } from './UserProfile';

beforeEach(() => {
  // Mock the global fetch to return controlled data — no real network in tests.
  global.fetch = vi.fn(() =>
    Promise.resolve({ ok: true, json: () => Promise.resolve({ name: 'Grace Hopper' }) })
  );
});
afterEach(() => vi.restoreAllMocks());

it('shows a loading state, then the fetched user', async () => {
  render(<UserProfile userId="1" />);

  expect(screen.getByText(/loading/i)).toBeInTheDocument();   // initial loading

  // findBy waits for the async update after fetch resolves.
  expect(await screen.findByText('Grace Hopper')).toBeInTheDocument();
  expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
});
```

> **Gotcha — `act(...)` warnings.** "An update to X was not wrapped in act(...)" means state updated after the test thought it was done — almost always an unawaited async update. The fix is to **`await` user-event calls and use `findBy`/`waitFor`** so RTL flushes pending updates. `userEvent.setup()` + awaiting handles most cases automatically.

> **Better fetch mocking — MSW.** For realistic tests, [Mock Service Worker (MSW)](https://mswjs.io) intercepts requests at the network layer, so you test your real fetch code against fake responses without stubbing `global.fetch`. It's the recommended approach for non-trivial apps.

---

## VI. TESTING HOOKS AND CONTEXT

### Custom hooks with `renderHook`

```jsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

it('increments the counter', () => {
  const { result } = renderHook(() => useCounter(0));

  expect(result.current.count).toBe(0);

  // State updates from outside React events must be wrapped in act().
  act(() => result.current.increment());

  expect(result.current.count).toBe(1);
});
```

### Components that need a provider — a custom `render`

```jsx
// test-utils.jsx — wrap render with the providers your app needs.
import { render } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter } from 'react-router-dom';
import { AuthProvider } from '../context/AuthProvider';

export function renderWithProviders(ui, { route = '/' } = {}) {
  const queryClient = new QueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <MemoryRouter initialEntries={[route]}>{ui}</MemoryRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
```

> **`MemoryRouter` for routing tests.** It keeps history in memory (no real URL), and `initialEntries` lets you start a test on any route. Use it to test route params, navigation, and protected routes (file 10) in isolation.

---

## VII. ACCESSIBILITY TESTING

Accessible markup makes both your app and your tests better (RTL queries *are* a11y checks). Add automated audits with `jest-axe`/`vitest-axe`.

```jsx
import { render } from '@testing-library/react';
import { axe } from 'vitest-axe';   // or 'jest-axe'
import { SignupForm } from './SignupForm';

it('has no detectable accessibility violations', async () => {
  const { container } = render(<SignupForm />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();   // fails on missing labels, bad contrast roles, etc.
});
```

> **Gotcha — automated a11y tools catch ~30–40%.** `axe` finds missing labels, invalid ARIA, and structural issues, but it **cannot** judge whether your tab order is logical, focus is managed in a modal, or content makes sense to a screen-reader user. Full WCAG compliance requires **manual testing with real assistive technology and expert review** — automated checks are a floor, not a ceiling.

Accessibility checklist (recurring across files): semantic elements (`<button>`, `<nav>`, `<main>`), every input has a `<label>`, images have `alt`, interactive elements are keyboard-reachable, focus is visible and managed, color isn't the only signal.

---

## VIII. TYPESCRIPT WITH REACT — TYPING COMPONENTS & PROPS

TypeScript catches prop mistakes at compile time and powers autocomplete. (Foundations in [`../03-TYPESCRIPT/`](../03-TYPESCRIPT/); this is the React-specific layer.) Use a `.tsx` extension for files with JSX.

```tsx
// Type props with a type (or interface). Optional props use ?, defaults via destructuring.
type ButtonProps = {
  label: string;
  variant?: 'primary' | 'secondary';   // union = only these strings allowed
  disabled?: boolean;
  onClick?: () => void;
};

function Button({ label, variant = 'primary', disabled = false, onClick }: ButtonProps) {
  return <button className={`btn-${variant}`} disabled={disabled} onClick={onClick}>{label}</button>;
}

<Button label="Save" variant="primary" />;     // ✅
// <Button label="Save" variant="danger" />;    // ❌ compile error: "danger" not allowed
// <Button variant="primary" />;                 // ❌ compile error: label is required
```

### Typing `children` and common React types

```tsx
import { ReactNode, PropsWithChildren } from 'react';

// children is typed as ReactNode (anything renderable: JSX, string, number, null…).
type CardProps = { title: string; children: ReactNode };
function Card({ title, children }: CardProps) {
  return <section><h2>{title}</h2>{children}</section>;
}

// PropsWithChildren<T> adds children to your props automatically.
type DialogProps = PropsWithChildren<{ open: boolean }>;
```

> **Gotcha — avoid `React.FC` for children.** Older code used `const X: React.FC<Props>`; it implicitly added `children` (even when unwanted) and had other quirks. The current recommendation is to type the props object directly (`function X(props: Props)`) and add `children: ReactNode` explicitly when needed.

---

## IX. TYPESCRIPT — HOOKS, EVENTS, REFS, GENERICS

### Typing hooks

```tsx
// useState usually INFERS the type from the initial value.
const [count, setCount] = useState(0);            // number
const [name, setName] = useState('');             // string

// When initial is null/empty, provide the type explicitly with a generic.
const [user, setUser] = useState<User | null>(null);
const [items, setItems] = useState<string[]>([]);

// useRef: DOM ref starts null; the generic is the element type.
const inputRef = useRef<HTMLInputElement>(null);
inputRef.current?.focus();                         // current is HTMLInputElement | null

// useReducer: type the state and action union.
type Action = { type: 'inc' } | { type: 'add'; amount: number };
function reducer(state: number, action: Action): number {
  switch (action.type) {
    case 'inc': return state + 1;
    case 'add': return state + action.amount;
  }
}
```

### Typing events

```tsx
// Use React's event types — they're generic over the element.
function Form() {
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => console.log(e.target.value);
  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => { e.preventDefault(); };
  const onClick  = (e: React.MouseEvent<HTMLButtonElement>) => console.log(e.clientX);
  const onKey    = (e: React.KeyboardEvent<HTMLInputElement>) => { if (e.key === 'Enter') {} };

  return (
    <form onSubmit={onSubmit}>
      <input onChange={onChange} onKeyDown={onKey} />
      <button onClick={onClick}>Go</button>
    </form>
  );
}
```

> **Tip — let inline handlers infer.** If you write the handler inline (`onChange={(e) => …}`), TypeScript infers `e`'s type from the JSX attribute automatically — no annotation needed. You only annotate when defining the handler *separately* from the JSX.

### Generic components & typed context

```tsx
// A generic List works for any item type, fully type-checked.
type ListProps<T> = {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
};
function List<T>({ items, renderItem }: ListProps<T>) {
  return <ul>{items.map((item, i) => <li key={i}>{renderItem(item)}</li>)}</ul>;
}

<List items={[{ id: 1, name: 'Ada' }]} renderItem={(u) => u.name} />;  // u inferred as {id;name}

// Typed context with a guard hook (file 05 pattern, now type-safe).
import { createContext, useContext } from 'react';
type AuthValue = { user: User | null; login: () => void; logout: () => void };
const AuthContext = createContext<AuthValue | null>(null);

function useAuth(): AuthValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;     // narrowed to AuthValue (not null) after the guard
}
```

| You're typing… | Use |
|----------------|-----|
| Props | `type Props = {…}` then `({}: Props)` |
| children | `children: ReactNode` |
| `useState` (clear initial) | inference; else `useState<T>()` |
| `useRef` to a DOM node | `useRef<HTMLInputElement>(null)` |
| `useReducer` | typed state + **discriminated-union** action |
| Events | `React.ChangeEvent<…>`, `React.FormEvent<…>`, `React.MouseEvent<…>` |
| Reusable component | generics `<T>` |
| Context | `createContext<T \| null>(null)` + guard hook |

---

## X. A COMPLETE TYPED + TESTED EXAMPLE

```tsx
// TodoInput.tsx — typed component
import { useState } from 'react';

type TodoInputProps = { onAdd: (text: string) => void };

export function TodoInput({ onAdd }: TodoInputProps) {
  const [text, setText] = useState('');

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;          // ignore empty
    onAdd(trimmed);
    setText('');
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="todo">New todo</label>
      <input id="todo" value={text} onChange={(e) => setText(e.target.value)} />
      <button type="submit">Add</button>
    </form>
  );
}
```

```tsx
// TodoInput.test.tsx — behavior test
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';
import { TodoInput } from './TodoInput';

it('adds a trimmed todo and clears the input', async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn();
  render(<TodoInput onAdd={onAdd} />);

  const input = screen.getByLabelText(/new todo/i);
  await user.type(input, '  Buy milk  ');
  await user.click(screen.getByRole('button', { name: /add/i }));

  expect(onAdd).toHaveBeenCalledWith('Buy milk');     // trimmed
  expect(input).toHaveValue('');                       // cleared
});

it('ignores an empty submission', async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn();
  render(<TodoInput onAdd={onAdd} />);

  await user.click(screen.getByRole('button', { name: /add/i }));
  expect(onAdd).not.toHaveBeenCalled();
});
```

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Testing implementation details | Tests break on refactor | Test visible behavior (text, roles, clicks) |
| `getBy` for absent element | Throws instead of clean fail | `queryBy…` + `not.toBeInTheDocument()` |
| `getBy` for async content | Fails before it appears | `await findBy…` / `waitFor` |
| Not awaiting `user-event` | `act(...)` warnings, flaky tests | `await user.click(...)`, `userEvent.setup()` |
| Overusing `getByTestId` | Brittle, hides a11y gaps | Prefer `getByRole`/`getByLabelText` |
| Real network in tests | Slow, flaky | Mock `fetch` or use MSW |
| Hook update outside `act` | Warning / wrong result | Wrap updates in `act()` (or use awaited events) |
| `React.FC` for typing | Implicit unwanted `children` | Type props directly; add `children: ReactNode` |
| `any` everywhere | Lost type safety | Type props, state, events properly |
| `useRef` without element generic | `current` typed as `unknown`/wrong | `useRef<HTMLInputElement>(null)` |
| Trusting axe alone for a11y | False sense of compliance | Add manual/assistive-tech testing |

---

## 🧠 KEY TAKEAWAYS

- **Test behavior, not internals** — "the more your tests resemble how the app is used, the more confidence they give." Invest most in **component/integration** tests.
- Use **Vitest** (or Jest) + **React Testing Library** + **user-event**; query with **`getByRole`/`getByLabelText`** first, `getByTestId` last.
- Know the variants: **`getBy`** (must exist, throws), **`queryBy`** (assert absence), **`findBy`** (await async appearance); **await** all user-event calls to avoid `act` warnings.
- **Mock the network** (`vi.fn()` on `fetch`, or **MSW**); test hooks with **`renderHook`** and wrap components needing providers in a custom render (with **`MemoryRouter`** for routing).
- **Automated a11y** (`axe`) catches ~a third of issues — a floor, not full WCAG compliance, which needs manual assistive-tech testing.
- **TypeScript** types **props** (`type Props`), **children** (`ReactNode`), **state/refs/reducers** (generics + discriminated unions), and **events** (`React.ChangeEvent<…>`); avoid `React.FC` and `any`.
- **Generics** make reusable components type-safe; **typed context** + a guard hook removes `null` checks at every call site.
- Types prevent bugs before runtime; tests prove behavior at runtime — use **both**.

---

**Prev:** [`10-Routing-With-React-Router.md`](./10-Routing-With-React-Router.md) · **Next:** [`../06-NEXTJS/00-Index.md`](../06-NEXTJS/00-Index.md) · **Index:** [`00-Index.md`](./00-Index.md)
