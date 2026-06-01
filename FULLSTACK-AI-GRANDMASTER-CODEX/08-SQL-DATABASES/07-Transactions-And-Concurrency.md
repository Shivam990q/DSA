# 🗄️ 07 — Transactions & Concurrency

> *"A transaction is a promise the database makes: all of it happens, or none of it does — and while it happens, the chaos of other users can't corrupt your view of the world."*

**Prev:** [`06-Indexing-And-Query-Optimization.md`](./06-Indexing-And-Query-Optimization.md) · **Next:** [`08-Advanced-SQL-And-Production.md`](./08-Advanced-SQL-And-Production.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT A TRANSACTION IS

A **transaction** is a group of SQL statements that the database treats as a **single, indivisible unit of work**. Either *every* statement succeeds and is made permanent (`COMMIT`), or *something* fails and the database undoes *all* of them as if none had run (`ROLLBACK`).

The canonical motivation: a **bank transfer**. Moving $100 from Alice to Bob is two statements:

```sql
UPDATE accounts SET balance = balance - 100 WHERE id = 'alice';   -- step 1
UPDATE accounts SET balance = balance + 100 WHERE id = 'bob';     -- step 2
```

If the server crashes *between* step 1 and step 2, Alice has lost $100 and Bob never received it. **Money vanished.** A transaction makes both steps atomic — they happen together or not at all:

```sql
BEGIN;                                                            -- start the transaction
  UPDATE accounts SET balance = balance - 100 WHERE id = 'alice';
  UPDATE accounts SET balance = balance + 100 WHERE id = 'bob';
COMMIT;                                                           -- both permanent, together
-- If anything fails before COMMIT, ROLLBACK undoes step 1 too — no money is ever lost.
```

> Without transactions, every multi-step operation is a corruption waiting to happen. With them, you reason about correctness at the level of *business operations* ("transfer money") instead of individual row writes.

---

## II. ACID — THE FOUR GUARANTEES, DEEPLY

ACID is the set of properties a transactional database promises. Each solves a specific class of disaster.

### A — Atomicity ("all or nothing")

All statements in a transaction succeed together or fail together. There is no partial application. If statement 3 of 5 errors, statements 1 and 2 are rolled back.

```sql
BEGIN;
  INSERT INTO orders (id, user_id, total) VALUES (1, 5, 99);
  INSERT INTO order_items (order_id, product_id) VALUES (1, 999);  -- FK violation → ERROR
COMMIT;
-- The whole transaction aborts: the orders row is NOT inserted either. All-or-nothing.
```

> Atomicity is what makes the bank transfer safe against crashes. The database keeps an **undo log** so it can reverse partial work.

### C — Consistency ("the database moves from one valid state to another")

A transaction can never leave the database violating its declared rules — constraints (`CHECK`, `NOT NULL`, `UNIQUE`, foreign keys), triggers, and cascades. If a transaction would violate any of them, it's rejected.

```sql
-- Suppose: CHECK (balance >= 0)
BEGIN;
  UPDATE accounts SET balance = balance - 1000 WHERE id = 'alice';  -- would go negative
COMMIT;
-- The CHECK constraint fails → the transaction is rolled back. Invariant preserved.
```

> Consistency here is the *database* kind (constraints hold). It's different from the "C" in the CAP theorem (distributed consistency) — don't conflate them. Your job: declare the right constraints so "valid" is actually enforced, not just hoped for.

### I — Isolation ("concurrent transactions don't step on each other")

Transactions running at the same time should behave *as if* they ran one after another. Without isolation, two transactions reading and writing the same rows interleave and produce anomalies (§IV). Isolation is a **spectrum** (§V) — stronger isolation = fewer anomalies but less concurrency.

### D — Durability ("once committed, it survives crashes")

After `COMMIT` returns success, the data is permanent — even if the server loses power one millisecond later. Databases achieve this with a **write-ahead log (WAL)**: changes are written to a durable log *before* `COMMIT` returns, so a crash can replay the log on restart.

```
COMMIT returns ──► WAL flushed to disk ──► even a crash now can't lose the data (replay on restart)
```

> **Gotcha — durability depends on the disk actually flushing.** If `fsync` is disabled (or a cheap disk lies about flushing), a committed transaction can still be lost on power failure. Postgres `synchronous_commit = off` trades a small durability window for speed — know when that tradeoff is acceptable (it usually isn't for money).

| Property | One-line meaning | Mechanism | Disaster it prevents |
|----------|------------------|-----------|----------------------|
| **Atomicity** | All or nothing | Undo log | Half-finished operations |
| **Consistency** | Only valid states | Constraints/triggers | Broken invariants (negative balance) |
| **Isolation** | As if run serially | Locks / MVCC | Concurrent corruption (§IV) |
| **Durability** | Survives crashes | Write-ahead log (WAL) | Losing committed data on crash |

---

## III. BEGIN / COMMIT / ROLLBACK / SAVEPOINT

### The core verbs

```sql
BEGIN;            -- (or START TRANSACTION) open a transaction; nothing is visible to others yet
  -- ... statements ...
COMMIT;           -- make all changes permanent and visible to other transactions
-- or:
ROLLBACK;         -- discard ALL changes since BEGIN; the database is as if nothing happened
```

> **Autocommit:** outside an explicit `BEGIN`, most databases run each statement in its own implicit transaction (it commits immediately). `BEGIN` is how you group multiple statements into one unit.

### SAVEPOINT — partial rollback within a transaction

A **savepoint** is a named checkpoint inside a transaction. You can roll back to it without abandoning the whole transaction — useful for "try this optional step; if it fails, skip it but keep the rest."

```sql
BEGIN;
  INSERT INTO orders (id, user_id, total) VALUES (10, 5, 200);

  SAVEPOINT add_coupon;                          -- checkpoint
  UPDATE orders SET total = total - 20 WHERE id = 10;   -- apply a coupon
  -- ...suppose we discover the coupon is invalid...
  ROLLBACK TO SAVEPOINT add_coupon;              -- undo ONLY the coupon; the order INSERT stays

  RELEASE SAVEPOINT add_coupon;                  -- optional: discard the savepoint
COMMIT;                                          -- the order (without coupon) is committed
```

> **Gotcha — in Postgres, an error aborts the *entire* transaction.** After any statement errors, the transaction enters a failed state and rejects everything until you `ROLLBACK` (or `ROLLBACK TO SAVEPOINT`). This is why ORMs/drivers wrap risky steps in savepoints — it lets them recover from a single failed statement without losing the whole unit. (MySQL is more lenient, but don't rely on that.)

---

## IV. CONCURRENCY ANOMALIES — WHAT GOES WRONG WITHOUT ISOLATION

When transactions run concurrently, their reads and writes interleave. Four classic anomalies result. Each is worked below as a timeline of two transactions, **T1** and **T2**.

### 1. Dirty Read — reading uncommitted data

T1 reads a value that T2 wrote but **hasn't committed** — and T2 might still roll back, making what T1 read *never have existed*.

```
T1                                  T2
                                    BEGIN
                                    UPDATE accounts SET balance=500 WHERE id='alice'  (was 100)
BEGIN
SELECT balance FROM accounts
   WHERE id='alice'  → 500  ← DIRTY: reads uncommitted 500
                                    ROLLBACK   ← balance is back to 100; the 500 never existed!
-- T1 made a decision based on a value that was rolled away. Corruption.
```

### 2. Non-Repeatable Read — same row, different value within one transaction

T1 reads a row twice; between the reads, T2 **commits an update**, so T1 sees two different values for the *same row* — its own view is inconsistent.

```
T1                                       T2
BEGIN
SELECT balance WHERE id='alice' → 100
                                         BEGIN
                                         UPDATE accounts SET balance=300 WHERE id='alice'
                                         COMMIT
SELECT balance WHERE id='alice' → 300   ← NON-REPEATABLE: same query, different answer
COMMIT
```

### 3. Phantom Read — same query, different *set of rows*

T1 runs a query returning a set of rows; T2 **inserts a new row** that matches the query's `WHERE`; T1 re-runs the query and a "phantom" row appears that wasn't there before.

```
T1                                          T2
BEGIN
SELECT COUNT(*) FROM orders
   WHERE total > 100   → 5
                                            BEGIN
                                            INSERT INTO orders (total) VALUES (250)
                                            COMMIT
SELECT COUNT(*) FROM orders
   WHERE total > 100   → 6   ← PHANTOM: a new row appeared in the result set
COMMIT
```

> **Non-repeatable vs phantom:** non-repeatable read is about an **existing row changing**; phantom read is about **new rows appearing/disappearing** in a range query. Different fixes (row locks vs range/predicate locks), so they're tracked separately.

### 4. Lost Update — two writers clobber each other

Two transactions read the same value, each computes a new value from it, and both write — the second write **overwrites** the first, so one update is silently lost.

```
T1                                       T2
BEGIN                                    BEGIN
SELECT balance → 100                     SELECT balance → 100
balance = 100 + 50 = 150                 balance = 100 + 30 = 130
UPDATE balance = 150                     
COMMIT                                   UPDATE balance = 130   ← clobbers T1's +50
                                         COMMIT
-- Final balance: 130. The +50 deposit VANISHED. Should be 180.
```

> Lost update is the most common real-world bug in naive "read-modify-write" application code. §VII (locking) and §VIII (optimistic concurrency) are the two cures.

---

## V. ISOLATION LEVELS — THE SPECTRUM

The SQL standard defines four **isolation levels**. Higher levels prevent more anomalies but reduce concurrency (more blocking/aborts). You trade correctness for throughput — deliberately.

| Isolation level | Dirty read | Non-repeatable read | Phantom read | Notes |
|-----------------|:---------:|:-------------------:|:------------:|-------|
| **READ UNCOMMITTED** | ⚠️ possible | ⚠️ possible | ⚠️ possible | Weakest; rarely useful |
| **READ COMMITTED** | ✅ prevented | ⚠️ possible | ⚠️ possible | **Postgres/Oracle default** |
| **REPEATABLE READ** | ✅ prevented | ✅ prevented | ⚠️ possible* | **MySQL/InnoDB default** |
| **SERIALIZABLE** | ✅ prevented | ✅ prevented | ✅ prevented | Strongest; as if transactions ran one at a time |

> *\* Per the SQL standard, REPEATABLE READ allows phantoms. In practice, **Postgres's REPEATABLE READ (a snapshot) also prevents phantoms**, and **InnoDB's REPEATABLE READ prevents them via next-key locks**. The standard is a floor, not a ceiling — real databases often exceed it.*

```
weaker ◄──────────────────────────────────────────────► stronger
READ UNCOMMITTED → READ COMMITTED → REPEATABLE READ → SERIALIZABLE
more concurrency, more anomalies      fewer anomalies, more blocking/aborts
```

### Setting the isolation level

```sql
-- Per transaction (the common way):
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  -- ... statements ...
COMMIT;

-- Postgres alternative inside a transaction:
BEGIN;
  SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
  -- ...
COMMIT;

-- Session-wide default (affects subsequent transactions):
SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

> **Gotcha — SERIALIZABLE doesn't mean "no concurrency," it means transactions can ABORT.** Postgres uses **Serializable Snapshot Isolation (SSI)**: it lets transactions run concurrently but aborts one with a `serialization_failure` (SQLSTATE `40001`) if their interleaving couldn't have happened serially. **Your application must catch that error and retry the transaction.** SERIALIZABLE pushes the cost from blocking to retries — design for it.

> **Gotcha — READ COMMITTED is the default and it allows lost updates.** Most apps run at READ COMMITTED without realizing non-repeatable reads, phantoms, *and* lost updates are all possible. If correctness depends on read-then-write (inventory, balances, counters), you must add explicit locking (§VII) or optimistic checks (§VIII) — the default level won't save you.

---

## VI. LOCKING — SHARED, EXCLUSIVE, ROW, TABLE

Databases enforce isolation partly with **locks**. Understanding them explains *why* a transaction is blocking or deadlocking.

### Shared (S) vs Exclusive (X) locks

- **Shared lock (S / read lock)** — many transactions can hold it simultaneously. Used for reads. Compatible with other shared locks.
- **Exclusive lock (X / write lock)** — only one transaction can hold it; blocks all other S and X locks on that resource. Used for writes.

| | Holder wants **S** | Holder wants **X** |
|---|:---:|:---:|
| Existing **S** lock | ✅ compatible | ❌ blocks |
| Existing **X** lock | ❌ blocks | ❌ blocks |

> "Many readers OR one writer." Reads share; writes are exclusive.

### Row locks vs table locks

- **Row-level lock** — locks only the affected rows. High concurrency; other rows stay free. This is the norm for `UPDATE`/`DELETE`.
- **Table-level lock** — locks the whole table. Low concurrency; used by DDL (`ALTER TABLE`), `LOCK TABLE`, and some bulk operations.

> **Prefer row locks.** Table locks serialize *everything* on the table. A migration that takes a table lock during peak traffic is a classic outage cause.

### Explicit row locking: `FOR UPDATE` / `FOR SHARE`

To prevent **lost updates**, lock the rows you intend to modify *at read time* so no one else can change them until you commit. This is **pessimistic locking** (§VIII).

```sql
BEGIN;
  -- Lock Alice's row exclusively; any other tx doing FOR UPDATE on it now WAITS:
  SELECT balance FROM accounts WHERE id = 'alice' FOR UPDATE;   -- → 100
  -- Safe read-modify-write: no one else can touch this row until we COMMIT
  UPDATE accounts SET balance = 100 + 50 WHERE id = 'alice';
COMMIT;                                                          -- lock released
```

```sql
-- FOR SHARE: lock for reading — others can also read (share) but NOT update until you commit.
SELECT * FROM products WHERE id = 7 FOR SHARE;

-- Don't want to wait? Fail fast or skip locked rows:
SELECT * FROM jobs WHERE status='pending' FOR UPDATE SKIP LOCKED LIMIT 1;  -- queue pattern
SELECT * FROM accounts WHERE id='alice' FOR UPDATE NOWAIT;                 -- error if locked
```

> **`SKIP LOCKED` is the idiomatic job-queue pattern**: many workers each grab a different pending row without blocking each other — the locked rows are simply skipped.

---

## VII. OPTIMISTIC vs PESSIMISTIC CONCURRENCY CONTROL

Two philosophies for handling the lost-update problem.

### Pessimistic — "assume conflict, lock first"

Lock the row before modifying it (`SELECT ... FOR UPDATE`, §VI). Other writers **wait**. Correct and simple, but holding locks reduces concurrency and risks deadlocks. Best when conflicts are **frequent** or contention is high.

### Optimistic — "assume no conflict, verify at write time"

Don't lock. Read a **version** (or timestamp) with the row. On write, check the version is unchanged; if someone else changed it, your update affects **0 rows** — detect that and retry. Best when conflicts are **rare** (most reads don't collide), avoiding lock overhead entirely.

```sql
-- Schema: accounts(id, balance, version INT)

-- 1. Read the row WITH its version (no lock):
SELECT balance, version FROM accounts WHERE id = 'alice';   -- → balance=100, version=7

-- 2. Compute the new value in app code: 100 + 50 = 150

-- 3. Write ONLY if the version is still 7, and bump it:
UPDATE accounts
   SET balance = 150, version = version + 1
 WHERE id = 'alice' AND version = 7;        -- ← the optimistic check

-- 4. Inspect rows affected:
--    1 row updated → success.
--    0 rows updated → someone else committed first (version moved). RETRY from step 1.
```

```javascript
// Application-side optimistic retry loop (Node-style pseudocode)
for (let attempt = 0; attempt < 3; attempt++) {
  const { balance, version } = await read(id);
  const result = await db.query(
    "UPDATE accounts SET balance=$1, version=version+1 WHERE id=$2 AND version=$3",
    [balance + 50, id, version]
  );
  if (result.rowCount === 1) return;     // success
  // else: conflict — loop and try again with the fresh version
}
throw new Error("too much contention");
```

| | **Pessimistic** | **Optimistic** |
|---|-----------------|----------------|
| Strategy | Lock before write (`FOR UPDATE`) | Check version at write; retry on conflict |
| Best when | Conflicts frequent / high contention | Conflicts rare |
| Cost | Lock waits, deadlock risk | Wasted work + retries on conflict |
| Concurrency | Lower (writers serialize) | Higher (no locks held) |
| Where it lives | Database locks | A `version` column + app retry logic |

> ORMs lean on this: Hibernate/JPA's `@Version`, Django's `select_for_update`, Prisma's optimistic concurrency — all implement one of these two patterns. Knowing the raw mechanics tells you which your framework is doing and why a write occasionally "fails."

---

## VIII. DEADLOCKS

A **deadlock** is a cycle: T1 holds lock A and wants lock B; T2 holds lock B and wants lock A. Neither can proceed; both wait forever. The database **detects the cycle and aborts one victim** (rolling it back) so the other can continue.

### A worked deadlock

```
T1                                       T2
BEGIN                                    BEGIN
UPDATE accounts WHERE id='alice'         UPDATE accounts WHERE id='bob'
  → locks Alice (X)                        → locks Bob (X)
UPDATE accounts WHERE id='bob'           UPDATE accounts WHERE id='alice'
  → wants Bob's lock... WAITS for T2       → wants Alice's lock... WAITS for T1
                  ── DEADLOCK ──
-- The DB detects the cycle and aborts one (e.g. T2) with:
--   ERROR: deadlock detected (SQLSTATE 40P01)
-- T1 then proceeds; the application RETRIES T2.
```

### Prevention

1. **Consistent lock ordering — the #1 cure.** If every transaction always locks rows in the *same order* (e.g. always the lower account id first), a cycle is impossible. The deadlock above happens *only* because T1 locks Alice→Bob and T2 locks Bob→Alice.

```sql
-- ✅ Always lock accounts in a deterministic order (e.g. by id ascending):
BEGIN;
  SELECT * FROM accounts WHERE id IN ('alice','bob') ORDER BY id FOR UPDATE;  -- both, in order
  UPDATE accounts SET balance = balance - 100 WHERE id = 'alice';
  UPDATE accounts SET balance = balance + 100 WHERE id = 'bob';
COMMIT;
```

2. **Keep transactions short.** The longer locks are held, the wider the window for a cycle. Do computation *before* `BEGIN`; don't make network/API calls while holding locks.
3. **Retry on deadlock.** Deadlocks are normal under load — catch SQLSTATE `40P01` (deadlock) / `40001` (serialization failure) and retry the whole transaction with a little backoff.
4. **Lower the isolation level if correctness allows**, or use `FOR UPDATE` to take locks up front in one statement instead of acquiring them piecemeal.

> **Gotcha — deadlocks are a *when*, not an *if*, at scale.** You cannot eliminate them entirely in a busy system. Mature applications **expect** deadlock/serialization errors and wrap transactions in a retry loop. A deadlock is a recoverable event, not a crash — treat it as one.

---

## IX. MVCC — HOW POSTGRES AVOIDS READ LOCKS

**Multi-Version Concurrency Control (MVCC)** is the reason Postgres (and Oracle, and InnoDB) can let readers and writers run concurrently **without readers blocking writers or vice versa**. The trick: instead of overwriting a row in place, an `UPDATE` writes a **new version** of the row and keeps the old one around. Each transaction sees a **snapshot** — the set of row versions that were committed as of when it started.

```
Row "alice", balance updates over time create versions:
  v1 (balance=100, committed at txid 50)   ← a transaction that started at txid 55 sees THIS
  v2 (balance=150, committed at txid 60)   ← a transaction that started at txid 65 sees THIS
Readers never wait: each just reads the version valid for its snapshot.
```

The famous slogan: **"readers don't block writers, and writers don't block readers."** A `SELECT` reads the appropriate old version while an `UPDATE` writes a new one — no lock contention between them. (Two *writers* to the same row still conflict — one waits.)

> **Gotcha — MVCC leaves dead row versions behind ("bloat").** Old versions that no transaction can see anymore are dead tuples; they consume space until **`VACUUM`** reclaims them (file 06). On update/delete-heavy tables, autovacuum must keep up or the table and its indexes bloat, slowing everything. This is the cost MVCC pays for lock-free reads.

> **How isolation maps to MVCC:** READ COMMITTED takes a fresh snapshot at the start of *each statement*; REPEATABLE READ takes one snapshot at the start of the *transaction* (so all reads are consistent — that's how it prevents non-repeatable reads and, in Postgres, phantoms). Same mechanism, different snapshot timing.

---

## X. TRANSACTIONS FROM APPLICATION CODE

The database verbs are only half the story — you must drive them correctly from code, with proper commit/rollback and resource cleanup.

### Node.js with `pg` — a client from the pool, try/commit/rollback

```javascript
// File: transfer.js — money transfer with a real transaction
const { Pool } = require("pg");
const pool = new Pool();   // connection pool (file 08)

async function transfer(fromId, toId, amount) {
  const client = await pool.connect();   // a SINGLE connection — a transaction lives on ONE connection
  try {
    await client.query("BEGIN");

    // Lock both rows in a consistent order to avoid deadlocks (§VIII):
    const ids = [fromId, toId].sort();
    await client.query("SELECT id FROM accounts WHERE id = ANY($1) ORDER BY id FOR UPDATE", [ids]);

    const { rows } = await client.query("SELECT balance FROM accounts WHERE id=$1", [fromId]);
    if (rows[0].balance < amount) throw new Error("insufficient funds");   // triggers rollback

    await client.query("UPDATE accounts SET balance = balance - $1 WHERE id=$2", [amount, fromId]);
    await client.query("UPDATE accounts SET balance = balance + $1 WHERE id=$2", [amount, toId]);

    await client.query("COMMIT");        // both updates permanent, together
  } catch (err) {
    await client.query("ROLLBACK");      // ANY failure → undo everything
    throw err;
  } finally {
    client.release();                    // ALWAYS return the connection to the pool
  }
}
```

> **Gotcha — a transaction must use ONE connection.** If you run `BEGIN` on one pooled connection and the `UPDATE` on another (e.g. by calling `pool.query` instead of `client.query`), they're in *different* transactions and your `BEGIN`/`COMMIT` won't wrap the work. Always `pool.connect()` a single client, run every statement on it, and `release()` it in `finally`. Forgetting `release()` leaks connections until the pool is exhausted and the app hangs.

### Java with JDBC — disable autocommit, commit/rollback, close

```java
// JDBC: the equivalent pattern. try-with-resources guarantees the connection closes.
try (Connection conn = dataSource.getConnection()) {
    conn.setAutoCommit(false);                 // start a transaction (autocommit is on by default!)
    try (PreparedStatement debit  = conn.prepareStatement(
            "UPDATE accounts SET balance = balance - ? WHERE id = ?");
         PreparedStatement credit = conn.prepareStatement(
            "UPDATE accounts SET balance = balance + ? WHERE id = ?")) {

        debit.setBigDecimal(1, amount); debit.setString(2, fromId); debit.executeUpdate();
        credit.setBigDecimal(1, amount); credit.setString(2, toId); credit.executeUpdate();

        conn.commit();                          // both permanent, together
    } catch (SQLException e) {
        conn.rollback();                        // undo everything on failure
        throw e;
    }
}
```

> **Gotcha — JDBC defaults to autocommit ON.** Every statement commits immediately unless you call `setAutoCommit(false)`. Forgetting this means your "transaction" is really N independent commits — no atomicity. (In Spring, `@Transactional` handles all of this for you, but the underlying mechanism is exactly the above.) Parameterized queries (`?`) here also prevent SQL injection — covered deeply in file 08.

---

## XI. COMMON PITFALLS

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Multi-step writes with no transaction | Partial updates corrupt data on crash | Wrap in `BEGIN`/`COMMIT` |
| Read-modify-write at READ COMMITTED | Lost updates (vanishing deposits) | `FOR UPDATE` lock or optimistic `version` check |
| Assuming SERIALIZABLE never aborts | Random `40001` errors in prod | Catch serialization failures and **retry** |
| Inconsistent lock ordering | Deadlocks under load | Lock rows in a deterministic order |
| Long transactions / work while locked | Lock waits, deadlocks, bloat | Keep tx short; compute before `BEGIN`; no I/O while locked |
| No deadlock retry logic | Transactions fail intermittently | Retry on `40P01`/`40001` with backoff |
| Transaction split across pooled connections | `BEGIN`/`COMMIT` don't wrap the work | One `client` per transaction; run all on it |
| Forgetting `client.release()` / `conn.close()` | Pool exhausted, app hangs | Release/close in `finally` (try-with-resources) |
| JDBC autocommit left on | No atomicity; each statement commits | `setAutoCommit(false)` |
| Ignoring an error mid-transaction (Postgres) | "current transaction is aborted" on every next stmt | `ROLLBACK` (or to a `SAVEPOINT`) to recover |
| Relying on the standard for phantom behavior | Surprises across databases | Test your DB; Postgres RR ≠ InnoDB RR ≠ standard |
| Autovacuum can't keep up (MVCC bloat) | Table/index bloat, slowdowns | Tune autovacuum; `VACUUM`; avoid huge long-running txns |

---

## 🧠 KEY TAKEAWAYS

- A **transaction** groups statements into an all-or-nothing unit (`BEGIN`/`COMMIT`/`ROLLBACK`); **savepoints** allow partial rollback within one.
- **ACID**: **Atomicity** (all-or-nothing via undo log), **Consistency** (constraints hold), **Isolation** (concurrent txns don't corrupt each other), **Durability** (committed survives crashes via the WAL).
- Without isolation you get four anomalies: **dirty read** (uncommitted), **non-repeatable read** (existing row changed), **phantom read** (new rows appear), and **lost update** (writers clobber each other).
- The four **isolation levels** trade concurrency for correctness: READ UNCOMMITTED → READ COMMITTED (Postgres default) → REPEATABLE READ (InnoDB default) → SERIALIZABLE. Stronger = fewer anomalies but more blocking/aborts.
- **SERIALIZABLE can abort transactions** (`40001`) — your app must **retry**. READ COMMITTED (the common default) still allows **lost updates** — guard read-then-write logic explicitly.
- Use **`SELECT ... FOR UPDATE`** (pessimistic) when conflicts are frequent; use a **`version` column + retry** (optimistic) when they're rare.
- **Deadlocks** come from inconsistent lock order — fix with **consistent ordering**, short transactions, and **retry loops**; they're a normal event at scale, not a crash.
- **MVCC** gives Postgres lock-free reads ("readers don't block writers") by keeping multiple row versions; the cost is **bloat** that `VACUUM` must reclaim.
- From code, a transaction lives on **one connection** — `BEGIN`, run every statement on that client, `COMMIT`/`ROLLBACK`, and **release/close in `finally`**. JDBC needs `setAutoCommit(false)`.

---

**Prev:** [`06-Indexing-And-Query-Optimization.md`](./06-Indexing-And-Query-Optimization.md) · **Next:** [`08-Advanced-SQL-And-Production.md`](./08-Advanced-SQL-And-Production.md) · **Index:** [`00-Index.md`](./00-Index.md)
