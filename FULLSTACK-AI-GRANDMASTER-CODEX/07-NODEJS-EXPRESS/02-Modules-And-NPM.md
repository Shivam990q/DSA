# 🟢 02 — Modules & NPM

> *"A program is a graph of small things that trust each other. Modules are the nodes; npm is the registry that brought a million strangers' code into your codebase. Master them — or be ruled by them."*

**Prev:** [`01-The-Nodejs-Runtime.md`](./01-The-Nodejs-Runtime.md) · **Next:** [`03-Core-Modules-And-Async.md`](./03-Core-Modules-And-Async.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHY MODULES EXIST

Browser JS used to be a single script that polluted one global object. That doesn't scale. Node was born with **modules** — every file is its own scope, exports a public surface, and imports what it needs. Today JavaScript has **two** module systems living side by side: **CommonJS (CJS)** and **ECMAScript Modules (ESM)**. You will meet both forever; learn both well.

```
Module = file = independent scope + a public API.
Modules form a graph; the entry point is the root.
```

---

## II. COMMONJS (CJS)

CommonJS was Node's original module system. It is **synchronous** and uses `require` / `module.exports`.

```js
// math.js  (CJS)
function add(a, b) { return a + b; }
function sub(a, b) { return a - b; }

module.exports = { add, sub };       // export an object
// or:  module.exports.add = add;    // attach individual exports
// or:  exports.add = add;           // shortcut — but DON'T reassign `exports` itself
```

```js
// app.js  (CJS)
const { add, sub } = require("./math");   // .js extension is implied
console.log(add(2, 3));                    // 5

// Default-import the whole module:
const math = require("./math");
console.log(math.sub(5, 1));               // 4
```

### What `require` actually does (short version)

1. **Resolve** the path (algorithm in section IV).
2. **Cache check** — already loaded? Return the cached `module.exports`.
3. **Load**: read the file, wrap it in a function, execute it.
4. **Cache** the resulting `module.exports` and return it.

The wrapper is roughly:

```js
(function (exports, require, module, __filename, __dirname) {
   // your file's code goes here
});
```

That is why `__dirname`, `__filename`, `module`, `exports`, and `require` "just exist" inside CJS modules — Node injects them.

> **Gotcha — `exports` vs `module.exports`.** `exports` starts as a reference to `module.exports`. Assigning `exports = something` only changes the local variable, **not** `module.exports`. If you want to replace the whole export, write `module.exports = ...`.

```js
// BUG
exports = function () { /* ... */ };   // no-op for the importer
// FIX
module.exports = function () { /* ... */ };
```

> **Gotcha — module caching is per-resolved-path.** The same file, required twice, returns the **same object**. That makes singletons easy and makes mutation across modules dangerous.

```js
// counter.js
let n = 0;
module.exports = {
  inc()   { return ++n; },
  value() { return n;   }
};

// a.js
const c = require("./counter"); c.inc();
// b.js
const c = require("./counter"); console.log(c.value());  // 1, not 0 — same instance
```

---

## III. ECMASCRIPT MODULES (ESM)

ESM is the **standard** module system, the same one browsers use. Syntax is `import` / `export`. ESM is **statically analyzable** (the imports are known before code runs), enables **tree-shaking** by bundlers, and supports **top-level `await`**.

```js
// math.mjs  (ESM)
export function add(a, b) { return a + b; }
export function sub(a, b) { return a - b; }
export const PI = 3.14159;

export default function multiply(a, b) { return a * b; }   // one default per file
```

```js
// app.mjs  (ESM)
import multiply, { add, sub, PI } from "./math.mjs";   // extension is REQUIRED
import * as math from "./math.mjs";                     // namespace import

console.log(add(2, 3), multiply(2, 3), math.PI);

// Top-level await — only works in ESM
const data = await fetch("https://api.github.com").then(r => r.json());
```

### Two ways to opt into ESM

1. **`.mjs` extension** — Node always treats it as ESM.
2. **`"type": "module"` in `package.json`** — every `.js` in that package is ESM. Use `.cjs` for CJS files.

```json
// package.json
{
  "name": "my-pkg",
  "type": "module"
}
```

> **Gotcha — extensions are required in ESM.** `import "./math"` fails. Write `import "./math.js"`. Node will not silently add extensions like CJS does.

> **Gotcha — `__dirname` and `__filename` don't exist in ESM.** Recreate them:

```js
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";
const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
```

### `import.meta`

```js
// Replaces several CJS conveniences
console.log(import.meta.url);          // file:///C:/.../app.mjs
import.meta.resolve("./math.mjs");     // resolve a path like require.resolve
```

### Dynamic imports

```js
// Works in BOTH CJS and ESM — returns a Promise
const lodash = await import("lodash");
console.log(lodash.default.shuffle([1,2,3]));

if (process.env.HEAVY === "1") {
  const { runHeavy } = await import("./heavy.mjs");
  await runHeavy();
}
```

---

## IV. MODULE RESOLUTION — HOW NODE FINDS A FILE

When you write `require("foo")` or `import "foo"`, Node walks an algorithm:

1. **Core module?** (`node:fs`, `node:http`, `fs`, `http`, ...) — return it.
2. **Path** starts with `./`, `../`, or `/`? Resolve relative.
   - Try the path as a file: `path`, `path.js`, `path.cjs`, `path.mjs`, `path/index.js` (CJS), or with the exact extension (ESM).
3. **Bare specifier** (`"express"`)? Walk up `node_modules`:
   - `./node_modules/express`, then `../node_modules/express`, then `../../node_modules/express`, etc., until root.
4. Inside a found package directory, consult `package.json`:
   - `"exports"` field (modern, restrictive) — wins if present.
   - `"main"` field (legacy default entry).
   - `"module"` field (some bundlers use it for ESM).
5. **Subpath imports** in your own package: `"#config"` → mapped via `"imports"` field.

### The `exports` map — a concrete example

```json
{
  "name": "my-lib",
  "type": "module",
  "exports": {
    ".":          { "import": "./dist/index.mjs", "require": "./dist/index.cjs" },
    "./utils":    { "import": "./dist/utils.mjs", "require": "./dist/utils.cjs" },
    "./package.json": "./package.json"
  }
}
```

Now consumers can `import "my-lib"` (gets the right file for their module system) and `import "my-lib/utils"`, but they **cannot** import `my-lib/internal/private.js` — the exports map *blocks* deep imports. That is the modern way to ship a library.

> **Gotcha — `exports` blocks deep imports.** A package with `"exports"` only exposes what's listed. If a tutorial says `import x from "lib/dist/internal"` and it 404s, the package locked it down deliberately.

### Tip — CommonJS interop with default exports

```js
// CJS module exports a function as the default
// legacy.cjs:  module.exports = function () { ... }

// ESM importer:
import legacy from "./legacy.cjs";   // legacy IS the function
```

When a CJS module uses `module.exports = { default: X }`, you may have to do `import x from "..."` and grab `x.default`. It varies; modern bundlers smooth it over.

---

## V. CHOOSING A MODULE SYSTEM TODAY

| Criterion | CommonJS | ESM |
|-----------|----------|-----|
| Standard | Node-only | Yes (browsers + Node) |
| Syntax | `require` / `module.exports` | `import` / `export` |
| Loading | Synchronous | Async (static + dynamic) |
| Top-level await | ❌ | ✅ |
| Tree-shaking by bundlers | Limited | ✅ |
| `__dirname` / `__filename` | Built-in | Derive from `import.meta.url` |
| Extensions on import | Optional | Required |
| Mature ecosystem | Most legacy code | Most new code |

> **Recommendation for new projects:** **ESM** unless you have a specific reason to stay on CJS (e.g. you publish a library that must support old runtimes). Set `"type": "module"`, write modern code, add a build step if you need to publish a dual-format package.

---

## VI. `package.json` — THE TRUE OWNER OF YOUR PROJECT

`package.json` is the manifest. Every Node project has one. Here is a tour with annotations:

```json
{
  "name": "my-api",
  "version": "1.0.0",
  "description": "A delightful Express API",
  "type": "module",
  "main": "src/index.js",
  "exports": {
    ".": "./src/index.js"
  },
  "imports": {
    "#config": "./src/config/index.js"
  },
  "bin": {
    "my-api": "./bin/cli.js"
  },
  "engines": {
    "node": ">=20.0.0"
  },
  "scripts": {
    "dev":   "node --watch src/index.js",
    "start": "node src/index.js",
    "test":  "jest",
    "lint":  "eslint .",
    "build": "tsc -p .",
    "preinstall":  "echo 'before install'",
    "postinstall": "echo 'after install'"
  },
  "dependencies": {
    "express": "^4.19.2"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "eslint": "^9.0.0"
  },
  "peerDependencies": {
    "react": ">=18"
  },
  "optionalDependencies": {
    "fsevents": "^2.3.0"
  },
  "files": [
    "dist/",
    "README.md"
  ],
  "keywords": ["express", "api"],
  "license": "MIT",
  "author": "Your Name <you@example.com>",
  "repository": {
    "type": "git",
    "url": "https://github.com/you/my-api.git"
  }
}
```

### Field crash course

| Field | Meaning |
|-------|---------|
| `name`, `version` | Identity in the registry. `version` follows semver. |
| `type` | `"module"` makes `.js` ESM; default is CJS. |
| `main` | Legacy entry point. |
| `exports` | Modern entry map; **wins over `main`**; can block deep imports. |
| `imports` | Subpath imports inside your own package (`#config`). |
| `bin` | Maps a command to a script — installed into `node_modules/.bin`. |
| `engines` | Hint about supported Node versions. |
| `scripts` | Named commands runnable with `npm run`. |
| `dependencies` | Required at runtime. Installed with `npm install`. |
| `devDependencies` | Required only for development (testing, linting, building). |
| `peerDependencies` | "Bring your own" — declares a version range a host app must provide. |
| `optionalDependencies` | Installed if possible, but failure is fine. |
| `files` | Whitelist of what gets published to npm. |
| `private: true` | Prevents accidental publish. |

> **Gotcha — `exports` wins.** If both `main` and `exports` exist, modern Node uses `exports`. Forgetting to add an entry to `exports` is the #1 reason "my package's submodule cannot be found."

---

## VII. SEMVER — VERSIONS WITH MEANING

Semantic versioning: `MAJOR.MINOR.PATCH`.

- **MAJOR** — breaking changes (`5.0.0` → `6.0.0`).
- **MINOR** — new, backward-compatible features (`5.2.0` → `5.3.0`).
- **PATCH** — backward-compatible bug fixes (`5.2.3` → `5.2.4`).
- Pre-release: `2.0.0-beta.1`, `2.0.0-rc.4`.

Range operators in your `package.json`:

| Range | Allows | Effective range for `1.2.3` |
|-------|--------|------------------------------|
| `1.2.3` | Exact | `=1.2.3` |
| `^1.2.3` | Compatible (no MAJOR bump) | `>=1.2.3 <2.0.0` |
| `~1.2.3` | Patch-level (no MINOR bump) | `>=1.2.3 <1.3.0` |
| `>=1.2.3` | Greater or equal | `>=1.2.3` |
| `1.x` | Any 1.* | `>=1.0.0 <2.0.0` |
| `*` | Anything | DON'T |
| `1.2.3 - 1.5.0` | Range | inclusive |
| `1.2.3 \|\| ^2.0.0` | OR | union |

> **Caret quirk for `0.x`:** `^0.2.3` means `>=0.2.3 <0.3.0`. With pre-1.0 packages, even minor bumps may break.

### `package-lock.json` — the actual installed graph

`package.json` lists *ranges*. `package-lock.json` records the *exact* version of every direct and transitive dependency. **Commit it.** It is what makes installs reproducible.

```bash
npm install                # respects package.json + updates lockfile if needed
npm ci                     # CI-friendly install — uses lockfile, fails on mismatch
npm install lodash         # add and lock
npm install -D jest        # add as devDependency
npm install -E react@18.2  # exact version (no caret)
npm uninstall lodash       # remove
npm update                 # bump within ranges
npm outdated               # what could be upgraded
npm audit                  # vulnerability scan
npm audit fix              # auto-bump within range
npm audit fix --force      # may bump majors — read the diff
```

> **Rule:** `npm install` is for development. `npm ci` is for CI/CD and Dockerfiles — it is faster, deterministic, and won't silently mutate the lockfile.

---

## VIII. NPM SCRIPTS — YOUR PROJECT'S COMMANDS

```json
"scripts": {
  "dev":   "node --watch src/index.js",
  "build": "tsc -p .",
  "start": "node dist/index.js",
  "test":  "jest --coverage",
  "lint":  "eslint .",
  "format": "prettier --write .",
  "ci":    "npm run lint && npm test && npm run build"
}
```

```bash
npm run dev          # explicit
npm test             # built-in alias for "test"
npm start            # built-in alias for "start"
npm run             # list all scripts
```

### Lifecycle hooks

`pre*` and `post*` hooks run automatically:

```json
"scripts": {
  "build": "tsc",
  "prebuild": "rimraf dist",     // runs before "build"
  "postbuild": "node scripts/copy-static.js"
}
```

Some hooks are special: `preinstall`, `postinstall`, `prepare` (runs before publish and after install), and `prepublishOnly` (runs only before `npm publish`).

> **Security note — postinstall is a footgun.** Malicious packages exploit `postinstall` to run arbitrary code on developer machines. `npm install --ignore-scripts` disables them, and `npm config set ignore-scripts true` makes that the default if you trust nobody.

---

## IX. NPX — RUN BINARIES WITHOUT INSTALLING GLOBALLY

```bash
npx create-react-app my-app    # downloads, runs, removes
npx eslint .                   # uses the local node_modules/.bin/eslint if present
npx -y -p some-pkg some-bin    # specify a package different from the binary name
```

`npx` bridges "run the local binary" and "run a package I don't have installed." Most modern scaffolding tools assume you'll use it.

---

## X. DEPENDENCIES, DEV DEPENDENCIES, AND PEER DEPS — IN PRACTICE

| Type | When to use | Installed by users? |
|------|-------------|---------------------|
| `dependencies` | Code that runs in production | ✅ |
| `devDependencies` | Tests, lint, build tools, types | ❌ if `--production` / `NODE_ENV=production` |
| `peerDependencies` | Plugins that piggyback on a host (e.g. an Express plugin) | App must install themselves |
| `optionalDependencies` | "Nice to have" (platform-specific binaries) | Failure is silent |

> **Tip:** When in doubt, put it in `dependencies`. When you're sure it's only for dev (TypeScript, Jest, ESLint), use `devDependencies`. Users who run `npm ci --omit=dev` (or in production Docker images) will skip them.

---

## XI. PUBLISHING A PACKAGE — THE 90-SECOND VERSION

```bash
# 1. Make sure you have an npm account
npm adduser

# 2. In your package, set the right files and bump the version
npm version patch        # 1.0.0 -> 1.0.1
npm version minor        # 1.0.1 -> 1.1.0
npm version major        # 1.1.0 -> 2.0.0

# 3. Pack and inspect what will be published — VERY useful
npm pack --dry-run

# 4. Publish (use a scoped name like @you/pkg if it's private/personal)
npm publish              # public
npm publish --access public   # required first time on a scoped public package

# 5. Deprecate a buggy version
npm deprecate my-pkg@1.0.1 "Use 1.0.2"
```

Use the **`files`** field (or a `.npmignore`) to ship exactly what's needed and nothing else (no tests, no source maps, no `.env`).

> **Common mistake:** publishing your `src/` and forgetting `dist/`. Always `npm pack --dry-run` first.

---

## XII. WORKSPACES & MONOREPOS

A **monorepo** keeps multiple packages in one repo, sharing dependencies and tooling. npm has built-in workspaces:

```json
// repo root package.json
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": ["packages/*", "apps/*"]
}
```

```
my-monorepo/
├── package.json
├── packages/
│   ├── ui/         (its own package.json)
│   └── core/
└── apps/
    └── web/        (depends on packages/ui)
```

```bash
npm install                  # one install at the root, hoisted node_modules
npm run -w apps/web dev      # run "dev" in a specific workspace
npm install lodash -w packages/core
```

For larger monorepos, use **pnpm workspaces** (faster, content-addressable store), **Yarn**, **Turborepo**, or **Nx**. Yarn/pnpm tend to win for big graphs; pnpm's strictness catches phantom dependencies.

---

## XIII. ALTERNATIVE PACKAGE MANAGERS

| Tool | One-line description |
|------|----------------------|
| **npm** | The default. Fine for most projects. |
| **pnpm** | Fast, disk-efficient, strict. Symlinks per package — no phantom deps. |
| **yarn** (modern Berry / classic) | Workspaces, plug'n'play, fast. Two flavors live in the wild. |
| **bun** | New runtime + package manager. Very fast installs; not 1:1 npm-compatible everywhere. |

You can swap most of them in: `pnpm install`, `yarn`, `bun install`. Lockfiles differ — pick one per repo.

---

## XIV. SECURITY HYGIENE FOR DEPENDENCIES

- Check `npm audit` regularly; treat **high/critical** as bugs.
- Use **Dependabot** / **Renovate** to PR upgrades.
- Pin majors via `^x.y.z` (default), and **commit the lockfile**.
- Avoid weird, low-download packages — typosquatting is real (`lodahs`, `expresss`).
- Limit `postinstall` scripts in CI: `npm ci --ignore-scripts` for sensitive jobs.
- Don't `npm install -g` for project-local needs — use `npx` or a devDependency.
- Don't commit `node_modules/`; do commit `package-lock.json`.

```bash
# Good Docker base for a Node service:
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --ignore-scripts
```

---

## XV. A COMPLETE LITTLE EXAMPLE — TWO-FILE PACKAGE

```json
// package.json
{
  "name": "greet",
  "version": "1.0.0",
  "type": "module",
  "main": "src/index.js",
  "exports": { ".": "./src/index.js" },
  "scripts": { "test": "node --test" },
  "engines": { "node": ">=20" }
}
```

```js
// src/index.js
export function greet(name = "world") {
  return `Hello, ${name}!`;
}
```

```js
// test/greet.test.js
import test from "node:test";
import assert from "node:assert";
import { greet } from "../src/index.js";

test("greets the world by default", () => assert.equal(greet(), "Hello, world!"));
test("greets a name",                 () => assert.equal(greet("Ada"), "Hello, Ada!"));
```

```bash
npm test
# ✔ greets the world by default
# ✔ greets a name
```

That is a publishable package with tests in fewer than 30 lines.

---

## XVI. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Reassigning `exports` in CJS | Importer gets `{}` | Use `module.exports = ...` |
| Forgetting `.js` extension in ESM | "Cannot find module" | Always include extensions in ESM |
| Missing `"type": "module"` | `Unexpected token 'export'` | Add it or rename to `.mjs` |
| Using `__dirname` in ESM | `__dirname is not defined` | Derive from `import.meta.url` |
| `exports` map missing a path | Submodule 404 from your package | Add it to `exports` |
| Committing `node_modules` | Huge repo, bad PRs | `.gitignore node_modules` |
| Not committing `package-lock.json` | Non-reproducible builds | Always commit it |
| `npm install` in CI | Slow & non-deterministic | `npm ci` |
| Trusting `*` ranges | Surprise major bumps | Use `^` (default) and lockfile |
| `postinstall` scripts from random packages | Supply-chain risk | `--ignore-scripts` for sensitive runs |
| Globally installing project tools | "Works on my machine" | Use devDependencies + `npx` |
| Dual CJS/ESM publishing without testing | Importers get the wrong file | Use `exports` conditional map; test both consumers |
| Caret on a `0.x` dep | Breakage on minor bump | Pin or read the changelog |

---

## 🧠 KEY TAKEAWAYS

- Node has **two module systems**: CJS (`require`/`module.exports`, sync) and ESM (`import`/`export`, standard, async, top-level await).
- ESM requires **extensions**, has **`import.meta`**, and lacks `__dirname`/`__filename` — derive them from `import.meta.url`.
- **Module resolution** walks core → relative → `node_modules`, then consults the package's `exports` (or legacy `main`).
- `package.json` is the manifest; `dependencies` vs `devDependencies` vs `peerDependencies` matter; **`exports` wins over `main`**.
- **Semver**: `^` for compatible upgrades, `~` for patch only; commit `package-lock.json`; use `npm ci` in CI.
- npm scripts are your project's command palette; understand `pre`/`post` hooks and the `postinstall` security risk.
- For monorepos, npm/pnpm/yarn workspaces; for new projects, **prefer ESM** and modern tooling.

---

**Prev:** [`01-The-Nodejs-Runtime.md`](./01-The-Nodejs-Runtime.md) · **Next:** [`03-Core-Modules-And-Async.md`](./03-Core-Modules-And-Async.md) · **Index:** [`00-Index.md`](./00-Index.md)
