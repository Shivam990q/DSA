# ⚛️ 03 — Building The React Frontend

> *"The backend is correct. The frontend is felt. A user never reads your service layer — they feel the spinner, the empty list, the error that explains itself. The seam between them is one axios call and three states you must never forget."*

**Prev:** [`02-Building-The-Backend-API.md`](./02-Building-The-Backend-API.md) · **Next:** [`04-Authentication-Across-The-Stack.md`](./04-Authentication-Across-The-Stack.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT WE ARE BUILDING

The TaskFlow backend from file 02 is live on `:5000`. Now we build the **React client** that consumes it. By the end you will have:

- A scaffolded **Vite** React app wired to the backend through the dev proxy
- **React Router** with layouts, pages, and dynamic routes
- A reusable **axios API client** (instance, base URL, interceptors)
- **TanStack Query** managing all server state (queries, mutations, cache invalidation)
- **Custom hooks** wrapping the data layer so components stay clean
- Full **CRUD UI** against the live API
- Proper **loading / error / empty** states — the three everyone forgets

> React internals (hooks, rendering, reconciliation) are taught deeply in [`05-REACT`](../05-REACT/00-Index.md). Here we *integrate* React with a real API.

---

## II. SCAFFOLD THE VITE REACT APP

From the monorepo root:

```bash
# scaffold into a folder named "client" (the . keeps it in ./client we cd into)
npm create vite@latest client -- --template react
cd client
npm install
```

Install the libraries this file uses:

```bash
npm install react-router-dom axios @tanstack/react-query
npm install --save-dev @tanstack/react-query-devtools
```

Add the dev proxy from file 01 (this is what makes `/api/...` reach Express without CORS):

```js
// client/vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:5000', changeOrigin: true },
      '/socket.io': { target: 'http://localhost:5000', ws: true }, // file 05
    },
  },
});
```

```bash
# client/.env  — only VITE_-prefixed vars reach the browser bundle
VITE_API_URL=/api
```

> **Gotcha — `import.meta.env`, not `process.env`.** Vite exposes env vars on `import.meta.env`, and only those prefixed `VITE_`. Writing `process.env.VITE_API_URL` returns `undefined` in the browser. This trips up everyone coming from Create React App / Node.

---

## III. THE AXIOS API CLIENT — CONFIGURE ONCE

Every network call goes through one configured instance. This is where base URL, credentials, and (in file 04) auth refresh live — set once, used everywhere.

```js
// client/src/api/client.js
import axios from 'axios';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // '/api' → proxied to Express in dev
  withCredentials: true,                  // send/receive cookies (auth, file 04)
  timeout: 15000,                         // don't hang forever on a dead network
});

// --- RESPONSE INTERCEPTOR ---
// Normalize errors so every caller sees the SAME shape, regardless of failure mode.
api.interceptors.response.use(
  (response) => response,                 // pass success through untouched
  (error) => {
    // The backend's error envelope (file 02): { error: { message, code, details } }
    const payload = error.response?.data?.error;
    const normalized = {
      message: payload?.message || error.message || 'Network error',
      code: payload?.code || (error.response ? 'HTTP_ERROR' : 'NETWORK_ERROR'),
      status: error.response?.status ?? 0,    // 0 = no response (offline/timeout)
      details: payload?.details || null,
    };
    return Promise.reject(normalized);    // callers catch THIS clean object
  }
);
```

> **Gotcha — distinguish "no response" from "error response".** If `error.response` is undefined, the request never reached the server (offline, CORS, timeout). If it exists, the server replied with a 4xx/5xx. Your UI handles these differently — "check your connection" vs "task not found". Normalizing in one interceptor means components never repeat this logic.

A tiny per-resource module keeps URLs in one place:

```js
// client/src/api/tasks.api.js
import { api } from './client';

export const tasksApi = {
  list: (params) => api.get('/tasks', { params }).then((r) => r.data),       // {data, meta}
  get: (id) => api.get(`/tasks/${id}`).then((r) => r.data.data),
  create: (payload) => api.post('/tasks', payload).then((r) => r.data.data),
  update: (id, payload) => api.patch(`/tasks/${id}`, payload).then((r) => r.data.data),
  remove: (id) => api.delete(`/tasks/${id}`).then((r) => r.data.data),
};
```

---

## IV. WIRE UP PROVIDERS AND THE ROUTER

`main.jsx` is where global providers wrap the app: TanStack Query's client and React Router.

```jsx
// client/src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import App from './App';
import './index.css';

// One QueryClient for the whole app — it holds the server-state cache.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,                    // retry a failed query once before showing error
      staleTime: 30_000,           // data is "fresh" for 30s → no needless refetch
      refetchOnWindowFocus: false, // disable aggressive refetch for a calmer dev UX
    },
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />  {/* inspect the cache while building */}
    </QueryClientProvider>
  </React.StrictMode>
);
```

```jsx
// client/src/App.jsx — route table
import { Routes, Route, Navigate } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import TasksPage from './pages/TasksPage';
import TaskDetailPage from './pages/TaskDetailPage';
import NotFoundPage from './pages/NotFoundPage';

export default function App() {
  return (
    <Routes>
      {/* Layout route: shared chrome (nav/header) wraps all children via <Outlet/> */}
      <Route element={<RootLayout />}>
        <Route index element={<Navigate to="/tasks" replace />} />
        <Route path="tasks" element={<TasksPage />} />
        <Route path="tasks/:id" element={<TaskDetailPage />} />  {/* dynamic param */}
        <Route path="*" element={<NotFoundPage />} />            {/* catch-all 404 */}
      </Route>
    </Routes>
  );
}
```

```jsx
// client/src/layouts/RootLayout.jsx
import { Outlet, Link } from 'react-router-dom';

export default function RootLayout() {
  return (
    <div className="app">
      <header className="app__header">
        <Link to="/tasks" className="app__brand">TaskFlow</Link>
        {/* auth controls (login/logout) added in file 04 */}
      </header>
      <main className="app__main">
        <Outlet /> {/* the matched child route renders here */}
      </main>
    </div>
  );
}
```

> **Gotcha — a layout route needs `<Outlet />`.** The parent `<Route element={<RootLayout />}>` renders `RootLayout`, but its children only appear where you place `<Outlet />`. Forget it and child pages silently never render. The `index` route + `Navigate` redirects `/` to `/tasks`.

---

## V. CLIENT STATE vs SERVER STATE — THE KEY DISTINCTION

Before writing data code, internalize this. There are **two kinds of state**, and conflating them is the most common React-data mistake:

| | Client state | Server state |
|---|--------------|--------------|
| Examples | form inputs, modal open/closed, theme, selected tab | the task list, the current user, anything from the API |
| Source of truth | the browser | the server (your DB) |
| Lifetime | this session, this tab | shared, persistent, can change behind your back |
| Right tool | `useState` / `useReducer` / Context | **TanStack Query** (cache + sync) |
| Hard parts | none, really | caching, refetching, staleness, dedupe, loading/error |

TanStack Query exists *specifically* to manage server state: it caches responses, dedupes requests, tracks loading/error, and refetches when needed. Trying to do this with `useState` + `useEffect` means reinventing all of it, badly (file 05 expands on this).

> **Gotcha — don't copy server data into `useState`.** `const [tasks, setTasks] = useState([])` then `useEffect(fetch)` is the pattern to *unlearn*. It creates a second source of truth that drifts out of sync, has no caching, and forces you to hand-roll loading/error/refetch. Let Query own server state.

---

## VI. CUSTOM HOOKS WRAPPING THE DATA LAYER

We wrap TanStack Query in custom hooks per feature. Components then call `useTasks()`, not Query primitives — the data layer is swappable and components stay declarative.

```js
// client/src/features/tasks/useTasks.js
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tasksApi } from '../../api/tasks.api';

// A stable, structured cache key. Including filters means each filter combo
// is cached separately and refetched independently.
const taskKeys = {
  all: ['tasks'],
  list: (filters) => ['tasks', 'list', filters],
  detail: (id) => ['tasks', 'detail', id],
};

// --- READ: list of tasks (with filters) ---
export function useTasks(filters = {}) {
  return useQuery({
    queryKey: taskKeys.list(filters),
    queryFn: () => tasksApi.list(filters),   // returns { data, meta }
    placeholderData: (prev) => prev,         // keep old page visible while next loads
  });
}

// --- READ: one task ---
export function useTask(id) {
  return useQuery({
    queryKey: taskKeys.detail(id),
    queryFn: () => tasksApi.get(id),
    enabled: Boolean(id),                    // don't run until we have an id
  });
}

// --- CREATE ---
export function useCreateTask() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload) => tasksApi.create(payload),
    onSuccess: () => {
      // Invalidate every task list → Query refetches them with the new task.
      qc.invalidateQueries({ queryKey: taskKeys.all });
    },
  });
}

// --- UPDATE ---
export function useUpdateTask() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...payload }) => tasksApi.update(id, payload),
    onSuccess: (updated) => {
      qc.invalidateQueries({ queryKey: taskKeys.all });
      qc.setQueryData(taskKeys.detail(updated._id), updated); // update detail cache directly
    },
  });
}

// --- DELETE ---
export function useDeleteTask() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => tasksApi.remove(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: taskKeys.all }),
  });
}
```

> **Gotcha — the query key IS the cache identity.** Two `useQuery` calls with the same key share one cache entry; different keys are different entries. Forget to include filters in the key and switching filters shows stale data; include too much and you cache-miss constantly. The structured `taskKeys` object keeps keys consistent across the app.

> **Why `invalidateQueries` and not manual updates?** After a mutation, the simplest correct strategy is to mark related queries stale and let Query refetch the source of truth. It is harder to introduce drift than hand-patching arrays. We layer optimistic updates on top in file 05 for snappier UX.

---

## VII. THE THREE STATES YOU MUST NEVER FORGET

Every server-state read has (at least) **loading**, **error**, and **empty** before it has "data". Build reusable components for them so you handle all three, every time.

```jsx
// client/src/components/states.jsx
export function Spinner({ label = 'Loading…' }) {
  return <div className="state state--loading" role="status">{label}</div>;
}

export function ErrorState({ error, onRetry }) {
  return (
    <div className="state state--error" role="alert">
      <p>{error?.message || 'Something went wrong.'}</p>
      {/* network errors (status 0) suggest a connection problem */}
      {error?.status === 0 && <p>Check your internet connection.</p>}
      {onRetry && <button onClick={onRetry}>Retry</button>}
    </div>
  );
}

export function EmptyState({ title = 'Nothing here yet', children }) {
  return (
    <div className="state state--empty">
      <h3>{title}</h3>
      {children}
    </div>
  );
}
```

> **Gotcha — empty is not the same as loading.** A finished request that returns `[]` is a *success* with no data — show an inviting empty state ("No tasks yet, create one!"), not a spinner (which implies something is still coming) and not an error. Conflating these three is the most common UX bug in data-driven UIs.

---

## VIII. THE CRUD UI — TASKS PAGE

Now the payoff: a page that lists, filters, creates, updates, and deletes tasks, handling all three states, using only our custom hooks.

```jsx
// client/src/pages/TasksPage.jsx
import { useState } from 'react';
import { useTasks } from '../features/tasks/useTasks';
import TaskForm from '../features/tasks/TaskForm';
import TaskList from '../features/tasks/TaskList';
import { Spinner, ErrorState, EmptyState } from '../components/states';

export default function TasksPage() {
  const [filters, setFilters] = useState({ status: '', page: 1, limit: 10 });

  // Strip empty filter values so we don't send status="" to the API.
  const cleanFilters = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== '')
  );

  const { data, isLoading, isError, error, refetch, isFetching } = useTasks(cleanFilters);

  return (
    <section>
      <h1>My Tasks</h1>

      {/* CREATE */}
      <TaskForm />

      {/* FILTER (client state drives a server query) */}
      <div className="filters">
        <label>
          Status:
          <select
            value={filters.status}
            onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value, page: 1 }))}
          >
            <option value="">All</option>
            <option value="todo">To do</option>
            <option value="in_progress">In progress</option>
            <option value="done">Done</option>
          </select>
        </label>
        {isFetching && <span className="muted"> updating…</span>}
      </div>

      {/* THE THREE STATES + data */}
      {isLoading ? (
        <Spinner label="Loading tasks…" />
      ) : isError ? (
        <ErrorState error={error} onRetry={refetch} />
      ) : data.data.length === 0 ? (
        <EmptyState title="No tasks yet">
          <p>Create your first task above.</p>
        </EmptyState>
      ) : (
        <>
          <TaskList tasks={data.data} />
          <Pagination meta={data.meta} onPage={(page) => setFilters((f) => ({ ...f, page }))} />
        </>
      )}
    </section>
  );
}

function Pagination({ meta, onPage }) {
  if (!meta || meta.pages <= 1) return null;
  return (
    <div className="pagination">
      <button disabled={meta.page <= 1} onClick={() => onPage(meta.page - 1)}>Prev</button>
      <span>Page {meta.page} of {meta.pages}</span>
      <button disabled={meta.page >= meta.pages} onClick={() => onPage(meta.page + 1)}>Next</button>
    </div>
  );
}
```

### The create form — a controlled component

```jsx
// client/src/features/tasks/TaskForm.jsx
import { useState } from 'react';
import { useCreateTask } from './useTasks';

export default function TaskForm() {
  const [title, setTitle] = useState('');
  const [priority, setPriority] = useState('medium');
  const createTask = useCreateTask();

  const onSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;                 // client-side check (UX only)
    createTask.mutate(
      { title: title.trim(), priority },
      { onSuccess: () => setTitle('') }        // clear field after the server confirms
    );
  };

  return (
    <form onSubmit={onSubmit} className="task-form">
      <input
        value={title}                          // controlled: React owns the value
        onChange={(e) => setTitle(e.target.value)}
        placeholder="New task title…"
        disabled={createTask.isPending}        // lock the input while saving
      />
      <select value={priority} onChange={(e) => setPriority(e.target.value)}>
        <option value="low">Low</option>
        <option value="medium">Medium</option>
        <option value="high">High</option>
      </select>
      <button type="submit" disabled={createTask.isPending}>
        {createTask.isPending ? 'Adding…' : 'Add task'}
      </button>

      {/* Surface SERVER validation errors back into the form (file 02 sends details) */}
      {createTask.isError && (
        <p className="form-error">
          {createTask.error.details?.title?.[0] || createTask.error.message}
        </p>
      )}
    </form>
  );
}
```

### The list and item — update + delete

```jsx
// client/src/features/tasks/TaskList.jsx
import { Link } from 'react-router-dom';
import { useUpdateTask, useDeleteTask } from './useTasks';

export default function TaskList({ tasks }) {
  const updateTask = useUpdateTask();
  const deleteTask = useDeleteTask();

  const cycleStatus = (task) => {
    const next = { todo: 'in_progress', in_progress: 'done', done: 'todo' }[task.status];
    updateTask.mutate({ id: task._id, status: next });
  };

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task._id} className={`task task--${task.status}`}>
          <button className="task__status" onClick={() => cycleStatus(task)}>
            {task.status === 'done' ? '✅' : task.status === 'in_progress' ? '🔄' : '⬜'}
          </button>
          <Link to={`/tasks/${task._id}`} className="task__title">{task.title}</Link>
          <span className={`badge badge--${task.priority}`}>{task.priority}</span>
          <button
            className="task__delete"
            onClick={() => deleteTask.mutate(task._id)}
            disabled={deleteTask.isPending}
          >
            🗑️
          </button>
        </li>
      ))}
    </ul>
  );
}
```

> **Gotcha — controlled inputs need both `value` and `onChange`.** Set `value` without `onChange` and the field is read-only (React warns). The flow is: state → `value` → user types → `onChange` → `setState` → re-render. React owns the source of truth, which is what lets you validate, disable, and clear it programmatically.

---

## IX. THE DETAIL PAGE — DYNAMIC ROUTES + DEPENDENT QUERIES

```jsx
// client/src/pages/TaskDetailPage.jsx
import { useParams, useNavigate } from 'react-router-dom';
import { useTask, useUpdateTask, useDeleteTask } from '../features/tasks/useTasks';
import { Spinner, ErrorState } from '../components/states';

export default function TaskDetailPage() {
  const { id } = useParams();                 // from the route path "tasks/:id"
  const navigate = useNavigate();
  const { data: task, isLoading, isError, error, refetch } = useTask(id);
  const updateTask = useUpdateTask();
  const deleteTask = useDeleteTask();

  if (isLoading) return <Spinner label="Loading task…" />;
  if (isError) return <ErrorState error={error} onRetry={refetch} />;

  return (
    <article className="task-detail">
      <button onClick={() => navigate(-1)}>← Back</button>
      <h1>{task.title}</h1>
      <p>{task.description || <em>No description</em>}</p>
      <dl>
        <dt>Status</dt><dd>{task.status}</dd>
        <dt>Priority</dt><dd>{task.priority}</dd>
        <dt>Created</dt><dd>{new Date(task.createdAt).toLocaleString()}</dd>
      </dl>

      <button onClick={() => updateTask.mutate({ id, status: 'done' })}>
        Mark done
      </button>
      <button
        onClick={async () => {
          await deleteTask.mutateAsync(id);    // mutateAsync → await, then navigate
          navigate('/tasks');
        }}
      >
        Delete
      </button>
    </article>
  );
}
```

> **Gotcha — `mutate` vs `mutateAsync`.** `mutate` is fire-and-forget (use callbacks). `mutateAsync` returns a promise you can `await` — needed here because we want to navigate away *after* the delete succeeds. Using `mutate` then navigating immediately would redirect before the request resolves.

---

## X. HOW IT ALL CONNECTS — ONE TRACE

Click "Add task" and follow the data, tying files 01–03 together:

```text
TaskForm submit
   └─ createTask.mutate({title, priority})        ← useCreateTask (custom hook)
        └─ tasksApi.create(payload)               ← per-resource API module
             └─ api.post('/tasks', payload)        ← axios instance (baseURL '/api', cookies)
                  └─ Vite proxy → http://localhost:5000/api/tasks   (file 01)
                       └─ Express route → controller → service → Mongoose → MongoDB  (file 02)
                  ◀── 201 { data: task }
        ◀── interceptor passes success through
   └─ onSuccess → queryClient.invalidateQueries(['tasks'])
        └─ useTasks refetches → TasksPage re-renders with the new task
```

That single trace contains the entire stack. When something breaks, walk it in order — the failure is always at one of these hops, and the **Network tab** tells you which.

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `process.env` in client | `undefined` config | Use `import.meta.env.VITE_*` |
| Server data in `useState`+`useEffect` | Stale data, no caching, manual loading | Use TanStack Query |
| Forgetting empty state | Spinner forever or blank screen on `[]` | Handle loading/error/**empty** distinctly |
| Query key missing filters | Stale data when filters change | Include all inputs in the query key |
| Not invalidating after mutation | UI shows old list after create/delete | `invalidateQueries` in `onSuccess` |
| Missing `<Outlet/>` in layout | Child routes don't render | Add `<Outlet/>` in the layout component |
| Controlled input without `onChange` | Read-only field, React warning | Provide both `value` and `onChange` |
| `mutate` then navigate | Navigates before request finishes | `await mutateAsync(...)` |
| Sending empty filter values | `?status=` confuses the API | Strip empty values before the request |
| Not disabling buttons during mutation | Double-submits | Disable with `isPending` |

---

## 🧠 KEY TAKEAWAYS

- Scaffold with **Vite**; read config via **`import.meta.env.VITE_*`**, and let the **dev proxy** forward `/api` to Express so there is no CORS in development.
- Configure **one axios instance** (base URL, `withCredentials`, interceptors) and normalize errors in a single response interceptor so components never repeat error logic.
- Separate **client state** (`useState`/Context) from **server state** (**TanStack Query**). Never copy server data into `useState` + `useEffect`.
- Wrap Query in **custom hooks** (`useTasks`, `useCreateTask`, …) with **structured query keys**; mutations **invalidate** related queries so the cache re-syncs with the source of truth.
- Always render the **three states** — loading, error, empty — as distinct, reusable components. Empty ≠ loading ≠ error.
- Use **controlled components** for forms, disable inputs/buttons during mutations, and surface **server validation errors** back into the form.
- Trace a feature end-to-end (hook → API module → axios → proxy → Express → Mongo → invalidate → re-render); the **Network tab** pinpoints which hop failed.

---

**Prev:** [`02-Building-The-Backend-API.md`](./02-Building-The-Backend-API.md) · **Next:** [`04-Authentication-Across-The-Stack.md`](./04-Authentication-Across-The-Stack.md) · **Index:** [`00-Index.md`](./00-Index.md)
