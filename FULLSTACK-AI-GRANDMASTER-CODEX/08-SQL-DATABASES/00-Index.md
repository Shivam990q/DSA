# 🗄️ SQL & Relational Databases

> *"Memory is what an application thinks. The database is what it remembers. The web tier comes and goes. The schema lives for a decade."*

> **Section 08 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module takes you from `SELECT 1;` to designing, querying, indexing, securing, and scaling production relational databases — PostgreSQL by default, with notes for MySQL and SQL Server where they diverge.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- The **relational model** itself — what a table, row, key, and relation actually are, and why this model has outlasted every challenger for fifty years.
- **Database design**: ER modeling, the five flavors of keys, the six normal forms (1NF → BCNF → 4NF), and when to *deliberately* denormalize.
- **DDL & DML**: `CREATE`/`ALTER`/`DROP`, every important data type, every constraint, and `INSERT`/`UPDATE`/`DELETE`/`MERGE`/`UPSERT` patterns.
- **Querying**: `SELECT`, `WHERE`, every operator, `ORDER BY`, `LIMIT`/`OFFSET`, `DISTINCT`, `NULL` semantics, `CASE`, and the standard string/date/math function library.
- **Joins** — `INNER`, `LEFT`, `RIGHT`, `FULL`, `CROSS`, `SELF`, lateral, anti, and semi joins — plus `UNION`/`INTERSECT`/`EXCEPT`.
- **Advanced SQL**: aggregates, `GROUP BY`/`HAVING`/`GROUPING SETS`/`ROLLUP`/`CUBE`, scalar/correlated/`EXISTS` subqueries, `WITH` (CTEs), recursive CTEs, **window functions**, views, materialized views.
- **Performance**: how B-tree and hash indexes work, composite/covering/partial indexes, when indexes hurt, reading `EXPLAIN ANALYZE`, statistics, query rewriting.
- **Transactions**: ACID in detail, isolation levels (with anomaly tables), MVCC, optimistic vs pessimistic locking, deadlocks, `SAVEPOINT`.
- **Production**: stored procedures, triggers, **SQL injection** (and how parameterized queries kill it), roles & grants, replication, sharding, partitioning, backups, connection pooling, and how Node (`pg`) and Java (JDBC/JPA) talk to the database.

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file builds on the previous. ⭐ marks the highest-leverage files — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here · roadmap · setup | — |
| 01 | [`01-Relational-Model-And-Design.md`](./01-Relational-Model-And-Design.md) | Tables, rows, columns, keys (PK/FK/composite/candidate/surrogate/natural), ER diagrams, relationships (1:1, 1:N, M:N), normalization 1NF→BCNF, denormalization | ⭐ |
| 02 | [`02-SQL-Basics-DDL-And-DML.md`](./02-SQL-Basics-DDL-And-DML.md) | `CREATE`/`ALTER`/`DROP`, data types (numeric, text, date/time, boolean, JSON, arrays, UUID), constraints (NOT NULL, UNIQUE, CHECK, DEFAULT, PK, FK), `INSERT`/`UPDATE`/`DELETE`/`TRUNCATE`, `SERIAL`/`IDENTITY`/sequences | Core |
| 03 | [`03-Querying-Data-SELECT.md`](./03-Querying-Data-SELECT.md) | `SELECT`, `WHERE`, comparison & logical operators, `IN`/`BETWEEN`/`LIKE`/`ILIKE`, `ORDER BY`, `LIMIT`/`OFFSET`, `DISTINCT`, `NULL`/`COALESCE`/`NULLIF`, `CASE`, string/date/numeric functions | ⭐ |
| 04 | [`04-Joins-And-Relationships.md`](./04-Joins-And-Relationships.md) | INNER / LEFT / RIGHT / FULL / CROSS / SELF joins, multi-table joins, USING vs ON, lateral joins, anti & semi joins, `UNION`/`UNION ALL`/`INTERSECT`/`EXCEPT` | ⭐ |
| 05 | [`05-Aggregation-And-Advanced-Queries.md`](./05-Aggregation-And-Advanced-Queries.md) | Aggregates, `GROUP BY`, `HAVING`, `GROUPING SETS`/`ROLLUP`/`CUBE`, subqueries (scalar/correlated/`IN`/`EXISTS`), CTEs (`WITH`, recursive), window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`/`LEAD`, `SUM OVER`, `PARTITION BY`), views & materialized views | ⭐ |
| 06 | [`06-Indexing-And-Query-Optimization.md`](./06-Indexing-And-Query-Optimization.md) | How B-tree indexes really work, clustered vs non-clustered, composite/covering/partial/expression/hash/GIN/BRIN indexes, when indexes *hurt*, `EXPLAIN`/`EXPLAIN ANALYZE`, reading query plans, statistics, query rewriting | ⭐ |
| 07 | [`07-Transactions-And-Concurrency.md`](./07-Transactions-And-Concurrency.md) | Transactions, ACID deeply, `BEGIN`/`COMMIT`/`ROLLBACK`/`SAVEPOINT`, isolation levels (RU/RC/RR/SI/SS), dirty/non-repeatable/phantom reads, MVCC, locking (row/table, optimistic vs pessimistic), deadlocks | ⭐ |
| 08 | [`08-Advanced-SQL-And-Production.md`](./08-Advanced-SQL-And-Production.md) | Stored procedures & functions, triggers, **SQL injection** + parameterized queries, roles/grants/security, connecting from Node (`pg`/Prisma) and Java (JDBC/JPA), connection pooling, replication, sharding, partitioning, backups, scaling | ⭐ |

---

## 🗺️ COMPLETE SQL ROADMAP (coverage checklist)

> Roadmap.sh-style exhaustive checklist. **Reading only this codex covers all of it.** Each topic links to the file where it lives.

### A. Relational model & design
- [x] What a relation, tuple, attribute, domain are → [`01`](./01-Relational-Model-And-Design.md)
- [x] Tables, rows, columns; the row-as-tuple intuition → [`01`](./01-Relational-Model-And-Design.md)
- [x] **Primary key** (PK), **candidate key**, **composite key**, **alternate key** → [`01`](./01-Relational-Model-And-Design.md)
- [x] **Foreign key** (FK), referential integrity, ON DELETE / ON UPDATE actions → [`01`](./01-Relational-Model-And-Design.md), [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] **Surrogate vs natural keys** — when to use which → [`01`](./01-Relational-Model-And-Design.md)
- [x] **ER modeling** (entities, attributes, relationships, cardinality, ER diagrams) → [`01`](./01-Relational-Model-And-Design.md)
- [x] Relationships: **1:1, 1:N, M:N**, junction (associative) tables → [`01`](./01-Relational-Model-And-Design.md)
- [x] **Normalization**: 1NF, 2NF, 3NF, BCNF (with examples), pointer to 4NF/5NF → [`01`](./01-Relational-Model-And-Design.md)
- [x] **Denormalization** — when and why to break the rules → [`01`](./01-Relational-Model-And-Design.md)
- [x] Naming conventions, schema layout, schemas vs databases → [`01`](./01-Relational-Model-And-Design.md), [`02`](./02-SQL-Basics-DDL-And-DML.md)

### B. DDL — defining schema
- [x] `CREATE DATABASE`, `CREATE SCHEMA` → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] `CREATE TABLE` with all common column types → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] **Data types** — numeric (`INT`, `BIGINT`, `NUMERIC`, `REAL`/`DOUBLE`), text (`CHAR`, `VARCHAR`, `TEXT`), date/time (`DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMPTZ`, `INTERVAL`), boolean, `UUID`, `JSON`/`JSONB`, arrays, enums → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] Constraints: `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, `PRIMARY KEY`, `FOREIGN KEY` → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] `ALTER TABLE` — add/drop/rename columns, change types, add constraints → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] `DROP TABLE`, `TRUNCATE TABLE` (and how they differ from `DELETE`) → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] **Auto-increment**: `SERIAL`, `BIGSERIAL`, `IDENTITY`, sequences → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] Generated/computed columns → [`02`](./02-SQL-Basics-DDL-And-DML.md)

### C. DML — changing data
- [x] `INSERT INTO` (single, multi-row, `INSERT ... SELECT`, `RETURNING`) → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] `UPDATE ... SET ... WHERE` (with `FROM` clause for cross-table updates) → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] `DELETE FROM ... WHERE` (and the dreaded "no WHERE" mistake) → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] **Upsert** — `INSERT ... ON CONFLICT` (Postgres), `MERGE`, `INSERT ... ON DUPLICATE KEY UPDATE` (MySQL) → [`02`](./02-SQL-Basics-DDL-And-DML.md)
- [x] `TRUNCATE` vs `DELETE` (table-level) → [`02`](./02-SQL-Basics-DDL-And-DML.md)

### D. Querying — `SELECT`
- [x] Logical query order (`FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`) → [`03`](./03-Querying-Data-SELECT.md), [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] `SELECT` clauses, column aliases, table aliases → [`03`](./03-Querying-Data-SELECT.md)
- [x] `WHERE`, comparison & logical operators (`=`, `<>`, `<`, `>`, `<=`, `>=`, `AND`, `OR`, `NOT`) → [`03`](./03-Querying-Data-SELECT.md)
- [x] `IN`, `NOT IN`, `BETWEEN`, `LIKE`/`ILIKE`, pattern matching → [`03`](./03-Querying-Data-SELECT.md)
- [x] `ORDER BY` (`ASC`/`DESC`, multiple columns, `NULLS FIRST`/`LAST`) → [`03`](./03-Querying-Data-SELECT.md)
- [x] `LIMIT`/`OFFSET`/`FETCH FIRST n ROWS ONLY` → [`03`](./03-Querying-Data-SELECT.md)
- [x] `DISTINCT` and `DISTINCT ON` (Postgres) → [`03`](./03-Querying-Data-SELECT.md)
- [x] **`NULL` semantics** — three-valued logic, `IS NULL`, `COALESCE`, `NULLIF` → [`03`](./03-Querying-Data-SELECT.md)
- [x] `CASE WHEN ... THEN ... ELSE ... END` → [`03`](./03-Querying-Data-SELECT.md)
- [x] **String functions** (`LENGTH`, `UPPER`/`LOWER`, `TRIM`, `SUBSTRING`, `POSITION`, `CONCAT`, `\|\|`, `LEFT`/`RIGHT`, `REPLACE`, `REGEXP_*`) → [`03`](./03-Querying-Data-SELECT.md)
- [x] **Date/time functions** (`NOW`, `CURRENT_DATE`, `EXTRACT`, `DATE_TRUNC`, `AGE`, intervals, `+`/`-` arithmetic) → [`03`](./03-Querying-Data-SELECT.md)
- [x] **Numeric/math functions** (`ABS`, `ROUND`, `CEIL`/`FLOOR`, `MOD`, `POWER`, `RANDOM`) → [`03`](./03-Querying-Data-SELECT.md)
- [x] Type casting (`CAST(x AS type)` and `x::type`) → [`03`](./03-Querying-Data-SELECT.md)

### E. Joins & set operations
- [x] **`INNER JOIN`** → [`04`](./04-Joins-And-Relationships.md)
- [x] **`LEFT` / `RIGHT` / `FULL OUTER JOIN`** → [`04`](./04-Joins-And-Relationships.md)
- [x] **`CROSS JOIN`** (Cartesian product) → [`04`](./04-Joins-And-Relationships.md)
- [x] **Self join** → [`04`](./04-Joins-And-Relationships.md)
- [x] **`USING`** vs **`ON`** vs **natural join** (and why `NATURAL JOIN` is dangerous) → [`04`](./04-Joins-And-Relationships.md)
- [x] **Lateral joins** (`LATERAL` / `CROSS APPLY`) → [`04`](./04-Joins-And-Relationships.md)
- [x] **Anti-joins** (`NOT EXISTS`, `LEFT JOIN ... IS NULL`) and **semi-joins** (`EXISTS`) → [`04`](./04-Joins-And-Relationships.md), [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] Multi-table joins, join order, ambiguous column references → [`04`](./04-Joins-And-Relationships.md)
- [x] **Set operations**: `UNION` / `UNION ALL` / `INTERSECT` / `EXCEPT` (`MINUS`) → [`04`](./04-Joins-And-Relationships.md)

### F. Aggregation, subqueries, CTEs, windows
- [x] **Aggregate functions**: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `STRING_AGG`/`GROUP_CONCAT`, `ARRAY_AGG`, `BOOL_AND`/`BOOL_OR` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] `GROUP BY`, `HAVING`, the difference from `WHERE` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] `GROUPING SETS`, `ROLLUP`, `CUBE` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] **Subqueries**: scalar, row, table, correlated, `IN`, `NOT IN`, `EXISTS`, `NOT EXISTS`, `ANY`/`ALL` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] **CTEs**: `WITH ... AS (...)`, multiple CTEs, `WITH RECURSIVE` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] **Window functions**: `OVER`, `PARTITION BY`, `ORDER BY`, `ROWS`/`RANGE` frames → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] Ranking: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] Offset: `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE` → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] **Aggregate-as-window**: running totals, moving averages → [`05`](./05-Aggregation-And-Advanced-Queries.md)
- [x] **Views** (regular) and **materialized views** (with `REFRESH`) → [`05`](./05-Aggregation-And-Advanced-Queries.md)

### G. Indexing & query optimization
- [x] What an index is, conceptually (sorted side-table mapping value → row) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **B-tree** indexes (default) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Clustered** vs **non-clustered** indexes (and Postgres's heap model) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Composite** indexes & left-prefix rule → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Covering** indexes (`INCLUDE`) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Partial** indexes (`WHERE`) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Expression** indexes (functional) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Unique** indexes (and the index-vs-constraint relationship) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **Hash, GIN, GiST, BRIN, SP-GiST** — when to use each → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] When indexes **hurt** (write amplification, wasted space) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] **`EXPLAIN`** & **`EXPLAIN ANALYZE`** — reading query plans, scan types, costs → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] Statistics (`ANALYZE`, `pg_stat_*`) → [`06`](./06-Indexing-And-Query-Optimization.md)
- [x] Query rewriting techniques, anti-patterns (`SELECT *`, function on indexed column, OR-with-mixed-columns) → [`06`](./06-Indexing-And-Query-Optimization.md)

### H. Transactions, ACID, concurrency
- [x] What a transaction is; `BEGIN`/`COMMIT`/`ROLLBACK` → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **ACID** properties — Atomicity, Consistency, Isolation, Durability → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **Isolation levels**: Read Uncommitted, Read Committed, Repeatable Read, Snapshot, Serializable → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **Anomalies**: dirty read, non-repeatable read, phantom read, lost update, write skew → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **MVCC** (Multi-Version Concurrency Control) — what Postgres really does → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **Locking** — row-level, table-level, shared vs exclusive, `SELECT ... FOR UPDATE` / `FOR SHARE` → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **Optimistic** vs **pessimistic** concurrency → [`07`](./07-Transactions-And-Concurrency.md)
- [x] **Deadlocks** — how they form and how to avoid them → [`07`](./07-Transactions-And-Concurrency.md)
- [x] `SAVEPOINT` / nested transactions → [`07`](./07-Transactions-And-Concurrency.md)
- [x] Read-only transactions, `BEGIN ... ISOLATION LEVEL ...` → [`07`](./07-Transactions-And-Concurrency.md)

### I. Production: procedures, triggers, security, scaling
- [x] **Stored procedures** & **functions** (`PL/pgSQL`, parameters, `RETURNS`, control flow) → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Triggers** (`BEFORE`/`AFTER`, `INSERT`/`UPDATE`/`DELETE`, row vs statement) → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **SQL injection** — how it works and how parameterized queries kill it → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Roles, users, `GRANT`/`REVOKE`**, principle of least privilege → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] Row-level security (RLS) → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Connecting from Node** with `pg`, prepared statements, Prisma overview → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Connecting from Java** with JDBC, `PreparedStatement`, JPA/Hibernate overview → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Connection pooling** (PgBouncer, HikariCP, `pg-pool`) → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Replication** — primary/replica, sync vs async, read scaling → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Sharding** — horizontal partitioning, hash vs range, the cost → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Partitioning** (table partitioning, list/range/hash) → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Backups** (logical with `pg_dump`, physical with WAL/PITR) → [`08`](./08-Advanced-SQL-And-Production.md)
- [x] **Migrations** — Flyway, Liquibase, Prisma Migrate, knex → [`08`](./08-Advanced-SQL-And-Production.md)

---

## 🛠️ SETUP — GET A WORKING DATABASE

You need a server (the database itself) and a client (something that sends SQL to it).

### Option A — Install PostgreSQL locally (recommended)

Postgres is the default dialect of this codex. It is open source, free, fast, and has the deepest standards compliance. Everything you learn transfers.

| OS | Easiest path |
|----|--------------|
| Windows | [postgresql.org/download/windows](https://www.postgresql.org/download/windows) installer (includes pgAdmin) · or `winget install PostgreSQL.PostgreSQL.16` |
| macOS | [Postgres.app](https://postgresapp.com) (drag-drop) · or `brew install postgresql@16 && brew services start postgresql@16` |
| Linux | `sudo apt install postgresql-16` (Ubuntu/Debian); equivalents on other distros |

Verify the install:

```bash
psql --version          # client
pg_isready              # is the server up?
```

### Connecting

`psql` is the official command-line client. After install:

```bash
# Connect to the default database as the default superuser
psql -U postgres

# Inside psql, useful meta-commands:
\l            -- list databases
\c codex      -- connect to database "codex"
\dt           -- list tables in current schema
\d users      -- describe the "users" table
\du           -- list roles/users
\q            -- quit
```

> **Gotcha — Windows + `psql`.** If `psql` is "not recognized," its install folder (e.g. `C:\Program Files\PostgreSQL\16\bin`) is not on your `PATH`. Add it, then open a new terminal.

### Create your sandbox database

```sql
-- inside psql
CREATE DATABASE codex;        -- our sandbox
\c codex                      -- connect to it
SELECT version();             -- prove it's running
```

### Option B — Run Postgres in Docker (zero-friction)

```bash
docker run --name pg-codex -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
docker exec -it pg-codex psql -U postgres
```

### Option C — Browser sandboxes (zero install)

Useful for quick experiments, *not* for the multi-file project work:

- **<https://sqliteonline.com>** — fast, supports PostgreSQL mode.
- **<https://www.db-fiddle.com>** — share runnable snippets.
- **<https://dbfiddle.uk>** — also supports MySQL, SQL Server, MariaDB, Oracle.
- **<https://supabase.com>** (free tier) — real Postgres in the cloud with a SQL editor.

### GUI clients (optional but nice)

| Tool | Notes |
|------|-------|
| **pgAdmin 4** | Ships with the official Windows installer. Heavy but complete. |
| **DBeaver Community** | Cross-DB, free, the practical default. |
| **TablePlus** | Sleek; free tier with row limits. |
| **DataGrip** | Paid; the gold standard if you live in databases. |
| **VS Code** + *SQLTools* | Inline SQL inside your editor. |

### A note on dialects

This codex uses **PostgreSQL** as the default. Where MySQL, SQL Server, or SQLite differ in a way that matters, a `> **MySQL note:** ...` callout appears. The *concepts* are universal — `JOIN`, `GROUP BY`, transactions, indexes — the syntax for sequences, upserts, dates, and limits is where dialects fight each other.

| Topic | Postgres | MySQL | SQL Server |
|-------|----------|-------|------------|
| Auto-increment | `SERIAL` / `IDENTITY` | `AUTO_INCREMENT` | `IDENTITY(1,1)` |
| Limit | `LIMIT n OFFSET m` | `LIMIT m, n` | `OFFSET m ROWS FETCH NEXT n ROWS ONLY` |
| Upsert | `INSERT ... ON CONFLICT` | `INSERT ... ON DUPLICATE KEY UPDATE` | `MERGE` |
| Boolean | true / false | TINYINT(1) | BIT |
| String concat | `\|\|` or `CONCAT` | `CONCAT` only | `+` or `CONCAT` |
| Quoting identifiers | `"table"` | `` `table` `` | `[table]` |
| Current timestamp | `NOW()` / `CURRENT_TIMESTAMP` | `NOW()` | `GETDATE()` / `SYSDATETIME()` |

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Type every query.** Have `psql` (or DBeaver) open beside the file. Run each example, then break it on purpose to read the error.
2. **Build one schema as you read.** A bookstore, a fitness log, a tiny e-commerce. Add tables, indexes, and queries to it as new concepts appear.
3. **Don't skip file 06.** Indexing is where intermediate engineers become senior.
4. **Run `EXPLAIN ANALYZE` on every query you ever care about.** It is the single most valuable habit in this section.
5. **Read every "Common Pitfalls" table.** Those bugs are how every senior engineer was forged.

### The Project (do it once, all the way through)

Pick a domain you care about (a bookstore, a movie tracker, a personal CRM) and grow its schema as you read:

| After file | Your DB should... |
|------------|--------------------|
| 01 | Have a clean ER diagram on paper, normalized to at least 3NF, with a junction table for one M:N. |
| 02 | Exist in Postgres with `CREATE TABLE`s, all PKs/FKs/CHECKs in place, seeded with `INSERT`s. |
| 03 | Have 20 useful read queries: filters, sorts, pagination, NULL-safe aggregations. |
| 04 | Use multi-table joins for every "get with related data" query and `UNION`/`EXCEPT` somewhere meaningful. |
| 05 | Use a `GROUP BY` analytics query, a recursive CTE, and at least two window functions. |
| 06 | Have indexes added based on `EXPLAIN ANALYZE`, with a write-up of the before/after numbers. |
| 07 | Wrap a multi-step write in a transaction; demonstrate at least one isolation-level conflict on purpose. |
| 08 | Be reachable from a tiny Node or Java client with parameterized queries, a connection pool, a migration tool, and a backup script. |

That single, growing database is worth ten tutorials.

---

## 📅 SUGGESTED CADENCE

If you can give it 1–2 hours a day, this section comfortably fits in **3 weeks**:

| Week | Focus | Files |
|------|-------|-------|
| 1 | Model + DDL/DML + queries | 01 → 03 |
| 2 | Joins + advanced queries + indexing | 04 → 06 |
| 3 | Transactions + production | 07 → 08 |

Spend the last weekend connecting your schema to your Express API from section [`07`](../07-NODEJS-EXPRESS/) — that is where it all snaps together.

---

## 🔗 RELATED SECTIONS

- Pairs with [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/) — the API layer that talks to this database.
- Contrasted with [`09-NOSQL-MONGODB`](../09-NOSQL-MONGODB/) — knowing both is what makes you dangerous.
- Combined into a full app in [`10-MERN-STACK`](../10-MERN-STACK/) and shipped in [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/).
- Java backends use this DB through Spring Data JPA — see [`04-JAVA-MASTERY/08-Spring-Boot-Data-And-JPA.md`](../04-JAVA-MASTERY/08-Spring-Boot-Data-And-JPA.md).

---

## 📖 DEEP REFERENCES

- **PostgreSQL docs** — <https://www.postgresql.org/docs/current/> (the API is the source of truth; the *Tutorial* and *SQL Language* parts are gold)
- **Use The Index, Luke!** — <https://use-the-index-luke.com> (the best free book on SQL indexing ever written)
- **PostgreSQL Exercises** — <https://pgexercises.com> (interactive practice with feedback)
- **Mode SQL Tutorial** — <https://mode.com/sql-tutorial/> (analyst-focused, well structured)
- **MySQL docs** — <https://dev.mysql.com/doc/> (when you need MySQL specifics)
- **Designing Data-Intensive Applications**, Martin Kleppmann — the textbook on the *why* behind databases (consistency, replication, partitioning).
- **The Art of PostgreSQL**, Dimitri Fontaine — practical SQL written by a Postgres committer.
- **SQL Antipatterns**, Bill Karwin — the bugs you would otherwise hit in production.

---

**→ Begin:** [`01-Relational-Model-And-Design.md`](./01-Relational-Model-And-Design.md) | Back to [`../README.md`](../README.md)
