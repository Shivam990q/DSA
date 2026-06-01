# 🔤 String Foundations

> *"A string is a sequence. Most string mastery is sequence mastery, specialized."*

---

## I. WHAT IS A STRING
A sequence of characters. Often immutable in modern languages (Python `str`, Java `String`). Mutable via char arrays / `StringBuilder` / C++ `string`.

---

## II. CORE OPERATIONS & COMPLEXITY
| Operation        | Typical complexity |
|------------------|--------------------|
| Length           | O(1)               |
| Index access     | O(1)               |
| Concatenation    | O(n+m)             |
| Substring        | O(k)               |
| Naive find       | O(nm)              |
| Compare          | O(min(n,m))        |

---

## III. THE MUTABILITY TRAP
Repeated string concatenation in a loop is O(n²) in many languages (each `+` copies). Use:
- C++: `string` with `+=` (amortized OK) or `ostringstream`
- Python: `''.join(list)` instead of `+=` in loops
- Java: `StringBuilder`

---

## IV. NAIVE SUBSTRING SEARCH — O(nm)
```cpp
for (int i = 0; i + m <= n; i++) {
    int j = 0;
    while (j < m && t[i+j] == p[j]) j++;
    if (j == m) found_at(i);
}
```
Worst case (e.g., "aaaa..." with "aaab"): O(nm). For large inputs, use KMP/Z/Rabin-Karp.

---

## V. THE STRING ALGORITHM PROGRESSION
1. Naive matching → understand the bottleneck
2. **Hashing** (Rabin-Karp): O(n) expected
3. **KMP / Z-algorithm**: O(n+m) guaranteed
4. **Aho-Corasick**: multiple patterns
5. **Manacher**: palindromes
6. **Suffix array / automaton**: advanced substring queries

---

## VI. CHARACTER FREQUENCY PATTERNS
Many string problems reduce to counting:
- Anagram check: compare frequency arrays
- First unique char: frequency map
- Group anagrams: sorted string or frequency as key

---

## VII. THE FULL TOOLKIT
For deep coverage of every string algorithm with code and complexity, see:
→ [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)

---

## VIII. STARTER PROBLEMS
- Reverse string (LC 344)
- Valid anagram (LC 242)
- Longest common prefix (LC 14)
- Implement strStr (LC 28)
- Longest substring without repeating (LC 3)

---

**→ Next:** Hashing, KMP, Z-algorithm, Suffix structures & all string algorithms → [`14-COMPENDIUM-All-String-Algorithms.md`](./14-COMPENDIUM-All-String-Algorithms.md)
