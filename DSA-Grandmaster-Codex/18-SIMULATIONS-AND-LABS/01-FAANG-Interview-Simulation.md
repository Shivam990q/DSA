# 🎬 FAANG Interview Simulation Lab

> *"You don't rise to the level of your ambition. You fall to the level of your training."*

---

## I. THE FORMAT

A FAANG L4-L5 onsite typically:
- **5 rounds** (4 technical + 1 behavioral)
- **45-50 min each**
- 1-2 problems per technical round
- 1 system design at L5+

---

## II. THE 5-ROUND SIMULATION (FULL DAY)

### Round 1: Coding — DSA Easy/Medium (45 min)
- 1 medium problem
- Communicate throughout
- Test edge cases
- Optimize after first solution

### Round 2: Coding — DSA Medium/Hard (45 min)
- 1 hard or 2 mediums
- Heavy emphasis on optimization

### Round 3: System Design (45 min) — L5+
- "Design X..." (URL shortener, news feed, etc.)
- Discuss: requirements, capacity estimation, high-level design, deep-dive components, tradeoffs

### Round 4: Coding — Patterns (45 min)
- Often a problem in your specialty
- Pattern recognition speed test

### Round 5: Behavioral (45 min)
- 5-7 STAR stories
- Tailored to company values (Amazon LP, Google "Googliness")

---

## III. SIMULATION SETUP

### What you need
- Quiet room, 5 hours
- Excalidraw / online whiteboard (for system design)
- Code editor without autocomplete (for whiteboard sim)
- Webcam recording (review yourself later)
- Timer
- Mock interviewer (peer / [Pramp](https://www.pramp.com) / [interviewing.io](https://interviewing.io)) OR self with strict timing

### How to run solo
- Pick 5 random problems matching difficulty
- Set 45-min timer for each
- Verbalize aloud throughout
- Record video
- Review for: silence, hesitation, missed edge cases, clarity

---

## IV. THE EVALUATION RUBRIC

After each round, score yourself (1-5):

### Communication
- Did I restate the problem? (clarify)
- Did I explore approaches before coding?
- Did I narrate my code?
- Did I respond to "hints" gracefully?

### Problem-solving
- Did I identify the pattern within 5 min?
- Did I propose brute force then optimize?
- Did I recognize tradeoffs?

### Coding
- Was code clean and modular?
- Were variable names meaningful?
- Did I write bug-free first try?

### Edge cases
- Did I think of n=0, n=1?
- Did I handle adversarial inputs?
- Did I test before submitting?

### Complexity
- Did I correctly state time / space?
- Did I discuss alternatives?

**Total**: 25 points. ≥18 = "would hire" signal.

---

## V. WEEKLY MOCK SCHEDULE (Pre-FAANG)

```
Mon: Solo mock × 2 (medium difficulty)
Tue: Pramp mock × 1 (peer)
Wed: Solo mock + system design × 1
Thu: interviewing.io mock × 1 (paid, with engineer)
Fri: Behavioral mock with friend
Sat: Full 5-round simulation (ALL DAY, mimics onsite)
Sun: Review + reflection
```

---

## VI. SAMPLE 5-ROUND SCRIPT

### Round 1: "Implement LRU cache"
- Time: 45 min
- Patterns: HashMap + Doubly Linked List
- Common follow-up: "What if multi-threaded?"

### Round 2: "Word Ladder II — return all shortest paths"
- Time: 45 min
- Patterns: BFS + backtracking + memoization
- Common follow-up: "What if dictionary is huge?"

### Round 3: System Design — "Design Twitter"
- Time: 45 min
- Discuss: feed (push vs pull), timeline storage, fan-out, hashtag service

### Round 4: "Sliding window maximum"
- Time: 45 min
- Patterns: Monotonic deque
- Follow-up: "What if window slides irregularly?"

### Round 5: Behavioral — Amazon LP focused
- 5 stories: Customer Obsession, Ownership, Bias for Action, Dive Deep, Deliver Results

---

## VII. POST-SIMULATION DEBRIEF

After each round:
- What went well?
- What stalled me?
- Did I pattern-match correctly?
- Was there a missing observation?
- How would I prep this differently?

After full day:
- Total score
- Top 3 strengths
- Top 3 weaknesses
- Action items for next week

---

## VIII. CALIBRATION

- 70% of self-mocks should succeed (else: drop difficulty)
- 30% should be struggle / failure (else: too easy)

**The struggle is the point.** A simulation where you ace everything is too easy.

---

## IX. THE MOCK LADDER

| Stage | Mock difficulty | Pass criteria       |
|-------|-----------------|---------------------|
| 1     | LC Medium       | 80%+ in 25 min      |
| 2     | LC Medium-Hard  | 70%+ in 35 min      |
| 3     | LC Hard         | 50%+ in 45 min      |
| 4     | LC Hard + behavioral | full day with rubric ≥18/25 |

---

## X. RECOMMENDED MOCK PARTNERS

- **Pramp** (free, peer-paired)
- **interviewing.io** (paid, FAANG engineers anonymously)
- **Karat** (some companies use them as the actual interview)
- **CodeMentor** (paid mentorship)
- **A friend at FAANG**

---

**→ Next:** [`02-ICPC-Contest-Simulation.md`](./02-ICPC-Contest-Simulation.md)
