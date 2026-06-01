# 🗄️ 06 — Indexing & Query Optimization

> *"An index is a promise: 'I will pay extra on every write so that reads can be miraculous.' Make that promise deliberately, and only where it pays."*

**Prev:** [`05-Aggregation-And-Advanced-Queries.md`](./05-Aggregation-And-Advanced-Queries.md) · **Next:** [`07-Transactions-And-Concurrency.md`](./07-Transactions-And-Concurrency.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE PROBLEM INDEXES SOLVE

Without an index, finding rows means a **sequential scan** (a.k.a. full table scan): read *every* row and test the condition. On a million-row table, `WHERE email = 'ada@x.com'` reads a million rows to find one. That's O(n).

An **index** is a separate, sorted data structure that maps column values to the rows that hold them — like the index at the back of a book. With it, the database jumps near-directly to matching rows in roughly **O(log n)**.

```
No index (seq scan):           With B-tree index:
read row 1 ... 1,000,000        descend the tree: ~3-4 hops to the leaf
O(n) — reads everything         O(log n) — reads a handful of pages
```

The trade: an index is a **copy of the data** (the indexed columns + a pointer), so it costs **disk space** and must be **updated on every `INSERT`/`UPDATE`/`DELETE`** of the indexed columns. Indexes make reads fast and writes slower. That tension is the whole game.

---

## II. HOW A B-TREE INDEX WORKS

The default index in every major database is the **B-tree** (balanced tree). It keeps keys **sorted** and stays shallow, so any lookup is a few page reads.

```
                    ┌───────────────┐
                    │   [50 | 100]  │   ← root (decision node)
                    └──┬─────┬─────┬─┘
            < 50 ──────┘  50–100  └────── > 100
            ▼             ▼                ▼
       ┌─────────┐   ┌─────────┐      ┌─────────┐
       │[20 | 35]│   │[70 | 85]│      │[130|160]│   ← internal nodes
       └─┬──┬──┬─┘   └─────────┘      └─────────┘
         ▼  ▼  ▼
     ...leaf pages: sorted keys → pointers to actual table rows...
     [10→ptr][15→ptr][20→ptr] ... linked left↔right for range scans
```

Two properties make B-trees ideal for databases:

1. **Balanced & shallow.** All leaves are at the same depth. Even billions of rows are ~4–5 levels deep, so a lookup is ~4–5 page reads. This is why it's O(log n).
2. **Sorted leaves, linked together.** Because keys are ordered and leaf pages link to their neighbors, B-trees serve not just `=` but **range** queries (`>`, `<`, `BETWEEN`), `ORDER BY`, and `LIKE 'prefix%'` efficiently — just walk the leaves.

```sql
-- Create a B-tree index (the default type — no need to say "USING btree")
CREATE INDEX idx_users_email ON users (email);

-- A UNIQUE index doubles as a uniqueness constraint
CREATE UNIQUE INDEX idx_users_email_uq ON users (email);

-- The PRIMARY KEY and UNIQUE constraints AUTOMATICALLY create an index. FKs do NOT.
```

> **Gotcha — foreign keys are NOT automatically indexed (in Postgres & MySInnoDB-aside).** The PK side is indexed, but the *referencing* column (`orders.user_id`) is not — yet you join and filter on it constantly, and `ON DELETE CASCADE` scans it. **Manually index every foreign key column.** This is one of the most common real-world performance oversights.

---

## III. CLUSTERED vs NON-CLUSTERED INDEXES

This distinction shapes how a database physically stores rows.

- **Clustered index** — the table's rows are *physically stored in the index's order*. There can be only **one** (the data can only be sorted one way). The leaf *is* the row.
- **Non-clustered (secondary) index** — a separate structure whose leaves hold pointers back to the actual rows. You can have **many**.

```
Clustered (rows live in the index):     Non-clustered (index points to rows):
 [1 | full row][2 | full row]...         [email→ptr][email→ptr]... → heap/clustered table
```

| | **PostgreSQL** | **MySQL (InnoDB)** | **SQL Server** |
|---|---------------|--------------------|----------------|
| Default storage | **Heap** (unordered) + all indexes are secondary | Table **is** clustered by the **primary key** | Heap unless you add a clustered index |
| Clustered index | No true clustered index (`CLUSTER` is a one-time reorder) | Always one (the PK) | One, you choose |
| Secondary index leaf points to | Physical row location (`ctid`) | The **PK value** (then a second lookup) | Row locator / clustering key |

> **Gotcha — InnoDB secondary indexes do a "double lookup."** Because an InnoDB secondary index stores the **primary key** (not a direct row pointer), looking up by a secondary index finds the PK, then walks the clustered index to fetch the row. This is why a **fat primary key** (e.g. a long natural string PK) bloats *every* secondary index in MySQL — another vote for compact surrogate keys (file 01).

---

## IV. COMPOSITE, COVERING, AND PARTIAL INDEXES

### Composite (multi-column) indexes — order is everything

```sql
-- Index on (user_id, created_at) — sorted by user_id first, THEN created_at
CREATE INDEX idx_orders_user_date ON orders (user_id, created_at);
```

A composite index works like a phone book sorted by *(last name, first name)*. The **leftmost-prefix rule** governs which queries it helps:

```sql
-- ✅ Uses the index (filters on the leading column, or a left-prefix)
WHERE user_id = 5
WHERE user_id = 5 AND created_at > '2024-01-01'
WHERE user_id = 5 ORDER BY created_at          -- index already in this order → no sort!

-- ❌ Cannot use this index efficiently (skips the leading column)
WHERE created_at > '2024-01-01'                -- no user_id → can't use idx_orders_user_date
```

> **Rule — put the most-filtered / equality columns first.** Equality predicates (`=`) should precede range predicates (`>`, `BETWEEN`) in a composite index, because once you hit a range, the columns after it are no longer sorted usefully. `(status, created_at)` beats `(created_at, status)` for `WHERE status='paid' AND created_at > ...`.

### Covering indexes — answer the query from the index alone

If an index contains **every column a query needs**, the database never touches the table — an **index-only scan**. This is the fastest possible read.

```sql
-- Query needs user_id (filter) and total (output). Put both in the index.
CREATE INDEX idx_cover ON orders (user_id) INCLUDE (total);  -- Postgres 11+ INCLUDE
-- Now: SELECT total FROM orders WHERE user_id = 5;  → index-only scan, no table fetch
```

> `INCLUDE` columns ride along in the index leaves without being part of the sort key. MySQL achieves covering by adding the columns to the composite index itself.

### Partial indexes — index only the rows you query

```sql
-- Only ~2% of orders are 'pending', and that's all the dashboard queries.
-- Index ONLY those rows → tiny index, faster, cheaper to maintain.
CREATE INDEX idx_pending ON orders (created_at) WHERE status = 'pending';

-- Enforce "one primary address per user" with a partial UNIQUE index
CREATE UNIQUE INDEX one_primary ON addresses (user_id) WHERE is_primary;
```

> **MySQL note.** MySQL has **no partial indexes** and no `INCLUDE`. It offers *prefix* indexes (index the first N chars of a string: `INDEX(name(10))`) which Postgres handles differently (expression indexes). Partial indexes are a notable Postgres advantage.

### Expression (functional) indexes

```sql
-- A query like WHERE LOWER(email) = '...' can't use a plain email index.
-- Index the EXPRESSION instead:
CREATE INDEX idx_email_lower ON users (LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'ada@x.com';   -- now uses the index
```

---

## V. OTHER INDEX TYPES (BEYOND B-TREE)

| Type | Good for | Not for | Notes |
|------|----------|---------|-------|
| **B-tree** | `=`, `<`, `>`, `BETWEEN`, `ORDER BY`, prefix `LIKE` | Full-text, containment | The default; use unless you have a reason not to |
| **Hash** | `=` only | Ranges, sorting | Fast equality; Postgres has it but B-tree usually wins |
| **GIN** | Full-text search, `JSONB`, arrays, containment (`@>`) | Range/sort | "Inverted" index; great for multi-value columns |
| **GiST** | Geometric/spatial, ranges, nearest-neighbor | Plain equality | Extensible; PostGIS builds on it |
| **BRIN** | Huge tables with natural ordering (time-series) | Random data | Tiny; stores per-block ranges, not per-row |

```sql
CREATE INDEX idx_doc_fts ON docs USING GIN (to_tsvector('english', body));  -- full-text
CREATE INDEX idx_meta    ON events USING GIN (metadata);                     -- JSONB queries
CREATE INDEX idx_logs_t  ON logs USING BRIN (created_at);                    -- append-only time data
```

---

## VI. WHEN INDEXES HURT — AND WHEN THEY'RE IGNORED

Indexes are not free wins. Add them thoughtfully.

**Indexes cost you when:**
- **Writes dominate.** Every `INSERT`/`UPDATE`/`DELETE` must update every affected index. A write-heavy table with 8 indexes pays 8× index-maintenance on writes.
- **Low selectivity / cardinality.** Indexing a `boolean` or `gender` column rarely helps — if a value matches 50% of rows, scanning the table is *cheaper* than bouncing between index and table. Indexes win when a predicate is **selective** (returns a small fraction of rows).
- **Small tables.** A 200-row table is faster to scan than to index-traverse. The planner will (correctly) ignore the index.
- **Bloat & space.** Indexes consume disk and memory (buffer cache competition).

**The planner ignores your index when:**

```sql
-- ❌ Wrapping the column in a function defeats a plain index (it indexed `email`, not LOWER(email))
WHERE LOWER(email) = 'ada@x.com'        -- needs an expression index (section IV)

-- ❌ Leading wildcard — can't use a sorted B-tree
WHERE name LIKE '%pen%'                 -- needs trigram/GIN index

-- ❌ Implicit type mismatch forces a cast on the column
WHERE user_id = '5'                     -- if user_id is INT, the cast can disable the index

-- ❌ Low selectivity — returning most of the table → seq scan is cheaper
WHERE is_active = true                  -- when 95% of rows are active
```

> **The term to know: *SARGable* (Search-ARGument-able).** A predicate is SARGable if the database can use an index for it — meaning the indexed **column stands alone** on one side. `WHERE created_at >= now() - INTERVAL '7 days'` is SARGable; `WHERE created_at + INTERVAL '7 days' >= now()` is **not** (the column is wrapped in arithmetic). Keep the column bare; move computation to the other side.

---

## VII. EXPLAIN — SEEING HOW THE DATABASE RUNS YOUR QUERY

`EXPLAIN` shows the **query plan**: the steps the planner chose. `EXPLAIN ANALYZE` actually *runs* the query and reports real timings and row counts. This is the single most important skill in query tuning — stop guessing, read the plan.

```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 5;            -- estimated plan, doesn't run

EXPLAIN ANALYZE SELECT * FROM orders WHERE user_id = 5;    -- runs it; real numbers
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)                    -- + cache hits/misses
    SELECT * FROM orders WHERE user_id = 5;
```

Reading a plan (Postgres example):

```
Seq Scan on orders  (cost=0.00..18584.00 rows=12 width=40)
                    (actual time=0.015..142.331 rows=12 loops=1)
  Filter: (user_id = 5)
  Rows Removed by Filter: 999988            ← scanned a million to return 12. BAD.
Planning Time: 0.1 ms
Execution Time: 142.4 ms
```

After adding `CREATE INDEX idx_orders_user_id ON orders(user_id);`:

```
Index Scan using idx_orders_user_id on orders  (cost=0.42..8.46 rows=12 width=40)
                                               (actual time=0.021..0.038 rows=12 loops=1)
  Index Cond: (user_id = 5)
Execution Time: 0.06 ms                       ← ~2000× faster
```

### What the numbers mean

| Field | Meaning |
|-------|---------|
| `cost=0.00..18584.00` | Planner's estimated cost: *startup..total* (arbitrary units, lower is better) |
| `rows=12` | **Estimated** rows returned |
| `actual ... rows=12 loops=1` | **Real** rows and how many times the node ran (`ANALYZE` only) |
| `Rows Removed by Filter` | Rows scanned then discarded — high = wasteful scan |
| `width` | Average row size in bytes |

> **Gotcha — estimated rows wildly different from actual rows = stale statistics.** If `EXPLAIN` estimates 5 rows but `ANALYZE` shows 500,000, the planner is working from bad statistics and will choose bad plans. Run `ANALYZE table_name;` to refresh them (section IX).

---

## VIII. READING SCAN & JOIN STRATEGIES

### Scan types (how a single table is read)

| Plan node | What it does | Good or bad? |
|-----------|--------------|--------------|
| **Seq Scan** | Read every row | Fine for small tables / low selectivity; **bad** when filtering for few rows in a big table |
| **Index Scan** | Walk the index, fetch matching rows from the table | Good for selective filters |
| **Index Only Scan** | Answer entirely from the index (covering) | **Best** — no table access |
| **Bitmap Index Scan** | Build a bitmap of matching rows, then fetch in physical order | Good for medium selectivity / combining indexes |

### Join strategies (how two tables are joined)

| Strategy | How | Best when |
|----------|-----|-----------|
| **Nested Loop** | For each outer row, look up matches in inner (ideally via index) | Small outer set + indexed inner |
| **Hash Join** | Build a hash table on one side, probe with the other | Large, unsorted inputs; equality joins |
| **Merge Join** | Sort both sides, walk in lockstep | Both inputs already sorted (e.g. on indexed keys) |

> You don't *choose* the strategy — the planner does, from cost estimates. Your job is to give it good indexes and accurate statistics, then verify it made a sane choice. A nested loop over a million unindexed rows is the classic "why is this query 30 seconds" culprit.

---

## IX. STATISTICS & THE QUERY PLANNER

The planner is a **cost-based optimizer**: it estimates the cost of alternative plans using **statistics** about your data (row counts, value distributions, how many distinct values, most common values) and picks the cheapest. Those statistics must be current.

```sql
ANALYZE orders;                 -- refresh statistics for one table
ANALYZE;                        -- whole database
VACUUM ANALYZE orders;          -- reclaim dead-row space AND refresh stats (Postgres)

-- Postgres autovacuum usually keeps stats fresh automatically, but bulk loads,
-- big deletes, or a fresh restore can leave them stale — analyze manually then.

-- Inspect what the planner believes:
SELECT attname, n_distinct, most_common_vals
FROM pg_stats WHERE tablename = 'orders';
```

> **MySQL note.** MySQL/InnoDB maintains index statistics automatically and updates them on `ANALYZE TABLE orders;`. The principle is identical: the optimizer is only as good as its statistics.

---

## X. OPTIMIZATION PLAYBOOK

Concrete techniques, roughly in order of impact:

1. **Index the columns in `WHERE`, `JOIN`, and `ORDER BY`** — especially every **foreign key**.
2. **Keep predicates SARGable** — bare column on one side; no functions/arithmetic wrapping it.
3. **Select only needed columns** — enables covering indexes; avoid `SELECT *`.
4. **Fix the N+1 query problem** — don't run one query per row in application code; use a single `JOIN` or `IN`:

```javascript
// ❌ N+1: 1 query for users + N queries for each user's orders (app code)
const users = await db.query('SELECT * FROM users');
for (const u of users) {
    u.orders = await db.query('SELECT * FROM orders WHERE user_id = $1', [u.id]); // N queries!
}
// ✅ One query with a JOIN (or one IN query), then group in app code
const rows = await db.query(`
    SELECT u.id, u.username, o.id AS order_id, o.total
    FROM users u LEFT JOIN orders o ON o.user_id = u.id`);
```

5. **Use keyset pagination** instead of deep `OFFSET` (file 03).
6. **Batch writes** — one multi-row `INSERT` beats a thousand single inserts.
7. **Avoid functions on indexed columns**; add an expression index if you must compute.
8. **Denormalize or use a materialized view** (file 05) for expensive, read-heavy aggregations — *after* measuring.
9. **Watch for over-indexing** — drop unused indexes (they slow writes). Find them:

```sql
-- Postgres: indexes that have never been used since stats reset
SELECT indexrelid::regclass AS index, idx_scan AS times_used
FROM pg_stat_user_indexes WHERE idx_scan = 0 ORDER BY 1;
```

10. **Maintain indexes** — heavily updated indexes bloat; `REINDEX` occasionally.

---

## XI. WHEN TO DENORMALIZE FOR PERFORMANCE (REVISITED)

File 01 introduced denormalization conceptually; here's the performance lens. *After* you've indexed correctly and read the plan, if an aggregation is still the bottleneck and reads dwarf writes, materialize it:

```sql
-- Option A: a cached column kept in sync by a trigger (file 08)
ALTER TABLE orders ADD COLUMN item_count INT NOT NULL DEFAULT 0;

-- Option B: a materialized view refreshed on a schedule (file 05)
CREATE MATERIALIZED VIEW user_stats AS
SELECT user_id, COUNT(*) AS orders, SUM(total) AS revenue
FROM orders GROUP BY user_id;
```

> **Order of operations: measure → index → rewrite query → *then* denormalize.** Denormalization adds sync complexity (and bugs). Reach for it only when indexing and query rewriting have been exhausted and the numbers prove the need.

---

## XII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Unindexed foreign keys | Slow joins & cascade deletes | Index every FK column |
| Function on an indexed column | Index ignored, seq scan | Expression index, or keep column bare (SARGable) |
| Indexing low-selectivity columns | Index unused; wasted writes | Index selective columns; consider partial indexes |
| Too many indexes | Slow writes, bloat | Drop unused indexes (`pg_stat_user_indexes`) |
| Wrong composite-index column order | Index not used for your filter | Equality cols first, then range; match query shape |
| Leading-wildcard `LIKE '%x'` | Full scan | Trigram/GIN or full-text index |
| Deep `OFFSET` pagination | Slow on big tables | Keyset pagination |
| N+1 queries from app code | Hundreds of tiny queries | One `JOIN`/`IN` query |
| Stale statistics | Planner picks bad plans | `ANALYZE` / `VACUUM ANALYZE` |
| Trusting `EXPLAIN` estimates as truth | Misdiagnosis | Use `EXPLAIN ANALYZE` for *actual* numbers |
| Premature denormalization | Sync bugs for no measured gain | Index & rewrite first; measure |

---

## 🧠 KEY TAKEAWAYS

- An **index** trades write cost and disk for fast reads, turning O(n) scans into ~O(log n) lookups; the default **B-tree** also serves ranges, sorting, and prefix `LIKE`.
- **Always index foreign keys** (they aren't automatic) and the columns in `WHERE`/`JOIN`/`ORDER BY`.
- Understand **clustered vs non-clustered** storage: Postgres tables are heaps with secondary indexes; InnoDB clusters by the PK and does a double lookup on secondary indexes (so keep PKs compact).
- Use **composite** indexes with equality columns first (leftmost-prefix rule), **covering**/`INCLUDE` indexes for index-only scans, and **partial**/expression indexes to target specific queries.
- Indexes **hurt** on write-heavy tables, low-selectivity columns, and small tables; the planner **ignores** them for non-**SARGable** predicates (functions/wildcards/type mismatches).
- **Read the plan**: `EXPLAIN ANALYZE` reveals seq vs index scans and nested-loop/hash/merge joins; mismatched estimated vs actual rows means **stale statistics** — run `ANALYZE`.
- Optimize in order: **index → keep predicates SARGable → select fewer columns → kill N+1 → keyset paginate → (only then) denormalize**.

---

**Prev:** [`05-Aggregation-And-Advanced-Queries.md`](./05-Aggregation-And-Advanced-Queries.md) · **Next:** [`07-Transactions-And-Concurrency.md`](./07-Transactions-And-Concurrency.md) · **Index:** [`00-Index.md`](./00-Index.md)
