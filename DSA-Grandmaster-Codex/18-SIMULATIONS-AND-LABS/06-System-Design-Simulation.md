# 🏗️ System Design Simulation

> *"Design a system that serves a billion users. You have 45 minutes."*

---

## I. THE FORMAT (FAANG L5+)
- 45 minutes
- "Design X" (Twitter, URL shortener, news feed, rate limiter, etc.)
- Evaluated on: requirements gathering, high-level design, deep dives, tradeoffs, scaling

---

## II. THE 6-STEP FRAMEWORK
```
1. REQUIREMENTS (5 min)
   - Functional: what does it do?
   - Non-functional: scale, latency, consistency?
   - Clarify scope with interviewer

2. ESTIMATION (5 min)
   - QPS (queries/sec), storage, bandwidth
   - Back-of-envelope: DAU, read/write ratio

3. API DESIGN (5 min)
   - Key endpoints, request/response

4. HIGH-LEVEL DESIGN (10 min)
   - Boxes and arrows: client, LB, services, DB, cache

5. DEEP DIVE (15 min)
   - Pick 1-2 components; detail them
   - Data model, sharding, caching, algorithms

6. TRADEOFFS & SCALING (5 min)
   - Bottlenecks, single points of failure
   - CAP tradeoffs, consistency models
```

---

## III. SIMULATE SOLO
- Pick a system from the list
- Set 45-min timer
- Use Excalidraw / whiteboard
- Narrate aloud (record yourself)
- Self-grade against the rubric

---

## IV. THE DSA-FLAVORED DEEP DIVES
Know the algorithms behind components:
- **Cache**: LRU/LFU (HashMap + DLL)
- **Distributed cache**: consistent hashing
- **Rate limiter**: token bucket / sliding window log
- **Autocomplete**: Trie + ranking
- **Feed**: push vs pull, fan-out
- **Unique counting**: HyperLogLog
- **Dedup / membership**: Bloom filter
- **DB index**: B+ tree / LSM tree

---

## V. THE 10 CLASSIC SYSTEMS
1. URL shortener
2. Twitter / news feed
3. Rate limiter
4. Search autocomplete
5. Distributed key-value store
6. Notification system
7. Chat (WhatsApp)
8. Ride-sharing (Uber)
9. Video streaming (YouTube)
10. Web crawler

---

## VI. EVALUATION RUBRIC
```
☐ Gathered requirements before designing
☐ Did capacity estimation
☐ Clear high-level design
☐ Reasonable data model
☐ Discussed sharding/replication
☐ Identified bottlenecks
☐ Articulated tradeoffs (CAP, consistency)
☐ Mentioned the DSA backbone
```

---

## VII. RESOURCES
- **System Design Interview** Vol 1 & 2 (Alex Xu) ⭐
- **Designing Data-Intensive Applications** (Kleppmann)
- **Grokking the System Design Interview**
- **[ByteByteGo](https://bytebytego.com)** (Alex Xu's YouTube/newsletter)

---

**→ Next:** [`07-Behavioral-Interview-Simulation.md`](./07-Behavioral-Interview-Simulation.md)
