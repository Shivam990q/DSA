# 🔤 Palindromic Tree (Eertree)

> *"A data structure where each node IS a distinct palindromic substring. Built in O(n)."*

---

## I. WHAT IS IT
The Palindromic Tree (a.k.a. **Eertree**, by Mikhail Rubinchik) stores all **distinct palindromic substrings** of a string.
- A string of length n has at most **n+1 distinct palindromic substrings** (a beautiful fact).
- Built **online** in O(n) (O(n·alphabet) or O(n log alphabet)).

---

## II. THE STRUCTURE
Two "roots":
- **Imaginary root** with length −1 (parent of odd-length palindromes)
- **Empty root** with length 0 (parent of even-length palindromes)

Each node stores:
- `len`: length of the palindrome
- `suffixLink`: longest proper palindromic suffix of this palindrome
- transitions: add char c on both sides → a longer palindrome

---

## III. WHAT IT COMPUTES
1. **Number of distinct palindromic substrings**: number of nodes (− the 2 roots) ⭐
2. **Count of each palindrome's occurrences** (with a propagation pass over suffix links)
3. **Number of palindromic substrings (total, with multiplicity)**
4. **Longest palindromic suffix at each position**
5. Palindrome-based DP (e.g., minimum palindrome partition variants)

---

## IV. CONSTRUCTION (online, conceptual)
Process the string left to right. Maintain the longest palindromic suffix ending at the current position. To add char c:
1. Follow suffix links from the current longest palindromic suffix until you find one that can be extended by c on the left (i.e., s[i − len − 1] == c).
2. Create a new node if this palindrome is new; set its suffix link by continuing to follow links.

Each step is amortized O(1) (like Manacher / SAM, the pointer only moves forward overall).

---

## V. APPLICATIONS
1. **Count distinct palindromic substrings** — the headline use ⭐
2. **Number of palindromic substrings** (total occurrences)
3. **Palindromic factorization** (split string into palindromes — DP on the tree)
4. **Richness of a string** (palindromic richness)
5. Hard CP problems involving palindromes

---

## VI. EERTREE VS MANACHER
| Need | Use |
|------|-----|
| Longest palindromic substring | Manacher (or expand-around-center) |
| Count DISTINCT palindromes | **Eertree** ⭐ |
| Count all palindromic substrings | Manacher (sum of radii) or Eertree |
| Palindromic factorization DP | Eertree |

---

## VII. PROBLEMS
- Count distinct palindromic substrings (CF / [SPOJ](https://www.spoj.com) "NUMOFPAL", "PALPROBLEM")
- Palindromic factorization problems
- CF problems tagged "palindromic tree" / "string"

---

## VIII. NOTE
Eertree is a Level 7 elite-CP structure. Elegant and surprisingly simple to code once understood. Study a reference implementation.

Reference: https://cp-algorithms.com/string/eertree.html (or "Eertree" original paper by Rubinchik & Shur)

---

**→ Next:** [`12-String-DP.md`](./12-String-DP.md)
