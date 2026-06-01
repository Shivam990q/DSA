# ⚔️ The Problem Attack Protocol

> *"In contest, you don't get a second chance. The protocol is your mind's army."*

---

## I. THE FULL PROTOCOL

For any problem (interview, contest, real life), execute in this exact order:

### Phase 1: **READ & UNDERSTAND** (3-7 min)
1. Read the problem 3 times (skim → detail → adversarial).
2. Note: input format, output format, constraints, time/memory limits.
3. Trace examples by hand.
4. **Restate the problem in your own 1-2 sentences.**

### Phase 2: **CLASSIFY** (1-2 min)
5. From constraints, infer the **algorithm class** (table in `02-Constraint-Analysis.md`).
6. Note the **keywords** that suggest patterns (`04-Pattern-Recognition.md`).
7. Identify whether it's: search, count, decide, construct, optimize.

### Phase 3: **OBSERVE & EXPLORE** (5-15 min for hard problems)
8. Compute small cases by hand if pattern unclear.
9. Look for invariants, monotonicity, symmetries (`08-Invariant-Discovery.md`).
10. Form hypotheses; test on examples.

### Phase 4: **DESIGN** (5-15 min)
11. Write the **brute force** — at least mentally; possibly literally.
12. Identify the bottleneck.
13. Design the optimization (or recognize a pattern).
14. Sketch the algorithm in pseudocode.
15. Verify time/space complexity fits the constraints.

### Phase 5: **PROVE (informally)** (2-5 min)
16. Convince yourself of correctness in 2-3 sentences.
17. If you can't, find a counterexample or rethink.

### Phase 6: **CODE** (10-30 min depending)
18. Write clean, modular code.
19. Use meaningful variable names.
20. Handle edge cases EXPLICITLY (n=0, n=1, all same, etc.).

### Phase 7: **TEST** (3-10 min)
21. Walk through provided examples mentally.
22. Test edge cases: n=0, n=1, all same, max constraints.
23. If unsure: **stress-test** against brute force.

### Phase 8: **SUBMIT** (1 min)
24. Verify input format matches expected.
25. Submit confidently.

### Phase 9: **POST-MORTEM** (5 min)
26. Wrong answer? Read editorial. Find the missing case/insight.
27. Right answer? Note the pattern. Update mistake log.
28. Mark for review in 7 days if hard.

---

## II. TIME ALLOCATION

For a 90-minute interview problem:
- Phase 1-3: 10 min (don't rush!)
- Phase 4-5: 15 min
- Phase 6: 30 min
- Phase 7: 10 min
- Phase 8-9: 5 min
- Buffer: 20 min

For a 30-minute [LeetCode](https://leetcode.com) Medium:
- Phase 1-3: 3-5 min
- Phase 4: 3-5 min
- Phase 6: 10-15 min
- Phase 7-8: 3-5 min

For a 2.5-hour CF round (5 problems):
- Per problem: 25-30 min target; less for easy, more for hard.

---

## III. THE RED LIGHTS

Stop and reassess if you find:

🚩 **>10 min of "I don't know what to do"** → re-read; try smaller examples; switch problems.

🚩 **Halfway through code, can't articulate the algorithm** → STOP. Step back. Plan in pseudocode.

🚩 **Multiple bugs / WA on submit** → STOP coding more. Read code line by line. Add debug prints.

🚩 **You're "almost done" for 30 min** → you might be in a tar pit. Switch problems if contest; redesign if not.

🚩 **Your solution feels too simple** → is it correct? Re-verify on adversarial cases.

🚩 **Your solution feels too complex** → is there a simpler observation you're missing?

---

## IV. SWITCHING PROBLEMS (CONTEST DISCIPLINE)

In contests, **never** sink-cost-fallacy. If 30 min into problem D you have nothing, switch to E.

**Rule of thumb**: if 40 min in with no breakthrough, switch. Return after solving easier problems.

The problem doesn't owe you a solution. Move on.

---

## V. DEBUG PROTOCOL (if WA)

When wrong-answer:

### Step 1: Re-read the problem
50% of WA bugs are misread problems. Re-read.

### Step 2: Re-examine examples
Trace your code on each provided example.

### Step 3: Add prints / debugger
Print intermediate values. Find the first wrong one.

### Step 4: Edge cases
Try n=0, n=1, all same, sorted, reverse-sorted, max value.

### Step 5: Stress test
Random gen + brute + diff. Find a small failing case.

### Step 6: Re-analyze
Maybe the algorithm is wrong, not just the implementation.

### Step 7: Hot reset
Clear your code. Re-implement from scratch. Often faster than debugging.

---

## VI. THE PROBLEM-ATTACK CHEAT-SHEET (for under desk)

```
┌─────────────────────────────────────────────────────────┐
│ PROBLEM ATTACK PROTOCOL                                 │
├─────────────────────────────────────────────────────────┤
│ 1. READ 3× (skim, detail, adversarial)                  │
│ 2. RESTATE in own words                                 │
│ 3. CLASSIFY: constraints → algo class                   │
│ 4. KEYWORDS → pattern category                          │
│ 5. SMALL EXAMPLES if stuck                              │
│ 6. INVARIANTS, MONOTONICITY                             │
│ 7. BRUTE FORCE first                                    │
│ 8. BOTTLENECK identification                            │
│ 9. OPTIMIZATION                                         │
│ 10. PROOF (2-3 sentences)                               │
│ 11. CODE clean                                          │
│ 12. EDGE CASES (n=0, n=1, all same)                     │
│ 13. STRESS TEST if uncertain                            │
│ 14. SUBMIT                                              │
└─────────────────────────────────────────────────────────┘
```

Print this. Tape to your monitor. Use until reflexive.

---

## VII. EXAMPLES OF THE PROTOCOL IN ACTION

### Easy: LC 1 — Two Sum
1. **Read**: array, target. Return two indices summing to target. Constraints: n ≤ 10⁴, exactly one solution.
2. **Restate**: find i, j s.t. a[i] + a[j] = target.
3. **Classify**: n=10⁴, O(n) or O(n log n) feasible.
4. **Keywords**: "pair sum" → hash map.
5. **Brute**: O(n²) double loop.
6. **Bottleneck**: inner loop searches for `target - a[i]`.
7. **Optimization**: hash map seen value → index.
8. **Proof**: as I iterate, check if complement was seen.
9. **Code**: 8 lines.
10. **Edge**: tested on examples; n=2 minimum case ok.
11. **Submit**.

Total: 5 minutes.

### Hard: LC 84 — Largest Rectangle in Histogram
1. **Read**: array of bar heights, find max rectangle area in histogram.
2. **Restate**: for each rect from indices l to r with height = min(a[l..r]), maximize width × height.
3. **Classify**: n=10⁵, need O(n) or O(n log n).
4. **Keywords**: "rectangle in histogram" → CLASSIC monotonic stack.
5. **Brute**: O(n²) — for each i, expand left/right while ≥ a[i].
6. **Bottleneck**: re-finding "first smaller to left/right" repeatedly.
7. **Optimization**: monotonic stack — for each bar, find PSE and NSE in O(n) total.
8. **Proof**: each bar pushed/popped once; computes its rectangle when popped.
9. **Code**: 20 lines.
10. **Edge**: empty array, single bar, all same heights.
11. **Submit**.

Total: 15-20 minutes.

---

## VIII. THE FINAL TRUTH

> **"Talent is what you do under pressure when no protocol guides you.  
>  Protocol is what makes talent appear in everyone."**

Master this protocol. It's the difference between contestants and grandmasters.

---

**→ Next universe:** [`../04-DATA-STRUCTURES-UNIVERSE/00-Index.md`](../04-DATA-STRUCTURES-UNIVERSE/00-Index.md)
