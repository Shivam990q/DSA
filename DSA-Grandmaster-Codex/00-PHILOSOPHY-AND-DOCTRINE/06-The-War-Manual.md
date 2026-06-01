# 🗡️ The War Manual — Sun Tzu for Problem Solvers

> *"The supreme art of war is to subdue the problem without solving it the obvious way."*  
> — Adapted from Sun Tzu

---

## I. KNOW THY PROBLEM, KNOW THYSELF

Sun Tzu: *"If you know the enemy and know yourself, you need not fear the result of a hundred battles."*

In algorithmic warfare:

| Knowing the Problem                       | Knowing Yourself                                  |
|-------------------------------------------|---------------------------------------------------|
| Constraints (n, time limit, memory)       | Your strongest topic                              |
| Special structure (sorted? distinct?)     | Your weakest topic                                |
| Pattern category                          | Your average solving time                          |
| Edge cases                                | Your typical bug categories                       |
| Brute force complexity                    | Your contest endurance                            |

A grandmaster never enters a problem blind. **Reconnaissance comes before assault.**

---

## II. THE FIVE FACTORS OF VICTORY

Sun Tzu identified five constants of war. Translated:

### 1. **The Way** (Doctrine)
Your daily training discipline. The deeper your foundation, the higher you can build.

### 2. **Heaven** (Timing)
When you attempt — fresh morning vs exhausted midnight. Energy dictates output.

### 3. **Earth** (Terrain)
Your environment. Quiet desk, fast internet, working keyboard. Friction kills focus.

### 4. **The Commander** (Skill)
Your accumulated patterns, theorems, and intuition.

### 5. **Method and Discipline** (Process)
Your problem-attack protocol. Read → understand → brute → optimize → test → submit.

**Win the five, win the war.**

---

## III. THE ART OF DECEPTION (Problem-Setter's Tactics)

Problem setters disguise problems. Common deceptions:

### Deception 1: **The Story Trap**
A problem about "rabbits jumping" is actually graph traversal. Don't be seduced by the narrative.
> **Cure**: Always restate in mathematical terms.

### Deception 2: **The Constraint Disguise**
n ≤ 10⁵ but a different parameter is small. Maybe k ≤ 20 → bitmask DP hidden.
> **Cure**: Look at *all* constraints, not just n.

### Deception 3: **The Reversal**
"Find the maximum X such that Y holds" — actually a binary search on X with feasibility check.
> **Cure**: When you see "maximum/minimum such that," think binary search.

### Deception 4: **The Complement**
Counting "ways NOT to do X" might be easier than "ways to do X."
> **Cure**: Always consider the complement.

### Deception 5: **The Aggregate**
Looks like need to compute for each i; but maybe sum over i has nice closed form.
> **Cure**: Think in terms of contribution, not iteration.

### Deception 6: **The Reformulation**
"Find subarray with property X" might transform via prefix sums into a 2-element problem.
> **Cure**: Always ask: "What transformation makes this trivial?"

### Deception 7: **The Random Trap**
A problem screaming "DP!" might have a randomized O(1) solution.
> **Cure**: Don't anchor on first impressions.

---

## IV. THE FIVE WAYS TO ATTACK A NEW PROBLEM

### Attack 1: **The Direct Assault** (Brute Force First)
Always derive the dumb O(n²) or O(n!) solution. It's your baseline AND your stress-test reference.

### Attack 2: **The Flank** (Symmetry/Reformulation)
Look at the problem from a different angle. Swap rows/columns. Consider the reverse. Examine the dual.

### Attack 3: **The Siege** (Decomposition)
Break into subproblems. Solve subproblems independently. Compose.

### Attack 4: **The Ambush** (Pattern Recognition)
"Wait — this is just LIS in disguise." Pattern matching saves hours.

### Attack 5: **The Scorched Earth** (Try Everything)
When stuck: brute force, pattern, math, randomized, observation, complement, sweep, two pointers, monotonic stack, binary search, DP states, graph model, geometric interpretation. **Cycle through your weapons until one fits.**

---

## V. THE OODA LOOP FOR PROBLEM SOLVING

Boyd's military OODA loop, adapted:

```
OBSERVE → ORIENT → DECIDE → ACT
   ↑                          │
   └──────────────────────────┘
```

### OBSERVE
Read the problem. Note constraints. Spot keywords ("subarray", "modulo", "minimum number of operations").

### ORIENT
What is the structure? Sorted? Tree? Graph? Independent? What pattern category?

### DECIDE
Pick an approach. Write the brute force first. Then plan optimization.

### ACT
Code. Test. Submit. If WA → loop back to OBSERVE with new information.

**The grandmaster's OODA loop is faster.** That's the entire game.

---

## VI. THE 36 STRATAGEMS (Selected for DSA)

Adapted from the Chinese classic:

| Stratagem                              | DSA Application                                                |
|----------------------------------------|----------------------------------------------------------------|
| **"Cross the sea by deceiving heaven"**| Hide expensive ops in lazy propagation                         |
| **"Besiege Wei to rescue Zhao"**       | Solve the dual problem instead of the original                 |
| **"Kill with a borrowed knife"**       | Use an existing data structure (segtree, BIT) for new purpose  |
| **"Wait at leisure for the exhausted"**| Precompute answers; query in O(1)                              |
| **"Loot a burning house"**             | Sort offline queries to batch-process                          |
| **"Make a sound in the east, attack in west"** | Solve a "harder" version that's actually easier        |
| **"Create something out of nothing"**  | Add dummy sentinels to simplify edge cases                     |
| **"Cross the path secretly"**          | Coordinate compression — work in compressed space              |
| **"Watch fires across the river"**     | Brute force smaller cases, observe pattern, generalize         |
| **"Hide a knife behind a smile"**      | Greedy that LOOKS suboptimal but is provably optimal           |
| **"Replace beams with rotten timbers"**| Replace heavy data structure with simpler one when possible    |
| **"Borrow a corpse to resurrect the soul"** | Old algorithm, new application (e.g., FFT for substring count) |

---

## VII. THE FIVE SINS OF GENERALSHIP (Sun Tzu)

A general who has these five faults loses. Translated:

### 1. **Recklessness** — leads to destruction
Coding without thinking. Submitting without testing.

### 2. **Cowardice** — leads to capture
Avoiding hard problems. Skipping the topic that scares you.

### 3. **Hasty temper** — provoked by insults
Rage-coding after WA. Fix bugs calmly.

### 4. **Delicacy of honor** — sensitive to shame
"I should know this" → not asking for help / reading editorial.

### 5. **Over-solicitude for his men** — exposed to worry
Over-helping juniors when you should be training. (For senior CPers.)

---

## VIII. THE WAR ROOM (Your Setup)

```
┌─────────────────────────────────────────────────────┐
│  WAR ROOM CHECKLIST                                 │
├─────────────────────────────────────────────────────┤
│  ✓ Quiet space, no notifications                    │
│  ✓ Pen and paper for problem-solving                │
│  ✓ Editor + compiler + debugger ready               │
│  ✓ Templates folder open                            │
│  ✓ CP-Algorithms / CP4 / cheatsheet bookmarked      │
│  ✓ Stress-test setup ready (gen.cpp, brute.cpp)     │
│  ✓ Timer (for timeboxing)                           │
│  ✓ Mistake log open                                 │
│  ✓ Water, snack, posture good                       │
│  ✓ Phone in another room                            │
└─────────────────────────────────────────────────────┘
```

---

## IX. CONTEST WARFARE

A 2.5-hour [Codeforces](https://codeforces.com) round is a battle. Treat it as such:

```
Minute 0-3:    Read ALL problems. Sort by mental ease.
Minute 3-30:   Solve A, B (the easy ones, gain blood).
Minute 30-60:  C — usually the differentiator. Spend deeply.
Minute 60-90:  D — apply your pattern library.
Minute 90-120: E/F — only if you've cleared the rest.
Minute 120+:   Verify all submissions. Stress-test if time.
```

**Never** lock into a problem for >40 min without progress. Switch problems. Return later.

---

## X. THE FINAL WAR MAXIM

> *"Victorious warriors win first and then go to war.  
> Defeated warriors go to war first and then seek to win."*  
> — Sun Tzu

Translation: **You win contests in the months of practice before, not in the contest itself.**

---

**→ Next:** [`07-The-Geeta-of-Problem-Solving.md`](./07-The-Geeta-of-Problem-Solving.md)
