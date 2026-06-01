# ⚛️ 07 — Data Fetching & Effects ⭐

> *"Fetching data is the moment your pure UI meets a messy, asynchronous world. Three things will bite you: forgetting to handle loading and errors, leaking state into unmounted components, and rendering a stale response that arrived late. Learn to handle all three by reflex — or let a library handle them for you."*

**Prev:** [`06-Forms-And-Controlled-Components.md`](./06-Forms-And-Controlled-Components.md) · **Next:** [`08-Performance-Optimization.md`](./08-Performance-Optimization.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE THREE STATES OF ASYNC DATA

Any piece of data you fetch is always in one of three states. **Model all three explicitly** or your UI will lie to the user.

```
        ┌──────────┐  request   ┌──────────┐  success   ┌──────────┐
        │  idle    │ ─────────► │ loading  │ ─────────► │ success  │
        └──────────┘            └────┬─────┘            └──────────┘
                                     │ failure
                                     ▼
                                ┌──────────┐
                                │  error   │
                                └──────────┘
```

```jsx
import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [data, setData]       = useState(null);
  const [loading, setLoading] = useState(true);   // start in loading
  const [error, setError]     = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetch(`/api/users/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);   // fetch does NOT throw on 4xx/5xx!
        return res.json();
      })
      .then((json) => setData(json))
      .catch((err) => setError(err))
      .finally(() => setLoading(false));
  }, [userId]);

  // Render every state. Order matters: handle loading/error before assuming data exists.
  if (loading) return <p>Loading…</p>;
  if (error)   return <p role="alert">Error: {error.message}</p>;
  return <h1>{data.name}</h1>;
}
```

> **Gotcha — `fetch` does NOT reject on HTTP errors.** A `404` or `500` still **resolves** the promise; only network failures reject. You must check `res.ok` (or `res.status`) and throw yourself, or your error branch never runs and you crash trying to read `data` that's an error page. (`axios` *does* throw on non-2xx — a key difference.)

---

## II. THE RACE CONDITION — THE BUG YOU CAN'T SEE LOCALLY

When `userId` changes quickly, you fire multiple requests. Responses can arrive **out of order**: you request user 1, then user 2, but user 1's (slower) response lands last and overwrites user 2's data. The screen shows the wrong user. This rarely shows up on fast localhost — and bites in production.

```
request user=1 ───────────────(slow)─────────► resolves LAST  ✗ overwrites
request user=2 ──────(fast)──► resolves FIRST
                                        Final UI shows user 1's data — WRONG.
```

### Fix 1 — the "ignore stale response" flag (the canonical pattern)

```jsx
useEffect(() => {
  let ignore = false;                     // closure flag, unique per effect run

  setLoading(true);
  fetch(`/api/users/${userId}`)
    .then((res) => res.json())
    .then((json) => {
      if (!ignore) setData(json);         // only apply if THIS effect is still current
    });

  return () => { ignore = true; };        // cleanup: mark the previous run stale
}, [userId]);
```

When `userId` changes, React runs the **cleanup** of the previous effect first (`ignore = true`), so the in-flight old request, when it finally resolves, sees `ignore === true` and silently drops its result. Only the latest request can write state.

### Fix 2 — `AbortController` (also cancels the network request)

`AbortController` doesn't just ignore the result — it actually **cancels the HTTP request**, saving bandwidth.

```jsx
useEffect(() => {
  const controller = new AbortController();

  setLoading(true);
  setError(null);
  fetch(`/api/users/${userId}`, { signal: controller.signal })  // pass the signal
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((json) => setData(json))
    .catch((err) => {
      if (err.name === 'AbortError') return;   // expected on cancel — ignore it
      setError(err);
    })
    .finally(() => setLoading(false));

  return () => controller.abort();             // cleanup: cancel the in-flight request
}, [userId]);
```

> **Gotcha — handle `AbortError`.** Aborting a fetch makes its promise reject with an `AbortError`. If you don't filter it out in `.catch`, you'll set a spurious error state on every navigation. Check `err.name === 'AbortError'` and return early.

> **Which to use?** The `ignore` flag is simpler and enough to prevent the *UI* bug. `AbortController` additionally frees the network. For real apps, prefer `AbortController` (and TanStack Query does this for you).

---

## III. THE "STALE CLOSURE" + DEPENDENCY DISCIPLINE

Recall from file 04: an effect captures the props/state from the render it was created in. For fetching, this means **whatever variables your fetch reads must be in the dependency array**, or you'll fetch with stale values.

```jsx
function Search({ query, pageSize }) {
  const [results, setResults] = useState([]);

  // ❌ Missing pageSize: changing pageSize won't refetch — stale results.
  // useEffect(() => { fetchResults(query, pageSize).then(setResults); }, [query]);

  // ✅ All read values declared. ESLint's exhaustive-deps rule enforces this.
  useEffect(() => {
    let ignore = false;
    fetchResults(query, pageSize).then((r) => { if (!ignore) setResults(r); });
    return () => { ignore = true; };
  }, [query, pageSize]);

  return <List items={results} />;
}
```

> **Gotcha — object/function deps refetch every render.** If a dependency is an object/array/function created during render, its identity changes every time, so the effect refetches endlessly. Depend on **primitives** (ids, strings, numbers), or memoize the object with `useMemo` (file 04/08). E.g. depend on `userId`, not the whole `user` object.

> **Don't fetch in an effect that also sets state it depends on** — that's the infinite loop from file 04. Fetch keyed by external inputs (props, params), not by data you set inside the effect.

---

## IV. EXTRACTING A REUSABLE `useFetch` HOOK

Writing the loading/error/race dance in every component is repetitive. Extract it into a custom hook (the pattern from file 04), now hardened.

```jsx
import { useState, useEffect } from 'react';

function useFetch(url, options) {
  const [state, setState] = useState({ data: null, loading: true, error: null });

  useEffect(() => {
    const controller = new AbortController();
    setState({ data: null, loading: true, error: null });

    fetch(url, { ...options, signal: controller.signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => setState({ data, loading: false, error: null }))
      .catch((error) => {
        if (error.name === 'AbortError') return;
        setState({ data: null, loading: false, error });
      });

    return () => controller.abort();
    // NOTE: `options` as a dep is dangerous if it's an inline object — see gotcha.
  }, [url]);  // deliberately only url; document that options must be stable

  return state;
}

// Usage — three lines per consumer.
function Repo({ name }) {
  const { data, loading, error } = useFetch(`https://api.github.com/repos/${name}`);
  if (loading) return <p>Loading…</p>;
  if (error)   return <p>Error: {error.message}</p>;
  return <h2>⭐ {data.stargazers_count}</h2>;
}
```

> **The hard limits of hand-rolled fetching.** `useFetch` still doesn't: cache across components, dedupe identical concurrent requests, refetch on window focus, retry on failure, paginate, or invalidate after a mutation. Every team eventually rebuilds these badly. That's exactly the gap a server-state library fills — and why the rest of this file is TanStack Query.

---

## V. WHY EFFECTS ARE THE WRONG DEFAULT FOR FETCHING

The React team itself now recommends **not** using `useEffect` as your primary data-fetching tool in real apps. The reasons:

- **No caching** — navigate away and back, you refetch from scratch.
- **Waterfalls** — child effects only fire after parents render, serializing requests that could be parallel.
- **Race conditions** — you must hand-handle them every time (Section II).
- **No dedup** — two components needing the same data fire two requests.
- **Boilerplate** — loading/error/cleanup repeated everywhere.

The modern answer is a **server-state library** (TanStack Query, RTK Query) for client apps, or a **framework** (Next.js) that fetches on the server. Effects remain perfect for *non-data* side effects: subscriptions, timers, manual DOM, analytics.

> **Server state is a cache, not state.** This is the file-05 insight again. API data lives on the server; your app holds a *copy* that goes stale. Treat it as a cache with keys, freshness, and invalidation — which is precisely TanStack Query's model.

---

## VI. TANSTACK QUERY (REACT QUERY) — THE DEEP DIVE

[TanStack Query](https://tanstack.com/query) manages server state declaratively. You describe *what* data you need (a query key + a fetch function); it handles caching, deduping, background refetching, retries, and loading/error state.

```bash
npm install @tanstack/react-query
```

```jsx
// Set up one QueryClient and provide it at the root.
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 60_000, retry: 1 },   // data fresh for 60s; retry once on error
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
    </QueryClientProvider>
  );
}
```

### `useQuery` — reading data

```jsx
import { useQuery } from '@tanstack/react-query';

function getTodos() {
  return fetch('/api/todos').then((r) => {
    if (!r.ok) throw new Error('Failed');   // throw → Query marks it an error
    return r.json();
  });
}

function Todos() {
  const {
    data,           // the cached data (undefined until first success)
    isPending,      // first load, no data yet
    isError, error, // error state
    isFetching,     // any fetch in flight (incl. background refetch)
    refetch,        // manual refetch
  } = useQuery({
    queryKey: ['todos'],   // unique cache key — identity of this data
    queryFn: getTodos,
  });

  if (isPending) return <p>Loading…</p>;
  if (isError)   return <p>Error: {error.message}</p>;

  return (
    <>
      {isFetching && <span>refreshing…</span>}
      <ul>{data.map((t) => <li key={t.id}>{t.title}</li>)}</ul>
      <button onClick={() => refetch()}>Refresh</button>
    </>
  );
}
```

What you got for free: caching by `['todos']`, automatic background refetch when the data goes stale, request **deduplication** (ten components using `['todos']` → one network call), retry on failure, and refetch on window refocus/reconnect.

### Query keys with parameters

```jsx
function useUser(userId) {
  return useQuery({
    queryKey: ['user', userId],                         // key includes the param
    queryFn: () => fetch(`/api/users/${userId}`).then((r) => r.json()),
    enabled: userId != null,                            // don't run until we have an id
  });
}
```

> **Query keys are the cache's identity.** `['user', 1]` and `['user', 2]` are separate cache entries; changing the id automatically fetches and caches the new one — and the race condition from Section II is handled internally. Include **every input** the query depends on in the key.

### `staleTime` vs `gcTime` (the two timers everyone confuses)

| Option | Meaning | Default |
|--------|---------|---------|
| `staleTime` | How long data is considered **fresh** (no background refetch while fresh) | `0` (immediately stale) |
| `gcTime` | How long **unused** (no mounted observers) cache is kept before garbage collection | 5 minutes |

```jsx
useQuery({
  queryKey: ['profile'],
  queryFn: getProfile,
  staleTime: 5 * 60_000,   // treat as fresh for 5 min → fewer refetches
  gcTime: 10 * 60_000,     // keep cached 10 min after last component unmounts
});
```

### `useMutation` — writing data

Reads are queries; writes (POST/PUT/DELETE) are **mutations**. After a successful mutation, you **invalidate** related queries so they refetch fresh data.

```jsx
import { useMutation, useQueryClient } from '@tanstack/react-query';

function AddTodo() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (title) =>
      fetch('/api/todos', { method: 'POST', body: JSON.stringify({ title }) })
        .then((r) => r.json()),
    onSuccess: () => {
      // Mark ['todos'] stale → it refetches and the UI updates with the new item.
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return (
    <button onClick={() => mutation.mutate('New task')} disabled={mutation.isPending}>
      {mutation.isPending ? 'Adding…' : 'Add todo'}
    </button>
  );
}
```

### Optimistic updates

Show the change instantly, roll back if the server rejects:

```jsx
const mutation = useMutation({
  mutationFn: toggleTodo,
  onMutate: async (id) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] });
    const previous = queryClient.getQueryData(['todos']);            // snapshot
    queryClient.setQueryData(['todos'], (old) =>                     // apply optimistically
      old.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
    return { previous };                                            // pass to onError
  },
  onError: (_err, _id, context) => {
    queryClient.setQueryData(['todos'], context.previous);          // roll back
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['todos'] }), // resync
});
```

### Pagination & infinite queries

```jsx
// Paginated: keep previous data visible while the next page loads.
function Page({ page }) {
  const { data, isPlaceholderData } = useQuery({
    queryKey: ['projects', page],
    queryFn: () => fetchProjects(page),
    placeholderData: (prev) => prev,   // keep last page's data during fetch (no flicker)
  });
  // ...
}

// Infinite scroll:
import { useInfiniteQuery } from '@tanstack/react-query';
const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ['feed'],
  queryFn: ({ pageParam }) => fetchFeed(pageParam),
  initialPageParam: 0,
  getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
});
```

| Concept | Hook / API | Purpose |
|---------|-----------|---------|
| Read data | `useQuery` | Fetch + cache + states |
| Write data | `useMutation` | POST/PUT/DELETE + lifecycle callbacks |
| Refresh after write | `invalidateQueries` | Mark cache stale → refetch |
| Manual cache edit | `setQueryData` | Optimistic updates, writes |
| Infinite/paginated | `useInfiniteQuery` | Cursor/page-based loading |
| Don't run yet | `enabled: false` | Dependent/lazy queries |

---

## VII. THE `use()` HOOK & SUSPENSE FOR DATA (REACT 19)

React 19 introduced `use()`, which **reads a promise** (or context) during render and integrates with **Suspense**: while the promise is pending, the nearest `<Suspense>` shows a fallback; when it resolves, the component renders with the value. No `loading` boolean in your component.

```jsx
import { use, Suspense } from 'react';

// The component "uses" a promise. React suspends until it resolves.
function Message({ messagePromise }) {
  const message = use(messagePromise);   // unwraps the promise; suspends while pending
  return <p>{message}</p>;
}

function App() {
  const messagePromise = fetchMessage();   // created by a parent / framework / cache
  return (
    <Suspense fallback={<p>Loading…</p>}>   {/* shown while Message is suspended */}
      <Message messagePromise={messagePromise} />
    </Suspense>
  );
}
```

> **Gotcha — don't create the promise inside the suspending component on every render.** `use(fetch(...))` written directly in render starts a new request each render → loops. The promise must come from a stable source: a cache, a parent, or a framework's data layer. This is why `use()` shines with Next.js / TanStack Query (which manage the promise) rather than raw `fetch` in a component.

> **Error handling pairs with Error Boundaries.** A rejected promise read by `use()` is caught by the nearest **Error Boundary** (file 09), and pending by the nearest `Suspense`. Together: declarative loading + error, no booleans. TanStack Query also supports a Suspense mode (`useSuspenseQuery`).

---

## VIII. A QUICK NOTE ON SSR & SERVER COMPONENTS

The cleanest way to avoid most client fetching headaches is to **fetch on the server**. **React Server Components** and frameworks like **Next.js** let you `await` data directly in a component that runs on the server, sending HTML (and data) to the client with no loading flash and no client waterfall.

```jsx
// Next.js App Router (Server Component) — runs on the server, can be async.
async function Page() {
  const res = await fetch('https://api.example.com/posts'); // server-side fetch
  const posts = await res.json();
  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
  // No useEffect, no loading state, no race condition — it's resolved before render.
}
```

> This is a *concept pointer*: the full treatment of SSR/SSG/ISR, Server Components, and server-side data fetching lives in [`../06-NEXTJS/`](../06-NEXTJS/). For a client-only SPA (Vite), TanStack Query is your tool; for production apps that can render on a server, prefer server fetching.

---

## IX. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Not checking `res.ok` | Crash reading error pages as data | `if (!res.ok) throw …` |
| No loading/error states | Blank screen / crash on undefined | Model all three states |
| Race condition on fast param change | Stale/wrong data shown | `ignore` flag or `AbortController` |
| Not handling `AbortError` | Spurious error on navigation | `if (err.name === 'AbortError') return` |
| Missing fetch deps | Stale results, no refetch | List all read values; trust exhaustive-deps |
| Object/function in deps | Endless refetch loop | Depend on primitives or `useMemo` |
| Hand-rolling caching in effects | Bugs, no dedup/refetch | TanStack Query / RTK Query |
| Server data in global client state | Stale, manual invalidation | Server-state library |
| Creating the promise in render for `use()` | Infinite requests | Promise from cache/parent/framework |
| `useEffect` fetch as the default in big apps | Waterfalls, no cache | Server-state lib or SSR |

---

## 🧠 KEY TAKEAWAYS

- Always model the **three states**: loading, error, success — and remember **`fetch` doesn't reject on HTTP errors**; check `res.ok`.
- **Race conditions** are the invisible fetch bug: fix with the **`ignore` flag** (UI) or **`AbortController`** (UI + cancels the request); ignore `AbortError`.
- Declare **all values your fetch reads** in the dependency array; depend on **primitives**, not objects, to avoid refetch loops.
- A custom `useFetch` removes boilerplate but still can't cache, dedupe, retry, or invalidate — the real limits of effect-based fetching.
- The modern guidance is **don't use `useEffect` as your main data-fetching tool**: server data is a **cache**, not state.
- **TanStack Query** manages server state declaratively: `useQuery` (read), `useMutation` (write), `invalidateQueries` (refresh), with caching, dedup, retries, and background refetch built in. Master `queryKey`, `staleTime`, and `gcTime`.
- React 19's **`use()` + Suspense** read promises declaratively (no loading boolean), pairing with **Error Boundaries** — but the promise must come from a stable source.
- For production apps, **server-side fetching** (Server Components / Next.js) sidesteps most client-fetch problems entirely.

---

**Prev:** [`06-Forms-And-Controlled-Components.md`](./06-Forms-And-Controlled-Components.md) · **Next:** [`08-Performance-Optimization.md`](./08-Performance-Optimization.md) · **Index:** [`00-Index.md`](./00-Index.md)
