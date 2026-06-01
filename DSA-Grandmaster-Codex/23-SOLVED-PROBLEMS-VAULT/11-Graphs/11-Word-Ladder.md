# Word Ladder

**Platform**: LeetCode 127 · **Difficulty**: Hard · **Topics**: Hash Table, String, BFS · **Pattern**: Shortest path via BFS on an implicit graph

---

## 📜 Problem Statement

A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:

- Every adjacent pair of words differs by a single letter.
- Every `si` for `1 <= i <= k` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.
- `sk == endWord`.

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return *the **number of words** in the **shortest transformation sequence** from `beginWord` to `endWord`, or `0` if no such sequence exists.*

### Examples

**Example 1:**
```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5
Explanation: One shortest transformation is
"hit" -> "hot" -> "dot" -> "dog" -> "cog", which is 5 words long.
```

**Example 2:**
```
Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
Output: 0
Explanation: endWord "cog" is not in wordList, so no valid sequence exists.
```

**Example 3:**
```
Input: beginWord = "a", endWord = "c", wordList = ["a","b","c"]
Output: 2
Explanation: "a" -> "c" is a single-letter change; the sequence has 2 words.
```

### Constraints
```
1 <= beginWord.length <= 10
endWord.length == beginWord.length
1 <= wordList.length <= 5000
wordList[i].length == beginWord.length
beginWord, endWord, and wordList[i] consist of lowercase English letters.
beginWord != endWord
All the words in wordList are unique.
```

---

## 🧠 Understanding the problem

Think of each word as a **node**. Two nodes share an edge if the words differ by exactly one letter. The question "shortest transformation length" is then "shortest path (in number of nodes) from `beginWord` to `endWord`" on this graph.

Because every edge has the same cost (one letter change), the shortest path is found by **breadth-first search** — BFS explores all words one change away, then two changes away, and so on. The first time we dequeue `endWord`, the number of levels traversed is the answer.

The graph is **implicit**: we never build all edges explicitly (that would be O(N²·L) to compare every pair). Instead, given a word, we **generate its neighbors on the fly** by trying all 26 letters in each of its `L` positions and keeping those present in the dictionary. We mark words used (remove from the set) so we don't revisit them.

`endWord` must be in `wordList`, otherwise no sequence can end there → return 0 immediately.

---

## Approach 1 — BFS generating neighbors by letter swap (recommended) ⭐

### Intuition
Standard BFS for an unweighted shortest path. Seed the queue with `beginWord` at distance 1. Expand a word by mutating each position to every letter `a..z`; any mutation found in the dictionary is a neighbor. Remove neighbors as you enqueue them to prevent re-processing.

### Algorithm
1. Put `wordList` into a hash set `dict`. If `endWord ∉ dict` → return 0.
2. BFS from `beginWord` with `steps = 1`.
3. For each word popped: if it equals `endWord`, return `steps`. Otherwise for each position and each letter `a..z`, build a candidate; if it is in `dict`, erase it and enqueue it.
4. Increment `steps` per BFS level. If the queue empties, return 0.

### Dry run on Example 1
```
dict = {hot,dot,dog,lot,log,cog}. endWord=cog present.
Level 1: [hit] (steps=1). hit→hot in dict → enqueue.
Level 2: [hot] (steps=2). hot→dot, lot → enqueue.
Level 3: [dot,lot] (steps=3). dot→dog; lot→log → enqueue.
Level 4: [dog,log] (steps=4). dog→cog; log→cog (already removed) → enqueue cog.
Level 5: [cog] (steps=5) == endWord → return 5.
```

### Code

```cpp
class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> dict(wordList.begin(), wordList.end());
        if (!dict.count(endWord)) return 0;
        queue<string> q;
        q.push(beginWord);
        int steps = 1;
        while (!q.empty()) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                string w = q.front(); q.pop();
                if (w == endWord) return steps;
                for (int j = 0; j < (int)w.size(); j++) {
                    char orig = w[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        w[j] = c;
                        if (dict.count(w)) {
                            dict.erase(w);
                            q.push(w);
                        }
                    }
                    w[j] = orig;
                }
            }
            steps++;
        }
        return 0;
    }
};
```
```java
class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> dict = new HashSet<>(wordList);
        if (!dict.contains(endWord)) return 0;
        Queue<String> q = new LinkedList<>();
        q.offer(beginWord);
        int steps = 1;
        while (!q.isEmpty()) {
            int sz = q.size();
            for (int i = 0; i < sz; i++) {
                String w = q.poll();
                if (w.equals(endWord)) return steps;
                char[] arr = w.toCharArray();
                for (int j = 0; j < arr.length; j++) {
                    char orig = arr[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        arr[j] = c;
                        String cand = new String(arr);
                        if (dict.contains(cand)) {
                            dict.remove(cand);
                            q.offer(cand);
                        }
                    }
                    arr[j] = orig;
                }
            }
            steps++;
        }
        return 0;
    }
}
```
```python
from collections import deque

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        dict_ = set(wordList)
        if endWord not in dict_:
            return 0
        q = deque([beginWord])
        steps = 1
        while q:
            for _ in range(len(q)):
                word = q.popleft()
                if word == endWord:
                    return steps
                for j in range(len(word)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        cand = word[:j] + c + word[j + 1:]
                        if cand in dict_:
                            dict_.remove(cand)
                            q.append(cand)
            steps += 1
        return 0
```

### Complexity
- **Time**: O(N · L² · 26) where N = number of words, L = word length. For each word we try `L · 26` mutations, each costing O(L) to build/hash.
- **Space**: O(N · L) for the dictionary and queue.

---

## Approach 2 — Bidirectional BFS

### Intuition
BFS explores a frontier that grows roughly like `branching^depth`. Searching **from both ends simultaneously** and meeting in the middle cuts the explored depth roughly in half, often a dramatic speedup. Always expand the smaller frontier to keep work balanced.

### Algorithm
1. If `endWord ∉ dict` → return 0.
2. Maintain two sets, `beginSet = {beginWord}` and `endSet = {endWord}`, and `steps = 1`.
3. Each round: expand the smaller set into `nextSet` by mutating each word; if any mutation is in the *other* set, the searches meet → return `steps + 1`. Add valid new mutations (in `dict`, mark visited) to `nextSet`.
4. Replace the smaller set with `nextSet`, `steps++`. Stop when either set is empty (return 0).

### Dry run on Example 1 (sketch)
```
beginSet={hit}, endSet={cog}, steps=1.
Expand begin → {hot}. Not in endSet. steps=2. beginSet={hot}.
endSet smaller? equal → expand cog → {dog,log}. steps=3. endSet={dog,log}.
Expand begin {hot} → {dot,lot}. steps=4. beginSet={dot,lot}.
Expand endSet {dog,log} → produces dot/lot which ARE in beginSet → meet → return 4+1=5.
```

### Code

```cpp
class Solution {
public:
    int ladderLength(string beginWord, string endWord, vector<string>& wordList) {
        unordered_set<string> dict(wordList.begin(), wordList.end());
        if (!dict.count(endWord)) return 0;
        unordered_set<string> beginSet{beginWord}, endSet{endWord};
        int steps = 1;
        while (!beginSet.empty() && !endSet.empty()) {
            if (beginSet.size() > endSet.size()) swap(beginSet, endSet);
            unordered_set<string> nextSet;
            for (string w : beginSet) {
                for (int j = 0; j < (int)w.size(); j++) {
                    char orig = w[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        w[j] = c;
                        if (endSet.count(w)) return steps + 1;
                        if (dict.count(w)) {
                            dict.erase(w);
                            nextSet.insert(w);
                        }
                    }
                    w[j] = orig;
                }
            }
            beginSet = nextSet;
            steps++;
        }
        return 0;
    }
};
```
```java
class Solution {
    public int ladderLength(String beginWord, String endWord, List<String> wordList) {
        Set<String> dict = new HashSet<>(wordList);
        if (!dict.contains(endWord)) return 0;
        Set<String> beginSet = new HashSet<>(), endSet = new HashSet<>();
        beginSet.add(beginWord);
        endSet.add(endWord);
        int steps = 1;
        while (!beginSet.isEmpty() && !endSet.isEmpty()) {
            if (beginSet.size() > endSet.size()) {
                Set<String> tmp = beginSet; beginSet = endSet; endSet = tmp;
            }
            Set<String> nextSet = new HashSet<>();
            for (String word : beginSet) {
                char[] arr = word.toCharArray();
                for (int j = 0; j < arr.length; j++) {
                    char orig = arr[j];
                    for (char c = 'a'; c <= 'z'; c++) {
                        arr[j] = c;
                        String cand = new String(arr);
                        if (endSet.contains(cand)) return steps + 1;
                        if (dict.contains(cand)) {
                            dict.remove(cand);
                            nextSet.add(cand);
                        }
                    }
                    arr[j] = orig;
                }
            }
            beginSet = nextSet;
            steps++;
        }
        return 0;
    }
}
```
```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        dict_ = set(wordList)
        if endWord not in dict_:
            return 0
        begin_set, end_set = {beginWord}, {endWord}
        steps = 1
        while begin_set and end_set:
            if len(begin_set) > len(end_set):
                begin_set, end_set = end_set, begin_set
            next_set = set()
            for word in begin_set:
                for j in range(len(word)):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        cand = word[:j] + c + word[j + 1:]
                        if cand in end_set:
                            return steps + 1
                        if cand in dict_:
                            dict_.remove(cand)
                            next_set.add(cand)
            begin_set = next_set
            steps += 1
        return 0
```

### Complexity
- **Time**: O(N · L² · 26) worst case, but in practice far fewer nodes are expanded than one-directional BFS.
- **Space**: O(N · L).

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| One-directional BFS | O(N·L²·26) | O(N·L) | simplest correct shortest-path ⭐ |
| Bidirectional BFS | O(N·L²·26) worst, much less typical | O(N·L) | meet-in-the-middle; big constant-factor win |

Both are guaranteed shortest because BFS expands by levels. Bidirectional BFS is the optimization to mention when the dictionary is large.

---

## 🧪 Edge cases & pitfalls
- **`endWord` not in the list** → return 0 right away (Example 2).
- **`beginWord` need not be in the list** — never require it to be in `dict`.
- **Remove a word from the dictionary when first reached** — otherwise multiple queue entries cause exponential blowup and wrong (non-shortest) handling.
- **Answer counts words, not edges** — a single change ("a" → "c") is length 2, not 1.
- **Generating neighbors by scanning the whole dictionary per word** (comparing every pair) is O(N²·L) and may TLE for N = 5000; the 26-letter mutation trick is the intended generator.

---

## 🔗 Related problems
- **Word Ladder II** (LC 126) — return *all* shortest sequences (BFS to build layers + DFS to reconstruct).
- **Minimum Genetic Mutation** (LC 433) — identical BFS over gene strings.
- **Open the Lock** (LC 752) — BFS over 4-digit states with dead-ends.
- **Shortest Path in a Grid / Binary Matrix** (LC 1091) — unweighted BFS shortest path.

---

**→ Next:** [`12-Walls-And-Gates.md`](./12-Walls-And-Gates.md) | **← Prev:** [`10-Redundant-Connection.md`](./10-Redundant-Connection.md) | [Problem set index](./00-Index.md)
