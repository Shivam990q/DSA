# 🚀 Optimization Narration

> *"Show the journey from brute force to optimal. That journey IS the senior-engineer signal."*

---

## I. WHY NARRATE THE OPTIMIZATION
Jumping straight to the optimal solution looks like memorization. Walking from brute force → optimal demonstrates genuine problem-solving — exactly what interviewers want to see.

---

## II. THE NARRATION ARC
```
"Let me start with the brute force.
 For each i, I'd check all j > i — that's O(n²).

 The bottleneck: I'm repeatedly searching for the complement.
 Can I trade space for time? A hash map gives O(1) lookup.

 Now it's O(n) time, O(n) space.
 For n = 10⁴, that's fine. Let me code it."
```

This shows:
- Awareness of brute force (baseline)
- Identification of the bottleneck
- Tradeoff reasoning (space vs time)
- Constraint awareness

---

## III. THE OPTIMIZATION VOCABULARY
Phrases that signal seniority:
- "The bottleneck here is..."
- "We're recomputing X, so let's cache it..."
- "This is monotonic, so binary search applies..."
- "We can trade O(n) space for O(n) → O(1) time on lookups..."
- "The amortized cost is..."
- "For the given constraints, O(n log n) suffices..."

---

## IV. THE TRADEOFF DISCUSSION
Always mention tradeoffs:
- Time vs space
- Simplicity vs performance
- Preprocessing cost vs query cost
- Worst-case vs average-case

> "I could sort for O(n log n) time and O(1) extra space, OR use a hash for O(n) time and O(n) space. Given the constraints, I'll prefer..."

---

## V. CONSTRAINT-DRIVEN OPTIMIZATION
Tie your optimization to constraints:
- "n is up to 10⁵, so O(n²) won't pass. I need O(n log n) or better."
- "n is only 20, so an exponential bitmask DP is fine."

This shows you read constraints (a junior tell when ignored).

---

## VI. WHEN BRUTE FORCE IS ENOUGH
Sometimes the brute force passes. Say so:
> "n is at most 100, so even O(n³) is only 10⁶ ops — the brute force is acceptable. Let me code that cleanly rather than over-engineer."

Knowing when NOT to optimize is also a senior signal.

---

## VII. PRACTICE
For each problem, explicitly narrate:
1. Brute force + complexity
2. The bottleneck
3. The optimization + new complexity
4. The tradeoff

Record yourself. The arc should be smooth and natural.

---

**→ Next:** [`06-Whiteboard-Coding.md`](./06-Whiteboard-Coding.md)
