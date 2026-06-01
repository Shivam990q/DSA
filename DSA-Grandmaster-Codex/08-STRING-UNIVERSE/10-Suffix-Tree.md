# 🔤 Suffix Tree

> *"A compressed trie of all suffixes. The Swiss Army knife of string algorithms — powerful but heavy."*

---

## I. WHAT IS IT
A suffix tree is a **compressed trie** containing all suffixes of a string s (usually s + '$').
- Edges are labeled with substrings (not single chars) — "compression."
- n leaves (one per suffix), at most 2n nodes.
- Built in **O(n)** with Ukkonen's algorithm (online, intricate).

---

## II. WHY IT'S POWERFUL
Once built, many queries are fast:
- **Substring check**: walk from root — O(|query|)
- **Longest repeated substring**: deepest internal node
- **Longest common substring** (generalized suffix tree of two strings)
- **Number of distinct substrings**: sum of edge lengths
- **Pattern occurrence count**: leaves in the subtree

---

## III. THE TRADEOFF
Suffix trees are O(n) to build but:
- Ukkonen's algorithm is **notoriously tricky** to implement correctly
- Higher memory constant than suffix arrays
- In competitive programming, **suffix array + LCP** or **suffix automaton** usually replace it (simpler, similar power)

---

## IV. SUFFIX TREE VS ARRAY VS AUTOMATON
| Need | Best choice |
|------|-------------|
| Most CP string tasks | Suffix Array + LCP (simpler) |
| Counting/occurrences/online | Suffix Automaton |
| Theoretical / classic exposition | Suffix Tree |

The suffix tree, suffix array, and suffix automaton are deeply related — all encode the same substring structure. SA and SAM are the practical favorites.

---

## V. CONSTRUCTION (conceptual)
- **Ukkonen's algorithm** (1995): online, O(n), using suffix links + "active point" + edge-label compression via [start, end] indices.
- This is one of the harder classic algorithms to implement; study it only when needed.

---

## VI. APPLICATIONS
1. Substring queries
2. Longest repeated / common substring
3. Distinct substring counting
4. Genome analysis (bioinformatics — finding motifs, repeats)
5. Data compression (LZ-family relationships)

---

## VII. PRACTICAL ADVICE
- For interviews: you essentially never need to implement a suffix tree.
- For CP: prefer suffix array (O(n log n), easy) or suffix automaton (O(n), online).
- Learn the suffix tree's CONCEPTS (suffix links, compression) — they illuminate SA and SAM.

Reference: https://cp-algorithms.com/string/suffix-tree-ukkonen.html

---

**→ Next:** [`11-Palindromic-Tree.md`](./11-Palindromic-Tree.md)
