# 🗄️ 05 — Aggregation & Advanced Queries

> *"Anyone can fetch a row. The engineer earns their title at the aggregate: turning a million rows into the one number a decision rests on."*

**Prev:** [`04-Joins-And-Relationships.md`](./04-Joins-And-Relationships.md) · **Next:** [`06-Indexing-And-Query-Optimization.md`](./06-Indexing-And-Query-Optimization.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. AGGREGATE FUNCTIONS — MANY ROWS INTO ONE VALUE

An **aggregate function** collapses a set of rows into a single value. Used without `GROUP BY`, it collapses the *whole table* into one row.

```sql
SELECT
    COUNT(*)        AS num_orders,     -- count ALL rows (including NULLs)
    COUNT(note)     AS with_note,      -- count rows where note IS NOT NULL
    COUNT(DISTINCT user_id) AS buyers, -- count distinct non-null user_ids
    SUM(total)      AS revenue,        -- add up totals
    AVG(total)      AS avg_total,      -- mean (ignores NULLs)
    MIN(total)      AS cheapest,
    MAX(total)      AS priciest
FROM orders;
```

| Function | Returns | NULL behavior |
|----------|---------|---------------|
| `COUNT(*)` | Number of rows | Counts every row |
| `COUNT(col)` | Rows where `col` is not null | Ignores NULLs |
| `COUNT(DISTINCT col)` | Distinct non-null values | Ignores NULLs |
| `SUM(col)` | Total | Ignores NULLs (NULL if no rows) |
| `AVG(col)` | Mean | Ignores NULLs (denominator excludes them) |
| `MIN`/`MAX(col)` | Extremes | Ignore NULLs |
| `STRING_AGG(col, ',')` | Concatenated string | Ignores NULLs |
| `ARRAY_AGG(col)` | Array of values | Includes NULLs |

```sql
-- STRING_AGG / ARRAY_AGG: gather a group's values into one cell (Postgres)
SELECT user_id, STRING_AGG(status, ', ' ORDER BY id) AS statuses
FROM orders GROUP BY user_id;
-- MySQL equivalent: GROUP_CONCAT(status ORDER BY id SEPARATOR ', ')
```

> **Gotcha — `AVG` ignores NULL, it does not treat it as 0.** `AVG` of `(10, 20, NULL)` is `15` (sum 30 / count 2), not `10`. If a NULL should count as zero in the average, wrap it: `AVG(COALESCE(col, 0))`.

> **Gotcha — `SUM` of no rows is `NULL`, not 0.** `SELECT SUM(total) FROM orders WHERE 1=0` returns `NULL`. Use `COALESCE(SUM(total), 0)` when you need a numeric zero.

---

## II. GROUP BY — AGGREGATING PER GROUP

`GROUP BY` partitions rows into groups by one or more columns, then applies aggregates **per group** — one output row per group.

```sql
-- Revenue and order count PER user
SELECT
    user_id,
    COUNT(*)   AS num_orders,
    SUM(total) AS revenue
FROM orders
GROUP BY user_id
ORDER BY revenue DESC;

-- Group by multiple columns → one row per unique COMBINATION
SELECT user_id, status, COUNT(*)
FROM orders
GROUP BY user_id, status;

-- Group by an expression (e.g. revenue per month)
SELECT DATE_TRUNC('month', created_at) AS month, SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', created_at)   -- (or GROUP BY month — Postgres allows the alias)
ORDER BY month;
```

> **THE cardinal rule of `GROUP BY`:** every column in the `SELECT` list must be **either** inside an aggregate function **or** listed in `GROUP BY`. Otherwise the database can't decide *which* of the many grouped values to show.

```sql
-- ❌ ERROR: "username" is neither grouped nor aggregated — which username for the group?
SELECT user_id, username, SUM(total) FROM orders GROUP BY user_id;

-- ✅ Fix A: group by it too
SELECT user_id, SUM(total) FROM orders GROUP BY user_id;
-- ✅ Fix B: aggregate it (if it varies, pick one with MAX/MIN, or join after grouping)
```

> **Gotcha — MySQL historically let you break this rule.** Old MySQL (with `ONLY_FULL_GROUP_BY` disabled) returned an *arbitrary* value for ungrouped columns — a silent source of wrong data. Modern MySQL enables `ONLY_FULL_GROUP_BY` by default, matching the standard. Postgres always enforced it.

### GROUPING SETS, ROLLUP, CUBE — multi-level subtotals

```sql
-- ROLLUP: subtotals + grand total (hierarchical). Great for reports.
SELECT category_id, status, SUM(total)
FROM orders_with_cat
GROUP BY ROLLUP (category_id, status);
-- yields: each (category,status), each category subtotal, AND the grand total

-- CUBE: every combination of subtotals across the listed columns
GROUP BY CUBE (category_id, status);

-- GROUPING SETS: you pick exactly which groupings to compute
GROUP BY GROUPING SETS ((category_id), (status), ());
```

---

## III. HAVING — FILTERING GROUPS

`WHERE` filters **rows** (before grouping). `HAVING` filters **groups** (after grouping). You need `HAVING` to filter on an aggregate.

```sql
-- Users who have spent more than $100 total (filter on an aggregate → HAVING)
SELECT user_id, SUM(total) AS revenue
FROM orders
GROUP BY user_id
HAVING SUM(total) > 100;          -- ✅ can't use WHERE here — the SUM doesn't exist yet

-- Combine both: WHERE narrows rows first, HAVING filters the resulting groups
SELECT user_id, COUNT(*) AS paid_orders
FROM orders
WHERE status = 'paid'             -- row filter: only paid orders enter the grouping
GROUP BY user_id
HAVING COUNT(*) >= 3;             -- group filter: keep users with 3+ paid orders
```

| Clause | Filters | Runs | Can reference aggregates? |
|--------|---------|------|---------------------------|
| `WHERE` | Individual rows | Before `GROUP BY` | ❌ No |
| `HAVING` | Groups | After `GROUP BY` | ✅ Yes |

> **Performance tip — filter in `WHERE`, not `HAVING`, when you can.** `WHERE status='paid'` discards rows *before* the expensive grouping. Putting a non-aggregate condition in `HAVING` makes the database group everything first, then throw groups away — wasteful. Use `HAVING` only for conditions on aggregates.

---

## IV. SUBQUERIES — A QUERY INSIDE A QUERY

A **subquery** (inner query) feeds a result to an outer query. Four flavors by what they return and where they sit.

### Scalar subquery — returns one value

```sql
-- Products priced above the overall average
SELECT name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);   -- inner returns ONE number

-- Scalar subquery in the SELECT list (a per-row lookup)
SELECT
    name,
    price,
    price - (SELECT AVG(price) FROM products) AS diff_from_avg
FROM products;
```

> **Gotcha — a scalar subquery must return at most one row & one column.** If `(SELECT id FROM users WHERE email = ?)` returns two rows, you get a runtime error: "more than one row returned by a subquery used as an expression." Add `LIMIT 1` or fix the filter.

### Subquery with IN / NOT IN — returns a column

```sql
-- Users who have placed at least one order
SELECT username FROM users
WHERE id IN (SELECT user_id FROM orders);

-- Products NEVER ordered  (beware NULLs — see file 03; prefer NOT EXISTS)
SELECT name FROM products
WHERE id NOT IN (SELECT product_id FROM order_items WHERE product_id IS NOT NULL);
```

### Subquery in FROM — a derived table

```sql
-- Treat a subquery's result as a table you can join/filter
SELECT bucket, COUNT(*)
FROM (
    SELECT id,
           CASE WHEN total > 100 THEN 'big' ELSE 'small' END AS bucket
    FROM orders
) AS classified                  -- derived tables MUST be aliased
GROUP BY bucket;
```

### Correlated subquery — references the outer row

```sql
-- For each user, their most recent order total — the inner query depends on the OUTER row
SELECT u.username,
       (SELECT o.total FROM orders o
        WHERE o.user_id = u.id            -- ← references u from the outer query
        ORDER BY o.created_at DESC LIMIT 1) AS latest_total
FROM users u;
```

> **Gotcha — correlated subqueries can be slow.** A correlated subquery conceptually re-runs *once per outer row* (O(n×m)). For large tables, a `JOIN` or a window function (section VI) is usually far faster. Modern planners sometimes rewrite them, but don't count on it — check the plan (file 06).

### EXISTS / NOT EXISTS — test for existence

```sql
-- EXISTS short-circuits on the first matching row — efficient existence test
SELECT u.username FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);    -- users WITH orders

SELECT u.username FROM users u
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id); -- users WITHOUT orders
```

| Pattern | Best for | Notes |
|---------|----------|-------|
| `IN (subquery)` | Small, NULL-free value lists | Readable; NULL-fragile with `NOT IN` |
| `EXISTS (subquery)` | "Does any related row exist?" | NULL-safe; short-circuits; usually fastest |
| `JOIN` | Need columns *from* the other table | Can duplicate rows (use `DISTINCT`/aggregate) |
| `= ANY` / `> ALL` | Compare against a set | `= ANY` ≡ `IN`; `<> ALL` ≡ `NOT IN` |

```sql
-- ANY / ALL: compare a value against every element of a set
SELECT name FROM products WHERE price > ALL (SELECT price FROM products WHERE category_id=1);
SELECT name FROM products WHERE price = ANY (SELECT price FROM clearance);  -- = ANY is just IN
```

---

## V. COMMON TABLE EXPRESSIONS (CTEs) — THE `WITH` CLAUSE

A **CTE** names a subquery up front, so the main query reads top-to-bottom like a pipeline. CTEs make complex queries *readable* and let you reference the same intermediate result multiple times.

```sql
-- Without CTEs, this nests into an unreadable ball. With them, it's a pipeline.
WITH user_revenue AS (              -- step 1: revenue per user
    SELECT user_id, SUM(total) AS revenue
    FROM orders
    WHERE status = 'paid'
    GROUP BY user_id
),
ranked AS (                          -- step 2: build on the first CTE
    SELECT user_id, revenue,
           revenue > 1000 AS is_vip
    FROM user_revenue
)
SELECT u.username, r.revenue, r.is_vip   -- step 3: final query uses the CTEs
FROM ranked r
JOIN users u ON u.id = r.user_id
ORDER BY r.revenue DESC;
```

> **CTE vs subquery — readability vs (sometimes) performance.** CTEs are usually clearer. In older Postgres (< 12), CTEs were an *optimization fence* — always materialized, sometimes slower than an equivalent subquery. Postgres 12+ can inline non-recursive CTEs (or you force it with `MATERIALIZED`/`NOT MATERIALIZED`). Prefer CTEs for clarity; check the plan if performance matters.

### Recursive CTEs — querying hierarchies and graphs

A **recursive CTE** references itself, processing tree/graph structures of arbitrary depth — something plain joins can't do.

```sql
-- Full management chain under the CEO (employees table from file 04)
WITH RECURSIVE org_chart AS (
    -- ANCHOR: the starting row(s) — the top of the tree
    SELECT id, name, manager_id, 1 AS depth
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- RECURSIVE term: join the table to the rows produced SO FAR
    SELECT e.id, e.name, e.manager_id, oc.depth + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.id   -- ← references the CTE itself
)
SELECT REPEAT('  ', depth - 1) || name AS tree, depth
FROM org_chart
ORDER BY depth;
```

```sql
-- Classic: generate a series of numbers/dates without a numbers table
WITH RECURSIVE nums(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM nums WHERE n < 10        -- termination condition is ESSENTIAL
)
SELECT n FROM nums;   -- 1..10
```

> **Gotcha — a recursive CTE without a termination condition runs forever.** The recursive term must eventually return no rows (here `WHERE n < 10`). If your data has cycles (A manages B manages A), you also need cycle detection (track visited IDs in an array, or use Postgres's `CYCLE` clause), or the query loops infinitely.

---

## VI. WINDOW FUNCTIONS — AGGREGATES WITHOUT COLLAPSING ROWS

This is the feature that separates intermediate from advanced SQL. A **window function** computes across a set of rows *related to the current row*, but — unlike `GROUP BY` — **keeps every row**. You get the aggregate *and* the detail in one result.

```sql
-- GROUP BY collapses; window keeps each row AND adds the group total beside it.
SELECT
    id, user_id, total,
    SUM(total)   OVER (PARTITION BY user_id) AS user_total,   -- per-user total on every row
    AVG(total)   OVER ()                     AS overall_avg,  -- empty OVER() = whole table
    total - AVG(total) OVER (PARTITION BY user_id) AS vs_user_avg
FROM orders;
```

The `OVER (...)` clause defines the **window**:
- `PARTITION BY` — split rows into groups (like `GROUP BY`, but rows survive).
- `ORDER BY` — order rows *within* the partition (required for ranking and running totals).
- frame (`ROWS`/`RANGE BETWEEN ...`) — which rows around the current one are in scope.

### Ranking functions

```sql
SELECT
    user_id, total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY total DESC) AS rn,   -- 1,2,3,4 (no ties)
    RANK()       OVER (PARTITION BY user_id ORDER BY total DESC) AS rnk,  -- 1,2,2,4 (gaps on ties)
    DENSE_RANK() OVER (PARTITION BY user_id ORDER BY total DESC) AS drnk, -- 1,2,2,3 (no gaps)
    NTILE(4)     OVER (ORDER BY total)                          AS quartile -- buckets 1–4
FROM orders;
```

| Function | On ties (e.g. values 90, 90) | Use for |
|----------|------------------------------|---------|
| `ROW_NUMBER()` | 1, 2 (arbitrary order) | Unique sequential number; "pick one per group" |
| `RANK()` | 1, 1, 3 (skips 2) | Standings where ties share a place |
| `DENSE_RANK()` | 1, 1, 2 (no skip) | Ranking without gaps |
| `NTILE(n)` | Splits into n buckets | Quartiles, percentiles, pagination buckets |

```sql
-- THE killer pattern: "top N per group" — the most-asked SQL interview question.
-- "Most expensive product in each category":
WITH ranked AS (
    SELECT name, category_id, price,
           ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) AS rn
    FROM products
)
SELECT name, category_id, price FROM ranked WHERE rn = 1;
```

### LAG / LEAD — peek at other rows

```sql
-- Compare each month's revenue to the previous month (LAG looks BACKWARD)
SELECT
    month, revenue,
    LAG(revenue)  OVER (ORDER BY month) AS prev_month,
    revenue - LAG(revenue) OVER (ORDER BY month) AS change,
    LEAD(revenue) OVER (ORDER BY month) AS next_month   -- LEAD looks FORWARD
FROM monthly_revenue;
```

### Running totals and moving averages (frames)

```sql
-- Running (cumulative) total: all rows from the start up to the current row
SELECT
    created_at, total,
    SUM(total) OVER (ORDER BY created_at
                     ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total,
    -- 3-row moving average (current + 2 preceding)
    AVG(total) OVER (ORDER BY created_at
                     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3,
    FIRST_VALUE(total) OVER (ORDER BY created_at) AS first_total,
    LAST_VALUE(total)  OVER (ORDER BY created_at
                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_total
FROM orders;
```

> **Gotcha — the default frame surprises everyone.** When you add `ORDER BY` to an `OVER()`, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — i.e. a *running* aggregate, not the whole partition. So `LAST_VALUE(x) OVER (ORDER BY t)` returns the *current* row's value, not the partition's last. To get the true last value, specify `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

> **Gotcha — window functions run after `WHERE`/`GROUP BY`/`HAVING`.** You cannot filter on a window function in `WHERE` (it doesn't exist yet). Wrap it in a CTE/subquery and filter in the outer query — exactly the "top N per group" pattern above.

---

## VII. VIEWS & MATERIALIZED VIEWS

A **view** is a stored, named query — a virtual table. It runs its underlying query every time you select from it. Views hide complexity, enforce a stable interface, and centralize logic (like that `WHERE deleted_at IS NULL` from file 02).

```sql
-- Create a view: now anyone can "SELECT * FROM active_user_revenue" without the gnarly query
CREATE VIEW active_user_revenue AS
SELECT u.id, u.username, COALESCE(SUM(o.total), 0) AS revenue
FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'paid'
WHERE u.is_active                              -- assume an is_active flag
GROUP BY u.id, u.username;

SELECT * FROM active_user_revenue WHERE revenue > 500;  -- query it like a table

CREATE OR REPLACE VIEW active_user_revenue AS ...;       -- redefine it
DROP VIEW active_user_revenue;
```

A **materialized view** stores the *result* physically. Reads are fast (no recomputation), but the data is a snapshot — you must `REFRESH` it.

```sql
CREATE MATERIALIZED VIEW daily_sales AS
SELECT DATE_TRUNC('day', created_at) AS day, SUM(total) AS revenue
FROM orders GROUP BY 1;

REFRESH MATERIALIZED VIEW daily_sales;                    -- recompute (locks reads)
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_sales;       -- recompute without blocking reads
                                                          -- (needs a UNIQUE index on the MV)
```

| | **View** | **Materialized view** |
|---|---------|----------------------|
| Stores | Just the query definition | The actual result data |
| Freshness | Always live (recomputed each read) | Stale until you `REFRESH` |
| Read speed | As slow as the query | Fast (precomputed) |
| Write cost | None | Pay on `REFRESH` |
| Use for | Simplifying/standardizing queries | Expensive aggregations read often |

> **MySQL note.** MySQL supports regular views but has **no materialized views** — emulate them with a real table that a scheduled job (or trigger) refreshes. Postgres and Oracle support them natively.

> **Updatable views.** A simple view (one table, no aggregation) can often be written through — `INSERT`/`UPDATE` on the view hit the base table. Complex views (joins, `GROUP BY`) are read-only unless you add an `INSTEAD OF` trigger (file 08).

---

## VIII. A CAPSTONE QUERY — EVERYTHING TOGETHER

```sql
-- "For each category, the top-3 products by revenue, with each product's share
--  of its category's total revenue and rank — readable as a pipeline."
WITH product_revenue AS (                        -- 1. revenue per product
    SELECT p.id, p.name, p.category_id,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM products p
    JOIN order_items oi ON oi.product_id = p.id
    GROUP BY p.id, p.name, p.category_id
),
ranked AS (                                       -- 2. rank within category + category total (window)
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY revenue DESC) AS rank_in_cat,
           SUM(revenue) OVER (PARTITION BY category_id) AS cat_revenue
    FROM product_revenue
)
SELECT c.name AS category, r.name AS product, r.revenue,
       ROUND(100.0 * r.revenue / r.cat_revenue, 1) AS pct_of_category
FROM ranked r
JOIN categories c ON c.id = r.category_id
WHERE r.rank_in_cat <= 3                          -- 3. filter the window result (must be outer)
ORDER BY c.name, r.revenue DESC;
```

---

## IX. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Non-aggregated column not in `GROUP BY` | Error (or wrong value in old MySQL) | Group it or aggregate it |
| Filtering an aggregate in `WHERE` | "aggregate functions are not allowed in WHERE" | Use `HAVING` |
| Non-aggregate filter in `HAVING` | Slow (groups everything first) | Move it to `WHERE` |
| `SUM`/`AVG` over zero rows | `NULL` instead of 0 | `COALESCE(SUM(x), 0)` |
| `NOT IN` with NULLs | Zero rows returned | Use `NOT EXISTS` |
| Scalar subquery returns >1 row | Runtime error | `LIMIT 1` or fix the filter |
| Correlated subquery on big tables | Very slow (per-row) | Rewrite as join or window function |
| Recursive CTE with no termination | Infinite loop | Add a stopping condition / cycle detection |
| `LAST_VALUE` returns current row | Default frame is up-to-current | Specify full `ROWS BETWEEN ... UNBOUNDED FOLLOWING` |
| Filtering a window function in `WHERE` | "window functions not allowed in WHERE" | Wrap in CTE/subquery, filter outside |
| Reading a stale materialized view | Old numbers | `REFRESH` (consider `CONCURRENTLY`) |

---

## 🧠 KEY TAKEAWAYS

- **Aggregates** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`) collapse rows; they **ignore NULLs**, and `SUM`/`AVG` over no rows is `NULL` (use `COALESCE`).
- `GROUP BY` aggregates per group; every selected column must be **grouped or aggregated**. `WHERE` filters rows *before* grouping; `HAVING` filters groups *after*.
- **Subqueries** come in scalar, `IN`, derived-table, and **correlated** forms; prefer **`EXISTS`** for existence tests and watch correlated subqueries for O(n×m) cost.
- **CTEs (`WITH`)** turn nested queries into readable pipelines; **recursive CTEs** traverse hierarchies and graphs (always with a termination condition).
- **Window functions** compute aggregates/rankings **without collapsing rows** — `ROW_NUMBER`/`RANK`/`DENSE_RANK`, `LAG`/`LEAD`, and `SUM/AVG OVER (PARTITION BY ... ORDER BY ...)` — and power the "top N per group" pattern.
- Mind the **default window frame** (running, up to current row) and that window functions can't be filtered in `WHERE` (wrap and filter outside).
- **Views** simplify and standardize queries; **materialized views** trade freshness for speed and must be `REFRESH`ed (MySQL lacks them natively).

---

**Prev:** [`04-Joins-And-Relationships.md`](./04-Joins-And-Relationships.md) · **Next:** [`06-Indexing-And-Query-Optimization.md`](./06-Indexing-And-Query-Optimization.md) · **Index:** [`00-Index.md`](./00-Index.md)
