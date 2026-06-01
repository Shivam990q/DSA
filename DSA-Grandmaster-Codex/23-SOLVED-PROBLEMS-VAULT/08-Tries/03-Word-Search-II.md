# Word Search II

**Platform**: LeetCode 212 · **Difficulty**: Hard · **Topics**: Array, String, Backtracking, Trie, Matrix · **Pattern**: Trie-driven board DFS

---

## 📜 Problem Statement

Given an `m x n` board of characters and a list of strings `words`, return *all words on the board*.

Each word must be constructed from letters of **sequentially adjacent** cells, where adjacent cells are horizontally or vertically neighboring. The **same letter cell may not be used more than once** in a word.

### Examples

**Example 1:**
```
Input:
board = [["o","a","a","n"],
         ["e","t","a","e"],
         ["i","h","k","r"],
         ["i","f","l","v"]]
words = ["oath","pea","eat","rain"]

Output: ["eat","oath"]

Explanation:
"oath": o(0,0) → a(0,1) → t(1,1) → h(2,1)  — all adjacent, no reuse.
"eat":  e(1,0) → a(1,1)? no... e(1,3) → a(0,3)? ... one valid path exists, so "eat" is found.
"pea" and "rain" cannot be formed.
```

**Example 2:**
```
Input:
board = [["a","b"],
         ["c","d"]]
words = ["abcb"]

Output: []

Explanation: "abcb" would need to reuse the cell 'b', which is not allowed.
```

**Example 3:**
```
Input:
board = [["a"]]
words = ["a"]

Output: ["a"]

Explanation: A single cell forms the single-letter word "a".
```

### Constraints
```
m == board.length
n == board[i].length
1 <= m, n <= 12
board[i][j] is a lowercase English letter.
1 <= words.length <= 3 * 10^4
1 <= words[i].length <= 10
words[i] consists of lowercase English letters.
All the strings of words are unique.
```

---

## 🧠 Understanding the problem

This is the multi-word cousin of **Word Search (LC 79)**. There, we searched the board for **one** word. Here we have up to 30,000 words and must return every one that appears.

The naive instinct — run the single-word DFS once per word — is far too slow. Two words like `"oath"` and `"oat"` share the prefix `"oat"`, yet a per-word search re-explores that prefix from scratch for each. With 30,000 words and a 12×12 board, this explodes.

The key realization: **the words share prefixes, and a trie stores shared prefixes exactly once.** So instead of asking "where is word W?" for each W, we walk the **board** once and, at every step, ask "is the path I've spelled so far still a prefix of *some* word?" The trie answers that in O(1) per character. The instant the current path isn't a prefix of any word, we prune the entire branch — no point continuing.

So we flip the loop: iterate over board cells (not words), and let the trie drive the DFS. A node in the trie marked as a word end means "the path that brought me here is a complete word — collect it."

---

## Approach 1 — DFS the board once per word (baseline)

### Intuition
Reuse the LC 79 single-word search. For each word, try to find a path on the board that spells it, starting from every cell. Collect the words that succeed.

### Algorithm
1. For each `word` in `words`:
   - For each starting cell `(r, c)`: run a backtracking DFS that matches `word` character by character, marking visited cells and unmarking on the way out.
   - If any start succeeds, add `word` to the result and stop searching for it.

### Dry run on board with "oath"
```
For "oath": try every start cell.
  start (0,0)='o' matches word[0] → go to neighbors for 'a'
    (0,1)='a' matches → neighbors for 't'
      (1,1)='t' matches → neighbors for 'h'
        (2,1)='h' matches → word complete → found "oath"
Repeat the whole machinery independently for "pea", "eat", "rain".
```
Notice "oath" and (hypothetically) "oat" would each redo the `o→a→t` walk.

### Code
```cpp
class Solution {
    int R, C;
    bool dfs(vector<vector<char>>& b, int r, int c, const string& w, int idx) {
        if (idx == (int)w.size()) return true;
        if (r < 0 || c < 0 || r >= R || c >= C || b[r][c] != w[idx]) return false;
        char tmp = b[r][c];
        b[r][c] = '#';                      // mark visited
        bool found = dfs(b, r+1, c, w, idx+1) || dfs(b, r-1, c, w, idx+1)
                  || dfs(b, r, c+1, w, idx+1) || dfs(b, r, c-1, w, idx+1);
        b[r][c] = tmp;                      // restore
        return found;
    }
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        R = board.size(); C = board[0].size();
        vector<string> res;
        for (const string& w : words) {
            bool ok = false;
            for (int r = 0; r < R && !ok; r++)
                for (int c = 0; c < C && !ok; c++)
                    if (dfs(board, r, c, w, 0)) ok = true;
            if (ok) res.push_back(w);
        }
        return res;
    }
};
```
```java
class Solution {
    private int R, C;

    public List<String> findWords(char[][] board, String[] words) {
        R = board.length; C = board[0].length;
        List<String> res = new ArrayList<>();
        for (String w : words) {
            boolean ok = false;
            for (int r = 0; r < R && !ok; r++)
                for (int c = 0; c < C && !ok; c++)
                    if (dfs(board, r, c, w, 0)) ok = true;
            if (ok) res.add(w);
        }
        return res;
    }
    private boolean dfs(char[][] b, int r, int c, String w, int idx) {
        if (idx == w.length()) return true;
        if (r < 0 || c < 0 || r >= R || c >= C || b[r][c] != w.charAt(idx)) return false;
        char tmp = b[r][c];
        b[r][c] = '#';
        boolean found = dfs(b, r+1, c, w, idx+1) || dfs(b, r-1, c, w, idx+1)
                     || dfs(b, r, c+1, w, idx+1) || dfs(b, r, c-1, w, idx+1);
        b[r][c] = tmp;
        return found;
    }
}
```
```python
class Solution:
    def findWords(self, board, words):
        R, C = len(board), len(board[0])

        def dfs(r, c, w, idx):
            if idx == len(w):
                return True
            if r < 0 or c < 0 or r >= R or c >= C or board[r][c] != w[idx]:
                return False
            tmp = board[r][c]
            board[r][c] = '#'
            found = (dfs(r+1, c, w, idx+1) or dfs(r-1, c, w, idx+1) or
                     dfs(r, c+1, w, idx+1) or dfs(r, c-1, w, idx+1))
            board[r][c] = tmp
            return found

        res = []
        for w in words:
            if any(dfs(r, c, w, 0) for r in range(R) for c in range(C)):
                res.append(w)
        return res
```

### Complexity
- **Time**: O(W · R · C · 4^L) where W = number of words, L = max word length. Restarts the full board search for every word with no prefix sharing.
- **Space**: O(L) recursion depth.

### Verdict
Correct, but with W up to 3·10⁴ it will **TLE**. It throws away the single biggest piece of available structure: the words' shared prefixes. That observation points straight at a trie.

---

## Approach 2 — Trie + single board DFS (optimal) ⭐

### Intuition
Insert **all** words into a trie. Now DFS the board **once**, and at each cell descend the trie by the cell's letter. The trie node tells us instantly whether the path so far is a live prefix:

- If the current letter is not a child of the current trie node → this path matches no word → **prune** (return immediately).
- If the node we land on is a word end → we've found a complete word → collect it.

Two crucial optimizations make this fast:
1. **Store the full word at the terminal node** (instead of a bare `isEnd` boolean). When we hit it, we can append the word directly — no need to reconstruct the path.
2. **De-duplicate found words** by clearing the stored word once collected (set it to null/empty). This also lets us prune even harder. An advanced version prunes leaf nodes after collection, but clearing the word is enough to avoid duplicate results.

The trie walks in lockstep with the board DFS, so a shared prefix like `"oat"` is traversed only once even if many words share it.

### Algorithm
1. **Build the trie**: for each word, walk/create nodes; at the terminal node store `node.word = word`.
2. **DFS from every cell** `(r, c)` starting at the trie root:
   - Read `ch = board[r][c]`. If `ch` is `'#'` (visited) or `root` has no child `ch` → return.
   - Descend `node = node.children[ch]`.
   - If `node.word` is non-empty → add it to results and clear it (avoid duplicates).
   - Mark `board[r][c] = '#'`; recurse into the 4 neighbors with `node`; restore the cell.
3. Return the collected words.

### Dry run
```
words = ["oath","eat"]  → trie:
  root -o-> -a-> -t-> -h(word="oath")
  root -e-> -a-> -t(word="eat")

DFS at (0,0)='o':
  root has child 'o' → node = o-node, mark (0,0)='#'
  neighbor (0,1)='a': o-node has child 'a' → node = a-node, mark
    neighbor (1,1)='t': a-node has child 't' → node = t-node, mark
      neighbor (2,1)='h': t-node has child 'h' → node = h-node; h-node.word="oath"
        → collect "oath", clear it; continue (children empty) → unwind, restore cells

DFS reaches some 'e' cell similarly and spells "eat" → collected.
Remaining starts that don't match any trie child are pruned at the first letter.
Result: ["oath","eat"]
```

### Code
```cpp
class Solution {
    struct Node {
        Node* children[26] = {};
        string word;                 // non-empty only at a word end
    };
    Node* root;
    int R, C;
    vector<string> res;

    void insert(const string& w) {
        Node* cur = root;
        for (char c : w) {
            int i = c - 'a';
            if (!cur->children[i]) cur->children[i] = new Node();
            cur = cur->children[i];
        }
        cur->word = w;
    }
    void dfs(vector<vector<char>>& b, int r, int c, Node* node) {
        if (r < 0 || c < 0 || r >= R || c >= C) return;
        char ch = b[r][c];
        if (ch == '#') return;
        Node* nxt = node->children[ch - 'a'];
        if (!nxt) return;            // prefix not in trie → prune
        if (!nxt->word.empty()) {
            res.push_back(nxt->word);
            nxt->word.clear();       // avoid duplicate collection
        }
        b[r][c] = '#';
        dfs(b, r+1, c, nxt); dfs(b, r-1, c, nxt);
        dfs(b, r, c+1, nxt); dfs(b, r, c-1, nxt);
        b[r][c] = ch;
    }
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        root = new Node();
        R = board.size(); C = board[0].size();
        for (const string& w : words) insert(w);
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                dfs(board, r, c, root);
        return res;
    }
};
```
```java
class Solution {
    private static class Node {
        Node[] children = new Node[26];
        String word = null;          // non-null only at a word end
    }
    private Node root;
    private int R, C;
    private List<String> res;

    public List<String> findWords(char[][] board, String[] words) {
        root = new Node();
        R = board.length; C = board[0].length;
        res = new ArrayList<>();
        for (String w : words) insert(w);
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++)
                dfs(board, r, c, root);
        return res;
    }
    private void insert(String w) {
        Node cur = root;
        for (char c : w.toCharArray()) {
            int i = c - 'a';
            if (cur.children[i] == null) cur.children[i] = new Node();
            cur = cur.children[i];
        }
        cur.word = w;
    }
    private void dfs(char[][] b, int r, int c, Node node) {
        if (r < 0 || c < 0 || r >= R || c >= C) return;
        char ch = b[r][c];
        if (ch == '#') return;
        Node nxt = node.children[ch - 'a'];
        if (nxt == null) return;     // prune
        if (nxt.word != null) {
            res.add(nxt.word);
            nxt.word = null;         // avoid duplicates
        }
        b[r][c] = '#';
        dfs(b, r+1, c, nxt); dfs(b, r-1, c, nxt);
        dfs(b, r, c+1, nxt); dfs(b, r, c-1, nxt);
        b[r][c] = ch;
    }
}
```
```python
class Solution:
    def findWords(self, board, words):
        root = {}
        for w in words:                 # build trie; '$' holds the full word
            cur = root
            for c in w:
                cur = cur.setdefault(c, {})
            cur['$'] = w

        R, C = len(board), len(board[0])
        res = []

        def dfs(r, c, node):
            if r < 0 or c < 0 or r >= R or c >= C:
                return
            ch = board[r][c]
            if ch == '#' or ch not in node:
                return                  # visited or prefix not in trie → prune
            nxt = node[ch]
            if '$' in nxt:
                res.append(nxt['$'])
                del nxt['$']            # avoid duplicate collection
            board[r][c] = '#'
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dfs(r + dr, c + dc, nxt)
            board[r][c] = ch

        for r in range(R):
            for c in range(C):
                dfs(r, c, root)
        return res
```

### Complexity
- **Time**: O(W · L) to build the trie, plus O(R · C · 4^Lmax) for the board DFS in the worst case — but pruning by the trie makes the practical cost dramatically lower, since branches die the instant they leave the trie. (`L` ≤ 10 here.)
- **Space**: O(W · L) for the trie + O(Lmax) recursion stack.

### Verdict
**The intended Hard answer.** Flipping the loop from "per word" to "per board cell, driven by a trie" is the whole insight. Shared prefixes are explored once and dead ends are pruned immediately. Storing the word at the terminal node and clearing it on collection keeps results clean without a separate visited-words set.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Prefix sharing | When to mention |
|----------|------|-------|----------------|-----------------|
| Per-word board DFS | O(W·R·C·4^L) | O(L) | none | baseline / will TLE |
| Trie + single board DFS | ~O(R·C·4^L) with heavy pruning, +O(W·L) build | O(W·L) | full ⭐ | the optimal answer |

The baseline pays the full board-search cost once per word. The trie pays it (roughly) once *total*, sharing every common prefix and pruning the moment a path leaves the dictionary.

---

## 🧪 Edge cases & pitfalls
- **Duplicate results**: the same word can be reachable from multiple board paths. Clearing the stored word (or marking the node) after the first collection prevents adding it twice. The problem guarantees unique input words, so per-word dedup is sufficient.
- **Restore the cell after recursion**: forgetting `board[r][c] = ch` corrupts the board for subsequent DFS roots. Mark before recursing, restore after.
- **Single-cell board / single-letter words**: a word of length 1 is collected immediately when its letter is the starting cell — make sure the word-end check happens *after* descending, before recursing.
- **Pitfall — using a plain `isEnd` boolean**: then on a hit you must reconstruct the path string. Storing the full word at the terminal node avoids that bookkeeping entirely.
- **Pitfall — not pruning**: if you keep recursing even when `node.children[ch]` is null, you've rebuilt the slow per-word search. The early `return` on a missing child *is* the optimization.
- **Advanced optimization (optional)**: after collecting a word, you can prune leaf trie nodes (children-empty) on the way up to shrink the trie and speed later searches. Not required to pass, but a strong talking point.

---

## 🔗 Related problems
- **Word Search** (LC 79) — the single-word version; the building block of the baseline here.
- **Implement Trie (Prefix Tree)** (LC 208) — the trie this solution is built on.
- **Design Add and Search Words** (LC 211) — trie + DFS over a pattern instead of a grid. *(previous file)*
- **Concatenated Words** (LC 472) — trie / DP over a word list.
- **Number of Islands** (LC 200) — pure grid DFS without the trie layer, good contrast for the traversal mechanics.

---

**→ Next:** [`../09-Heap-Priority-Queue/00-Index.md`](../09-Heap-Priority-Queue/00-Index.md) | **← Prev:** [`02-Add-And-Search-Word.md`](./02-Add-And-Search-Word.md) | Back to [`00-Index.md`](./00-Index.md)
