# 🏆 Competitive Programming Wisdom — The Complete Compendium

> *"To rise, train. To train, grind. To grind, love the game."*

---

## 01 — CODEFORCES MASTERY

### The CF rating system
- Newbie: < 1200 (gray)
- Pupil: 1200-1399 (green)
- Specialist: 1400-1599 (cyan)
- Expert: 1600-1899 (blue)
- Candidate Master: 1900-2099 (purple)
- Master: 2100-2299 (orange)
- International Master: 2300-2399 (red border)
- Grandmaster: 2400-2599 (red)
- International Grandmaster: 2600-2999 (red, boldest)
- Legendary Grandmaster: 3000+

### What each level can do
- **Newbie**: A in Div 4, occasionally B in Div 4
- **Pupil**: A-B in Div 3
- **Specialist**: A-C in Div 3, A-B in Div 2
- **Expert**: B-C in Div 2 sometimes D
- **CM**: D in Div 2, sometimes E
- **Master**: E in Div 2, A-C in Div 1
- **IGM**: D-E in Div 1
- **LGM**: F+ in Div 1, top contests like Tourist

### Rating Climbing Strategies

#### Newbie → Specialist (1100 → 1500)
- Solve 1300-1500 rated problems daily
- Focus: arrays, strings, basic greedy, sorting, BFS/DFS, basic DP
- Sheets: [NeetCode](https://neetcode.io) 150, Striver A2Z, ATC course

#### Specialist → Expert (1500 → 1700)
- Solve 1500-1800 rated daily
- Focus: segtree/BIT, DP, graph algos, math basics
- CF EDU: segment trees, DP

#### Expert → CM (1800 → 2000)
- Solve 1800-2200 daily
- Focus: hard DP, advanced graphs, strings (KMP/Z), constructive
- Read editorials of E/F problems

#### CM → Master (2000 → 2200)
- Solve 2200-2500 daily
- Focus: advanced data structures, FFT/NTT, suffix structures, constructive at scale

#### Master+ (2200+)
- Daily diet: Div 1 problems, ICPC archives
- Specialize in your strongest domain (DP / strings / data structures / etc.)
- Train with virtuals (recreate live conditions)

### How to participate in rounds

```
Pre-round:
  - 5 min before: warmup with an easy problem
  - Stand up; deep breath
  - Open template

Minute 0-5: read all problems
Minute 5-25: solve A, B (free points)
Minute 25-60: solve C
Minute 60-90: attempt D
Minute 90-120: attempt E (or stress-test/verify)
Final 5 min: ensure all submissions correct; do NOT submit untested code in panic

Post-round:
  - Read editorials of unsolved
  - Upsolve next day
  - Note new patterns
```

### Hacking (Educational rounds)
After contest, you can hack others' solutions with custom inputs. Earn rating bonus. Learn typical mistakes.

---

## 02 — ATCODER MASTERY

### AtCoder color tiers
- Gray: < 400
- Brown: 400-799
- Green: 800-1199
- Cyan: 1200-1599
- Blue: 1600-1999
- Yellow: 2000-2399
- Orange: 2400-2799
- Red: 2800+

### Contest types
- **ABC** (Beginner Contest): A-G or A-Ex, varying difficulty
- **ARC** (Regular Contest): hard but accessible
- **AGC** (Grand Contest): legendary, super-hard observation problems

### Why AtCoder is special
- Strong educational sequences (DP Contest, EDPC)
- Cleaner problem statements (less ambiguity)
- Great for ad-hoc / observation-heavy training
- Editorial DPC: best DP introduction

### Recommended start
- AtCoder Beginner Contest archive (chronological)
- [AtCoder DP Contest](https://atcoder.jp/contests/dp) (26 problems, all foundational DP)
- AtCoder ABC E/F problems for intermediate
- AGC for elite observation training

---

## 03 — ICPC SYSTEMS

### Team composition
- 3 students, 1 computer
- 5 hours, 8-13 problems
- Strategy: divide and conquer

### Roles (typical)
- **Coder/Implementer**: types solutions
- **Algorithmist**: thinks problems
- **Manager**: tracks time, decides switches

### Team strategy
- Read all problems immediately (everyone reads ~3)
- Identify "easy" trio first
- Implementer goes solo on easies; others read deeper
- For hard problems: pair up — one sketches, one verifies

### Practice
- Virtual ICPC: weekly with team for 5h
- Upsolve every regional / world final on [Codeforces](https://codeforces.com)

### India / World specific
- ICPC Asia Regionals (multiple rounds)
- ICPC World Finals (top ~135 teams)
- Top India teams: IIT Roorkee, IIT BHU, IIT Bombay, IIT Madras (varying years)

---

## 04 — IOI SYSTEMS

### IOI = International Olympiad in Informatics
- Individual contest for high school
- 2 days × 5 hours, 3 problems per day
- Each problem: 100 points; partial credit for partial solutions

### Subtask grading
Each problem has subtasks with constraint reductions. Solve simpler ones for partial credit.

### Strategy
- Read all 3 problems immediately
- Solve easier subtasks of each first → secure points
- Then attack hardest subtasks
- Don't get stuck on full solution if subtask points still unclaimed

### Training resources
- IOI Past Problems ([oi.uz](https://oi.uz), ioi.tw)
- [USACO Guide](https://usaco.guide) (mirrors IOI training)
- Codeforces Olympiad rounds
- Camps: [USACO](https://www.usaco.org) Camp, IIO Indian Olympiad camps

---

## 05 — CONTEST STRATEGY (THE GENERIC PLAYBOOK)

### Pre-contest (24 hours before)
- Light practice; no new heavy concepts
- Sleep 8 hours
- Hydrate, eat well

### 30 min before
- Glucose snack; coffee if you tolerate
- Open editor, template, scratch pad
- Verify internet, judge accessible

### Round opening
- Read ALL problems first (5-10 min)
- Sort mentally: easiest → hardest
- Note constraints for each

### During the round
- Solve in difficulty order (easiest first)
- For each problem:
  1. Understand
  2. Brute force complexity check
  3. Identify optimization
  4. Code (clean, compile early)
  5. Test on examples + edge cases
  6. Submit

### Switching problems
- 30-40 minutes stuck on one → switch
- Return after solving easier ones with fresh perspective

### Last 10 minutes
- DO NOT submit untested code
- Verify submitted ones are not pretests-only
- Stress-test if uncertain

---

## 06 — UPSOLVING FRAMEWORK

After every contest:

1. **Solve unsolved problems** WITHOUT editorial first (give 30-60 min)
2. **Read editorial** of remaining unsolved
3. **Re-implement** from understanding (no copy-paste)
4. **Note the pattern** in your problem journal
5. **Star problems for re-solving** in 7 days

> "Upsolving teaches you what the contest didn't."

---

## 07 — EDITORIAL READING

### Discipline
- Read for **idea**, not for code
- Stop when you understand the approach
- Close editorial; re-derive
- Implement on your own

### What to extract
- The key observation
- The pattern category
- The complexity argument
- Any new technique you learned

### Worth-keeping notes
- Pattern → "When X, try Y"
- Technique → "Knuth optimization applies when..."
- Mistake → "I missed that ... was monotonic"

---

## 08 — RATING CLIMBING SYSTEMS

### The 3-Phase Rating Climb

#### Phase 1: Establish baseline (1-3 months)
- Solve 30+ problems at current level
- Stabilize
- Understand your weakest topics

#### Phase 2: Targeted weaknesses (3-6 months)
- Solve 20+ problems per weak topic
- Theory + practice
- Move to next-tier-up problems

#### Phase 3: Volume (continuous)
- Daily problems above your rating
- Weekly contests
- Upsolving discipline

### When you plateau
- 3 weeks without rating gain → topical immersion week
- Pick weakest topic; drill 50 problems
- Re-engage rated contests

### When you regress
- 200+ rating drop → diagnose: rest? distraction? topical gap?
- Take 1 week light practice + recovery
- Re-engage with smaller goals

---

## 09 — ANTI-HACK THINKING

### What is hacking?
Other contestants find a counterexample to break your solution. Your solution gets "hacked" → WA → rating drop.

### Common hack triggers
- **Hash collisions**: use custom hash with random seed
- **Integer overflow**: long long for sums
- **Unsigned underflow**: careful with modular arithmetic
- **Off-by-one**: especially boundary cases
- **Special inputs**: n=1, all same, max values
- **Adversarial data structures**: e.g., quicksort worst case → use random pivot or std::sort
- **Unordered_map worst case**: use custom hash or `map`

### Defense before submit
- Test on n=1, n=2, all same, max constraints
- Stress test against brute force
- Use safe hashing
- Prefer std::map over unordered_map for adversarial CF Educational rounds

---

## 10 — STRESS TESTING

### The 4-file setup
1. **gen.cpp**: random valid input generator
2. **brute.cpp**: obviously-correct slow solution
3. **sol.cpp**: your optimized solution
4. **runner.sh** / **runner.bat**: loop, compare

### Linux runner.sh
```bash
g++ -O2 gen.cpp -o gen
g++ -O2 brute.cpp -o brute
g++ -O2 sol.cpp -o sol
for i in {1..10000}; do
    ./gen $i > in.txt
    ./brute < in.txt > out_brute.txt
    ./sol < in.txt > out_sol.txt
    if ! diff -q out_brute.txt out_sol.txt > /dev/null; then
        echo "MISMATCH on seed $i"
        cat in.txt
        echo "Brute:"; cat out_brute.txt
        echo "Sol:";   cat out_sol.txt
        break
    fi
done
```

### When to stress test
- Whenever WA on a problem you "thought was right"
- For greedy algorithms (always)
- For complex DP / data-structure code
- Before final submit on hard problems

---

## 11 — TEMPLATE ENGINEERING

### What a CP template should have
1. **Headers + namespaces**
2. **Type aliases** (vi, vvi, pii, ll, etc.)
3. **Macros** (rep, all, debug)
4. **Fast I/O** (sync_with_stdio(false); cin.tie(NULL))
5. **Common utilities** (gcd, modPow, modInv)

### What to add gradually
- Modular arithmetic class
- DSU
- Segment tree (lazy)
- BIT
- Hash function with custom seed
- Debugger (`dbg(x)` macro)

### Don't over-template
- 200-line template = error magnet
- Add only what you use frequently
- Test all template code thoroughly

(Full template in `19-TEMPLATES-AND-IMPLEMENTATIONS/`)

---

## 12 — THE 50 CP RULES

1. Show up. Even tired. Even unmotivated.
2. Read all problems before starting.
3. Solve easy first.
4. Write brute force first.
5. Stress test before submit.
6. Read editorials with discipline (idea, not code).
7. Upsolve every contest.
8. Track rating but don't obsess.
9. One language deeply, others optionally.
10. Templates are tools, not crutches.
11. Don't anchor on first impression.
12. Constraints whisper algorithms.
13. Always check edge cases (n=0, 1, all same, max).
14. Sleep is preprocessing.
15. Compete against yesterday-you.
16. Learn from every WA.
17. Don't argue editorials; learn them.
18. Specialize after foundation, not before.
19. Pair up with someone at your level.
20. Mentor someone below your level.
21. Read [CP-Algorithms.com](https://cp-algorithms.com) weekly.
22. Solve a USACO problem weekly.
23. Read 1 IOI problem per month.
24. Read [Errichto](https://www.youtube.com/@Errichto) / Tourist solutions occasionally.
25. Don't switch languages mid-contest.
26. Always use `long long` for sums in CP.
27. `int main()` returns 0 by default; `ios_base::sync_with_stdio(false)` for speed.
28. `cin.tie(NULL)` to unlink cin from cout.
29. `'\n'` over `endl` (flushes!).
30. Modular arithmetic everywhere it's required.
31. Custom hash for unordered_map in adversarial rounds.
32. Random shuffle inputs to avoid worst case.
33. Don't use `freopen` unless required.
34. `cerr` for debug; remove before submit (or `#ifdef LOCAL`).
35. Pre-allocate capacity for vectors when size is known.
36. Avoid `vector<bool>` (bit-packed, slow access). Use `vector<char>`.
37. Iterative implementations are faster than recursive (constant factor).
38. Cache locality matters; iterate in row-major order.
39. Avoid recursion for n > 10⁵ unless depth bounded.
40. `__builtin_popcount`, `__lg`, `__builtin_ctz` are your friends.
41. `__int128` for products that overflow long long.
42. Multiple test cases? Reset state carefully.
43. Greedy without proof is gambling.
44. Practice typing speed.
45. Ergonomic setup matters (chair, keyboard, screen).
46. Don't compete sleep-deprived for serious rounds.
47. Take breaks between rounds.
48. Build a long-term consistency habit.
49. Celebrate every milestone (Specialist → Expert → CM).
50. The best contestant is the one who never stops learning.

---

## 13 — RECOMMENDED RESOURCES

### Books
- **[Competitive Programming 4](https://cpbook.net)** (Halim) ⭐
- **[Competitive Programmer's Handbook](https://cses.fi/book/book.pdf)** (Laaksonen) ⭐ FREE
- **Looking for a Challenge** (Polish CP team)
- **Algorithmic Toolkit** (Coursera Sedgewick equivalent)

### Sites
- **Codeforces** ⭐
- **AtCoder** ⭐
- **[CodeChef](https://www.codechef.com)**
- **[CSES Problem Set](https://cses.fi/problemset/)** ⭐
- **CP-Algorithms.com** ⭐
- **codeforces.com/edu** — interactive courses
- **USACO Guide** ⭐

### YouTube
- **Errichto** ⭐
- **[William Lin](https://www.youtube.com/@tmwilliamlin168)**
- **[SecondThread](https://www.youtube.com/@SecondThread)**
- **Algorithms Live!**
- **Tourist's streams**

### Templates
- **[KACTL](https://github.com/kth-competitive-programming/kactl)** (KTH) ⭐
- **[AtCoder Library](https://github.com/atcoder/ac-library)**
- **JCantin's library**

---

**→ Next:** [`../13-INTERVIEW-DSA-UNIVERSE/`](../13-INTERVIEW-DSA-UNIVERSE/)
