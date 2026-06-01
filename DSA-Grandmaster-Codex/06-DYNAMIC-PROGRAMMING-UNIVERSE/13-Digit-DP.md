# 🧬 Digit DP

> *"Count numbers in [L, R] with some property — digit by digit, in O(digits)."*

---

## I. THE PROBLEM TYPE
"How many integers in [L, R] satisfy property P?" where P depends on the digits (e.g., digit sum, no two equal adjacent digits, contains digit 7, divisible by something based on digits).

Range trick: **answer(L, R) = f(R) − f(L−1)** where f(N) counts valid numbers in [0, N].

---

## II. THE STATE
Build the number digit by digit from most significant:
- **pos**: current digit position
- **tight**: are we still bounded by N's prefix? (if tight, the current digit can't exceed N's digit)
- **leading_zero**: are we still in leading zeros? (affects properties like "first digit")
- **state**: problem-specific (e.g., digit sum so far, last digit, remainder, mask of used digits)

```cpp
int digits[20], len;
long long memo[20][2][SOME_STATE];

long long rec(int pos, bool tight, bool lead, int state) {
    if (pos == len) return is_valid(state) ? 1 : 0;
    if (!tight && !lead && memo[pos][...] != -1) return memo[pos][...];
    int limit = tight ? digits[pos] : 9;
    long long res = 0;
    for (int d = 0; d <= limit; d++) {
        bool ntight = tight && (d == limit);
        bool nlead  = lead && (d == 0);
        int nstate  = update(state, d, nlead);
        res += rec(pos + 1, ntight, nlead, nstate);
    }
    if (!tight && !lead) memo[pos][...] = res;  // only memoize unbounded states
    return res;
}

long long f(long long N) {
    if (N < 0) return 0;
    len = 0;
    for (long long t = N; t > 0; t /= 10) digits[len++] = t % 10;
    reverse(digits, digits + len);
    memset(memo, -1, sizeof memo);
    return rec(0, true, true, initial_state);
}
// answer = f(R) - f(L - 1)
```

---

## III. KEY SUBTLETIES ⭐
1. **Only memoize when `tight == false`** — tight states depend on N's specific prefix and can't be reused across different N.
2. **leading_zero** matters when the property cares about "actual" digits (e.g., "no leading zeros count," "smallest digit").
3. Define `state` as the MINIMAL info needed to verify the property at the end.

---

## IV. EXAMPLE PROPERTIES
- **Digit sum equals / divisible by k**: state = sum mod k.
- **No two equal adjacent digits**: state = last digit.
- **Strictly increasing digits**: state = last digit.
- **Contains a specific digit / pattern**: state = boolean / small automaton state.
- **Number itself divisible by m**: state = number mod m.
- **Count of a digit**: state = count so far.
- **Digits form a set (no repeats)**: state = bitmask of used digits (digit DP + bitmask).

---

## V. WHEN TO USE
- Constraints like L, R up to 10¹⁸ (way too many to iterate) but the property is **digit-based**.
- "Count numbers in a range with property X."

---

## VI. COMPLEXITY
O(num_digits × states × 10) — typically tiny (e.g., 18 × small_state × 10). Effectively instant even for 10¹⁸ ranges.

---

## VII. PROBLEMS
- Count Numbers with Unique Digits (LC 357)
- Numbers At Most N Given Digit Set (LC 902)
- Count of Integers (LC 2719)
- Numbers With Repeated Digits (LC 1012)
- Classy Numbers, Digit sum problems (CF)
- [CSES](https://cses.fi/problemset/) "Counting Numbers"
- [SPOJ](https://www.spoj.com) classic digit DP problems

---

**→ Next:** [`14-Probability-Expected-DP.md`](./14-Probability-Expected-DP.md)
