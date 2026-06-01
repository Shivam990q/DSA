# Time Based Key-Value Store

**Platform**: LeetCode 981 · **Difficulty**: Medium · **Topics**: Hash Table, String, Binary Search, Design · **Pattern**: Binary search for the rightmost timestamp ≤ query

---

## 📜 Problem Statement

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the `TimeMap` class:

- `TimeMap()` Initializes the object of the data structure.
- `void set(String key, String value, int timestamp)` Stores the key `key` with the value `value` at the given time `timestamp`.
- `String get(String key, int timestamp)` Returns a value such that `set` was called previously, with `timestamp_prev <= timestamp`. If there are multiple such values, it returns the value associated with the **largest** `timestamp_prev`. If there are no values, it returns `""`.

**Note**: All the timestamps `timestamp` of `set` are **strictly increasing** for a given key.

### Examples

**Example 1:**
```
Input:
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]

Output:
[null, null, "bar", "bar", null, "bar2", "bar2"]

Explanation:
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);   // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);          // return "bar"
timeMap.get("foo", 3);          // "bar" is the value with the largest timestamp (1) <= 3.
timeMap.set("foo", "bar2", 4);  // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);          // return "bar2"
timeMap.get("foo", 5);          // return "bar2"
```

**Example 2:**
```
get("foo", 0)  on an empty/earlier store → ""   (no timestamp <= 0 exists)
```

### Constraints
```
1 <= key.length, value.length <= 100
key and value consist of lowercase English letters and digits.
1 <= timestamp <= 10^7
All the timestamps timestamp of set() are strictly increasing.
At most 2 * 10^5 calls will be made to set and get.
```

---

## 🧠 Understanding the problem

Two operations, two requirements:

1. **`set(key, value, timestamp)`** — record that at time `timestamp`, `key` had `value`.
2. **`get(key, timestamp)`** — return the value stored at the **largest timestamp that is `<= timestamp`** (the most recent value "as of" that query time). If nothing was stored at or before that time, return `""`.

The golden fact, stated right in the problem: for a given key, **timestamps are strictly increasing in call order**. So if we just append `(timestamp, value)` pairs to a per-key list as they arrive, that list is **automatically sorted by timestamp** — no sorting needed.

Once each key's history is a sorted list of timestamps, `get` becomes a classic search: *"find the rightmost entry whose timestamp is `<= query`."* That is exactly an **upper-bound / predecessor** binary search.

So the design is:
- A hash map: `key → list of (timestamp, value)` in increasing timestamp order.
- `set`: O(1) append.
- `get`: O(log n) binary search on the key's list.

---

## Approach 1 — Linear scan back from the end (baseline)

### Intuition
Store the per-key history as before. For `get`, walk the list from the newest entry backward and return the first entry whose timestamp is `<= query`.

### Algorithm
1. `set`: `map[key].append((timestamp, value))`.
2. `get`: iterate the key's list from the back; return the first `value` with `timestamp <= query`; if none, return `""`.

### Code

```cpp
class TimeMap {
    unordered_map<string, vector<pair<int,string>>> m;
public:
    TimeMap() {}
    void set(string key, string value, int timestamp) {
        m[key].push_back({timestamp, value});
    }
    string get(string key, int timestamp) {
        auto& v = m[key];
        for (int i = (int)v.size() - 1; i >= 0; i--)
            if (v[i].first <= timestamp) return v[i].second;
        return "";
    }
};
```
```java
class TimeMap {
    private Map<String, List<Object[]>> map;   // key -> list of {timestamp, value}

    public TimeMap() {
        map = new HashMap<>();
    }

    public void set(String key, String value, int timestamp) {
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(new Object[]{timestamp, value});
    }

    public String get(String key, int timestamp) {
        List<Object[]> list = map.getOrDefault(key, new ArrayList<>());
        for (int i = list.size() - 1; i >= 0; i--) {
            if ((int) list.get(i)[0] <= timestamp) return (String) list.get(i)[1];
        }
        return "";
    }
}
```
```python
class TimeMap:
    def __init__(self):
        self.map = {}                          # key -> list of (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.map.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        for ts, val in reversed(self.map.get(key, [])):
            if ts <= timestamp:
                return val
        return ""
```

### Complexity
- **set**: O(1).
- **get**: O(n) per call where `n` is the number of stores for that key — worst case slow when one key is queried many times after many sets.
- **Space**: O(total stores).

### Verdict
Correct, and fine if queries usually hit recent timestamps. But with up to `2·10^5` calls and one hot key, repeated `get` scans can degrade to O(n) each. We have a sorted list — we should binary search it.

---

## Approach 2 — Binary search for the predecessor timestamp (optimal) ⭐

### Intuition
Each key's list is sorted by timestamp. To answer `get`, binary search for the **rightmost** index whose timestamp is `<= query`. Keep a running `result` whenever we see a valid (`<=`) timestamp and push `lo` rightward to look for an even later valid one.

### Algorithm
1. `set`: append `(timestamp, value)` to `map[key]` (stays sorted by the strictly-increasing guarantee).
2. `get(key, timestamp)`:
   - `v = map[key]` (empty if key unseen).
   - `lo = 0`, `hi = v.size() - 1`, `res = ""`.
   - While `lo <= hi`:
     - `mid = lo + (hi - lo) / 2`.
     - If `v[mid].timestamp <= timestamp` → this is a candidate; record `res = v[mid].value` and search right (`lo = mid + 1`) for a later valid one.
     - Else → too late; search left (`hi = mid - 1`).
   - Return `res`.

### Dry run on the Example 1 store for key `"foo"`
```
After two sets, foo → [(1,"bar"), (4,"bar2")]

get("foo", 5):
  lo=0, hi=1, res=""
    mid=0 → ts=1 <= 5 → res="bar", search right → lo=1
  lo=1, hi=1
    mid=1 → ts=4 <= 5 → res="bar2", search right → lo=2
  lo=2 > hi=1 → return "bar2" ✅

get("foo", 3):
  lo=0, hi=1, res=""
    mid=0 → ts=1 <= 3 → res="bar", lo=1
  lo=1, hi=1
    mid=1 → ts=4 > 3 → hi=0
  lo=1 > hi=0 → return "bar" ✅

get("foo", 0):
  lo=0, hi=1, res=""
    mid=0 → ts=1 > 0 → hi=-1
  lo=0 > hi=-1 → return "" ✅
```

### Code

```cpp
class TimeMap {
    unordered_map<string, vector<pair<int,string>>> m;
public:
    TimeMap() {}

    void set(string key, string value, int timestamp) {
        m[key].push_back({timestamp, value});   // timestamps arrive increasing
    }

    string get(string key, int timestamp) {
        auto it = m.find(key);
        if (it == m.end()) return "";
        auto& v = it->second;
        int lo = 0, hi = (int)v.size() - 1;
        string res = "";
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (v[mid].first <= timestamp) {     // candidate; look for a later one
                res = v[mid].second;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return res;
    }
};
```
```java
class TimeMap {
    private Map<String, List<Pair>> map;

    private static class Pair {
        int timestamp;
        String value;
        Pair(int t, String v) { timestamp = t; value = v; }
    }

    public TimeMap() {
        map = new HashMap<>();
    }

    public void set(String key, String value, int timestamp) {
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(new Pair(timestamp, value));
    }

    public String get(String key, int timestamp) {
        List<Pair> v = map.get(key);
        if (v == null) return "";
        int lo = 0, hi = v.size() - 1;
        String res = "";
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            if (v.get(mid).timestamp <= timestamp) {   // candidate; look right
                res = v.get(mid).value;
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
        return res;
    }
}
```
```python
class TimeMap:
    def __init__(self):
        self.map = {}                          # key -> list of (timestamp, value)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.map.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        v = self.map.get(key, [])
        lo, hi = 0, len(v) - 1
        res = ""
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if v[mid][0] <= timestamp:         # candidate; look for a later one
                res = v[mid][1]
                lo = mid + 1
            else:
                hi = mid - 1
        return res
```

**Python alternative using `bisect`** (store timestamps and values in parallel lists):
```python
import bisect

class TimeMap:
    def __init__(self):
        self.times = {}    # key -> list of timestamps (sorted)
        self.vals = {}     # key -> list of values (parallel)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.times.setdefault(key, []).append(timestamp)
        self.vals.setdefault(key, []).append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.times:
            return ""
        # rightmost index with timestamp <= query
        i = bisect.bisect_right(self.times[key], timestamp)
        return self.vals[key][i - 1] if i else ""
```

### Complexity
- **set**: O(1) amortized (append).
- **get**: O(log n) where `n` is the number of stores for that key.
- **Space**: O(total number of stores).

### Verdict
**The optimal answer.** It exploits the strictly-increasing timestamp guarantee to keep each key's list sorted for free, then binary searches it. The `get` loop is the "rightmost value `<=` target" predecessor template — a reusable building block.

---

## ⚖️ Approach comparison

| Approach | set | get | Space | When to mention |
|----------|-----|-----|-------|-----------------|
| Linear scan from end | O(1) | O(n) | O(n) | baseline; ok if queries hit recent times |
| Binary search predecessor | O(1) | **O(log n)** | O(n) | the optimal answer ⭐ |

The key realization to verbalize: *"because timestamps for a key arrive strictly increasing, appends keep the per-key list sorted, so `get` is a predecessor binary search."*

---

## 🧪 Edge cases & pitfalls
- **Key never set** → `get` returns `""` (the map lookup yields an empty list / null).
- **Query before the earliest timestamp** (`get("foo", 0)`) → no valid entry → `""`. The `res` stays `""` because no `mid` satisfied `<=`.
- **Query at or after the latest timestamp** → returns the last stored value (the binary search walks `lo` to the end).
- **Exact-match timestamp** → `<=` includes equality, so an exact hit returns that entry's value.
- **Pitfall — using `bisect_left` instead of `bisect_right`**: for "largest timestamp `<= query`", use `bisect_right(times, query) - 1`. `bisect_left` would mishandle an exact match by excluding it.
- **Pitfall — assuming timestamps are sorted for free across keys**: the guarantee is *per key*. Each key keeps its own list; don't merge keys into one list.
- **Pitfall — the clever `(timestamp, chr(127))` sentinel trick** works but is fragile; storing parallel timestamp/value lists (or explicit binary search) is clearer and just as fast.

---

## 🔗 Related problems
- **Binary Search** (LC 704) — the predecessor search is a small twist on this.
- **Search Insert Position** (LC 35) — the lower-bound sibling of this upper-bound search.
- **Snapshot Array** (LC 1146) — same versioned-history-with-binary-search idea.
- **Online Election** (LC 911) — precompute a sorted timeline, then binary search queries.

---

**→ Next:** [`07-Median-of-Two-Sorted-Arrays.md`](./07-Median-of-Two-Sorted-Arrays.md) | **→ Prev:** [`05-Search-Rotated-Sorted-Array.md`](./05-Search-Rotated-Sorted-Array.md) | [Problem set index](./00-Index.md)
