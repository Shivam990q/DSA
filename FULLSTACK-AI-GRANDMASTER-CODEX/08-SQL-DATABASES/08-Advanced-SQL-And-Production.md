# 🗄️ 08 — Advanced SQL & Production

> *"The query that runs on your laptop is a hypothesis. The query that runs safely, under load, against real data, behind a connection pool, with backups you've actually restored — that's a production database."*

**Prev:** [`07-Transactions-And-Concurrency.md`](./07-Transactions-And-Concurrency.md) · **Next:** [`../09-NOSQL-MONGODB/00-Index.md`](../09-NOSQL-MONGODB/00-Index.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

> The final SQL chapter. You can model schemas, write any query, read a plan, and reason about transactions. Now you'll push logic *into* the database (functions, triggers), **defend it** (injection, roles, least privilege), **connect to it** from real code with **connection pools**, and **scale and protect** it (replication, partitioning, sharding, backups, migrations). These are the production skills that keep data correct and available.

---

## I. STORED PROCEDURES & FUNCTIONS

A **stored function/procedure** is code that lives *inside* the database and runs *next to the data* — no round trip to the application for each step. PostgreSQL's procedural language is **PL/pgSQL**.

- **Function** (`CREATE FUNCTION`) — returns a value (or table); callable inside a query (`SELECT my_fn(...)`). Cannot manage transactions.
- **Procedure** (`CREATE PROCEDURE`, Postgres 11+) — invoked with `CALL`; can `COMMIT`/`ROLLBACK` inside (useful for batch jobs).

```sql
-- A function: compute a customer's lifetime value, server-side
CREATE OR REPLACE FUNCTION customer_ltv(p_user_id INT)
RETURNS NUMERIC AS $$                       -- $$ = dollar-quoting, so the body needs no escaping
DECLARE
  total NUMERIC;                            -- a local variable
BEGIN
  SELECT COALESCE(SUM(total), 0)            -- COALESCE so a customer with no orders returns 0
    INTO total
    FROM orders
   WHERE user_id = p_user_id;
  RETURN total;
END;
$$ LANGUAGE plpgsql;

-- Call it like any built-in function:
SELECT customer_ltv(5);                     -- → 1240.00
SELECT id, customer_ltv(id) AS ltv FROM users;   -- even per-row in a query
```

```sql
-- A procedure: archive old orders in batches, committing as it goes
CREATE OR REPLACE PROCEDURE archive_old_orders()
LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO orders_archive SELECT * FROM orders WHERE created_at < now() - INTERVAL '1 year';
  DELETE FROM orders                       WHERE created_at < now() - INTERVAL '1 year';
  COMMIT;                                   -- procedures CAN commit; functions cannot
END;
$$;

CALL archive_old_orders();
```

### When to use — and when to avoid

| Use stored logic when... | Avoid it when... |
|--------------------------|------------------|
| Logic is **data-intensive** (avoids shipping rows to the app) | Logic is **business rules** better tested/versioned in app code |
| You need **atomic, set-based** operations close to the data | Your team can't easily **version-control / review** DB code |
| Multiple apps share the **same critical logic** | It creates **vendor lock-in** (PL/pgSQL ≠ T-SQL ≠ PL/SQL) |
| Performance demands minimal round trips | It hides logic where app developers won't find it |

> **Gotcha — stored procedures are powerful but easy to lose track of.** Business logic buried in the database is hard to test, hard to diff in code review, and invisible to app developers debugging a bug. Keep procedures for genuinely data-intensive or integrity-critical work; keep business rules in application code where your test suite and CI can see them. If you do use them, **store the SQL in your repo and apply it via migrations** (§X), never by hand.

---

## II. TRIGGERS

A **trigger** runs a function **automatically** in response to `INSERT`/`UPDATE`/`DELETE` on a table. Great for audit logs and keeping derived data in sync — but invisible side effects, so use with care.

- **Timing:** `BEFORE` (can modify or reject the row *before* it's written) vs `AFTER` (the row is already written; react to it).
- **Granularity:** `FOR EACH ROW` (fires once per affected row) vs `FOR EACH STATEMENT` (fires once per statement, regardless of row count).

### Example 1 — an audit log (AFTER trigger)

```sql
-- Audit table records every change to accounts
CREATE TABLE accounts_audit (
  id BIGSERIAL PRIMARY KEY,
  account_id INT, old_balance NUMERIC, new_balance NUMERIC,
  changed_by TEXT DEFAULT current_user, changed_at TIMESTAMPTZ DEFAULT now()
);

CREATE OR REPLACE FUNCTION log_balance_change()
RETURNS TRIGGER AS $$                        -- trigger functions return TRIGGER
BEGIN
  -- NEW = the row after the change; OLD = the row before (available in UPDATE/DELETE)
  INSERT INTO accounts_audit (account_id, old_balance, new_balance)
  VALUES (NEW.id, OLD.balance, NEW.balance);
  RETURN NEW;                                -- AFTER triggers ignore the return, but return NEW by convention
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_audit_balance
  AFTER UPDATE OF balance ON accounts        -- only when `balance` changes
  FOR EACH ROW
  WHEN (OLD.balance IS DISTINCT FROM NEW.balance)   -- skip no-op updates
  EXECUTE FUNCTION log_balance_change();
```

### Example 2 — keep a counter in sync (denormalization helper)

```sql
-- Keep users.order_count accurate as orders come and go (the denormalization from file 06)
CREATE OR REPLACE FUNCTION sync_order_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE users SET order_count = order_count + 1 WHERE id = NEW.user_id;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE users SET order_count = order_count - 1 WHERE id = OLD.user_id;
  END IF;
  RETURN NULL;                               -- AFTER trigger: return value ignored
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_order_count
  AFTER INSERT OR DELETE ON orders
  FOR EACH ROW EXECUTE FUNCTION sync_order_count();
```

> **Gotcha — triggers are invisible action-at-a-distance.** An `UPDATE` that mysteriously also writes three other tables, fires twice, or slows to a crawl is often an unsuspected trigger. They don't show up in application code, they complicate bulk operations, and a trigger that errors will **abort the whole statement**. Document every trigger, keep them simple and fast, and never put slow work (or external calls) inside one. For complex sync, an application-level event or a scheduled job is often clearer.

---

## III. SQL INJECTION — IN DEPTH & PREVENTION

**SQL injection** is the most damaging and most common database vulnerability: an attacker smuggles SQL into a query by exploiting **string concatenation** of untrusted input. It's #3 (Injection) on the OWASP Top 10 and has caused some of history's largest breaches.

### Why string concatenation is fatal

```javascript
// ❌ CATASTROPHIC — user input is glued straight into the SQL text
const q = "SELECT * FROM users WHERE email = '" + req.body.email + "'";
db.query(q);
```

Now consider what an attacker submits as `email`:

```sql
-- Input:  ' OR '1'='1
-- Resulting query — the WHERE is now always true, returning EVERY user:
SELECT * FROM users WHERE email = '' OR '1'='1';

-- Input:  '; DROP TABLE users; --
-- Resulting query — a second, destructive statement is injected:
SELECT * FROM users WHERE email = ''; DROP TABLE users; --';
```

The database can't tell the attacker's text from your intended SQL — to it, it's all one string. Data and code got mixed.

### The fix: parameterized queries (prepared statements)

With **parameters**, you send the SQL **template** and the **values separately**. The database compiles the query structure first, then binds the values as *pure data* — they can never be interpreted as SQL, no matter what they contain. This is the single most important defense.

```javascript
// ✅ SAFE — placeholders ($1, $2), values passed as a separate array
const q = "SELECT * FROM users WHERE email = $1";
db.query(q, [req.body.email]);
// Now the input ' OR '1'='1 is treated as a literal email string. It matches nothing. No injection.
```

```javascript
// ✅ SAFE — INSERT with parameters
db.query(
  "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
  [req.body.name, req.body.email]
);
```

> **Gotcha — escaping by hand is NOT a substitute.** Manually doubling quotes or stripping characters is fragile and bypassable (encodings, edge cases, second-order injection). **Always use parameterized queries / prepared statements** — every driver supports them. The only exception is identifiers (table/column names) which can't be parameterized; for those, **validate against an allowlist**, never interpolate raw input.

| | String concatenation | Parameterized query |
|---|----------------------|---------------------|
| How values arrive | Glued into SQL text | Sent separately as data |
| Injection possible? | **Yes — trivially** | No (values can't become SQL) |
| Plan caching | New plan per value | Reusable prepared plan (also faster) |
| Verdict | **Never** | **Always** |

### Defense in depth: least privilege

Even with perfect parameterization, limit the blast radius. The account your app connects with should have **only the privileges it needs** (§IV). If a vulnerability *is* found, an app user that can't `DROP TABLE` or read other schemas contains the damage.

---

## IV. ROLES, GRANT/REVOKE, ROW-LEVEL SECURITY

PostgreSQL access control is built on **roles** (a role is a user and/or a group). You grant **privileges** on objects to roles.

```sql
-- Create a login role for the application (NOT a superuser):
CREATE ROLE app_user WITH LOGIN PASSWORD 'use-a-secret-manager-not-this';

-- Grant ONLY what the app needs (principle of least privilege):
GRANT CONNECT ON DATABASE codexdb TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
-- Note: NO DROP, NO TRUNCATE, NO DDL, NO superuser. The app can't damage structure.

-- Make it apply to future tables too:
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Take privileges away:
REVOKE DELETE ON orders FROM app_user;       -- e.g. orders are soft-deleted only

-- Group roles: grant a role TO another role
CREATE ROLE readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
GRANT readonly TO analyst_jane;               -- Jane inherits read-only access
```

> **Gotcha — never let your app connect as a superuser (or `postgres`).** A superuser bypasses *all* permission checks; a single injection or bug then has unlimited power (drop tables, read every row, alter the schema). Create a dedicated least-privilege role per application and connect as that.

### Row-Level Security (RLS) — per-row access policies

RLS lets the database itself enforce *which rows* a role may see or modify — invaluable for multi-tenant apps where every query must be scoped to one tenant.

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- A policy: a user can only see their own rows
CREATE POLICY user_isolation ON documents
  USING (owner_id = current_setting('app.current_user_id')::INT);
-- The app sets the variable per request:  SET app.current_user_id = '5';
-- Now even a buggy `SELECT * FROM documents` returns only user 5's rows.
```

> RLS is a powerful safety net for multi-tenant SaaS, but it's an advanced topic — it interacts with connection pooling (you must set the per-request variable on the pooled connection) and adds query overhead. Reach for it when tenant isolation must be guaranteed at the data layer, not just in app code.

---

## V. CONNECTING FROM CODE & CONNECTION POOLING

### Why pools matter

Opening a database connection is **expensive** — a TCP handshake, authentication, and backend process startup, often 20–50ms+. Doing that per request would dominate your latency and exhaust the database (Postgres forks a backend process per connection; thousands of connections will crush it). A **connection pool** keeps a small set of connections open and **reuses** them across requests.

```
Without a pool:  request → open conn (slow) → query → close → repeat   (handshake every time)
With a pool:     request → borrow conn from pool → query → return to pool   (reused, fast)
```

### Node.js with `pg` — pooled and parameterized

```javascript
// File: db.js
const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 10,                       // max connections this app instance holds (see sizing below)
  idleTimeoutMillis: 30_000,     // close a connection idle this long
  connectionTimeoutMillis: 5_000 // fail fast if no connection is available
});

// For one-off queries, pool.query borrows + returns a connection automatically:
async function getUser(id) {
  const { rows } = await pool.query(
    "SELECT id, email FROM users WHERE id = $1", [id]   // parameterized — always (§III)
  );
  return rows[0];
}
// (For multi-statement TRANSACTIONS, check out a single client — see file 07 §X.)
```

### Java — JDBC + a pool (HikariCP), or JPA

```java
// HikariCP is the de-facto JDBC connection pool.
HikariConfig cfg = new HikariConfig();
cfg.setJdbcUrl("jdbc:postgresql://localhost:5432/codexdb");
cfg.setUsername("app_user");
cfg.setMaximumPoolSize(10);                 // pool size (see sizing)
HikariDataSource ds = new HikariDataSource(cfg);

try (Connection conn = ds.getConnection();  // borrow from the pool
     PreparedStatement ps = conn.prepareStatement("SELECT email FROM users WHERE id = ?")) {
    ps.setInt(1, id);                        // parameterized — prevents injection
    try (ResultSet rs = ps.executeQuery()) {
        if (rs.next()) return rs.getString("email");
    }
}                                            // try-with-resources returns the conn to the pool
```

> **Higher-level option — JPA/Hibernate / Spring Data.** Most Java apps use an ORM (JPA via Hibernate, exposed through Spring Data JPA) rather than raw JDBC. It maps rows to objects and generates SQL, but **sits on top of JDBC + a pool** — the fundamentals here still apply. The deep treatment of Java persistence lives in [`../04-JAVA-MASTERY/`](../04-JAVA-MASTERY/00-Index.md).

### Pool sizing — smaller than you think

```
A good starting point (PostgreSQL):  connections ≈ ((core_count * 2) + effective_spindle_count)
```

> **Gotcha — bigger pools are usually slower.** It's counter-intuitive: a database with 8 cores can only *truly* run a handful of queries at once; 200 connections just thrash on context switches, locks, and memory. Keep each app instance's pool small (often 5–20). Remember to multiply by the number of app instances (§IV scaling) — 20 instances × 20 connections = 400 connections hitting the database. If that exceeds the DB's limit, put a **server-side pooler like PgBouncer** in front to multiplex many app connections onto few database connections.

---

## VI. SCALING — REPLICATION

A single database server has a ceiling. The first scaling move is usually **replication**: keep one or more **copies** of the database on other servers.

- **Primary (leader)** — accepts **writes** (and reads). The source of truth.
- **Replica (follower/standby)** — a read-only copy that streams changes from the primary via the WAL (file 07). Serves **reads**, providing **read scaling** and **high availability** (promote a replica if the primary dies).

```
              writes
   clients ──────────► [ PRIMARY ] ──WAL stream──► [ REPLICA 1 ] ◄─ reads
                            │         ──WAL stream──► [ REPLICA 2 ] ◄─ reads
   Route reads to replicas; writes only to the primary.
```

| | **Synchronous replication** | **Asynchronous replication** |
|---|------------------------------|------------------------------|
| Commit waits for replica? | Yes — primary waits for replica to confirm | No — primary commits immediately |
| Durability on primary failure | No committed data lost | Recent commits may be lost |
| Write latency | Higher | Lower |
| Use for | Financial / zero-loss requirements | Most apps (read scaling, lower latency) |

> **Gotcha — replication lag means replicas can be stale.** With async replication, a replica is a few milliseconds (sometimes seconds under load) behind the primary. A user who writes then immediately reads from a replica may **not see their own write** ("read-your-writes" violation). Fix: route reads that must be current to the primary, or wait for the replica to catch up. Don't assume a replica is instantly consistent.

---

## VII. SCALING — PARTITIONING & SHARDING

### Partitioning — split one big table into pieces (same server)

When a table grows to hundreds of millions of rows, splitting it into **partitions** keeps each piece small: queries scan only the relevant partition ("partition pruning"), and you can drop old partitions instantly.

```sql
-- Range partitioning by month — common for time-series / logs
CREATE TABLE events (id BIGSERIAL, created_at DATE NOT NULL, payload JSONB)
  PARTITION BY RANGE (created_at);

CREATE TABLE events_2024_01 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE events_2024_02 PARTITION OF events
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
-- A query WHERE created_at >= '2024-02-10' only touches events_2024_02 (pruning).
-- Dropping old data is instant: DROP TABLE events_2024_01;  (vs a slow bulk DELETE)
```

| Strategy | Splits rows by... | Good for |
|----------|-------------------|----------|
| **Range** | A range of values (dates, ids) | Time-series, anything with natural ordering |
| **List** | A discrete value (region, type) | Categorical data (per-country, per-tenant) |
| **Hash** | A hash of the key | Even distribution when there's no natural range |

### Sharding — split data across multiple servers

**Sharding** is horizontal partitioning across **different machines**. Each shard holds a subset of the data (e.g. users A–M on shard 1, N–Z on shard 2). This scales **writes** and storage beyond one server — the thing replication can't do.

```
                        ┌─ shard 1 (users A–M) ─┐
   app ── shard key ───►├─ shard 2 (users N–Z) ─┤  each is a full, independent database
                        └─ shard 3 (users ...) ─┘
```

> **Gotcha — sharding is a one-way door; delay it as long as possible.** It breaks things you took for granted: cross-shard `JOIN`s and transactions become hard or impossible, the **shard key** is painful to change later, and rebalancing is complex. Exhaust the cheaper options first — **indexing (file 06), caching (Redis), read replicas, and partitioning** — before sharding. Many teams that "needed sharding" actually needed a missing index.

### When to reach for each (in order)

```
1. Index & optimize queries (file 06)      ← cheapest, do this first
2. Cache hot reads (Redis)                  ← offload the database
3. Read replicas                            ← scale READS
4. Partition large tables                   ← keep tables manageable on one server
5. Shard                                     ← scale WRITES/storage — last resort
```

---

## VIII. BACKUPS & POINT-IN-TIME RECOVERY

A database without **tested** backups is a future disaster. Hardware fails, fingers fat-finger `DELETE` without a `WHERE`, and ransomware happens.

```bash
# Logical backup — a portable dump of schema + data (good for small/medium DBs, migrations)
pg_dump codexdb > backup.sql                 # plain SQL
pg_dump -Fc codexdb > backup.dump            # custom compressed format (restore selectively)
pg_restore -d codexdb backup.dump            # restore the custom format

# Physical backup — a binary copy of the data files (fast for large DBs)
pg_basebackup -D /backups/base -Ft -z        # base backup for PITR
```

**Point-in-Time Recovery (PITR)** combines a base backup with the archived **WAL** (file 07) so you can restore to *any moment* — e.g. "the state at 14:32, one minute before the bad `DELETE`." You replay the WAL up to that timestamp.

```
base backup (Sunday) ──── + replay WAL ────► restore to exactly 14:32:07 Tuesday
```

> **Gotcha — an untested backup is not a backup.** The only way to know a backup works is to **restore it** — into a scratch database, regularly, ideally automated. Countless teams discovered at the worst possible moment that their backups were empty, corrupt, or un-restorable. Schedule restore drills. Also: store backups **off-site/off-host** (a backup on the same disk that fails is no backup).

---

## IX. MIGRATIONS — VERSIONING YOUR SCHEMA

Your schema changes over time (new columns, tables, indexes). **Migrations** are versioned, ordered scripts that evolve the schema in a repeatable way — the equivalent of git for your database structure. Never change a production schema by hand; write a migration, commit it, and apply it through the pipeline.

```sql
-- File: migrations/0007_add_phone_to_users.sql  (forward / "up")
ALTER TABLE users ADD COLUMN phone TEXT;

-- A "down" / rollback companion (many tools track both):
-- ALTER TABLE users DROP COLUMN phone;
```

| Tool | Ecosystem | Style |
|------|-----------|-------|
| **Flyway / Liquibase** | Java / language-agnostic | Plain SQL (Flyway) or XML/YAML changesets (Liquibase) |
| **Prisma Migrate** | Node/TypeScript | Generates SQL from a declarative schema |
| **Knex migrations** | Node | JavaScript up/down functions |
| **Alembic** | Python (SQLAlchemy) | Python up/down scripts |
| **Rails Active Record** | Ruby | Ruby DSL migrations |

```javascript
// Knex example — programmatic up/down
exports.up   = (knex) => knex.schema.alterTable("users", t => t.string("phone"));
exports.down = (knex) => knex.schema.alterTable("users", t => t.dropColumn("phone"));
```

> **Gotcha — some migrations lock the table and cause downtime.** Adding a column with a non-constant default, creating an index without `CONCURRENTLY`, or changing a column type can lock a big table and stall all writes. For zero-downtime: add nullable columns first, backfill in batches, create indexes `CONCURRENTLY`, and split risky changes across multiple deploys. Always test a migration against production-sized data before shipping it.

---

## X. SQL vs NoSQL — THE DECISION

You've now mastered the relational model. The natural next question: when is a relational database the *wrong* choice? That's the bridge to the next section.

| Choose **SQL (relational)** when... | Consider **NoSQL** when... |
|-------------------------------------|----------------------------|
| Data is **structured & relational** (clear entities, joins) | Data is **schema-flexible / document-shaped** |
| You need **ACID transactions** (money, inventory) | You need **massive horizontal write scale** above all |
| **Complex queries / ad-hoc reporting** (joins, aggregates) | Access patterns are **simple key/document lookups** |
| **Strong consistency** is required | **Eventual consistency** is acceptable for speed/availability |
| The schema is **stable** | The schema **changes constantly** or varies per record |

> **The honest default:** for most applications, **start with PostgreSQL.** It's relational *and* handles JSON (`JSONB`), full-text search, arrays, and huge scale — covering many "NoSQL" needs without giving up ACID and joins. Reach for a document store, key-value store, or wide-column database when a *specific* access pattern or scale requirement genuinely demands it.

> **The deep dive into document databases — MongoDB, the document model, when documents beat tables, and the tradeoffs you're accepting — is the entire next section: [`../09-NOSQL-MONGODB/`](../09-NOSQL-MONGODB/00-Index.md).** This is the pointer; that section is where the comparison becomes hands-on.

---

## XI. COMMON PITFALLS

| Pitfall | Symptom / Risk | Fix |
|---------|----------------|-----|
| String-concatenated SQL | SQL injection → breach / data loss | Parameterized queries / prepared statements, always |
| Hand-rolled escaping | Bypassable; second-order injection | Use driver parameters; allowlist identifiers |
| App connects as superuser | Any bug/injection has unlimited power | Dedicated least-privilege role |
| Business logic buried in triggers/procs | Invisible, untested, hard to debug | Keep business rules in app code; version DB code in migrations |
| Slow/external work inside a trigger | Every write stalls; statement aborts on error | Keep triggers tiny; use jobs/events for heavy sync |
| No connection pool | Latency + DB connection exhaustion | Pool connections; reuse them |
| Pool too large | Context-switch thrash, slower under load | Small pool per instance; PgBouncer to multiplex |
| Reading from a stale replica | "I don't see my own write" | Route current-read to primary; mind replication lag |
| Sharding too early | Lost joins/transactions, huge complexity | Index → cache → replicas → partition first |
| Untested backups | Unrecoverable on disaster | Restore drills; off-site copies |
| Schema changed by hand | Drift between environments; no rollback | Versioned migrations through the pipeline |
| Locking migration on a big table | Downtime during deploy | `CONCURRENTLY`, nullable-first, batched backfills |
| Picking NoSQL by hype | Lost ACID/joins you actually needed | Default to Postgres; choose NoSQL for a real reason |

---

## 🧠 KEY TAKEAWAYS

- **Stored functions/procedures** (PL/pgSQL) run logic next to the data — great for data-intensive, integrity-critical work; keep ordinary **business rules in app code** where tests and reviews can see them, and ship DB code via **migrations**.
- **Triggers** automate reactions to writes (audit logs, keeping counters in sync) but are **invisible side effects** — keep them small and fast, document them, and never do heavy/external work inside one.
- **SQL injection** comes from concatenating untrusted input into SQL; the cure is **parameterized queries** (values sent separately from the SQL template) plus **least-privilege** roles as defense in depth. Hand-escaping is not enough.
- Use **roles** with `GRANT`/`REVOKE` to give the app only what it needs (never superuser); **row-level security** can enforce per-tenant row isolation in the database itself.
- **Connection pools** reuse expensive connections — keep them **small** (bigger is usually slower), multiply by instance count, and add **PgBouncer** when totals get large. Always parameterize from `pg`/JDBC; transactions use one connection (file 07).
- Scale in order: **index → cache → read replicas → partition → shard**. Replicas scale **reads** (mind **replication lag**); **partitioning** keeps big tables manageable on one server; **sharding** scales writes but is a one-way door that breaks joins/transactions.
- Keep **tested, off-site backups** and understand **PITR** (base backup + WAL replay to any moment). An untested backup is not a backup.
- Evolve schemas with **versioned migrations**; beware locking migrations on large tables (use `CONCURRENTLY`, nullable-first, batched backfills).
- **Default to PostgreSQL**; choose **NoSQL** only when a specific access pattern or scale need genuinely demands it — the hands-on comparison is section 09.

---

**Prev:** [`07-Transactions-And-Concurrency.md`](./07-Transactions-And-Concurrency.md) · **Next:** [`../09-NOSQL-MONGODB/00-Index.md`](../09-NOSQL-MONGODB/00-Index.md) · **Index:** [`00-Index.md`](./00-Index.md)
