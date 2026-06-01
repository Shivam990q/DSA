# 🏗️ Systems Thinking

> *"The whole emerges from interactions. Optimize the system, not the parts."*

---

## THE WORLDVIEW
In real engineering, the bottleneck is rarely a single algorithm — it's how components interact. Systems thinking asks: where is the constraint? what's the blast radius? what fails first?

## THE TRIGGERS
- "What's the bottleneck?"
- "What latency / throughput do we need?"
- "Where is contention / a single point of failure?"
- Production systems, distributed systems, performance work

## KEY CONCEPTS
- **Bottleneck**: the slowest component dictates overall throughput (Amdahl's law)
- **Latency vs throughput**: response time vs requests/sec
- **Tail latency**: p99 matters more than average
- **Blast radius**: how far does a failure spread?
- **Backpressure**: how does the system handle overload?

## ALGORITHMS HIDDEN IN SYSTEMS
- LRU/LFU in caches
- Consistent hashing in distributed stores
- Bloom filters to avoid disk reads
- B-trees/LSM-trees in databases
- Token bucket in rate limiters
- HyperLogLog in analytics

## THE OPTIMIZATION ORDER (production)
1. Algorithmic (Big-O class) — biggest gains
2. Data structure (right access pattern)
3. Memory layout (cache locality)
4. Parallelism (multi-core / SIMD)
5. Micro-optimizations (last resort)

## THE LITTLE'S LAW
L = λ × W (items in system = arrival rate × time in system). Foundational for capacity planning.

## EXERCISE
1. Where's the bottleneck in: client → load balancer → app server → database?
2. Why does p99 latency matter more than average for user experience?
3. How does consistent hashing minimize re-distribution when a node joins?

---

**→ Next:** [`10-Probabilistic-Thinking.md`](./10-Probabilistic-Thinking.md) | Deep dive: [`../01-LEVELS-PROGRESSION/Level-08-Algorithm-Engineering.md`](../01-LEVELS-PROGRESSION/Level-08-Algorithm-Engineering.md)
