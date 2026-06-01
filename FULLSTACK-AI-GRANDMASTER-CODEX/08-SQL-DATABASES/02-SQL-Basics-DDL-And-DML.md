# 🗄️ 02 — SQL Basics: DDL & DML

> *"DDL writes the laws of your data. DML lives by them. Most production fires are not bugs — they are unconstrained DDL letting bad data sneak past a missing CHECK."*

**Prev:** [`01-Relational-Model-And-Design.md`](./01-Relational-Model-And-Design.md) · **Next:** [`03-Querying-Data-SELECT.md`](./03-Querying-Data-SELECT.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE THREE FAMILIES OF SQL

SQL is one language with several sub-languages, each with its own job:

| Family | Stands for | Statements | Touches |
|--------|------------|------------|---------|
| **DDL** | Data **Definition** Language | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` | The schema (tables, columns, constraints) |
| **DML** | Data **Manipulation** Language | `INSERT`, `UPDATE`, `DELETE`, `MERGE` | The data inside tables |
| **DQL** | Data **Query** Language | `SELECT` | Reading data (file [`03`](./03-Querying-Data-SELECT.md)) |
| **DCL** | Data **Control** Language | `GRANT`, `REVOKE` | Permissions (file [`08`](./08-Advanced-SQL-And-Production.md)) |
| **TCL** | Transaction **Control** Language | `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` | Transactions (file [`07`](./07-Transactions-And-Concurrency.md)) |

This file covers DDL + DML in depth. The rest get their own chapters.

> **Implicit commits.** In most engines (including Postgres in default mode), each DDL statement runs in its own transaction *unless* you wrap them. A failed `ALTER TABLE` halfway through a migration leaves the schema in a half-changed state. Always wrap migrations in `BEGIN ... COMMIT;` so a failure rolls back cleanly.

---

## II. DDL — DEFINING SCHEMA

### `CREATE DATABASE` and `CREATE SCHEMA`

```sql
-- Top-level container.
CREATE DATABASE bookstore
    WITH OWNER     = postgres
         ENCODING  = 'UTF8'
         LC_COLLATE = 'en_US.UTF-8'
         LC_CTYPE   = 'en_US.UTF-8'
         TEMPLATE  = template0;

-- Connect to it.
\c bookstore

-- A schema is a namespace inside a database — it groups related tables.
CREATE SCHEMA sales;
CREATE SCHEMA inventory AUTHORIZATION postgres;

-- Default search path:
SHOW search_path;             -- "$user", public
SET search_path TO sales, public;
```

> **MySQL note:** in MySQL, `CREATE DATABASE` and `CREATE SCHEMA` are synonyms — there is no separate "schema" concept. You group with prefixes (`sales_orders`, `inventory_books`).

### `CREATE TABLE` — the canonical form

```sql
CREATE TABLE customers (
    -- column_name  data_type      [column_constraints...]
    customer_id     BIGSERIAL      PRIMARY KEY,
    email           TEXT           NOT NULL UNIQUE,
    name            TEXT           NOT NULL,
    age             INT            CHECK (age IS NULL OR age >= 13),
    country_code    CHAR(2)        DEFAULT 'US',
    is_active       BOOLEAN        NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ    NOT NULL DEFAULT NOW(),

    -- table-level constraint (a constraint that spans columns)
    CONSTRAINT chk_email_lower CHECK (email = LOWER(email))
);
```

What is happening:
- Each row is `column_name TYPE [constraints]`.
- *Column-level* constraints sit on the column line.
- *Table-level* constraints sit at the bottom (with `CONSTRAINT name`) — useful when a constraint references multiple columns.

> **Gotcha — `IF NOT EXISTS`**. Use `CREATE TABLE IF NOT EXISTS` in scripts that may run twice; it skips the create instead of failing. Same applies to `DROP TABLE IF EXISTS`.

---

## III. DATA TYPES — THE FULL TOUR (POSTGRES)

Pick the **smallest, most specific** type the data deserves. Wider types waste memory, weaker types let nonsense through.

### Numeric

| Type | Bytes | Range / notes |
|------|-------|---------------|
| `SMALLINT` | 2 | ±32 K |
| `INT` / `INTEGER` | 4 | ±2.1 B — the workhorse |
| `BIGINT` | 8 | ±9.2 quintillion — for IDs and counts |
| `NUMERIC(p, s)` / `DECIMAL(p,s)` | variable | **Exact**. `NUMERIC(10,2)` = up to 10 digits, 2 after the decimal — the choice for **money** |
| `REAL` | 4 | ~6 sig figs, **inexact** binary float |
| `DOUBLE PRECISION` | 8 | ~15 sig figs, inexact |
| `SERIAL` / `BIGSERIAL` | 4 / 8 | `INT`/`BIGINT` + auto-incrementing sequence (legacy form of `IDENTITY`) |

```sql
CREATE TABLE invoices (
    invoice_id BIGSERIAL PRIMARY KEY,
    amount     NUMERIC(12,2) NOT NULL CHECK (amount >= 0),  -- exact for money
    discount   REAL          NOT NULL DEFAULT 0,            -- approximate is fine for percentages
    quantity   INT           NOT NULL
);
```

> **Gotcha — never use floats for money.** `0.1 + 0.2 = 0.30000000000000004`. Floating-point is binary; most decimals are inexact. Use `NUMERIC(p,s)` and pass values as strings from your code (`'19.99'`).

### Character / text

| Type | Notes |
|------|-------|
| `CHAR(n)` | Fixed length, **right-padded with spaces**. Almost never what you want |
| `VARCHAR(n)` | Variable length, capped at `n`. Length check at insert |
| `VARCHAR` (no `n`) | Effectively unlimited (1 GB) |
| `TEXT` | Unlimited; **identical performance to VARCHAR** in Postgres. Use this by default |

```sql
CREATE TABLE comments (
    comment_id BIGSERIAL PRIMARY KEY,
    body       TEXT NOT NULL CHECK (LENGTH(body) BETWEEN 1 AND 10000),
    -- prefer TEXT + CHECK over VARCHAR(10000) — the meaning is at the constraint level
);
```

> **MySQL/SQL Server note:** there `VARCHAR(n)` and `TEXT` differ in storage and indexing. The "use TEXT" rule is Postgres-specific; on MySQL prefer `VARCHAR(n)` with a sane `n`.

### Date and time — get this right once

| Type | Stores | Postgres `NOW()` returns |
|------|--------|--------------------------|
| `DATE` | Calendar day (no time) | n/a |
| `TIME` | Time of day, no date | n/a |
| `TIMESTAMP` | Date + time, **no timezone** | n/a |
| **`TIMESTAMPTZ`** (`TIMESTAMP WITH TIME ZONE`) | Instant in time, stored UTC, displayed in session TZ | **This** |
| `INTERVAL` | A duration (`'5 days'`, `'2 hours'`) | n/a |

**Strong default: `TIMESTAMPTZ` for any "when did this happen" column.** The DB stores UTC and converts on display, eliminating an entire class of timezone bugs.

```sql
CREATE TABLE events (
    event_id   BIGSERIAL PRIMARY KEY,
    happens_at TIMESTAMPTZ NOT NULL,
    duration   INTERVAL    NOT NULL DEFAULT '1 hour',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO events (happens_at) VALUES ('2025-12-31 23:59:59+00'::timestamptz);

SELECT happens_at AT TIME ZONE 'Asia/Kolkata' AS local_time FROM events;
```

> **Gotcha — `TIMESTAMP` (no TZ) silently drops zone info.** Inserting `'2025-01-01 10:00+05'` into a `TIMESTAMP` column stores `'2025-01-01 10:00'` *as-is* — the zone offset vanishes. Use `TIMESTAMPTZ` and learn to love it.

### Boolean

```sql
CREATE TABLE feature_flags (
    flag_id  BIGSERIAL PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE,
    enabled  BOOLEAN NOT NULL DEFAULT FALSE
);
```

> **MySQL note:** MySQL does not have a true `BOOLEAN`; it is an alias for `TINYINT(1)`. SQL Server uses `BIT`.

### UUID

```sql
CREATE TABLE api_keys (
    key_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),  -- pgcrypto / Postgres 13+
    user_id     BIGINT NOT NULL,
    revoked_at  TIMESTAMPTZ
);
-- If gen_random_uuid() is missing: CREATE EXTENSION pgcrypto;
```

UUIDs are 16 bytes. They're great for distributed ID generation (no central sequence) and for IDs you expose in URLs (no leak of "we have N users"). For internal joins where size matters, `BIGSERIAL` is cheaper.

### JSON / JSONB

```sql
CREATE TABLE webhooks (
    hook_id BIGSERIAL PRIMARY KEY,
    payload JSONB NOT NULL                                  -- binary, indexed, queryable
);

INSERT INTO webhooks (payload) VALUES ('{"type":"order","id":42}'::jsonb);

-- Query inside JSON
SELECT * FROM webhooks WHERE payload->>'type' = 'order';
SELECT * FROM webhooks WHERE payload @> '{"type":"order"}';   -- contains operator
CREATE INDEX idx_webhooks_payload ON webhooks USING GIN (payload);
```

`JSONB` is the binary, queryable form. `JSON` keeps the original text. Reach for `JSONB` 99% of the time — but **don't use it as an excuse to skip relational design**. Use it for genuinely variable-shape data (third-party payloads, attribute bags), not for "I'll model it later."

### Arrays

```sql
CREATE TABLE posts (
    post_id BIGSERIAL PRIMARY KEY,
    title   TEXT NOT NULL,
    tags    TEXT[] NOT NULL DEFAULT '{}'
);

INSERT INTO posts (title, tags) VALUES ('Hello', ARRAY['intro', 'meta']);

SELECT * FROM posts WHERE 'intro' = ANY (tags);
SELECT * FROM posts WHERE tags @> ARRAY['meta'];
CREATE INDEX idx_posts_tags ON posts USING GIN (tags);
```

> **Use sparingly.** Arrays *technically* violate 1NF. They're fine for tiny, immutable, unordered sets like `tags` — for anything you'll filter, count, or join on, use a child table.

### Enums

```sql
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'shipped', 'cancelled');

CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    status   order_status NOT NULL DEFAULT 'pending'
);

-- Add a new value (Postgres 12+, no rewrite of the table):
ALTER TYPE order_status ADD VALUE 'refunded';
```

Enums are compact and self-documenting, but **renaming/removing values is painful**. For statuses that change, prefer `TEXT` + a `CHECK` constraint or a small `statuses` lookup table.

---

## IV. CONSTRAINTS — SCHEMA AS GUARDRAILS

Constraints are the database doing your validation for you. **Every layer above the database can have bugs; the database is the last line of defense.**

### `NOT NULL`

```sql
CREATE TABLE products (
    product_id  BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    description TEXT             -- nullable: missing description is meaningful
);
```

Default to `NOT NULL`. Require an explicit reason for nullability — *"NULL means 'we don't know'"* — not "I forgot."

### `DEFAULT`

```sql
CREATE TABLE messages (
    message_id BIGSERIAL PRIMARY KEY,
    sent_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_read    BOOLEAN     NOT NULL DEFAULT FALSE
);
```

`DEFAULT` provides a value when the `INSERT` doesn't. Useful for timestamps, flags, status fields.

### `UNIQUE`

```sql
ALTER TABLE customers ADD CONSTRAINT uq_customers_email UNIQUE (email);

-- Composite UNIQUE (one user can like a post at most once):
ALTER TABLE likes ADD CONSTRAINT uq_likes_user_post UNIQUE (user_id, post_id);
```

`UNIQUE` allows multiple `NULL`s in standard SQL — Postgres treats two `NULL`s as distinct. (Postgres 15+ adds `NULLS NOT DISTINCT` to override.) MySQL does the same as Postgres by default.

### `CHECK`

```sql
CREATE TABLE accounts (
    account_id BIGSERIAL PRIMARY KEY,
    balance    NUMERIC(12,2) NOT NULL CHECK (balance >= 0),
    currency   CHAR(3)       NOT NULL CHECK (currency IN ('USD','EUR','GBP','INR'))
);

-- Multi-column CHECK at table level:
ALTER TABLE events
    ADD CONSTRAINT chk_dates CHECK (ends_at > starts_at);
```

`CHECK` is a per-row predicate. The DB rejects any insert/update that would make it false. Use it for value ranges, format checks, and cross-column invariants.

### `PRIMARY KEY`

Already covered in [`01`](./01-Relational-Model-And-Design.md). Implies `NOT NULL` + `UNIQUE` + an index.

### `FOREIGN KEY`

```sql
CREATE TABLE order_items (
    order_id  BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk_order_items_order   FOREIGN KEY (order_id)   REFERENCES orders(order_id)   ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);
```

The `ON DELETE`/`ON UPDATE` actions are listed in the previous file — `RESTRICT` is the safe default; `CASCADE` is for true ownership relationships (a parent's death takes its children with it).

### Naming constraints

Letting Postgres auto-name your constraints (`orders_status_check1`) is fine for a hobby project. In production, name them explicitly so error messages and migrations are readable:

```sql
ALTER TABLE orders
    ADD CONSTRAINT chk_orders_status_valid
    CHECK (status IN ('pending','paid','shipped','cancelled'));
```

---

## V. AUTO-INCREMENTING IDs

### `SERIAL` / `BIGSERIAL` (legacy, still common)

```sql
CREATE TABLE legacy_users (
    user_id BIGSERIAL PRIMARY KEY,
    name    TEXT NOT NULL
);

-- Behind the scenes, Postgres creates:
--   1. A sequence: legacy_users_user_id_seq
--   2. A column default: nextval('legacy_users_user_id_seq')
```

### `IDENTITY` (modern, SQL standard)

```sql
CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email   TEXT NOT NULL UNIQUE
);

-- BY DEFAULT vs ALWAYS:
--   GENERATED BY DEFAULT — you can override (e.g. INSERT INTO users (user_id, email) VALUES (...))
--   GENERATED ALWAYS     — overriding requires OVERRIDING SYSTEM VALUE (rare; safer)
```

`IDENTITY` is the SQL-standard form; new schemas should prefer it. Behavior is the same as `SERIAL` but it's tied to the column rather than a freestanding sequence.

### Sequences (the underlying mechanism)

```sql
CREATE SEQUENCE order_number_seq START 1000 INCREMENT 1;

CREATE TABLE orders (
    order_id     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_number BIGINT NOT NULL DEFAULT nextval('order_number_seq')
);

-- Inspect / advance manually:
SELECT nextval('order_number_seq');     -- returns next number, increments the sequence
SELECT currval('order_number_seq');     -- last value handed out in THIS session
ALTER SEQUENCE order_number_seq RESTART WITH 5000;
```

> **Gotcha — gaps in IDs.** If a transaction rolls back after `nextval` was called, the number is **not reused**. Sequences guarantee uniqueness, not contiguity. Don't build code that assumes "every ID exists."

> **MySQL note:** `AUTO_INCREMENT` is per-column and per-table; there are no cross-table sequences without manual emulation. SQL Server uses `IDENTITY(seed, increment)`.

### Generated (computed) columns

```sql
CREATE TABLE invoices (
    invoice_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subtotal   NUMERIC(10,2) NOT NULL,
    tax_rate   NUMERIC(4,4)  NOT NULL DEFAULT 0.0825,
    total      NUMERIC(10,2) GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) STORED
);
-- STORED = computed at write time, persisted on disk
-- VIRTUAL (other engines) = computed at read time
```

Useful for derived data you want to index or filter on.

---

## VI. `ALTER TABLE` — EVOLVING THE SCHEMA

Schemas live for years. You will alter them.

```sql
-- Add a column
ALTER TABLE customers
    ADD COLUMN phone TEXT;

-- Add with a NOT NULL + default (Postgres rewrites the table for the default; on big tables, do it in two steps — see below)
ALTER TABLE customers
    ADD COLUMN signup_source TEXT NOT NULL DEFAULT 'web';

-- Drop a column
ALTER TABLE customers DROP COLUMN phone;

-- Rename column / table
ALTER TABLE customers RENAME COLUMN name TO full_name;
ALTER TABLE customers RENAME TO people;

-- Change a column's type (may require an explicit USING)
ALTER TABLE products
    ALTER COLUMN list_price TYPE NUMERIC(12,2) USING list_price::NUMERIC(12,2);

-- Constraints
ALTER TABLE orders ADD CONSTRAINT chk_orders_total_positive CHECK (total_amount >= 0);
ALTER TABLE orders DROP CONSTRAINT chk_orders_total_positive;
ALTER TABLE orders ADD COLUMN customer_id BIGINT REFERENCES customers(customer_id);
```

### Big-table `ALTER` — the safe pattern

A naive `ADD COLUMN ... NOT NULL DEFAULT 'web'` on a billion-row table can lock the table for hours. The safe pattern in production:

```sql
-- 1. Add the column nullable, no default → fast metadata-only change
ALTER TABLE big_table ADD COLUMN new_col TEXT;

-- 2. Backfill in batches (in your app or a script)
UPDATE big_table SET new_col = 'default' WHERE new_col IS NULL AND id BETWEEN 1 AND 100000;
-- ... repeat in chunks ...

-- 3. Set NOT NULL once the column is fully populated
ALTER TABLE big_table ALTER COLUMN new_col SET NOT NULL;

-- 4. (Optional) Add the default for future inserts
ALTER TABLE big_table ALTER COLUMN new_col SET DEFAULT 'default';
```

> **Postgres 11+ shortcut:** `ADD COLUMN ... DEFAULT ...` no longer rewrites the table — it stores the default as metadata. But if you also add `NOT NULL`, plan carefully on huge tables.

---

## VII. `DROP` AND `TRUNCATE`

```sql
DROP TABLE IF EXISTS test_table CASCADE;   -- CASCADE drops dependent FKs/views too

DROP DATABASE old_db;                       -- gone forever

TRUNCATE TABLE logs;                        -- empties the table FAST (much faster than DELETE)
TRUNCATE TABLE logs RESTART IDENTITY;       -- also resets the IDENTITY sequence to start
TRUNCATE TABLE logs, audits CASCADE;        -- truncate multiple, including dependents
```

| | `DELETE FROM logs` | `TRUNCATE TABLE logs` | `DROP TABLE logs` |
|-|---|---|---|
| Removes rows | Yes | Yes | Yes (and the table) |
| Triggers fire? | Yes | No (no row-level events) | n/a |
| Returns affected count? | Yes | No | n/a |
| Inside a transaction (Postgres)? | Yes (rollback works) | Yes (Postgres-only; **MySQL TRUNCATE is auto-commit**) | Yes |
| Resets identity sequence? | No | Optional (`RESTART IDENTITY`) | Yes (table is gone) |
| Speed on big tables | Slow (per-row) | Very fast | Very fast |

> **Gotcha — `TRUNCATE` ignores `WHERE`.** It truncates the whole table, no filter. To delete a subset, use `DELETE`.

---

## VIII. DML — CHANGING DATA

### `INSERT`

```sql
-- Single row, named columns (the safe form — order-independent, robust to schema changes)
INSERT INTO customers (email, name, country_code)
VALUES ('alice@example.com', 'Alice', 'US');

-- Multi-row insert (one statement, one round trip → much faster than N inserts)
INSERT INTO customers (email, name) VALUES
    ('bob@example.com',   'Bob'),
    ('carol@example.com', 'Carol'),
    ('dan@example.com',   'Dan');

-- INSERT ... SELECT — copy from another table
INSERT INTO archived_orders (order_id, customer_id, placed_at, total_amount)
SELECT order_id, customer_id, placed_at, total_amount
FROM   orders
WHERE  placed_at < NOW() - INTERVAL '1 year';

-- RETURNING — get back what was inserted (Postgres) — invaluable for grabbing generated IDs
INSERT INTO orders (customer_id, total_amount)
VALUES (1, 99.95)
RETURNING order_id, placed_at;
```

> **Gotcha — positional inserts.** `INSERT INTO customers VALUES (...)` (no column list) breaks the moment you add or reorder a column. Always list the columns.

### `UPDATE`

```sql
-- Update with a filter
UPDATE customers
   SET city       = 'Berlin',
       updated_at = NOW()
 WHERE customer_id = 42;

-- Update with a join (Postgres "UPDATE ... FROM")
UPDATE order_items oi
   SET unit_price = b.list_price
  FROM books b
 WHERE oi.book_id = b.book_id
   AND oi.unit_price IS NULL;

-- Update with RETURNING — get the new values back
UPDATE orders
   SET status = 'shipped'
 WHERE status = 'paid'
RETURNING order_id, status;
```

> **Gotcha — the `WHERE` you forgot.** `UPDATE customers SET city = 'Berlin';` with no WHERE updates **every row**. Always run the equivalent `SELECT ... WHERE ...` first to confirm the row count, or run inside a transaction:

```sql
BEGIN;
UPDATE customers SET city = 'Berlin' WHERE customer_id = 42;
SELECT customer_id, city FROM customers WHERE customer_id = 42;   -- verify
-- ROLLBACK;     -- if it looks wrong
COMMIT;
```

### `DELETE`

```sql
DELETE FROM orders WHERE status = 'cancelled' AND placed_at < NOW() - INTERVAL '90 days';

-- DELETE with a join-equivalent via USING (Postgres)
DELETE FROM order_items oi
   USING orders o
  WHERE oi.order_id = o.order_id
    AND o.status = 'cancelled';

-- DELETE with RETURNING — handy for audit / soft-delete migration
DELETE FROM sessions
 WHERE expires_at < NOW()
RETURNING session_id, user_id;
```

The same WHERE-omission warning as `UPDATE` applies — `DELETE FROM orders;` empties the table.

### Soft delete (the alternative)

Deletion is final. For business data, prefer **soft delete**: a `deleted_at TIMESTAMPTZ` column, `NULL` for live rows.

```sql
ALTER TABLE customers ADD COLUMN deleted_at TIMESTAMPTZ;

-- "Delete" by setting the column
UPDATE customers SET deleted_at = NOW() WHERE customer_id = 42;

-- Live rows only:
SELECT * FROM customers WHERE deleted_at IS NULL;

-- Index that excludes deleted rows (a partial index — see file 06)
CREATE INDEX idx_customers_active_email
    ON customers(email)
    WHERE deleted_at IS NULL;
```

### `MERGE` / `UPSERT` — insert or update

The classic problem: "insert this row, or update it if it already exists."

#### Postgres — `INSERT ... ON CONFLICT`

```sql
INSERT INTO products (sku, name, list_price)
VALUES ('SKU-001', 'Widget', 9.99)
ON CONFLICT (sku)                            -- conflict target = the UNIQUE column
DO UPDATE SET                                -- on conflict, update these:
    name       = EXCLUDED.name,              -- EXCLUDED = the row we tried to insert
    list_price = EXCLUDED.list_price,
    updated_at = NOW();

-- "Insert if missing, do nothing if it's there":
INSERT INTO tags (name) VALUES ('intro')
ON CONFLICT (name) DO NOTHING;
```

#### MySQL — `INSERT ... ON DUPLICATE KEY UPDATE`

```sql
INSERT INTO products (sku, name, list_price) VALUES ('SKU-001', 'Widget', 9.99)
ON DUPLICATE KEY UPDATE name = VALUES(name), list_price = VALUES(list_price);
```

#### Standard SQL — `MERGE` (Postgres 15+, SQL Server, Oracle)

```sql
MERGE INTO products p
USING (VALUES ('SKU-001', 'Widget', 9.99)) AS s(sku, name, list_price)
ON p.sku = s.sku
WHEN MATCHED THEN
    UPDATE SET name = s.name, list_price = s.list_price
WHEN NOT MATCHED THEN
    INSERT (sku, name, list_price) VALUES (s.sku, s.name, s.list_price);
```

`ON CONFLICT` is the most ergonomic Postgres tool; `MERGE` is more general and the cross-dialect option.

---

## IX. PUTTING IT TOGETHER — A SEED SCRIPT

Here is a minimal, runnable seed for the bookstore from file [`01`](./01-Relational-Model-And-Design.md). Save as `seed.sql`, run with `psql -f seed.sql codex`.

```sql
BEGIN;

-- Wipe and rebuild (safe in a transaction; rolls back on any error)
DROP TABLE IF EXISTS order_items, orders, book_authors, books, authors, customers CASCADE;

CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    city        TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE authors (
    author_id  BIGSERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    birth_year INT
);

CREATE TABLE books (
    book_id      BIGSERIAL PRIMARY KEY,
    isbn         CHAR(13) UNIQUE,
    title        TEXT NOT NULL,
    pages        INT CHECK (pages > 0),
    published_on DATE,
    list_price   NUMERIC(10,2) NOT NULL CHECK (list_price >= 0)
);

CREATE TABLE book_authors (
    book_id   BIGINT NOT NULL REFERENCES books(book_id)     ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES authors(author_id) ON DELETE RESTRICT,
    role      TEXT NOT NULL DEFAULT 'primary',
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE orders (
    order_id    BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    placed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','paid','shipped','cancelled'))
);

CREATE TABLE order_items (
    order_id   BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    book_id    BIGINT NOT NULL REFERENCES books(book_id),
    quantity   INT    NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),
    PRIMARY KEY (order_id, book_id)
);

-- FK indexes
CREATE INDEX idx_book_authors_author_id ON book_authors(author_id);
CREATE INDEX idx_orders_customer_id     ON orders(customer_id);
CREATE INDEX idx_order_items_book_id    ON order_items(book_id);

-- Seed
INSERT INTO customers (email, name, city) VALUES
    ('alice@example.com', 'Alice Adams',   'Boston'),
    ('bob@example.com',   'Bob Brown',     'Berlin'),
    ('carol@example.com', 'Carol Carter',  'Boston');

INSERT INTO authors (name, birth_year) VALUES
    ('Martin Kleppmann',  1980),
    ('Robert C. Martin',  1952),
    ('Donald E. Knuth',   1938);

INSERT INTO books (isbn, title, pages, published_on, list_price) VALUES
    ('9781449373320', 'Designing Data-Intensive Applications', 616, '2017-03-16', 50.00),
    ('9780132350884', 'Clean Code',                            464, '2008-08-01', 35.00),
    ('9780201896831', 'The Art of Computer Programming Vol 1', 672, '1997-07-17', 80.00);

INSERT INTO book_authors (book_id, author_id) VALUES
    (1, 1),
    (2, 2),
    (3, 3);

-- One order with two items, demonstrating RETURNING
WITH new_order AS (
    INSERT INTO orders (customer_id, status)
    VALUES (1, 'paid')
    RETURNING order_id
)
INSERT INTO order_items (order_id, book_id, quantity, unit_price)
SELECT order_id, 1, 1, 50.00 FROM new_order
UNION ALL
SELECT order_id, 2, 2, 35.00 FROM new_order;

COMMIT;

-- Verify
SELECT (SELECT COUNT(*) FROM customers)   AS customers,
       (SELECT COUNT(*) FROM books)       AS books,
       (SELECT COUNT(*) FROM orders)      AS orders,
       (SELECT COUNT(*) FROM order_items) AS order_items;
```

---

## X. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| `INSERT` without column list | Schema change breaks every insert | Always list columns |
| Using `VARCHAR(255)` because "that's what people do" | Misleading documentation | Use `TEXT` (Postgres) or pick a real upper bound |
| `TIMESTAMP` instead of `TIMESTAMPTZ` | Time-zone confusion, off-by-N-hours bugs | Default to `TIMESTAMPTZ` |
| Floating point for money | Cent-level rounding errors | `NUMERIC(p,s)`, pass values as strings |
| `DELETE`/`UPDATE` without `WHERE` | Whole table affected | Always preview with `SELECT` or wrap in a transaction |
| Adding a `NOT NULL` column with default to a huge table | Long lock | Add nullable → backfill → `SET NOT NULL` |
| Forgetting `ON DELETE` action on FK | Surprises at delete time | Pick `RESTRICT` or `CASCADE` explicitly |
| Trusting client-side validation alone | Bad data slips in | `CHECK` constraints + `NOT NULL` |
| Using enums for fast-changing categories | Migrations get painful | Use a `categories` lookup table |
| Reusing a sequence after rollback assuming gaps won't happen | Logic that breaks on first gap | Treat IDs as opaque; never "next ID" math |
| Adding tons of FKs without indexing them | Slow deletes, mysterious lock waits | Index every FK column |

---

## 🧠 KEY TAKEAWAYS

- **DDL** defines schema; **DML** changes data; **DQL** reads it. Wrap migrations in transactions.
- Pick the **smallest, most specific** type. Use `TEXT` (Postgres) for strings, `NUMERIC(p,s)` for money, `TIMESTAMPTZ` for instants, `BOOLEAN` for true/false, `JSONB` only when shape is genuinely variable.
- **Constraints are validation that always runs.** `NOT NULL`, `UNIQUE`, `CHECK`, `PRIMARY KEY`, `FOREIGN KEY`. Default to `NOT NULL`; name your constraints.
- Prefer **`IDENTITY` columns** over `SERIAL` in new schemas; expect gaps in IDs after rollbacks.
- `TRUNCATE` is fast and resets identities (`RESTART IDENTITY`); `DELETE` is per-row, fires triggers, and respects `WHERE`.
- Use **`INSERT ... ON CONFLICT`** for Postgres upserts; `MERGE` for portable / SQL-Server-style writes.
- Always use **multi-row inserts** and the named-column form. Always preview destructive changes inside a transaction.
- For schema changes on big tables, do it **in stages** to avoid long locks: nullable add → backfill → `NOT NULL`.

---

**Prev:** [`01-Relational-Model-And-Design.md`](./01-Relational-Model-And-Design.md) · **Next:** [`03-Querying-Data-SELECT.md`](./03-Querying-Data-SELECT.md) · **Index:** [`00-Index.md`](./00-Index.md)
