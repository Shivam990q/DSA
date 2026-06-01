# Merge Triplets to Form Target

**Platform**: LeetCode 1899 · **Difficulty**: Medium · **Topics**: Array, Greedy · **Pattern**: Filter-then-flag greedy

---

## 📜 Problem Statement

A triplet is an array of three integers. You are given a 2D integer array `triplets`, where `triplets[i] = [a_i, b_i, c_i]` describes the `i`-th triplet. You are also given an integer array `target = [x, y, z]` that describes the triplet you want to obtain.

To obtain `target`, you may apply the following operation on `triplets` **any number of times** (possibly zero):

- Choose two indices (0-indexed) `i` and `j` (`i != j`) and **update** `triplets[j]` to become `[max(a_i, a_j), max(b_i, b_j), max(c_i, c_j)]`.

Return `true` if it is possible to obtain the `target` triplet `[x, y, z]` as **an element** of `triplets`, or `false` otherwise.

### Examples

**Example 1:**
```
Input:  triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
Output: true
Explanation: Perform the operation on indices 0 and 2:
[max(2,1), max(5,7), max(3,5)] = [2,7,5]. The last triplet equals target.
```

**Example 2:**
```
Input:  triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
Output: false
Explanation: It is impossible to have [3,2,5] as an element because the second
value (4 or 5) can never be reduced to 2 via max operations.
```

**Example 3:**
```
Input:  triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
Output: true
Explanation: Combine [2,5,3] (gives the 5 in position b) and [5,2,3] (gives the 5
in position a) and [1,2,5] (gives the 5 in position c) → [5,5,5].
```

### Constraints
```
1 <= triplets.length <= 10^5
triplets[i].length == target.length == 3
1 <= a_i, b_i, c_i, x, y, z <= 1000
```

---

## 🧠 Understanding the problem

The only operation is element-wise `max`, which can **only increase** a coordinate (or leave it unchanged). So:

1. A triplet is **usable** only if none of its three values exceeds the corresponding target value. If any component is `> target`, merging it would overshoot a coordinate forever (max never decreases) — that triplet is poison and must be ignored entirely.
2. Among usable triplets, combining them with `max` lets us pick, per coordinate, the maximum value available. To hit `target = [x,y,z]` exactly, we need some usable triplet that contributes exactly `x` in position 0, some (possibly different) usable triplet contributing exactly `y` in position 1, and some contributing exactly `z` in position 2.

If all three target coordinates are individually achievable from usable triplets, then merging those (up to three) triplets yields exactly the target — no coordinate overshoots (they're all usable) and each hits its needed value. So the answer is: keep three booleans, scan once.

---

## Approach 1 — Greedy filter + per-coordinate flags (optimal) ⭐

### Intuition
Walk the triplets once. Skip any triplet that exceeds the target in any coordinate. For each surviving (usable) triplet, mark which exact target coordinates it matches. If by the end all three coordinates have been matched, return `true`.

### Algorithm
1. `a = b = c = false`.
2. For each triplet `t`:
   - If `t[0] > target[0]` or `t[1] > target[1]` or `t[2] > target[2]` → skip.
   - Else: `a |= (t[0] == target[0])`, `b |= (t[1] == target[1])`, `c |= (t[2] == target[2])`.
3. Return `a && b && c`.

### Dry run on `triplets=[[2,5,3],[1,8,4],[1,7,5]], target=[2,7,5]`
```
[2,5,3]: usable (2<=2,5<=7,3<=5). matches pos0 (2==2) → a=true
[1,8,4]: 8 > 7 → poison, skip
[1,7,5]: usable. matches pos1 (7==7) and pos2 (5==5) → b=true, c=true
a&&b&&c → true  ✓
```

### Code
```cpp
bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
    bool a = false, b = false, c = false;
    for (auto& t : triplets) {
        if (t[0] > target[0] || t[1] > target[1] || t[2] > target[2]) continue;
        if (t[0] == target[0]) a = true;
        if (t[1] == target[1]) b = true;
        if (t[2] == target[2]) c = true;
    }
    return a && b && c;
}
```
```java
public boolean mergeTriplets(int[][] triplets, int[] target) {
    boolean a = false, b = false, c = false;
    for (int[] t : triplets) {
        if (t[0] > target[0] || t[1] > target[1] || t[2] > target[2]) continue;
        if (t[0] == target[0]) a = true;
        if (t[1] == target[1]) b = true;
        if (t[2] == target[2]) c = true;
    }
    return a && b && c;
}
```
```python
def mergeTriplets(triplets, target):
    found = [False, False, False]
    for t in triplets:
        if all(t[i] <= target[i] for i in range(3)):
            for i in range(3):
                if t[i] == target[i]:
                    found[i] = True
    return all(found)
```

### Complexity
- **Time**: O(n) — single pass over the triplets.
- **Space**: O(1) — three booleans.

### Verdict
**Optimal.** The two observations (filter poison, then flag exact matches) make this a clean linear scan with constant memory.

---

## Approach 2 — Explicit merge of usable triplets

### Intuition
Same idea framed differently: maintain a running element-wise max over all usable triplets, then compare it to the target at the end. If the merged max equals the target, success.

### Algorithm
1. `merged = [0,0,0]`.
2. For each usable triplet `t` (all coords `<= target`): `merged[k] = max(merged[k], t[k])`.
3. Return `merged == target`.

This works because the merged max over usable triplets is the best we can build, and it can equal the target only if every coordinate is individually achievable (and never overshoots, since only usable triplets contribute).

### Dry run on `triplets=[[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target=[5,5,5]`
```
all four triplets are usable (every coord <= 5)
merged after [2,5,3] = [2,5,3]
after [2,3,4]        = [2,5,4]
after [1,2,5]        = [2,5,5]
after [5,2,3]        = [5,5,5]
merged == target → true  ✓
```

### Code
```cpp
bool mergeTriplets(vector<vector<int>>& triplets, vector<int>& target) {
    int mx = 0, my = 0, mz = 0;
    for (auto& t : triplets) {
        if (t[0] > target[0] || t[1] > target[1] || t[2] > target[2]) continue;
        mx = max(mx, t[0]);
        my = max(my, t[1]);
        mz = max(mz, t[2]);
    }
    return mx == target[0] && my == target[1] && mz == target[2];
}
```
```java
public boolean mergeTriplets(int[][] triplets, int[] target) {
    int mx = 0, my = 0, mz = 0;
    for (int[] t : triplets) {
        if (t[0] > target[0] || t[1] > target[1] || t[2] > target[2]) continue;
        mx = Math.max(mx, t[0]);
        my = Math.max(my, t[1]);
        mz = Math.max(mz, t[2]);
    }
    return mx == target[0] && my == target[1] && mz == target[2];
}
```
```python
def mergeTriplets(triplets, target):
    merged = [0, 0, 0]
    for t in triplets:
        if all(t[i] <= target[i] for i in range(3)):
            for i in range(3):
                merged[i] = max(merged[i], t[i])
    return merged == target
```

### Complexity
- **Time**: O(n).
- **Space**: O(1).

### Verdict
Equally optimal and arguably the most intuitive ("merge everything usable, then compare"). Either approach is a great answer.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Filter + flags | O(n) | O(1) | three booleans ⭐ |
| Merge max | O(n) | O(1) | "merge usable, compare" — most intuitive |

Both are linear and constant-space; they are essentially the same algorithm. There is no meaningful brute force here other than trying subsets, which would be exponential and pointless given the clean greedy.

---

## 🧪 Edge cases & pitfalls
- **A target value never matched exactly** → even if achievable as a max, you need an *exact* hit; the merge-max version captures this because the running max would fall short or overshoot.
- **Every triplet poison** → no usable triplets → flags stay false → `false`.
- **Pitfall**: counting a poison triplet's matching coordinate. A triplet with `t[1] > target[1]` must be skipped **entirely**, even if `t[0] == target[0]` — using it would force `b`-coordinate over target permanently.
- **Single triplet equal to target** → trivially `true`.

---

## 🔗 Related problems
- **Maximum of Absolute Value Expression** (LC 1131) — coordinate-wise reasoning.
- **Dota2 Senate** (LC 649) — another flag/greedy elimination.
- **Largest Number** (LC 179) — greedy comparison ordering.
- **Boats to Save People** (LC 881) — two-pointer greedy on filtered items.

---

**→ Next:** [`07-Partition-Labels.md`](./07-Partition-Labels.md) | **Prev:** [`05-Hand-of-Straights.md`](./05-Hand-of-Straights.md) | [Problem set index](./00-Index.md)
