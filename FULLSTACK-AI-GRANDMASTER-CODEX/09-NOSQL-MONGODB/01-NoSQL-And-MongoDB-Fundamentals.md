# 🍃 01 — NoSQL & MongoDB Fundamentals

> *"A document database doesn't replace tables — it admits that the world is shaped like nested objects, and stops pretending otherwise."*

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-CRUD-Operations-And-Query-Operators.md`](./02-CRUD-Operations-And-Query-Operators.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. WHAT "NOSQL" ACTUALLY MEANS

**NoSQL** is a family of databases that stepped away from the relational model — fixed tables, fixed schemas, joins, SQL — to handle data and workloads that relational systems struggled with at the scale of the 2000s web (Google, Amazon, Facebook). The name is misleading: it's better read as "**N**ot **O**nly **SQL**." Many NoSQL systems even speak SQL-flavored query languages now. What actually unites them is a different set of *tradeoffs*:

- Flexible or schema-less data shapes — store irregular, evolving records without migrations.
- Horizontal scale-out — designed from day one to spread across many machines.
- Looser consistency where needed — to keep writes fast and clusters available during partitions.
- Specialized data models — documents, key-value pairs, wide columns, or graphs — instead of forcing every problem into rows-and-columns.

A database is "NoSQL" because it makes a *different deal* with you than Postgres or MySQL, not because it forbids tables.

> **Gotcha — "schemaless" is a marketing word.** Your data has a schema; the database just doesn't enforce it for you. Without discipline (Mongoose, JSON Schema validators, code review) "schemaless" becomes "every document is slightly different and queries break in odd ways." File 05 makes this concrete.

---

## II. THE FOUR FAMILIES OF NOSQL

The NoSQL world is not one thing. There are four major families, each with a *core data model* and a *workload* it was designed for.

### 1. Document databases — MongoDB, Couchbase, Firestore

The unit of storage is a **document** — a self-contained, nested record (think JSON / BSON). A collection of documents replaces a table of rows.

```js
// One document — a user with embedded address and tags array
{
  _id: ObjectId("65f9ab..."),
  name: "Ada Lovelace",
  email: "ada@analytical.engine",
  address: { city: "London", country: "UK" },   // nested object
  tags: ["mathematician", "first-programmer"],   // array
  createdAt: ISODate("2024-03-19T12:00:00Z")
}
```

**Strengths:** matches how you already model data in code (objects), great for content/catalogs/user profiles, schema can evolve per document, rich query language. **Weaknesses:** joins exist (`$lookup`) but aren't as cheap as in SQL; expensive to maintain referential integrity manually.

### 2. Key-value stores — Redis, DynamoDB, Riak, Memcached

The simplest model: a giant distributed `Map<Key, Value>`. The value is opaque (a string, a binary blob, sometimes a structured value like a list/hash/set in Redis).

```bash
# Redis
SET user:42 "{\"name\":\"Ada\"}"
GET user:42
INCR page:home:visits
```

**Strengths:** O(1)-ish lookups, blazing-fast, trivial to scale, perfect for caches/session stores/feature flags/leaderboards/rate limiters. **Weaknesses:** no real querying — you can only ask "what's at this key?" Pattern-matching scans are slow.

### 3. Column-family / wide-column — Cassandra, HBase, Bigtable, ScyllaDB

Data is organized by **column families** rather than rows. Conceptually each row has a primary key and an arbitrarily wide set of columns (often sparse). Built for **massive write throughput** and **petabyte scale** across thousands of nodes.

```cql
-- Cassandra CQL — looks like SQL, behaves very differently
CREATE TABLE events_by_user (
  user_id uuid,
  occurred_at timestamp,
  type text,
  payload text,
  PRIMARY KEY (user_id, occurred_at)
) WITH CLUSTERING ORDER BY (occurred_at DESC);
```

**Strengths:** linearly scalable writes, time-series and event-log workloads. **Weaknesses:** queries must match how you partitioned the data — flexibility is low, modeling is upfront.

### 4. Graph databases — Neo4j, ArangoDB, Amazon Neptune, JanusGraph

The data model is **nodes and edges with properties**. Designed for *relationship-heavy* queries — "shortest path," "friends of friends," "who is two hops from this account through any payment."

```cypher
// Neo4j Cypher
MATCH (u:User {email:"ada@x.com"})-[:FRIEND*1..3]->(f:User)
RETURN DISTINCT f.name;
```

**Strengths:** path queries that would be horrific in SQL or Mongo — fraud rings, recommendation, knowledge graphs. **Weaknesses:** smaller ecosystem, harder operational story, not the right hammer for plain CRUD.

### Comparison at a glance

| Family | Example | Mental model | Sweet spot |
|--------|---------|--------------|-----------|
| Document | **MongoDB** | JSON-like docs in collections | Catalogs, content, user data, irregular structures |
| Key-value | Redis | Distributed `Map<K, V>` | Cache, sessions, counters, real-time |
| Column-family | Cassandra | Sparse "row → many columns" by partition key | Write-heavy, time-series, very large scale |
| Graph | Neo4j | Nodes + typed edges with properties | Relationship traversal, recommendation, fraud |

Real systems often combine multiple — Mongo for the source of truth, Redis as a cache, an analytics column store for warehousing.

---

## III. NOSQL VS SQL — WHEN TO PICK WHICH

You'll meet pundits who claim one is "modern" and the other "legacy." Both are wrong. They are tools with different strengths.

| Question | Lean **SQL** (Postgres, MySQL) | Lean **NoSQL** (Mongo, etc.) |
|----------|--------------------------------|------------------------------|
| Is the schema stable & relational? | ✅ | ❌ |
| Multi-row, multi-table transactions? | ✅ ACID by default | ⚠️ Possible (Mongo since 4.0) but not the default |
| Data shape is nested / irregular? | ❌ ugly to model | ✅ natural |
| Need full-power joins / set algebra? | ✅ | ⚠️ `$lookup` works, joins are expensive |
| Horizontal scale to PB / millions of ops/sec? | Possible (sharded Postgres, Vitess) but harder | ✅ first-class |
| Need flexible schema for fast iteration? | Migrations on every change | ✅ document evolves freely |
| Workload is graph traversal? | ❌ | ❌ — use a graph DB |
| Workload is "give me one thing by key, fast"? | OK | ✅ key-value wins |

**Rule of thumb:** when in doubt, default to Postgres. Reach for MongoDB when your data is genuinely document-shaped (catalogs, profiles, content, telemetry payloads) or when schema evolution is constant. Reach for Redis as a cache, never as a system of record. Reach for a graph DB only when graph traversal is the *primary* workload.

> **Polyglot persistence is normal.** A real backend often runs Postgres for transactional core data, Mongo for content, Redis for cache, and an analytics warehouse on top. Pick per workload.

---

## IV. THE CAP THEOREM — THE LAW THAT CREATED NOSQL

Eric Brewer's **CAP theorem** (proved by Gilbert & Lynch, 2002) says: in any distributed data system, when a **network partition** happens (some nodes can't talk to others), you must choose between:

- **C — Consistency:** every read sees the most recent write (linearizable).
- **A — Availability:** every request gets a non-error response.
- **P — Partition tolerance:** the system keeps working despite the split.

**You cannot have all three** during a partition. Since partitions are inevitable in any real distributed system (network blips, dead switches, AWS zone outages), the real choice is **C vs A** when one happens.

```
        C (consistency)
       /   \
      /     \
     /       \
    A---------P
   (availability)  (partition tolerance)
```

| System leans | Behavior during a partition | Example |
|--------------|-----------------------------|---------|
| **CP** | Refuse to serve writes on the split-off side until healed | MongoDB (default config), HBase, etcd, Zookeeper |
| **AP** | Keep accepting writes on both sides; reconcile later | Cassandra, DynamoDB (default), Couchbase |
| CA only | Only possible if you assume the network never partitions — i.e., a single node | A toy single-server DB |

> **Gotcha — "MongoDB is CP" is not the whole story.** With `writeConcern: "majority"` and `readConcern: "majority"` on a healthy replica set, MongoDB is strongly consistent. Configure it differently (read from secondaries with `readPreference: secondary`) and you trade away linearizability for latency. CAP is *configurable per query* in modern Mongo.

### PACELC — the follow-up

CAP only describes the partition case. **PACELC** (Daniel Abadi, 2010) extends it: *if* there's a Partition you trade A vs C; **E**lse, even when running normally, you trade **L**atency vs **C**onsistency. Reading from the nearest secondary is faster (low L) but might be slightly stale (low C). Reading with `majority` consistency is slower but always correct. Most NoSQL systems are honest PA/EL (give up consistency for both availability and latency). Mongo defaults closer to PC/EC (consistency-first).

---

## V. ACID VS BASE

The relational world's contract is **ACID**:

- **Atomicity** — all-or-nothing within a transaction.
- **Consistency** — the DB moves from one valid state to another (constraints, integrity).
- **Isolation** — concurrent transactions don't see each other's intermediate state.
- **Durability** — once committed, data survives crashes.

Many NoSQL systems chose to relax ACID to scale horizontally and stay available. Their contract is called **BASE**:

- **B**asically **A**vailable — system always responds, even if not with the latest data.
- **S**oft state — replicas may be temporarily inconsistent.
- **E**ventual consistency — given no new writes, replicas converge.

| Property | ACID (SQL) | BASE (NoSQL) |
|----------|------------|--------------|
| Consistency model | Strong, immediate | Eventual (typically) |
| Availability under partition | Lower | Higher |
| Throughput / scale | Bounded by single node coordination | Designed to scale out |
| Programming model | Transactions are easy | Idempotency, retries, conflict resolution on you |

> **MongoDB's modern stance.** Single-document operations have always been atomic. Since **MongoDB 4.0** you can run **multi-document ACID transactions** on a replica set; since **4.2** across sharded clusters. MongoDB is no longer "just BASE" — it's a hybrid that lets you choose. File 07 covers this.

---

## VI. MONGODB — THE 30,000-FOOT VIEW

MongoDB is the document database we'll use for the rest of this section. The core ideas you need before any query:

```
┌───────────────────────────────────────────────────────┐
│                MongoDB Server (mongod)                │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Database: "shop"                                │  │
│  │  ┌────────────────┐  ┌─────────────────────┐    │  │
│  │  │ Collection:    │  │ Collection:         │    │  │
│  │  │   "users"      │  │   "products"        │    │  │
│  │  │  Document      │  │  Document           │    │  │
│  │  │  Document      │  │  Document           │    │  │
│  │  │  …             │  │  …                  │    │  │
│  │  └────────────────┘  └─────────────────────┘    │  │
│  └─────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────┐  │
│  │ Database: "blog"                                │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

### Mapping from SQL

| SQL | MongoDB |
|-----|---------|
| Database | **Database** |
| Table | **Collection** |
| Row | **Document** |
| Column | **Field** |
| Primary key | **`_id`** field (auto `ObjectId` if you don't supply one) |
| `JOIN` | `$lookup` aggregation stage |
| Index | Index (same name) |
| `INSERT INTO ...` | `db.coll.insertOne(...)` |
| `SELECT * FROM ...` | `db.coll.find(...)` |
| `UPDATE ... SET ...` | `db.coll.updateOne(filter, { $set: ... })` |
| `DELETE FROM ...` | `db.coll.deleteOne(...)` |

### Server processes

- **`mongod`** — the database server itself. Listens on TCP `27017` by default.
- **`mongos`** — query router for sharded clusters (file 08). Looks the same to clients.
- **`mongosh`** — the modern interactive shell (replaced legacy `mongo`).
- **MongoDB Compass** — official GUI; visual schema, query plans, aggregation builder.

### Storage engine

The default storage engine is **WiredTiger**: B-tree indexes, document-level locking, snappy compression, MVCC for transactions, journaling for durability. You rarely touch it directly, but knowing it's a B-tree underneath explains why indexes look like SQL indexes (file 03).

---

## VII. BSON — THE BINARY DOCUMENT FORMAT

You write documents as JSON, but MongoDB stores **BSON** ("Binary JSON"): a binary encoding that's compact, ordered, traversable, and crucially adds **types JSON lacks** (dates, ObjectIds, decimals, binary blobs, regex, longs).

| BSON type | JS / mongosh literal | Notes |
|-----------|----------------------|-------|
| Double | `3.14` | 64-bit IEEE-754 |
| String | `"hello"` | UTF-8 |
| Object | `{ ... }` | Embedded document |
| Array | `[1, 2, 3]` | Indexed list |
| Binary | `BinData(0, "...")` | Raw bytes |
| ObjectId | `ObjectId("65f9...")` | 12-byte identifier |
| Boolean | `true` / `false` | |
| Date | `ISODate("2024-03-19T...")` or `new Date()` | Stored as ms since epoch |
| Null | `null` | Distinct from "field missing" |
| Regex | `/^abc/i` | Native regex value |
| Int32 | `NumberInt(42)` | 32-bit integer |
| Timestamp | `Timestamp(1, 1)` | Internal — used by oplog |
| Int64 | `NumberLong("9000000000")` | 64-bit integer |
| Decimal128 | `NumberDecimal("0.1")` | Exact decimal — use for **money** |
| MinKey / MaxKey | `MinKey()` / `MaxKey()` | Comparison sentinels |

> **Gotcha — the JSON Trap.** Plain JSON only knows strings, numbers, booleans, null, objects, arrays. When you `JSON.stringify` a Mongo document, `Date` becomes a string and `ObjectId` becomes `{ "$oid": "..." }` (in extended JSON). Drivers usually round-trip transparently — but a hand-written `JSON.parse` of an exported document will give you back strings, not real `Date`s. Use **EJSON** (Extended JSON) when serializing for tools.

### Why use Decimal128 for money

```js
// BAD — IEEE-754 floats can't represent 0.1 exactly
db.payments.insertOne({ amount: 0.1 + 0.2 });  // stores 0.30000000000000004

// GOOD — exact decimal arithmetic
db.payments.insertOne({ amount: NumberDecimal("0.30") });
```

---

## VIII. THE `_id` FIELD AND `ObjectId`

Every document **must** have a unique `_id` within its collection. If you don't supply one, MongoDB generates an **`ObjectId`** — a 12-byte value that is sortable, globally unique, and informative.

```
ObjectId("65f9abcd1234567890abcdef")
         └──┬───┘ └──┬─┘ └─┬─┘ └─┬───┘
       4-byte  5-byte  3-byte
       seconds random  counter
       (epoch) (per-process)
```

Practical consequences:

- **`ObjectId`s sort approximately by creation time** — newest documents have larger `_id`s. You can paginate "newest first" by sorting `_id` descending without a separate `createdAt` index.
- They're **96 bits**, not 128, but collision is astronomically unlikely in practice.
- They can be generated **client-side** before insert, which lets you build cross-collection references without a round-trip.

```js
// Mongosh / Node — extract creation time from an ObjectId
const id = ObjectId();
id.getTimestamp();   // ISODate("2024-03-19T12:00:00Z")
```

You can supply your own `_id` of any BSON type — UUIDs, slugs, integers — as long as it's unique:

```js
db.products.insertOne({ _id: "sku-1234", name: "Mechanical keyboard", price: 129 });
db.products.insertOne({ _id: "sku-1234", name: "Duplicate" });
// → E11000 duplicate key error on _id
```

> **Gotcha — `_id` is immutable.** You cannot change a document's `_id` once written. To "rename" it, copy the doc with a new `_id` and delete the old one (do this in a transaction if it matters).

---

## IX. CONNECTION STRINGS

The way every client (mongosh, Node driver, Mongoose, Compass) finds the server. Two flavors:

### Standard form

```
mongodb://[username:password@]host1[:port1][,host2[:port2]...]/[database][?option=value&...]
```

```bash
# Local single-node
mongodb://localhost:27017

# With auth and a default database
mongodb://alice:s3cret@db.example.com:27017/shop?authSource=admin

# Replica set — list seed members, give the set a name
mongodb://node1:27017,node2:27017,node3:27017/shop?replicaSet=rs0
```

### SRV form (Atlas, DNS-driven)

```bash
mongodb+srv://alice:s3cret@cluster0.xxxxx.mongodb.net/shop?retryWrites=true&w=majority
```

The `+srv` form looks up DNS SRV records to discover the cluster topology and pulls TLS settings automatically — that's how Atlas hides "where is my replica set" from you.

### The options that matter

| Option | What it does |
|--------|--------------|
| `retryWrites=true` | Driver retries one-time-failed writes (default in modern drivers) |
| `w=majority` | Write isn't acknowledged until a majority of replica members confirm |
| `readPreference=primary` | Where reads go — `primary`, `primaryPreferred`, `secondary`, `secondaryPreferred`, `nearest` |
| `tls=true` | Use TLS for transport (Atlas always; on-prem when configured) |
| `replicaSet=rs0` | Name of the replica set; required for the standard form on a replica set |
| `authSource=admin` | Which DB holds the user document for auth |
| `appName=my-api` | Tags connections in server logs — invaluable for ops |
| `maxPoolSize=10` | Max sockets the driver will open (file 06, 08) |

> **Gotcha — passwords in URIs need URL-encoding.** A password of `p@ss/word` must become `p%40ss%2Fword`. The driver won't always tell you why auth fails; it may just say "Authentication failed."

---

## X. MONGOSH — THE SHELL YOU'LL LIVE IN

`mongosh` is a JavaScript REPL with a database client glued on. Anything that runs in Node-ish JS (`for`, `await`, arrow functions, `const`) runs here.

```bash
mongosh "mongodb://localhost:27017"
```

```js
// Inside the shell:

show dbs                                   // list databases on this server
use codex                                  // switch to (or create) "codex"
db                                         // 'codex' — the current DB
db.getName()                               // 'codex'

show collections                           // list collections in current DB
db.users.insertOne({ name: "Ada", age: 36 })
db.users.find()                            // query — returns a cursor
db.users.find().pretty()                   // formatted print
db.users.countDocuments()                  // 1

// Cursors — find() is lazy until you iterate
const cur = db.users.find({ age: { $gte: 18 } });
cur.hasNext();                             // true
cur.next();                                // { _id: ..., name: 'Ada', age: 36 }

// You can run normal JS
for (let i = 0; i < 5; i++) {
  db.users.insertOne({ name: "User" + i, age: 20 + i });
}

// Multi-line scripts work
const adults = db.users.find({ age: { $gte: 21 } }).toArray();
console.log(`Found ${adults.length} adults`);
```

### Useful one-liners

```js
db.dropDatabase()                          // nuke current DB — careful
db.users.drop()                            // drop a single collection
db.users.stats()                           // size, count, avg doc size, indexes
db.serverStatus().connections              // active server connections
db.runCommand({ ping: 1 })                 // health check
db.getCollectionNames()                    // array of collections
load("seed.js")                            // run a JS file inside the shell
```

### `mongoimport` / `mongoexport` / `mongodump` / `mongorestore`

The CLI tools that get data in and out.

```bash
# JSON / CSV import (one document per line for JSON)
mongoimport --uri "mongodb://localhost:27017" -d codex -c users --file users.json --jsonArray

# Export as JSON
mongoexport --uri "mongodb://localhost:27017" -d codex -c users --out users.json --jsonArray

# Binary backup (BSON) — preserves all types, unlike mongoexport
mongodump --uri "mongodb://localhost:27017" --db codex --out ./backup
mongorestore --uri "mongodb://localhost:27017" --db codex ./backup/codex
```

> **Gotcha — `mongoexport` is lossy.** It writes JSON, which loses BSON types unless you pass `--jsonFormat=canonical` for Extended JSON. For real backups, **always use `mongodump`** — it writes BSON and round-trips every type.

---

## XI. INSERTING AND READING — A FIRST TASTE

A complete first dialogue with MongoDB:

```js
// 1. Switch to a fresh DB
use codex

// 2. Insert a few users — collection is created on first write
db.users.insertMany([
  { name: "Ada Lovelace",   email: "ada@x.com",   age: 36, tags: ["math", "first-programmer"] },
  { name: "Grace Hopper",   email: "grace@x.com", age: 85, tags: ["compiler", "navy"] },
  { name: "Linus Torvalds", email: "linus@x.com", age: 54, tags: ["kernel", "git"] }
])
// → { acknowledged: true, insertedIds: { '0': ObjectId(...), '1': ..., '2': ... } }

// 3. Read everything
db.users.find()

// 4. Read one — first match
db.users.findOne({ name: "Ada Lovelace" })

// 5. Filtered query
db.users.find({ age: { $gte: 50 } })             // operators come in file 02

// 6. Projection — return only some fields
db.users.find({}, { name: 1, email: 1, _id: 0 }) // only name, email; hide _id

// 7. Sort, limit, skip
db.users.find().sort({ age: -1 }).limit(2)       // 2 oldest

// 8. Update one
db.users.updateOne({ name: "Ada Lovelace" }, { $set: { age: 37 } })

// 9. Delete one
db.users.deleteOne({ name: "Linus Torvalds" })

// 10. Drop the whole collection when you're done playing
db.users.drop()
```

The next file (02) takes every operator and option from this dialogue and goes deep. This file's job was to make sure you know *what* is happening; the next one teaches you *how* to wield it.

---

## XII. FROM SHELL TO NODE — A FIRST DRIVER USAGE

You will rarely run production queries from `mongosh`. Real apps use the driver. The native MongoDB driver and Mongoose (file 06) speak the same protocol the shell does.

```bash
npm install mongodb dotenv
```

```js
// connect.js — native driver, ESM
import "dotenv/config";
import { MongoClient } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI);

try {
  await client.connect();
  const db = client.db("codex");
  const users = db.collection("users");

  // Same operations as mongosh, just method calls on the driver
  const id = (await users.insertOne({ name: "Ada", email: "ada@x.com" })).insertedId;
  const doc = await users.findOne({ _id: id });
  console.log("Inserted then read:", doc);
} finally {
  await client.close();
}
```

```bash
node connect.js
# Inserted then read: { _id: new ObjectId("..."), name: 'Ada', email: 'ada@x.com' }
```

That's the whole shape of the integration: the driver returns `Promise`s, results are plain JS objects (with real `ObjectId` and `Date` instances), and connections must be closed (or pooled — file 06 covers Mongoose's pool handling).

---

## XIII. DOCUMENT SIZE LIMIT AND OTHER HARD LIMITS

The single most important *constant* in MongoDB:

- **A single document cannot exceed 16 MB.** Period. Try to insert a larger one and you get an error.
- Maximum nesting depth: **100 levels**.
- Maximum index name length, field name length, and a few others — see <https://www.mongodb.com/docs/manual/reference/limits/>.

The 16 MB limit forces good design: if a document is *approaching* even 1 MB, you almost certainly want references or buckets (file 05) instead of unbounded embedding. Storing arbitrary user uploads (videos, PDFs) in documents is wrong; for those use **GridFS** (which splits big files across chunks across two collections) or, better, an object store like S3 with the URL embedded in your document.

---

## XIV. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Treating "schemaless" as "no schema" | Inconsistent docs, queries that miss data | Mongoose schemas (file 06) or JSON Schema validators (file 05) |
| Using `double` for money | Off-by-fractions errors | `Decimal128` / `NumberDecimal` |
| Hand-rolling JSON for export | Lost dates / ObjectIds | Use `mongodump`/`mongorestore` for backups |
| Putting password into URI un-encoded | `Authentication failed` with no clue why | URL-encode special chars in user/password |
| Letting documents grow without bound | Updates slow as docs move on disk | Bucket pattern (file 05) or capped collections |
| Ignoring 16 MB limit | `BSONObjectTooLarge` | Reference, GridFS, or S3 for binaries |
| Reading from secondaries by default | Stale reads in production | `readPreference=primary` unless you *want* eventual reads |
| Treating CAP as "MongoDB is just CP" | Surprised by stale reads with `secondary` preference | Pick read/write concerns per query; understand the spectrum |
| `mongoexport` for backups | Type info silently lost | Use `mongodump`/`mongorestore` |

---

## 🧠 KEY TAKEAWAYS

- "**NoSQL**" is an umbrella for four families — **document, key-value, column-family, graph** — each with a *different* tradeoff, not a single replacement for SQL.
- The **CAP theorem** says under a network partition you must pick **C** or **A**; **PACELC** adds that even when healthy, you trade **L**atency vs **C**onsistency. NoSQL exists because many systems chose A/L over C.
- **ACID** vs **BASE** is the application-level shape of those tradeoffs. **MongoDB 4.0+** offers ACID multi-document transactions, blurring the old line.
- MongoDB stores **documents** in **collections** in **databases** in **`mongod`**. The on-disk format is **BSON** — JSON plus dates, ObjectIds, Decimal128, and friends.
- Every document has an **`_id`**; if you don't supply one, you get an **ObjectId** that's globally unique and roughly time-sortable.
- A **connection string** (`mongodb://` or `mongodb+srv://`) carries auth, hosts, replica-set name, read/write concerns, and TLS — most production bugs trace back to its options.
- Your interactive partner is **`mongosh`** — a JS REPL. Your production partner is the **driver** (or Mongoose). Both speak the same wire protocol and the same query language you're about to learn.
- Hard limits to remember: **16 MB per document, 100 levels of nesting**. Design for them.

---

**Prev:** [`00-Index.md`](./00-Index.md) · **Next:** [`02-CRUD-Operations-And-Query-Operators.md`](./02-CRUD-Operations-And-Query-Operators.md) · **Index:** [`00-Index.md`](./00-Index.md)
