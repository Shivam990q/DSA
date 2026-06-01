# ▲ 03 — Server & Client Components

> *"The question is no longer 'what does this component render?' but 'where does this component run?' Master that one question and the entire App Router clicks into place."*

**Prev:** [`02-App-Router-And-Routing.md`](./02-App-Router-And-Routing.md) · **Next:** [`04-Rendering-Strategies-SSR-SSG-ISR.md`](./04-Rendering-Strategies-SSR-SSG-ISR.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE BIG SHIFT — REACT SERVER COMPONENTS

For a decade, React ran in the **browser**. Every component, every line of your app, was downloaded as JavaScript and executed on the user's device. **React Server Components (RSC)** change that. Now a component can run on the **server**, render to HTML, and send the *result* to the browser — often with **zero JavaScript shipped** for that component.

In the App Router, **every component is a Server Component by default.** You opt *into* the browser with `"use client"`, not the other way around. This is the inverse of the old mental model, and it is the single most important thing to internalize in this section.

```
                ┌──────────────── SERVER ────────────────┐
                │  Server Components run here.            │
                │  • Can be async                         │
                │  • Can read the database / filesystem   │
                │  • Can use secrets                      │
                │  • Render to HTML/RSC payload           │
                │  • Ship ZERO JS to the browser          │
                └────────────────┬───────────────────────┘
                                 │  HTML + serialized props
                                 ▼
                ┌──────────────── BROWSER ───────────────┐
                │  Client Components run here.            │
                │  • Interactivity (onClick, onChange)    │
                │  • State & effects (useState, etc.)     │
                │  • Browser APIs (window, localStorage)  │
                │  • Cost JS that must be downloaded      │
                └─────────────────────────────────────────┘
```

> **Mental model.** Server Components are like a backend template renderer (think PHP or a templating engine) but written in React. Client Components are the classic interactive React you already know. An app is a *tree* mixing both.

---

## II. SERVER COMPONENTS — THE DEFAULT

A Server Component runs only on the server. It never appears in the browser's JavaScript bundle. Because it runs on the server, it can do things browser code simply cannot:

```tsx
// app/users/page.tsx
// No "use client" → this is a SERVER COMPONENT (the default).
// Notice it's `async` — Server Components can be async functions.
import { db } from "@/lib/db";              // a real DB client, server-side only

export default async function UsersPage() {
  // Talk to the database DIRECTLY. No API route, no fetch to your own backend.
  const users = await db.user.findMany();

  // This secret never reaches the browser — it's used on the server only.
  const apiKey = process.env.SECRET_API_KEY;

  return (
    <ul>
      {users.map((u) => (
        <li key={u.id}>{u.name}</li>
      ))}
    </ul>
  );
}
```

What just happened that React-in-the-browser could never do:

- The component is **`async`** and `await`s data *before* rendering — no loading spinner, no `useEffect`.
- It queries the **database directly**. There is no separate API call from the client.
- It read a **secret** (`SECRET_API_KEY`) safely, because this code runs on the server and is never sent to the user.
- It shipped **no JavaScript** to the browser for this component — only the resulting HTML.

**Use Server Components for:** fetching data, accessing backend resources (DB, filesystem), keeping secrets/large dependencies off the client, and rendering mostly-static content. This is the *majority* of most apps.

---

## III. CLIENT COMPONENTS — `"use client"`

When you need **interactivity, state, effects, or browser APIs**, you opt into the client by putting the `"use client"` directive at the very top of the file.

```tsx
"use client"; // ← MUST be the first line, before imports

import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);     // state requires a Client Component

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

`"use client"` marks the **boundary** where your app transitions from server to client. Everything in this file — and every component it imports — becomes part of the client bundle.

**You need a Client Component when you use any of:**

| Capability | Examples |
|------------|----------|
| State | `useState`, `useReducer` |
| Lifecycle / effects | `useEffect`, `useLayoutEffect` |
| Event handlers | `onClick`, `onChange`, `onSubmit` |
| Browser-only APIs | `window`, `document`, `localStorage`, `navigator` |
| Context consumers/providers | `useContext`, most `<Provider>`s |
| Most third-party hooks | animation libs, form libs, etc. |
| Class components | always client |

> **Gotcha — `"use client"` is "infectious" downward, not upward.** Marking a file `"use client"` makes it *and all its imported child components* client components. But it does **not** turn its *parents* into client components — a Server Component can render a Client Component child. The directive defines where the boundary *starts*, descending into the tree.

---

## IV. SERVER vs CLIENT — THE DECISION TABLE

| You need to… | Component type |
|--------------|----------------|
| Fetch data before rendering | **Server** |
| Query a database or read files | **Server** |
| Use API keys / secrets | **Server** |
| Reduce client JavaScript | **Server** |
| Render large dependencies (e.g. a markdown parser) | **Server** |
| Handle `onClick` / `onChange` | **Client** |
| Use `useState` / `useEffect` | **Client** |
| Use `window`, `localStorage`, geolocation | **Client** |
| Use a Context provider | **Client** |
| Add animations / transitions | **Client** |

**The strategy senior engineers use: keep components on the server by default, and push `"use client"` as far down the tree (as close to the leaf) as possible.** A page is a Server Component that fetches data; only the small interactive bits (a like button, a dropdown) are Client Components.

---

## V. THE COMPOSITION RULES

This is where most confusion lives. The rules are simple once stated plainly.

### ✅ Rule 1 — Server Components can render Client Components

This is normal and expected. A server page renders an interactive client widget:

```tsx
// app/page.tsx — Server Component (default)
import Counter from "./counter";            // a "use client" component

export default async function Page() {
  const data = await getData();             // server-side data fetch
  return (
    <main>
      <h1>{data.title}</h1>
      <Counter />                            {/* Client Component island */}
    </main>
  );
}
```

### ❌ Rule 2 — Client Components CANNOT import Server Components

A Client Component cannot directly import and render a Server Component, because once you cross into the client, that code must run in the browser — and a Server Component (async, DB access) cannot.

```tsx
"use client";
import ServerThing from "./server-thing"; // ❌ this won't work as intended
```

### ✅ Rule 3 — ...but you CAN pass a Server Component as `children` (the slot pattern)

The escape hatch: a Client Component can *receive* server-rendered content as a prop (commonly `children`). The server renders it; the client just slots it in. The client never "imports" or runs server code — it just places already-rendered output.

```tsx
// app/components/Tabs.tsx — Client Component (needs state for the active tab)
"use client";
import { useState } from "react";

export default function Tabs({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(true);
  return (
    <div>
      <button onClick={() => setOpen(!open)}>Toggle</button>
      {open && children}                     {/* server-rendered content slots in here */}
    </div>
  );
}
```

```tsx
// app/page.tsx — Server Component composes them
import Tabs from "./components/Tabs";
import ServerContent from "./components/ServerContent"; // a Server Component

export default function Page() {
  return (
    <Tabs>
      <ServerContent />     {/* rendered on the server, passed as children to the client Tabs */}
    </Tabs>
  );
}
```

```
The pattern that unlocks everything:

   <ClientComponent>          ← runs in browser, owns interactivity/state
       <ServerComponent />    ← rendered on server, passed in as children
   </ClientComponent>
```

> **Gotcha — "Client Component can't import Server Component" trips up everyone.** The fix is almost always the children/slot pattern: lift the Server Component up to a server parent and pass it *into* the client component as a prop. Don't try to import down across the boundary.

---

## VI. THE SERIALIZATION BOUNDARY

When a Server Component passes **props** to a Client Component, those props must cross the network (server → browser). Therefore they must be **serializable** — convertible to a wire format. You cannot pass functions, class instances, Dates-with-methods-you-rely-on, or other non-serializable values across the boundary.

```tsx
// app/page.tsx — Server Component
import ClientWidget from "./client-widget";

export default async function Page() {
  const user = await getUser();

  return (
    <ClientWidget
      name={user.name}             // ✅ string — serializable
      age={42}                     // ✅ number
      tags={["a", "b"]}            // ✅ array/object of primitives
      onSave={() => save()}        // ❌ FUNCTION — cannot serialize → error
    />
  );
}
```

| Serializable (✅ can cross) | Not serializable (❌ cannot cross) |
|----------------------------|-----------------------------------|
| string, number, boolean, null | functions / callbacks |
| plain objects & arrays of the above | class instances |
| `Date` (handled by RSC) | Symbols, Map/Set (in general) |
| Promises (RSC streams them) | JSX with event handlers attached server-side |

> **Gotcha — you cannot pass an event handler from server to client.** `onClick`, `onChange`, etc. are functions. They must be *defined inside a Client Component*. If a client child needs a callback, define it within the client tree (or use a Server Action — file 05 — which is the sanctioned way to "pass a server function" to the client).

---

## VII. KEEPING SERVER CODE OFF THE CLIENT — `server-only`

A subtle danger: a module that uses secrets or server resources might *accidentally* get imported into a Client Component, leaking it into the browser bundle. The `server-only` package turns that mistake into a **build-time error**.

```ts
// lib/secrets.ts
import "server-only";                       // ← throws at build if imported by client code

export async function getSecretData() {
  const key = process.env.PRIVATE_KEY;      // never want this in the browser
  return fetch("https://internal.api/data", {
    headers: { Authorization: `Bearer ${key}` },
  }).then((r) => r.json());
}
```

Now if any `"use client"` file imports `getSecretData`, the build fails loudly instead of silently shipping your secret. There is a matching `client-only` package for the reverse case (code that must never run on the server).

> **Gotcha — environment variables and the browser.** Only env vars prefixed with `NEXT_PUBLIC_` are exposed to the client. A plain `process.env.SECRET_API_KEY` is `undefined` in the browser. This is a safety feature — but it means if you reference a non-public var in a Client Component, it will be `undefined`, not an error. More in file 07.

---

## VIII. A REALISTIC MIXED TREE

Here is how a real product page composes server and client. The page fetches data on the server; only the interactive leaves are clients.

```tsx
// app/products/[id]/page.tsx — SERVER Component
import { db } from "@/lib/db";
import AddToCartButton from "./add-to-cart-button"; // client
import ReviewForm from "./review-form";             // client
import Reviews from "./reviews";                     // SERVER (fetches its own data)

export default async function ProductPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const product = await db.product.findUnique({ where: { id } }); // direct DB, server-side

  return (
    <main>
      {/* Static, server-rendered content — zero JS */}
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <strong>${product.price}</strong>

      {/* Interactive island — ships JS, runs in browser */}
      <AddToCartButton productId={product.id} />

      {/* Another Server Component — renders its own server data */}
      <Reviews productId={product.id} />

      {/* Interactive form island */}
      <ReviewForm productId={product.id} />
    </main>
  );
}
```

```tsx
// app/products/[id]/add-to-cart-button.tsx — CLIENT Component
"use client";
import { useState } from "react";

export default function AddToCartButton({ productId }: { productId: string }) {
  const [added, setAdded] = useState(false);
  return (
    <button onClick={() => setAdded(true)}>
      {added ? "✓ Added" : "Add to cart"}
    </button>
  );
}
```

The result: the page is fast (mostly server HTML, minimal JS), data is fetched without client waterfalls, and the bits that *need* the browser are small, isolated islands.

```
ProductPage (server)
├── <h1>, <p>, price        ← server HTML, 0 JS
├── AddToCartButton         ← client island (small JS)
├── Reviews (server)        ← server HTML, fetches its own data
└── ReviewForm              ← client island (small JS)
```

---

## IX. HYDRATION — HOW THE TWO MEET

The server sends HTML so the page is visible immediately. Then React **hydrates** the Client Components — it downloads their JS and attaches event listeners to the already-present HTML, making them interactive. Server Components are *not* hydrated (they have no client JS), which is exactly why they are cheap.

```
1. Server renders page → sends HTML (visible instantly, even before JS)
2. Browser downloads JS for Client Components only
3. React "hydrates" those islands → buttons/inputs become interactive
4. Server Components: never hydrated, no JS, just HTML
```

> **Gotcha — hydration mismatches.** If a Client Component renders different output on the server vs the first client render (e.g. using `Date.now()`, `Math.random()`, or `window` during render), React throws a *hydration mismatch* warning. Fix by moving such values into a `useEffect` (which runs only on the client) or gating with a "mounted" state.

---

## X. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using `useState`/`onClick` without `"use client"` | Build error about hooks/handlers | Add `"use client"` at top of file |
| Importing a Server Component *into* a Client Component | Error / it behaves like client | Use the children/slot pattern instead |
| Passing a function as a prop server→client | "Functions cannot be passed..." error | Define handlers in the client; or use a Server Action |
| Putting `"use client"` not on line 1 | Directive ignored | It must be the first statement, before imports |
| Reading a secret env var in a client file | Value is `undefined` | Use it server-side; only `NEXT_PUBLIC_*` reach the browser |
| Marking everything `"use client"` | Large bundles, lost server benefits | Keep server default; push client to the leaves |
| `window`/`localStorage` during render | Hydration mismatch / "window is not defined" | Access them inside `useEffect` (client only) |
| Expecting `async` in a Client Component | Client components can't be async functions | Fetch on the server, or use `useEffect`/a data hook |

---

## 🧠 KEY TAKEAWAYS

- In the App Router, **components are Server Components by default**; you opt into the browser with **`"use client"`**.
- **Server Components** can be `async`, query the database directly, use secrets, and ship **zero JS** — use them for data and static content (the majority of your app).
- **Client Components** are for **interactivity**: state, effects, event handlers, and browser APIs.
- **Composition rules:** Server can render Client ✅; Client cannot import Server ❌; but Client can *receive* server content via **`children`** (the slot pattern) ✅.
- Props crossing the server→client boundary must be **serializable** — no functions, no class instances.
- Guard server-only modules with **`import "server-only"`** so secrets can never leak into the client bundle.
- The winning strategy: **default to the server, push `"use client"` to the leaves.** Small interactive islands on a fast server-rendered page.

---

**Prev:** [`02-App-Router-And-Routing.md`](./02-App-Router-And-Routing.md) · **Next:** [`04-Rendering-Strategies-SSR-SSG-ISR.md`](./04-Rendering-Strategies-SSR-SSG-ISR.md) · **Index:** [`00-Index.md`](./00-Index.md)
