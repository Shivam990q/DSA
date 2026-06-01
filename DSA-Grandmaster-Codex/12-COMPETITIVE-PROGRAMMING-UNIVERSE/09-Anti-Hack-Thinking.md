# 🛡️ Anti-Hack Thinking

> *"In Educational rounds, others can hack your solution. Defend it."*

---

## I. WHAT IS HACKING
In [Codeforces](https://codeforces.com) Educational rounds (and some others), after the contest you can submit custom inputs to BREAK others' accepted solutions. A successful hack → their solution becomes WA → rating impact.

---

## II. COMMON HACK TRIGGERS (defend against these)

### 1. Hash collisions
`unordered_map` can be forced to O(n) per operation with crafted keys.
**Defense**: custom hash with random seed, or use `map`.

### 2. Integer overflow
Sums of int values can overflow.
**Defense**: use `long long` for sums.

### 3. Unsigned underflow
`a - b` with unsigned when b > a wraps around.
**Defense**: careful with modular subtraction: `(a - b + MOD) % MOD`.

### 4. Off-by-one boundaries
n=1, empty, max constraints.
**Defense**: test all edge cases.

### 5. Quicksort worst case
`std::sort` is introsort (safe), but a hand-rolled quicksort can be O(n²).
**Defense**: use `std::sort` or random pivot.

### 6. Recursion depth
Deep recursion on n=10⁶ stack-overflows.
**Defense**: iterative or increase stack.

---

## III. THE CUSTOM HASH (essential)
```cpp
struct CustomHash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t SEED = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + SEED);
    }
};
unordered_map<long long, int, CustomHash> safe_map;
```

---

## IV. THE PRE-SUBMIT DEFENSE CHECKLIST
```
☐ Used long long for sums?
☐ Custom hash for unordered_map (or used map)?
☐ Tested n=1, n=2, all same, max constraints?
☐ No hand-rolled quicksort (use std::sort)?
☐ Recursion depth safe for max n?
☐ Modular subtraction handles negatives?
☐ Stress-tested?
```

---

## V. HACKING OTHERS (offense = learning)
Reading others' solutions to find bugs teaches you:
- Common mistakes (so you avoid them)
- How to construct adversarial inputs
- Deeper understanding of edge cases

Hacking is both defense training AND rating bonus.

---

## VI. THE MINDSET
Write code that survives adversaries. Assume someone WILL try to break it. This discipline produces robust, correct solutions even outside Educational rounds.

---

**→ Next:** [`10-Stress-Testing.md`](./10-Stress-Testing.md)
