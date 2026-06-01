# ▲ 07 — Auth & Full-Stack Next.js

> *"Authentication answers 'who are you?'; authorization answers 'what may you do?'. Next.js lets both live beside your UI — a session read in a Server Component, a gate enforced in middleware, a write guarded in an action."*

**Prev:** [`06-API-Routes-And-Route-Handlers.md`](./06-API-Routes-And-Route-Handlers.md) · **Next:** [`08-Optimization-And-Deployment.md`](./08-Optimization-And-Deployment.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE FULL-STACK SHAPE OF A NEXT.JS APP

Before auth, internalize what "full-stack Next.js" means: a single project owns the **database schema**, the **server logic** (actions + handlers), and the **UI** — all deployed together. A feature flows top to bottom in one codebase:

```
   DATABASE  ──►  DATA LAYER  ──►  SERVER LOGIC  ──►  UI
   (schema)       (ORM/queries)   (Server Actions/    (Server + Client
                                   Route Handlers)      Components)
        ▲                                                   │
        └───────────── revalidate / redirect ◄──────────────┘
```

Auth threads through every layer: the schema stores users/sessions, the data layer reads them, middleware and actions enforce access, and the UI reflects who's logged in. We'll build the layers, add auth, then wire a complete guarded feature.

---

## II. ENVIRONMENT VARIABLES — THE FOUNDATION

Auth needs secrets (provider keys, a session-signing secret, a DB URL). Next.js has firm rules about what reaches the browser.

```bash
# .env.local  (gitignored — never commit real secrets)
DATABASE_URL="postgresql://user:pass@localhost:5432/app"
AUTH_SECRET="a-long-random-string-openssl-rand-base64-32"
GITHUB_ID="..."
GITHUB_SECRET="..."

# Exposed to the browser ONLY because of the NEXT_PUBLIC_ prefix:
NEXT_PUBLIC_SITE_URL="http://localhost:3000"
```

| Variable | Visible to browser? | Use for |
|----------|--------------------|---------|
| `DATABASE_URL`, `AUTH_SECRET`, `GITHUB_SECRET` | **No** (server-only) | Secrets, DB, API keys |
| `NEXT_PUBLIC_SITE_URL` | **Yes** (inlined at build) | Public config (base URLs, analytics IDs) |

```tsx
// Server Component / Action / Handler — full access:
const dbUrl = process.env.DATABASE_URL;          // ✅ works on server

// Client Component — only NEXT_PUBLIC_* exist:
"use client";
const site = process.env.NEXT_PUBLIC_SITE_URL;   // ✅
const secret = process.env.AUTH_SECRET;          // ❌ undefined in the browser
```

> **Gotcha — `NEXT_PUBLIC_` values are inlined at *build* time and are public forever.** They're baked into the JS bundle, so anyone can read them. Never put a secret behind `NEXT_PUBLIC_`. And because they're build-time, changing one requires a rebuild — they're not runtime-configurable.

> **Gotcha — `.env.local` is for secrets and is gitignored by default.** Use `.env` for non-secret defaults that *can* be committed, `.env.local` for machine-specific secrets. Never commit real credentials; provide a `.env.example` with blank keys for teammates.

---

## III. AUTHENTICATION WITH AUTH.JS (NEXTAUTH v5)

**Auth.js** (formerly NextAuth.js) is the de-facto auth library for Next.js. Version 5 is built for the App Router. It handles OAuth providers (Google, GitHub, ...), email/credentials, sessions, CSRF, and cookie management for you.

```bash
npm install next-auth@beta      # Auth.js v5
```

### Configure providers and export helpers

```ts
// auth.ts (project root) — the single source of auth truth.
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
  ],
  pages: {
    signIn: "/login",            // custom sign-in page (optional)
  },
});
```

### Mount the auth API route

Auth.js needs HTTP endpoints for the OAuth dance (callbacks, sign-in, sign-out). One Route Handler wires them all:

```ts
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";
export const { GET, POST } = handlers;   // catch-all handles all auth endpoints
```

> **Mental model.** `auth.ts` is configuration + helpers; the `[...nextauth]/route.ts` catch-all is the live endpoint. The helpers (`auth`, `signIn`, `signOut`) are what you call from your app code.

---

## IV. SESSIONS — JWT vs DATABASE

A **session** is how the server remembers a logged-in user across requests. Auth.js offers two strategies:

| Strategy | How it works | Pros | Cons |
|----------|--------------|------|------|
| **JWT** (default) | Encrypted token stored in a cookie; no DB read to verify | Fast, stateless, scales horizontally | Can't instantly revoke; size limits |
| **Database** | Session row in your DB, cookie holds an id | Revocable, queryable, audit trail | A DB read per request |

```ts
// auth.ts — choose a strategy
export const { handlers, auth, signIn, signOut } = NextAuth({
  session: { strategy: "jwt" },        // or "database" (needs an adapter)
  providers: [/* ... */],
});
```

For the database strategy, add an **adapter** that maps Auth.js to your DB:

```ts
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/db";

export const { handlers, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),
  session: { strategy: "database" },
  providers: [/* ... */],
});
```

> **Gotcha — middleware can't reach a database session.** Middleware runs on the Edge with no DB access. If you protect routes in middleware (next section), you typically need the **JWT** strategy so the session is readable from the cookie without a DB call. Database sessions are still great for server-side checks in components/actions.

---

## V. READING THE SESSION

The `auth()` helper reads the current session anywhere on the server — components, actions, handlers.

```tsx
// app/profile/page.tsx — Server Component reading the session.
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function Profile() {
  const session = await auth();
  if (!session?.user) redirect("/login");      // not logged in → bounce

  return <h1>Welcome, {session.user.name}</h1>;
}
```

### Sign in / sign out buttons

`signIn` and `signOut` are Server Actions you can hand straight to a form:

```tsx
// app/components/AuthButtons.tsx — Server Component, no client JS needed.
import { signIn, signOut, auth } from "@/auth";

export default async function AuthButtons() {
  const session = await auth();

  if (session?.user) {
    return (
      <form action={async () => { "use server"; await signOut(); }}>
        <button>Sign out ({session.user.email})</button>
      </form>
    );
  }
  return (
    <form action={async () => { "use server"; await signIn("github"); }}>
      <button>Sign in with GitHub</button>
    </form>
  );
}
```

### Client-side session access

If a Client Component needs the session, wrap the app in `SessionProvider` and use `useSession`:

```tsx
"use client";
import { useSession } from "next-auth/react";

export function Avatar() {
  const { data: session, status } = useSession();
  if (status === "loading") return <Spinner />;
  return session?.user ? <img src={session.user.image ?? ""} alt="" /> : null;
}
```

> **Gotcha — prefer reading the session on the server.** `useSession` triggers a client request and adds a loading state. In the App Router, read it with `auth()` in Server Components/actions whenever possible; reserve `useSession` for genuinely interactive client UI.

---

## VI. PROTECTING ROUTES VIA MIDDLEWARE

The cleanest gate for whole sections of the app is **middleware** — it runs before the route and can redirect unauthenticated users in one place.

```ts
// middleware.ts
import { auth } from "@/auth";                 // Auth.js exposes an auth() middleware wrapper
import { NextResponse } from "next/server";

export default auth((req) => {
  const isLoggedIn = Boolean(req.auth);         // req.auth is populated by Auth.js
  const isProtected = req.nextUrl.pathname.startsWith("/dashboard");

  if (isProtected && !isLoggedIn) {
    const login = new URL("/login", req.nextUrl.origin);
    login.searchParams.set("callbackUrl", req.nextUrl.pathname);
    return NextResponse.redirect(login);
  }
  return NextResponse.next();
});

export const config = {
  // Run on everything except static assets and the auth API:
  matcher: ["/((?!api/auth|_next/static|_next/image|favicon.ico).*)"],
};
```

> **Gotcha — middleware is a *first* line of defense, not the only one.** A determined caller can hit a Server Action or Route Handler directly. **Always re-check authorization at the point of the mutation/data access too** — middleware reduces noise and redirects users, but server-side checks in actions/handlers are what actually keep data safe. Defense in depth.

---

## VII. AUTHORIZATION — ROLES & PERMISSIONS

Authentication ≠ authorization. Once you know *who* the user is, check *what they may do*. Store a role on the user and verify it server-side.

```ts
// lib/auth-guards.ts — reusable server-side guards.
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export async function requireUser() {
  const session = await auth();
  if (!session?.user) redirect("/login");
  return session.user;
}

export async function requireAdmin() {
  const user = await requireUser();
  if (user.role !== "admin") redirect("/forbidden");   // authenticated but not allowed
  return user;
}
```

```tsx
// app/admin/page.tsx — gated by role at the data-access point.
import { requireAdmin } from "@/lib/auth-guards";

export default async function AdminPage() {
  const admin = await requireAdmin();          // throws/redirects if not an admin
  return <h1>Admin console — {admin.name}</h1>;
}
```

> **Gotcha — never trust a role from the client.** A role rendered in client state can be spoofed. Read the role from the *server session* (or DB) at the moment of the protected action. Hiding an admin button in the UI is UX, not security.

---

## VIII. A COMPLETE FULL-STACK FEATURE — END TO END

Let's build a guarded "Notes" feature: schema → data layer → Server Action → guarded UI. This is the synthesis of files 03–07.

### 1) Schema (Prisma)

```prisma
// prisma/schema.prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  role  String @default("user")
  notes Note[]
}

model Note {
  id        String   @id @default(cuid())
  text      String
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
}
```

### 2) Server Action (guarded mutation)

```tsx
// app/notes/actions.ts
"use server";
import { z } from "zod";
import { prisma } from "@/lib/db";
import { requireUser } from "@/lib/auth-guards";
import { revalidatePath } from "next/cache";

const NoteSchema = z.object({ text: z.string().min(1, "Note can't be empty") });

export async function createNote(prev: { error?: string }, formData: FormData) {
  const user = await requireUser();                       // 🔒 auth check at the write
  const parsed = NoteSchema.safeParse({ text: formData.get("text") });
  if (!parsed.success) return { error: parsed.error.issues[0].message };

  await prisma.note.create({
    data: { text: parsed.data.text, authorId: user.id },  // tie to the logged-in user
  });

  revalidatePath("/notes");                                // refresh the list
  return { error: undefined };
}

export async function deleteNote(id: string) {
  const user = await requireUser();
  // 🔒 ownership check: only delete YOUR note
  await prisma.note.deleteMany({ where: { id, authorId: user.id } });
  revalidatePath("/notes");
}
```

### 3) UI (Server Component list + Client form)

```tsx
// app/notes/page.tsx — Server Component: reads session + data, renders the feature.
import { requireUser } from "@/lib/auth-guards";
import { prisma } from "@/lib/db";
import { deleteNote } from "./actions";
import NoteForm from "./note-form";

export default async function NotesPage() {
  const user = await requireUser();                          // 🔒 page-level gate
  const notes = await prisma.note.findMany({
    where: { authorId: user.id },
    orderBy: { createdAt: "desc" },
  });

  return (
    <main>
      <h1>{user.email}'s notes</h1>
      <NoteForm />                                            {/* client form island */}
      <ul>
        {notes.map((n) => (
          <li key={n.id}>
            {n.text}
            <form action={deleteNote.bind(null, n.id)}>       {/* bind the id */}
              <button>Delete</button>
            </form>
          </li>
        ))}
      </ul>
    </main>
  );
}
```

```tsx
// app/notes/note-form.tsx — Client Component for pending/error UX.
"use client";
import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { createNote } from "./actions";

function Submit() {
  const { pending } = useFormStatus();
  return <button disabled={pending}>{pending ? "Saving…" : "Add note"}</button>;
}

export default function NoteForm() {
  const [state, action] = useActionState(createNote, { error: undefined });
  return (
    <form action={action}>
      <input name="text" placeholder="New note…" />
      {state.error && <p style={{ color: "red" }}>{state.error}</p>}
      <Submit />
    </form>
  );
}
```

This feature is **fully full-stack** with no API endpoint hand-written: middleware redirects anonymous users, the page re-checks auth, the action validates + verifies ownership before writing, and `revalidatePath` keeps the list fresh. Every security check is on the server.

---

## IX. SECURITY CHECKLIST

| Concern | Where to handle it |
|---------|--------------------|
| Anonymous users hitting protected pages | Middleware redirect + page-level `requireUser()` |
| Direct action/handler calls bypassing UI | Re-check auth **inside** the action/handler |
| Users editing others' data | Ownership check in the query (`where: { authorId }`) |
| Roles | Server session/DB, never client state |
| Secrets in the browser | Never `NEXT_PUBLIC_`; use server-only env vars |
| Input from forms/APIs | Validate (Zod) before touching the DB |
| Session signing | A strong `AUTH_SECRET`, rotated carefully |
| CSRF | Auth.js handles it; Server Actions are POST-only with origin checks |

> **Gotcha — Server Actions are publicly reachable endpoints.** Even though you call them like functions, Next.js exposes each as a POST endpoint. Treat every action as untrusted input: authenticate, authorize, and validate inside it. "It's only called from my form" is not a security boundary.

---

## X. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Secret behind `NEXT_PUBLIC_` | Secret leaks in the bundle | Use a server-only var (no prefix) |
| Database session + middleware gate | Middleware can't read it | Use JWT strategy for middleware checks |
| Only gating in middleware | Actions/handlers still callable | Re-check auth at every mutation/data access |
| Trusting a client-side role | Privilege escalation | Read role from server session/DB |
| No ownership check on delete/update | Users edit others' rows | `where: { id, authorId: user.id }` |
| `redirect()` inside a `try` in an action | Redirect swallowed | Call it last, outside `try/catch` |
| Changing `NEXT_PUBLIC_` var without rebuild | Old value persists | Rebuild — public vars are inlined at build |
| Committing `.env.local` | Secrets in git history | Keep it gitignored; rotate any leaked secret |

---

## 🧠 KEY TAKEAWAYS

- Full-stack Next.js owns **schema → data → server logic → UI** in one project; auth threads through every layer.
- **Environment variables:** server-only by default; only `NEXT_PUBLIC_`-prefixed vars reach the browser (inlined at build, never for secrets).
- **Auth.js (NextAuth v5)** handles OAuth/credentials, sessions, and CSRF; configure in `auth.ts` and mount the `[...nextauth]` catch-all handler.
- **Sessions** are JWT (stateless, Edge-readable, hard to revoke) or database (revocable, needs a DB read). Middleware gating usually requires JWT.
- Read the session server-side with **`auth()`**; protect sections with **middleware**, but **always re-check auth and ownership inside actions/handlers** — middleware alone is not a security boundary.
- **Authorization is separate from authentication:** store roles server-side and verify at the protected operation; never trust client state.
- A complete feature needs **no hand-written API** — middleware + a guarded Server Action + `revalidatePath` + Server/Client components is the whole stack.

---

**Prev:** [`06-API-Routes-And-Route-Handlers.md`](./06-API-Routes-And-Route-Handlers.md) · **Next:** [`08-Optimization-And-Deployment.md`](./08-Optimization-And-Deployment.md) · **Index:** [`00-Index.md`](./00-Index.md)
