# 🗄️ 04 — Joins & Relationships

> *"Normalization scatters your data across tables for safety. Joins are how you put it back together for meaning. Master joins and the whole relational model clicks."*

**Prev:** [`03-Querying-Data-SELECT.md`](./03-Querying-Data-SELECT.md) · **Next:** [`05-Aggregation-And-Advanced-Queries.md`](./05-Aggregation-And-Advanced-Queries.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHY JOINS EXIST

In file 01 you normalized data into separate tables to avoid redundancy. A user's name lives in `users`; their orders live in `orders`, linked by `orders.user_id → users.id`. To answer *"show each order with the buyer's username,"* you must **recombine** those tables. That recombination is a **join**.

```
users                          orders
┌────┬──────────┐              ┌────┬─────────┬───────┐
│ id │ username │              │ id │ user_id │ total │
├────┼──────────┤              ├────┼─────────┼───────┤
│ 1  │ ada      │              │ 10 │   1     │  50   │
│ 2  │ grace    │              │ 11 │   1     │  20   │
│ 3  │ linus    │  ← no orders │ 12 │   2     │  99   │
└────┴──────────┘              │ 13 │   9     │  10   │ ← user 9 doesn't exist
                               └────┴─────────┴───────┘
```

A join walks one table, and for each row finds matching rows in the other table according to a **join condition** (usually `FK = PK`). The *type* of join decides what happens to rows that have **no match**.

### Sample data for this file

```sql
-- Run these to follow along
CREATE TABLE users  (id INT PRIMARY KEY, username TEXT);
CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, total NUMERIC);

INSERT INTO users VALUES (1,'ada'), (2,'grace'), (3,'linus');     -- linus has no orders
INSERT INTO orders VALUES (10,1,50), (11,1,20), (12,2,99), (13,9,10); -- order 13 → ghost user 9
```

---

## II. INNER JOIN — ONLY MATCHING ROWS

`INNER JOIN` returns rows where the condition matches **on both sides**. Rows with no partner (linus with no order; order 13 with no user) are **dropped**.

```sql
SELECT u.username, o.id AS order_id, o.total
FROM users u
INNER JOIN orders o ON o.user_id = u.id;   -- JOIN keyword alone also means INNER JOIN
```

```
Result (4 rows): linus and order 13 vanish — no match on the other side.
 username | order_id | total
----------+----------+-------
 ada      |    10    |  50
 ada      |    11    |  20
 grace    |    12    |  99
```

```
INNER JOIN = the intersection
   users        orders
    (    A  ∩  B    )      ← only rows present in BOTH
```

> **Gotcha — `INNER JOIN` silently hides unmatched rows.** If your "total revenue per user" report is missing users, an inner join dropped the ones with zero orders. When you need *all* rows from one side regardless of matches, you want an **outer** join (next).

---

## III. LEFT / RIGHT / FULL OUTER JOINS — KEEPING UNMATCHED ROWS

**Outer joins** keep unmatched rows from one or both sides, filling the missing columns with `NULL`.

### LEFT JOIN — keep all left rows

```sql
-- ALL users, with their orders if any. Users with no orders → order columns are NULL.
SELECT u.username, o.id AS order_id, o.total
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;
```

```
 username | order_id | total
----------+----------+-------
 ada      |    10    |  50
 ada      |    11    |  20
 grace    |    12    |  99
 linus    |  NULL    | NULL    ← KEPT, padded with NULLs (no orders)
```

> **The single most useful join in practice.** "All X, plus their Y if it exists" is the shape of most real reports. `LEFT JOIN` then `WHERE y.id IS NULL` is also the classic **"find rows with no match"** (anti-join) pattern:

```sql
-- Users who have NEVER placed an order
SELECT u.username
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;          -- the LEFT JOIN made these NULL; keep only those
-- → linus
```

### RIGHT JOIN — keep all right rows

```sql
-- ALL orders, with their user if it exists. Orphan order 13 → user columns NULL.
SELECT u.username, o.id AS order_id
FROM users u
RIGHT JOIN orders o ON o.user_id = u.id;
-- order 13 appears with username = NULL (ghost user 9)
```

> `RIGHT JOIN` is just a `LEFT JOIN` with the tables flipped. Most teams **avoid `RIGHT JOIN`** entirely and always write `LEFT JOIN` (reorder the tables) because reading left-to-right matches the "keep everything from the first table" mental model.

### FULL OUTER JOIN — keep everything

```sql
-- ALL users AND ALL orders; unmatched rows on either side get NULLs.
SELECT u.username, o.id AS order_id
FROM users u
FULL OUTER JOIN orders o ON o.user_id = u.id;
-- includes linus (NULL order) AND order 13 (NULL user)
```

> **MySQL note.** MySQL has **no `FULL OUTER JOIN`**. Emulate it with `LEFT JOIN ... UNION ... RIGHT JOIN` (see set operations below). PostgreSQL, SQL Server, and Oracle support it natively.

---

## IV. CROSS JOIN — THE CARTESIAN PRODUCT

`CROSS JOIN` pairs **every** left row with **every** right row — no condition. Result size = `rows(A) × rows(B)`.

```sql
-- Every size paired with every color → a full product matrix
CREATE TABLE sizes  (s TEXT); INSERT INTO sizes  VALUES ('S'),('M'),('L');
CREATE TABLE colors (c TEXT); INSERT INTO colors VALUES ('red'),('blue');

SELECT s, c FROM sizes CROSS JOIN colors;   -- 3 × 2 = 6 rows
-- S/red, S/blue, M/red, M/blue, L/red, L/blue
```

> **Gotcha — the accidental cross join.** If you list two tables in `FROM` and forget the join condition (`SELECT * FROM users, orders`), you get a cross join — every user paired with every order. On a 100k × 100k table that's 10 *billion* rows and a hung server. Always specify the join condition; the explicit `JOIN ... ON` syntax makes a missing condition a visible mistake.

Legitimate uses: generating combinations, building a calendar/number series, pairing each row with a single-row config table.

---

## V. SELF JOIN — A TABLE JOINED TO ITSELF

When rows in a table relate to *other rows in the same table* (hierarchies, pairs), join the table to itself using two aliases.

```sql
CREATE TABLE employees (
    id        INT PRIMARY KEY,
    name      TEXT,
    manager_id INT            -- references employees.id (a self-reference)
);
INSERT INTO employees VALUES (1,'CEO',NULL), (2,'VP',1), (3,'Dev',2), (4,'Dev2',2);

-- Pair each employee with their manager's name
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;  -- LEFT so the CEO (no manager) is kept
```

```
 employee | manager
----------+---------
 CEO      | NULL
 VP       | CEO
 Dev      | VP
 Dev2     | VP
```

> Self joins handle *one level* of a hierarchy. For arbitrary-depth trees ("everyone under the VP, recursively"), you need a **recursive CTE** (file 05).

---

## VI. ON vs USING vs NATURAL JOIN

Three ways to express the join condition:

```sql
-- ON: explicit, fully general — works for any condition, including renamed/multiple columns
SELECT * FROM orders o JOIN users u ON o.user_id = u.id;
SELECT * FROM a JOIN b ON a.x = b.x AND a.y >= b.y;   -- can be any boolean expression

-- USING: shorthand when the columns have the SAME NAME in both tables
-- It also MERGES the column (appears once, unqualified) in the result.
SELECT * FROM order_items JOIN products USING (product_id);
-- product_id appears once, not twice

-- NATURAL JOIN: auto-joins on ALL identically-named columns. Convenient but DANGEROUS.
SELECT * FROM order_items NATURAL JOIN products;
```

> **Gotcha — avoid `NATURAL JOIN`.** It silently joins on *every* column that happens to share a name. Add a `created_at` column to both tables later and your join condition secretly changes, quietly returning wrong results. Be explicit with `ON`. `USING` is a safe middle ground when you control the column names.

| Syntax | When to use | Risk |
|--------|-------------|------|
| `ON a.x = b.y` | Always safe; required for different names or complex conditions | None — explicit |
| `USING (col)` | Same-named key columns; want a merged column | Low |
| `NATURAL JOIN` | Never (in production) | High — implicit, fragile |

---

## VII. MULTI-TABLE JOINS

Real queries chain several joins. Each `JOIN` adds one table; conditions link it to a table already in the query.

```sql
-- "Each order line: who bought what, in which category, at what price"
SELECT
    u.username,
    o.id          AS order_id,
    p.name        AS product,
    c.name        AS category,
    oi.quantity,
    oi.quantity * oi.unit_price AS line_total
FROM orders o
JOIN users      u  ON u.id = o.user_id          -- order → buyer
JOIN order_items oi ON oi.order_id = o.id         -- order → its line items
JOIN products   p  ON p.id = oi.product_id        -- line item → product
LEFT JOIN categories c ON c.id = p.category_id    -- product → category (LEFT: maybe uncategorized)
WHERE o.status = 'paid'
ORDER BY o.id, line_total DESC;
```

> **Gotcha — one `LEFT JOIN` "poisons" the chain.** Once you `LEFT JOIN` a table, putting a condition on *that* table in the `WHERE` clause (`WHERE c.name = 'Electronics'`) silently turns it back into an inner join (because `NULL = 'Electronics'` is false, dropping the unmatched rows). If you must filter an outer-joined table while keeping unmatched rows, put the condition in the `ON` clause instead:

```sql
-- Filter in ON (keeps unmatched products), not WHERE (would drop them)
LEFT JOIN categories c ON c.id = p.category_id AND c.name = 'Electronics'
```

> **Join order & performance.** You write joins in a readable order, but the **query planner** chooses the actual execution order based on statistics (file 06). Logically, though, joins evaluate left-to-right, and the result set can only *shrink* with `INNER` joins and *grow or stay* with each new matching row.

---

## VIII. JOIN TYPES — THE COMPARISON TABLE

| Join | Keeps | Drops | Mental model | Typical use |
|------|-------|-------|--------------|-------------|
| `INNER JOIN` | Rows matching on both sides | Unmatched rows from both | Intersection (A ∩ B) | "Orders *with* a valid user" |
| `LEFT [OUTER] JOIN` | All left rows + matches | Nothing from left | All of A, B if present | "All users + their orders (or none)" |
| `RIGHT [OUTER] JOIN` | All right rows + matches | Nothing from right | All of B, A if present | Rare — rewrite as LEFT |
| `FULL [OUTER] JOIN` | All rows from both sides | Nothing | Union of both | "Reconcile two datasets" |
| `CROSS JOIN` | Every pairing | Nothing | A × B (Cartesian) | Generate combinations |
| `SELF JOIN` | Rows paired within one table | Depends on inner/outer | Table ⋈ itself | Hierarchies, pairs |

```
INNER          LEFT           RIGHT          FULL
 A ∩ B        A + (A∩B)      (A∩B) + B      A ∪ B
  ▓▓           ▓▓▓             ▓▓             ▓▓▓▓
 ╱  ╲         ▓▓▓░            ░▓▓            ▓▓▓▓
(    )       (    )          (    )        (    )
```

---

## IX. SET OPERATIONS — UNION, INTERSECT, EXCEPT

Joins combine tables **horizontally** (adding columns). Set operations combine query results **vertically** (stacking rows). Each operand must have the **same number of columns with compatible types**.

```sql
-- UNION: all rows from both queries, DUPLICATES REMOVED (and a dedup sort — costly)
SELECT email FROM customers
UNION
SELECT email FROM newsletter_subscribers;     -- unique emails across both lists

-- UNION ALL: stack rows, KEEP duplicates (faster — no dedup). Prefer when you know rows are distinct.
SELECT product_id FROM order_items_2023
UNION ALL
SELECT product_id FROM order_items_2024;

-- INTERSECT: rows present in BOTH queries
SELECT email FROM customers
INTERSECT
SELECT email FROM newsletter_subscribers;     -- customers who also subscribe

-- EXCEPT (MINUS in Oracle): rows in the first query NOT in the second
SELECT email FROM customers
EXCEPT
SELECT email FROM newsletter_subscribers;     -- customers who DON'T subscribe
```

```
A UNION B        A INTERSECT B      A EXCEPT B
 ▓▓▓▓▓             ░░▓▓░░            ▓▓░░░░
(  A∪B  )         (  A∩B  )         ( A − B )
```

> **Gotcha — `UNION` deduplicates, `UNION ALL` does not.** `UNION` does extra work to remove duplicate rows (effectively a sort/hash). If duplicates are impossible or acceptable, **`UNION ALL` is faster** and is usually what you want. Reaching for `UNION` out of habit silently adds a dedup cost.

| Operation | Returns | Removes duplicates? |
|-----------|---------|---------------------|
| `UNION` | Rows in A **or** B | ✅ Yes (slower) |
| `UNION ALL` | Rows in A **or** B | ❌ No (faster) |
| `INTERSECT` | Rows in A **and** B | ✅ Yes |
| `EXCEPT` / `MINUS` | Rows in A **not** in B | ✅ Yes |

```sql
-- Rules: column COUNT and TYPES must align; ORDER BY goes ONCE, at the very end.
SELECT id, name FROM a
UNION ALL
SELECT id, name FROM b
ORDER BY name;        -- applies to the combined result
```

> **MySQL note.** MySQL gained `INTERSECT` and `EXCEPT` only in version 8.0.31+. Older MySQL emulates `INTERSECT` with an inner join and `EXCEPT` with a `LEFT JOIN ... WHERE ... IS NULL`.

---

## X. JOIN vs SUBQUERY — A PREVIEW

Many questions can be answered with either a join or a subquery (file 05). A quick orientation:

```sql
-- "Users who placed an order" — via JOIN (may produce duplicates → needs DISTINCT)
SELECT DISTINCT u.username
FROM users u JOIN orders o ON o.user_id = u.id;

-- Same answer — via EXISTS (no duplicates, often clearer for "does any match exist?")
SELECT u.username
FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

Rule of thumb: use a **join** when you need columns *from both* tables in the output; use **`EXISTS`/`IN`** when you only need to *test for the existence* of a related row. Full treatment in file 05.

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `INNER JOIN` when you needed all rows | Report missing zero-activity rows | Use `LEFT JOIN` |
| Missing join condition | Explosive row count (cross join) | Always specify `ON`; use explicit `JOIN` syntax |
| Filtering a `LEFT JOIN`ed table in `WHERE` | Outer join silently becomes inner | Put the filter in the `ON` clause |
| `NATURAL JOIN` | Wrong results after a column is added | Use explicit `ON` |
| `UNION` instead of `UNION ALL` | Slow (unnecessary dedup) | `UNION ALL` when duplicates are fine |
| Mismatched columns in set ops | "each UNION query must have the same number of columns" | Align column count & types |
| `ORDER BY` inside a UNION operand | Syntax error / ignored | One `ORDER BY` at the very end |
| Forgetting `DISTINCT` on a 1:N join | Duplicated left rows | `DISTINCT`, or aggregate (file 05), or `EXISTS` |
| Ambiguous column name | "column reference is ambiguous" | Qualify with table alias (`u.id`) |
| `RIGHT JOIN` confusion | Hard to read, easy to misjudge | Rewrite as `LEFT JOIN` with tables flipped |

---

## 🧠 KEY TAKEAWAYS

- A **join** recombines normalized tables on a condition; the join *type* decides what happens to rows with **no match**.
- `INNER JOIN` keeps only matches; `LEFT JOIN` keeps all left rows (the workhorse, and the basis of the "find rows with no match" anti-join pattern); `FULL OUTER JOIN` keeps everything.
- `CROSS JOIN` is every pairing (`A × B`) — guard against the *accidental* cross join from a missing condition.
- A **self join** relates rows within one table (hierarchies); deeper trees need a recursive CTE (file 05).
- Prefer explicit **`ON`**; `USING` is a safe shorthand for same-named keys; **avoid `NATURAL JOIN`**.
- Filtering an outer-joined table belongs in **`ON`**, not `WHERE`, or the outer join collapses to an inner join.
- **Set operations** stack rows vertically: `UNION` (dedup) vs `UNION ALL` (fast, keeps dupes), plus `INTERSECT` and `EXCEPT`.

---

**Prev:** [`03-Querying-Data-SELECT.md`](./03-Querying-Data-SELECT.md) · **Next:** [`05-Aggregation-And-Advanced-Queries.md`](./05-Aggregation-And-Advanced-Queries.md) · **Index:** [`00-Index.md`](./00-Index.md)
