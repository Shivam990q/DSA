# 🏗️ Level 8 — Algorithm Engineering (The Production Architect)

> *"The textbook algorithm is the seed. The production algorithm is the tree."*

---

## 🎯 OUTCOME

You can:
- Design production-grade algorithmic systems (search, ranking, recommendation, payment risk, ML pipelines)
- Optimize algorithms for cache, SIMD, distributed setting
- Debug performance bottlenecks via profiling
- Translate textbook algorithms into reliable production code
- Lead architectural decisions on systems with millions of QPS

---

## 📚 PREREQUISITE

Level 5 (FAANG) + Level 6 (CP) ideally; Level 7 if research-bent.

---

## 🧱 CURRICULUM (10 Modules, ~800 hours)

### Module 8.1 — Modern CPU Architecture for Algo Engineers (40 hours)

**Topics:**
1. CPU caches (L1/L2/L3), cache lines (typically 64 bytes)
2. Memory hierarchy: register → L1 → L2 → L3 → DRAM → SSD
3. Branch prediction & branch misses
4. SIMD: SSE, AVX, AVX-512 (intrinsics)
5. Pipelining, instruction-level parallelism
6. False sharing in multi-threaded code
7. NUMA architectures
8. Profiling tools: `perf`, VTune, gprof, callgrind

**Practical:** Re-implement a textbook algo (e.g., binary search) and profile it. Apply cache-friendly transformations. Measure speedup.

**Reading:**
- *What Every Programmer Should Know About Memory* — Ulrich Drepper
- Agner Fog's optimization manuals
- *Performance Engineering of Software Systems* ([MIT 6.172](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018/)) ⭐

---

### Module 8.2 — Cache-Oblivious & Cache-Aware Algorithms (30 hours)

**Topics:**
1. Cache-oblivious model
2. Cache-oblivious matrix transpose
3. Cache-oblivious matrix multiplication (Strassen + tiling)
4. Cache-oblivious B-trees
5. van Emde Boas layout for trees
6. Funnel sort (cache-oblivious sort)

---

### Module 8.3 — Concurrent Data Structures (30 hours)

**Topics:**
1. Lock-free vs lock-based
2. Atomic operations, CAS
3. ABA problem
4. Hazard pointers, RCU
5. Concurrent hash tables (Java's `ConcurrentHashMap`, Folly's `AtomicHashMap`)
6. Concurrent skip list
7. Lock-free queues (Michael-Scott)

---

### Module 8.4 — Distributed Algorithms (40 hours)

**Topics:**
1. Consensus: Paxos, Raft
2. Distributed hash tables: Chord, Kademlia
3. Gossip protocols
4. CRDTs (conflict-free replicated data types)
5. Vector clocks, Lamport timestamps
6. Distributed sorting (TeraSort, MapReduce)
7. Bloom filter (revisit, deeply)
8. HyperLogLog
9. Count-Min Sketch

---

### Module 8.5 — Approximation & Streaming Algorithms (30 hours)

**Topics:**
1. Reservoir sampling
2. Misra-Gries (heavy hitters)
3. Count-Min Sketch
4. HyperLogLog (cardinality estimation)
5. Bloom filter, Cuckoo filter
6. AMS sketch (frequency moments)
7. MinHash + LSH (similarity search)

---

### Module 8.6 — String Indexing in Production (20 hours)

**Topics:**
1. Inverted index (search engines)
2. Suffix arrays in production (e.g., bioinformatics)
3. FM-index, BWT
4. Aho-Corasick at scale
5. Trie with compressed children

---

### Module 8.7 — Graph Algorithms in Production (40 hours)

**Topics:**
1. PageRank (Google's algorithm)
2. Personalized PageRank
3. Community detection (Louvain)
4. Graph partitioning (METIS)
5. Distributed BFS (Pregel-style)
6. Approximate shortest paths
7. Hub labeling
8. Contraction hierarchies (Google Maps)

---

### Module 8.8 — Database & Storage Algorithms (40 hours)

**Topics:**
1. B-tree, B+ tree (indexes)
2. LSM tree (Cassandra, RocksDB)
3. Skip list
4. Bloom filters in DBs
5. Hash indexes vs tree indexes
6. Query optimization (cost-based, rule-based)
7. Join algorithms (nested loop, hash, sort-merge)
8. ACID, MVCC

---

### Module 8.9 — Real Production Case Studies (60 hours)

Study (read papers + system blogs):
1. **Google Search** indexing & ranking
2. **Google Maps** route planning (CHs, A*)
3. **Facebook News Feed** ranking
4. **Stripe Radar** payment fraud
5. **Uber dispatch** algorithm
6. **Amazon recommendations** (collaborative filtering)
7. **Bitcoin** UTXO + merkle trees
8. **Cassandra/DynamoDB** consistent hashing
9. **Redis Cluster** sharding
10. **YouTube** video recommendation

---

### Module 8.10 — Build Real Projects (200+ hours)

Build (with tests, benchmarks, docs):
1. A search engine over a 10GB Wikipedia dump
2. A rate-limiter library (production-grade)
3. A LSM tree-based key-value store (toy version)
4. A recommendation engine (matrix factorization)
5. An A* maze solver with heuristics
6. A graph database with Cypher subset

---

## 📊 PROJECT & PROBLEM VOLUME

This level is measured in **projects and papers**, not problem counts:
- **6+ production-grade projects** (Module 8.10), each with tests + benchmarks
- **10 real-world system case studies** (Module 8.9)
- **5+ landmark systems papers** (MapReduce, GFS, Spanner, Dynamo, Raft)
- ~50 focused exercises across the cache, concurrency, and profiling modules

---

## ⏱️ ESTIMATED TIME

- ~800 hours
- ~20 months at 10 hours/week
- ~8 months at 25 hours/week
- (Module 8.10 alone is 200+ hours — budget the build work accordingly.)

---

## ✅ EXIT TEST

Build a production-grade KV store (or rate limiter) with:
- Configurable backend (memory + disk)
- Concurrent access (lock-free or fine-grained locks)
- Benchmarked at 10K+ QPS on a laptop
- Unit tests + integration tests + chaos tests

---

## 📌 RESOURCES

### Books
- **Designing Data-Intensive Applications** (Kleppmann) ⭐
- **Database Internals** (Petrov)
- **The Algorithm Design Manual** (Skiena)
- **Engineering a Compiler** (Cooper, Torczon)
- **Hacker's Delight** (Warren) — bit tricks
- **The Art of Multiprocessor Programming** (Herlihy, Shavit)

### Courses
- **MIT 6.172 — Performance Engineering of Software Systems** ⭐⭐⭐
- **CMU Database Systems**
- **MIT 6.824 — Distributed Systems**

### Papers
- The "MapReduce" paper (Google)
- The "GFS" paper (Google)
- The "Spanner" paper (Google)
- The "Dynamo" paper (Amazon)
- The "Raft" paper

---

## 🚀 ON COMPLETION

You can now design, build, and optimize algorithmic systems at scale. You think in cache lines, QPS, and failure modes — not just Big-O.

**→ Proceed to:** [`Level-09-Research-Level.md`](./Level-09-Research-Level.md)
