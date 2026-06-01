# Implement Trie (Prefix Tree)

**Platform**: LeetCode 208 · **Difficulty**: Medium · **Topics**: Hash Table, String, Design, Trie · **Pattern**: Prefix tree

---

## 📜 Problem Statement

A **trie** (pronounced as "try") or **prefix tree** is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the `Trie` class:

- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts the string `word` into the trie.
- `boolean search(String word)` Returns `true` if the string `word` is in the trie (i.e., was inserted before), and `false` otherwise.
- `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string `word` that has the prefix `prefix`, and `false` otherwise.

### Examples

**Example 1:**
```
Input:
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]

Output:
[null, null, true, false, true, null, true]

Explanation:
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");     // returns True
trie.search("app");       // returns False  (only "apple" was inserted, "app" is a prefix not a word)
trie.startsWith("app");   // returns True   ("apple" has prefix "app")
trie.insert("app");
trie.search("app");       // returns True   (now "app" itself was inserted)
```

**Example 2:**
```
Input:
["Trie", "insert", "startsWith", "search"]
[[], ["abc"], ["abcd"], ["abc"]]

Output:
[null, null, false, true]

Explanation:
"abcd" is longer than the only stored word "abc", so no stored word has it as a prefix.
"abc" was inserted, so search returns true.
```

**Example 3:**
```
Input:
["Trie", "search", "startsWith"]
[[], ["a"], ["a"]]

Output:
[null, false, false]

Explanation: Nothing was inserted yet, so every query is false.
```

### Constraints
```
1 <= word.length, prefix.length <= 2000
word and prefix consist only of lowercase English letters.
At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.
```

---

## 🧠 Understanding the problem

Three operations, and the subtle distinction is between `search` and `startsWith`:

- `search("app")` is `true` **only if the exact word `"app"` was inserted**.
- `startsWith("app")` is `true` if **any** inserted word *begins* with `"app"` (it could be `"apple"`, `"apply"`, `"app"` itself, …).

That distinction is the whole reason we need a node-level "this path spells a complete word" flag. Walking the structure tells us the prefix exists; the flag tells us whether a *word* ends there.

The alphabet is fixed: 26 lowercase letters. That bounds each node's fan-out to 26, which lets us pick between a fixed-size array (fast, more memory) or a hash map (lazy, less memory). Every operation should run in **O(L)** where `L` is the length of the query string — independent of how many words we have stored. That independence from the dataset size is the trie's superpower.

---

## Approach 1 — Hash set of words (baseline, fails `startsWith`)

### Intuition
The lazy first instinct: dump every inserted word into a hash set. `search` becomes a single O(L) membership test. The catch is `startsWith` — a hash set only knows *exact* keys, so to answer "does any word start with this prefix?" we must scan **every** stored word and test its prefix.

### Algorithm
1. Keep a `HashSet<String> words`.
2. `insert(word)` → add to the set.
3. `search(word)` → return `words.contains(word)`.
4. `startsWith(prefix)` → iterate over all stored words; return `true` if any one starts with `prefix`.

### Dry run on insert("apple"), startsWith("app")
```
words = {"apple"}
startsWith("app"): scan set → "apple".startsWith("app") == true → return true
```
Correct — but the scan in step 4 touches every word. With up to 3·10⁴ words each up to length 2000, repeated `startsWith` calls degrade to O(N·L) per call.

### Code
```cpp
class Trie {
    unordered_set<string> words;
public:
    Trie() {}
    void insert(string word) {
        words.insert(word);
    }
    bool search(string word) {
        return words.count(word) > 0;
    }
    bool startsWith(string prefix) {
        for (const string& w : words)
            if (w.size() >= prefix.size() &&
                w.compare(0, prefix.size(), prefix) == 0)
                return true;
        return false;
    }
};
```
```java
class Trie {
    private Set<String> words;

    public Trie() {
        words = new HashSet<>();
    }
    public void insert(String word) {
        words.add(word);
    }
    public boolean search(String word) {
        return words.contains(word);
    }
    public boolean startsWith(String prefix) {
        for (String w : words)
            if (w.startsWith(prefix)) return true;
        return false;
    }
}
```
```python
class Trie:
    def __init__(self):
        self.words = set()

    def insert(self, word: str) -> None:
        self.words.add(word)

    def search(self, word: str) -> bool:
        return word in self.words

    def startsWith(self, prefix: str) -> bool:
        return any(w.startswith(prefix) for w in self.words)
```

### Complexity
- **Time**: `insert` O(L), `search` O(L) average, `startsWith` **O(N·L)** — scans all N stored words.
- **Space**: O(total characters stored).

### Verdict
Passes correctness but `startsWith` does not scale; it defeats the entire purpose of the problem. It exists only to show *why* we need a structure that shares prefixes. On to the real trie.

---

## Approach 2 — Array-of-26 trie (optimal) ⭐

### Intuition
Store words **character by character along tree edges**. The word `"apple"` becomes a path `root → a → p → p → l → e`, and the node at the end of that path is marked `isEnd = true`. Inserting `"app"` reuses the first three nodes and marks the third one as a word end too. Now:

- `startsWith(prefix)` = can I *walk* the path for `prefix` without falling off the tree?
- `search(word)` = can I walk the path **and** is the final node flagged `isEnd`?

Because each node has at most 26 children and we only ever follow `L` edges, every operation is O(L), totally independent of how many words live in the trie.

### Algorithm
**Node**: 26 child pointers (index `c - 'a'`) plus a boolean `isEnd`.

`insert(word)`:
1. `cur = root`.
2. For each char `c`: if `cur.children[c]` is null, create it; descend `cur = cur.children[c]`.
3. After the loop, set `cur.isEnd = true`.

`search(word)`:
1. Walk the path; if any child is missing, return `false`.
2. Return `cur.isEnd`.

`startsWith(prefix)`:
1. Walk the path; if any child is missing, return `false`.
2. Return `true` (we reached the end of the prefix; existence is enough).

### Dry run
```
insert("apple"):
  root -a-> n1 -p-> n2 -p-> n3 -l-> n4 -e-> n5 ; n5.isEnd = true

search("apple"):
  walk a,p,p,l,e → reach n5 → n5.isEnd == true → return true

search("app"):
  walk a,p,p → reach n3 → n3.isEnd == false → return false

startsWith("app"):
  walk a,p,p → reach n3 (no missing child) → return true

insert("app"):
  walk a,p,p → reach n3 → set n3.isEnd = true

search("app"):
  walk a,p,p → reach n3 → n3.isEnd == true → return true
```

### Code
```cpp
class Trie {
    struct Node {
        Node* children[26] = {};   // all 26 initialized to nullptr
        bool isEnd = false;
    };
    Node* root;
public:
    Trie() {
        root = new Node();
    }
    void insert(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->isEnd = true;
    }
    bool search(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return cur->isEnd;
    }
    bool startsWith(string prefix) {
        Node* cur = root;
        for (char c : prefix) {
            int i = c - 'a';
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return true;
    }
};
```
```java
class Trie {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd = false;
    }
    private final Node root;

    public Trie() {
        root = new Node();
    }
    public void insert(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) cur.children[i] = new Node();
            cur = cur.children[i];
        }
        cur.isEnd = true;
    }
    public boolean search(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) return false;
            cur = cur.children[i];
        }
        return cur.isEnd;
    }
    public boolean startsWith(String prefix) {
        Node cur = root;
        for (char c : prefix.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) return false;
            cur = cur.children[i];
        }
        return true;
    }
}
```
```python
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            i = ord(c) - ord('a')
            if cur.children[i] is None:
                cur.children[i] = TrieNode()
            cur = cur.children[i]
        cur.is_end = True

    def search(self, word: str) -> bool:
        cur = self.root
        for c in word:
            i = ord(c) - ord('a')
            if cur.children[i] is None:
                return False
            cur = cur.children[i]
        return cur.is_end

    def startsWith(self, prefix: str) -> bool:
        cur = self.root
        for c in prefix:
            i = ord(c) - ord('a')
            if cur.children[i] is None:
                return False
            cur = cur.children[i]
        return True
```

### Complexity
- **Time**: `insert`, `search`, `startsWith` all **O(L)** where L is the length of the argument. No dependence on the number of stored words.
- **Space**: O(total characters inserted × 26) worst case for the fixed arrays; in practice the 26-slot arrays make each node heavier but lookups are a single index.

### Verdict
**The canonical answer.** Constant-factor-fast because child lookup is a raw array index. This is what you write in an interview.

---

## Approach 3 — Hash-map trie (memory-friendly variant)

### Intuition
Most nodes don't actually use all 26 children — a fixed array of 26 pointers wastes memory on sparse tries (e.g., long words sharing little). Swap the fixed array for a hash map `char → Node` that only allocates entries that are actually used. The algorithm is byte-for-byte identical; only the child container changes.

### Algorithm
Same three walks as Approach 2, but child access is `cur.children.get(c)` / `setdefault` instead of an array index. Useful when the alphabet is large (Unicode, mixed case, digits) or the trie is sparse.

### Dry run
Identical traversal to Approach 2; the only difference is that a node for `"apple"` stores exactly the keys `{'a'}`, `{'p'}`, … rather than a 26-length array with 25 nulls.

### Code
```cpp
class Trie {
    struct Node {
        unordered_map<char, Node*> children;
        bool isEnd = false;
    };
    Node* root;
public:
    Trie() {
        root = new Node();
    }
    void insert(string word) {
        Node* cur = root;
        for (char c : word) {
            if (!cur->children.count(c)) cur->children[c] = new Node();
            cur = cur->children[c];
        }
        cur->isEnd = true;
    }
    bool search(string word) {
        Node* cur = root;
        for (char c : word) {
            auto it = cur->children.find(c);
            if (it == cur->children.end()) return false;
            cur = it->second;
        }
        return cur->isEnd;
    }
    bool startsWith(string prefix) {
        Node* cur = root;
        for (char c : prefix) {
            auto it = cur->children.find(c);
            if (it == cur->children.end()) return false;
            cur = it->second;
        }
        return true;
    }
};
```
```java
class Trie {
    private static class Node {
        Map<Character, Node> children = new HashMap<>();
        boolean isEnd = false;
    }
    private final Node root;

    public Trie() {
        root = new Node();
    }
    public void insert(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            cur.children.putIfAbsent(c, new Node());
            cur = cur.children.get(c);
        }
        cur.isEnd = true;
    }
    public boolean search(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            cur = cur.children.get(c);
            if (cur == null) return false;
        }
        return cur.isEnd;
    }
    public boolean startsWith(String prefix) {
        Node cur = root;
        for (char c : prefix.toCharArray()) {
            cur = cur.children.get(c);
            if (cur == null) return false;
        }
        return true;
    }
}
```
```python
class Trie:
    def __init__(self):
        self.root = {}          # nested dicts; '$' marks a word end

    def insert(self, word: str) -> None:
        cur = self.root
        for c in word:
            cur = cur.setdefault(c, {})
        cur['$'] = True

    def search(self, word: str) -> bool:
        cur = self.root
        for c in word:
            if c not in cur:
                return False
            cur = cur[c]
        return '$' in cur

    def startsWith(self, prefix: str) -> bool:
        cur = self.root
        for c in prefix:
            if c not in cur:
                return False
            cur = cur[c]
        return True
```

### Complexity
- **Time**: O(L) per operation (hash lookup is O(1) average).
- **Space**: O(total characters inserted) — only allocates children that exist, so much leaner on sparse tries.

### Verdict
The pragmatic choice when the alphabet is big or the trie is sparse. Slightly higher constant factor than the array version (hashing vs. indexing) but lighter memory. Functionally equivalent.

---

## ⚖️ Approach comparison

| Approach | insert | search | startsWith | Space | When to mention |
|----------|--------|--------|------------|-------|-----------------|
| Hash set of words | O(L) | O(L) | **O(N·L)** | O(chars) | only to motivate the trie |
| Array-26 trie | O(L) | O(L) | O(L) | O(chars·26) | default optimal answer ⭐ |
| Hash-map trie | O(L) | O(L) | O(L) | O(chars) | large/sparse alphabet, tighter memory |

The headline trade-off: the hash set makes `search` trivial but cannot answer prefix queries efficiently. The trie shares prefixes, making every operation O(L) regardless of dataset size. Array vs. hash-map trie is a pure **speed-vs-memory** dial within the same algorithm.

---

## 🧪 Edge cases & pitfalls
- **Prefix that is also a word**: insert `"apple"`, then `search("app")` must be `false` while `startsWith("app")` is `true`. This is exactly why the `isEnd` flag is non-negotiable — without it you cannot distinguish a word from a mere prefix.
- **Empty-string queries**: the constraints guarantee length ≥ 1, but a robust implementation returns `isEnd` of the root for an empty `search` and `true` for an empty `startsWith` (every word has the empty prefix).
- **Duplicate inserts**: inserting the same word twice is harmless — you re-walk the same path and re-set `isEnd = true`.
- **Pitfall — forgetting to mark `isEnd`**: if you only build nodes but never set the terminal flag, `search` always returns `false`.
- **Pitfall — `search` returning `true` for any walkable path**: that's the `startsWith` behavior. Remember `search` must check `isEnd`, `startsWith` must not.
- **Pitfall (C++)**: leaving the 26-pointer array uninitialized. `Node* children[26] = {}` zero-initializes; a bare `Node* children[26];` contains garbage and will crash.

---

## 🔗 Related problems
- **Design Add and Search Words** (LC 211) — the same trie, but `search` supports a `.` wildcard that branches via DFS. *(next file)*
- **Word Search II** (LC 212) — build a trie of many words, then DFS a grid in lockstep.
- **Replace Words** (LC 648) — insert dictionary roots, then for each word find its shortest stored prefix.
- **Map Sum Pairs** (LC 677) — trie where each terminal stores a value; `startsWith`-style sum query.
- **Longest Word in Dictionary** (LC 720) — trie + check that every prefix is also a word.

---

**→ Next:** [`02-Add-And-Search-Word.md`](./02-Add-And-Search-Word.md) | Back to [`00-Index.md`](./00-Index.md)
