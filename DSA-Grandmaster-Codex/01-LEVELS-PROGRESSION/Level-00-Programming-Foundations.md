# 🌱 Level 0 — Programming Foundations (The Genesis)

> *"Before you can solve, you must speak the language."*

---

## 🎯 OUTCOME (After completing this level)

You can:
- Read a problem description and translate it to code
- Write loops, conditionals, functions, and basic recursion fluently
- Understand variables, scope, and basic memory model
- Read and write input/output in your chosen language
- Trace through code mentally to predict output
- Debug simple errors using print statements

---

## 📚 PREREQUISITE

**Zero**. This is for absolute beginners. If you have *any* programming experience, skim and proceed to Level 1.

---

## 🧱 CURRICULUM (8 Modules, ~50 hours)

### Module 0.1 — Choosing Your Weapon (3 hours)

**Pick ONE language** for the entire DSA journey:

| Language | Best For                                  | Difficulty | Speed in Contests |
|----------|-------------------------------------------|------------|-------------------|
| **C++**  | Competitive Programming, deep performance | Hard       | Fastest           |
| **Python** | Interviews, prototyping, beginners      | Easiest    | Slow but readable |
| **Java** | Interviews (esp. India/big tech)          | Medium     | Medium            |

**My recommendation**:
- 🏆 **For CP / FAANG combined** → C++
- 🌱 **For pure beginners** → Python (easier syntax → focus on logic)
- 💼 **For Java/Indian placements** → Java

**You will master your chosen language by the end of Level 2.** Other languages can come later.

---

### Module 0.2 — Setup (1 hour)

**Install:**
- Code editor: VSCode (free, universal)
- Compiler/interpreter: g++ for C++, Python 3.11+, JDK 17+
- Online judges: [LeetCode](https://leetcode.com), [Codeforces](https://codeforces.com), [AtCoder](https://atcoder.jp), [HackerRank](https://www.hackerrank.com) accounts

**First program** in your language:
```cpp
// C++
#include <iostream>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
```
```python
# Python
print("Hello, World!")
```

---

### Module 0.3 — Variables & Types (4 hours)

**Concepts:**
- Variables = labeled memory cells
- Types = what kind of data (integer, real number, character, boolean, string)
- Type-checking: static (C++/Java) vs dynamic (Python)
- Memory: each variable occupies bytes; types determine how many

**Drills (do all):**
1. Declare variables of each primitive type. Print them.
2. Compute area of a rectangle (input length, width).
3. Convert temperature Celsius → Fahrenheit.
4. Swap two variables (with and without temp).
5. Compute compound interest given P, R, T, n.

**Mini-Project**: Build a calculator (add, sub, mul, div, mod) that takes user input.

---

### Module 0.4 — Conditionals (4 hours)

**Concepts:**
- `if`, `else if`, `else`, `switch`/`match`
- Boolean expressions, comparison operators
- Logical operators: `&&`, `||`, `!`
- Truthiness/falsiness (esp. Python)

**Drills:**
1. Determine if a number is positive, negative, or zero.
2. Find the largest of three numbers.
3. Determine if a year is a leap year. (Rule: divisible by 4, except divisible by 100 unless divisible by 400.)
4. Grade calculator (90+ A, 80-89 B, etc.)
5. Determine if a triangle is valid given 3 sides; classify (equilateral/isosceles/scalene).

---

### Module 0.5 — Loops (6 hours)

**Concepts:**
- `for`, `while`, `do-while`
- Loop counters, termination conditions
- `break`, `continue`
- Nested loops
- Iterating over collections

**Drills (do all):**
1. Print numbers 1 to N.
2. Print the multiplication table of N.
3. Sum the digits of a number.
4. Reverse a number.
5. Check if a number is prime (basic O(n) and O(√n) versions).
6. Print Fibonacci up to N terms.
7. Find GCD of two numbers (Euclidean algorithm — your first algorithm!).
8. Print all prime numbers up to N (sieve later).
9. Patterns: print a pyramid, diamond, hollow square (10 patterns).
10. Find factorial.
11. Check if number is a palindrome.
12. Find Armstrong numbers up to N.

**Time goal**: All 12 drills in <5 hours.

---

### Module 0.6 — Functions (5 hours)

**Concepts:**
- Function = reusable block of code
- Parameters (inputs), return values (outputs)
- Pass by value vs pass by reference (C++)
- Scope: local vs global
- Function decomposition

**Drills:**
1. Write `int gcd(int a, int b)`.
2. Write `bool isPrime(int n)`.
3. Write `long long factorial(int n)`.
4. Write `int reverseNumber(int n)`.
5. Write `bool isPalindrome(int n)`.
6. Write `int countDigits(int n)`.
7. Write `void printDivisors(int n)`.
8. Write `bool isArmstrong(int n)`.
9. Write `int sumOfDigits(int n)`.
10. Write `int power(int base, int exp)` (linear, then later: fast exponentiation).

**Now refactor**: Take 5 of your loop drills above and rewrite using functions.

---

### Module 0.7 — Arrays / Lists (8 hours)

**Concepts:**
- Array = contiguous block of same-type elements
- Indexing (0-based in C++/Java/Python)
- Memory layout, cache friendliness (preview)
- Multi-dimensional arrays
- Dynamic arrays (`vector` in C++, `list` in Python, `ArrayList` in Java)

**Drills:**
1. Read N numbers, print in reverse.
2. Find max, min, sum, average.
3. Count occurrences of element X.
4. Linear search (return index or -1).
5. Reverse an array in-place.
6. Find second largest element.
7. Check if array is sorted.
8. Remove duplicates (assume sorted).
9. Print 2D matrix.
10. Transpose a matrix.
11. Add two matrices.
12. Multiply two matrices.
13. Find the row with maximum 1s in a binary matrix.
14. Spiral traversal of matrix.
15. Rotate matrix by 90°.

---

### Module 0.8 — Strings (6 hours)

**Concepts:**
- String = sequence of characters (often immutable)
- Indexing, slicing, concatenation
- Common methods: length, substring, find, replace, split, join
- ASCII / Unicode basics

**Drills:**
1. Read string, print length.
2. Reverse a string.
3. Check palindrome.
4. Count vowels and consonants.
5. Convert to uppercase / lowercase.
6. Count occurrences of a character.
7. Replace spaces with `%20` (URLify).
8. Check if two strings are anagrams.
9. Find the longest word in a sentence.
10. Reverse words in a sentence (e.g., "hello world" → "world hello").
11. Find first non-repeating character.
12. String compression (e.g., "aaabbc" → "a3b2c1").

---

### Module 0.9 — Recursion Primer (10 hours)

**Concepts:**
- Recursion = function calling itself
- Base case (when to stop)
- Recursive case (how to break the problem down)
- Call stack
- Recursion vs iteration
- Tail recursion (preview)

**Master Theorem of Recursion** (informal):
> *Every recursion has 3 things: base case, smaller subproblem call, combination step.*

**Drills (do them ALL by hand-tracing first, then coding):**
1. `factorial(n)`
2. `fibonacci(n)` (recursive — note the exponential time!)
3. `power(base, exp)` (linear, then logarithmic)
4. `sum(n)` = 1 + 2 + ... + n
5. `gcd(a, b)` recursively
6. Print numbers from N to 1 (recursively)
7. Print numbers from 1 to N (recursively)
8. Reverse a string recursively
9. Check palindrome recursively
10. Sum of digits recursively
11. Count digits recursively
12. Tower of Hanoi (classic)
13. Print all subsets of a set (introduces backtracking!)
14. Print all permutations of a string (introduces backtracking!)

**The Recursion Mindset:**
> *"Trust the recursion. Don't trace too deep. State the contract clearly: 'fn(n) returns the answer for size n, given fn(n-1) returns answer for size n-1.'"*

---

### Module 0.10 — I/O Mastery (3 hours)

**Concepts:**
- Read single value, multiple values, until EOF, line-by-line
- Fast I/O (esp. C++: `ios_base::sync_with_stdio(false); cin.tie(NULL);`)
- Print with formatting (precision for floats)

**Templates** for your chosen language. Memorize. (Provided in `19-TEMPLATES-AND-IMPLEMENTATIONS/`.)

---

## 📊 PROBLEM VOLUME

- **Total drills**: 100+
- **Plus**: 50 LeetCode "Easy" problems (any topic)
- **Plus**: First 10 problems on Codeforces with rating ≤ 800

---

## ⏱️ ESTIMATED TIME

- 50 hours of focused practice
- ~5-8 weeks at 7-10 hours/week
- ~2-3 weeks at 25 hours/week (intensive)

---

## ✅ EXIT TEST (Pass to advance)

Without using any references, in <2 hours:

1. Solve [LeetCode 1: Two Sum](https://leetcode.com/problems/two-sum) (any approach OK).
2. Solve [LeetCode 9: Palindrome Number](https://leetcode.com/problems/palindrome-number).
3. Solve [LeetCode 14: Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix).
4. Solve [LeetCode 26: Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array).
5. Write `int gcd(int a, int b)` recursively.
6. Write `vector<vector<int>> generateSubsets(vector<int> v)` recursively (backtracking).
7. Trace by hand: `fib(5)` and draw the call tree.
8. Explain in 1 paragraph: "What is recursion, and what are its 3 parts?"

**Pass criteria**: 6/8 correct, in under 2 hours.

If you fail, return to the modules of weakness. **Never advance without the foundation.**

---

## 📌 RESOURCES

### Books
- **[FREE]** *Think Like a Programmer* — V. Anton Spraul (excellent for true beginners)
- **[FREE]** *Automate the Boring Stuff with Python* — Al Sweigart
- **[PAID]** *Programming: Principles and Practice Using C++* — Bjarne Stroustrup

### Online Courses
- **[FREE]** Harvard [CS50](https://cs50.harvard.edu) (HarvardX on edX)
- **[FREE]** MIT 6.0001 (OCW) — Python
- **[FREE]** [freeCodeCamp](https://www.freecodecamp.org) YouTube (multi-language)

### YouTube Channels
- **CS50** (Harvard) — David Malan
- **mycodeschool** — recursion + DS gold for beginners (legendary RIP)
- **[NeetCode](https://neetcode.io)** — beginner-friendly problem walkthroughs

### Practice Platforms
- **HackerRank** — *30 Days of Code* (perfect Level 0)
- **Codecademy** — interactive learning
- **LeetCode** — Easy problems (Two Sum, Palindrome, etc.)

### Reference
- C++: [cppreference](https://en.cppreference.com)
- Python: docs.python.org
- Java: oracle docs

---

## 🚀 ON COMPLETION

You are no longer a non-programmer. You are a programmer.

**→ Proceed to:** [`Level-01-Beginner-DSA.md`](./Level-01-Beginner-DSA.md)
