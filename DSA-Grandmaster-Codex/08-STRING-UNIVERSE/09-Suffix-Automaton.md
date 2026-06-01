# 🔤 Suffix Automaton (SAM)

> *"The smallest machine that recognizes every substring of a string — built online in O(n)."*

---

## I. WHAT IS IT
A Suffix Automaton (SAM) is the **minimal deterministic finite automaton** that accepts all suffixes (and hence all substrings) of a string s.

- States ≤ 2n − 1
- Transitions ≤ 3n − 4
- Built **online** (add one character at a time) in O(n) (with O(n·alphabet) or O(n log alphabet) for transitions)

Each state represents an **equivalence class** of substrings that share the same set of ending positions (endpos).

---

## II. KEY CONCEPTS
- **endpos(t)**: the set of ending positions of substring t in s.
- Two substrings are in the same SAM state iff they have the same endpos set.
- **len[v]**: longest substring in state v.
- **link[v]** (suffix link): points to the state of the longest proper suffix in a different endpos class.
- The suffix links form a tree (the "suffix link tree" / parent tree).

---

## III. CONSTRUCTION (online, O(n))
```cpp
struct SAM {
    struct State { int len, link; map<char,int> next; };
    vector<State> st;
    int last;
    void init() { st.push_back({0, -1, {}}); last = 0; }
    void extend(char c) {
        int cur = st.size();
        st.push_back({st[last].len + 1, -1, {}});
        int p = last;
        while (p != -1 && !st[p].next.count(c)) { st[p].next[c] = cur; p = st[p].link; }
        if (p == -1) st[cur].link = 0;
        else {
            int q = st[p].next[c];
            if (st[p].len + 1 == st[q].len) st[cur].link = q;
            else {
                int clone = st.size();
                st.push_back({st[p].len + 1, st[q].link, st[q].next});
                while (p != -1 && st[p].next[c] == q) { st[p].next[c] = clone; p = st[p].link; }
                st[q].link = st[cur].link = clone;
            }
        }
        last = cur;
    }
};
```

---

## IV. APPLICATIONS (huge)
1. **Number of distinct substrings**: `Σ (len[v] − len[link[v]])` over all states ⭐
2. **Total length of distinct substrings**
3. **Check if a string is a substring**: walk transitions — O(|query|)
4. **Number of occurrences of a substring**: size of endpos (compute via suffix link tree)
5. **k-th lexicographic substring**
6. **Longest common substring of two strings**: build SAM on s, walk t through it ⭐
7. **Smallest cyclic shift**
8. **Number of times each substring occurs**

---

## V. LONGEST COMMON SUBSTRING (classic SAM use)
Build SAM on string A. Walk string B through the automaton:
- Maintain current state + current matched length.
- On each char: if transition exists, advance; else follow suffix links until a transition exists (or reset).
- Track the maximum matched length.

O(|A| + |B|).

---

## VI. SAM VS SUFFIX ARRAY
| Task | SAM | Suffix Array |
|------|-----|--------------|
| Distinct substrings | easy (formula) | easy (with LCP) |
| Occurrence counting | natural (endpos) | needs extra work |
| Online construction | yes ⭐ | no (mostly offline) |
| LCS of two strings | clean | also works |
| Lexicographic queries | good | excellent |

---

## VII. PROBLEMS
- Number of distinct substrings ([CSES](https://cses.fi/problemset/) "Distinct Substrings")
- Longest common substring of two strings
- CF problems tagged "suffix automaton" / "string suffix structures"
- [SPOJ](https://www.spoj.com) classic SAM problems

---

## VIII. NOTE
SAM is a Level 7 (elite CP) topic — beautiful but intricate. Study [CP-Algorithms](https://cp-algorithms.com)' treatment, implement carefully, test on small strings.

Reference: https://cp-algorithms.com/string/suffix-automaton.html

---

**→ Next:** [`10-Suffix-Tree.md`](./10-Suffix-Tree.md)
