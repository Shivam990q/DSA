# 🔤 Aho-Corasick — Multi-Pattern Matching

> *"KMP finds one pattern. Aho-Corasick finds thousands — simultaneously, in one pass."*

---

## I. THE PROBLEM
Given a text T and a dictionary of k patterns, find all occurrences of ALL patterns in O(|T| + total pattern length + number of matches).

---

## II. THE STRUCTURE = TRIE + FAILURE LINKS
1. **Trie** of all patterns (a tree where paths spell patterns).
2. **Failure links** (like KMP's failure function, generalized to the trie): from each node, the failure link points to the longest proper suffix that is also a node (prefix of some pattern) in the trie.
3. **Output links**: chains of patterns that end at suffixes of the current node.

It's "KMP on a trie."

---

## III. BUILDING IT
```
Step 1: Insert all patterns into a trie.
Step 2: BFS the trie to compute failure links:
        - Root's children fail to root.
        - For node u with parent p via char c:
            fail[u] = the child-via-c of fail[p] (following fail links until found, or root).
        - "goto" transitions are filled so each (node, char) has a defined next state.
Step 3: Output links chain matches that end here.
```

---

## IV. MATCHING
Walk the text char by char. At each char:
1. Follow the goto transition (using failure links implicitly via the automaton).
2. At the current state, report all patterns ending here (via output links).

Each text character is processed once → O(|T| + matches).

---

## V. COMPLEXITY
- Build: O(total length of patterns × alphabet) for goto, O(total length) for fail links
- Match: O(|T| + number of matches)

---

## VI. APPLICATIONS
1. **Dictionary / spell-check** — find all dictionary words in a document
2. **Network intrusion detection** — match many attack signatures in a packet stream
3. **DNA / bioinformatics** — find many motifs in a genome
4. **Content filtering** — find banned words
5. **Multi-pattern search** in general
6. **DP on the automaton** — count strings avoiding/containing certain patterns (Aho-Corasick + DP is a powerful CP combo)

---

## VII. AHO-CORASICK + DP (the advanced CP use)
"Count strings of length L that contain none of the given patterns":
- Build the automaton.
- DP over (position, automaton state), forbidding states that complete a pattern.
- `dp[len][state]` = number of valid strings.

This appears in hard CP problems.

---

## VIII. AHO-CORASICK VS ALTERNATIVES
| Need | Use |
|------|-----|
| One pattern | KMP / Z |
| Many patterns, same length | Rabin-Karp (hash set) |
| Many patterns, varied length | **Aho-Corasick** ⭐ |
| All substrings of one string | Suffix automaton |

---

## IX. PROBLEMS
- Stream of Characters (LC 1032) — classic Aho-Corasick (reversed trie) ⭐
- Multi-pattern search problems on [CSES](https://cses.fi/problemset/) / CF
- CF problems tagged "aho-corasick" / "string"
- Count strings avoiding patterns (DP on automaton)

---

## X. NOTE ON IMPLEMENTATION
Aho-Corasick is intricate. Study a reference implementation ([CP-Algorithms](https://cp-algorithms.com) has a clean one), understand the failure-link BFS deeply, and test on small cases before trusting it.

Reference: https://cp-algorithms.com/string/aho_corasick.html

---

**→ Next:** [`07-Manacher.md`](./07-Manacher.md)
