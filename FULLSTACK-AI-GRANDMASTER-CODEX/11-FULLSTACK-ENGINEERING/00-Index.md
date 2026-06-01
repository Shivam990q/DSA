# 🏗️ Full-Stack Engineering

> *"Anyone can make code that runs. An engineer makes code that survives — under load, under attack, under change, under a pager at 3 a.m. This section is where the coder becomes the engineer."*

> **Section 11 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module covers everything *beyond* writing features: the auth, security, testing, version control, containers, pipelines, deployment, system design, API craft, and observability that turn an app into a product and a developer into a professional.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- **Authentication & authorization, deeply**: sessions vs JWT, access/refresh tokens, OAuth2 & OpenID Connect, SSO, RBAC vs ABAC, password hashing (bcrypt/argon2), MFA/TOTP, and the cookie flags that keep it all safe
- **Web security**: the OWASP Top 10 end to end — XSS, CSRF, SQL/NoSQL injection, CORS, CSP, HTTPS/TLS, secrets management, security headers, rate limiting, dependency hygiene
- **Testing strategy**: the pyramid and the trophy, unit/integration/e2e, TDD, mocking/stubbing/spies, coverage that means something, Jest/Vitest, Supertest, Playwright/Cypress — and what *not* to test
- **Git & collaboration**: the real Git mental model, branching strategies (Git Flow, GitHub Flow, trunk-based), pull requests, code review, conventional commits, conflict resolution, tags & releases
- **Containers**: what containers really are vs VMs, images & layers, Dockerfiles (incl. multi-stage), volumes & networks, Compose for multi-service apps, image optimization, and a Kubernetes concepts primer
- **CI/CD & deployment**: pipelines, GitHub Actions, build→test→deploy automation, deployment targets (PaaS/VPS/serverless/containers), environments, blue-green & canary, CDN/DNS/load balancing, rollbacks
- **System design**: the interview framework, scalability, load balancing, caching everywhere, databases at scale (replication/sharding/partitioning), message queues, monolith vs microservices, CAP & consistency, worked designs
- **API design & observability**: REST done right, GraphQL, gRPC, WebSockets/SSE, versioning, pagination, rate limiting, idempotency, gateways — then logging, metrics (RED/USE), tracing, monitoring, alerting, SLIs/SLOs

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Files build on each other but each stands alone as a reference. The ⭐ files are the highest-leverage — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here — overview, the complete roadmap checklist, references | — |
| 01 | [`01-Authentication-And-Authorization.md`](./01-Authentication-And-Authorization.md) | Sessions vs JWT, access/refresh tokens, OAuth2/OIDC, SSO, RBAC/ABAC, bcrypt/argon2, MFA/TOTP, cookie security, auth vulnerabilities | ⭐ |
| 02 | [`02-Web-Security.md`](./02-Web-Security.md) | OWASP Top 10, XSS, CSRF, SQL/NoSQL injection, CORS, CSP, HTTPS/TLS, secrets, security headers, rate limiting, dependency security | ⭐ |
| 03 | [`03-Testing-Strategies.md`](./03-Testing-Strategies.md) | Pyramid/trophy, unit/integration/e2e, TDD, mocks/stubs/spies, coverage, Jest/Vitest, Supertest, Playwright/Cypress, what not to test | ⭐ |
| 04 | [`04-Git-And-Collaboration.md`](./04-Git-And-Collaboration.md) | Git model, merge vs rebase, branching strategies, PRs & code review, conventional commits, conflicts, `.gitignore`, tags/releases | Core |
| 05 | [`05-Docker-And-Containers.md`](./05-Docker-And-Containers.md) | Containers vs VMs, images/layers, Dockerfile + multi-stage, volumes/networks, Compose, `.dockerignore`, optimization, Kubernetes intro | ⭐ |
| 06 | [`06-CICD-And-Deployment.md`](./06-CICD-And-Deployment.md) | CI/CD concepts, GitHub Actions, build→test→deploy, deployment targets, environments, blue-green/canary, CDN/DNS/LB, rollbacks | ⭐ |
| 07 | [`07-System-Design-Fundamentals.md`](./07-System-Design-Fundamentals.md) | The interview framework, scalability, load balancing, caching, replication/sharding, queues, monolith vs microservices, CAP, worked designs | ⭐ |
| 08 | [`08-API-Design-And-Observability.md`](./08-API-Design-And-Observability.md) | REST/GraphQL/gRPC/WebSockets, versioning, pagination, rate limiting, idempotency, gateways; logging, metrics, tracing, monitoring, SLIs/SLOs | ⭐ |

---

## 🗺️ COMPLETE FULL-STACK ENGINEERING ROADMAP (coverage checklist)

> This is the **roadmap.sh-style master checklist**. Every skill that turns a coder into a professional engineer maps to a file below. If you can check every box, you have complete coverage of this section's domain — nothing left out. The **→ `NN`** marks the file where each concept is taught.

### 1 — Authentication & Authorization → `01`
- [x] Authentication vs authorization (who you are vs what you may do) → `01`
- [x] **Stateful sessions** (session IDs, server-side stores, `express-session`) → `01`
- [x] **Stateless JWT** (header.payload.signature, signing & verifying) → `01`
- [x] Sessions vs JWT tradeoffs (revocation, scale, size, XSS/CSRF surface) → `01`
- [x] **Access tokens vs refresh tokens** & rotation, reuse detection → `01`
- [x] Token storage: cookies vs `localStorage` (and why it matters) → `01`
- [x] **OAuth2** roles, grant types, the **Authorization Code + PKCE** flow → `01`
- [x] **OpenID Connect** (ID tokens, `/userinfo`, OAuth2 vs OIDC) → `01`
- [x] **SSO** (Single Sign-On), SAML vs OIDC, identity providers → `01`
- [x] **RBAC** (roles/permissions) vs **ABAC** (attribute/policy-based) → `01`
- [x] **Password hashing** with bcrypt & argon2 (salt, cost, peppering) → `01`
- [x] **MFA / 2FA** and **TOTP** (authenticator apps, recovery codes) → `01`
- [x] **Cookie security** (`HttpOnly`, `Secure`, `SameSite`, `Domain`, `Path`) → `01`
- [x] Common auth vulnerabilities (fixation, weak JWT, `alg:none`, IDOR) → `01`

### 2 — Web Security → `02`
- [x] The **OWASP Top 10** walkthrough (2021), mapped to defenses → `02`
- [x] **XSS** — stored, reflected, DOM-based; output encoding & CSP → `02`
- [x] **CSRF** — synchronizer tokens, double-submit, `SameSite` → `02`
- [x] **SQL injection** & **NoSQL injection** — parameterization → `02`
- [x] Command injection, SSRF, path traversal (injection family) → `02`
- [x] **CORS** deeply (origins, preflight, credentials, common mistakes) → `02`
- [x] **Content Security Policy** (directives, nonces, report-only) → `02`
- [x] **HTTPS / TLS** (handshake, certs, HSTS, redirect to HTTPS) → `02`
- [x] **Security headers** (helmet, X-Frame-Options, X-Content-Type-Options) → `02`
- [x] **Secrets management** (env, vaults, never commit, rotation) → `02`
- [x] **Rate limiting** & brute-force / credential-stuffing defense → `02`
- [x] **Dependency security** (audit, SCA, lockfiles, supply chain) → `02`
- [x] Authentication & access-control failures, secure defaults → `02`

### 3 — Testing Strategies → `03`
- [x] Why we test; the cost-of-a-bug curve → `03`
- [x] The **testing pyramid** & the **testing trophy** → `03`
- [x] **Unit tests** (pure functions, fast, isolated) → `03`
- [x] **Integration tests** (modules + real-ish deps, DB, HTTP) → `03`
- [x] **End-to-end tests** (full stack through the browser) → `03`
- [x] **TDD** — red/green/refactor → `03`
- [x] **Test doubles** — mocks, stubs, spies, fakes, dummies → `03`
- [x] **Coverage** (line/branch/function) and its limits → `03`
- [x] **Jest / Vitest** (matchers, lifecycle, async, snapshots) → `03`
- [x] **Supertest** (HTTP/API integration testing) → `03`
- [x] **Playwright / Cypress** (browser e2e) → `03`
- [x] Arrange-Act-Assert, naming, fixtures, factories → `03`
- [x] Flaky tests, test isolation, parallelism, CI integration → `03`
- [x] **What NOT to test** (framework code, getters, over-mocking) → `03`

### 4 — Git & Collaboration → `04`
- [x] Git's model (snapshots, the three trees, the DAG, SHAs) → `04`
- [x] Core workflow (`add`/`commit`/`status`/`log`/`diff`) → `04`
- [x] **Branches** & HEAD; fast-forward vs 3-way merge → `04`
- [x] **Merge vs rebase** (and the golden rule of rebase) → `04`
- [x] **Branching strategies** — Git Flow, GitHub Flow, trunk-based → `04`
- [x] **Pull requests** & the **code review** craft → `04`
- [x] **Conventional commits** & semantic release → `04`
- [x] **Resolving conflicts** (and avoiding them) → `04`
- [x] `.gitignore`, `.gitattributes`, large files (LFS) → `04`
- [x] **Tags & releases**, semantic versioning in practice → `04`
- [x] Undo toolkit (`reset`, `revert`, `restore`, `reflog`, `stash`, `cherry-pick`) → `04`
- [x] Working in teams (forks, remotes, hooks, signed commits) → `04`

### 5 — Docker & Containers → `05`
- [x] What a container is; **containers vs VMs** → `05`
- [x] Images, **layers**, the union filesystem, tags & registries → `05`
- [x] **Dockerfile** (FROM/RUN/COPY/CMD/ENTRYPOINT/EXPOSE/ENV/ARG) → `05`
- [x] `docker build` / `run` / `ps` / `logs` / `exec` essentials → `05`
- [x] **Multi-stage builds** (small, secure production images) → `05`
- [x] **Volumes** (persistence) & bind mounts → `05`
- [x] **Networks** (bridge, container-to-container DNS) → `05`
- [x] **docker-compose** for multi-service apps → `05`
- [x] `.dockerignore` & build context hygiene → `05`
- [x] **Image optimization** (base image, caching, distroless, non-root) → `05`
- [x] **Kubernetes concepts intro** (pods, services, deployments, ingress) → `05`

### 6 — CI/CD & Deployment → `06`
- [x] **Continuous Integration / Delivery / Deployment** defined → `06`
- [x] Pipeline anatomy (stages: build → test → scan → deploy) → `06`
- [x] **GitHub Actions** (workflows, jobs, steps, runners, triggers) → `06`
- [x] **Secrets** in CI & OIDC to cloud (no long-lived keys) → `06`
- [x] Caching, matrices, artifacts, reusable workflows → `06`
- [x] **Deployment targets** — PaaS, VPS, serverless, containers → `06`
- [x] **Environments** (dev/staging/prod), promotion, config per env → `06`
- [x] **Blue-green** & **canary** releases, feature flags → `06`
- [x] **CDN, DNS, load balancing** in deployment → `06`
- [x] **Environment config** (12-factor) & build-time vs run-time → `06`
- [x] **Rollbacks**, health gates, migrations in pipelines → `06`

### 7 — System Design → `07`
- [x] The **system design interview framework** (requirements → estimate → API → data → scale) → `07`
- [x] **Scalability** — vertical vs horizontal, statelessness → `07`
- [x] **Load balancing** (L4/L7, algorithms, health checks) → `07`
- [x] **Caching** everywhere (client/CDN/app/DB, Redis, strategies, eviction) → `07`
- [x] **Databases at scale** — replication, sharding, partitioning, indexing → `07`
- [x] SQL vs NoSQL selection at scale → `07`
- [x] **Message queues** & streams (Kafka, RabbitMQ, SQS), async patterns → `07`
- [x] **Monolith vs microservices** (and the modular monolith) → `07`
- [x] **CAP theorem**, consistency models, eventual consistency → `07`
- [x] Back-of-the-envelope estimation, numbers every engineer knows → `07`
- [x] Worked designs: **URL shortener**, **news feed**, rate limiter → `07`

### 8 — API Design & Observability → `08`
- [x] **REST** maturity (Richardson), resource design, status codes → `08`
- [x] **Pagination** (offset vs cursor), filtering, sorting → `08`
- [x] **API versioning** (URL, header, media type) → `08`
- [x] **Idempotency** (keys, safe retries) → `08`
- [x] **Rate limiting** algorithms (token/leaky bucket, windows) → `08`
- [x] **GraphQL** (schema, resolvers, N+1, when to use) → `08`
- [x] **gRPC** & Protocol Buffers (when binary RPC wins) → `08`
- [x] **WebSockets** & **SSE** (real-time choices) → `08`
- [x] **API gateways** & BFF (backend-for-frontend) → `08`
- [x] **Structured logging** (levels, correlation IDs, JSON logs) → `08`
- [x] **Metrics** — the **RED** & **USE** methods, Prometheus model → `08`
- [x] **Distributed tracing** (spans, context propagation, OpenTelemetry) → `08`
- [x] **Monitoring & alerting**, **SLIs/SLOs/SLAs**, error budgets → `08`
- [x] **Health checks** (liveness vs readiness) → `08`

> **Coverage promise:** Every box above is taught with runnable code or config inside this section. Where a topic is *developed in depth elsewhere* (e.g., Node/Express auth wiring in [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/00-Index.md), SQL internals in [`08-SQL-DATABASES`](../08-SQL-DATABASES/00-Index.md)), the file links across so you never hit a dead end.

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Build a "production-grade" version of one app.** Take an API from [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/00-Index.md) and harden it chapter by chapter: add auth (01), lock it down (02), test it (03), version-control it well (04), containerize it (05), ship it via a pipeline (06), and instrument it (08).
2. **Treat security as non-negotiable.** Files 01 and 02 are flagged ⚠️ throughout. Read those callouts as if a code reviewer wrote them — because in production, one will.
3. **Run the configs.** Dockerfiles, Compose files, and GitHub Actions YAML are all runnable. Spin them up locally. Break the pipeline on purpose and read the failure.
4. **Design before the interview.** File 07 gives you a repeatable framework. Practice it out loud on the worked examples until the structure is automatic.
5. **Think in tradeoffs.** Every choice here (sessions vs JWT, monolith vs microservices, merge vs rebase) is a tradeoff, not a winner. Learn the *axes*, not the dogma.

---

## 🔗 RELATED SECTIONS

- **The app you harden:** [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/00-Index.md) — auth, middleware, and Docker basics are introduced there and deepened here.
- **The data layer at scale:** [`08-SQL-DATABASES`](../08-SQL-DATABASES/00-Index.md) and [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/00-Index.md) — replication, sharding, and injection defenses connect to files 02 and 07.
- **The frontend you protect:** [`05-REACT`](../05-REACT/00-Index.md) and [`06-NEXTJS`](../06-NEXTJS/00-Index.md) — XSS, CSP, CORS, and token storage all land in the browser.
- **The language & types:** [`02-JAVASCRIPT-MASTERY`](../02-JAVASCRIPT-MASTERY/00-Index.md), [`03-TYPESCRIPT`](../03-TYPESCRIPT/00-Index.md).
- **Philosophy & roadmap:** [`00-ROADMAP-AND-PHILOSOPHY`](../00-ROADMAP-AND-PHILOSOPHY/00-Index.md).

---

## 📎 DEEP REFERENCES (authoritative sources)

- **OWASP Top 10** — [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/)
- **OWASP Cheat Sheet Series** — [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/) (auth, session, CSRF, JWT, password storage)
- **The Twelve-Factor App** — [12factor.net](https://12factor.net/) (config, build/release/run, logs, disposability)
- **OAuth 2.0** — [oauth.net/2](https://oauth.net/2/) · **OpenID Connect** — [openid.net/connect](https://openid.net/developers/how-connect-works/)
- **JWT** — [jwt.io](https://jwt.io/) and RFC 7519
- **Docker docs** — [docs.docker.com](https://docs.docker.com/) · **Dockerfile best practices** — [docs.docker.com/build/building/best-practices](https://docs.docker.com/build/building/best-practices/)
- **Kubernetes concepts** — [kubernetes.io/docs/concepts](https://kubernetes.io/docs/concepts/)
- **GitHub Actions docs** — [docs.github.com/actions](https://docs.github.com/en/actions)
- **Pro Git book (free)** — [git-scm.com/book](https://git-scm.com/book/en/v2)
- **Conventional Commits** — [conventionalcommits.org](https://www.conventionalcommits.org/) · **SemVer** — [semver.org](https://semver.org/)
- **Google SRE Books (free)** — [sre.google/books](https://sre.google/books/) (SLIs/SLOs, error budgets, monitoring)
- **The RED method** — Tom Wilkie · **The USE method** — Brendan Gregg ([brendangregg.com/usemethod.html](https://www.brendangregg.com/usemethod.html))
- **OpenTelemetry** — [opentelemetry.io/docs](https://opentelemetry.io/docs/)
- **System Design Primer** — [github.com/donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer)
- **Testing best practices (community)** — [github.com/goldbergyoni/javascript-testing-best-practices](https://github.com/goldbergyoni/javascript-testing-best-practices)

---

**→ Begin:** [`01-Authentication-And-Authorization.md`](./01-Authentication-And-Authorization.md) | Back to [`../README.md`](../README.md)
