# 🐳 05 — Docker & Containers

> *"'It works on my machine' is the oldest excuse in software. Containers turn that excuse into a guarantee — your machine, their machine, the server, all running the exact same box."*

**Prev:** [`04-Git-And-Collaboration.md`](./04-Git-And-Collaboration.md) · **Next:** [`06-CICD-And-Deployment.md`](./06-CICD-And-Deployment.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT A CONTAINER ACTUALLY IS — vs A VM

A **container** packages your app with *everything it needs to run* — code, runtime, libraries, system tools — into one portable unit that runs identically anywhere Docker runs. The magic is that it does this *without* shipping a whole operating system.

A **virtual machine** virtualizes *hardware*: each VM runs a full guest OS on top of a hypervisor. A **container** virtualizes the *operating system*: all containers share the host's kernel but are isolated from each other using Linux primitives (**namespaces** for isolation, **cgroups** for resource limits).

```
   VIRTUAL MACHINES                         CONTAINERS
 ┌──────┐ ┌──────┐ ┌──────┐            ┌──────┐ ┌──────┐ ┌──────┐
 │ App  │ │ App  │ │ App  │            │ App  │ │ App  │ │ App  │
 │ Libs │ │ Libs │ │ Libs │            │ Libs │ │ Libs │ │ Libs │
 │GuestOS│ │GuestOS│ │GuestOS│          └──────┘ └──────┘ └──────┘
 └──────┘ └──────┘ └──────┘            ┌──────────────────────────┐
 ┌──────────────────────────┐         │   Docker Engine          │
 │      Hypervisor          │         ├──────────────────────────┤
 ├──────────────────────────┤         │   Host OS (shared kernel)│
 │      Host OS             │         ├──────────────────────────┤
 ├──────────────────────────┤         │      Hardware            │
 │      Hardware           │         └──────────────────────────┘
 └──────────────────────────┘
```

| | **Virtual Machine** | **Container** |
|---|---|---|
| Virtualizes | Hardware | OS (shares host kernel) |
| Size | GBs (full OS) | MBs |
| Startup | Minutes | Milliseconds–seconds |
| Isolation | Strong (separate kernels) | Process-level (namespaces) |
| Overhead | High | Low |
| Density | Few per host | Many per host |

> **Gotcha — containers share the host kernel, so isolation is weaker than a VM's.** A kernel exploit can escape a container in ways it couldn't escape a VM. For hostile multi-tenant workloads, add a sandbox (gVisor, Kata, Firecracker) or use VMs. For *your own* services, container isolation is plenty.

---

## II. IMAGES, LAYERS & THE UNION FILESYSTEM

An **image** is a read-only template — the blueprint. A **container** is a running instance of an image (image : container :: class : object). You build an image once and run many containers from it.

Images are built in **layers**, one per instruction in the Dockerfile. Each layer is a diff stacked on the previous one via a **union filesystem**. Layers are **cached and shared**:

```
Image = stack of read-only layers + a thin writable layer on top (per container)

   ┌─────────────────────────┐  ← writable container layer (ephemeral)
   ├─────────────────────────┤  ← COPY . .            (your code)
   ├─────────────────────────┤  ← RUN npm ci          (dependencies)
   ├─────────────────────────┤  ← COPY package.json
   └─────────────────────────┘  ← FROM node:20-slim   (base image)
```

This is why layer **order matters** (§V optimization): if a layer's inputs haven't changed, Docker reuses the cached layer instead of rebuilding it. Two images from the same base share that base layer on disk — storage and pull bandwidth are saved.

**Tags & registries:** an image is named `registry/repository:tag`, e.g. `docker.io/library/node:20-slim`. A **registry** (Docker Hub, GHCR, ECR) stores and distributes images.

```bash
docker pull node:20-slim          # download an image from a registry
docker images                     # list local images
docker tag myapp:latest ghcr.io/me/myapp:1.2.0
docker push ghcr.io/me/myapp:1.2.0
```

> **⚠️ Gotcha — `latest` is a trap, not a version.** `latest` is just a default tag, not "the newest" — it's whatever was last pushed with that tag. Deploying `:latest` makes builds non-reproducible (you can't tell what's actually running). Pin explicit versions (`myapp:1.2.0`) in production.

---

## III. THE DOCKERFILE

A **Dockerfile** is the recipe for an image. Each instruction creates a layer.

```dockerfile
# FROM — the base image every build starts from (REQUIRED, first instruction)
FROM node:20-slim

# WORKDIR — set the working directory for following instructions (creates it if absent)
WORKDIR /app

# COPY — copy files from build context into the image
COPY package*.json ./

# RUN — execute a command at BUILD time, baking the result into a layer
RUN npm ci --omit=dev

COPY . .

# ENV — set an environment variable available at build AND run time
ENV NODE_ENV=production

# ARG — a build-time-only variable (not present in the running container)
ARG BUILD_VERSION=dev

# EXPOSE — document which port the app listens on (metadata; doesn't publish it)
EXPOSE 3000

# CMD — the DEFAULT command run when a container starts (overridable at `docker run`)
CMD ["node", "server.js"]
```

| Instruction | Purpose | When it runs |
|-------------|---------|--------------|
| `FROM` | Base image | Build |
| `WORKDIR` | Set/scope working dir | Build |
| `COPY` / `ADD` | Bring files in (`COPY` preferred) | Build |
| `RUN` | Execute build commands → layer | Build |
| `ENV` | Env var (persists into runtime) | Build + Run |
| `ARG` | Build-time variable only | Build |
| `EXPOSE` | Document a port (metadata) | — |
| `CMD` | Default runtime command (overridable) | Run |
| `ENTRYPOINT` | Fixed runtime executable | Run |

### CMD vs ENTRYPOINT — the classic confusion

```dockerfile
ENTRYPOINT ["node"]          # the fixed executable — always runs
CMD ["server.js"]            # the default ARGUMENT — overridable at `docker run`
# `docker run img`            → node server.js
# `docker run img worker.js`  → node worker.js   (CMD replaced, ENTRYPOINT stays)
```

> **Gotcha — use the JSON/"exec" form `["node","server.js"]`, not the shell form `node server.js`.** The shell form wraps your process in `/bin/sh -c`, which swallows Unix signals — so `SIGTERM` on shutdown never reaches your app and the container is force-killed after a timeout (losing in-flight requests). The exec form makes your app PID 1 and signal-receiving.

> **Gotcha — `ADD` does surprising things (URL fetch, auto-extract archives).** Prefer `COPY` for plain file copies; reach for `ADD` only when you specifically want tar auto-extraction.

---

## IV. THE ESSENTIAL COMMANDS

```bash
# BUILD an image from a Dockerfile in the current dir; -t tags it
docker build -t myapp:1.0 .

# RUN a container
docker run -d \                    # -d detached (background)
  --name web \                     # name it
  -p 8080:3000 \                   # publish host:container port (host 8080 → container 3000)
  -e NODE_ENV=production \         # set an env var
  --restart unless-stopped \       # restart policy
  myapp:1.0

docker ps                          # list RUNNING containers
docker ps -a                       # include stopped ones
docker logs -f web                 # stream logs (-f follow)
docker exec -it web sh             # open a shell INSIDE a running container (debugging)
docker stop web && docker rm web   # stop then remove
docker rmi myapp:1.0               # remove an image
docker system prune                # reclaim disk (dangling images, stopped containers)
```

> **Gotcha — `-p 8080:3000` order is `HOST:CONTAINER`.** Mixing it up means you connect to the wrong port. The container listens on 3000 (matching your app); you reach it from the host on 8080.

---

## V. MULTI-STAGE BUILDS & IMAGE OPTIMIZATION

Naively building ships your *entire* build toolchain (compilers, dev dependencies, source) to production — huge, slow, and a bigger attack surface. **Multi-stage builds** use one stage to build and a clean, minimal stage to run.

```dockerfile
# ---- Stage 1: BUILD (has all the dev tooling) ----
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci                          # ALL deps, including dev (TypeScript, bundler)
COPY . .
RUN npm run build                   # produces /app/dist

# ---- Stage 2: RUNTIME (tiny, only what's needed to run) ----
FROM node:20-slim AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev               # production deps only
COPY --from=build /app/dist ./dist  # copy ONLY the built artifact from stage 1
USER node                           # run as non-root (security)
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

The final image contains *only* the runtime stage — the build tools never ship.

**Optimization checklist:**

| Technique | Why |
|-----------|-----|
| **Small base image** (`slim`, `alpine`, `distroless`) | Less size, fewer CVEs |
| **Multi-stage build** | Drop build tooling from the final image |
| **Order layers by change frequency** | Copy `package.json` + install *before* copying source → dependency layer stays cached |
| **`.dockerignore`** | Don't send `node_modules`, `.git` into the build context |
| **Run as non-root** (`USER node`) | Limit blast radius of a compromise |
| **Combine `RUN` steps & clean caches** | Fewer/smaller layers |

```dockerfile
# Layer caching done right — deps install only re-runs when package.json changes
COPY package*.json ./        # changes rarely
RUN npm ci                   # cached unless package.json changed
COPY . .                     # changes often — kept AFTER the expensive install
```

> **⚠️ Gotcha — by default containers run as root.** A process running as root inside a container that escapes (via a kernel/runtime bug) is root-ish on the host. Always add a non-root `USER`. **Distroless** images (no shell, no package manager) shrink the attack surface further — but you lose `docker exec ... sh` for debugging.

---

## VI. .dockerignore & BUILD CONTEXT

When you run `docker build .`, Docker sends the whole directory (the **build context**) to the daemon. Without a `.dockerignore`, that includes `node_modules`, `.git`, secrets — slowing builds and risking leaks.

```bash
# .dockerignore — mirror your .gitignore plus build-specific excludes
node_modules
.git
.env                  # never bake secrets into an image!
dist
*.log
Dockerfile
.dockerignore
README.md
coverage
```

> **⚠️ Gotcha — never `COPY .env` or secrets into an image.** Image layers are inspectable: anyone who pulls the image can extract a baked-in secret with `docker history` / layer extraction — even if a later layer "deletes" it. Pass secrets at **runtime** (`-e`, secret mounts, orchestrator secrets), never at build time.

---

## VII. VOLUMES & PERSISTENCE

Containers are **ephemeral** — the writable layer dies with the container. To persist data (databases, uploads) you mount storage that outlives the container.

```bash
# NAMED VOLUME — Docker-managed; the right choice for databases
docker volume create pgdata
docker run -d --name db -v pgdata:/var/lib/postgresql/data postgres:16

# BIND MOUNT — map a host path into the container; great for live-reload in dev
docker run -d -v "$(pwd)/src:/app/src" myapp:dev
```

| | **Named volume** | **Bind mount** |
|---|---|---|
| Managed by | Docker | You (host path) |
| Best for | Databases, production data | Dev (live code), config files |
| Portability | High (Docker-managed) | Tied to host filesystem layout |
| Performance | Optimized | Can be slow on macOS/Windows |

> **Gotcha — without a volume, your database data vanishes on `docker rm`.** People run `postgres` in a container, lose the container, and lose the data. Always mount a named volume for any stateful service.

---

## VIII. NETWORKS & CONTAINER DNS

Docker gives containers their own virtual networks. On a **user-defined bridge network**, containers reach each other **by name** via Docker's built-in DNS — no hardcoded IPs.

```bash
docker network create appnet
docker run -d --name db   --network appnet postgres:16
docker run -d --name api  --network appnet myapi:1.0
# Inside the api container, the DB host is simply "db" — Docker DNS resolves it.
#   DATABASE_URL=postgres://user:pass@db:5432/mydb
```

| Network mode | Behavior |
|--------------|----------|
| `bridge` (default) | Isolated virtual network; containers talk via published ports |
| **user-defined bridge** | Like bridge + automatic name-based DNS between containers |
| `host` | Container shares the host's network stack (no isolation) |
| `none` | No networking |

> **Gotcha — the default `bridge` network has no DNS by name.** Container-to-container name resolution only works on a **user-defined** network (or via Compose, which creates one for you). On the default bridge you'd need `--link` (deprecated) or IPs. Always create a user-defined network for multi-container apps.

---

## IX. DOCKER COMPOSE — MULTI-SERVICE APPS

Real apps are several containers (API, database, cache). **Compose** defines them all in one YAML file and runs them together with one command.

```yaml
# compose.yaml — an API + Postgres + Redis stack
services:
  api:
    build: .                          # build from the local Dockerfile
    ports:
      - "8080:3000"                   # host:container
    environment:
      DATABASE_URL: postgres://app:secret@db:5432/app   # "db" resolves via Compose network
      REDIS_URL: redis://cache:6379
    depends_on:
      db:
        condition: service_healthy    # wait until db is actually ready (see gotcha)
    restart: unless-stopped

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: secret       # in real life: use secrets, not inline
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data   # persist the database
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 5

  cache:
    image: redis:7

volumes:
  pgdata:                             # named volume declared once, reused above
```

```bash
docker compose up -d          # build + start everything in the background
docker compose logs -f api    # follow one service's logs
docker compose ps             # status of all services
docker compose down           # stop & remove containers + network (volumes kept)
docker compose down -v        # ...also remove volumes (deletes data!)
```

> **⚠️ Gotcha — `depends_on` waits for the container to *start*, not to be *ready*.** Postgres's container being "up" doesn't mean it accepts connections yet. Use a `healthcheck` + `condition: service_healthy` (as above), or have your app retry the connection on startup. Otherwise the API races the DB and crashes on boot.

---

## X. KUBERNETES — A CONCEPTS PRIMER

Compose runs containers on *one* machine. **Kubernetes (K8s)** orchestrates containers across a *cluster* of machines — handling scaling, self-healing, rolling updates, and service discovery at scale. You don't need it for a small app, but you should understand its vocabulary.

```
Cluster
 ├── Node (a worker machine)
 │    └── Pod (smallest unit — one+ containers sharing network/storage)
 │         └── Container (your app)
 ├── Deployment  → declares "I want N replicas of this Pod"; self-heals & rolls updates
 ├── Service     → stable network endpoint + load balancing across Pods
 └── Ingress     → routes external HTTP(S) traffic to Services (the front door)
```

| Concept | What it is |
|---------|-----------|
| **Pod** | Smallest deployable unit — one or more tightly-coupled containers |
| **Deployment** | Declares desired replica count; recreates/rolls Pods to match |
| **Service** | Stable internal DNS name + load balancing over a set of Pods |
| **Ingress** | HTTP routing + TLS termination from the outside world |
| **ConfigMap / Secret** | Inject configuration / sensitive values |
| **Namespace** | Logical partition of cluster resources |

```yaml
# A minimal Deployment + Service — declarative: you state the desired end state
apiVersion: apps/v1
kind: Deployment
metadata: { name: api }
spec:
  replicas: 3                         # K8s keeps exactly 3 healthy Pods running
  selector: { matchLabels: { app: api } }
  template:
    metadata: { labels: { app: api } }
    spec:
      containers:
        - name: api
          image: ghcr.io/me/myapp:1.2.0   # pinned version, not :latest
          ports: [{ containerPort: 3000 }]
          readinessProbe:                  # don't route traffic until ready (file 08)
            httpGet: { path: /healthz, port: 3000 }
```

> **Gotcha — Kubernetes is declarative, and often overkill.** You describe the *desired state*; K8s continuously reconciles reality to match it. But its operational complexity is enormous — for a single app or small team, a PaaS or Compose-on-a-VPS is usually the right call. Adopt K8s when you genuinely need multi-node scale, self-healing, and rolling deploys.

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Deploying `:latest` | Can't tell what's running; non-reproducible | Pin explicit version tags |
| Running as root | Larger compromise blast radius | Add `USER node`/non-root; distroless |
| Baking secrets into the image | Extractable from layers | Pass secrets at runtime |
| No `.dockerignore` | Slow builds, leaked files | Add `.dockerignore` (node_modules, .git, .env) |
| `COPY . .` before `npm ci` | Cache busts deps on every code change | Copy `package.json` + install first |
| Shipping build tools to prod | Huge, insecure images | Multi-stage build |
| Shell-form `CMD` | Signals ignored, slow/forced shutdown | Use exec form `["node","server.js"]` |
| No volume for a database | Data lost on `docker rm` | Mount a named volume |
| Default bridge for multi-container | Name resolution fails | User-defined network or Compose |
| `depends_on` without healthcheck | App races DB and crashes | `condition: service_healthy` + retries |
| `docker compose down -v` by habit | Deletes volumes/data | Use plain `down`; reserve `-v` |
| Reaching for K8s too early | Crushing complexity | PaaS/Compose until you truly need scale |

---

## 🧠 KEY TAKEAWAYS

- A **container** virtualizes the OS (shares the host kernel) — tiny, fast, and portable — versus a **VM** that virtualizes hardware with a full guest OS. Container isolation is weaker; sandbox hostile workloads.
- An **image** is a layered, read-only blueprint; a **container** is a running instance. Layers are **cached and shared**, so instruction order drives build speed. Pin versions — `:latest` is not a version.
- The **Dockerfile** builds images: `FROM`/`WORKDIR`/`COPY`/`RUN`/`ENV`/`ARG`/`EXPOSE`/`CMD`/`ENTRYPOINT`. Use the **exec form** so signals reach your app.
- **Multi-stage builds** keep build tooling out of production; optimize with small bases, cache-friendly layer order, `.dockerignore`, and a **non-root** user.
- **Never bake secrets into images** — they're extractable from layers; inject at runtime.
- Containers are ephemeral — mount **named volumes** for stateful data, and use **user-defined networks** so containers resolve each other by name.
- **Compose** runs a multi-service stack from one YAML file; use **healthchecks** + `service_healthy` so apps don't race their dependencies.
- **Kubernetes** orchestrates containers across a cluster (Pods, Deployments, Services, Ingress) declaratively — powerful but often overkill; adopt it only when scale demands it.

---

**Prev:** [`04-Git-And-Collaboration.md`](./04-Git-And-Collaboration.md) · **Next:** [`06-CICD-And-Deployment.md`](./06-CICD-And-Deployment.md) · **Index:** [`00-Index.md`](./00-Index.md)
