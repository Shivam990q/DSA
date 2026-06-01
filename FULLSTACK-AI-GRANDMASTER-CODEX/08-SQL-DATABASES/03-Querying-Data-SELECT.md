# 🗄️ 03 — Querying Data: `SELECT`

> *"`SELECT` is the universal interface to truth. Every dashboard, every report, every API response, every ML feature — all of it is a `SELECT` underneath. Master `SELECT` and the data bows."*

**Prev:** [`02-SQL-Basics-DDL-And-DML.md`](./02-SQL-Basics-DDL-And-DML.md) · **Next:** [`04-Joins-And-Relationships.md`](./04-Joins-And-Relationships.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE LOGICAL QUERY ORDER

A `SELECT` *reads* like English from `SELECT` down, but the database *executes* it in a different, **logical order**. Internalize this — it explains every "why can't I use my alias here?" mystery.

```
1. FROM        — pick the source tables (and apply joins)
2. WHERE       — filter individual rows
3. GROUP BY    — collapse rows into groups
4. HAVING      — filter groups
5. SELECT      — choose columns / compute expressions
6. DISTINCT    — drop duplicate output rows
7. ORDER BY    — sort the result
8. LIMIT/OFFSET — slice the result
```

Two huge consequences:

1. **You cannot use a `SELECT` alias in `WHERE` or `GROUP BY`** — those clauses run *before* `SELECT`. You can use it in `ORDER BY` (which runs after).
2. **Aggregates only exist after `GROUP BY`.** That's why aggregate filters live in `HAVING`, not `WHERE`.

```sql
-- ❌ Won't compile — `discounted_price` isn't known yet at WHERE time
SELECT list_price * 0.9 AS discounted_price
FROM   books
WHERE  discounted_price < 30;

-- ✅ Either repeat the expression…
SELECT list_price * 0.9 AS discounted_price
FROM   books
WHERE  list_price * 0.9 < 30;

-- ✅ …or wrap in a subquery / CTE so the alias exists at WHERE time of the outer query.
SELECT * FROM (
    SELECT book_id, list_price * 0.9 AS discounted_price FROM books
) t
WHERE discounted_price < 30;
```

---

## II. `SELECT` BASICS

```sql
-- Pick specific columns (the right way — keeps the contract stable)
SELECT book_id, title, list_price FROM books;

-- All columns (fine for ad-hoc, NEVER in production code — schema changes break callers)
SELECT * FROM books;

-- Constants and computations
SELECT 1 + 1 AS two,
       NOW() AS right_now,
       'hello' AS greeting;

-- Aliases — `AS` is optional but readable
SELECT book_id        AS id,
       title          AS name,
       list_price * 0.9 AS sale_price
FROM   books;
```

> **Gotcha — `SELECT *` in production.** It locks you to the current column order, breaks DTO mapping when columns are added, hauls back data you don't need (wasting cache and network), and prevents the planner from picking covering indexes. Use it interactively, never in stored code.

### Distinct rows

```sql
-- Drop duplicates across the SELECT list
SELECT DISTINCT city FROM customers;

-- Distinct on multiple columns = unique combinations
SELECT DISTINCT customer_id, status FROM orders;

-- Postgres-only: DISTINCT ON — keep the first row per group, by ORDER BY
-- "The most recent order per customer":
SELECT DISTINCT ON (customer_id) customer_id, order_id, placed_at
FROM   orders
ORDER  BY customer_id, placed_at DESC;
-- The DISTINCT ON columns must come first in ORDER BY.
```

`DISTINCT ON` is a Postgres super-tool — the cross-dialect equivalent uses window functions (file [`05`](./05-Aggregation-And-Advanced-Queries.md)).

---

## III. `WHERE` — FILTERING ROWS

`WHERE` evaluates a boolean expression for each row and keeps the row if it's `TRUE`.

### Comparison operators

```sql
SELECT * FROM books WHERE pages = 616;
SELECT * FROM books WHERE pages <> 616;     -- not equal (also written !=)
SELECT * FROM books WHERE pages > 500;
SELECT * FROM books WHERE pages >= 500;
SELECT * FROM books WHERE pages <  300;
SELECT * FROM books WHERE pages <= 300;
```

### Logical operators

```sql
-- AND, OR, NOT (parentheses make precedence explicit)
SELECT * FROM books
WHERE  pages > 300
  AND  list_price < 50
  AND  (genre = 'Tech' OR genre = 'Science');

-- Negation
SELECT * FROM books WHERE NOT (pages < 300);
```

| Operator | Notes |
|----------|-------|
| `AND` | Both sides true |
| `OR` | Either side true |
| `NOT` | Negation |
| `=`, `<>`, `<`, `>`, `<=`, `>=` | Comparison |
| `IS NULL`, `IS NOT NULL` | Null check (more on this below) |
| `IS DISTINCT FROM`, `IS NOT DISTINCT FROM` | Null-safe equality |
| `IN (...)` | Match any in list |
| `NOT IN (...)` | Match none — *with a NULL gotcha (below)* |
| `BETWEEN a AND b` | `>= a AND <= b` (inclusive both ends) |
| `LIKE`, `NOT LIKE`, `ILIKE` | Pattern match (`%`/`_` wildcards) |
| `~`, `~*`, `!~`, `!~*` | Regex match (Postgres) |

### `IN`, `BETWEEN`, ranges

```sql
SELECT * FROM orders WHERE status IN ('paid','shipped');
SELECT * FROM orders WHERE status NOT IN ('cancelled');

SELECT * FROM books WHERE pages BETWEEN 300 AND 600;   -- inclusive both sides
SELECT * FROM events WHERE happens_at BETWEEN '2025-01-01' AND '2025-12-31';

-- BETWEEN with timestamps is treacherous (it's <=, not <):
--   BETWEEN '2025-01-01' AND '2025-01-31' MISSES Jan 31 23:59. Prefer:
SELECT * FROM events
WHERE  happens_at >= '2025-01-01'
  AND  happens_at <  '2025-02-01';     -- half-open interval is safer
```

### `LIKE`, `ILIKE` — pattern matching

`%` matches any number of chars; `_` matches exactly one.

```sql
SELECT * FROM books WHERE title LIKE 'Clean%';     -- starts with "Clean"
SELECT * FROM books WHERE title LIKE '%Code';      -- ends with "Code"
SELECT * FROM books WHERE title LIKE '%data%';     -- contains "data"  (case-sensitive!)
SELECT * FROM books WHERE title ILIKE '%data%';    -- Postgres: case-INsensitive
SELECT * FROM books WHERE title LIKE 'C_ean%';     -- single-char wildcard

-- Escape literal % or _ with backslash (or ESCAPE '!')
SELECT * FROM logs WHERE message LIKE '50!%%' ESCAPE '!';   -- matches messages starting with "50%"
```

> **Gotcha — leading `%` defeats the index.** `LIKE 'Clean%'` can use a B-tree index; `LIKE '%Code'` cannot. For substring search at scale use a trigram (GIN) or full-text index — file [`06`](./06-Indexing-And-Query-Optimization.md).

### Regex (Postgres)

```sql
SELECT * FROM books WHERE title ~  '^[A-Z]';    -- starts with uppercase
SELECT * FROM books WHERE title ~* 'data';      -- case-insensitive
SELECT * FROM books WHERE title !~ '\\d';       -- NO digits  (note doubled backslash in SQL string)
```

---

## IV. `NULL` — THE THREE-VALUED LOGIC

`NULL` is **not** "no value" — it is "**unknown**." Anything compared with `NULL` returns `NULL` (which is treated as not-true).

```sql
SELECT NULL = NULL;         -- NULL  (unknown)
SELECT NULL <> NULL;        -- NULL
SELECT NULL = 1;            -- NULL
SELECT 1 + NULL;            -- NULL
SELECT 'abc' || NULL;       -- NULL  (string concat with NULL is NULL)

-- Use IS / IS NOT for null checks:
SELECT * FROM customers WHERE city IS NULL;
SELECT * FROM customers WHERE city IS NOT NULL;
```

### Three-valued logic table

| `A AND B` | `T` | `F` | `NULL` |
|-|-|-|-|
| `T` | T | F | NULL |
| `F` | F | F | F |
| `NULL` | NULL | F | NULL |

| `A OR B` | `T` | `F` | `NULL` |
|-|-|-|-|
| `T` | T | T | T |
| `F` | T | F | NULL |
| `NULL` | T | NULL | NULL |

### `NOT IN` + `NULL` — the most-bitten gotcha in SQL

```sql
-- If the subquery returns ANY NULL, NOT IN returns NO rows:
SELECT *
FROM   customers
WHERE  customer_id NOT IN (SELECT customer_id FROM blacklist);
-- If blacklist contains a NULL row → result is empty. Forever.

-- Safe form: NOT EXISTS (file 04/05)
SELECT *
FROM   customers c
WHERE  NOT EXISTS (
    SELECT 1 FROM blacklist b WHERE b.customer_id = c.customer_id
);
```

### `COALESCE`, `NULLIF`, `IS DISTINCT FROM`

```sql
-- COALESCE — first non-NULL argument
SELECT COALESCE(nickname, name, 'Anonymous') AS display_name FROM users;

-- NULLIF — return NULL if two args equal, else the first
SELECT NULLIF(divisor, 0) FROM stats;           -- avoid div-by-zero crash; result becomes NULL

-- Null-safe equality (treats two NULLs as equal)
SELECT * FROM logs WHERE old_value IS DISTINCT FROM new_value;
-- "Did the value actually change, even if one side is NULL?"
```

`COALESCE` is enormously useful — it gives you "default if missing" semantics anywhere expressions are allowed.

---

## V. `ORDER BY`, `LIMIT`, `OFFSET`

### Ordering

```sql
SELECT title, pages FROM books ORDER BY pages;            -- ASC by default
SELECT title, pages FROM books ORDER BY pages DESC;
SELECT title, pages FROM books ORDER BY pages DESC, title ASC;  -- tie-breakers
SELECT title, pages FROM books ORDER BY 2 DESC;            -- by column position (1-based) — readable for ad-hoc, fragile for code

-- NULL handling — by default Postgres puts NULLs LAST in ASC, FIRST in DESC. Override:
SELECT * FROM books ORDER BY published_on DESC NULLS LAST;
```

> **Gotcha — `ORDER BY` is the *only* place sorting is guaranteed.** A query without `ORDER BY` returns rows in undefined order; never depend on insertion order.

### Pagination — `LIMIT` / `OFFSET`

```sql
-- The first 10 rows
SELECT * FROM books ORDER BY title LIMIT 10;

-- Page 3, page size 10 (skip the first 20):
SELECT * FROM books ORDER BY title LIMIT 10 OFFSET 20;

-- SQL-standard form (Postgres / SQL Server / DB2):
SELECT * FROM books ORDER BY title OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

> **Gotcha — `OFFSET` is O(N).** The DB still computes and discards the first N rows. For deep pagination (page 5,000), use **keyset (seek) pagination**:

```sql
-- Page 1 (no cursor):
SELECT * FROM books ORDER BY published_on DESC, book_id DESC LIMIT 20;

-- Subsequent pages — pass the last (published_on, book_id) of the previous page:
SELECT * FROM books
WHERE  (published_on, book_id) < ('2017-03-16', 100)
ORDER  BY published_on DESC, book_id DESC
LIMIT 20;
-- O(log N) with the right index. Stable under inserts, no skipped/duplicated rows.
```

> **MySQL note:** `LIMIT 10 OFFSET 20` works. `LIMIT 20, 10` (offset, count) also works in MySQL — confusing, prefer the first form.

---

## VI. `CASE` — INLINE CONDITIONALS

`CASE` is SQL's `if/else` for expressions. Two forms:

```sql
-- Searched CASE — most flexible
SELECT order_id,
       total_amount,
       CASE
           WHEN total_amount > 1000 THEN 'big'
           WHEN total_amount > 100  THEN 'medium'
           ELSE                        'small'
       END AS bucket
FROM orders;

-- Simple CASE — compares one expression to constants
SELECT status,
       CASE status
           WHEN 'pending'   THEN '⏳'
           WHEN 'paid'      THEN '✅'
           WHEN 'shipped'   THEN '📦'
           WHEN 'cancelled' THEN '❌'
           ELSE                 '?'
       END AS icon
FROM orders;
```

### `CASE` in `ORDER BY` — custom ordering

```sql
-- Sort by a domain priority that isn't alphabetical:
SELECT * FROM tickets
ORDER BY CASE severity
            WHEN 'critical' THEN 1
            WHEN 'high'     THEN 2
            WHEN 'medium'   THEN 3
            WHEN 'low'      THEN 4
         END;
```

### `CASE` for conditional aggregation (preview of file [`05`](./05-Aggregation-And-Advanced-Queries.md))

```sql
-- "Pivot" booleans by counting matching rows
SELECT
    COUNT(*)                                              AS total_orders,
    COUNT(*) FILTER (WHERE status = 'paid')               AS paid_orders,         -- Postgres
    SUM(CASE WHEN status = 'paid' THEN 1 ELSE 0 END)      AS paid_orders_portable -- works everywhere
FROM orders;
```

---

## VII. STRING FUNCTIONS

### Length, case, trimming

```sql
SELECT LENGTH('hello');              -- 5
SELECT CHAR_LENGTH('héllo');         -- 5 chars (LENGTH returns bytes; same for ASCII)
SELECT UPPER('hello'), LOWER('WORLD');           -- HELLO, world
SELECT INITCAP('the great gatsby');              -- The Great Gatsby
SELECT TRIM('  hello  ');                         -- 'hello' (both ends)
SELECT LTRIM('  hi'), RTRIM('hi  ');             -- 'hi', 'hi'
SELECT TRIM(BOTH 'x' FROM 'xxhelloxx');          -- 'hello'
```

### Substring / position

```sql
SELECT SUBSTRING('Hello World' FROM 1 FOR 5);    -- 'Hello'   (1-indexed!)
SELECT SUBSTRING('Hello World', 7);              -- 'World'
SELECT LEFT('Hello World', 5);                   -- 'Hello'
SELECT RIGHT('Hello World', 5);                  -- 'World'
SELECT POSITION('World' IN 'Hello World');       -- 7  (or 0 if not found)
```

### Concat, replace, split

```sql
SELECT 'Hello, ' || 'World';                     -- 'Hello, World'  (||  = standard SQL concat)
SELECT CONCAT('Hello, ', 'World', '!');          -- 'Hello, World!' — CONCAT treats NULL as ''
SELECT 'a' || NULL;                              -- NULL  (|| with NULL is NULL)
SELECT CONCAT('a', NULL);                        -- 'a'   (the safer choice if NULLs are possible)

SELECT REPLACE('foo bar foo', 'foo', 'baz');     -- 'baz bar baz'
SELECT SPLIT_PART('a,b,c', ',', 2);              -- 'b'  (Postgres)
SELECT STRING_TO_ARRAY('a,b,c', ',');            -- {a,b,c}
```

### Padding, repeating, regex

```sql
SELECT LPAD('42', 5, '0');                        -- '00042'
SELECT RPAD('hi', 6, '.');                        -- 'hi....'
SELECT REPEAT('ab', 3);                           -- 'ababab'
SELECT REVERSE('abc');                            -- 'cba'

SELECT REGEXP_REPLACE('user_42', '\\d+', 'X');    -- 'user_X'
SELECT REGEXP_MATCHES('error code 500', '(\\d+)');-- {500}
SELECT REGEXP_SPLIT_TO_ARRAY('a, b ,  c', '\\s*,\\s*');  -- {a,b,c}
```

> **MySQL note:** MySQL uses `CONCAT(...)` rather than `||` (`||` in MySQL is logical OR by default). Wrap in `SET sql_mode='PIPES_AS_CONCAT'` if you need it.

---

## VIII. NUMERIC / MATH FUNCTIONS

```sql
SELECT ABS(-7);                  -- 7
SELECT CEIL(4.2),  FLOOR(4.8);   -- 5,  4
SELECT ROUND(4.5);               -- 5  (banker's rounding may apply on some engines)
SELECT ROUND(3.14159, 2);        -- 3.14
SELECT TRUNC(3.99, 1);           -- 3.9
SELECT MOD(10, 3),  10 % 3;       -- 1, 1
SELECT POWER(2, 10);             -- 1024
SELECT SQRT(81);                 -- 9
SELECT EXP(1), LN(EXP(1));       -- 2.718…, 1
SELECT GREATEST(3, 7, 2),  LEAST(3, 7, 2);     -- 7, 2

-- Random number in [0, 1)
SELECT RANDOM();                 -- Postgres
SELECT FLOOR(RANDOM() * 100);    -- random integer 0..99
```

---

## IX. DATE / TIME FUNCTIONS

### Current values

```sql
SELECT NOW();                    -- TIMESTAMPTZ — instant the transaction started
SELECT CURRENT_TIMESTAMP;        -- same as NOW()
SELECT CURRENT_DATE;             -- DATE
SELECT CURRENT_TIME;             -- TIME WITH TIME ZONE
SELECT LOCALTIMESTAMP;           -- TIMESTAMP without TZ (in session TZ)
SELECT CLOCK_TIMESTAMP();        -- changes within a transaction (true wall clock)
```

### Extracting parts

```sql
SELECT EXTRACT(YEAR  FROM happens_at) AS y,
       EXTRACT(MONTH FROM happens_at) AS m,
       EXTRACT(DAY   FROM happens_at) AS d,
       EXTRACT(DOW   FROM happens_at) AS day_of_week,    -- 0 (Sun) – 6
       EXTRACT(EPOCH FROM happens_at) AS unix_seconds
FROM events;

-- DATE_PART is the same:
SELECT DATE_PART('hour', happens_at) FROM events;
```

### Truncation and bucketing

```sql
SELECT DATE_TRUNC('day',   happens_at) AS day_bucket,
       DATE_TRUNC('hour',  happens_at) AS hour_bucket,
       DATE_TRUNC('month', happens_at) AS month_bucket
FROM events;

-- "Orders per day this month":
SELECT DATE_TRUNC('day', placed_at) AS day, COUNT(*) AS orders
FROM   orders
WHERE  placed_at >= DATE_TRUNC('month', NOW())
GROUP  BY 1
ORDER  BY 1;
```

### Arithmetic with intervals

```sql
SELECT NOW() + INTERVAL '7 days';
SELECT NOW() - INTERVAL '1 month';
SELECT placed_at + INTERVAL '30 days' AS expires FROM orders;

-- Difference between two timestamps
SELECT AGE(NOW(), '2000-01-01');           -- e.g. '25 years 4 mons 12 days …'  (Postgres)
SELECT NOW() - placed_at AS time_since_order FROM orders;
```

### Formatting and parsing

```sql
SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS TZ');     -- '2025-…'
SELECT TO_CHAR(NOW(), 'Day, DD Month YYYY');           -- 'Tuesday  , 14 January 2025'
SELECT TO_DATE('2025-01-14', 'YYYY-MM-DD');
SELECT TO_TIMESTAMP('2025-01-14 09:30', 'YYYY-MM-DD HH24:MI');
```

> **MySQL note:** MySQL uses `DATE_FORMAT(now(), '%Y-%m-%d %H:%i:%s')` and `STR_TO_DATE()`. The format strings differ.

### "Last 7 days," "this week," "this month"

```sql
-- Last 7 days
SELECT * FROM events WHERE happens_at >= NOW() - INTERVAL '7 days';

-- Today (using truncation; safer than EXTRACT comparisons):
SELECT * FROM events
WHERE  happens_at >= DATE_TRUNC('day', NOW())
  AND  happens_at <  DATE_TRUNC('day', NOW()) + INTERVAL '1 day';

-- This month:
SELECT * FROM events
WHERE  happens_at >= DATE_TRUNC('month', NOW())
  AND  happens_at <  DATE_TRUNC('month', NOW()) + INTERVAL '1 month';
```

---

## X. TYPE CASTING

Two equivalent forms in Postgres: `CAST(x AS T)` (standard) and `x::T` (Postgres shortcut).

```sql
SELECT CAST('42' AS INT),  '42'::INT;                  -- 42, 42
SELECT CAST('3.14' AS NUMERIC(5,2));                    -- 3.14
SELECT CAST('2025-01-14' AS DATE);                      -- 2025-01-14
SELECT CAST(123 AS TEXT)   || ' books';                 -- '123 books'
SELECT 'true'::BOOLEAN;                                  -- true
SELECT '{1,2,3}'::INT[];                                 -- {1,2,3}
SELECT '{"a":1}'::JSONB ->> 'a';                          -- '1'
```

Casts can fail if the string isn't valid for the type — that throws an error and aborts the statement (and the transaction). For best-effort parsing, validate first or wrap in a `CASE` / function.

---

## XI. PUTTING IT TOGETHER — REAL QUERIES

Using the bookstore schema seeded in file [`02`](./02-SQL-Basics-DDL-And-DML.md):

```sql
-- 1. Top 5 most expensive books, with a discount column
SELECT title,
       list_price,
       ROUND(list_price * 0.85, 2) AS sale_price,
       CASE WHEN list_price > 50 THEN 'premium' ELSE 'standard' END AS tier
FROM   books
ORDER  BY list_price DESC
LIMIT  5;

-- 2. Customers from Boston, sorted by signup time (newest first)
SELECT customer_id, name, email
FROM   customers
WHERE  city = 'Boston'
ORDER  BY created_at DESC;

-- 3. Search books by partial title (case-insensitive)
SELECT title, list_price
FROM   books
WHERE  title ILIKE '%data%'
ORDER  BY published_on DESC NULLS LAST;

-- 4. Orders placed in the last 30 days
SELECT order_id, customer_id, status, placed_at
FROM   orders
WHERE  placed_at >= NOW() - INTERVAL '30 days'
ORDER  BY placed_at DESC;

-- 5. Format an order summary line
SELECT order_id,
       TO_CHAR(placed_at, 'YYYY-MM-DD') AS day,
       UPPER(status)                    AS status,
       'Order #' || order_id            AS label
FROM   orders;

-- 6. Distinct cities our customers come from
SELECT DISTINCT city FROM customers WHERE city IS NOT NULL ORDER BY city;

-- 7. Bucket orders by size with CASE
SELECT order_id,
       status,
       CASE
           WHEN status = 'paid'      THEN '💰 paid'
           WHEN status = 'shipped'   THEN '📦 shipped'
           WHEN status = 'cancelled' THEN '❌ cancelled'
           ELSE                           '⏳ pending'
       END AS pretty_status
FROM   orders;

-- 8. Replace missing city with 'Unknown' for a report
SELECT name, COALESCE(city, 'Unknown') AS city FROM customers ORDER BY name;

-- 9. Books published in the 2010s
SELECT title, published_on
FROM   books
WHERE  EXTRACT(YEAR FROM published_on) BETWEEN 2010 AND 2019
ORDER  BY published_on;

-- 10. Keyset pagination — second page of 5, ordered by title
SELECT book_id, title FROM books
WHERE  title > 'Designing Data-Intensive Applications'
ORDER  BY title
LIMIT  5;
```

---

## XII. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `SELECT *` in code | Breaks when columns are added/reordered | List the columns you need |
| Using a `SELECT` alias in `WHERE` | `column "x" does not exist` | Repeat the expression, or move to subquery/CTE |
| `column = NULL` instead of `IS NULL` | Always returns no rows | `IS NULL` / `IS NOT NULL` |
| `NOT IN (… NULL …)` returns nothing | Empty result that shouldn't be | Use `NOT EXISTS` or filter NULLs |
| `BETWEEN` for a date *range* with timestamps | Misses last day's afternoon | Use `>= start AND < end_exclusive` |
| Leading `%` in `LIKE` | Slow on large tables | Trigram / full-text index |
| Floating-point `=` comparison | Sometimes false for "equal" values | `ABS(a - b) < epsilon`, or use `NUMERIC` |
| `OFFSET` on huge tables | Very slow at deep pages | Keyset (seek) pagination |
| Forgetting `ORDER BY` with `LIMIT` | Non-deterministic page contents | Always `ORDER BY` something stable |
| Casting strings that may not parse | Whole transaction aborts | Validate first, or use a safe-cast function |
| String concat with NULL | Result becomes NULL | `CONCAT()` (treats NULL as `''`) or `COALESCE` |
| `LIKE 'A%'` matching unexpected case | Postgres is case-sensitive | Use `ILIKE` or `LOWER()` on both sides |

---

## 🧠 KEY TAKEAWAYS

- The **logical query order** is `FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT`. Aliases live in `SELECT`, so `WHERE`/`GROUP BY` cannot use them.
- Avoid `SELECT *` in code; pick the columns you need.
- `NULL` is "unknown" — comparisons return `NULL`. Use `IS NULL`/`IS NOT NULL`, prefer `NOT EXISTS` over `NOT IN` when nulls are possible, and reach for `COALESCE`/`NULLIF` to tame them.
- Use `BETWEEN` cautiously with timestamps; prefer half-open ranges (`>= start AND < end`).
- `LIKE 'X%'` can use indexes; `LIKE '%X'` cannot — use trigram/full-text for substring search.
- Master the **string**, **numeric**, **date/time** function libraries — `COALESCE`, `CASE`, `DATE_TRUNC`, `TO_CHAR`, `EXTRACT`, regex.
- For pagination, prefer **keyset (seek) pagination** over deep `OFFSET`s.
- A `SELECT` without `ORDER BY` has no defined order. Always order what you slice.

---

**Prev:** [`02-SQL-Basics-DDL-And-DML.md`](./02-SQL-Basics-DDL-And-DML.md) · **Next:** [`04-Joins-And-Relationships.md`](./04-Joins-And-Relationships.md) · **Index:** [`00-Index.md`](./00-Index.md)
