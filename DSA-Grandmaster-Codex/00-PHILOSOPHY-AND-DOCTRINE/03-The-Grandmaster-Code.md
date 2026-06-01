# ⚔️ The Grandmaster Code — 21 Commandments

> *"Discipline is the bridge between aspiration and achievement."*

These are the 21 non-negotiable laws that govern every grandmaster's life. Violate them at your peril.

---

## I. THE COMMANDMENTS

### **I. Thou shalt write the brute force first.**
Before any optimization, write the dumb solution. It is your oracle, your stress-test reference, your sanity.

### **II. Thou shalt understand the problem before coding.**
Read 3 times. Identify input, output, constraints, edge cases. Restate in your own words. Only then touch the keyboard.

### **III. Thou shalt always check constraints first.**
n ≤ 20 → bitmask DP / brute. n ≤ 500 → O(n³). n ≤ 10⁴ → O(n²). n ≤ 10⁶ → O(n log n). n ≤ 10⁹ → O(log n) or math. Constraints whisper the algorithm class.

### **IV. Thou shalt write code as if a grandmaster will read it.**
Variable names that mean something. Functions that do one thing. No magic numbers. Modular code is debuggable code.

### **V. Thou shalt test edge cases ruthlessly.**
n=0, n=1, all same, all distinct, sorted, reverse-sorted, max constraints, negative values, overflow, empty input. Every. Single. Time.

### **VI. Thou shalt prove before thou shalt code.**
Especially for greedy. If you cannot prove it, you do not believe it. If you do not believe it, do not submit it.

### **VII. Thou shalt practice typing with intent.**
Speed of typing matters in contests. But more — typing without thinking is the death of correctness. Pause. Then type.

### **VIII. Thou shalt read editorials with discipline.**
Read until you understand the *idea*, not the code. Close the editorial. Re-derive. Re-implement. Without copy-paste.

### **IX. Thou shalt upsolve every contest.**
A contest where you don't upsolve the unsolved problems is a contest wasted. Upsolving > Contesting in learning value.

### **X. Thou shalt master one language deeply before learning others.**
C++ for CP. Python for prototyping. Java/Kotlin for interviews. Master ONE deeply (containers, idioms, debugger, compiler). Then add others.

### **XI. Thou shalt build templates.**
Disjoint-set union, segment tree, BIT, modular arithmetic, fast I/O, debugging macros — these are your weapons. Forge them. Test them. Trust them.

### **XII. Thou shalt stress-test.**
Write brute. Write your solution. Write a random generator. Compare for thousands of cases. Bugs hide in the unexamined.

### **XIII. Thou shalt timebox.**
30-45 minutes of struggle on a problem before peeking. Beyond that, you're not learning — you're stuck. Read editorial. Learn. Move on.

### **XIV. Thou shalt review thy mistakes.**
Maintain a *Mistake Log*. Every WA, every TLE, every RE — note the root cause. Re-read it weekly. Patterns will emerge.

### **XV. Thou shalt sleep, eat, and exercise.**
The brain is the instrument. A starved, exhausted, sedentary brain solves no problems. Treat your body as the substrate of your mind.

### **XVI. Thou shalt not multitask while practicing.**
No phone. No Discord. No music with lyrics. Deep focus is the multiplier. 1 hour of deep practice > 4 hours of distracted practice.

### **XVII. Thou shalt practice problem types thou hatest.**
You're weak in DP? Solve only DP for two weeks. You hate geometry? Drown in geometry. Comfort zones produce mediocre engineers.

### **XVIII. Thou shalt teach what thou learnest.**
Explain to a friend, write a blog, record a video, answer on [Codeforces](https://codeforces.com). Teaching forces Stage 4 understanding.

### **XIX. Thou shalt not compare thy chapter 1 to another's chapter 20.**
Tourist solves Div1F in 10 minutes. He has 15+ years. Compare yourself only to *yesterday's you*.

### **XX. Thou shalt embrace the suck.**
You will be confused. You will feel stupid. You will lose to easier problems. **This is the path. Confusion is the prerequisite to mastery. Welcome it.**

### **XXI. Thou shalt finish what thou started.**
Half-solved problems poison your psyche. If you started a problem, finish it (solve, or learn the solution and re-implement). No abandoned tickets.

---

## II. THE DAILY DISCIPLINE

A grandmaster's day:

```
Morning  (1.5h):  Warm-up → 1 medium problem → Read 1 editorial
Afternoon (2h):  Hard problem (timed) → Upsolve previous contest
Evening  (1h):   Theory study (book chapter / paper)
Weekend (4-6h):  Live contest + 2-day upsolve cycle
```

Total: ~25-30 hours/week of *deep* work. Sustainable for years. Lethal in compounding effect.

---

## III. THE SACRED TOOLS

| Tool                     | Purpose                              |
|--------------------------|--------------------------------------|
| Editor (VSCode/Vim/CLion)| Coding environment                   |
| Local stress-test setup  | Brute + random gen + diff            |
| Templates folder         | Reusable verified components         |
| Mistake log (notebook)   | Self-feedback loop                   |
| Codeforces / [AtCoder](https://atcoder.jp)     | Competitive practice                 |
| [LeetCode](https://leetcode.com)                 | Interview practice                   |
| [Project Euler](https://projecteuler.net)            | Math + algo                          |
| [CP-Algorithms.com](https://cp-algorithms.com)        | Reference encyclopedia               |
| [USACO Guide](https://usaco.guide)              | Structured curriculum                |
| Books (CLRS, CP4, etc.)  | Deep theory                          |

---

## IV. THE RANK PROGRESSION

| Codeforces Rating | What You Should Be Doing                                                |
|-------------------|-------------------------------------------------------------------------|
| Newbie (< 1200)   | Loops, conditionals, arrays, strings. Master the basics ruthlessly.     |
| Pupil (1200-1399) | Sorting, two pointers, basic greedy, basic DP, BFS/DFS.                 |
| Specialist (1400-1599) | Advanced DP, segment tree, BIT, basic graph algos, number theory.   |
| Expert (1600-1899) | Advanced graphs, strings (KMP, Z), tree DP, harder DP.                 |
| Candidate Master (1900-2099) | Heavy DP optimizations, segtree beats, advanced data structures.|
| Master (2100-2299) | FFT/NTT, suffix structures, link-cut trees, flows.                     |
| Int'l Master (2300-2399) | Complex ad-hoc, deep observations, hard constructive.            |
| Grandmaster (2400+) | Research-grade. You're inventing now.                                 |

---

## V. THE FINAL COMMANDMENT

> **"There is no path to mastery — mastery IS the path.  
> You do not arrive. You become."**

---

**→ Next:** [`04-The-Path-of-Mastery.md`](./04-The-Path-of-Mastery.md)
