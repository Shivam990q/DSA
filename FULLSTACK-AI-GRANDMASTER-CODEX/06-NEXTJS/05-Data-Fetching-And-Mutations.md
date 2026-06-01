# ▲ 05 — Data Fetching & Mutations

> *"Reads happen where the data lives — on the server. Writes happen through a function you can call from a form. Server Actions collapse the frontend/backend divide into a single import."*

**Prev:** [`04-Rendering-Strategies-SSR-SSG-ISR.md`](./04-Rendering-Strategies-SSR-SSG-ISR.md) · **Next:** [`06-API-Routes-And-Route-Handlers.md`](./06-API-Routes-And-Route-Handlers.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE NEW DATA MODEL — FETCH ON THE SERVER

In a classic React SPA, data fetching is a client-side ritual: render an empty component, fire `useEffect`, set loading state, `fetch`, set data state, re-render. Every screen ships that boilerplate and creates a **request waterfall** (component renders → *then* asks for data).

Server Components delete all of it. A Server Component is `async`; it `await`s its data **before** rendering and sends finished HTML:

```tsx
// app/posts/page.tsx — Server Component. Fetch happens on the server, before render.
export default async function Posts() {
  const posts = await fetch("https://api.example.com/posts").then((r) => r.json());

  return (
    <ul>
      {posts.map((p: { id: string; title: string }) => (
        <li key={p.id}>{p.title}</li>
      ))}
    </ul>
  );
}
```

```
Classic SPA (client):  render → useEffect → fetch → setState → re-render   (waterfall, spinner)
Server Component:      fetch (server) → render finished HTML                (no spinner, no waterfall)
```

No `useState`, no `useEffect`, no loading flag. The data is there when the component renders. This is the default and the right tool for the overwhelming majority of reads.

> **Gotcha — you can still fetch on the client when you must.** Polling, infinite scroll, or data that depends on client interaction can still use `useEffect` or a library like **TanStack Query** / **SWR** inside a `"use client"` component. But reach for server fetching first — it's faster, simpler, and SEO-friendly.

---

## II. THE EXTENDED `fetch` — CACHING & REVALIDATION

Next.js extends the native `fetch` with caching controls (this ties directly to the Data Cache from file 04). The relevant options:

```tsx
// Cache forever (default in Next 14; opt-in in Next 15):
await fetch(url, { cache: "force-cache" });

// Never cache — fetch fresh every request (forces dynamic rendering):
await fetch(url, { cache: "no-store" });

// Time-based revalidation (ISR) — cache, but treat as stale after 60s:
await fetch(url, { next: { revalidate: 60 } });

// Tag-based — label this data so you can invalidate it on demand later:
await fetch(url, { next: { tags: ["posts"] } });
```

| Option | Behavior | Rendering effect |
|--------|----------|------------------|
| `cache: "force-cache"` | Reuse cached result indefinitely | Stays static |
| `cache: "no-store"` | Always fetch fresh | Forces dynamic |
| `next: { revalidate: N }` | Cache, refresh after N seconds | ISR (static + refresh) |
| `next: { tags: [...] }` | Cache + attach tags for `revalidateTag` | Static until invalidated |

> **Gotcha — version-dependent default (again).** Next 14 caches `fetch` by default; Next 15 does not. Always pass the option you mean. Tagging (`next.tags`) is the most powerful pattern: it lets a mutation later say "anything tagged `posts` is now stale" without knowing every URL.

---

## III. FETCHING FROM A DATABASE DIRECTLY

You are not limited to HTTP `fetch`. Because Server Components run on the server, you can call your ORM or DB client directly — no API layer in between.

```tsx
// lib/db.ts — a Prisma client singleton (avoids exhausting connections in dev)
import { PrismaClient } from "@prisma/client";
const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };
export const prisma = globalForPrisma.prisma ?? new PrismaClient();
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

```tsx
// app/users/page.tsx — query the DB straight from the component.
import { prisma } from "@/lib/db";

export default async function Users() {
  const users = await prisma.user.findMany({ orderBy: { createdAt: "desc" } });
  return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

Direct DB access isn't tracked by the `fetch` Data Cache. To cache the *result* of a non-`fetch` data function across requests, wrap it with `unstable_cache`:

```tsx
import { unstable_cache } from "next/cache";
import { prisma } from "@/lib/db";

export const getUsers = unstable_cache(
  async () => prisma.user.findMany(),
  ["all-users"],                       // cache key parts
  { revalidate: 60, tags: ["users"] }, // same revalidate/tags semantics as fetch
);
```

To dedupe a DB call *within a single render* (Request Memoization for non-fetch functions), wrap it in React's `cache`:

```tsx
import { cache } from "react";
import { prisma } from "@/lib/db";

// Called in layout AND page in the same render → runs the query once.
export const getUser = cache(async (id: string) =>
  prisma.user.findUnique({ where: { id } }),
);
```

---

## IV. AVOIDING WATERFALLS — PARALLEL FETCHING

Sequential `await`s create a waterfall: each waits for the previous even when they're independent. Fire independent requests **in parallel** with `Promise.all`.

```tsx
// ❌ SEQUENTIAL — total time = user + posts + comments
export default async function Slow({ id }: { id: string }) {
  const user = await getUser(id);          // wait...
  const posts = await getPosts(id);        // ...then wait...
  const comments = await getComments(id);  // ...then wait
  return <Profile user={user} posts={posts} comments={comments} />;
}

// ✅ PARALLEL — total time = the SLOWEST single request
export default async function Fast({ id }: { id: string }) {
  const [user, posts, comments] = await Promise.all([
    getUser(id),
    getPosts(id),
    getComments(id),
  ]);
  return <Profile user={user} posts={posts} comments={comments} />;
}
```

> **Gotcha — only parallelize *independent* requests.** If `getPosts` needs the result of `getUser` (e.g. the user's id), it genuinely must wait — that's a real dependency, not a waterfall. Parallelize only what doesn't depend on each other. To start a fetch early without blocking, you can kick it off (don't `await`) and `await` it later, or preload via a helper.

---

## V. MUTATIONS — SERVER ACTIONS (`"use server"`)

For **writes** (create/update/delete), Next.js gives you **Server Actions**: async functions that run *only* on the server but can be called directly from your components and forms. No manual API route, no `fetch` to your own backend, no client-side request plumbing.

Mark a function (or a whole file) with the **`"use server"`** directive:

```tsx
// app/actions.ts — every export here is a Server Action.
"use server";

import { prisma } from "@/lib/db";
import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string;     // read the submitted field
  const body = formData.get("body") as string;

  await prisma.post.create({ data: { title, body } }); // write to the DB on the server

  revalidatePath("/posts");                            // refresh the cached /posts page
}
```

> **Mental model.** A Server Action is a function you *import on the client* but that *executes on the server*. Next.js replaces the function body in the client bundle with a stub that POSTs to a generated endpoint. You get the ergonomics of a local function call with the safety of server-only code.

> **Gotcha — `"use server"` ≠ `"use client"`.** They are opposites and unrelated in purpose. `"use client"` marks a component boundary (UI that runs in the browser). `"use server"` marks **functions** as server-callable actions. Mixing them up is a classic confusion — `"use server"` is for *actions/mutations*, not components.

---

## VI. FORMS WITH SERVER ACTIONS

The cleanest mutation pattern: pass a Server Action straight to a `<form>`'s `action` prop. This works **without JavaScript** (progressive enhancement) — the form submits to the server even if the client bundle hasn't loaded.

```tsx
// app/posts/new/page.tsx — a Server Component rendering a form.
import { createPost } from "@/app/actions";

export default function NewPost() {
  return (
    <form action={createPost}>            {/* the action runs on the server on submit */}
      <input name="title" placeholder="Title" required />
      <textarea name="body" placeholder="Write…" required />
      <button type="submit">Publish</button>
    </form>
  );
}
```

You can also define an **inline** action inside a Server Component (the directive goes on the function):

```tsx
export default function Page() {
  async function add(formData: FormData) {
    "use server";                                  // inline Server Action
    await prisma.todo.create({ data: { text: formData.get("text") as string } });
    revalidatePath("/");
  }
  return (
    <form action={add}>
      <input name="text" />
      <button>Add</button>
    </form>
  );
}
```

### Passing extra arguments — `bind`

To pass data beyond the form fields (like an id), use `.bind`:

```tsx
import { updatePost } from "@/app/actions";

export default function EditButton({ postId }: { postId: string }) {
  const updateWithId = updatePost.bind(null, postId);  // prepends postId as first arg
  return (
    <form action={updateWithId}>
      <input name="title" />
      <button>Save</button>
    </form>
  );
}
// action signature: updatePost(postId: string, formData: FormData)
```

---

## VII. VALIDATION, RETURN VALUES & `useActionState`

Real actions validate input and report errors back to the UI. Return a serializable result object and surface it with **`useActionState`** (called `useFormState` in older React).

```tsx
// app/actions.ts
"use server";
import { z } from "zod";
import { revalidatePath } from "next/cache";

const Schema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters"),
  body: z.string().min(1, "Body is required"),
});

export type State = { error?: string; success?: boolean };

export async function createPost(prev: State, formData: FormData): Promise<State> {
  const parsed = Schema.safeParse({
    title: formData.get("title"),
    body: formData.get("body"),
  });
  if (!parsed.success) {
    return { error: parsed.error.issues[0].message };   // back to the UI
  }
  await prisma.post.create({ data: parsed.data });
  revalidatePath("/posts");
  return { success: true };
}
```

```tsx
// app/posts/new/form.tsx — CLIENT component wires the action to UI state.
"use client";
import { useActionState } from "react";
import { createPost, type State } from "@/app/actions";

export default function PostForm() {
  const [state, formAction, pending] = useActionState<State, FormData>(createPost, {});

  return (
    <form action={formAction}>
      <input name="title" />
      <textarea name="body" />
      {state.error && <p style={{ color: "red" }}>{state.error}</p>}
      {state.success && <p style={{ color: "green" }}>Published!</p>}
      <button disabled={pending}>{pending ? "Saving…" : "Publish"}</button>
    </form>
  );
}
```

---

## VIII. PENDING STATE & OPTIMISTIC UI

### `useFormStatus` — a self-aware submit button

A child of a `<form>` can read the form's pending state with **`useFormStatus`**, without prop-drilling. Perfect for a reusable submit button.

```tsx
"use client";
import { useFormStatus } from "react-dom";

export function SubmitButton() {
  const { pending } = useFormStatus();          // true while the action runs
  return <button disabled={pending}>{pending ? "Saving…" : "Save"}</button>;
}
```

> **Gotcha — `useFormStatus` must be a *child* of the `<form>`, not the component that renders the form.** It reads the nearest parent form's status via context. Put the button in its own component placed inside the `<form>`.

### `useOptimistic` — instant UI before the server responds

Show the result *immediately*, then reconcile when the action finishes. Great for likes, todos, comments.

```tsx
"use client";
import { useOptimistic } from "react";
import { addTodo } from "@/app/actions";

export default function Todos({ todos }: { todos: { id: string; text: string }[] }) {
  const [optimistic, addOptimistic] = useOptimistic(
    todos,
    (state, newText: string) => [...state, { id: "temp", text: newText }],
  );

  return (
    <>
      <ul>{optimistic.map((t) => <li key={t.id}>{t.text}</li>)}</ul>
      <form
        action={async (formData) => {
          const text = formData.get("text") as string;
          addOptimistic(text);                  // show INSTANTLY
          await addTodo(formData);              // then persist on the server
        }}
      >
        <input name="text" />
        <button>Add</button>
      </form>
    </>
  );
}
```

> **Gotcha — optimistic state reverts if the action throws.** If the server rejects, React rolls back the optimistic update to the real state. Always handle the error path (toast, retry) so the user understands why their item vanished.

---

## IX. REVALIDATION & REDIRECTS AFTER MUTATIONS

After a write, the cached pages showing that data are stale. Two tools fix this from inside an action:

```tsx
"use server";
import { revalidatePath, revalidateTag } from "next/cache";
import { redirect } from "next/navigation";

export async function publishPost(formData: FormData) {
  const post = await prisma.post.create({ data: { /* ... */ } });

  // Option A — invalidate a specific route's cache:
  revalidatePath("/posts");

  // Option B — invalidate everything tagged "posts" (matches fetch next.tags):
  revalidateTag("posts");

  // Then send the user to the new post (redirect throws — put it LAST):
  redirect(`/posts/${post.id}`);
}
```

| Function | Invalidates | Use when |
|----------|-------------|----------|
| `revalidatePath("/posts")` | The Data + Full Route cache for that path | You know the exact route(s) affected |
| `revalidatePath("/posts/[id]", "page")` | A dynamic path pattern | The path has dynamic segments |
| `revalidateTag("posts")` | Every `fetch`/`unstable_cache` with that tag | Data appears on many routes; tag once, invalidate everywhere |
| `redirect("/somewhere")` | (navigation, not cache) | After create/delete, move the user |

> **Gotcha — `redirect()` must come AFTER your DB work and revalidation, and OUTSIDE `try/catch`.** It throws an internal signal to perform navigation, so anything after it won't run, and a surrounding `try` would catch (swallow) the redirect. Do the mutation, revalidate, then redirect last.

---

## X. LOADING & ERROR UX FOR THE WHOLE FLOW

Tie it together with the file-convention UX from file 02:

- **`loading.tsx`** — shown while the server component's reads resolve (Suspense streaming).
- **`error.tsx`** — catches a thrown error during render (a failed fetch, a DB outage).
- **`useActionState` / `useFormStatus`** — per-mutation pending and error state inside forms.
- **`useOptimistic`** — instant feedback for the common happy path.

```tsx
// app/posts/loading.tsx
export default function Loading() {
  return <PostListSkeleton />;     // shown while Posts() fetches
}
```

```tsx
// app/posts/error.tsx
"use client";
export default function Error({ reset }: { error: Error; reset: () => void }) {
  return (
    <div>
      <p>Couldn't load posts.</p>
      <button onClick={reset}>Retry</button>
    </div>
  );
}
```

A complete mutation pipeline therefore looks like: **form → Server Action (validate → DB write → revalidate → redirect)**, with `useActionState` carrying validation errors back and `loading`/`error` files covering the read side. No API endpoint was written, yet you have a fully functioning full-stack feature.

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Using `useEffect` + `fetch` for first-load data | Spinners, waterfalls, no SEO | Fetch in a Server Component instead |
| Sequential `await`s for independent data | Slow pages | `Promise.all` to parallelize |
| Forgetting to revalidate after a write | UI shows stale data | `revalidatePath`/`revalidateTag` in the action |
| `redirect()` before the DB write / inside `try` | Write skipped or redirect swallowed | Put `redirect()` last, outside `try/catch` |
| Confusing `"use server"` with `"use client"` | Errors about directives | `"use server"` = actions/functions; `"use client"` = browser components |
| `useFormStatus` in the form's parent | `pending` always false | It must be a child *inside* the `<form>` |
| Not validating Server Action input | Bad/malicious data hits the DB | Validate (e.g. Zod) at the top of every action |
| Returning non-serializable values from an action | Runtime error | Return plain objects/strings/numbers only |
| Relying on Next 14 `fetch` cache default in Next 15 | Unexpected fresh/stale data | Pass explicit `cache`/`revalidate` options |

---

## 🧠 KEY TAKEAWAYS

- **Read on the server.** `async` Server Components `await` data before rendering — no `useEffect`, no spinners, no waterfalls for first-load data.
- The extended **`fetch`** controls caching: `force-cache`, `no-store`, `next.revalidate`, and `next.tags`. For non-`fetch` data use `unstable_cache` (persistent) and React `cache` (per-render dedupe).
- **Parallelize independent requests** with `Promise.all`; only serialize genuine dependencies.
- **Server Actions (`"use server"`)** are server-only functions callable from forms/components — mutations without a hand-written API. They support progressive enhancement.
- Surface results with **`useActionState`**, pending state with **`useFormStatus`**, and instant feedback with **`useOptimistic`**. Always validate action input.
- After a write, **`revalidatePath`/`revalidateTag`** clears stale caches and **`redirect()`** (last, outside `try`) moves the user on.

---

**Prev:** [`04-Rendering-Strategies-SSR-SSG-ISR.md`](./04-Rendering-Strategies-SSR-SSG-ISR.md) · **Next:** [`06-API-Routes-And-Route-Handlers.md`](./06-API-Routes-And-Route-Handlers.md) · **Index:** [`00-Index.md`](./00-Index.md)
