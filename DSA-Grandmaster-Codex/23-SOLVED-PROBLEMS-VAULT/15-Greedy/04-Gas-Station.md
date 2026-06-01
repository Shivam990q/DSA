# Gas Station

**Platform**: LeetCode 134 · **Difficulty**: Medium · **Topics**: Array, Greedy · **Pattern**: Running-tank one-pass

---

## 📜 Problem Statement

There are `n` gas stations along a **circular** route, where the amount of gas at the `i`-th station is `gas[i]`.

You have a car with an unlimited gas tank, and it costs `cost[i]` of gas to travel from the `i`-th station to its next `(i + 1)`-th station. You begin the journey with an empty tank at one of the gas stations.

Given two integer arrays `gas` and `cost`, return *the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return* `-1`. If a solution exists, it is **guaranteed to be unique**.

### Examples

**Example 1:**
```
Input:  gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3
Explanation:
Start at station 3 (index 3) and fill up with 4 units. Tank = 0 + 4 = 4
Travel to station 4. Tank = 4 - 1 + 5 = 8
Travel to station 0. Tank = 8 - 2 + 1 = 7
Travel to station 1. Tank = 7 - 3 + 2 = 6
Travel to station 2. Tank = 6 - 4 + 3 = 5
Travel to station 3 (back to start). Tank = 5 - 5 + 4 = 4
Therefore, return 3 as the starting index.
```

**Example 2:**
```
Input:  gas = [2,3,4], cost = [3,4,3]
Output: -1
Explanation: You can't start at any station and complete the circuit.
```

### Constraints
```
n == gas.length == cost.length
1 <= n <= 10^5
0 <= gas[i], cost[i] <= 10^4
```

---

## 🧠 Understanding the problem

At each station you gain `gas[i]` and immediately spend `cost[i]` to reach the next one, so the **net change** at station `i` is `diff[i] = gas[i] - cost[i]`. Starting from some index, the tank must stay `>= 0` at every step all the way around the loop.

Two facts unlock the O(n) solution:

1. **Feasibility test**: the trip is possible *somewhere* iff the total `sum(gas) >= sum(cost)`, i.e. `sum(diff) >= 0`. If the total is negative you can never close the loop, period.
2. **Where to start**: if you begin at index `start` and your running tank goes negative for the first time at index `i`, then **no station in `[start, i]` can be a valid start**. Why? Each of those stations would have begun with a tank `≥ 0` and reached `i` with even less fuel than the run that started at `start` (which itself started at 0). So the only hope is to restart at `i+1`.

Combine the two: do a single sweep, reset `start` to `i+1` whenever the tank dips negative, and at the end check the total. Because a unique answer is guaranteed when feasible, this start index is the answer.

---

## Approach 1 — Brute force (try every start)

### Intuition
For each candidate start, simulate the whole loop and check the tank never drops below zero.

### Algorithm
1. For each `start` in `0..n-1`:
   - Run `n` steps around the circle accumulating `diff`; if the tank ever goes negative, abandon this start.
   - If you complete `n` steps, return `start`.
2. Return `-1`.

### Dry run on `gas=[1,2,3,4,5], cost=[3,4,5,1,2]`
```
start 0: tank 1-3 = -2 → fail
start 1: tank 2-4 = -2 → fail
start 2: tank 3-5 = -2 → fail
start 3: 4-1=3, +5-2=6, +1-3=4, +2-4=2, +3-5=0 → survives → return 3
```

### Code
```cpp
int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
    int n = gas.size();
    for (int start = 0; start < n; start++) {
        int tank = 0;
        bool ok = true;
        for (int step = 0; step < n; step++) {
            int i = (start + step) % n;
            tank += gas[i] - cost[i];
            if (tank < 0) { ok = false; break; }
        }
        if (ok) return start;
    }
    return -1;
}
```
```java
public int canCompleteCircuit(int[] gas, int[] cost) {
    int n = gas.length;
    for (int start = 0; start < n; start++) {
        int tank = 0;
        boolean ok = true;
        for (int step = 0; step < n; step++) {
            int i = (start + step) % n;
            tank += gas[i] - cost[i];
            if (tank < 0) { ok = false; break; }
        }
        if (ok) return start;
    }
    return -1;
}
```
```python
def canCompleteCircuit(gas, cost):
    n = len(gas)
    for start in range(n):
        tank = 0
        ok = True
        for step in range(n):
            i = (start + step) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                ok = False
                break
        if ok:
            return start
    return -1
```

### Complexity
- **Time**: O(n²) — up to ~10^10 at n = 10^5. **TLE.**
- **Space**: O(1).

### Verdict
Correct baseline. The wasted work is re-simulating overlapping prefixes; the greedy proves we can skip them.

---

## Approach 2 — One-pass greedy (optimal) ⭐

### Intuition
Track two accumulators: `total` (net over the whole array, for the feasibility verdict) and `tank` (net since the last restart). When `tank` goes negative at index `i`, discard `[start, i]` and set `start = i+1`, `tank = 0`. After the sweep, if `total >= 0` the answer is `start`; otherwise `-1`.

### Algorithm
1. `total = tank = start = 0`.
2. For `i` from `0` to `n-1`:
   - `diff = gas[i] - cost[i]`; add to both `total` and `tank`.
   - If `tank < 0`: `start = i + 1`, `tank = 0`.
3. Return `total >= 0 ? start : -1`.

### Dry run on `gas=[1,2,3,4,5], cost=[3,4,5,1,2]`
```
diffs = [-2,-2,-2,3,3]
i=0: total=-2 tank=-2 <0 → start=1 tank=0
i=1: total=-4 tank=-2 <0 → start=2 tank=0
i=2: total=-6 tank=-2 <0 → start=3 tank=0
i=3: total=-3 tank=3
i=4: total=0  tank=6
total(0) >= 0 → return start = 3  ✓
```

### Code
```cpp
int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < (int)gas.size(); i++) {
        int diff = gas[i] - cost[i];
        total += diff;
        tank += diff;
        if (tank < 0) { start = i + 1; tank = 0; }
    }
    return total >= 0 ? start : -1;
}
```
```java
public int canCompleteCircuit(int[] gas, int[] cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < gas.length; i++) {
        int diff = gas[i] - cost[i];
        total += diff;
        tank += diff;
        if (tank < 0) { start = i + 1; tank = 0; }
    }
    return total >= 0 ? start : -1;
}
```
```python
def canCompleteCircuit(gas, cost):
    total = tank = start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        tank += diff
        if tank < 0:
            start = i + 1
            tank = 0
    return start if total >= 0 else -1
```

### Complexity
- **Time**: O(n) — single pass.
- **Space**: O(1).

### Verdict
**Optimal.** The whole problem collapses to two running sums and one reset rule, backed by the "no station in a failed prefix can start" argument.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n²) | O(1) | baseline; TLE |
| One-pass greedy | **O(n)** | **O(1)** | optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **`total < 0`** → return `-1` regardless of where `start` landed.
- **`start = n`**: if the negative happens on the last index, `start` becomes `n`. This only occurs when `total < 0`, so we return `-1` anyway and never index out of range.
- **Exactly balanced** (`total == 0`) → still feasible (`>=`), and the unique start is valid.
- **Single station** (`n=1`) → feasible iff `gas[0] >= cost[0]`; the formula returns `0` or `-1` correctly.
- **Pitfall**: testing `total > 0` instead of `total >= 0` — the equal case must succeed.
- **Pitfall**: forgetting to reset `tank` to `0` on restart; it must, because the new run begins empty.

---

## 🔗 Related problems
- **Maximum Subarray** (LC 53) — same "reset when running sum hurts" greedy.
- **Jump Game** (LC 55) — single-pass feasibility scan.
- **Candy** (LC 135) — another greedy with a two-direction sweep.
- **Minimum Size Subarray Sum** (LC 209) — running-sum window control.

---

**→ Next:** [`05-Hand-of-Straights.md`](./05-Hand-of-Straights.md) | **Prev:** [`03-Jump-Game-II.md`](./03-Jump-Game-II.md) | [Problem set index](./00-Index.md)
