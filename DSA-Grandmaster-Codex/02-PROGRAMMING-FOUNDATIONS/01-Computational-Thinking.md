# 🧠 Computational Thinking

> *"Computational thinking is the mental discipline of formulating problems and their solutions so that the solutions can be effectively carried out by an information-processing agent."*  
> — Jeannette Wing, *Computational Thinking*, CACM 2006

---

## I. THE FOUR PILLARS OF COMPUTATIONAL THINKING

### 1. **Decomposition**
Break a complex problem into smaller, manageable parts.

> Example: "Build a Twitter clone" → User auth + Tweet storage + Feed generation + Search + Notifications. Each becomes its own subproblem.

### 2. **Pattern Recognition**
Identify similarities across problems and reuse strategies.

> Example: Recognizing that Word Ladder is BFS, that LIS uses DP, that array shifting is a circular buffer.

### 3. **Abstraction**
Strip away non-essential detail. Work with the *essence*.

> Example: When solving graph problems, you don't care if the nodes are people, cities, or atoms. You care about the *relations*.

### 4. **Algorithm Design**
Develop step-by-step solutions that always work for the problem class.

> Example: A sorting algorithm must work for *any* array, not just the example one.

---

## II. THE MIND OF A COMPUTER

To program well, you must think like a computer:

1. **Sequential** — instructions execute one at a time (mostly).
2. **Mechanical** — no understanding, only rules.
3. **Memory-bound** — every value lives somewhere; storage costs.
4. **Time-bound** — every operation costs cycles.
5. **Deterministic** — same input → same output (assuming no randomness).
6. **Bounded** — finite memory, finite registers, finite stack.

**Implication**: When you think about your code, simulate the machine. Trace the variables. Visualize the memory.

---

## III. THE ALGORITHMIC MINDSET

Five lenses to apply to any problem:

### Lens 1: **Input → Process → Output**
What goes in? What comes out? What's the transformation?

### Lens 2: **State → Transition**
What state defines the system? What changes the state?

### Lens 3: **Search → Decision**
Are we exploring possibilities, or evaluating one?

### Lens 4: **Construction → Verification**
Are we building the answer, or checking a candidate?

### Lens 5: **Discrete → Continuous**
Are we counting cases, or working with real numbers?

Each problem has dominant lenses. Learn to identify them quickly.

---

## IV. THE PROBLEM TRANSLATION HIERARCHY

```
NATURAL LANGUAGE
  ↓ (formalize)
MATHEMATICAL SPECIFICATION
  ↓ (algorithmic)
ALGORITHM (pseudocode)
  ↓ (implement)
PROGRAM (real code)
  ↓ (execute)
COMPUTATION (machine output)
```

Most beginners fail at the *first* arrow: translating English into math. Practice this:

> *"Find the maximum profit you can make by buying and selling a stock once."*  
> → *"Given array a, maximize a[j] - a[i] subject to i < j."*  
> → *"Maintain min-so-far. For each j, update answer with a[j] - min."*  
> → *Code in 5 lines.*

---

## V. ESSENTIAL HABITS

### Habit 1: **Trace Before You Type**
Before writing code, trace by hand on a small example. Many bugs die before birth.

### Habit 2: **Name Things Precisely**
`i`, `j`, `temp` are sometimes acceptable. `idx`, `count`, `prefixSum` are better. `shortestPathFromSourceToK` is best.

### Habit 3: **One Thing per Function**
A function that does one thing is testable, debuggable, reusable. A function that does five things is a tar pit.

### Habit 4: **Embrace Edge Cases**
n=0. n=1. Negative inputs. Empty containers. Maximum inputs. Always test.

### Habit 5: **Read Before You Write**
Before modifying code, *read* it. Understand what's there. Then change.

### Habit 6: **Trust the Recursion**
When writing recursion, write the recursive call as if it works. Don't trace too deep. Trust the contract.

---

## VI. THE COMPUTATIONAL UNCONSCIOUS

After enough practice, computational thinking happens *automatically*:
- You see a problem and immediately ask, "What's the input domain?"
- You hear "find such that maximum" and your mind whispers "binary search?"
- You see "subarray sum" and "prefix sums" lights up.
- You see "n ≤ 20" and bitmask DP rings.

This is what we're training. Not memorization. **Algorithmic instinct.**

---

## VII. EXERCISE: TRANSLATE ENGLISH → MATH

For each, write a 1-line mathematical specification:

1. "Find the longest substring without repeating characters."
2. "Given a tree, find the sum of all path sums between leaves."
3. "How many ways to climb n stairs taking 1 or 2 steps?"
4. "Find the median element in a sliding window of size k."
5. "Given m triangles in 2D, find total covered area."

### Sample answers (try first, then check)
1. Maximize `(j − i + 1)` over all `i ≤ j` such that `s[i..j]` has all distinct characters.
2. Compute `Σ dist(u, v)` over all leaf pairs `(u, v)`, where `dist` is the number of edges on the unique path between them.
3. Find `f(n)` where `f(n) = f(n−1) + f(n−2)`, `f(0) = f(1) = 1` (the Fibonacci recurrence).
4. For each window `W = a[t .. t+k−1]`, output the order statistic of rank `⌈k/2⌉` of `W`.
5. Compute `|⋃ Tᵢ|` (area of the union of the `m` triangle regions), handling overlaps via inclusion-exclusion or a sweep line.

---

## VIII. RECOMMENDED READING

- **Wing, "Computational Thinking"** (CACM 2006) — the seminal essay
- **Polya, "How to Solve It"** ⭐ — the eternal classic
- **Spraul, "Think Like a Programmer"** — gentle for beginners
- **Felleisen et al., "How to Design Programs"** — rigorous design

---

**→ Next:** [`02-Memory-Models.md`](./02-Memory-Models.md)
