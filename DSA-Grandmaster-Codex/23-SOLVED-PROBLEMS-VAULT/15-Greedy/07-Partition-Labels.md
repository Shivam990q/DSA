# Partition Labels

**Platform**: LeetCode 763 · **Difficulty**: Medium · **Topics**: Hash Table, Two Pointers, String, Greedy · **Pattern**: Last-occurrence sweep

---

## 📜 Problem Statement

You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in **at most one** part. Note that the partition is done so that after concatenating all the parts in order, the resultant string should be `s`.

Return *a list of integers representing the size of these parts*.

### Examples

**Example 1:**
```
Input:  s = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
This is a partition so that each letter appears in at most one part.
A partition like "ababcbacadefegde", "hijhklij" is incorrect, because it splits s into less parts.
```

**Example 2:**
```
Input:  s = "eccbbbbdec"
Output: [10]
Explanation: The whole string is one part because 'e' first appears at index 0
and last at index 7, 'c' spans 1..9, etc. — everything is tangled together.
```

**Example 3:**
```
Input:  s = "abcde"
Output: [1,1,1,1,1]
Explanation: Every letter is unique, so each is its own part.
```

### Constraints
```
1 <= s.length <= 500
s consists of lowercase English letters.
```

---

## 🧠 Understanding the problem

A letter must live entirely within one part. So if a letter `x` appears at positions `p1 < p2 < … < pk`, the part containing `x` must stretch at least from `p1` to `pk` — it has to swallow the letter's **last occurrence**. And if some other letter `y` appears inside that span, the part must also cover `y`'s last occurrence, possibly extending further, which may pull in more letters, and so on.

So a part is the smallest window that is "closed" under last-occurrences: starting from some index, keep extending the right boundary to the farthest last-index of any letter seen so far. The moment the scanning cursor catches up to that boundary, no letter inside the window appears later — we can cut. This greedy gives the maximum number of parts because we cut at the earliest legal point every time.

---

## Approach 1 — Last-index greedy sweep (optimal) ⭐

### Intuition
First record, for each of the 26 letters, the index of its **last** appearance. Then scan the string maintaining the current part's tentative `end = max(end, last[c])`. When `i == end`, the window is self-contained → record its size and start a new part.

### Algorithm
1. Build `last[c]` = last index of letter `c` (one pass).
2. `start = end = 0`, `res = []`.
3. For `i` from `0` to `n-1`:
   - `end = max(end, last[s[i]])`.
   - If `i == end`: push `end - start + 1`, set `start = i + 1`.
4. Return `res`.

### Dry run on `s = "ababcbacadefegdehijhklij"`
```
last: a→8, b→5, c→7, d→14, e→15, f→11, g→13, h→19, i→22, j→23, k→20, l→21
i=0 'a': end=max(0,8)=8
i=1 'b': end=max(8,5)=8
... up to i=8 'a': end stays 8; i==end(8) → cut size 8-0+1=9, start=9
i=9 'd': end=14 ... i=15 'e': end=15; i==15 → cut size 15-9+1=7, start=16
i=16 'h': end=19 ... i=23 'j': end=23; i==23 → cut size 23-16+1=8
res = [9,7,8]  ✓
```

### Code
```cpp
vector<int> partitionLabels(string s) {
    vector<int> last(26, 0);
    for (int i = 0; i < (int)s.size(); i++) last[s[i] - 'a'] = i;
    vector<int> res;
    int start = 0, end = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        end = max(end, last[s[i] - 'a']);
        if (i == end) {
            res.push_back(end - start + 1);
            start = i + 1;
        }
    }
    return res;
}
```
```java
public List<Integer> partitionLabels(String s) {
    int[] last = new int[26];
    for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
    List<Integer> res = new ArrayList<>();
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        end = Math.max(end, last[s.charAt(i) - 'a']);
        if (i == end) {
            res.add(end - start + 1);
            start = i + 1;
        }
    }
    return res;
}
```
```python
def partitionLabels(s):
    last = {c: i for i, c in enumerate(s)}
    res = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res
```

### Complexity
- **Time**: O(n) — two linear passes.
- **Space**: O(1) — at most 26 entries in `last` (O(σ), the alphabet size).

### Verdict
**Optimal.** The "extend the window to the farthest last-index, cut when caught up" pattern is the canonical answer and generalizes to interval-merging on the fly.

---

## Approach 2 — Interval merging view

### Intuition
Each letter defines an interval `[firstIndex, lastIndex]`. Two letters whose intervals overlap must be in the same part. So the answer is exactly the **merged** intervals — and each merged interval's length is a part size. This is conceptually identical to "Merge Intervals" but specialized to 26 letters.

### Algorithm
1. For each present letter compute `[first[c], last[c]]`.
2. Sort the 26 intervals by start.
3. Merge overlapping intervals; each merged interval's length (`end - start + 1`) is a part.

### Dry run on `s = "abcde"`
```
intervals: a[0,0], b[1,1], c[2,2], d[3,3], e[4,4] — none overlap
merged sizes = [1,1,1,1,1]  ✓
```

### Code
```cpp
vector<int> partitionLabels(string s) {
    vector<int> first(26, -1), last(26, -1);
    for (int i = 0; i < (int)s.size(); i++) {
        int c = s[i] - 'a';
        if (first[c] == -1) first[c] = i;
        last[c] = i;
    }
    vector<pair<int,int>> iv;
    for (int c = 0; c < 26; c++)
        if (first[c] != -1) iv.push_back({first[c], last[c]});
    sort(iv.begin(), iv.end());
    vector<int> res;
    int s0 = iv[0].first, e0 = iv[0].second;
    for (int k = 1; k < (int)iv.size(); k++) {
        if (iv[k].first <= e0) e0 = max(e0, iv[k].second);
        else { res.push_back(e0 - s0 + 1); s0 = iv[k].first; e0 = iv[k].second; }
    }
    res.push_back(e0 - s0 + 1);
    return res;
}
```
```java
public List<Integer> partitionLabels(String s) {
    int[] first = new int[26], last = new int[26];
    Arrays.fill(first, -1); Arrays.fill(last, -1);
    for (int i = 0; i < s.length(); i++) {
        int c = s.charAt(i) - 'a';
        if (first[c] == -1) first[c] = i;
        last[c] = i;
    }
    List<int[]> iv = new ArrayList<>();
    for (int c = 0; c < 26; c++) if (first[c] != -1) iv.add(new int[]{first[c], last[c]});
    iv.sort((a, b) -> a[0] - b[0]);
    List<Integer> res = new ArrayList<>();
    int s0 = iv.get(0)[0], e0 = iv.get(0)[1];
    for (int k = 1; k < iv.size(); k++) {
        if (iv.get(k)[0] <= e0) e0 = Math.max(e0, iv.get(k)[1]);
        else { res.add(e0 - s0 + 1); s0 = iv.get(k)[0]; e0 = iv.get(k)[1]; }
    }
    res.add(e0 - s0 + 1);
    return res;
}
```
```python
def partitionLabels(s):
    first, last = {}, {}
    for i, c in enumerate(s):
        if c not in first:
            first[c] = i
        last[c] = i
    iv = sorted([first[c], last[c]] for c in first)
    res = []
    s0, e0 = iv[0]
    for st, en in iv[1:]:
        if st <= e0:
            e0 = max(e0, en)
        else:
            res.append(e0 - s0 + 1)
            s0, e0 = st, en
    res.append(e0 - s0 + 1)
    return res
```

### Complexity
- **Time**: O(n + σ log σ) — with σ ≤ 26 the sort is effectively constant, so O(n).
- **Space**: O(σ).

### Verdict
A nice way to *see* the structure (it's interval merging!), but the single-pass last-index sweep is shorter and just as fast. Use Approach 1 in an interview, mention this as the underlying idea.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Last-index sweep | O(n) | O(σ) | shortest, canonical ⭐ |
| Interval merge | O(n) | O(σ) | reveals the "merge intervals" structure |

---

## 🧪 Edge cases & pitfalls
- **All distinct letters** → every position is its own part → all `1`s.
- **All same letter** (`"aaaa"`) → one part of size `n`.
- **Single character** → `[1]`.
- **Pitfall**: cutting when `i` reaches *a* letter's last index instead of the running `max`. You must extend `end` over *every* letter seen in the current window, not just the current character.
- **Pitfall**: forgetting that the parts must concatenate back to `s` in order — this is automatic with the left-to-right sweep, but a "sort the sizes" mistake would break it.

---

## 🔗 Related problems
- **Merge Intervals** (LC 56) — the general version of Approach 2.
- **Employee Free Time** (LC 759) — interval sweeping.
- **Maximum Number of Non-overlapping Substrings** (LC 1520) — last-index expansion taken further.
- **Video Stitching** (LC 1024) — interval-cover greedy.

---

**→ Next:** [`08-Valid-Parenthesis-String.md`](./08-Valid-Parenthesis-String.md) | **Prev:** [`06-Merge-Triplets-To-Form-Target.md`](./06-Merge-Triplets-To-Form-Target.md) | [Problem set index](./00-Index.md)
