# ⚛️ 10 — Routing With React Router

> *"A single-page app has one HTML document but many 'pages.' Routing is the illusion engine: it maps the URL to a component tree, updates the address bar without a reload, and makes the back button work. Get routing right and your SPA feels like the web it's pretending to be."*

**Prev:** [`09-React-Patterns-And-Best-Practices.md`](./09-React-Patterns-And-Best-Practices.md) · **Next:** [`11-Testing-And-TypeScript-React.md`](./11-Testing-And-TypeScript-React.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHY ROUTING NEEDS A LIBRARY

React renders one component tree into one `<div id="root">`. There are no "pages." Yet users expect distinct URLs (`/`, `/about`, `/users/42`), a working back button, bookmarkable links, and no full-page reload when navigating. A **router** provides all of that by:

1. Reading the current URL.
2. Rendering the component(s) that match it.
3. Intercepting link clicks to update the URL via the **History API** (`pushState`) instead of reloading.
4. Re-rendering when the URL changes (including back/forward).

**React Router** is the de-facto routing library. This file targets **v6/v7** (the modern API). v7 is largely v6 plus framework features; the routing API below is shared.

```bash
npm install react-router-dom
```

> **Gotcha — React Router v5 → v6 was a big breaking change.** v5 used `<Switch>`, `component={X}`, and `exact`. v6 uses `<Routes>`, `element={<X/>}`, and matches exactly by default. Old tutorials using `<Switch>`/`component=` are v5 — the API below is different. Always check the version.

---

## II. SETUP — THE ROUTER, ROUTES, AND LINKS

Wrap your app in a router, declare routes, and navigate with `<Link>` (never plain `<a>` for internal links — `<a>` triggers a full reload).

```jsx
// main.jsx — wrap the app once at the root.
import { BrowserRouter } from 'react-router-dom';

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
```

```jsx
// App.jsx — declare the URL → component mapping.
import { Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link>{' '}
        <Link to="/about">About</Link>{' '}
        <Link to="/users">Users</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/users" element={<Users />} />
        <Route path="*" element={<NotFound />} />   {/* catch-all 404 */}
      </Routes>
    </>
  );
}
```

> **Gotcha — `<Link to>`, not `<a href>`, for internal navigation.** A raw `<a href="/about">` reloads the whole page, throwing away your app state and re-downloading everything. `<Link>` updates the URL client-side. Use `<a>` only for external links.

> **`BrowserRouter` vs `HashRouter`.** `BrowserRouter` uses clean URLs (`/about`) but needs the server to serve `index.html` for all routes (a "SPA fallback"). `HashRouter` uses `/#/about` and works on any static host without server config, at the cost of ugly URLs. Prefer `BrowserRouter` and configure your host's fallback.

### `NavLink` — links that know when they're active

```jsx
import { NavLink } from 'react-router-dom';

// NavLink gives you active state for styling the current nav item.
<NavLink
  to="/users"
  className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
>
  Users
</NavLink>
```

---

## III. ROUTE PARAMETERS — DYNAMIC SEGMENTS

A `:param` in a path captures a dynamic segment. Read it with `useParams`.

```jsx
<Routes>
  <Route path="/users/:userId" element={<UserDetail />} />
  <Route path="/posts/:postId/comments/:commentId" element={<Comment />} />
</Routes>
```

```jsx
import { useParams } from 'react-router-dom';

function UserDetail() {
  const { userId } = useParams();   // string from the URL, e.g. "42"
  // Use it to fetch (file 07) or look up data.
  const { data, isPending } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });
  if (isPending) return <p>Loading…</p>;
  return <h1>{data.name}</h1>;
}
```

> **Gotcha — params are always strings.** `userId` from `/users/42` is `"42"`, not `42`. Convert with `Number(userId)` if you need a number for math or strict comparisons.

### Query strings with `useSearchParams`

For optional/filter data (`/search?q=react&page=2`), use the query string, not path params. `useSearchParams` works like `useState` for the URL's query.

```jsx
import { useSearchParams } from 'react-router-dom';

function Search() {
  const [searchParams, setSearchParams] = useSearchParams();
  const q = searchParams.get('q') ?? '';
  const page = Number(searchParams.get('page') ?? '1');

  return (
    <>
      <input
        value={q}
        onChange={(e) => setSearchParams({ q: e.target.value, page: '1' })}
      />
      <p>Searching "{q}", page {page}</p>
      <button onClick={() => setSearchParams({ q, page: String(page + 1) })}>Next</button>
    </>
  );
}
```

> **Path param vs query param — which?** Use a **path param** for an item's identity (`/users/42` — required, part of the resource). Use a **query param** for optional view state (filters, sort, page, search) that doesn't change *which* resource you're on. The URL is shareable state — put filters there so a link reproduces the view.

---

## IV. NESTED ROUTES & `<Outlet>` — SHARED LAYOUTS

Real apps share layout: a dashboard with a persistent sidebar where only the main panel changes. **Nested routes** render a parent layout once and swap children inside an **`<Outlet>`**.

```jsx
function App() {
  return (
    <Routes>
      <Route path="/dashboard" element={<DashboardLayout />}>   {/* parent layout */}
        <Route index element={<Overview />} />                  {/* /dashboard */}
        <Route path="stats" element={<Stats />} />              {/* /dashboard/stats */}
        <Route path="settings" element={<Settings />} />        {/* /dashboard/settings */}
      </Route>
    </Routes>
  );
}

import { Outlet, NavLink } from 'react-router-dom';

function DashboardLayout() {
  return (
    <div className="dashboard">
      <aside>
        <NavLink to="/dashboard">Overview</NavLink>
        <NavLink to="/dashboard/stats">Stats</NavLink>
        <NavLink to="/dashboard/settings">Settings</NavLink>
      </aside>
      <main>
        <Outlet />   {/* the matched child route renders HERE */}
      </main>
    </div>
  );
}
```

The sidebar renders once and stays mounted; navigating between `stats` and `settings` only swaps what's in `<Outlet>`. Note:
- **`index` route** — the default child shown at the parent's exact path (`/dashboard`).
- **Relative paths** — child `path="stats"` (no leading `/`) resolves to `/dashboard/stats`.

> **Gotcha — forgetting `<Outlet>`.** If a parent layout route has children but no `<Outlet>`, the children match but render *nothing* (there's nowhere to put them). The layout shows, the child silently doesn't. Always render `<Outlet>` where children should appear.

---

## V. PROGRAMMATIC NAVIGATION — `useNavigate`

Navigate from code (after a form submit, a login, a timeout) with `useNavigate`.

```jsx
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    await login(/* ... */);
    navigate('/dashboard');             // go to a new route
    // navigate('/dashboard', { replace: true });  // replace history (no "back" to login)
    // navigate(-1);                                // go back one entry (like the back button)
    // navigate('/users', { state: { from: 'login' } });  // pass state without a query param
  }

  return <form onSubmit={handleSubmit}>{/* ... */}</form>;
}
```

> **Gotcha — prefer `<Link>` over `navigate()` for user-initiated navigation.** Links are accessible (focusable, right-clickable, openable in a new tab) and need no JS to work. Use `useNavigate` only for navigation that follows an *action* (submit, login, redirect) where there's no clickable link.

```jsx
// Read state passed via navigate(..., { state }) or location with useLocation.
import { useLocation } from 'react-router-dom';
function Page() {
  const location = useLocation();        // { pathname, search, state, hash }
  const from = location.state?.from;
  return <p>Came from: {from}</p>;
}
```

---

## VI. PROTECTED ROUTES — GUARDING AUTHENTICATED PAGES

Restrict routes to logged-in users by wrapping them in a guard that redirects unauthenticated visitors to `/login` (remembering where they wanted to go).

```jsx
import { Navigate, useLocation, Outlet } from 'react-router-dom';

// A guard component. Renders the protected content or redirects.
function RequireAuth() {
  const { user } = useAuth();           // your auth context/hook (file 05)
  const location = useLocation();

  if (!user) {
    // Redirect to login, remembering the attempted URL so we can return after login.
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return <Outlet />;                     // authenticated → render the nested routes
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<Home />} />

      {/* Everything nested under RequireAuth is protected. */}
      <Route element={<RequireAuth />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
    </Routes>
  );
}
```

```jsx
// After a successful login, send the user back where they came from.
function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  async function handleLogin() {
    await login();
    navigate(from, { replace: true });   // return to the originally requested page
  }
  return <button onClick={handleLogin}>Log in</button>;
}
```

> **Gotcha — client-side route guards are UX, not security.** Anyone can read your JS and call your API directly. A route guard only hides UI; the **server must enforce authorization** on every protected request. Never trust the client. (See [`../11-FULLSTACK-ENGINEERING/`](../11-FULLSTACK-ENGINEERING/) for real auth.)

---

## VII. THE DATA ROUTER — LOADERS & ACTIONS (v6.4+)

React Router 6.4 introduced a **data router** (`createBrowserRouter`) with **loaders** (fetch data *before* a route renders) and **actions** (handle form submissions). This eliminates loading flashes and the fetch-in-effect waterfall (file 07) by loading data as part of routing.

```jsx
import {
  createBrowserRouter, RouterProvider, useLoaderData, Form, redirect,
} from 'react-router-dom';

const router = createBrowserRouter([
  {
    path: '/users/:id',
    element: <UserPage />,
    // loader runs BEFORE the route renders; its return is available via useLoaderData.
    loader: async ({ params }) => {
      const res = await fetch(`/api/users/${params.id}`);
      if (!res.ok) throw new Response('Not Found', { status: 404 });
      return res.json();
    },
    // action handles non-GET form submissions to this route.
    action: async ({ request, params }) => {
      const formData = await request.formData();
      await updateUser(params.id, Object.fromEntries(formData));
      return redirect(`/users/${params.id}`);   // navigate after the mutation
    },
    errorElement: <RouteError />,                // catches loader/action throws
  },
]);

function Root() {
  return <RouterProvider router={router} />;     // replaces <BrowserRouter>
}

function UserPage() {
  const user = useLoaderData();                  // data is already here — no loading state!
  return (
    <Form method="post">                          {/* submits to the route's action */}
      <input name="name" defaultValue={user.name} />
      <button type="submit">Save</button>
    </Form>
  );
}
```

> **Why loaders matter.** With effect-based fetching, the component mounts, *then* fetches, so you flash a spinner and risk waterfalls. A **loader** fetches in parallel with routing, before render — the component receives ready data via `useLoaderData`. Combined with `errorElement`, you get declarative loading and error handling at the route level. This model heavily influenced Next.js and Remix.

> **Two APIs, one library.** The classic `<BrowserRouter>` + `<Routes>` (Sections II–VI) and the data router `createBrowserRouter` + `RouterProvider` (this section) coexist. Loaders/actions/`useLoaderData` require the **data router**. Many apps still use the classic API with TanStack Query for data — that's a perfectly good choice too.

---

## VIII. LAZY ROUTES — CODE SPLITTING PER PAGE

Combine routing with code splitting (file 08) so each route's code downloads only when visited — the highest-impact bundle optimization.

```jsx
// Classic API: lazy + Suspense around the routes.
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports   = lazy(() => import('./pages/Reports'));

function App() {
  return (
    <Suspense fallback={<PageSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Suspense>
  );
}
```

```jsx
// Data router: each route can lazily load its component AND loader together.
const router = createBrowserRouter([
  {
    path: '/reports',
    lazy: async () => {
      const { Reports, reportsLoader } = await import('./pages/Reports');
      return { element: <Reports />, loader: reportsLoader };
    },
  },
]);
```

> **Route-based splitting is the default win.** Users land on one page; there's no reason to ship the code for all the others up front. Split at route boundaries first, then split heavy components within a route if needed.

---

## IX. SCROLL RESTORATION & A FEW EXTRAS

```jsx
// SPAs don't reset scroll on navigation by default. Data router has <ScrollRestoration/>;
// for the classic API, a small effect does it:
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => { window.scrollTo(0, 0); }, [pathname]);  // reset on route change
  return null;
}
// Render <ScrollToTop /> once inside the router.
```

| Hook / Component | Purpose |
|------------------|---------|
| `<Link>` / `<NavLink>` | Client-side navigation (NavLink adds active state) |
| `useParams` | Read `:param` path segments |
| `useSearchParams` | Read/write the query string (like `useState` for the URL) |
| `useNavigate` | Navigate from code |
| `useLocation` | Current location object (pathname, state, hash) |
| `<Outlet>` | Where nested child routes render |
| `<Navigate>` | Declarative redirect (render → navigate) |
| `useLoaderData` / loaders | Data fetched before render (data router) |
| `Form` / actions | Declarative mutations (data router) |

---

## X. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `<a href>` for internal links | Full page reload, state lost | Use `<Link to>` |
| Following a v5 tutorial | `<Switch>`/`component=` don't work | Use v6 `<Routes>`/`element=` |
| Forgetting `<Outlet>` in a layout | Child routes render nothing | Add `<Outlet>` where children go |
| Treating params as numbers | Comparison/math bugs | `Number(useParams().id)` |
| Filters in path instead of query | Rigid, un-shareable URLs | Use `useSearchParams` |
| No catch-all route | Blank screen on bad URL | Add `<Route path="*">` |
| Trusting route guards for security | Data exposed via API | Enforce authz on the server |
| `BrowserRouter` without SPA fallback | 404 on refresh of a deep link | Configure host to serve `index.html` |
| Not splitting routes | Huge initial bundle | `lazy` + `Suspense` per route |
| `navigate()` for everything | Inaccessible "links" | Prefer `<Link>`; `navigate` for actions |

---

## 🧠 KEY TAKEAWAYS

- A router maps the **URL → component tree** and updates the address bar via the History API without a reload; **React Router** is the standard (use **v6/v7**, not v5).
- Wrap the app in `<BrowserRouter>`, declare `<Routes>`/`<Route element={…}>`, and navigate with **`<Link>`/`<NavLink>`** — never `<a>` for internal links.
- Read dynamic segments with **`useParams`** (always **strings**); put optional/filter state in the query string via **`useSearchParams`** so URLs are shareable.
- **Nested routes** share a layout; the matched child renders in **`<Outlet>`** (with `index` for the default child).
- Navigate from code with **`useNavigate`** (after actions); prefer real links for user navigation.
- **Protected routes** wrap children in a guard that redirects with `<Navigate>` — but guards are **UX only; the server enforces real authorization**.
- The **data router** (`createBrowserRouter`) adds **loaders** (data before render, no flash/waterfall) and **actions** (declarative mutations) with `errorElement`.
- **Split code per route** with `lazy` + `Suspense` for the biggest bundle win; remember scroll restoration on navigation.

---

**Prev:** [`09-React-Patterns-And-Best-Practices.md`](./09-React-Patterns-And-Best-Practices.md) · **Next:** [`11-Testing-And-TypeScript-React.md`](./11-Testing-And-TypeScript-React.md) · **Index:** [`00-Index.md`](./00-Index.md)
