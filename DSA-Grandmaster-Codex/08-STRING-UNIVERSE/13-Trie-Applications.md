# 🔤 Trie Applications

> *"The prefix tree: where words become paths, and prefixes become power."*

---

## I. THE TRIE RECAP
A trie stores strings as paths from root. Each node has children (array of 26 for lowercase, or a map). Operations: insert/search/startsWith in O(L) where L = string length.

(Implementation: [`../19-TEMPLATES-AND-IMPLEMENTATIONS/trie.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/trie.cpp))

---

## II. THE APPLICATIONS

### 1. Autocomplete / Typeahead ⭐
Store dictionary in trie. On prefix input, walk to the prefix node, then DFS to collect (or store top-k at each node for ranking).
- LC 1268: Search Suggestions System
- LC 642: Design Search Autocomplete System

### 2. Word dictionaries with wildcards
- LC 211: Add and Search Word (`.` matches any char) — DFS at `.` nodes
- LC 212: Word Search II — Trie + DFS on a board ⭐ (classic: build trie of words, DFS the grid pruning by trie)

### 3. Maximum XOR (Binary Trie) ⭐
Store numbers as 32-bit paths. To maximize XOR with x, greedily go to the opposite bit at each level.
- LC 421: Maximum XOR of Two Numbers
- LC 1707: Maximum XOR With an Element From Array
- LC 1938: Maximum Genetic Difference Query

### 4. Prefix counting / frequency
Store a count at each node = number of words passing through. Answer "how many words start with prefix P" in O(|P|).

### 5. Longest common prefix / word problems
- LC 14: Longest Common Prefix
- LC 648: Replace Words (replace words by shortest root)
- LC 720: Longest Word in Dictionary

### 6. Concatenated / compound words
- LC 472: Concatenated Words (trie + DP)

### 7. Stream of characters
- LC 1032: Stream of Characters (Aho-Corasick = trie + fail links; or reversed trie)

### 8. IP routing (longest prefix match)
Binary trie over IP bits — routers use this to find the longest matching prefix.

---

## III. THE BINARY TRIE (deep dive)
For XOR problems on integers:
```cpp
struct BinaryTrie {
    struct Node { Node* ch[2] = {nullptr, nullptr}; };
    Node* root = new Node();
    void insert(int x) {
        Node* cur = root;
        for (int b = 30; b >= 0; --b) {
            int bit = (x >> b) & 1;
            if (!cur->ch[bit]) cur->ch[bit] = new Node();
            cur = cur->ch[bit];
        }
    }
    int maxXor(int x) {
        Node* cur = root; int ans = 0;
        for (int b = 30; b >= 0; --b) {
            int bit = (x >> b) & 1, opp = bit ^ 1;
            if (cur->ch[opp]) { ans |= (1 << b); cur = cur->ch[opp]; }
            else cur = cur->ch[bit];
        }
        return ans;
    }
};
```

---

## IV. TRIE VARIANTS
- **Compressed trie / Radix tree**: merge single-child chains (saves memory)
- **Ternary search tree**: space-efficient trie variant
- **Suffix trie** → use suffix tree/array/automaton instead (suffix trie is O(n²))
- **Persistent trie**: versioned, for offline XOR queries with constraints

---

## V. COMPLEXITY
- Insert/search/startsWith: O(L)
- Space: O(total characters × alphabet) — can be large; use maps for sparse alphabets

---

## VI. PROBLEMS (curated)
- Implement Trie (LC 208), Add and Search Word (LC 211)
- Word Search II (LC 212) ⭐
- Maximum XOR (LC 421) ⭐
- Replace Words (LC 648), Longest Word in Dictionary (LC 720)
- Search Suggestions System (LC 1268)
- Concatenated Words (LC 472)
- Stream of Characters (LC 1032)
- Map Sum Pairs (LC 677), Word Squares (LC 425)

---

## VII. WHEN TO REACH FOR A TRIE
- Prefix-based queries (autocomplete, prefix count)
- Dictionary lookups with wildcards
- XOR maximization/queries (binary trie)
- Many strings sharing prefixes (space-efficient)

---

**→ Back to:** [`00-Index.md`](./00-Index.md) | All string algorithms → [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)
