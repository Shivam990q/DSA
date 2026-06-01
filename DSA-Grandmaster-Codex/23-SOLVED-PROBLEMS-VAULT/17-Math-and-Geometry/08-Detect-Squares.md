# Detect Squares

**Platform**: LeetCode 2013 · **Difficulty**: Medium · **Topics**: Array, Hash Table, Design, Counting · **Pattern**: Point-count map + diagonal scan

---

## 📜 Problem Statement

You are given a stream of points on the X-Y plane. Design an algorithm that:

- **Adds** new points from the stream into a data structure. Duplicate points are allowed and should be treated as different points.
- Given a query point, **counts** the number of ways to choose three points from the data structure such that the three points and the query point form an **axis-aligned square** with **positive area**.

An **axis-aligned square** is a square whose edges are all the same length and are either parallel or perpendicular to the x-axis and y-axis.

Implement the `DetectSquares` class:

- `DetectSquares()` Initializes the object.
- `void add(int[] point)` Adds a new point `point = [x, y]` to the data structure.
- `int count(int[] point)` Counts the number of ways to form **axis-aligned squares** with point `point = [x, y]` as described above.

### Examples

**Example 1:**
```
Input:
["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
[[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
Output:
[null, null, null, null, 1, 0, null, 2]

Explanation:
DetectSquares detectSquares = new DetectSquares();
detectSquares.add([3, 10]);
detectSquares.add([11, 2]);
detectSquares.add([3, 2]);
detectSquares.count([11, 10]);   // return 1. Square: [11,10],[3,10],[11,2],[3,2]
detectSquares.count([14, 8]);    // return 0. No square can be formed.
detectSquares.add([11, 2]);      // Adding a duplicate point.
detectSquares.count([11, 10]);   // return 2. Two squares now (the duplicate [11,2]).
```

### Constraints
```
point.length == 2
0 <= x, y <= 1000
At most 3000 calls in total will be made to add and count.
```

---

## 🧠 Understanding the problem

The query point is **one corner** of the square. For an axis-aligned square we want a second point that is the **diagonal** corner — call it `(px, py)`. A diagonal corner must satisfy `|px - qx| == |py - qy|` (equal horizontal and vertical distance, i.e. it lies on a 45° diagonal) and the side must be **positive** (`px != qx`, which also implies `py != qy`).

Given a query `(qx, qy)` and a diagonal corner `(px, py)`, the other two corners are forced: `(qx, py)` and `(px, qy)`. The number of squares using this particular diagonal corner is `count(qx, py) × count(px, qy)` (since duplicates count as distinct points, we multiply the frequencies). Sum over all stored points that qualify as diagonal corners.

So we keep a frequency map of points. `add` is O(1). For `count`, scanning all *distinct* stored points and testing the diagonal condition is the clean approach.

---

## Approach 1 — Frequency map + scan distinct points (optimal) ⭐

### Intuition
Store how many times each point has been added. To count squares for a query, look at every distinct stored point `(px, py)`; if it's a valid diagonal corner, multiply the counts of the two remaining corners and add to the total.

### Algorithm
1. `cnt` = map from `(x,y)` to frequency.
2. `add(p)` → `cnt[p]++`.
3. `count(q=(qx,qy))`:
   - `total = 0`.
   - For each distinct point `(px, py)` in `cnt`:
     - If `abs(px-qx) == abs(py-qy)` and `px != qx` (positive area, diagonal):
       - `total += cnt[(px,py)] * cnt[(qx,py)] * cnt[(px,qy)]`.
   - Return `total`.

### Dry run on the example (after adding `[3,10],[11,2],[3,2]`, query `[11,10]`)
```
q=(11,10). Scan distinct points:
(3,10): |3-11|=8, |10-10|=0 → not equal → skip
(11,2): |11-11|=0 → px==qx → skip (zero side)
(3,2):  |3-11|=8, |2-10|=8 → equal & px!=qx → diagonal!
        other corners: (qx,py)=(11,2) cnt=1, (px,qy)=(3,10) cnt=1
        total += cnt(3,2)=1 * 1 * 1 = 1
return 1  ✓
```
After adding a second `[11,2]`, the same scan gives `cnt(11,2)=2` → `1*2*1 = 2`.

### Code
```cpp
class DetectSquares {
    map<pair<int,int>,int> freq;   // point -> frequency
public:
    DetectSquares() {}
    void add(vector<int> point) {
        freq[{point[0], point[1]}]++;
    }
    int count(vector<int> point) {
        int qx = point[0], qy = point[1];
        long long total = 0;
        for (auto& [p, f] : freq) {
            int px = p.first, py = p.second;
            if (abs(px - qx) == abs(py - qy) && px != qx) {
                long long c1 = f;
                long long c2 = freq.count({qx, py}) ? freq[{qx, py}] : 0;
                long long c3 = freq.count({px, qy}) ? freq[{px, qy}] : 0;
                total += c1 * c2 * c3;
            }
        }
        return (int)total;
    }
};
```
```java
class DetectSquares {
    private Map<Integer, Integer> cnt;  // encoded x*1001+y -> freq
    private List<int[]> distinct;
    public DetectSquares() {
        cnt = new HashMap<>();
        distinct = new ArrayList<>();
    }
    private int key(int x, int y) { return x * 2001 + y; }
    public void add(int[] point) {
        int k = key(point[0], point[1]);
        if (cnt.getOrDefault(k, 0) == 0) distinct.add(new int[]{point[0], point[1]});
        cnt.merge(k, 1, Integer::sum);
    }
    public int count(int[] point) {
        int qx = point[0], qy = point[1];
        long total = 0;
        for (int[] p : distinct) {
            int px = p[0], py = p[1];
            if (Math.abs(px - qx) == Math.abs(py - qy) && px != qx) {
                long c1 = cnt.getOrDefault(key(px, py), 0);
                long c2 = cnt.getOrDefault(key(qx, py), 0);
                long c3 = cnt.getOrDefault(key(px, qy), 0);
                total += c1 * c2 * c3;
            }
        }
        return (int) total;
    }
}
```
```python
from collections import defaultdict
class DetectSquares:
    def __init__(self):
        self.cnt = defaultdict(int)   # (x, y) -> freq
    def add(self, point):
        self.cnt[(point[0], point[1])] += 1
    def count(self, point):
        qx, qy = point
        total = 0
        for (px, py), f in list(self.cnt.items()):
            if abs(px - qx) == abs(py - qy) and px != qx:
                total += f * self.cnt[(qx, py)] * self.cnt[(px, qy)]
        return total
```

### Complexity
- **add**: O(1).
- **count**: O(D) where `D` is the number of distinct points (≤ number of adds, ≤ 3000).
- **Space**: O(D).

### Verdict
**Optimal for the constraints.** Scanning distinct points and multiplying the three relevant frequencies is clean and well within the 3000-call budget. The `px != qx` guard enforces positive area.

---

## Approach 2 — Column-indexed scan (scan points sharing the query's x)

### Intuition
Instead of scanning all distinct points, fix the **vertical side** first: look only at stored points with the **same x as the query** (`px == qx`). Each such point `(qx, py)` gives a side length `d = |py - qy|`; the square can extend left or right, so check both `(qx ± d, qy)` and `(qx ± d, py)`. This narrows the scan to one column.

### Algorithm
1. Keep `cnt[(x,y)]` and an index `byX[x] = list of y's seen at column x`.
2. `count(q)`: for each `py` in `byX[qx]` with `py != qy`:
   - `d = abs(py - qy)`.
   - For `nx` in `{qx - d, qx + d}`: `total += cnt[(qx,py)] * cnt[(nx,qy)] * cnt[(nx,py)]`.

### Dry run on query `[11,10]` (points `[3,10],[11,2],[3,2]`)
```
column qx=11 has y's: {2}. py=2 (≠10): d=|2-10|=8
nx=11-8=3: cnt(11,2)=1 * cnt(3,10)=1 * cnt(3,2)=1 = 1
nx=11+8=19: cnt(19,10)=0 → 0
total = 1  ✓
```

### Code
```cpp
class DetectSquares {
    map<pair<int,int>,int> cnt;
    unordered_map<int, vector<int>> byX;  // x -> list of y (with duplicates ok)
public:
    DetectSquares() {}
    void add(vector<int> point) {
        cnt[{point[0], point[1]}]++;
        byX[point[0]].push_back(point[1]);
    }
    int count(vector<int> point) {
        int qx = point[0], qy = point[1];
        long long total = 0;
        if (!byX.count(qx)) return 0;
        for (int py : byX[qx]) {
            if (py == qy) continue;
            int d = abs(py - qy);
            for (int nx : {qx - d, qx + d}) {
                long long c1 = cnt.count({nx, qy}) ? cnt[{nx, qy}] : 0;
                long long c2 = cnt.count({nx, py}) ? cnt[{nx, py}] : 0;
                total += c1 * c2;   // this (qx,py) is one fixed point, so weight 1 each occurrence
            }
        }
        return (int)total;
    }
};
```
```java
class DetectSquares {
    private Map<Integer,Integer> cnt = new HashMap<>();
    private Map<Integer, List<Integer>> byX = new HashMap<>();
    private int key(int x, int y) { return x * 2001 + y; }
    public DetectSquares() {}
    public void add(int[] point) {
        cnt.merge(key(point[0], point[1]), 1, Integer::sum);
        byX.computeIfAbsent(point[0], k -> new ArrayList<>()).add(point[1]);
    }
    public int count(int[] point) {
        int qx = point[0], qy = point[1];
        long total = 0;
        List<Integer> col = byX.get(qx);
        if (col == null) return 0;
        for (int py : col) {
            if (py == qy) continue;
            int d = Math.abs(py - qy);
            for (int nx : new int[]{qx - d, qx + d}) {
                long c1 = cnt.getOrDefault(key(nx, qy), 0);
                long c2 = cnt.getOrDefault(key(nx, py), 0);
                total += c1 * c2;
            }
        }
        return (int) total;
    }
}
```
```python
from collections import defaultdict
class DetectSquares:
    def __init__(self):
        self.cnt = defaultdict(int)
        self.by_x = defaultdict(list)
    def add(self, point):
        self.cnt[(point[0], point[1])] += 1
        self.by_x[point[0]].append(point[1])
    def count(self, point):
        qx, qy = point
        total = 0
        for py in self.by_x.get(qx, []):
            if py == qy:
                continue
            d = abs(py - qy)
            for nx in (qx - d, qx + d):
                total += self.cnt[(nx, qy)] * self.cnt[(nx, py)]
        return total
```

### Complexity
- **add**: O(1).
- **count**: O(C) where `C` is the number of points sharing the query's column (with multiplicity). In the worst case this equals total adds, same as Approach 1.
- **Space**: O(N) (stores y's with multiplicity).

### Verdict
A nice optimization when points cluster across many columns — it only walks one column. It iterates points *with* multiplicity, so each occurrence of `(qx,py)` contributes once, which naturally accounts for duplicates at the vertical-side corner.

---

## ⚖️ Approach comparison

| Approach | add | count | Space | Notes |
|----------|-----|-------|-------|-------|
| Distinct-point scan | O(1) | O(D) | O(D) | simplest; multiply three freqs ⭐ |
| Column-indexed scan | O(1) | O(C) | O(N) | scans one column only |

Both are well within the 3000-call limit. Approach 1 is the most common interview answer.

---

## 🧪 Edge cases & pitfalls
- **Zero-area "squares"** (a candidate with `px == qx`) → must be excluded; otherwise you'd count degenerate points. The `px != qx` / `py != qy` guard handles it.
- **Duplicate points** → counted as distinct via the frequency multiplication. This is exactly why `count` returns 2 after a duplicate `[11,2]` is added.
- **No matching corners** → returns 0.
- **Pitfall — only checking one diagonal direction**: in the distinct-point scan you naturally see both diagonal corners as you iterate all points, but the column-scan must check both `qx - d` and `qx + d`.
- **Pitfall — overflow**: products of three counts can grow; use `long`/`long long` for the accumulator to be safe (counts are small here, but it's good practice).

---

## 🔗 Related problems
- **Number of Boomerangs** (LC 447) — counting with distance hashing.
- **Max Points on a Line** (LC 149) — geometric counting via slopes.
- **Minimum Area Rectangle** (LC 939) — axis-aligned rectangles from a point set.
- **Detect Squares** generalizes the "fix a diagonal, the other corners are forced" idea.

---

**→ Next:** [`../18-Bit-Manipulation/00-Index.md`](../18-Bit-Manipulation/00-Index.md) | **Prev:** [`07-Plus-One.md`](./07-Plus-One.md) | [Problem set index](./00-Index.md)
