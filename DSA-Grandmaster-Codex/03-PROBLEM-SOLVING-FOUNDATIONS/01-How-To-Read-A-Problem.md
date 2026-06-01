# 📖 How to Read a Problem — The Forensic Discipline

> *"Most wrong solutions begin with misread problems."*

---

## I. THE THREE-READ RULE

Every problem must be read **at least three times**, with different lenses each time:

### Read 1: Skim for Story
What's the situation? What's the goal? Don't worry about details.
> "Ah, it's about a robot moving on a grid avoiding obstacles."

### Read 2: Detailed Read
Note every detail. Underline. Take notes.
> "Robot starts at (0,0). Target is (n-1, m-1). Can move right or down. Some cells are obstacles. Count paths."

### Read 3: Adversarial Read
Ask: "What could trip me up? What are weird edge cases?"
> "What if start or end is an obstacle? What about an empty grid? What if n or m is 1?"

---

## II. THE PROBLEM ANATOMY

Every well-posed problem has 6 parts. Identify each:

### 1. **Inputs** — what's given
- Variables, their types, their names
- Format of input (lines, space-separated, etc.)

### 2. **Outputs** — what's asked
- Single value? Array? Modified input?
- Format: print, return, modify in-place

### 3. **Constraints** — bounds and assumptions
- Sizes (n ≤ 10⁵)
- Value ranges (a[i] ≤ 10⁹, possibly negative)
- Special structures (sorted, distinct, non-empty)

### 4. **Examples** — concrete instances
- Small enough to verify by hand
- Cover normal + edge cases

### 5. **Time/space limits** — performance budget
- 1 second typical, 2-3 sec for hard
- 256 MB typical

### 6. **Hidden assumptions** — read carefully
- "All numbers are positive" (or are they?)
- "There's exactly one solution" (or is the answer existence?)

---

## III. THE RESTATE-IN-YOUR-WORDS TEST

After reading, **restate the problem in 1-2 sentences in your own words**.

If you can't, you don't understand it. Re-read.

> Original: *"You have an array of size n. In one operation, you can pick two adjacent elements and replace them with their sum. Repeat until the array has one element. What's the minimum total cost (sum of values created)?"*
>
> Restated: *"Greedily merge adjacent pairs to minimize total intermediate sums."*
>
> *(That restatement is wrong — it's actually a Huffman coding problem if you allow ANY pairs, but with adjacency constraint it's interval DP. Re-read!)*

---

## IV. THE EXAMPLE-VERIFICATION DRILL

For every example given:
1. **Trace the input by hand** to the expected output
2. **Identify the rule** that produces this output

If you can't trace the example to the output, you've misunderstood. Re-read.

---

## V. KEYWORDS THAT TRIGGER PATTERNS

| Keyword                                    | Likely Pattern                       |
|--------------------------------------------|--------------------------------------|
| "subarray", "contiguous"                   | Sliding window, prefix sum, Kadane   |
| "subsequence" (any order, gaps OK)         | DP                                   |
| "sorted" / "search"                        | Binary search                        |
| "minimum/maximum such that"                | Binary search on answer              |
| "shortest path"                            | BFS (unweighted) / Dijkstra (weighted) |
| "all paths" / "all combinations"           | Backtracking                         |
| "number of ways"                           | DP (counting)                        |
| "K most/least frequent/closest"            | Heap                                 |
| "pair sum"                                 | Two pointers / hash                  |
| "nested intervals" / "balance"             | Stack                                |
| "consecutive characters" / "matching"      | Stack                                |
| "next greater/smaller"                     | Monotonic stack                      |
| "median in stream"                         | Two heaps                            |
| "infinite sequence"                        | Hash for cycle detection             |
| "modulo m" / "mod 10⁹+7"                   | Modular arithmetic; combinatorics    |
| "exactly k of something"                   | Sliding window or DP                 |
| "2D grid"                                  | BFS/DFS, dynamic programming         |
| "tree" / "ancestor" / "subtree"            | DFS, tree DP, LCA                    |
| "expected value" / "probability"           | Probability DP                       |
| "n ≤ 20"                                   | Bitmask DP                           |
| "n ≤ 12"                                   | Permutation / brute force            |
| "n ≤ 40"                                   | Meet in the middle                   |
| "n ≤ 5000"                                 | O(n²) DP                             |
| "n ≤ 10⁵"                                  | O(n log n)                           |
| "n ≤ 10⁹"                                  | Binary search / math                 |

---

## VI. THE NOTE-TAKING DISCIPLINE

For every non-trivial problem, take notes (paper or whiteboard):

```
PROBLEM: [name]

INPUTS:
  n: 1 ≤ n ≤ 10^5
  arr[i]: -10^9 ≤ arr[i] ≤ 10^9

OUTPUT: integer (could be negative? could overflow?)

CONSTRAINTS:
  Time: 1s
  Memory: 256MB

EXAMPLES:
  Input: ...  Output: ...  (trace by hand)

OBSERVATIONS:
  - 
  - 

APPROACH IDEAS:
  - Brute: O(n²) — possible? 10^10 ops, NO
  - Optimize?

EDGE CASES:
  - n=1
  - All same
  - All distinct
  - Sorted / reverse-sorted
  - Empty?
```

---

## VII. THE 5-MINUTE RULE

If after 5 minutes of reading, you don't understand the problem, you have a problem-reading deficit, not a problem-solving deficit. **Slow down.**

- Re-read the original
- Examine more examples
- Search the web for similar problems' descriptions (don't read solutions — just descriptions)
- If a contest, ask in clarification (if allowed)

---

## VIII. RED FLAGS WHILE READING

🚩 You're skimming.
🚩 You're already coding.
🚩 You haven't reread the constraints.
🚩 You haven't traced an example.
🚩 You're "pretty sure" what it asks but can't restate it.
🚩 You ignored the "modulo" or "negative inputs allowed" detail.

If any flag → STOP. RE-READ.

---

## IX. THE FINAL PROTOCOL

```
1. Read 1 (skim)
2. Read 2 (detailed, take notes)
3. Read 3 (adversarial)
4. Restate in own words
5. Verify all examples by hand
6. Identify pattern keywords
7. Note constraints → algorithm class
8. Note edge cases
9. ONLY NOW start thinking about approach
```

This takes 3-7 minutes for hard problems. **Investment that returns 10×.**

---

**→ Next:** [`02-Constraint-Analysis.md`](./02-Constraint-Analysis.md)
