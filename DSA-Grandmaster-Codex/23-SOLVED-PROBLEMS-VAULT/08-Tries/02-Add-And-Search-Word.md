# Design Add and Search Words Data Structure

**Platform**: LeetCode 211 · **Difficulty**: Medium · **Topics**: String, DFS, Design, Trie · **Pattern**: Trie + wildcard DFS

---

## 📜 Problem Statement

Design a data structure that supports adding new words and finding if a string matches any previously added string.

Implement the `WordDictionary` class:

- `WordDictionary()` Initializes the object.
- `void addWord(word)` Adds `word` to the data structure, it can be matched later.
- `bool search(word)` Returns `true` if there is any string in the data structure that matches `word` or `false` otherwise. `word` may contain dots `'.'` where dots can be matched with **any** letter.

### Examples

**Example 1:**
```
Input:
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]

Output:
[null,null,null,null,false,true,true,true]

Explanation:
WordDictionary wd = new WordDictionary();
wd.addWord("bad");
wd.addWord("dad");
wd.addWord("mad");
wd.search("pad");   // return False — "pad" was never added
wd.search("bad");   // return True
wd.search(".ad");   // return True — matches "bad", "dad", and "mad"
wd.search("b..");   // return True — matches "bad"
```

**Example 2:**
```
Input:
["WordDictionary","addWord","search","search"]
[[],["a"],["a"],["."]]

Output:
[null,null,true,true]

Explanation:
"a" matches the stored word "a".
"." matches any single letter, and "a" is one letter long, so it matches.
```

**Example 3:**
```
Input:
["WordDictionary","addWord","search"]
[[],["ab"],["a."]]

Output:
[null,null,true]

Explanation: "a." matches "ab" — 'a' is literal, '.' matches 'b'.
```

### Constraints
```
1 <= word.length <= 25
word in addWord consists of lowercase English letters.
word in search consists of '.' or lowercase English letters.
There will be at most 2 dots in word for search queries when calling search.
At most 10^4 calls will be made to addWord and search.
```

---

## 🧠 Understanding the problem

This is **Implement Trie** with one twist: the search query can contain `'.'`, a wildcard that matches any single letter. Everything about insertion is unchanged — `addWord` builds the same character-by-character path with an `isEnd` flag.

The interesting part is `search`. For a normal letter we follow exactly one edge, just like before. For a `'.'` we don't know which edge to follow, so we must **try all of them** — branch into every existing child and ask "does the rest of the pattern match from here?" That branching is naturally a **DFS / recursion**: the pattern position is the recursion index, and the current trie node is the recursion state.

A subtle but critical detail: a `'.'` matches **exactly one** character, not zero or many. So `".ad"` must match three-letter words only, and the recursion must reach the end of the pattern *and* land on a node with `isEnd = true`. Matching the pattern but stopping at a non-terminal node is a failure.

The constraints (≤ 2 dots, length ≤ 25) keep the branching tame, so the simple DFS is plenty fast.

---

## Approach 1 — Store words in a list, match with wildcard scan (baseline)

### Intuition
Forget tries for a moment. Keep every added word in a list. For `search`, compare the pattern against each stored word of the same length, treating `'.'` as "always matches." Return `true` on the first full match.

### Algorithm
1. `addWord(word)` → append to a list.
2. `search(pattern)` → for each stored `w` with `len(w) == len(pattern)`:
   - Compare position by position; a `'.'` matches anything, a letter must match exactly.
   - If all positions matched, return `true`.
3. Return `false`.

### Dry run on words ["bad","dad","mad"], search(".ad")
```
".ad" length 3.
 vs "bad": '.'~'b' ok, 'a'=='a' ok, 'd'=='d' ok → MATCH → return true
```

### Code
```cpp
class WordDictionary {
    vector<string> words;
public:
    WordDictionary() {}
    void addWord(string word) {
        words.push_back(word);
    }
    bool search(string word) {
        for (const string& w : words) {
            if (w.size() != word.size()) continue;
            bool ok = true;
            for (int i = 0; i < (int)word.size(); i++) {
                if (word[i] != '.' && word[i] != w[i]) { ok = false; break; }
            }
            if (ok) return true;
        }
        return false;
    }
};
```
```java
class WordDictionary {
    private List<String> words;

    public WordDictionary() {
        words = new ArrayList<>();
    }
    public void addWord(String word) {
        words.add(word);
    }
    public boolean search(String word) {
        for (String w : words) {
            if (w.length() != word.length()) continue;
            boolean ok = true;
            for (int i = 0; i < word.length(); i++) {
                char c = word.charAt(i);
                if (c != '.' && c != w.charAt(i)) { ok = false; break; }
            }
            if (ok) return true;
        }
        return false;
    }
}
```
```python
class WordDictionary:
    def __init__(self):
        self.words = []

    def addWord(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        n = len(word)
        for w in self.words:
            if len(w) != n:
                continue
            if all(word[i] == '.' or word[i] == w[i] for i in range(n)):
                return True
        return False
```

### Complexity
- **Time**: `addWord` O(1). `search` **O(N·L)** — every stored word may be scanned, where N = number of words, L = word length.
- **Space**: O(total characters).

### Verdict
Correct and dead simple. With up to 10⁴ calls and 10⁴ words it can drift toward 10⁸ character comparisons, which is borderline. It also shares zero work between similar words. The trie fixes both by collapsing common prefixes.

---

## Approach 2 — Trie + DFS for wildcards (optimal) ⭐

### Intuition
Build a standard trie on `addWord`. For `search`, recurse through the pattern alongside a trie node:

- **Literal char** `c`: there is only one possible edge. If `node.children[c]` exists, recurse into it at the next pattern index; otherwise fail.
- **Wildcard `'.'`**: any child could be the match. **Try every existing child**; if any one leads to a successful match of the remaining pattern, succeed.
- **End of pattern**: succeed only if the current node has `isEnd = true` (we've spelled a complete stored word).

The trie collapses shared prefixes so a literal walk is O(L), and the wildcard branching is bounded by the number of children (≤ 26) at each dot — with ≤ 2 dots per query, this stays tiny.

### Algorithm
**Node**: 26 children + `isEnd`.

`addWord(word)`: identical to LC 208 insert — walk/create nodes, set `isEnd` at the last node.

`search(pattern)` → `dfs(root, 0)`:
1. If index `== len(pattern)`: return `node.isEnd`.
2. Let `c = pattern[index]`.
3. If `c == '.'`: for every non-null child `ch`, if `dfs(ch, index+1)` is `true`, return `true`; after the loop return `false`.
4. Else: if `node.children[c]` is null, return `false`; otherwise return `dfs(node.children[c], index+1)`.

### Dry run
```
addWord("bad"), addWord("dad"), addWord("mad")
Trie root has children b, d, m, each leading to a→d (isEnd at the 'd' node).

search(".ad") → dfs(root, 0):
  pattern[0]='.' → try every child of root:
    child 'b': dfs(b-node, 1)
       pattern[1]='a' → b-node has child 'a' → dfs(a-node, 2)
          pattern[2]='d' → a-node has child 'd' → dfs(d-node, 3)
             index==3==len → d-node.isEnd == true → return true
    → propagates true up the chain → search returns true

search("pad") → dfs(root, 0):
  pattern[0]='p' literal → root has no child 'p' → return false
```

### Code
```cpp
class WordDictionary {
    struct Node {
        Node* children[26] = {};
        bool isEnd = false;
    };
    Node* root;

    bool dfs(Node* node, const string& word, int idx) {
        if (idx == (int)word.size()) return node->isEnd;
        char c = word[idx];
        if (c == '.') {
            for (int k = 0; k < 26; k++)
                if (node->children[k] && dfs(node->children[k], word, idx + 1))
                    return true;
            return false;
        }
        Node* nxt = node->children[c - 'a'];
        if (!nxt) return false;
        return dfs(nxt, word, idx + 1);
    }
public:
    WordDictionary() {
        root = new Node();
    }
    void addWord(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->isEnd = true;
    }
    bool search(string word) {
        return dfs(root, word, 0);
    }
};
```
```java
class WordDictionary {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd = false;
    }
    private final Node root;

    public WordDictionary() {
        root = new Node();
    }
    public void addWord(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) cur.children[i] = new Node();
            cur = cur.children[i];
        }
        cur.isEnd = true;
    }
    public boolean search(String word) {
        return dfs(root, word, 0);
    }
    private boolean dfs(Node node, String word, int idx) {
        if (idx == word.length()) return node.isEnd;
        char c = word.charAt(idx);
        if (c == '.') {
            for (int k = 0; k < 26; k++)
                if (node.children[k] != null && dfs(node.children[k], word, idx + 1))
                    return true;
            return false;
        }
        Node nxt = node.children[c - 'a'];
        if (nxt == null) return false;
        return dfs(nxt, word, idx + 1);
    }
}
```
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        cur = self.root
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.is_end = True

    def search(self, word: str) -> bool:
        def dfs(node: TrieNode, idx: int) -> bool:
            if idx == len(word):
                return node.is_end
            c = word[idx]
            if c == '.':
                return any(dfs(child, idx + 1) for child in node.children.values())
            if c not in node.children:
                return False
            return dfs(node.children[c], idx + 1)
        return dfs(self.root, 0)
```

### Complexity
- **Time**: `addWord` O(L). `search` O(L) when the pattern has no dots; with `d` dots the worst case is O(26^d · L), but the constraint caps `d ≤ 2`, so it is effectively O(L) with a tiny constant.
- **Space**: O(total characters added) for the trie, plus O(L) recursion stack.

### Verdict
**The intended answer.** A trie for compact storage plus DFS to handle the only twist — wildcards. Clean, fast within the constraints, and a textbook demonstration of "recurse through a structure when one step is non-deterministic."

---

## ⚖️ Approach comparison

| Approach | addWord | search (no dots) | search (with dots) | Space | When to mention |
|----------|---------|------------------|--------------------|-------|-----------------|
| Word list + scan | O(1) | O(N·L) | O(N·L) | O(chars) | only as the baseline |
| Trie + DFS | O(L) | O(L) | O(26^d · L), d ≤ 2 | O(chars) | the optimal answer ⭐ |

The list approach re-scans the entire dataset on every search. The trie shares prefixes so the common case (no dots) is O(L), and the wildcard branching is contained because the alphabet is bounded and dots are few.

---

## 🧪 Edge cases & pitfalls
- **`'.'` matches exactly one character**: `"."` matches `"a"` but not `"ab"` or the empty string. The recursion enforces this because length must line up before the `isEnd` check.
- **Pattern longer/shorter than every word**: if the pattern can't be walked to completion, or completes on a non-terminal node, `search` returns `false` — the `idx == len` base case checks `isEnd`.
- **All dots**: `"..."` matches any stored 3-letter word; it explores up to 26 children per level but the length guard prunes mismatched depths instantly.
- **Pitfall — returning `true` at end of pattern without checking `isEnd`**: that wrongly matches prefixes. The base case must return `node.isEnd`, not `true`.
- **Pitfall — treating `'.'` as zero-or-more**: it is a single-character wildcard (like regex `.`), not `.*`. Don't skip a level or consume multiple.
- **Pitfall — iterating all 26 slots for a literal char**: only branch over all children on a dot. For a literal, follow the single matching edge.

---

## 🔗 Related problems
- **Implement Trie (Prefix Tree)** (LC 208) — the wildcard-free foundation. *(previous file)*
- **Word Search II** (LC 212) — trie + DFS, but over a 2-D grid instead of a pattern string. *(next file)*
- **Regular Expression Matching** (LC 10) — full regex with `.` and `*`, DP/recursion.
- **Wildcard Matching** (LC 44) — `?` and `*` matching, greedy/DP.
- **Short Encoding of Words** (LC 820) — suffix trie to compress a word list.

---

**→ Next:** [`03-Word-Search-II.md`](./03-Word-Search-II.md) | **← Prev:** [`01-Implement-Trie.md`](./01-Implement-Trie.md) | Back to [`00-Index.md`](./00-Index.md)
