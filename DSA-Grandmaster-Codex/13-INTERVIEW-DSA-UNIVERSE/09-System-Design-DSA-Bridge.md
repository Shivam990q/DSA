# 🌉 System Design ↔ DSA Bridge

> *"Every system design has algorithms at its heart. Know them to design well."*

---

## I. THE BRIDGE
System design (L5+) tests architecture. But the deep-dive components are powered by DSA. Knowing the algorithmic backbone separates strong candidates.

---

## II. THE ALGORITHM-COMPONENT MAP

| System component         | Underlying DSA                              |
|--------------------------|---------------------------------------------|
| Cache (LRU/LFU)          | HashMap + Doubly Linked List                |
| Distributed cache        | Consistent hashing (sorted ring + BS)       |
| DB membership check      | Bloom filter (avoid disk reads)             |
| DB index                 | B+ tree / LSM tree                          |
| Sorted set (Redis)       | Skip list                                   |
| Rate limiter             | Token bucket / sliding window log           |
| Autocomplete             | Trie + ranking heap                         |
| Unique count (analytics) | HyperLogLog                                 |
| Feed generation          | Heap (merge), fan-out                       |
| Nearest neighbor (geo)   | KD-tree / geohash / quadtree                |
| Dedup at scale           | MinHash / LSH                               |
| Frequency in stream      | Count-Min Sketch                            |
| Job scheduling           | Priority queue (heap)                       |
| Search ranking           | Inverted index + scoring                    |

---

## III. THE DEEP-DIVE STRATEGY
In a system design interview, when asked to detail a component, show the DSA:
> "For the cache, I'll use an LRU — a HashMap for O(1) lookup plus a doubly linked list for O(1) eviction of the least-recently-used entry."

> "For the rate limiter, a token bucket: each user has a bucket refilled at a fixed rate; a request consumes a token. O(1) per request."

---

## IV. THE 10 SYSTEMS + THEIR DSA
1. **URL shortener**: base62 encoding, hash, KV store
2. **Twitter**: feed (heap merge), fan-out, graph (follows)
3. **Rate limiter**: token bucket / sliding window
4. **Autocomplete**: Trie + top-K heap
5. **Distributed cache**: consistent hashing
6. **KV store**: LSM tree / B+ tree, Bloom filter
7. **Notification**: queue, pub-sub
8. **Chat**: websockets, message queue, sharding
9. **Ride-sharing**: geospatial index (quadtree/geohash), matching
10. **Web crawler**: BFS, dedup (Bloom filter), politeness queue

---

## V. WHAT TO STUDY
- **Algorithms**: LRU, consistent hashing, Bloom filter, Trie, skip list, LSM tree, token bucket, HyperLogLog
- **Systems**: Alex Xu's books, DDIA (Kleppmann)

---

## VI. THE INTEGRATION DRILL
For each of the 10 systems:
1. Sketch the high-level design
2. Pick 1-2 components
3. Detail the DSA backbone
4. Discuss tradeoffs

---

**→ Next:** [`10-Top-100-Per-Company.md`](./10-Top-100-Per-Company.md)
