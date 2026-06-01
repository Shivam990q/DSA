# 🌌 Advanced Paradigms Compendium

---

## 01 — RANDOMIZED ALGORITHMS

### Las Vegas vs Monte Carlo
- **Las Vegas**: always correct, expected runtime probabilistic (e.g., randomized quicksort)
- **Monte Carlo**: bounded runtime, may give wrong answer with small probability (e.g., Miller-Rabin)

### Famous algorithms
1. **Randomized quicksort** — pivot at random; O(n log n) expected, O(n²) worst (rare)
2. **Treap** — random priorities → expected O(log n) operations
3. **Skip list** — random level promotion
4. **Miller-Rabin primality** — Monte Carlo
5. **Karger's min cut** — Monte Carlo, O(V²) per trial; success probability 1/C(V,2)
6. **Reservoir sampling** — uniform random sample from stream
7. **Bloom filter** — false positive only, never false negative
8. **Locality-sensitive hashing** — sublinear nearest neighbors
9. **Randomized incremental construction** — geometry (Voronoi, etc.)
10. **Polynomial identity testing** — Schwartz-Zippel

### Probabilistic analysis
- Use linearity of expectation for sum-of-indicator analyses
- Markov's inequality: P(X ≥ a) ≤ E[X] / a
- Chebyshev's: P(|X − μ| ≥ kσ) ≤ 1/k²
- Chernoff bounds for sums of independent random variables

---

## 02 — APPROXIMATION ALGORITHMS

### Vertex cover (2-approximation)
Greedy: pick any edge; add both endpoints to cover; remove both.

### TSP (metric, 2-approximation via MST)
1. Compute MST.
2. DFS the MST; record visit order.
3. Output Hamiltonian via shortcuts.

### TSP (Christofides 1.5-approximation, metric)
1. Compute MST.
2. Find odd-degree vertices.
3. Compute minimum-weight perfect matching on those.
4. Combine MST + matching → Eulerian.
5. Shortcut.

### Set cover (greedy O(log n))
At each step, pick the set covering the most uncovered elements.

### Knapsack FPTAS
ε-approximation in time poly(n, 1/ε).

### Max-Cut (0.878 via SDP — Goemans-Williamson)

---

## 03 — ONLINE ALGORITHMS

### Competitive ratio
A's cost / OPT's cost ≤ c (with hindsight).

### Famous online problems
- **Paging / page replacement**: LRU is k-competitive (k = cache size); FIFO same; LFU not competitive.
- **List update**: Move-to-front is 2-competitive.
- **Ski rental**: Buy-after-day-k is 2-competitive.
- **Online bipartite matching**: Karp-Vazirani-Vazirani 1-1/e ≈ 0.632.
- **Online scheduling**: various ratios.

---

## 04 — STREAMING ALGORITHMS

### Reservoir sampling (k samples from stream of unknown size)
```cpp
vector<int> reservoir(int k) {
    vector<int> R(k);
    int i = 0, x;
    while (cin >> x) {
        if (i < k) R[i] = x;
        else { int j = rand() % (i + 1); if (j < k) R[j] = x; }
        i++;
    }
    return R;
}
```

### Misra-Gries (top-k frequent)
Bounded memory candidates; for each item, increment its counter or decrement all and evict zeros.

### Count-Min Sketch
d hash functions × w columns. Insert: increment all d cells. Query: min of d cells. Error: ≤ ε · n with probability 1 − δ.

### HyperLogLog
- Hash each item; track max trailing-zero count
- Use multiple "buckets" (registers), harmonic mean
- ~2% error with 12-16 KB for billions of items

### Sliding window aggregates
For "sum/min/max over last k items": use deque + circular buffer.

---

## 05 — PARALLEL ALGORITHMS

### Work-span model
- **Work** T₁: total operations
- **Span** T_∞: longest dependency chain
- Speedup with p processors: T_p ≥ T₁/p, T_p ≥ T_∞

### Parallel reduce (sum of n elements)
- Tree-style reduction: O(n) work, O(log n) span
- p processors: O(n/p + log n) time

### Parallel scan / prefix sum
- Hillis-Steele: O(n log n) work, O(log n) span
- Blelloch: O(n) work, O(log n) span (better!)

### Parallel sort
- Bitonic sort: O(n log²n) work, O(log²n) span — GPU-friendly
- Sample sort: distributed-friendly
- Radix sort: well-parallelizable

### MapReduce
Functional model: map (parallel transform) + reduce (parallel aggregate). Used for big data.

---

## 06 — DISTRIBUTED ALGORITHMS

### Consensus
Multiple nodes agree on a value despite failures.

#### Paxos
- Phase 1 (prepare): proposer sends prepare(N); acceptors promise not to accept lower N
- Phase 2 (accept): proposer sends accept(N, value); acceptors confirm
- Tolerates F failures with 2F+1 nodes

#### Raft
Simpler consensus. Leader-based. Three states: leader, follower, candidate.
- Leader election via timeouts
- Log replication
- Safety via term numbers

### Gossip protocols
Each node periodically sends state to a random subset. Eventually consistent.

### Vector clocks
Each node maintains vector of counters. Compare for "happens-before" relationship.

### Lamport timestamps
Single counter per node. Provides total order (not partial).

### Two-phase commit (2PC)
Coordinator + participants. Phase 1: prepare. Phase 2: commit/abort. Blocks on coordinator failure.

### Three-phase commit (3PC)
Adds pre-commit phase. Non-blocking but assumes synchronous network.

### CAP theorem
Cannot simultaneously have:
- **Consistency** (all nodes see same data)
- **Availability** (every request gets a response)
- **Partition tolerance** (works under network partitions)

In practice: CP (e.g., HBase) or AP (e.g., Cassandra). CA only without partitions.

### CRDTs (Conflict-free Replicated Data Types)
Data structures that converge across replicas without coordination.
- G-Counter (grow-only)
- PN-Counter (positive-negative)
- LWW-Set (last-write-wins)
- OR-Set (observed-remove)

---

## 07 — QUANTUM ALGORITHMS (Intro)

### Quantum bits (qubits)
- Classical: 0 or 1
- Quantum: superposition α|0⟩ + β|1⟩, |α|² + |β|² = 1

### Famous quantum algorithms
- **Grover's search**: O(√n) for unstructured search (vs O(n) classical)
- **Shor's factoring**: polynomial-time factoring (vs exp classical) — breaks RSA
- **Quantum Fourier Transform**: foundation for many algorithms
- **HHL**: linear systems
- **Quantum walks**: search on graphs

### Where we are (2026)
- ~1000 noisy qubits in best machines (IBM, Google, IonQ)
- Below "quantum supremacy" threshold for general problems
- Niche advantages in specific simulations
- Practical RSA-breaking still distant (need 4000+ logical qubits)

---

## 08 — RECOMMENDED READING

- **Motwani & Raghavan**, *Randomized Algorithms* ⭐
- **Williamson & Shmoys**, *The Design of Approximation Algorithms* ⭐
- **Borodin & El-Yaniv**, *Online Computation and Competitive Analysis*
- **Muthukrishnan**, *Data Streams: Algorithms and Applications*
- **Lynch**, *Distributed Algorithms*
- **Nielsen & Chuang**, *Quantum Computation and Quantum Information*

---

**→ Next universe:** [`../12-COMPETITIVE-PROGRAMMING-UNIVERSE/00-Index.md`](../12-COMPETITIVE-PROGRAMMING-UNIVERSE/00-Index.md)
