# 🔨 Brute Force First — The Sacred Starting Point

> *"The brute force is the foundation. Skip it, and your tower falls."*

---

## I. WHY BRUTE FORCE?

Even when you "know" the optimal, write the brute force first. Reasons:

1. **It's a baseline**: a sanity check.
2. **It's a stress-test reference**: compare against your "smart" solution.
3. **It clarifies the problem**: unambiguous statement of what to compute.
4. **It exposes structure**: reveals what's redundant → guides optimization.
5. **It catches misunderstandings**: a wrong brute force = wrong problem reading.
6. **It earns partial credit**: in contests with subtasks, brute force gets points.

---

## II. THE BRUTE FORCE TEMPLATES

### Template 1: **Try every possibility**
```python
best = -inf
for combination in all_combinations:
    if is_valid(combination):
        best = max(best, value(combination))
```

### Template 2: **Simulate exactly**
```python
state = initial_state
while not is_done(state):
    state = transition(state)
return value(state)
```

### Template 3: **Recursive enumeration**
```python
def solve(i, state):
    if i == n: return value(state)
    return max(solve(i+1, state), solve(i+1, state_with_choice(i)))
```

### Template 4: **Test every range**
```python
for i in range(n):
    for j in range(i, n):
        # check property of subarray a[i..j]
```

---

## III. THE BRUTE FORCE COMPLEXITY ANALYSIS

For each problem, ask: "What's the brute force complexity?"

| Problem               | Brute Force      | Optimal           |
|-----------------------|------------------|-------------------|
| LIS                   | O(2ⁿ)            | O(n log n)        |
| LCS                   | O(2^(n+m))       | O(nm)             |
| Subset Sum            | O(2ⁿ)            | O(n × sum)        |
| Pair Sum              | O(n²)            | O(n) (hash) / O(n log n) (sort) |
| Sorting               | O(n²)            | O(n log n)        |
| Shortest Path (unweighted) | O(V × E)    | O(V+E) (BFS)      |
| Find max subarray sum | O(n²)            | O(n) (Kadane)     |
| TSP                   | O(n!)            | O(2ⁿ × n) (bitmask DP) |
| All pairs shortest    | O(V × (V+E))     | O(V³) (Floyd) or O(VE log V) |

The leap from brute to optimal is the heart of algorithm design.

---

## IV. WHEN BRUTE FORCE IS THE ANSWER

For tiny n, brute force IS optimal. Don't over-engineer.

> n ≤ 12 → factorial brute force works (5×10⁸ ops at edge but feasible).
> n ≤ 20 → 2²⁰ subsets feasible.
> n ≤ 100, m ≤ 100 → 10⁴ ops, anything works.

**Don't write Dijkstra for n=8.** Write nested loops.

---

## V. STRESS TESTING (THE MURDER WEAPON)

After writing your "smart" solution:

```bash
# 1. Random generator (gen.cpp): produces random valid input
# 2. Brute force (brute.cpp): obviously-correct, slow
# 3. Smart solution (sol.cpp): your optimized solution
# 4. Comparator script: runs both, diffs output

# Pseudocode:
for i in 1..10000:
    ./gen > input.txt
    ./brute < input.txt > brute_out.txt
    ./sol < input.txt > sol_out.txt
    if diff brute_out.txt sol_out.txt:
        echo "MISMATCH on input.txt"
        cat input.txt; break
```

This finds 90% of bugs. Use it relentlessly.

**A real grandmaster runs stress tests by reflex.**

---

## VI. THE BRUTE FORCE SHRINKAGE

Sometimes the brute force is "obvious" and slow. The smart solution is "non-obvious" and fast. The art: shrink the brute step by step.

> Example: pair sum.
> Brute: for each i, for each j, check a[i]+a[j]=k. O(n²).
> Step 1: for each i, the j satisfying a[j]=k-a[i] is unique. So we just need to **find** it. → reduces inner to O(log n) (binary search if sorted) → O(n log n).
> Step 2: replace BS with hash → O(n).

This is **algorithmic refinement**: not a magic leap, but progressive shrinkage.

---

## VII. WHY BEGINNERS SKIP BRUTE FORCE

1. **Ego**: "It's beneath me."
2. **Time pressure**: "I'll just code the optimal."
3. **Pattern matching**: "I see this is X, here's the X solution."

**All three are mistakes.** The 2 minutes spent on brute force saves 30 minutes of debugging the optimal.

---

## VIII. THE BRUTE → OPTIMAL JOURNEY

For Two Sum:

### Brute (O(n²))
```python
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```

**Bottleneck identified**: inner loop just searches for `target - nums[i]`.

### Optimal (O(n))
```python
def two_sum(nums, target):
    seen = {}  # value → index
    for j, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], j]
        seen[x] = j
```

The journey from brute to optimal: identify what's expensive (linear search), replace with cheaper structure (hash).

---

## IX. THE FINAL TRUTH

> **"Every elegant algorithm is a brute force that learned to walk."**

---

**→ Next:** [`06-Optimization-Thinking.md`](./06-Optimization-Thinking.md)
