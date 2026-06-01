# 🧪 03 — Testing Strategies

> *"Tests are not about proving you're right. They're about giving you the courage to change code without fear — and the speed to know in seconds, not in production."*

**Prev:** [`02-Web-Security.md`](./02-Web-Security.md) · **Next:** [`04-Git-And-Collaboration.md`](./04-Git-And-Collaboration.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHY WE TEST — THE COST-OF-A-BUG CURVE

A bug's cost grows by orders of magnitude the later it's found:

```
Caught while typing (test)   →  ~seconds, ~$1
Caught in code review        →  minutes
Caught in CI                 →  minutes–hours
Caught in QA / staging       →  hours–days
Caught in PRODUCTION         →  outage, data loss, reputation, $$$$$
```

Tests are a machine that pushes detection as far left as possible. But they buy more than bug-catching:

- **Confidence to refactor** — change internals freely; green tests say behavior held.
- **Living documentation** — a test shows exactly how code is meant to be used.
- **Design pressure** — code that's hard to test is usually badly coupled. Tests expose that early.
- **Regression safety** — a fixed bug gets a test so it can never silently return.

> **The real goal isn't coverage — it's confidence.** A test suite is good if, when it's green, you'd deploy without anxiety, and when it's red, it's because something *actually* broke.

---

## II. THE PYRAMID vs THE TROPHY

How should tests be distributed across levels? Two influential models:

```
   TESTING PYRAMID (Mike Cohn)          TESTING TROPHY (Kent C. Dodds)

         /\   E2E (few, slow)                  ___  E2E
        /  \                                   |  |
       /----\  Integration                   /----\  Integration  ← the bulk
      /      \                               |      |
     /--------\  Unit (many, fast)           \------/  Unit
    /__________\                              \____/
                                              ‗‗‗‗  Static (types, lint)
```

- **Pyramid** — *many* fast unit tests, fewer integration, *very few* slow e2e. Classic, optimizes for speed and isolation.
- **Trophy** — emphasizes **integration** tests (the best ROI for most apps) on a base of **static analysis** (TypeScript, ESLint), because they catch real-world bugs that isolated units miss.

| Level | Speed | Confidence | Cost to write/maintain | How many |
|-------|-------|-----------|------------------------|----------|
| Static (types/lint) | Instant | Low-ish (per bug) | Tiny | Everything |
| Unit | Milliseconds | Low (isolated) | Low | Many |
| Integration | 10s–100s ms | **High** | Medium | A lot |
| E2E | Seconds | **Highest** | High (flaky, slow) | Few, critical paths |

> **The unifying rule (Dodds):** *"Write tests. Not too many. Mostly integration."* Spend your testing budget where each test buys the most confidence per millisecond — usually integration. Don't dogmatically chase a shape; chase confidence.

---

## III. THE THREE LEVELS

### Unit tests — one piece, in isolation

Test a single function/module with no real I/O. Fast, deterministic, pinpoint failures.

```js
// pure function — the ideal unit-test target
export function slugify(title) {
  return title.toLowerCase().trim().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

// slugify.test.js
import { describe, it, expect } from "vitest";
import { slugify } from "./slugify";

describe("slugify", () => {
  it("lowercases and hyphenates", () => {
    expect(slugify("Hello World")).toBe("hello-world");
  });
  it("strips leading/trailing separators", () => {
    expect(slugify("  Hello!  ")).toBe("hello");
  });
});
```

### Integration tests — pieces working together

Test multiple units plus real-ish dependencies (a test DB, an HTTP layer). Highest confidence-per-effort because they exercise the seams where bugs actually hide.

```js
// Test the route + validation + DB layer together, against a real test database.
import request from "supertest";
import { app } from "../app";
import { db } from "../db";

beforeEach(async () => { await db.migrate.latest(); await db("users").truncate(); });
afterAll(async () => { await db.destroy(); });

describe("POST /users", () => {
  it("creates a user and persists it", async () => {
    const res = await request(app).post("/users").send({ email: "a@b.com", name: "Ada" });
    expect(res.status).toBe(201);
    const row = await db("users").where({ email: "a@b.com" }).first();
    expect(row.name).toBe("Ada");
  });
  it("rejects invalid email with 400", async () => {
    const res = await request(app).post("/users").send({ email: "nope" });
    expect(res.status).toBe(400);
  });
});
```

### End-to-end tests — the whole system, as a user

Drive a real browser through the full stack. Maximum confidence, maximum cost — reserve for critical journeys (login, checkout).

```js
// Playwright — a real user flow through the deployed app
import { test, expect } from "@playwright/test";

test("user can log in and see dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("ada@example.com");
  await page.getByLabel("Password").fill("correct horse");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```

> **Gotcha — don't push logic down to e2e.** E2E tests are slow and flaky; use them for a handful of golden paths. If you're testing every validation rule through the browser, you've inverted the pyramid and your suite will be painfully slow.

---

## IV. TDD — RED, GREEN, REFACTOR

**Test-Driven Development** writes the test *first*, then the code to pass it. A tight three-beat loop:

```
🔴 RED      Write a failing test for the next small behavior.
🟢 GREEN    Write the SIMPLEST code that makes it pass (even if ugly).
🔵 REFACTOR Clean up code AND tests — still green — with no behavior change.
            Repeat.
```

```js
// 🔴 RED — write the test first; it fails (function doesn't exist yet)
import { fizzbuzz } from "./fizzbuzz";
it("returns 'Fizz' for multiples of 3", () => expect(fizzbuzz(3)).toBe("Fizz"));

// 🟢 GREEN — simplest passing implementation
export const fizzbuzz = (n) => (n % 3 === 0 ? "Fizz" : String(n));

// 🔵 REFACTOR — generalize once more tests drive it (5 → Buzz, 15 → FizzBuzz),
//    confident because the tests stay green at each step.
```

**Why it works:** you only write code you need (the test demands it), you get a regression suite for free, and your code is testable by construction. The discipline is hard at first; the payoff is design clarity.

> **Gotcha — TDD is a design tool, not a religion.** It shines for logic with clear inputs/outputs. For exploratory UI or spikes, writing tests first can fight you. Use it where it helps; don't dogmatically force it everywhere.

---

## V. TEST DOUBLES — MOCK, STUB, SPY, FAKE, DUMMY

A **test double** stands in for a real dependency so a test stays fast, deterministic, and isolated. The five types (Gerard Meszaros's taxonomy) are often all lumped as "mocks," but they differ:

| Double | What it does | Use when |
|--------|--------------|----------|
| **Dummy** | Passed but never used (fills a parameter) | Satisfy a signature |
| **Stub** | Returns canned answers | You need a dependency to *return* something |
| **Spy** | A stub that also *records* how it was called | Verify a function was called (and how) |
| **Mock** | Pre-programmed with *expectations*, fails if not met | Assert interactions happened correctly |
| **Fake** | A working but simplified implementation | In-memory DB, fake payment gateway |

```js
import { vi, it, expect } from "vitest";

// STUB — canned return value
const getRate = vi.fn().mockReturnValue(1.1);
expect(convert(100, getRate)).toBe(110);

// SPY — record calls (often on a real object)
const logger = { info: vi.fn() };
doWork(logger);
expect(logger.info).toHaveBeenCalledWith("done");      // spying on the interaction

// MOCK — set an expectation and verify behavior
const mailer = { send: vi.fn().mockResolvedValue(true) };
await registerUser({ email: "a@b.com" }, mailer);
expect(mailer.send).toHaveBeenCalledOnce();             // the interaction is the assertion

// FAKE — a lightweight real implementation
class InMemoryUserRepo {
  #users = new Map();
  async save(u) { this.#users.set(u.id, u); }
  async find(id) { return this.#users.get(id); }
}
```

> **⚠️ Gotcha — over-mocking tests the mocks, not the code.** If you mock everything, you assert that your code calls mocks in a certain order — which proves nothing about real behavior and breaks on every refactor. Prefer real objects and **fakes** over mocks; mock only true boundaries (network, time, payment APIs, randomness).

---

## VI. COVERAGE AND ITS LIMITS

**Code coverage** measures how much code your tests execute.

| Metric | Measures |
|--------|----------|
| **Line** | % of lines run |
| **Branch** | % of `if`/`else`/`?:` paths taken |
| **Function** | % of functions called |
| **Statement** | % of statements executed |

```bash
vitest run --coverage          # generates a coverage report
```

```js
// vitest.config.js — enforce a floor in CI (but read the gotcha)
export default {
  test: {
    coverage: { provider: "v8", thresholds: { lines: 80, branches: 75 }, reporter: ["text", "html"] },
  },
};
```

> **⚠️ Gotcha — 100% coverage ≠ correct.** Coverage tells you what code *ran*, not what was *verified*. This test gives 100% coverage and asserts nothing useful:
> ```js
> it("runs", () => { add(2, 2); });   // executes add(), never checks the result!
> ```
> Coverage finds *untested* code (valuable). It cannot prove *tested* code is correct. Treat ~70–85% as a healthy signal, not a sacred target — chasing 100% breeds brittle, assertion-free tests.

---

## VII. JEST / VITEST — THE TOOLKIT

Jest and Vitest share nearly identical APIs (Vitest is the faster, ESM-native, Vite-friendly option). Core building blocks:

```js
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";

describe("Cart", () => {
  let cart;
  beforeEach(() => { cart = new Cart(); });        // lifecycle: runs before each test
  afterEach(() => { vi.restoreAllMocks(); });       // clean up doubles

  // --- Matchers ---
  it("uses common matchers", () => {
    expect(2 + 2).toBe(4);                  // strict equality (===)
    expect({ a: 1 }).toEqual({ a: 1 });     // deep equality
    expect([1, 2, 3]).toContain(2);
    expect("hello").toMatch(/ell/);
    expect(cart.items).toHaveLength(0);
    expect(() => cart.checkout()).toThrow("Cart is empty");
    expect(0.1 + 0.2).toBeCloseTo(0.3);     // floating-point safe
  });

  // --- Async ---
  it("handles promises", async () => {
    await expect(fetchUser(1)).resolves.toMatchObject({ id: 1 });
    await expect(fetchUser(-1)).rejects.toThrow();
  });

  // --- Mocking time & modules ---
  it("controls time", () => {
    vi.useFakeTimers();
    const cb = vi.fn();
    setTimeout(cb, 1000);
    vi.advanceTimersByTime(1000);           // no real waiting
    expect(cb).toHaveBeenCalled();
    vi.useRealTimers();
  });
});
```

```js
// --- Snapshot testing --- captures output, flags changes on later runs
it("renders the welcome banner", () => {
  expect(renderBanner({ name: "Ada" })).toMatchSnapshot();
});
```

> **Gotcha — snapshots rot.** Huge snapshots get rubber-stamped on update (`-u`) without anyone reading the diff, so they stop catching bugs. Keep snapshots small and intentional; prefer explicit assertions for logic. Snapshots are best for stable serialized output.

---

## VIII. SUPERTEST — TESTING HTTP APIs

Supertest drives your Express/HTTP app in-process (no real port needed), perfect for integration testing endpoints.

```js
import request from "supertest";
import { app } from "../app";

describe("Todo API", () => {
  it("full CRUD lifecycle", async () => {
    // CREATE
    const created = await request(app)
      .post("/todos").send({ title: "Write tests" })
      .expect(201);
    const id = created.body.id;

    // READ
    await request(app).get(`/todos/${id}`).expect(200)
      .expect((res) => expect(res.body.title).toBe("Write tests"));

    // UPDATE
    await request(app).patch(`/todos/${id}`).send({ done: true }).expect(200);

    // DELETE
    await request(app).delete(`/todos/${id}`).expect(204);
    await request(app).get(`/todos/${id}`).expect(404);
  });

  it("requires auth", async () => {
    await request(app).get("/todos").expect(401);                       // no token
    await request(app).get("/todos").set("Authorization", "Bearer x").expect(401); // bad token
  });
});
```

---

## IX. PLAYWRIGHT / CYPRESS — BROWSER E2E

Both automate a real browser. Playwright (multi-browser, fast, auto-waiting) and Cypress (great DX, time-travel debugger) are the leading choices.

```js
// Playwright — resilient selectors + auto-waiting
import { test, expect } from "@playwright/test";

test("checkout flow", async ({ page }) => {
  await page.goto("/products");
  await page.getByRole("button", { name: "Add to cart" }).first().click();
  await page.getByRole("link", { name: "Cart" }).click();
  await page.getByRole("button", { name: "Checkout" }).click();
  await expect(page).toHaveURL(/\/order\/confirmed/);
  await expect(page.getByText("Thank you")).toBeVisible();
});
```

> **Gotcha — select by role/text/test-id, never by CSS class.** Selectors like `.btn-primary.css-1x9z` break the moment a designer tweaks styling. Use `getByRole`, `getByLabel`, or `data-testid` — they reflect user-facing semantics and survive refactors.

| | **Playwright** | **Cypress** |
|---|---|---|
| Browsers | Chromium, Firefox, WebKit | Chromium-family, Firefox |
| Architecture | Out-of-process, parallel | In-browser |
| Speed / parallelism | Faster, native parallel | Slower across many specs |
| Debugging DX | Trace viewer | Time-travel UI |

---

## X. CRAFT — AAA, NAMING, FIXTURES, FACTORIES

**Arrange-Act-Assert** structures every test:

```js
it("applies a 10% discount for members", () => {
  // ARRANGE — set up state & inputs
  const cart = new Cart([{ price: 100 }]);
  const member = { tier: "member" };

  // ACT — perform the one action under test
  const total = cart.totalFor(member);

  // ASSERT — verify the outcome
  expect(total).toBe(90);
});
```

**Naming** — describe behavior, not implementation. `it("returns 404 when the order doesn't exist")` beats `it("test order 2")`.

**Factories** beat hand-built fixtures — generate valid objects with only the relevant field varied:

```js
// A factory keeps tests DRY and intention-revealing
function makeUser(overrides = {}) {
  return { id: crypto.randomUUID(), email: "test@example.com", role: "viewer", ...overrides };
}
it("denies viewers from deleting", () => {
  const user = makeUser({ role: "viewer" });   // only the relevant attribute is explicit
  expect(canDelete(user)).toBe(false);
});
```

---

## XI. FLAKY TESTS, ISOLATION, PARALLELISM, CI

A **flaky test** passes sometimes and fails sometimes with no code change. Flakes are corrosive — people start ignoring red builds.

| Cause of flakiness | Fix |
|--------------------|-----|
| Shared state between tests | Reset/isolate state in `beforeEach` |
| Real time / `setTimeout` | Fake timers; never `sleep()` |
| Real network calls | Mock/stub; or hermetic test server |
| Test order dependence | Each test must set up its own world |
| Fixed waits in e2e | Auto-waiting assertions, not `wait(2000)` |
| Random data / time zones | Seed RNG; freeze the clock |

```js
// ❌ Order-dependent & shared state — flaky
let total = 0;
it("adds", () => { total += 10; expect(total).toBe(10); });   // breaks if another test ran first

// ✅ Isolated — each test owns its state
it("adds", () => { const t = add(0, 10); expect(t).toBe(10); });
```

**Parallelism** makes suites fast but demands isolation (separate DB schemas/transactions per worker). **CI integration** runs the suite on every push/PR and blocks merges on failure:

```yaml
# .github/workflows/test.yml — run tests on every PR (see file 06 for CI depth)
name: test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test -- --coverage
```

> **⚠️ Gotcha — never ignore a flaky test by retrying blindly.** Auto-retries hide real race conditions that *will* bite in production. Quarantine the flake, find the root cause (usually shared state or timing), and fix it. A test you can't trust is worse than no test.

---

## XII. WHAT *NOT* TO TEST

Testing the wrong things wastes time and creates brittle suites that fight every refactor.

| Don't test | Why |
|------------|-----|
| Framework/library internals | React, Express are already tested — trust them |
| Trivial getters/setters | No logic = no risk = no value |
| Implementation details | Test behavior/outputs, not private methods — or every refactor breaks tests |
| Third-party APIs (live) | Mock them; don't depend on the network in unit tests |
| Generated code / config | Not your logic |
| The language itself | `expect(1 + 1).toBe(2)` proves nothing |

> **The test that matters asks "what does this code *promise* to do?" and verifies that promise.** Test behavior and contracts, not internals. If a refactor that preserves behavior breaks your test, the test was coupled to the wrong thing.

---

## XIII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Chasing 100% coverage | Brittle, assertion-free tests | Aim ~70–85%; assert behavior |
| Over-mocking | Tests break on every refactor | Use real objects/fakes; mock only boundaries |
| Testing implementation details | Refactors turn suite red | Test public behavior/outputs |
| Inverted pyramid (too many e2e) | Slow, flaky suite | Push logic to unit/integration |
| `wait(2000)` in e2e | Flaky, slow | Auto-waiting assertions |
| Shared state between tests | Order-dependent flakes | Isolate in `beforeEach` |
| Real time/network in unit tests | Nondeterministic | Fake timers; stub network |
| Giant snapshots | Rubber-stamped, catch nothing | Small, intentional snapshots |
| No CI gate | Broken code merges | Run tests on every PR, block on red |
| Retrying flakes to "fix" them | Hidden race conditions ship | Find & fix the root cause |
| Vague test names | Can't tell what broke | Name the behavior being verified |

---

## 🧠 KEY TAKEAWAYS

- Tests push bug detection **left**, where fixing is cheap — and buy refactoring confidence, documentation, and design feedback.
- Follow **"write tests, not too many, mostly integration."** Choose the shape (pyramid/trophy) that maximizes *confidence per millisecond*, not dogma.
- **Unit** = isolated and fast; **integration** = best ROI; **e2e** = a few critical journeys only.
- **TDD** (red-green-refactor) is a design tool: write the failing test, the simplest passing code, then clean up — use it where it helps.
- Know your **test doubles** (dummy/stub/spy/mock/fake); prefer fakes and real objects, and **mock only true boundaries** to avoid testing the mocks.
- **Coverage finds untested code but never proves correctness** — assert outcomes, target ~70–85%, don't worship 100%.
- Master **Jest/Vitest** (matchers, lifecycle, async, fake timers, snapshots), **Supertest** for APIs, and **Playwright/Cypress** for e2e with role/test-id selectors.
- Structure with **Arrange-Act-Assert**, name by behavior, use **factories**, and run everything in **CI** on every PR.
- **Kill flakiness at the root** (isolation, fake time, no real network) instead of retrying — and **don't test** framework internals, trivial accessors, or implementation details.

---

**Prev:** [`02-Web-Security.md`](./02-Web-Security.md) · **Next:** [`04-Git-And-Collaboration.md`](./04-Git-And-Collaboration.md) · **Index:** [`00-Index.md`](./00-Index.md)
