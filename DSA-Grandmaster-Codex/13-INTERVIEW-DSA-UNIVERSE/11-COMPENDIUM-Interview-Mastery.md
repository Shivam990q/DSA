# 💼 Interview Mastery — The Complete FAANG/MAANG Compendium

> *"Coding is half the interview. Communication is the other half."*

---

## 01 — THE FAANG PREPARATION ROADMAP

### 0-3 months out (foundations)
- Solve LC Easy → Medium consistently
- Master Top 25 patterns
- Solve [NeetCode](https://neetcode.io) 150 / Striver SDE Sheet
- Daily: 2-3 problems, weekly: 1 mock

### 3-6 months out (depth)
- LC Medium → Hard
- Company-specific tagged problems (LC Premium)
- Mock interviews 3+ per week
- System design lite

### 6-9 months out (polish)
- Behavioral story preparation (10+ stories)
- Mock interviews 5+ per week
- Specific company prep (visit company-specific resources)
- Negotiate practice ([levels.fyi](https://www.levels.fyi), Reddit)

### 9-12 months: applying
- Apply to 30+ companies in waves
- Track applications in spreadsheet
- Maintain practice momentum during interviews

---

## 02 — THE 25 INTERVIEW PATTERNS (FULL BIBLE)

| #  | Pattern                       | Trigger keywords                                    | Top 3 problems                                      |
|----|-------------------------------|------------------------------------------------------|------------------------------------------------------|
| 1  | Sliding Window                | "subarray of size k", "longest substring with..."    | LC 3, 76, 239                                        |
| 2  | Two Pointers                  | "sorted", "pair sum", "palindrome"                   | LC 11, 15, 167                                       |
| 3  | Fast & Slow Pointers          | "cycle", "midpoint", "kth from end"                  | LC 141, 142, 287                                     |
| 4  | Merge Intervals               | "intervals", "overlapping", "merge"                  | LC 56, 57, 253                                       |
| 5  | Cyclic Sort                   | "1 to n", "missing number", "duplicates"             | LC 268, 41, 442                                      |
| 6  | In-Place Reversal of Linked List | "reverse linked list", "reverse k-group"          | LC 206, 25, 92                                       |
| 7  | Tree BFS                      | "level order", "minimum depth", "right side view"    | LC 102, 103, 199                                     |
| 8  | Tree DFS                      | "all paths", "path sum", "ancestor"                  | LC 112, 113, 124                                     |
| 9  | Two Heaps                     | "median in stream", "schedule"                       | LC 295, 480, 502                                     |
| 10 | Subsets / Backtracking        | "all combinations", "all permutations"               | LC 78, 46, 22                                        |
| 11 | Modified Binary Search        | "rotated sorted", "infinite stream"                  | LC 33, 153, 154                                      |
| 12 | Bitwise XOR                   | "single number", "missing number"                    | LC 136, 137, 268                                     |
| 13 | Top K Elements                | "K most/least frequent/closest"                      | LC 215, 347, 973                                     |
| 14 | K-way Merge                   | "merge K sorted", "Kth smallest in matrix"           | LC 23, 378, 632                                      |
| 15 | 0/1 Knapsack DP               | "subset sum", "partition"                            | LC 416, 494, 698                                     |
| 16 | Unbounded Knapsack DP         | "coin change", "rod cutting"                         | LC 322, 518, 377                                     |
| 17 | Fibonacci Numbers DP          | "climbing stairs", "house robber"                    | LC 70, 198, 213                                      |
| 18 | Palindromic Subsequence DP    | "longest palindrome", "min cuts"                     | LC 5, 516, 132                                       |
| 19 | Longest Common Substring/Subseq DP | "common substring", "edit distance"             | LC 1143, 72, 583                                     |
| 20 | Topological Sort              | "schedule courses", "dependencies"                   | LC 207, 210, 269                                     |
| 21 | Dijkstra / Bellman-Ford       | "shortest path", "weighted graph"                    | LC 743, 787, 1631                                    |
| 22 | Union-Find                    | "connected components", "redundant edge"             | LC 547, 684, 947                                     |
| 23 | Minimum Spanning Tree         | "minimum cost to connect"                            | LC 1135, 1584, 1489                                  |
| 24 | Trie                          | "prefix", "autocomplete", "word search"              | LC 208, 211, 212                                     |
| 25 | Monotonic Stack/Queue         | "next greater", "max in window"                      | LC 84, 239, 496                                      |

---

## 03 — LEETCODE STRATEGY

### Tier 1: Free Lists
- **NeetCode 150** ⭐ — best free curated list
- **Blind 75** — original FAANG-prep list
- **LC Top 100 Liked**
- **LC Top Interview 150**

### Tier 2: Premium Lists
- LC company-tagged (Google, Meta, Amazon, Microsoft) — sorted by frequency in last 6 months
- LC SQL & Shell sections (data engineering roles)

### Strategy
1. Start with NeetCode 150 (cover all 25 patterns)
2. Then top 100 of your target company
3. Hard problems if you have time

### Daily ritual
- 2 problems: 1 below your level (warmup) + 1 at-or-above
- Track in spreadsheet: problem, time taken, pattern, mistakes
- Review weekly: any pattern failing repeatedly → drill

---

## 04 — INTERVIEW COMMUNICATION

### The narration structure

```
1. UNDERSTAND
   "Let me restate to make sure I understand..."
   "What if input is empty? Negative? Very large?"

2. EXPLORE
   "Can I assume sorted?"
   "Can I modify the input?"
   "What's the expected size of n?"

3. EXAMPLES
   "Let's trace through the given example..."
   "What about edge cases — n=1, all same?"

4. APPROACHES
   "Brute force would be O(n²) — for each pair check..."
   "Can we do better? If we sort first..."
   "Or with a hash map, we can do O(n)..."

5. DESIGN
   "I'll go with approach C. Here's my plan:
    - Step 1: build hash...
    - Step 2: iterate and check..."

6. CODE
   (Code while narrating each line's purpose)

7. TEST
   "Let me trace through example 1..."
   "Now edge case n=1..."
   "Now adversarial..."

8. COMPLEXITY
   "Time: O(n) since each element is processed once.
    Space: O(n) for the hash map."

9. ALTERNATIVES
   "If memory was very tight, we could sort and use two pointers
    with O(n log n) time, O(1) space."
```

### Communication don'ts
- Don't go silent for 5+ minutes
- Don't argue with the interviewer
- Don't dive into code without sharing approach
- Don't pretend to understand if you don't
- Don't be defensive about bugs

### Communication dos
- Think aloud
- Ask clarifying questions
- Acknowledge tradeoffs
- Embrace hints gracefully
- Show your reasoning even when wrong

---

## 05 — OPTIMIZATION NARRATION

When optimizing, narrate the journey:

```
"Let me start with the brute force.
For each i, we'd iterate over all j > i, that's O(n²).

The bottleneck: we're recomputing 'is there a complement' n times.
Can we trade space for time? Yes — a hash map.

Now we look up complement in O(1) → total O(n) time.
Tradeoff: O(n) extra space.
For n=10⁴, this is fine. Let me code it up."
```

This narration shows:
- Awareness of brute force
- Identification of bottleneck
- Tradeoff thinking
- Constraint awareness

These are senior-engineer signals.

---

## 06 — WHITEBOARD CODING

### Setup
- Top-left: variable definitions / assumptions
- Center: main code
- Bottom: trace examples / edge cases
- Right: time/space complexity

### Tips
- Write LARGE
- Pseudocode if uncertain; transcribe to real code last
- Use indentation rigorously
- Don't erase; cross out
- Variable names: meaningful but short

### Common whiteboard languages
- Python (most popular for clarity)
- Java (verbose but explicit)
- C++ (popular if also doing CP)

Choose ONE and stick with it for interviews.

---

## 07 — MOCK INTERVIEW SYSTEM

### Sources of mocks
- **[Pramp](https://www.pramp.com)** (free) — peer pairing
- **[interviewing.io](https://interviewing.io)** (paid; FAANG engineers)
- **Karat** (some companies use them as the interview itself)
- **Friends in industry**
- **Discord communities**

### Self-mock protocol
- Pick random LC Medium
- Set 25-min timer
- Verbalize aloud (record yourself)
- Solve as if interviewer is watching
- Watch playback; identify silence, fumbling, lack of clarity
- Score: communication, problem-solving, code quality, edge cases

### Frequency
- 2 weeks before: 5/week
- 1 week before: daily
- Day before: rest

---

## 08 — BEHAVIORAL INTEGRATION

### STAR Method
- **S**ituation: brief context
- **T**ask: your responsibility
- **A**ction: what YOU did (specific)
- **R**esult: what happened, ideally with metrics

### Amazon Leadership Principles (16, as of recent years)
Customer Obsession, Ownership, Invent and Simplify, Are Right A Lot, Learn and Be Curious, Hire and Develop the Best, Insist on the Highest Standards, Think Big, Bias for Action, Frugality, Earn Trust, Dive Deep, Have Backbone Disagree and Commit, Deliver Results, Strive to be Earth's Best Employer, Success and Scale Bring Broad Responsibility.

For Amazon: prepare 2-3 stories per LP. Don't recycle stories.

### Google "Googliness"
- Collaboration
- Comfort with ambiguity
- Bias to action
- Continuous learning

### Meta
- Move fast
- Be bold
- Build social value
- Focus on impact

### 10 universal stories to prepare
1. Most challenging technical problem
2. Conflict with teammate
3. Project failure / lesson learned
4. Project that exceeded expectations
5. Time you took initiative without being asked
6. Disagreement with your manager
7. Tight deadline with ambiguous requirements
8. Time you mentored someone
9. Technical decision with tradeoffs
10. Time you went above and beyond

### Format
- 2-3 minutes each
- Specific (not abstract)
- "I" not "we"
- Practice aloud with a timer

---

## 09 — SYSTEM DESIGN DSA BRIDGE

For senior interviews (L5+):

### Algorithms hidden in system design
- **LRU/LFU** in caches
- **Consistent hashing** in distributed cache
- **Bloom filters** in DBs (avoid false-negative disk reads)
- **Skip lists** in Redis sorted sets
- **B-trees** in DB indexes
- **LSM trees** in log-structured stores (Cassandra, RocksDB)
- **Trie** in autocomplete service
- **Min-heap** in rate limiters
- **Token bucket / leaky bucket** algorithms in rate limiters
- **HyperLogLog** in unique-counting (analytics)

### Common system design questions
1. Design URL shortener
2. Design Twitter
3. Design news feed
4. Design search autocomplete
5. Design rate limiter
6. Design key-value store
7. Design distributed cache
8. Design notification system
9. Design ride-sharing (Uber/Lyft)
10. Design messaging (WhatsApp)

For each: be ready to discuss the **DSA backbone** + **scaling/sharding**.

---

## 10 — COMPANY-SPECIFIC CHEATSHEETS

### Google
- Style: open-ended, "how would you approach..."
- Loves: graphs, design, optimization narration
- 1-2 problems per round, 45 min each
- Top 10: word ladder, search in rotated, LRU cache, LFU cache, longest palindromic substring, course schedule, regular expression matching, decode ways, coin change, find the duplicate

### Meta (Facebook)
- Style: direct, fast-paced
- Loves: trees, graphs, BFS/DFS, optimization
- 2 problems in 35 min (medium-hard)
- Top 10: subarray sum equals K, valid palindrome II, kth largest, K closest points, lowest common ancestor (LCA), serialize/deserialize binary tree, merge intervals, minimum remove to make valid parens, range sum of BST, alien dictionary

### Amazon
- Style: behavioral-heavy + DSA + system design
- Loves: trees, BFS/DFS, OOP design, leadership principles
- Top 10: number of islands, two-sum, LRU cache, copy list with random pointer, word ladder, design parking lot (OOD), trapping rain water, course schedule, group anagrams, top K frequent

### Microsoft
- Style: balanced, classical
- Loves: linked lists, trees, dp
- Top 10: reverse linked list, valid parentheses, balanced binary tree, max depth, palindrome partitioning, climbing stairs, set matrix zeroes, intersection of two linked lists, copy list with random pointer, lowest common ancestor

### Apple
- Style: closer to design + iOS-specific (some)
- Loves: graphs, design patterns, optimization
- Top 10: LRU cache, two-sum, valid palindrome, longest palindrome, design hit counter, group anagrams, longest substring without repeating, merge intervals, word search, reverse string

### Indian unicorns (Razorpay, Paytm, Flipkart, etc.)
- Style: similar to FAANG L4
- Top: pattern-based mediums + 1-2 hards
- Behavioral: light to moderate
- System design: lite for SDE-2

---

## 11 — NEGOTIATION (BONUS)

After getting an offer:

1. **Don't accept on the spot.** Always ask for time (1-2 weeks).
2. **Get competing offers** if possible (Levels.fyi, [Glassdoor](https://www.glassdoor.com) for ranges).
3. **Negotiate**: total comp, sign-on, equity, vacation, start date.
4. **Use specific numbers**: "I was hoping for $X total" not "more."
5. **Be polite, never threatening**: it's a negotiation, not a fight.
6. **Get the final offer in writing.**

Resources: levels.fyi, Reddit r/cscareerquestions, "Salary Negotiation: Make More Money, Be More Valued" by Patrick McKenzie.

---

## 12 — DAY-OF-INTERVIEW CHECKLIST

```
24h before:
☐ Solid sleep (8+ hours)
☐ Light review of your strongest topics
☐ Prep questions to ASK them (1-2 per round)

2h before:
☐ Eat well; hydrate
☐ Test camera/mic/screen-share
☐ Quiet room; lighting good

30 min before:
☐ Bathroom break
☐ Pen + paper ready
☐ Water bottle
☐ Loose, calm; deep breaths

During:
☐ Smile (visible energy)
☐ Restate problem
☐ Communicate continuously
☐ Test before submitting
☐ Ask thoughtful questions

After:
☐ Thank you email within 24h (optional but classy)
☐ Note what went well & what didn't
☐ Move on (don't ruminate)
```

---

## 13 — PSYCHOLOGY & MINDSET

- **One bad interview ≠ failure.** Companies vary; interviewers vary.
- **Don't compare yourself to others' offers.** Your path is yours.
- **Each rejection is data.** Note what to improve.
- **Most engineers fail FAANG interviews multiple times before passing.** Persistence wins.
- **Imposter syndrome is universal.** Even L7s feel it.

---

## 14 — RECOMMENDED READING

- **Cracking the Coding Interview** (McDowell)
- **Elements of Programming Interviews** (Aziz)
- **System Design Interview** (Alex Xu) Vol 1 & 2
- **The [Tech Interview Handbook](https://www.techinterviewhandbook.org)** (free online)
- **Designing Data-Intensive Applications** (Kleppmann) — for senior interviews

---

**→ Next:** [`../14-ALGORITHM-DESIGN-SCIENCE/`](../14-ALGORITHM-DESIGN-SCIENCE/)
