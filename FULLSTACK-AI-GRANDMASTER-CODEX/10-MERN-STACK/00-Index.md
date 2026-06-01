# 🔗 MERN Stack

> *"You learned the instruments one by one — React, Express, Node, MongoDB. This is where you sit down and play the symphony. One codebase, one data flow, one shipped product."*

> **Section 10 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module is the **integration capstone**. It does not re-teach React, Express, Node, or MongoDB — it shows how the four lock together into **one real, deployable, production-style full-stack application** with authentication, file uploads, real-time updates, tests, and a deployment pipeline.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- The **MERN architecture**: the complete request/data flow from a browser click, through React, across the network to Express, into Mongoose/MongoDB, and all the way back to the rendered pixel
- **Project structure decisions**: separate repos vs monorepo, folder layout, a dev environment where a Vite frontend and an Express backend run together cleanly (proxy, `concurrently`, CORS)
- A **layered backend**: Express + Mongoose with models, routes, controllers, services, validation, centralized error handling, and environment config — purpose-built for the app's frontend
- A **real React frontend**: routing, pages/components, a typed API client, server-state with TanStack Query, full CRUD against the live API, loading/error/empty states
- **End-to-end authentication**: register/login with bcrypt + JWT, the httpOnly-cookie-vs-localStorage decision, refresh-token rotation, auth middleware on the backend, an auth context + protected routes on the frontend, logout, and session persistence
- **Global state, file uploads, and real-time**: server state vs client state, image/file uploads (multer), optimistic updates, and live notifications with Socket.IO
- **Shipping it**: testing the stack (Jest + Supertest backend, React Testing Library frontend), production builds, the two serving strategies, and deploying frontend + backend + database (Vercel/Netlify + Render/Railway/Fly + MongoDB Atlas) with a production checklist

---

## 🧩 THE PROJECT — "TaskFlow"

Everything in this section builds **one** application, layer by layer: **TaskFlow**, a collaborative task manager (think a stripped-down Trello/Todoist). It is small enough to finish and rich enough to exercise every MERN concern.

| Feature | Exercises |
|---------|-----------|
| Sign up / log in / log out | bcrypt, JWT, refresh tokens, auth context, protected routes |
| Create / read / update / delete tasks | REST CRUD across the full stack, Mongoose models, React Query mutations |
| Tasks belong to the logged-in user | authorization, ownership checks, populated references |
| Filter / sort / paginate tasks | query params end-to-end |
| Upload an avatar / task attachment | multer, multipart forms, static file serving |
| Live "task updated" notifications | Socket.IO rooms, optimistic UI |
| Validation everywhere | zod on the server, controlled forms on the client |

By file 06 you will have deployed this app to the internet with a real database behind it.

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file **adds a layer** to TaskFlow. The ⭐ files are the highest-leverage — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here — overview, the project, the complete roadmap, prerequisites, setup | — |
| 01 | [`01-The-MERN-Architecture.md`](./01-The-MERN-Architecture.md) | What MERN is, the full request/data flow diagram, why this stack, monorepo vs separate repos, folder layout, the dev environment (Vite + Express + proxy + `concurrently`) | ⭐ |
| 02 | [`02-Building-The-Backend-API.md`](./02-Building-The-Backend-API.md) | Scaffold Express + Mongoose, env config, DB connection, `User` + `Task` models, routes → controllers → services layering, CRUD REST endpoints, validation, error handling, CORS for the client | ⭐ |
| 03 | [`03-Building-The-React-Frontend.md`](./03-Building-The-React-Frontend.md) | Scaffold Vite React, routing, pages/components, the axios API client, calling the backend, full CRUD UI, loading/error/empty states, TanStack Query | ⭐ |
| 04 | [`04-Authentication-Across-The-Stack.md`](./04-Authentication-Across-The-Stack.md) | Register/login endpoints (bcrypt + JWT), httpOnly cookie vs localStorage, refresh-token rotation, auth middleware, auth context + protected routes, logout, session persistence | ⭐ |
| 05 | [`05-State-File-Uploads-And-Realtime.md`](./05-State-File-Uploads-And-Realtime.md) | Global state choice, React Query for server state, file/image uploads (multer + forms), Socket.IO real-time notifications, optimistic updates | Core |
| 06 | [`06-Testing-Building-And-Deploying-MERN.md`](./06-Testing-Building-And-Deploying-MERN.md) | Backend tests (Jest + Supertest), frontend tests (RTL), prod env vars, building React, serving strategies, deploying backend/frontend/DB, CI/CD, the production checklist | ⭐ |

---

## 🗺️ COMPLETE MERN ROADMAP (coverage checklist)

> This is the **roadmap.sh-style master checklist** for full-stack MERN integration. Every concept maps to the file that teaches it. If you can check every box, you can build and ship a complete MERN app — nothing left out.

### 1 — MERN Architecture & Data Flow → `01`
- [x] What MERN is (MongoDB + Express + React + Node) and what each layer owns
- [x] The **end-to-end request/data flow** (browser → React → HTTP → Express → Mongoose → MongoDB → back)
- [x] Client-side rendering (SPA) vs server-rendered — where MERN sits, and the Next.js alternative
- [x] JSON as the contract between frontend and backend
- [x] Why this stack (one language, JSON-native, huge ecosystem) and its tradeoffs
- [x] Synchronous user action vs asynchronous network round-trip (the mental model)

### 2 — Project Structure & Dev Environment → `01`
- [x] **Separate repos vs monorepo** (tradeoffs, when to pick each)
- [x] Recommended folder layout (`/client` + `/server`, or workspaces)
- [x] Running frontend + backend together (`concurrently`, root scripts)
- [x] The **Vite dev proxy** (avoid CORS in dev, single origin)
- [x] Shared types/contracts between client and server (note)
- [x] `.env` files per side, never committed; `.gitignore` hygiene

### 3 — Backend: Express + Mongoose → `02`
- [x] Scaffolding the Express app & server entry point
- [x] **Environment config** (dotenv, config module, validation)
- [x] **Connecting to MongoDB** with Mongoose (connection, events, retries)
- [x] **Models** (`User`, `Task`) with schemas, types, validation, refs, timestamps
- [x] **Layered architecture**: routes → controllers → services
- [x] **CRUD REST endpoints** for the domain (tasks)
- [x] **Request validation** (zod) at the boundary
- [x] **Centralized error handling** + custom `AppError` + async wrapper
- [x] **CORS** configured for the React client
- [x] Consistent JSON response envelopes & status codes

### 4 — REST API Design for the App → `02`, `03`
- [x] Resource modeling for TaskFlow (`/api/auth`, `/api/tasks`, `/api/users`)
- [x] HTTP verbs & status codes used correctly
- [x] **Pagination, filtering, sorting** via query params (end-to-end)
- [x] Ownership / scoping responses to the current user
- [x] API versioning & base path (`/api`)
- [x] Error shape the frontend can rely on

### 5 — Frontend: React + Routing + State → `03`
- [x] Scaffolding a **Vite** React app
- [x] **Routing** (React Router): pages, layouts, nested & dynamic routes
- [x] Component/page/feature folder structure
- [x] **API client** wrapper (axios instance, interceptors, base URL)
- [x] Displaying / creating / updating / deleting data against the API
- [x] **Loading / error / empty** states (the three you always forget)
- [x] **TanStack Query** for server state (queries, mutations, cache invalidation)
- [x] Custom hooks wrapping the data layer

### 6 — Connecting Frontend ↔ Backend → `01`, `03`, `04`
- [x] **fetch vs axios** (and why a wrapper)
- [x] The **Vite proxy** in dev; absolute base URL in prod
- [x] **CORS** in production (origins, credentials)
- [x] Sending/receiving JSON; sending cookies (`withCredentials`)
- [x] Environment-based API base URL (`import.meta.env`)

### 7 — Authentication End-to-End → `04`
- [x] **Register** endpoint (bcrypt hashing, unique email)
- [x] **Login** endpoint (verify password, issue tokens)
- [x] **JWT** access tokens (sign, verify, expiry, payload)
- [x] **Refresh tokens** & rotation (issue, store, rotate, revoke)
- [x] **httpOnly cookies vs localStorage** — the security tradeoff, spelled out
- [x] **Auth middleware** on the backend (protect routes, attach `req.user`)
- [x] **Auth context** + **protected routes** on the frontend
- [x] **Logout** (clear cookie / token, revoke refresh)
- [x] **Persisting sessions** across reloads (silent refresh / `/me`)
- [x] CSRF considerations with cookie auth

### 8 — Global State & Server State → `05`, `03`
- [x] Client state vs **server state** (why the distinction matters)
- [x] **Context** for auth/UI state; when it's enough
- [x] **Redux Toolkit / Zustand** — when to reach for them (decision guide)
- [x] **TanStack Query** as the server-state cache (the recommended default)
- [x] Avoiding the "put everything in global state" anti-pattern

### 9 — Forms & Validation Across the Stack → `02`, `03`, `04`
- [x] Controlled components & form state on the client
- [x] Client-side validation (instant feedback) — UX only, never trust it
- [x] **Server-side validation** (the real gate) with zod
- [x] Surfacing server validation errors back into the form
- [x] React Hook Form note for larger forms

### 10 — File Uploads → `05`
- [x] **Multipart/form-data** vs JSON
- [x] **multer** on the backend (disk vs memory storage, limits, file filter)
- [x] The upload form & `FormData` on the frontend
- [x] Serving uploaded files (static dir) vs **cloud storage** (S3/Cloudinary) note
- [x] Validating size/type; security of uploads

### 11 — Real-Time (Socket.IO) → `05`
- [x] When you need WebSockets vs polling
- [x] **Socket.IO** server setup alongside Express
- [x] Authenticated sockets (passing the JWT)
- [x] **Rooms** (per-user notifications)
- [x] Client connection + reacting to events (live task updates)
- [x] **Optimistic updates** paired with real-time confirmation

### 12 — Error Handling Across the Stack → `02`, `03`, `04`, `06`
- [x] Backend: centralized handler, operational vs programmer errors
- [x] Network/transport errors on the client (timeouts, offline)
- [x] 401/403 handling (auto-logout / refresh) via interceptors
- [x] Error boundaries in React
- [x] Consistent error shape contract

### 13 — Environment Config → `01`, `02`, `06`
- [x] `.env` on the server (`PORT`, `MONGODB_URI`, `JWT_SECRET`, …)
- [x] `import.meta.env` on the client (Vite `VITE_` prefix)
- [x] Dev vs prod config layering; secrets never in the bundle
- [x] 12-factor config principles

### 14 — Building for Production → `06`
- [x] `vite build` → static assets; what the bundle contains
- [x] Backend prod settings (NODE_ENV, trust proxy, compression, helmet)
- [x] **Serving strategies**: separate hosts vs Express serving the static build
- [x] Caching, gzip/brotli, cache-busting hashes

### 15 — Deployment (Frontend + Backend + DB) → `06`
- [x] **MongoDB Atlas** (managed DB, network access, connection string)
- [x] **Backend** deploy (Render / Railway / Fly.io) — env vars, health checks
- [x] **Frontend** deploy (Vercel / Netlify) — env, rewrites, SPA fallback
- [x] CORS & cookie domains across deployed origins
- [x] **CI/CD** overview (GitHub Actions: test → build → deploy)
- [x] The **production readiness checklist**

### 16 — Testing the Stack → `06`
- [x] Backend **unit + integration** tests (Jest + Supertest, in-memory Mongo)
- [x] Frontend tests (**React Testing Library** + Vitest, MSW for API mocks)
- [x] Testing auth flows & protected routes
- [x] What to test vs what to skip (the testing pyramid for MERN)

> **Coverage promise:** Every box above is taught with runnable code inside this section. Where a topic is developed deeply in another section (React internals in `05`, Express/Node internals in `07`, MongoDB internals in `09`), this section *integrates* it and links back rather than repeating it.

---

## ✅ PREREQUISITES — DO NOT SKIP

This section assumes you have worked through (or are comfortable with) the three pillars it ties together. If a concept here feels shaky, the deep treatment is one link away:

| You should already know | From section | Specifically |
|-------------------------|--------------|--------------|
| React components, hooks, routing, data fetching, forms | [`05-REACT`](../05-REACT/00-Index.md) | [`04-Hooks-Deep-Dive`](../05-REACT/04-Hooks-Deep-Dive.md), [`07-Data-Fetching-And-Effects`](../05-REACT/07-Data-Fetching-And-Effects.md), [`10-Routing-With-React-Router`](../05-REACT/10-Routing-With-React-Router.md), [`06-Forms-And-Controlled-Components`](../05-REACT/06-Forms-And-Controlled-Components.md) |
| Node runtime, Express routing/middleware, REST, auth/security | [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/00-Index.md) | [`04-Express-Fundamentals`](../07-NODEJS-EXPRESS/04-Express-Fundamentals.md), [`05-Building-REST-APIs`](../07-NODEJS-EXPRESS/05-Building-REST-APIs.md), [`07-Authentication-And-Security`](../07-NODEJS-EXPRESS/07-Authentication-And-Security.md) |
| MongoDB document model, CRUD, Mongoose ODM, data modeling | [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/00-Index.md) | [`04-Data-Modeling-And-Schema-Design`](../09-NOSQL-MONGODB/04-Data-Modeling-And-Schema-Design.md), [`06-Mongoose-ODM`](../09-NOSQL-MONGODB/06-Mongoose-ODM.md) |
| JavaScript (closures, `this`, async/await, modules) | [`02-JAVASCRIPT-MASTERY`](../02-JAVASCRIPT-MASTERY/00-Index.md) | the whole section |

> **Honest note:** this section moves fast on each individual technology because it has to cover the *seams* between them. If you have never built a React component or a single Express route, build those first. The MERN magic is in the integration, and integration is hard to appreciate without the pieces.

---

## 🛠️ SETUP — TOOLS FOR THE WHOLE STACK

You will run **two processes** during development: the Vite dev server (frontend) and the Express server (backend). One database (local or Atlas) backs them.

### What you need installed

```bash
node -v     # v18+ (LTS recommended: 20 or 22) — runtime for the backend AND Vite
npm -v      # ships with Node — package manager
git --version   # version control, required for deployment
```

| Tool | Why | Get it |
|------|-----|--------|
| **Node 18+ (LTS)** | runs Express and Vite | [nodejs.org](https://nodejs.org) or a version manager (`nvm`/`fnm`) |
| **MongoDB** | the database | local via Docker/installer, **or** a free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster (recommended) |
| **MongoDB Compass** | GUI to inspect your data | [mongodb.com/products/compass](https://www.mongodb.com/products/compass) |
| **VS Code** | editor | + ESLint, Prettier, and the REST Client / Thunder Client extensions |
| **An API client** | hit endpoints before the UI exists | Postman, Insomnia, Thunder Client, `curl`, or `httpie` |
| **A browser with React DevTools** | inspect component tree & state | Chrome/Firefox extension |

### The top-level shape we will build (monorepo)

```text
taskflow/
├── package.json          # root: scripts to run both sides with `concurrently`
├── .gitignore            # node_modules, .env, dist, uploads
├── client/               # Vite + React app (section 03)
│   ├── package.json
│   ├── vite.config.js    # dev proxy → backend
│   ├── .env              # VITE_API_URL
│   └── src/
└── server/               # Express + Mongoose API (section 02)
    ├── package.json
    ├── .env              # PORT, MONGODB_URI, JWT_SECRET, ...
    └── src/
```

We justify the monorepo choice (vs two separate repos) in file 01 — both are valid, and you will know exactly when to pick which.

### One command to rule them both (preview)

```jsonc
// taskflow/package.json (root) — full version built in file 01
{
  "name": "taskflow",
  "private": true,
  "scripts": {
    // run client + server together; each restarts on its own changes
    "dev": "concurrently -n client,server -c blue,green \"npm:dev:client\" \"npm:dev:server\"",
    "dev:client": "npm --prefix client run dev",
    "dev:server": "npm --prefix server run dev"
  },
  "devDependencies": { "concurrently": "^9.0.0" }
}
```

```bash
npm run dev     # boots Vite (http://localhost:5173) AND Express (http://localhost:5000)
```

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Build TaskFlow as you read.** This is not a section to skim — type the project. Each file leaves you with a working app that does more than the last.
2. **Run both servers and a database from file 01 onward.** The integration only makes sense when the pieces are live and talking.
3. **Watch the network tab.** Every concept here is visible as an HTTP request/response. Open DevTools → Network and watch React talk to Express.
4. **Trace one feature top to bottom.** Pick "create a task" and follow it: button click → React Query mutation → axios → Express route → controller → service → Mongoose → MongoDB → response → cache update → re-render. That trace *is* MERN.
5. **Break the seams on purpose.** Misconfigure CORS, drop the token, kill the database connection. The errors you cause here are the errors you will debug in production.

---

## 🔗 RELATED SECTIONS

- **The three pillars:** [`05-REACT`](../05-REACT/00-Index.md), [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/00-Index.md), [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/00-Index.md) — the deep dives this section integrates.
- **Type it:** [`03-TYPESCRIPT`](../03-TYPESCRIPT/00-Index.md) — real MERN apps are TypeScript end-to-end; everything here maps 1:1.
- **The framework alternative:** [`06-NEXTJS`](../06-NEXTJS/00-Index.md) — when you want SSR/SSG and a unified full-stack framework instead of separate client/server.
- **Relational alternative:** [`08-SQL-DATABASES`](../08-SQL-DATABASES/00-Index.md) — swap the "M" for Postgres and you have the PERN stack; the integration patterns are identical.
- **Ship it for real:** [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/00-Index.md) — CI/CD depth, Docker, system design, observability, scaling beyond one box.

---

## 📎 DEEP REFERENCES (authoritative sources)

- **The MERN concept** — [mongodb.com/resources/languages/mern-stack](https://www.mongodb.com/resources/languages/mern-stack)
- **Express docs** — [expressjs.com](https://expressjs.com/)
- **Mongoose docs** — [mongoosejs.com/docs](https://mongoosejs.com/docs/)
- **React docs** — [react.dev](https://react.dev/)
- **React Router** — [reactrouter.com](https://reactrouter.com/)
- **TanStack Query** — [tanstack.com/query](https://tanstack.com/query/latest)
- **Vite** — [vitejs.dev](https://vitejs.dev/)
- **Socket.IO** — [socket.io/docs](https://socket.io/docs/v4/)
- **MongoDB Atlas** — [mongodb.com/atlas](https://www.mongodb.com/atlas)
- **JWT** — [jwt.io](https://jwt.io/) and [datatracker.ietf.org/doc/html/rfc7519](https://datatracker.ietf.org/doc/html/rfc7519)
- **OWASP Top 10** — [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/)

---

**→ Begin:** [`01-The-MERN-Architecture.md`](./01-The-MERN-Architecture.md) | Back to [`../README.md`](../README.md)
