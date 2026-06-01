# 🍃 02 — CRUD Operations & Query Operators

> *"Every query is a question. Every operator is a way to ask it precisely. Master the vocabulary and the database stops being a black box."*

**Prev:** [`01-NoSQL-And-MongoDB-Fundamentals.md`](./01-NoSQL-And-MongoDB-Fundamentals.md) · **Next:** [`03-Indexing-And-Performance.md`](./03-Indexing-And-Performance.md) · **Index:** [`00-Index.md`](./00-Index.md)

---

## I. THE CRUD MAP

Every interaction with MongoDB falls into one of four categories. Memorize the surface:

| Category | mongosh / driver method | What it does |
|----------|--------------------------|--------------|
| **C**reate | `insertOne`, `insertMany` | Add one or many documents |
| **R**ead   | `find`, `findOne`, `countDocuments`, `distinct`, `aggregate` | Query documents |
| **U**pdate | `updateOne`, `updateMany`, `replaceOne`, `findOneAndUpdate`, `findOneAndReplace` | Modify documents in place |
| **D**elete | `deleteOne`, `deleteMany`, `findOneAndDelete` | Remove documents |
| Bulk       | `bulkWrite` | Mix all of the above in one round-trip |

All examples below run in **mongosh** unless noted. Same calls work from the Node driver — just `await` them and pull `.insertedId` / `.matchedCount` etc. off the result.

> **Set up the demo data once:**
> ```js
> use codex
> db.users.drop()
> db.users.insertMany([
>   { name: "Ada",    age: 36, role: "admin",  tags: ["math"],     scores: [90, 85, 95], joined: ISODate("2024-01-10") },
>   { name: "Grace",  age: 85, role: "admin",  tags: ["compiler"], scores: [88],         joined: ISODate("2023-11-02") },
>   { name: "Linus",  age: 54, role: "editor", tags: ["kernel"],   scores: [70, 60],     joined: ISODate("2024-02-15") },
>   { name: "Margaret", age: 87, role: "editor", tags: ["apollo"], scores: [],           joined: ISODate("2023-05-01") }
> ])
> ```

---

## II. CREATE — `insertOne` / `insertMany`

### `insertOne`

```js
const r = db.users.insertOne({ name: "Tim", age: 70, role: "guest" });
r.insertedId;          // ObjectId(...) of the new doc
r.acknowledged;        // true unless writeConcern says "fire and forget"
```

A doc with no `_id` gets an auto `ObjectId`. Supplying your own `_id` is allowed:

```js
db.products.insertOne({ _id: "sku-100", name: "Keyboard", price: 99 });
db.products.insertOne({ _id: "sku-100", name: "Dup" });
// → MongoServerError: E11000 duplicate key error
```

### `insertMany`

```js
db.users.insertMany([
  { name: "A" }, { name: "B" }, { name: "C" }
]);
```

The `ordered` option (default `true`) controls behavior on errors:

```js
// ordered:true  — stop at first error, items before it succeed, items after don't
// ordered:false — keep going past errors, return all failures at the end (faster too)
db.users.insertMany(
  [ { _id: 1, name: "A" }, { _id: 1, name: "DUP" }, { _id: 2, name: "C" } ],
  { ordered: false }
);
// A and C inserted; one E11000 error reported for the duplicate
```

> **Gotcha — partial failure with `ordered: true`.** If insert #5 fails, inserts #1–#4 are *already* committed. `insertMany` is **not** a transaction. Wrap it in a transaction (file 07) if you need all-or-nothing.

---

## III. READ — `find`, `findOne`, cursors

### Basic shape

```js
db.users.find()                                  // all documents (returns a cursor)
db.users.find({ role: "admin" })                 // filter
db.users.findOne({ name: "Ada" })                // first match (returns a document or null)
db.users.countDocuments({ age: { $gte: 50 } })   // accurate count
db.users.estimatedDocumentCount()                // metadata-based, fast, may be stale
db.users.distinct("role")                         // distinct values: ["admin", "editor", "guest"]
```

### Cursors — the lazy iterator

`find()` returns a **cursor**, not a result array. Nothing leaves the server until you iterate.

```js
const cur = db.users.find({ age: { $gte: 50 } });

cur.hasNext();          // does the server have another doc to give us?
cur.next();             // pull the next one
cur.toArray();          // pull EVERYTHING into an array (careful with big collections)
cur.forEach(doc => print(doc.name));

// Cursor options
db.users.find()
  .sort({ age: -1 })    // -1 desc, 1 asc — combine fields with order
  .skip(10)             // skip the first 10
  .limit(5)             // return at most 5
  .batchSize(100)       // wire-protocol batches (perf knob)
  .maxTimeMS(2000)      // server-side time budget — fail if longer
  .hint({ age: 1 })     // force a specific index
  .explain("executionStats");   // see the query plan (file 03)
```

> **Gotcha — `.toArray()` on a giant collection.** It loads everything into memory. For million-doc collections, iterate or paginate. Cursors stream.

---

## IV. QUERY OPERATORS — THE COMPLETE VOCABULARY

The query language is built from operators prefixed with `$`. Without operators you get **equality** matching:

```js
db.users.find({ name: "Ada" })        // name == "Ada"
db.users.find({ name: "Ada", age: 36 }) // implicit AND on every key
```

### A. Comparison operators

| Operator | Meaning |
|----------|---------|
| `$eq`    | Equal (rarely needed — implicit) |
| `$ne`    | Not equal |
| `$gt`    | Greater than |
| `$gte`   | Greater than or equal |
| `$lt`    | Less than |
| `$lte`   | Less than or equal |
| `$in`    | Value is in an array |
| `$nin`   | Value is **not** in an array |

```js
db.users.find({ age: { $gt: 50 } })
db.users.find({ age: { $gte: 18, $lt: 65 } })   // range — both bounds
db.users.find({ role: { $in: ["admin", "editor"] } })
db.users.find({ role: { $nin: ["guest"] } })
db.users.find({ name: { $ne: "Ada" } })
```

> **Gotcha — `$ne` and `$nin` ignore indexes.** They have to scan documents that *don't match* a value, which usually defeats the index. Prefer positive matches (`$in`) when you can.

### B. Logical operators

| Operator | Meaning |
|----------|---------|
| `$and`   | All clauses match |
| `$or`    | At least one matches |
| `$not`   | Inverts the inner condition |
| `$nor`   | None of the clauses match |

```js
db.users.find({ $or: [ { age: { $gt: 80 } }, { role: "admin" } ] })

db.users.find({
  $and: [
    { age: { $gte: 30 } },
    { age: { $lte: 60 } },
    { role: "admin" }
  ]
})  // implicit AND would do the same — $and is needed when keys repeat

db.users.find({ age: { $not: { $gt: 50 } } })   // age <= 50 OR field missing

db.users.find({
  $nor: [{ role: "admin" }, { age: { $lt: 30 } }]
})  // NOT admin AND NOT young
```

> **Implicit AND vs explicit `$and`.** Multiple keys in the same object are AND'd automatically. You only need `$and` when you have *the same key twice* — e.g., two regex patterns on `name` you both want to match.

### C. Element operators

| Operator | Meaning |
|----------|---------|
| `$exists` | Field exists (or doesn't) on the document |
| `$type`   | Field has a specific BSON type (or types) |

```js
db.users.find({ deletedAt: { $exists: false } })  // not soft-deleted
db.users.find({ middleName: { $exists: true, $ne: "" } })

db.users.find({ age: { $type: "int" } })          // BSON type alias
db.users.find({ age: { $type: ["int", "long"] } })// any of these types
db.users.find({ phone: { $type: "string" } })     // catch the case where phone got saved as a number somewhere
```

### D. Evaluation operators

| Operator | Meaning |
|----------|---------|
| `$regex` | Field matches a regular expression |
| `$mod`   | `[divisor, remainder]` — fast modulo test |
| `$expr`  | Use aggregation expressions in a query (compare two fields, run `$cond`, etc.) |
| `$jsonSchema` | Validate against a JSON Schema |
| `$text`  | Text search (requires text index — file 03) |
| `$where` | Run a JS function — **avoid**, very slow, unsafe |

```js
// Regex — case-insensitive prefix match (anchor with ^ for index use)
db.users.find({ name: { $regex: /^A/i } })          // names starting with A or a
db.users.find({ name: /grace/i })                   // shorthand: regex literal directly

// $expr — compare two fields in the same document
db.orders.find({ $expr: { $gt: ["$paid", "$due"] } })

// $jsonSchema — enforce shape inside a query (also used as a collection validator)
db.users.find({
  $jsonSchema: {
    bsonType: "object",
    required: ["email"],
    properties: { email: { bsonType: "string", pattern: "@" } }
  }
})

// $mod — pick every 3rd id (rarely useful, but exists)
db.events.find({ ticket: { $mod: [3, 0] } })
```

> **Gotcha — anchored vs unanchored regex.** `/^prefix/` can use an index on `name`; `/contains/` cannot — it has to scan every value. Build a text index (file 03) for substring/full-text search.

### E. Array operators

| Operator | Meaning |
|----------|---------|
| `$all`        | Array contains **all** of these values |
| `$elemMatch`  | At least one element matches an inner query (multi-condition) |
| `$size`       | Array has exactly N elements |

```js
db.users.find({ tags: "math" })           // matches if "math" is one of the elements
db.users.find({ tags: { $all: ["math", "science"] } }) // BOTH must be present (any order)

// $elemMatch — used when you need MULTIPLE conditions on the SAME array element
db.users.find({
  scores: { $elemMatch: { $gte: 80, $lt: 90 } }
})  // at least ONE score in [80, 90)

db.users.find({ scores: { $size: 0 } })   // empty array
```

> **Gotcha — `tags: { $gt: "a", $lt: "z" }` does not require ONE element to satisfy both.** Each clause can match a *different* element. Use `$elemMatch` when both clauses must hit the same element.

### F. Querying nested fields & arrays

```js
// Nested object — dot path
db.users.find({ "address.city": "London" })

// Array of objects — match by element fields
db.users.insertOne({
  name: "Mira",
  scores: [{ subject: "math", value: 90 }, { subject: "english", value: 70 }]
});

db.users.find({ "scores.subject": "math" })          // any element with subject:math
db.users.find({                                      // and same element with value≥85
  scores: { $elemMatch: { subject: "math", value: { $gte: 85 } } }
})
```

### G. Geospatial query operators (preview — file 03)

`$near`, `$nearSphere`, `$geoWithin`, `$geoIntersects` query points/polygons — they require a `2dsphere` index. Covered in file 03.

### H. Projection operators (in `find` second arg)

`$elemMatch`, `$slice`, and the positional `$` are projection-only operators that shape the returned document.

```js
// Return only the first matching subdoc from an array
db.users.find({ tags: "math" }, { name: 1, "tags.$": 1 })  // tags will contain ONLY "math"

// $elemMatch projection — multi-condition picker
db.users.find(
  {},
  { name: 1, scores: { $elemMatch: { $gte: 80 } } }
)   // each user gets one score >=80 (or scores omitted)

// $slice — return only N elements of an array
db.users.find({}, { name: 1, scores: { $slice: 2 } })            // first 2 scores
db.users.find({}, { name: 1, scores: { $slice: -3 } })           // last 3
db.users.find({}, { name: 1, scores: { $slice: [1, 2] } })       // skip 1, take 2
```

---

## V. PROJECTION — SHAPING WHAT COMES BACK

The 2nd argument to `find` selects fields. `1` includes, `0` excludes. **You cannot mix include/exclude** in the same projection (one exception — you can always exclude `_id`).

```js
db.users.find({}, { name: 1, age: 1 })          // name + age + _id (always returned unless excluded)
db.users.find({}, { name: 1, age: 1, _id: 0 })  // only name + age
db.users.find({}, { password: 0 })              // everything EXCEPT password
db.users.find({}, { name: 1, "address.city": 1, _id: 0 }) // dot path projection

// Mixing include + exclude is illegal (except _id)
db.users.find({}, { name: 1, age: 0 })          // ERROR
```

Projection is enforced **server-side** — the omitted fields aren't sent over the wire, saving CPU and bandwidth. Always project on hot endpoints.

---

## VI. SORT, LIMIT, SKIP — AND PAGINATION

```js
db.users.find().sort({ age: -1 })                     // oldest first
db.users.find().sort({ role: 1, age: -1 })            // role asc, then age desc within each role
db.users.find().sort({ age: -1 }).limit(5)            // top 5
db.users.find().sort({ age: -1 }).skip(20).limit(10)  // page 3 (20 per page... wait, see below)

// Skip+limit pagination — simple, works for small offsets
const PAGE = 3, PER = 10;
db.users.find().sort({ joined: -1 }).skip((PAGE - 1) * PER).limit(PER);
```

> **Gotcha — `skip` is O(N).** The server still walks past the skipped docs. For deep pagination (page 1000+), use **cursor-based pagination** with the last seen `_id`/timestamp:

```js
// "Give me the next page after the last item I saw"
const last = ObjectId("65f9ab...");           // _id of the last item from previous page
db.users.find({ _id: { $gt: last } })
        .sort({ _id: 1 }).limit(PER);
```

This stays O(log N) because it's just a range scan on the index.

> **Gotcha — sort needs an index or RAM.** A non-indexed `.sort()` on a big collection runs in memory and **fails at 100 MB** by default. Either index the sort key (file 03) or pass `.allowDiskUse()` (aggregation only).

---

## VII. UPDATE — OPERATORS, NOT REPLACEMENT

The cardinal sin of new MongoDB users is replacing whole documents instead of updating fields. Use **update operators**:

```js
// REPLACES the entire doc with { age: 37 } — name and everything else GONE
db.users.updateOne({ name: "Ada" }, { age: 37 })       // ❌ this is replaceOne semantics... actually it errors in mongosh now

// Correct — use $set
db.users.updateOne({ name: "Ada" }, { $set: { age: 37 } })
```

### A. Field update operators

| Operator | What it does |
|----------|--------------|
| `$set`         | Set field to value (creates if missing) |
| `$unset`       | Remove a field |
| `$inc`         | Increment numeric field (negative to decrement) |
| `$mul`         | Multiply numeric field |
| `$min`         | Set to smaller of (current, new) |
| `$max`         | Set to larger of (current, new) |
| `$rename`      | Rename a field |
| `$currentDate` | Set field to current date/timestamp |
| `$setOnInsert` | Apply only if upsert inserts a new doc |

```js
db.users.updateOne({ name: "Ada" }, {
  $set: { "address.city": "Cambridge", lastSeen: new Date() },
  $unset: { temporaryFlag: "" },
  $inc: { loginCount: 1 },
  $min: { lowestScore: 50 },
  $max: { highScore: 99 },
  $mul: { creditMultiplier: 1.05 },
  $rename: { oldField: "newField" },
  $currentDate: { updatedAt: true, lastTouchTs: { $type: "timestamp" } }
});
```

### B. Array update operators

| Operator | What it does |
|----------|--------------|
| `$push`     | Append element to array |
| `$pull`     | Remove all elements matching a query |
| `$pop`      | Remove first (`-1`) or last (`1`) element |
| `$addToSet` | Append only if not already present |
| `$pullAll`  | Remove every value from a list |
| `$each`     | Modifier — apply to every element of a list |
| `$slice`    | After `$push`, trim array to length |
| `$position` | After `$push`, insert at index |
| `$sort`     | After `$push`, sort the array |

```js
// Append one
db.users.updateOne({ name: "Ada" }, { $push: { tags: "logic" } })

// Append many, keep array bounded to 5 most recent
db.users.updateOne({ name: "Ada" }, {
  $push: { activity: { $each: [{ at: new Date(), kind: "login" }], $slice: -5 } }
})

// Append at index 0
db.users.updateOne({ name: "Ada" }, {
  $push: { activity: { $each: [{ kind: "preview" }], $position: 0 } }
})

// Set semantics — push only if not present
db.users.updateOne({ name: "Ada" }, { $addToSet: { tags: "math" } })  // no-op if already there
db.users.updateOne({ name: "Ada" }, { $addToSet: { tags: { $each: ["a", "b", "c"] } } })

// Remove
db.users.updateOne({ name: "Ada" }, { $pull: { tags: "obsolete" } })
db.users.updateOne({ name: "Ada" }, { $pull: { scores: { $lt: 50 } } })   // remove scores below 50
db.users.updateOne({ name: "Ada" }, { $pullAll: { tags: ["a", "b"] } })
db.users.updateOne({ name: "Ada" }, { $pop: { scores: 1 } })              // remove last
db.users.updateOne({ name: "Ada" }, { $pop: { scores: -1 } })             // remove first
```

### C. Positional operators — updating the right array element

The hardest part of array updates: targeting one (or some) of the elements.

| Operator | Targets |
|----------|---------|
| `$` (positional) | The first element matched by the query filter |
| `$[]` (all)      | Every element |
| `$[<id>]` + `arrayFilters` | Elements matching named conditions |

```js
// "$" — first matching element
db.users.updateOne(
  { name: "Mira", "scores.subject": "math" },
  { $set: { "scores.$.value": 100 } }   // updates the first element with subject:math
);

// "$[]" — every element
db.users.updateMany(
  {},
  { $inc: { "scores.$[].value": 5 } }    // bump every score by 5
);

// "$[id]" with arrayFilters — every element matching a condition
db.users.updateOne(
  { name: "Mira" },
  { $set: { "scores.$[low].value": 0 } },
  { arrayFilters: [ { "low.value": { $lt: 50 } } ] }    // zero out failing scores
);
```

> **Gotcha — `$` only finds the FIRST match.** If a doc has two array elements satisfying the filter, only the first is updated. Use `arrayFilters` for "all matching."

### D. Aggregation pipeline updates (4.2+)

Update commands can take a *pipeline* instead of an operator object — useful for computed updates that depend on the current document:

```js
db.users.updateMany({}, [
  { $set: {
      fullName: { $concat: ["$firstName", " ", "$lastName"] },
      ageGroup: { $switch: {
        branches: [
          { case: { $lt: ["$age", 18] }, then: "minor" },
          { case: { $lt: ["$age", 65] }, then: "adult" }
        ],
        default: "senior"
      } }
  } }
])
```

### E. `updateOne` vs `updateMany` vs `replaceOne`

| Method | Behavior |
|--------|----------|
| `updateOne(filter, update)` | Apply operators to first match |
| `updateMany(filter, update)` | Apply operators to **every** match |
| `replaceOne(filter, doc)` | Replace the whole document (no operators) — `_id` preserved |

```js
db.users.updateMany(
  { role: "guest" },
  { $set: { role: "user", upgradedAt: new Date() } }
);

db.users.replaceOne({ name: "Tim" }, { name: "Tim", role: "admin", age: 70 });
```

### F. Upsert — insert if not found

```js
// "Set Ada's last login; if Ada doesn't exist, create her with this state."
db.users.updateOne(
  { name: "Ada" },
  {
    $set: { lastLogin: new Date() },
    $setOnInsert: { name: "Ada", role: "user", createdAt: new Date() }
  },
  { upsert: true }
);
```

`$setOnInsert` only applies if the upsert inserts. Without it the *filter* itself supplies fields on insert, which often surprises people.

### G. `findOneAndUpdate` — atomic find + update + return

```js
const updated = db.users.findOneAndUpdate(
  { name: "Ada" },
  { $inc: { loginCount: 1 } },
  { returnDocument: "after" }     // or "before" — default is "before"
);
// returns the document, atomic at the document level
```

The driver equivalent (Node) is `findOneAndUpdate` with `{ returnDocument: "after" }`. Use this when you need the post-update doc and *cannot* tolerate a race between read and write — counters, queues, sequence generation.

---

## VIII. DELETE

```js
db.users.deleteOne({ name: "Tim" })            // first match
db.users.deleteMany({ role: "guest" })         // all matches
db.users.deleteMany({})                        // EVERY document — be careful

// Find + delete + return the deleted doc, atomically
const removed = db.users.findOneAndDelete({ name: "Linus" });
```

Soft-delete pattern — preferred for anything you might want to restore or audit:

```js
db.users.updateOne(
  { _id: id },
  { $set: { deletedAt: new Date() } }
);

// All "live" queries filter it out
db.users.find({ deletedAt: { $exists: false } });
```

> **Gotcha — `db.users.remove()` is removed.** That was the legacy `mongo` shell API. Use `deleteOne` / `deleteMany`.

---

## IX. BULK WRITES — MIX AND MATCH IN ONE ROUND-TRIP

`bulkWrite` accepts an array of operations and ships them together. Single network round-trip, single command on the server.

```js
const result = db.users.bulkWrite([
  { insertOne: { document: { name: "X", role: "user" } } },
  { updateOne: {
      filter: { name: "Ada" },
      update: { $inc: { loginCount: 1 } }
  } },
  { updateMany: {
      filter: { role: "editor" },
      update: { $set: { active: true } }
  } },
  { deleteOne: { filter: { name: "Tim" } } },
  { replaceOne: {
      filter: { name: "Grace" },
      replacement: { name: "Grace Hopper", role: "admin" },
      upsert: true
  } }
], { ordered: false });   // false = parallel, faster, no early stop on error
```

Result includes `insertedCount`, `matchedCount`, `modifiedCount`, `deletedCount`, `upsertedCount`, `upsertedIds`. Use bulk writes for batch import, ETL, and any time your app would otherwise loop and call `updateOne` 100 times.

---

## X. WRITE CONCERN AND READ CONCERN (preview)

Every write call accepts a `writeConcern` and every read accepts a `readConcern` and `readPreference`. They control durability and freshness; full coverage is in **file 07**, but the cheat sheet:

```js
// "Don't ack until a majority of replica members have it journaled"
db.users.insertOne({ name: "X" }, { writeConcern: { w: "majority", j: true, wtimeout: 5000 } });

// Read what a majority has confirmed (avoids reading writes that might roll back)
db.users.find({ active: true }).readConcern("majority");

// Send reads to the nearest secondary (faster, possibly stale)
db.users.find().readPref("secondaryPreferred");
```

In a single-node cluster these don't change much; on a real replica set they're the difference between "Web 2.0" eventual reads and "always correct."

---

## XI. NOSQL INJECTION — DO NOT SHIP THIS BUG

If your API takes JSON body parameters and passes them straight into `find`, an attacker can supply *operators* and rewrite your query.

```js
// Vulnerable Express handler
app.post("/login", async (req, res) => {
  // req.body = { user: "ada", pass: { $ne: null } }   ← attacker sent this
  const u = await User.findOne({ user: req.body.user, pass: req.body.pass });
  if (u) return res.send("welcome");
});
```

`{ $ne: null }` matches any non-null password. Login succeeds without a password.

Fixes:

1. **Validate input shape** (zod, Joi, express-validator). `pass` must be a `string`.
2. **Cast / coerce** explicitly before queries: `String(req.body.user)`.
3. **Disable operators** in user input — `mongoose-sanitize` / `express-mongo-sanitize` strip keys starting with `$` or containing `.`.
4. Use **parameterized queries** in spirit — never spread `req.body` into a filter object directly.

```js
import sanitize from "express-mongo-sanitize";
app.use(sanitize());                // strip $ and . from keys in req.body / req.query / req.params
```

---

## XII. A REAL CRUD PATTERN — NODE NATIVE DRIVER

Putting it together. Connect once, reuse the client, pool connections, handle errors.

```js
// users.js — a tiny repository
import { MongoClient, ObjectId } from "mongodb";

const client = new MongoClient(process.env.MONGODB_URI, {
  maxPoolSize: 10
});
await client.connect();
const users = client.db("codex").collection("users");

export async function createUser(data) {
  const r = await users.insertOne({ ...data, createdAt: new Date() });
  return r.insertedId;
}

export async function listUsers({ skip = 0, limit = 20, q = "" } = {}) {
  const filter = q
    ? { name: { $regex: `^${q}`, $options: "i" } }   // anchored — index-friendly
    : {};
  return users.find(filter)
              .project({ name: 1, role: 1, age: 1 })
              .sort({ _id: -1 })
              .skip(skip)
              .limit(limit)
              .toArray();
}

export async function getUser(id) {
  if (!ObjectId.isValid(id)) return null;             // never trust user input
  return users.findOne({ _id: new ObjectId(id) });
}

export async function updateUser(id, patch) {
  const allowed = ["name", "age", "role"];
  const $set = Object.fromEntries(
    Object.entries(patch).filter(([k]) => allowed.includes(k))
  );
  if (!Object.keys($set).length) throw new Error("No valid fields to update");
  return users.findOneAndUpdate(
    { _id: new ObjectId(id) },
    { $set, $currentDate: { updatedAt: true } },
    { returnDocument: "after" }
  );
}

export async function deleteUser(id) {
  return users.deleteOne({ _id: new ObjectId(id) });
}
```

That repository fits cleanly under an Express handler from section 07. Mongoose (file 06) does the same thing with schemas and validators bolted on.

---

## XIII. COMMON PITFALLS — A CHECKLIST

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Forgetting `$set` in update | Whole doc replaced (or modern error) | Always wrap field changes in operators |
| Mixing include + exclude in projection | `Cannot do exclusion on field X in inclusion projection` | Pick one (you can always exclude `_id`) |
| Skip pagination for deep pages | Slow page loads at page 1000 | Cursor-based pagination on indexed sort key |
| `$ne` / `$nin` on indexed field | Slow query, full collection scan | Rewrite as `$in` / equality where possible |
| Unanchored regex | Full collection scan | Anchor with `^` or use a text index |
| `$elemMatch` skipped when needed | Wrong array element matched | Use `$elemMatch` for multi-condition array queries |
| `arrayFilters` not provided | "Could not find array filter…" | Match every `$[name]` with an entry in `arrayFilters` |
| `replaceOne` instead of `updateOne` | Fields silently disappear | Use `updateOne` with operators for partial updates |
| `bulkWrite` ordered:true with mixed ops | One failure aborts the rest | `{ ordered: false }` if order doesn't matter |
| Spreading `req.body` into a filter | NoSQL injection | Validate, sanitize, never trust user input |
| `_id` not converted to `ObjectId` | Query "finds nothing" with a string id | `new ObjectId(id)` (validate first) |

---

## 🧠 KEY TAKEAWAYS

- The CRUD verbs are `insertOne/Many`, `find`/`findOne`, `updateOne/Many` + `replaceOne` + `findOneAndUpdate`, `deleteOne/Many` + `findOneAndDelete`, plus `bulkWrite` to combine them.
- Queries are **JSON objects** of filters plus operators. Memorize the comparison ($eq/$ne/$gt/$gte/$lt/$lte/$in/$nin), logical ($and/$or/$not/$nor), element ($exists/$type), evaluation ($regex/$expr/$jsonSchema/$text), and array ($all/$elemMatch/$size) operators.
- Updates **must** use operators — `$set`, `$unset`, `$inc`, `$push`, `$pull`, `$addToSet` and friends. Forgetting them replaces the whole document.
- The positional operators `$`, `$[]`, and `$[name]` (with `arrayFilters`) target the right array elements. Use them precisely.
- Use **projection** to avoid sending unneeded fields, **sort+limit** with indexed keys to avoid in-memory sorts, and **cursor pagination** for deep pages.
- `findOneAndUpdate` with `returnDocument:"after"` gives you atomic read-modify-write semantics on a single document.
- `bulkWrite` is your friend for batch jobs — one round-trip, one server command.
- **NoSQL injection is real.** Validate user input, sanitize `$`/`.`-prefixed keys, cast `_id`s through `ObjectId.isValid`.

---

**Prev:** [`01-NoSQL-And-MongoDB-Fundamentals.md`](./01-NoSQL-And-MongoDB-Fundamentals.md) · **Next:** [`03-Indexing-And-Performance.md`](./03-Indexing-And-Performance.md) · **Index:** [`00-Index.md`](./00-Index.md)
