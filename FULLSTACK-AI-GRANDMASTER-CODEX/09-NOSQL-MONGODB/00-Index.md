# 🍃 NoSQL & MongoDB

> *"Tables forced the world into rows. The world is not rows. It's nested, irregular, and changing under your feet. The document model said: stop fighting reality, and store it the way it shows up."*

> **Section 09 of the** [`FULLSTACK-AI-GRANDMASTER-CODEX`](../README.md). This module takes you from "what even is NoSQL" to a sharded, replicated, secured MongoDB cluster you can model, query, aggregate, and run in production with Mongoose on top.

---

## 🎯 WHAT YOU WILL OWN AFTER THIS SECTION

- The **NoSQL landscape**: the four families (document, key-value, column-family, graph), what each is *for*, and the **CAP theorem** + **BASE vs ACID** tradeoffs that drove their existence.
- **MongoDB architecture** end to end: the `mongod` server, databases, collections, documents, **BSON** types, the magical `_id` / `ObjectId`, and connection strings.
- **CRUD** the way real engineers do it: `insertOne/Many`, `find` with the *full* query operator vocabulary (`$eq/$ne/$gt/$gte/$lt/$lte/$in/$nin/$exists/$type/$regex/$and/$or/$not/$nor/$expr`), update operators (`$set/$unset/$inc/$mul/$min/$max/$rename/$currentDate/$push/$pull/$pop/$addToSet/$pullAll`), `arrayFilters`, `findOneAndUpdate`, `replaceOne`, projection, sort/limit/skip.
- **Indexes**: single, compound (the **ESR rule**), multikey, text, 2dsphere geospatial, TTL, partial, sparse, unique, hashed — and how to read `explain()` output.
- The **aggregation pipeline**: every stage that matters (`$match/$project/$group/$sort/$limit/$skip/$lookup/$unwind/$facet/$bucket/$bucketAuto/$addFields/$replaceRoot/$count/$out/$merge/$graphLookup`) and the expression operators that go inside them.
- **Schema design patterns**: embedding vs referencing for *every* cardinality, plus the canonical patterns (versioning, computed, bucket, attribute, polymorphic, extended-reference, outlier, and the four tree patterns).
- **Mongoose**: schemas, models, validators, middleware, virtuals, populate, discriminators, plugins, transactions, the full CRUD service layer in Node + Express.
- **Production MongoDB**: multi-document **transactions**, **replica sets** (oplog, elections, read preferences, write concerns), **change streams**, **sharding** (shard key choice, chunks, mongos, balancer), **security** (auth, RBAC, TLS, encryption-at-rest), backups, monitoring, **MongoDB Atlas**.

---

## 📚 CONTENTS — LEARNING ORDER

> Read in order. Each file builds on the previous. ⭐ marks the highest-leverage files — do not skim them.

| # | File | What it covers | Priority |
|---|------|----------------|----------|
| 00 | [`00-Index.md`](./00-Index.md) | You are here · roadmap · setup | — |
| 01 | [`01-NoSQL-And-MongoDB-Fundamentals.md`](./01-NoSQL-And-MongoDB-Fundamentals.md) | What NoSQL is, the four families, CAP, BASE vs ACID, MongoDB architecture, BSON, `_id`/`ObjectId`, connection strings, mongosh basics | ⭐ |
| 02 | [`02-CRUD-Operations-And-Query-Operators.md`](./02-CRUD-Operations-And-Query-Operators.md) | Insert/find/update/delete with the **complete** operator vocabulary, projection, sort/limit/skip, `arrayFilters`, `findOneAndUpdate`, `replaceOne`, bulk writes | ⭐ |
| 03 | [`03-Indexing-And-Performance.md`](./03-Indexing-And-Performance.md) | Single, compound (ESR), multikey, text, geo, TTL, partial, unique, sparse, hashed indexes; `explain()`, covered queries, profiler, working set | ⭐ |
| 04 | [`04-Aggregation-Pipeline.md`](./04-Aggregation-Pipeline.md) | Pipeline model, every important stage and expression operator, `$lookup`/`$graphLookup`, `$facet`/`$bucket`, `$out`/`$merge`, optimization | ⭐ |
| 05 | [`05-Schema-Design-Patterns.md`](./05-Schema-Design-Patterns.md) | Embedding vs referencing for every cardinality, denormalization tradeoffs, schema versioning/computed/bucket/attribute/polymorphic patterns, the four tree patterns | ⭐ |
| 06 | [`06-Mongoose-And-Nodejs-Integration.md`](./06-Mongoose-And-Nodejs-Integration.md) | Mongoose schemas (every option), models, validators, middleware/hooks, virtuals, instance/static methods, populate, discriminators, plugins, full Express CRUD | ⭐ |
| 07 | [`07-Transactions-And-Replication.md`](./07-Transactions-And-Replication.md) | Multi-document ACID transactions (sessions, `withTransaction`, retry), replica sets, oplog, elections, read preferences, write concerns, change streams | ⭐ |
| 08 | [`08-Sharding-Security-And-Production.md`](./08-Sharding-Security-And-Production.md) | Sharding (shard key, hashed vs ranged, chunks, balancer, mongos), security (auth, RBAC, TLS, encryption-at-rest), backups, monitoring, Atlas, production checklist | ⭐ |

---

## 🗺️ COMPLETE NOSQL + MONGODB ROADMAP (coverage checklist)

> Roadmap.sh-style exhaustive checklist. **Reading only this codex covers all of it.** Each topic links to the file where it lives.

### A. NoSQL fundamentals & families
- [x] What "NoSQL" actually means (history, motivation) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **Document** databases (MongoDB, Couchbase, Firestore) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **Key-value** stores (Redis, DynamoDB, Riak) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **Column-family / wide-column** (Cassandra, HBase, Bigtable) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **Graph** databases (Neo4j, ArangoDB, Neptune) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] When to use NoSQL vs SQL — decision matrix → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **CAP theorem** (Consistency / Availability / Partition tolerance) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **PACELC** (the CAP follow-up) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **BASE** (Basically Available, Soft state, Eventual consistency) vs **ACID** → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] Eventual vs strong consistency → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md), [`07`](./07-Transactions-And-Replication.md)

### B. MongoDB architecture
- [x] What MongoDB is, history, philosophy → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] `mongod`, `mongos`, `mongosh`, MongoDB Compass → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md), [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Database → Collection → Document** hierarchy → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] **BSON** (Binary JSON), all BSON types → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] The **`_id`** field & **`ObjectId`** structure → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] Connection strings (`mongodb://`, `mongodb+srv://`, options) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md), [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] WiredTiger storage engine (overview) → [`03`](./03-Indexing-And-Performance.md), [`08`](./08-Sharding-Security-And-Production.md)
- [x] Document size limit (16 MB), nesting limit → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md), [`05`](./05-Schema-Design-Patterns.md)

### C. mongosh & shell basics
- [x] `mongosh` REPL, `show dbs`, `use`, `show collections` → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] Importing / exporting (`mongoimport`, `mongoexport`, `mongodump`, `mongorestore`) → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md), [`08`](./08-Sharding-Security-And-Production.md)
- [x] JSON vs Extended JSON → [`01`](./01-NoSQL-And-MongoDB-Fundamentals.md)
- [x] Cursors, iteration, batching → [`02`](./02-CRUD-Operations-And-Query-Operators.md)

### D. CRUD — Create / Read / Update / Delete
- [x] `insertOne`, `insertMany`, `ordered` flag → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] `find`, `findOne`, cursors, `toArray`, `forEach` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Comparison operators**: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Logical operators**: `$and`, `$or`, `$not`, `$nor` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Element operators**: `$exists`, `$type` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Evaluation operators**: `$regex`, `$expr`, `$mod`, `$jsonSchema`, `$text`, `$where` → [`02`](./02-CRUD-Operations-And-Query-Operators.md), [`03`](./03-Indexing-And-Performance.md)
- [x] **Array operators**: `$all`, `$elemMatch`, `$size` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Update operators**: `$set`, `$unset`, `$inc`, `$mul`, `$min`, `$max`, `$rename`, `$currentDate` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Array update operators**: `$push`, `$pull`, `$pop`, `$addToSet`, `$pullAll`, `$each`, `$slice`, `$position`, `$sort` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Positional operators**: `$`, `$[]`, `$[<id>]` (`arrayFilters`) → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] `updateOne`, `updateMany`, `replaceOne`, `findOneAndUpdate`, **upsert** → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] `deleteOne`, `deleteMany`, `findOneAndDelete` → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] **Projection** (inclusion, exclusion, `$elemMatch`, `$slice`) → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] `sort`, `limit`, `skip`, pagination → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] `bulkWrite`, ordered vs unordered → [`02`](./02-CRUD-Operations-And-Query-Operators.md)
- [x] Read concern, write concern (preview) → [`02`](./02-CRUD-Operations-And-Query-Operators.md), [`07`](./07-Transactions-And-Replication.md)

### E. Indexes & performance
- [x] Why indexes exist, B-tree underlying structure → [`03`](./03-Indexing-And-Performance.md)
- [x] **Single-field** indexes → [`03`](./03-Indexing-And-Performance.md)
- [x] **Compound** indexes & the **ESR rule** (Equality, Sort, Range) → [`03`](./03-Indexing-And-Performance.md)
- [x] **Multikey** indexes (on arrays) → [`03`](./03-Indexing-And-Performance.md)
- [x] **Text** indexes → [`03`](./03-Indexing-And-Performance.md)
- [x] **Geospatial** indexes (`2d`, `2dsphere`) → [`03`](./03-Indexing-And-Performance.md)
- [x] **TTL** indexes (auto-expire) → [`03`](./03-Indexing-And-Performance.md)
- [x] **Partial** & **sparse** indexes → [`03`](./03-Indexing-And-Performance.md)
- [x] **Unique** & **hashed** indexes → [`03`](./03-Indexing-And-Performance.md), [`08`](./08-Sharding-Security-And-Production.md)
- [x] Wildcard indexes (overview) → [`03`](./03-Indexing-And-Performance.md)
- [x] **`explain()`** & reading query plans (COLLSCAN, IXSCAN, FETCH, SORT) → [`03`](./03-Indexing-And-Performance.md)
- [x] **Covered queries** → [`03`](./03-Indexing-And-Performance.md)
- [x] Index intersection → [`03`](./03-Indexing-And-Performance.md)
- [x] **Working set** & RAM sizing → [`03`](./03-Indexing-And-Performance.md), [`08`](./08-Sharding-Security-And-Production.md)
- [x] Database **profiler** & slow query log → [`03`](./03-Indexing-And-Performance.md)
- [x] Hot / cold data, capped collections → [`03`](./03-Indexing-And-Performance.md)

### F. Aggregation pipeline
- [x] What the pipeline is, mental model → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$match`**, **`$project`**, **`$addFields`** / `$set`, `$unset` → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$group`** & accumulators (`$sum`, `$avg`, `$min`, `$max`, `$first`, `$last`, `$push`, `$addToSet`) → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$sort`**, **`$limit`**, **`$skip`**, `$count` → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$lookup`** (left outer join) and uncorrelated `$lookup` with pipeline → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$unwind`** (flatten arrays), `preserveNullAndEmptyArrays` → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$facet`**, `$bucket`, `$bucketAuto` → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$replaceRoot`** / `$replaceWith` → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$out`** & **`$merge`** (materialized views) → [`04`](./04-Aggregation-Pipeline.md)
- [x] **`$graphLookup`** (recursive traversal) → [`04`](./04-Aggregation-Pipeline.md), [`05`](./05-Schema-Design-Patterns.md)
- [x] Window functions (`$setWindowFields`) → [`04`](./04-Aggregation-Pipeline.md)
- [x] Expression operators (`$cond`, `$ifNull`, `$switch`, `$arrayElemAt`, `$map`, `$filter`, `$reduce`, `$dateToString`, `$concat`, `$split`...) → [`04`](./04-Aggregation-Pipeline.md)
- [x] Aggregation optimization (stage ordering, index use, allowDiskUse, `$match` early) → [`04`](./04-Aggregation-Pipeline.md)

### G. Schema design patterns
- [x] **Embedding vs referencing** — the cardinality decision → [`05`](./05-Schema-Design-Patterns.md)
- [x] One-to-one, one-to-few, one-to-many, **one-to-squillions** → [`05`](./05-Schema-Design-Patterns.md)
- [x] Denormalization tradeoffs (read speed vs write coordination) → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Schema versioning** pattern → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Computed** pattern → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Bucket** pattern (time-series / IoT) → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Attribute** pattern (sparse fields) → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Polymorphic** pattern → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Extended Reference** pattern → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Outlier** pattern → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Subset** pattern → [`05`](./05-Schema-Design-Patterns.md)
- [x] **Tree patterns** — parent reference, child reference, ancestor array, materialized path → [`05`](./05-Schema-Design-Patterns.md)
- [x] Time-series collections (native) → [`05`](./05-Schema-Design-Patterns.md)
- [x] JSON Schema validation on collections → [`05`](./05-Schema-Design-Patterns.md), [`06`](./06-Mongoose-And-Nodejs-Integration.md)

### H. Mongoose & Node.js integration
- [x] Why Mongoose? When **not** to use it → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Connecting (`mongoose.connect`, options, events, retries) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Schemas — every field option (`type`, `required`, `default`, `min`, `max`, `enum`, `match`, `validate`, `lowercase`, `trim`, `index`, `unique`, `sparse`, `select`) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] SchemaTypes (String, Number, Date, Boolean, Buffer, ObjectId, Mixed, Array, Decimal128, Map) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Models, `Model.create`, `find`, `findById`, `findOne`, `updateOne`, `findOneAndUpdate`, `deleteOne` → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] **Validators** (built-in & custom) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] **Middleware / hooks** (`pre`/`post` for `save`, `validate`, `remove`, `findOneAndUpdate`, aggregate) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] **Virtuals** (regular & populated) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Instance methods, **statics**, query helpers → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] **Populate** (single, multiple, nested, virtual populate, with `select`/`match`) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] **Discriminators** (single-collection inheritance) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] **Plugins** (reusable schema features) → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Lean queries (`.lean()`) and performance → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Transactions in Mongoose (`session`, `withTransaction`) → [`06`](./06-Mongoose-And-Nodejs-Integration.md), [`07`](./07-Transactions-And-Replication.md)
- [x] Error handling, validation errors, cast errors, duplicate-key → [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Full **Express + Mongoose** REST CRUD example → [`06`](./06-Mongoose-And-Nodejs-Integration.md)

### I. Transactions & replication
- [x] Single-document atomicity guarantees → [`07`](./07-Transactions-And-Replication.md)
- [x] **Multi-document ACID transactions** (4.0+, 4.2+ across shards) → [`07`](./07-Transactions-And-Replication.md)
- [x] Sessions, `startTransaction`, `commitTransaction`, `abortTransaction` → [`07`](./07-Transactions-And-Replication.md)
- [x] **`withTransaction`** helper & retry logic (TransientTransactionError, UnknownTransactionCommitResult) → [`07`](./07-Transactions-And-Replication.md)
- [x] When **not** to use transactions (model first) → [`07`](./07-Transactions-And-Replication.md)
- [x] **Replica sets** — primary, secondary, arbiter, hidden, delayed → [`07`](./07-Transactions-And-Replication.md)
- [x] **Oplog** mechanics → [`07`](./07-Transactions-And-Replication.md)
- [x] Elections, heartbeats, priorities → [`07`](./07-Transactions-And-Replication.md)
- [x] **Read preferences** (`primary`, `primaryPreferred`, `secondary`, `secondaryPreferred`, `nearest`) → [`07`](./07-Transactions-And-Replication.md)
- [x] **Write concerns** (`w: 1`, `w: "majority"`, `j: true`, `wtimeout`) → [`07`](./07-Transactions-And-Replication.md)
- [x] Read concerns (`local`, `available`, `majority`, `linearizable`, `snapshot`) → [`07`](./07-Transactions-And-Replication.md)
- [x] Failover behavior, retryable writes → [`07`](./07-Transactions-And-Replication.md)
- [x] **Change streams** (collection / db / cluster, `resumeToken`, `fullDocument`) → [`07`](./07-Transactions-And-Replication.md)

### J. Sharding
- [x] Why & when to shard → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Sharded cluster components (`mongos`, config servers, shards) → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Shard key** choice (cardinality, frequency, monotonic risk) → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Hashed** vs **ranged** shard keys → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Compound shard keys, zone (tag-aware) sharding → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Chunks**, balancer, jumbo chunks → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Targeted vs scatter-gather queries → [`08`](./08-Sharding-Security-And-Production.md)

### K. Security
- [x] **Authentication** (SCRAM, x.509, LDAP, Kerberos) → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Authorization / RBAC** — built-in roles, custom roles → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **TLS / SSL** for transport → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Encryption at rest** (WiredTiger encryption, KMIP) → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Client-side field-level encryption** (CSFLE) — overview → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Network isolation, firewall, IP allow-list → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Audit log → [`08`](./08-Sharding-Security-And-Production.md)
- [x] OWASP-style: NoSQL injection, why operators in user input are dangerous → [`02`](./02-CRUD-Operations-And-Query-Operators.md), [`08`](./08-Sharding-Security-And-Production.md)

### L. Operations & production
- [x] **Backups** — `mongodump`/`mongorestore`, filesystem snapshots, point-in-time recovery → [`08`](./08-Sharding-Security-And-Production.md)
- [x] **Monitoring** — `mongostat`, `mongotop`, `db.serverStatus()`, Atlas metrics, OpenTelemetry → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Connection pooling, `maxPoolSize` → [`08`](./08-Sharding-Security-And-Production.md), [`06`](./06-Mongoose-And-Nodejs-Integration.md)
- [x] Capacity planning (CPU, RAM = working set, disk, IOPS) → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Deployment options — self-hosted, Docker, Kubernetes operator, **MongoDB Atlas** → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Atlas tiers, search indexes, triggers, data lake (overview) → [`08`](./08-Sharding-Security-And-Production.md)
- [x] Production checklist → [`08`](./08-Sharding-Security-And-Production.md)

---

## 🛠️ SETUP — GET A WORKING MONGODB TOOLCHAIN

You write queries in **mongosh** (the shell) or in your app (via a driver / Mongoose). Behind both is **`mongod`**, the database server. You have two equally good ways to get one:

### Option A — MongoDB Atlas (recommended for learning)

A cloud-hosted MongoDB. The free **M0** cluster gives you 512 MB and is plenty for this section. Zero install pain, real replica set, real connection string.

1. Sign up at <https://www.mongodb.com/cloud/atlas/register>.
2. Create a free **M0** cluster (pick a region near you).
3. Create a database user (write down the password).
4. **Network Access** → add your IP (or `0.0.0.0/0` while learning).
5. Click **Connect** → "Drivers" → copy the connection string. It will look like:

```
mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### Option B — MongoDB Community Edition (local install)

Run `mongod` on your laptop. Better for offline work and total control.

| OS | Easiest path |
|----|--------------|
| Windows | Installer at <https://www.mongodb.com/try/download/community> · or `winget install MongoDB.Server` |
| macOS | `brew tap mongodb/brew && brew install mongodb-community@7.0` then `brew services start mongodb-community@7.0` |
| Linux | Follow the distro guide at <https://www.mongodb.com/docs/manual/administration/install-on-linux/> |
| Docker | `docker run -d --name mongo -p 27017:27017 -v mongodata:/data/db mongo:7` |

After install, `mongod` listens on `localhost:27017` by default and your connection string is simply:

```
mongodb://localhost:27017
```

### The shell — `mongosh`

Install **mongosh** (the modern shell) separately if your install didn't include it: <https://www.mongodb.com/try/download/shell>.

```bash
mongosh "mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/"   # Atlas
mongosh                                                         # local default
```

```js
// Inside mongosh:
show dbs                              // list databases
use codex                             // switch to (or create) database "codex"
db.users.insertOne({ name: "Ada" })   // creates collection "users" on first write
db.users.find()                       // see what you stored
```

### MongoDB Compass — the GUI

Install Compass (<https://www.mongodb.com/products/compass>) to *visually* browse documents, build aggregation pipelines stage by stage, view query plans, and analyze schemas. Hugely useful while learning the aggregation framework (file 04).

### Node.js client setup

We use **Mongoose** in file 06 (and the rest of the codex). The native driver is also covered.

```bash
mkdir mongo-codex && cd mongo-codex
npm init -y
npm install mongoose dotenv
echo "MONGODB_URI=mongodb://localhost:27017/codex" > .env
echo "node_modules" > .gitignore
```

```js
// hello.js — confirm everything talks to everything
import "dotenv/config";
import mongoose from "mongoose";

await mongoose.connect(process.env.MONGODB_URI);
console.log("Connected to:", mongoose.connection.host, mongoose.connection.name);
await mongoose.disconnect();
```

```bash
node hello.js
# Connected to: localhost codex
```

---

## 🧭 HOW TO STUDY THIS SECTION

1. **Have mongosh open the whole time.** Type every snippet. Mutate a document. Re-query. Reading without typing leaves no fingerprints.
2. **Build one project.** Pick a domain (recipes, books, gym log) and grow its data layer through every chapter — by file 06 it should be a Mongoose-backed Express API; by file 08 it has a replica-set deploy plan and a backup story.
3. **Use Compass as a teaching aid.** When a query is hard to reason about, paste it into Compass's aggregation builder and run stage-by-stage. The intuition you build is permanent.
4. **Don't skip schema design (file 05).** The query knowledge from file 02 is reversible; bad schemas in production are not.
5. **Read every "Common Pitfalls" table.** Those are the bugs you would otherwise hit live.

### The Project (do this once, all the way through)

| After file | Your project should... |
|------------|-------------------------|
| 01 | Connect, create a DB, insert a few docs by hand. |
| 02 | Have full CRUD scripts in `scripts/` using the native driver or mongosh. |
| 03 | Have indexes you justified with `explain()` output. |
| 04 | Have at least 3 aggregation pipelines (a report, a top-N, a join). |
| 05 | Have a written *schema design doc* (1 page) explaining every embed/ref decision. |
| 06 | Be a Mongoose-backed Express CRUD API with validation and middleware. |
| 07 | Use a transaction for one multi-document operation; have a `change-stream-listener.js`. |
| 08 | Have a deploy plan (Atlas or self-hosted), backup script, and a security checklist applied. |

---

## 🔗 RELATED SECTIONS

- Pairs with [`07-NODEJS-EXPRESS`](../07-NODEJS-EXPRESS/) — the API layer that talks to MongoDB.
- Contrast with [`08-SQL-DATABASES`](../08-SQL-DATABASES/) — same problem, different tradeoffs. Read both before designing real data layers.
- Combined into a full app in [`10-MERN-STACK`](../10-MERN-STACK/) and shipped in [`11-FULLSTACK-ENGINEERING`](../11-FULLSTACK-ENGINEERING/).
- Frontend that consumes these APIs: [`05-REACT`](../05-REACT/) and [`06-NEXTJS`](../06-NEXTJS/).
- Language depth: [`02-JAVASCRIPT-MASTERY`](../02-JAVASCRIPT-MASTERY/) and [`03-TYPESCRIPT`](../03-TYPESCRIPT/).

---

## 📖 DEEP REFERENCES

- **MongoDB Manual** — <https://www.mongodb.com/docs/manual/> (the source of truth)
- **MongoDB University** — <https://learn.mongodb.com/> (free certified courses)
- **Aggregation reference** — <https://www.mongodb.com/docs/manual/reference/operator/aggregation/>
- **Mongoose docs** — <https://mongoosejs.com/docs/guide.html>
- **MongoDB drivers** — <https://www.mongodb.com/docs/drivers/>
- **Building with Patterns** (MongoDB blog series) — <https://www.mongodb.com/blog/post/building-with-patterns-a-summary>
- **CAP theorem (Gilbert & Lynch)** — <https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf>
- **MongoDB Atlas docs** — <https://www.mongodb.com/docs/atlas/>

---

**→ Begin:** [`01-NoSQL-And-MongoDB-Fundamentals.md`](./01-NoSQL-And-MongoDB-Fundamentals.md) | Back to [`../README.md`](../README.md)
