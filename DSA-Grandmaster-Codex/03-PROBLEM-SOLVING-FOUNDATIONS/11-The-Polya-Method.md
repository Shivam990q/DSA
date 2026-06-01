# 🧙 The Polya Method — The Eternal Four Steps

> *"How to Solve It" — George Polya, 1945*  
> *(The most-influential problem-solving manual ever written.)*

---

## I. POLYA'S FOUR STEPS

In his immortal *How to Solve It*, Polya identified four phases:

### 1. **UNDERSTAND THE PROBLEM**
- What's given?
- What's asked?
- What are the constraints?
- Can you restate it in your own words?
- Can you identify the unknown? The data? The condition?

### 2. **DEVISE A PLAN**
- Have you seen a similar problem?
- Can you reformulate it?
- Can you solve a simpler version?
- Can you solve a special case?
- Can you generalize / specialize?
- What patterns / techniques apply?

### 3. **EXECUTE THE PLAN**
- Carry out each step.
- Check each step is correct.
- Can you prove it's correct?

### 4. **LOOK BACK** (the most-skipped, most-valuable step)
- Can you verify the result? On examples?
- Can you derive the result differently?
- Can you use this result for other problems?
- What did you learn?

---

## II. POLYA'S QUESTIONS — THE FULL LIST

(From *How to Solve It*, slightly modernized.)

### Step 1: Understanding
- *"What is the unknown?"*
- *"What are the data?"*
- *"What is the condition?"*
- *"Is it possible to satisfy the condition? Is the condition sufficient to determine the unknown?"*
- *"Draw a figure. Introduce suitable notation."*
- *"Separate the various parts of the condition."*

### Step 2: Devising
- *"Have you seen the problem before?"*
- *"Do you know a related problem?"*
- *"Look at the unknown — and try to think of a familiar problem with the same or similar unknown."*
- *"Could you restate the problem? Could you restate it in still another way?"*
- *"If you cannot solve the proposed problem, try to solve first some related problem. Could you imagine a more accessible related problem? A more general one? A more specific one? An analogous one?"*
- *"Could you solve a part of the problem?"*
- *"Did you use all the data? Did you use the whole condition?"*

### Step 3: Executing
- *"Can you see clearly that the step is correct?"*
- *"Can you prove that it is correct?"*

### Step 4: Looking back
- *"Can you check the result?"*
- *"Can you check the argument?"*
- *"Can you derive the result differently?"*
- *"Can you use the result, or the method, for some other problem?"*

---

## III. POLYA APPLIED TO DSA

### Example: Find the longest substring without repeating characters

#### Step 1: Understand
- Input: a string s
- Output: an integer (max length of contiguous substring with all distinct characters)
- Examples: "abcabcbb" → 3 ("abc"); "" → 0; "bbbbb" → 1 ("b")

#### Step 2: Devise
- Brute force: try every substring, check if all distinct → O(n³)
- Have I seen this? Yes — sliding window!
- Plan: maintain window [l, r] with all distinct; expand r; if duplicate, shrink l.

#### Step 3: Execute
```python
def length_of_longest(s):
    seen = {}
    l, ans = 0, 0
    for r, c in enumerate(s):
        if c in seen and seen[c] >= l:
            l = seen[c] + 1
        seen[c] = r
        ans = max(ans, r - l + 1)
    return ans
```

#### Step 4: Look back
- Verify on examples: ✓
- Alternative? Could I use last-seen index without if-check? Yes — slightly cleaner.
- Generalization? Yes — "longest substring with at most K distinct characters" — same pattern, just relax constraint.

---

## IV. THE POLYA TEMPLATES

### Template A: Specialize
Solve the problem for a *special* case first. Often the special case reveals the structure.

> "Find the maximum profit from buying and selling stock multiple times, with a 1-day cooldown."
> Special case: no cooldown → easy (just sum positive deltas).
> With cooldown: now needs DP with state (day, holding, cooldown).

### Template B: Generalize
Solve a *more general* problem; the original is a corollary.

> "Sum of subarray minimums."
> Generalize: for each element a[i], how many subarrays have a[i] as min? Use NSE/PSE.
> Sum = Σ a[i] × (count of subarrays).

### Template C: Reformulate
Restate the problem in different language.

> "Maximum weight non-overlapping intervals" → graph DP / weighted interval scheduling.

### Template D: Reduce
Convert to a known problem.

> "Most frequent element in stream" → priority queue / counter + heap.

### Template E: Reverse
Solve the inverse / dual.

> "Minimum cost to cover all points" → maximum savings / pairing optimization.

---

## V. THE LOOKING-BACK DISCIPLINE

After every problem:

### Check 1: Verify
- Re-test on all examples.
- Test on edge cases (n=0, n=1, all same, etc.)
- Stress-test against brute force.

### Check 2: Refactor
- Is the code clean?
- Could it be more elegant?
- Are variable names clear?

### Check 3: Reflect
- What's the key insight here?
- What pattern is this an instance of?
- Where else have I seen this?
- Where would I see this again?

### Check 4: Internalize
- Add to your pattern library.
- Mistake log: any sub-mistake to record?
- Star this problem if worth re-solving in 7 days.

---

## VI. THE POLYA SPIRAL

Polya's steps aren't strictly linear. You spiral:

```
Understand → Devise → Execute → Look back
    ↑                              │
    └──────────────────────────────┘ (often back to "understand")
```

If execution fails → maybe you misunderstood. Re-read. Re-plan.

---

## VII. POLYA-STYLE EXERCISES

For each problem you solve, fill out:

```
PROBLEM: 
UNDERSTAND:
  - What's given:
  - What's asked:
  - Restated:
  - Examples:
  - Edge cases:

DEVISE:
  - Similar problems:
  - Approach idea:
  - Brute force complexity:
  - Optimal complexity:

EXECUTE:
  - [code]
  - [verification]

LOOK BACK:
  - Key insight:
  - Pattern:
  - Where else useful:
  - Lessons:
```

This template is your "Polya journal." Maintain for 100 problems → permanent transformation.

---

## VIII. RECOMMENDED READING

- **George Polya, *How to Solve It*** ⭐⭐⭐ — the eternal classic; read it once a year
- **Polya, *Mathematics and Plausible Reasoning*** — the deeper sequel
- **Polya, *Mathematical Discovery*** — extended applications

---

## IX. THE FINAL TRUTH

> **"There is no problem-solving genius. There is only Polya's method, applied with discipline."**

---

**→ Next:** [`12-The-Problem-Attack-Protocol.md`](./12-The-Problem-Attack-Protocol.md)
