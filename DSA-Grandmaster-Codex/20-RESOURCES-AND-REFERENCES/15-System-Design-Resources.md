# 🏗️ System Design Resources — Complete Guide

> For senior interviews (L5+), unicorns, and big tech. The other pillar beyond DSA.

---

## THE TWO TYPES
- **HLD (High-Level Design)** — distributed systems, scalability, architecture (FAANG senior)
- **LLD (Low-Level Design)** — OOP design, design patterns, class structure (machine coding rounds)

---

## TOP RESOURCES (FREE)

### GitHub ⭐
- **donnemartin/system-design-primer** ⭐⭐ — the legendary free guide
- **ashishps1/awesome-system-design-resources** ⭐ — curated free resources
- **ByteByteGoHq/system-design-101** ⭐ — visual explanations
- **alex-xu-system/bytebytego** — companion to the books
- **madd86/awesome-system-design** — curated list
- Search "awesome-low-level-design" for LLD repos

### YouTube ⭐
- **[ByteByteGo](https://bytebytego.com) (Alex Xu)** ⭐⭐ — visual system design
- **[Gaurav Sen](https://www.youtube.com/@gkcs)** ⭐ — fundamentals
- **Tech Dummies Narendra L** — detailed walkthroughs
- **[Hussein Nasser](https://www.youtube.com/@hnasr)** — backend/databases deep dives
- **codeKarle**, **System Design Interview** channels

### Books
- **System Design Interview Vol 1 & 2** (Alex Xu) ⭐⭐
- **Designing Data-Intensive Applications** (Martin Kleppmann) ⭐⭐ — the depth bible
- **Database Internals** (Petrov)
- **Understanding Distributed Systems** (Vitillo)

### Courses (paid)
- **Grokking the System Design Interview** ([DesignGurus](https://www.designgurus.io) / Educative)
- **Grokking the Advanced System Design Interview**
- **ByteByteGo course**

---

## THE HLD CONCEPTS TO MASTER
1. **Scalability** — horizontal vs vertical, load balancing
2. **Caching** — LRU/LFU, write-through/back, CDN, Redis
3. **Databases** — SQL vs NoSQL, sharding, replication, indexing
4. **Consistency** — CAP theorem, eventual vs strong, ACID vs BASE
5. **Messaging** — queues (Kafka, RabbitMQ), pub-sub
6. **Consistent hashing** — distributing data
7. **Rate limiting** — token bucket, sliding window
8. **Microservices** — vs monolith, API gateway
9. **Storage** — blob storage, file systems, object stores
10. **Networking** — DNS, CDN, load balancers, proxies
11. **Probabilistic structures** — Bloom filter, HyperLogLog, Count-Min
12. **Search** — inverted index, Elasticsearch

---

## THE LLD CONCEPTS TO MASTER
- OOP (4 pillars) — see [`12-CS-Core-Subjects/04-OOP.md`](./12-CS-Core-Subjects/04-OOP.md)
- SOLID principles
- Design patterns (creational, structural, behavioral)
- UML basics
- Machine coding: build working systems (Splitwise, parking lot, etc.)

---

## CLASSIC HLD PROBLEMS
1. URL shortener (TinyURL)
2. Twitter / news feed
3. Rate limiter
4. Search autocomplete (typeahead)
5. Distributed key-value store
6. Notification system
7. Chat system (WhatsApp/Messenger)
8. Ride-sharing (Uber)
9. Video streaming (YouTube/Netflix)
10. Web crawler
11. Distributed cache
12. Payment system (Stripe-like)
13. Google Drive / Dropbox
14. Ticketmaster / booking system
15. Instagram / photo sharing

## CLASSIC LLD PROBLEMS
1. Parking lot
2. Splitwise
3. Elevator system
4. Vending machine
5. Library management
6. Tic-tac-toe / chess
7. Snake & ladder
8. ATM
9. Logging framework
10. In-memory cache / rate limiter

---

## THE FRAMEWORK (HLD interview)
```
1. Requirements (functional + non-functional) — 5 min
2. Capacity estimation (QPS, storage, bandwidth) — 5 min
3. API design — 5 min
4. High-level design (boxes + arrows) — 10 min
5. Deep dive (1-2 components) — 15 min
6. Tradeoffs, bottlenecks, scaling — 5 min
```
(Detail: [`../18-SIMULATIONS-AND-LABS/06-System-Design-Simulation.md`](../18-SIMULATIONS-AND-LABS/06-System-Design-Simulation.md))

---

## THE PREP PLAN (6-8 weeks)
```
Week 1-2: Fundamentals (scalability, caching, databases, CAP)
Week 3-4: read system-design-primer + ByteByteGo; study 5 classic problems
Week 5-6: practice 10 HLD problems (narrate, draw)
Week 7-8: LLD + machine coding practice + mocks
```

---

## THE DSA CONNECTION
Every component has a DSA backbone. See [`../13-INTERVIEW-DSA-UNIVERSE/09-System-Design-DSA-Bridge.md`](../13-INTERVIEW-DSA-UNIVERSE/09-System-Design-DSA-Bridge.md).

---

**→ Back to:** [`00-Index.md`](./00-Index.md)
