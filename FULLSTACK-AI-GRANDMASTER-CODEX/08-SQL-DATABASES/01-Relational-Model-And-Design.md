# 🗄️ 01 — Relational Model & Database Design

> *"The schema is the constitution of the application. You can rewrite the API, you can rewrite the UI, but the schema is what your data IS. Get it right and the system bends to you. Get it wrong and you fight your own data forever."*

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-SQL-Basics-DDL-And-DML.md`](./02-SQL-Basics-DDL-And-DML.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT THE RELATIONAL MODEL ACTUALLY IS

In 1970 Edgar F. Codd proposed that data should live in **relations** — sets of tuples — and be queried with a *language of relations*, not by walking pointers through trees and lists. That paper, *"A Relational Model of Data for Large Shared Data Banks,"* is the reason your bank balance is correct.

The model has three pieces:

1. **Structure** — data is organized as relations (tables).
2. **Integrity** — rules (keys, constraints) keep the data honest.
3. **Manipulation** — you describe *what* you want, not *how* to fetch it; the engine plans the *how*.

### Tables, rows, columns — and what they really are

```
relation  →  table
tuple     →  row    (exactly one fact about one thing)
attribute →  column (one property of that thing)
domain    →  the set of legal values for a column (its type + constraints)
```

A table is a **set of tuples** in the mathematical sense:

- Order of rows is **not significant** — `ORDER BY` exists because the relation itself is unordered.
- Order of columns is, in theory, also irrelevant — though SQL acknowledges it.
- There are **no duplicate rows** in a true relation — primary keys enforce that in practice.

```sql
-- A relation called "books"
CREATE TABLE books (
    id          BIGSERIAL PRIMARY KEY,        -- attribute "id",     domain: positive 64-bit ints
    title       TEXT NOT NULL,                -- attribute "title",  domain: non-null text
    isbn        CHAR(13) UNIQUE,              -- attribute "isbn",   domain: 13-char strings, unique
    pages       INTEGER CHECK (pages > 0),    -- attribute "pages",  domain: positive ints
    published   DATE,                         -- attribute "published", domain: dates (or NULL)
    genre       TEXT
);

-- A row (tuple) is one book.
INSERT INTO books (title, isbn, pages, published, genre)
VALUES ('Designing Data-Intensive Applications', '9781449373320', 616, '2017-03-16', 'Tech');
```

> **Mental model.** A row is one *fact* about one *thing*. A column is one *property* of that thing. The table is the set of all such facts of that kind.

### Why this beats the alternatives

| Model | Why it lost (mostly) |
|-------|----------------------|
| **Hierarchical** (IBM IMS, 1960s) | Forces a single tree; cross-cutting access is hard |
| **Network / CODASYL** | You navigate by pointer; the schema *is* the access path |
| **Document** (early 2010s NoSQL) | Trades joins for embedding; great for some shapes, painful for others (and MongoDB has been adding joins ever since) |
| **Key-value** | Simple, fast, but offloads all relationships to your code |

The relational model wins because **the access pattern is decoupled from the storage**. You design *what is true*; the optimizer picks *how to fetch it*. New queries work without changing the schema.

---

## II. KEYS — THE FIVE FLAVORS

A **key** is a column (or set of columns) that uniquely identifies a row. Get keys right and the rest of the schema falls into place.

### 1. Candidate key

A minimal set of columns whose values are **unique** and **never NULL**. A table can have many candidate keys.

```sql
-- Two candidate keys for "users":
--   • email (unique, required)
--   • phone (unique, required)
CREATE TABLE users (
    user_id  BIGSERIAL,
    email    TEXT NOT NULL UNIQUE,
    phone    TEXT NOT NULL UNIQUE,
    name     TEXT NOT NULL
);
```

### 2. Primary key (PK)

The **one** candidate key you choose as the row's official identifier. There is exactly one PK per table. By convention it is `id` (a surrogate, see below).

```sql
ALTER TABLE users ADD PRIMARY KEY (user_id);
-- email and phone remain UNIQUE (alternate keys) but are not THE primary key.
```

A primary key is automatically:
- `NOT NULL`
- `UNIQUE`
- backed by an index (on most engines, the **clustering** index)

### 3. Composite key

A primary or candidate key made of **more than one column**. Used heavily in junction tables.

```sql
-- A student can enroll in many courses; a course has many students.
-- The "natural" identity of an enrollment is (student_id, course_id).
CREATE TABLE enrollments (
    student_id BIGINT NOT NULL REFERENCES students(student_id),
    course_id  BIGINT NOT NULL REFERENCES courses(course_id),
    enrolled_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (student_id, course_id)   -- composite PK
);
```

### 4. Alternate key

Any candidate key that is **not** the primary key. Enforced via `UNIQUE`.

### 5. Foreign key (FK)

A column (or set) in one table whose values must match a primary/unique key in another table — or be `NULL`. This is **referential integrity**: the database refuses to let you create dangling references.

```sql
CREATE TABLE authors (
    author_id BIGSERIAL PRIMARY KEY,
    name      TEXT NOT NULL
);

CREATE TABLE books (
    book_id   BIGSERIAL PRIMARY KEY,
    title     TEXT NOT NULL,
    author_id BIGINT NOT NULL REFERENCES authors(author_id)   -- FK
        ON DELETE RESTRICT       -- can't delete an author who has books
        ON UPDATE CASCADE        -- if author_id changes (rare), update books too
);
```

`ON DELETE` actions you should know:

| Action | Behavior on parent delete |
|--------|----------------------------|
| `RESTRICT` / `NO ACTION` | Reject the delete if any child rows exist (the safe default) |
| `CASCADE` | Delete child rows too (use sparingly — easy to nuke half your DB) |
| `SET NULL` | Set the FK column to `NULL` in children (column must be nullable) |
| `SET DEFAULT` | Set to the column's `DEFAULT` value |

> **Gotcha — implicit "no FK index."** A foreign key column gets *no automatic index* in Postgres. Without one, deleting a parent row can scan the entire child table. Add an index on every FK column. We come back to this in file [`06`](./06-Indexing-And-Query-Optimization.md).

### Surrogate vs natural keys

A **natural key** comes from the real world: ISBN, email, social security number, country code. A **surrogate key** is invented by the system: `id BIGSERIAL`, `id UUID`.

| | Natural | Surrogate |
|-|---------|-----------|
| Source | Real world | Generated |
| Stability | Can change (people change emails) | Never changes |
| Size | Variable (text often) | Compact (8 bytes for `BIGINT`) |
| Joins | Larger keys → fatter indexes | Cheap |
| Privacy | Leaks meaningful data | Opaque |
| Debugging | "User 42" is meaningless | "alice@example.com" is obvious |

**Rule of thumb (modern):** use a **surrogate primary key** (`BIGSERIAL` or `UUID`) for stability and join speed; keep the natural key as a `UNIQUE` constraint so the database still refuses duplicates.

```sql
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,    -- surrogate (the "stable handle")
    sku        TEXT NOT NULL UNIQUE,     -- natural key — still enforced unique
    name       TEXT NOT NULL
);
```

> **`BIGSERIAL` vs `UUID`.** `BIGSERIAL` is small, sortable, and gives sequential disk locality (great for indexes). `UUID` is globally unique without coordination — perfect for distributed systems and client-generated IDs — but is 16 bytes and randomly distributed (worse cache locality unless you use UUIDv7). Use `BIGSERIAL` by default; use `UUID` when you need distributed generation or want to expose IDs in URLs without leaking row counts.

---

## III. ENTITY-RELATIONSHIP (ER) MODELING

ER modeling is how you go from "we sell books" to a working schema. You draw entities, give them attributes, and connect them with relationships.

### Vocabulary

- **Entity** — a thing you store data about: `Author`, `Book`, `Order`.
- **Attribute** — a property of that entity: `Book.title`, `Book.pages`.
- **Relationship** — an association between entities: *Author writes Book*.
- **Cardinality** — how many of each side participate: 1:1, 1:N, M:N.
- **Participation** — mandatory (every order has a customer) or optional (a customer might have zero orders).

### A worked example — a bookstore

Stakeholder says:

> "We sell books. A book has one or more authors. Authors write many books. Customers place orders. Each order has many books on it."

Entities: **Author**, **Book**, **Customer**, **Order**.
Relationships:
- *Authors ↔ Books* — many-to-many (M:N).
- *Customers ↔ Orders* — one-to-many (1:N) — one customer, many orders.
- *Orders ↔ Books* — many-to-many (M:N) — order has many books, a book is on many orders.

Cardinality on a Crow's Foot diagram:

```
              writes                            places
   AUTHOR  ─<───────>─  BOOK         CUSTOMER  ─<───────  ORDER
                                                      │
                                                      │ contains
                                                      ▼
                                                    BOOK   (M:N via order_items)
```

(`─<` = "many" side, `──` = "one" side.)

---

## IV. RELATIONSHIPS IN SQL

### One-to-One (1:1)

Each row in A is associated with at most one row in B and vice versa. Less common — usually used to split rarely-needed columns into a separate table.

```sql
CREATE TABLE users (
    user_id   BIGSERIAL PRIMARY KEY,
    email     TEXT NOT NULL UNIQUE,
    name      TEXT NOT NULL
);

-- Sensitive profile data is stored separately, with a 1:1 relationship.
-- The trick: the FK is ALSO the PK on the child side → max one row per user.
CREATE TABLE user_profiles (
    user_id     BIGINT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    bio         TEXT,
    birth_date  DATE
);
```

### One-to-Many (1:N) — the workhorse

Each row in A relates to many rows in B; each row in B relates to one row in A.

```sql
-- One author has many books; each book has one (primary) author.
CREATE TABLE authors (
    author_id BIGSERIAL PRIMARY KEY,
    name      TEXT NOT NULL
);

CREATE TABLE books (
    book_id   BIGSERIAL PRIMARY KEY,
    title     TEXT NOT NULL,
    author_id BIGINT NOT NULL REFERENCES authors(author_id)  -- the FK lives on the "many" side
);

-- Always index the FK column (Postgres won't do it for you):
CREATE INDEX idx_books_author_id ON books(author_id);
```

### Many-to-Many (M:N) — junction (associative) tables

There is no native M:N in SQL; you decompose it into two 1:N relationships through a third table.

```sql
-- The famous "junction" or "join" or "associative" table.
-- Composite PK guarantees a (book, author) pair appears at most once.
CREATE TABLE book_authors (
    book_id   BIGINT NOT NULL REFERENCES books(book_id)     ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES authors(author_id) ON DELETE CASCADE,
    role      TEXT,           -- 'primary', 'co-author', 'editor', ...
    PRIMARY KEY (book_id, author_id)
);

CREATE INDEX idx_book_authors_author_id ON book_authors(author_id); -- for "which books did X write?"
-- The PK already gives us an index on (book_id, author_id) so "authors of book Y" is fast.
```

When the M:N has *its own* attributes (a date, a quantity, a price), the junction table becomes a real entity:

```sql
CREATE TABLE order_items (
    order_id     BIGINT NOT NULL REFERENCES orders(order_id),
    book_id      BIGINT NOT NULL REFERENCES books(book_id),
    quantity     INT    NOT NULL CHECK (quantity > 0),
    unit_price   NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (order_id, book_id)
);
```

### Self-referential (recursive)

A row references another row in the **same** table. Classic case: an org chart.

```sql
CREATE TABLE employees (
    employee_id BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    manager_id  BIGINT REFERENCES employees(employee_id)   -- nullable: the CEO has no boss
);
```

We will walk this hierarchy with a `WITH RECURSIVE` CTE in file [`05`](./05-Aggregation-And-Advanced-Queries.md).

---

## V. NORMALIZATION — 1NF → BCNF, EXPLAINED

Normalization is a series of rules for organizing columns into tables so the schema **doesn't lie to you**. Each normal form removes a class of redundancy and update anomaly.

The three classic anomalies:
- **Update anomaly** — same fact stored in many places, so you have to update them all (and forget one).
- **Insertion anomaly** — you can't add a fact because some unrelated piece of data is missing.
- **Deletion anomaly** — deleting a row deletes a fact you didn't mean to lose.

### The bad schema we will fix

```sql
-- ANTI-PATTERN — purchases table that violates normalization head to toe.
CREATE TABLE purchases_bad (
    purchase_id   BIGINT PRIMARY KEY,
    customer_id   BIGINT,
    customer_name TEXT,                          -- ← duplicated for every purchase by Alice
    customer_city TEXT,                          -- ← also duplicated
    book_titles   TEXT,                          -- ← e.g. "Book A, Book B" (repeating group!)
    book_prices   TEXT,                          -- ← parallel array, easy to desync
    total         NUMERIC(10,2)
);
```

### 1NF — First Normal Form: atomic columns, no repeating groups

> **Each column holds a single atomic value, not a list, set, or nested structure.**

The `book_titles` and `book_prices` strings violate 1NF — they're lists shoved into a column.

```sql
-- 1NF: split repeating groups into rows in a child table.
CREATE TABLE purchases_1nf (
    purchase_id   BIGINT PRIMARY KEY,
    customer_id   BIGINT,
    customer_name TEXT,
    customer_city TEXT,
    total         NUMERIC(10,2)
);

CREATE TABLE purchase_items_1nf (
    purchase_id BIGINT REFERENCES purchases_1nf(purchase_id),
    book_title  TEXT,
    price       NUMERIC(10,2),
    PRIMARY KEY (purchase_id, book_title)
);
```

> **Modern note.** If you're on Postgres, `JSONB` and array types technically allow non-atomic columns. They have legitimate uses (denormalized read models, sparse attributes), but **start in 1NF and only deviate when the cost of joining is proven to hurt**.

### 2NF — Second Normal Form: no partial dependencies

> **Every non-key column depends on the *whole* primary key, not just part of it.** (Only relevant when the PK is composite.)

```sql
-- Suppose this table's PK is composite (purchase_id, book_id).
CREATE TABLE purchase_items_bad (
    purchase_id   BIGINT,
    book_id       BIGINT,
    book_title    TEXT,    -- ← depends ONLY on book_id, not the whole (purchase_id, book_id)
    quantity      INT,
    PRIMARY KEY (purchase_id, book_id)
);
```

Fix: move the partially dependent column to the table where its key really lives.

```sql
CREATE TABLE books (
    book_id BIGINT PRIMARY KEY,
    title   TEXT NOT NULL
);

CREATE TABLE purchase_items_2nf (
    purchase_id BIGINT,
    book_id     BIGINT REFERENCES books(book_id),
    quantity    INT,
    PRIMARY KEY (purchase_id, book_id)
);
```

### 3NF — Third Normal Form: no transitive dependencies

> **Every non-key column depends on the key, the *whole* key, and *nothing but* the key.**

In `purchases_1nf`, `customer_city` depends on `customer_id`, which depends on `purchase_id`. That is a *transitive* dependency: `customer_city` depends on the PK only *through* another column.

Fix:

```sql
CREATE TABLE customers (
    customer_id   BIGINT PRIMARY KEY,
    customer_name TEXT,
    customer_city TEXT
);

CREATE TABLE purchases_3nf (
    purchase_id BIGINT PRIMARY KEY,
    customer_id BIGINT REFERENCES customers(customer_id),
    total       NUMERIC(10,2)
);
```

Now Alice's city is stored *once*. Update one row to move her to Berlin and every purchase reflects it.

### BCNF — Boyce-Codd Normal Form

> **For every non-trivial dependency `X → Y`, `X` is a superkey.**

BCNF strengthens 3NF for the rare case where you have overlapping candidate keys. Practical example: a course-instructor-room table where `(course, time) → room` and `(room, time) → course`. 3NF lets weirdness sneak in; BCNF doesn't.

If you can articulate every dependency in your table and every left-hand side is a key, you are in BCNF — which most well-designed schemas naturally are.

### 4NF and 5NF (pointer)

- **4NF** removes *multi-valued dependencies* — when one column independently determines two unrelated lists.
- **5NF (PJ/NF)** decomposes when a table can only be reconstructed by joining three or more.

These rarely matter in OLTP systems but appear in deep modeling work. The Wikipedia entries are the standard reference if you need them.

### A normalization quick-test

When designing a table, ask:
1. Does each column hold one value? *(1NF)*
2. Does the PK fully identify every other column? *(2NF, 3NF)*
3. Could any non-key column be inferred from another non-key column? If yes → split. *(3NF)*
4. Are there overlapping candidate keys with weird dependencies? *(BCNF)*

| NF | Removes | Mnemonic |
|----|---------|----------|
| 1NF | Repeating groups, non-atomic columns | "atomic" |
| 2NF | Partial dependency on a composite PK | "the whole key" |
| 3NF | Transitive dependency through non-keys | "and nothing but the key" |
| BCNF | Anomalies from overlapping candidate keys | "every determinant is a key" |
| 4NF | Multi-valued dependencies | "independent multi-values split" |
| 5NF | Join dependencies | "no spurious tuples on rejoin" |

---

## VI. DENORMALIZATION — BREAKING THE RULES, ON PURPOSE

Normalization optimizes for **write integrity**. Denormalization optimizes for **read speed**, paid for with extra writes.

You denormalize when, and only when:
- Profiling shows a join or aggregation is the actual bottleneck.
- The denormalized data has a clear maintenance plan (trigger, materialized view, scheduled job).
- The team accepts the extra write cost and complexity.

### Common denormalization techniques

| Technique | What | When |
|-----------|------|------|
| **Caching computed columns** | Store `total` on `orders` instead of summing items every read | High-read OLTP |
| **Duplicating reference data** | Copy `customer_name` onto `orders` for fast list views | Reporting |
| **Materialized view** | Precomputed query result, refreshed on a schedule | Dashboards, analytics |
| **Read replicas** | Whole-DB copy, normalization unchanged | Scaling reads (file [`08`](./08-Advanced-SQL-And-Production.md)) |
| **Wide table / OLAP star schema** | Fact + dimension tables; controlled redundancy | Data warehouse |

```sql
-- A denormalized "fast list" table for the dashboard.
-- Updated by a trigger or a scheduled job; not the source of truth.
CREATE TABLE order_summary (
    order_id        BIGINT PRIMARY KEY,
    customer_name   TEXT NOT NULL,
    item_count      INT  NOT NULL,
    total_amount    NUMERIC(10,2) NOT NULL,
    placed_at       TIMESTAMPTZ NOT NULL
);
```

> **Gotcha — denormalized data goes stale.** The moment you copy a fact, you must own its synchronization. Pick your sync mechanism (trigger, materialized view, application logic) *before* you ship the duplication.

---

## VII. NAMING CONVENTIONS THAT SAVE FUTURE-YOU

A schema you can read at 3 a.m. is a schema that bows to you.

| Convention | Why |
|------------|-----|
| `snake_case`, lowercase | Postgres lower-cases unquoted identifiers; mixing styles invites bugs |
| Plural table names: `users`, `orders` | A row is one user; the table is the set |
| Singular column names: `user_id`, `created_at` | One value per cell |
| `_id` suffix for FKs: `author_id`, `customer_id` | Self-documenting joins |
| Time columns: `created_at`, `updated_at`, `deleted_at` | Soft-delete + audit ready |
| Boolean: `is_*` / `has_*` (`is_active`, `has_paid`) | Reads like English |
| Junction tables: alphabetical: `book_authors`, not `authors_book` | Predictable |
| Index names: `idx_<table>_<columns>` | Greppable |
| FK constraint names: `fk_<table>_<col>` | Easy to drop/rename |

```sql
-- Clean, conventional layout:
CREATE TABLE orders (
    order_id     BIGSERIAL PRIMARY KEY,
    customer_id  BIGINT NOT NULL REFERENCES customers(customer_id),
    placed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_paid      BOOLEAN NOT NULL DEFAULT FALSE,
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_placed_at   ON orders(placed_at DESC);
```

### Schemas vs databases

A **database** is the top-level container; a **schema** is a namespace inside it.

```sql
CREATE DATABASE bookstore;
\c bookstore

CREATE SCHEMA sales;     -- group all sales tables here
CREATE SCHEMA inventory; -- group all inventory tables here

CREATE TABLE sales.orders (...);
CREATE TABLE inventory.books (...);

-- The default schema is "public". The search path picks which schema is searched first:
SHOW search_path;          -- "$user", public
SET search_path TO sales, public;
```

Use schemas to group related tables in larger systems and to separate microservices' data inside one Postgres instance.

---

## VIII. A WORKED DESIGN — A REAL BOOKSTORE

Here is a normalized, conventional, production-feeling design for the bookstore example. Save this — you will extend it across files [`02`](./02-SQL-Basics-DDL-And-DML.md)–[`08`](./08-Advanced-SQL-And-Production.md).

```sql
-- =========================================================================
-- BOOKSTORE — normalized to 3NF, with the most useful indexes.
-- =========================================================================

-- People we sell to.
CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    email       TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    city        TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- People who write books.
CREATE TABLE authors (
    author_id  BIGSERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    birth_year INT
);

-- Books (one row per title, not per copy).
CREATE TABLE books (
    book_id      BIGSERIAL PRIMARY KEY,
    isbn         CHAR(13) UNIQUE,                 -- natural key, kept unique
    title        TEXT NOT NULL,
    pages        INT CHECK (pages > 0),
    published_on DATE,
    list_price   NUMERIC(10,2) NOT NULL CHECK (list_price >= 0)
);

-- M:N — a book can have many authors; an author writes many books.
CREATE TABLE book_authors (
    book_id   BIGINT NOT NULL REFERENCES books(book_id)     ON DELETE CASCADE,
    author_id BIGINT NOT NULL REFERENCES authors(author_id) ON DELETE RESTRICT,
    role      TEXT NOT NULL DEFAULT 'primary',
    PRIMARY KEY (book_id, author_id)
);

CREATE INDEX idx_book_authors_author_id ON book_authors(author_id);

-- Orders header.
CREATE TABLE orders (
    order_id    BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    placed_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status      TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending','paid','shipped','cancelled'))
);

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_placed_at   ON orders(placed_at DESC);

-- Line items — M:N between orders and books, with its own attributes.
CREATE TABLE order_items (
    order_id   BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    book_id    BIGINT NOT NULL REFERENCES books(book_id),
    quantity   INT    NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10,2) NOT NULL CHECK (unit_price >= 0),  -- snapshot of price at sale time
    PRIMARY KEY (order_id, book_id)
);

CREATE INDEX idx_order_items_book_id ON order_items(book_id);
```

Why this is good:

- **3NF**: every non-key column depends only on the key; no transitive dependencies.
- **Surrogate PKs** (`*_id BIGSERIAL`) for stable, fast joins; `isbn` and `email` kept as `UNIQUE`.
- **Junction tables** (`book_authors`, `order_items`) for both M:N relationships, with composite PKs.
- **`unit_price` snapshot** on `order_items` — a *deliberate* denormalization. The list price might change tomorrow; the order should remember what was charged.
- **FK indexes** on every FK column. Postgres won't auto-create them.
- **Status `CHECK` constraint** keeps bad values out (we'll see enums in file [`02`](./02-SQL-Basics-DDL-And-DML.md)).

---

## IX. DESIGN SMELLS — THE THINGS WE NEVER DO

| Smell | Why it's bad |
|-------|--------------|
| Comma-separated values in a column (`tags: 'a,b,c'`) | Violates 1NF; can't index, can't join, breaks at the first comma in a value |
| Numbered columns (`tag1`, `tag2`, `tag3`) | What about tag 4? You'll be running `ALTER TABLE` forever |
| Boolean column for every status (`is_pending`, `is_paid`, `is_shipped`) | Use one `status` column with a `CHECK` or enum |
| Storing computed totals when the source is in the same DB | Either compute on read or use a materialized view |
| One giant `users` table with 80 columns | Split into `users` + `user_profiles` + `user_settings` |
| Reusing PKs after deletion | Causes orphaned data confusion; never recycle IDs |
| `VARCHAR(255)` everywhere for no reason | Pick the type the data actually wants (`TEXT`, `EMAIL` domain, `UUID`) |
| FK without index | Slow deletes/updates on the parent |
| Storing `state` AND `city` AND `country` AND `zip` all as free text | Look up against reference tables |
| Mixing case in identifiers (`MyTable`) | Postgres lower-cases unquoted names — confusion guaranteed |

---

## X. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Forgetting `NOT NULL` on a column that should always be present | Half your rows have `NULL`; aggregates lie | Default to `NOT NULL`; require an explicit reason to allow `NULL` |
| FK without `ON DELETE` action | Cascade chaos *or* deletes blocked unexpectedly | Pick `RESTRICT` (safe) or `CASCADE` (with care); never leave it implicit |
| Missing index on FK column | Slow deletes on parent, slow "child of X" queries | `CREATE INDEX` on every FK |
| Composite PK in wrong column order | Wrong index works for some queries, not others | Put the most-filtered column first |
| Floats for money | Off-by-cent errors | Use `NUMERIC(p, s)` (file [`02`](./02-SQL-Basics-DDL-And-DML.md)) |
| Premature denormalization | Sync drift, bugs that "work on dev" | Normalize first; denormalize only with proof and a sync plan |
| Reusing IDs after delete | Stale references resolve to the wrong row | Never reset sequences in production |
| Storing display strings instead of enum codes | Translation/i18n nightmares | Store stable codes; map to display in the app |
| Accidentally storing two facts in one column (`"NY, USA"`) | Can't filter by country alone | Split into atomic columns |
| Skipping a junction table for "small" M:Ns | Becomes M:N anyway, but messy | Use a junction table from day one |

---

## 🧠 KEY TAKEAWAYS

- The **relational model** is structure (tables) + integrity (keys/constraints) + a declarative query language. *What*, not *how*.
- A **table is a set of facts**; a row is one fact; a column is one property. Order is irrelevant; uniqueness comes from keys.
- Master the **five key types**: candidate, primary, composite, alternate, foreign. Default to a **surrogate PK + UNIQUE on the natural key**.
- Foreign keys are the difference between a database and a pile of spreadsheets — and **they need indexes**.
- Use **ER thinking** to discover entities and relationships. M:N relationships always become **junction tables**.
- **Normalize to 3NF/BCNF by default.** Each NF removes a class of update/insert/delete anomaly; each fix prevents a future incident.
- **Denormalize on purpose**, with proof and a sync plan — never as the default.
- Apply ruthless **naming discipline**: `snake_case`, plural tables, `_id` suffixes, `created_at`/`updated_at`, indexed FKs.

---

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-SQL-Basics-DDL-And-DML.md`](./02-SQL-Basics-DDL-And-DML.md) · **Index:** [`00-Index.md`](./00-Index.md)
