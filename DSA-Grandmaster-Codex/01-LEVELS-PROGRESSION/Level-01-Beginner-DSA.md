# 🌿 Level 1 — Beginner DSA (The First Steps)

> *"You now have the alphabet. Time to form words."*

---

## 🎯 OUTCOME

You can:
- Use arrays, strings, hash tables, and basic stacks/queues to solve problems
- Implement linear and binary search
- Implement bubble, selection, insertion sort and understand their complexities
- Reason about Big-O notation for simple loops
- Solve [LeetCode](https://leetcode.com) Easy problems comfortably (>80% success rate)

---

## 📚 PREREQUISITE

Level 0 passed.

---

## 🧱 CURRICULUM (12 Modules, ~80 hours)

### Module 1.1 — Big-O Notation (4 hours)

**Concepts:**
- What is "complexity"? Why do we care?
- O(1), O(log n), O(n), O(n log n), O(n²), O(n³), O(2ⁿ), O(n!)
- Best vs worst vs average case
- Space complexity vs time complexity

**The Constraint Cheat-Sheet:**
| n      | Acceptable Complexity |
|--------|-----------------------|
| ≤ 12   | O(n!)                 |
| ≤ 25   | O(2ⁿ × n)             |
| ≤ 100  | O(n⁴)                 |
| ≤ 500  | O(n³)                 |
| ≤ 5000 | O(n²)                 |
| ≤ 10⁶  | O(n log n) or O(n)    |
| ≤ 10¹⁸ | O(log n) or O(1)      |

**Drill**: For each of these, give the Big-O:
```python
for i in range(n):           # O(n)
    for j in range(n):       # 
        print(i*j)           #

for i in range(n):           # O(?)
    for j in range(i, n):    # 
        print(j)             #

i = n                        # O(?)
while i > 0:                 # 
    i //= 2                  #
```

(Answers: O(n²), O(n²), O(log n))

---

### Module 1.2 — Arrays Deep Dive (8 hours)

**Patterns:**
1. **Two pointers** — opposite ends, same direction
2. **Prefix sum** — O(1) range sum queries after O(n) preprocessing
3. **Kadane's algorithm** — maximum subarray sum (intro to DP!)
4. **Sliding window** — fixed-size & variable-size

**Must-solve problems (15):**
1. Maximum subarray sum (Kadane's)
2. Move zeros to end
3. Find duplicate in array (1 to n+1)
4. Best time to buy and sell stock
5. Container with most water
6. Trapping rain water (intro — full solution at Level 2)
7. Two-sum (sorted)
8. Remove duplicates from sorted array
9. Rotate array by k
10. Find missing number in 1..N
11. Maximum sum subarray of size k (sliding window)
12. Longest subarray with sum k
13. Subarray sum equals k (prefix sum + hash map)
14. Majority element (Boyer-Moore voting)
15. Find single non-duplicate element (XOR trick)

---

### Module 1.3 — Strings Deep Dive (6 hours)

**Patterns:**
- Character counting (frequency arrays / hash maps)
- Two pointers on strings
- Hash maps for substrings

**Must-solve problems (12):**
1. Reverse string
2. Reverse words in a string
3. Check if two strings are anagrams
4. Group anagrams
5. Valid palindrome (with non-alphanumeric ignored)
6. Longest substring without repeating characters (sliding window)
7. Longest palindromic substring (expand around center)
8. String compression
9. Implement strStr() (naïve substring search — KMP comes at Level 4)
10. Roman to integer
11. Integer to roman
12. Valid parentheses (intro to stacks)

---

### Module 1.4 — Searching (4 hours)

**Linear Search**: O(n). When to use: unsorted data.

**Binary Search**: O(log n). When to use: monotonic predicate.

**Binary Search template** — memorize this:
```cpp
int lo = 0, hi = n - 1;
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;  // avoid overflow
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) lo = mid + 1;
    else hi = mid - 1;
}
return -1;
```

**Drills:**
1. Implement binary search.
2. First and last position of element in sorted array.
3. Search in rotated sorted array (intro).
4. Find peak element.
5. Square root of n (using BS).
6. Find Kth missing positive number.

**Key insight**: Binary search isn't just for sorted arrays — it's for any *monotonic predicate*. We'll exploit this heavily later.

---

### Module 1.5 — Sorting (Basic) (6 hours)

**Implement from scratch:**
1. **Bubble sort** — O(n²). Educational only.
2. **Selection sort** — O(n²). Educational only.
3. **Insertion sort** — O(n²) but excellent for nearly-sorted data, used inside hybrid sorts.

**Understand (don't implement yet):**
- Merge sort: O(n log n) — Level 2 in detail
- Quick sort: O(n log n) average, O(n²) worst — Level 2 in detail

**Use built-in sort** for actual problems:
```cpp
sort(arr.begin(), arr.end());                // ascending
sort(arr.begin(), arr.end(), greater<int>()); // descending
sort(arr.begin(), arr.end(), [](int a, int b) { return abs(a) < abs(b); }); // custom
```

**Drills:**
1. Sort an array of 0s, 1s, 2s (Dutch national flag).
2. Sort by frequency.
3. Custom sort: sort strings by length.
4. Sort 2D points by distance from origin.

---

### Module 1.6 — Hash Tables (8 hours)

**Concepts:**
- Hash function: maps key → bucket
- Collisions: chaining vs open addressing (preview)
- O(1) expected lookup, insert, delete
- Hash sets vs hash maps
- When to use: O(n²) → O(n) by using a hash for "have I seen this?"

**Languages:**
- C++: `unordered_map`, `unordered_set` (and `map`, `set` for ordered)
- Python: `dict`, `set`
- Java: `HashMap`, `HashSet`

**Must-solve problems (12):**
1. Two-sum (unsorted) — the canonical hash problem
2. Contains duplicate
3. Valid anagram (with hash map)
4. Group anagrams
5. Top K frequent elements (bucket sort + hash)
6. Longest consecutive sequence (hash set + clever iteration)
7. First unique character in string
8. Subarray sum equals K
9. Continuous subarray sum (mod K)
10. Intersection of two arrays
11. Happy number (hash for cycle detection)
12. Isomorphic strings

**Pattern**: *"When you need to ask 'have I seen X?' in O(1), reach for a hash table."*

---

### Module 1.7 — Stacks (6 hours)

**Concepts:**
- LIFO (Last In, First Out)
- Operations: push, pop, top, empty
- Implementations: array-based, linked-list-based
- The call stack (recursion!)

**Patterns:**
- Matching pairs (parentheses)
- Monotonic stack (next greater/smaller element)
- Expression evaluation (postfix)

**Must-solve problems (10):**
1. Valid parentheses
2. Min stack (O(1) min query)
3. Implement queue using stacks
4. Evaluate reverse polish notation
5. Daily temperatures (monotonic stack — IMPORTANT)
6. Next greater element I & II
7. Largest rectangle in histogram (preview — Level 3 deep)
8. Asteroid collision
9. Decode string ("3[a2[c]]" → "accaccacc")
10. Backspace string compare

---

### Module 1.8 — Queues (4 hours)

**Concepts:**
- FIFO (First In, First Out)
- Operations: enqueue, dequeue, front, empty
- Implementations: circular array, linked list
- Deque (double-ended queue)
- Priority queue (preview — Level 2)

**Must-solve problems (6):**
1. Implement queue using arrays
2. Implement stack using queues
3. First negative number in every window of size k (deque)
4. Sliding window maximum (deque — IMPORTANT)
5. Number of recent calls
6. Design hit counter

---

### Module 1.9 — Linked Lists (8 hours)

**Concepts:**
- Singly linked list: each node has data + next pointer
- Doubly linked list: data + prev + next
- Circular linked list
- Why use them? Dynamic size, O(1) insert/delete at known position
- Why NOT use them? O(n) random access, cache-unfriendly

**Implement from scratch:**
- Insert at head/tail/position
- Delete at head/tail/value
- Search
- Reverse
- Length

**Must-solve problems (12):**
1. Reverse a linked list (iterative + recursive)
2. Detect cycle in linked list (Floyd's algorithm — IMPORTANT)
3. Find start of cycle
4. Middle of linked list (slow/fast pointers)
5. Merge two sorted linked lists
6. Remove Nth node from end
7. Add two numbers (linked list digits)
8. Palindrome linked list
9. Intersection of two linked lists
10. Reorder list
11. Copy linked list with random pointer
12. Remove duplicates from sorted linked list

**Two-Pointer Wisdom**: slow + fast = master pattern. Used for cycle detection, midpoint, kth from end.

---

### Module 1.10 — Recursion Deepening (8 hours)

**Concepts revisited:**
- Recursion tree
- Time complexity of recursion (recurrence relations)
- Subset / permutation generation (intro to backtracking)
- Recursion vs iteration trade-offs

**Must-solve problems (10):**
1. Print all subsets (power set)
2. Print all permutations
3. Generate all valid parentheses (n pairs)
4. Letter combinations of phone number
5. Combination sum (with repetition allowed)
6. Subsets II (with duplicates)
7. Permutations II (with duplicates)
8. N-th Fibonacci (compare: recursive O(2ⁿ), memoized O(n), iterative O(n), matrix O(log n) — preview)
9. Reverse a stack using recursion (no extra DS)
10. Sort a stack using recursion

---

### Module 1.11 — Complexity Analysis Practice (4 hours)

For each of the following code snippets, derive the Big-O:

**Snippet 1:**
```cpp
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= n; j *= 2)
        sum++;
```
**Answer**: O(n log n)

**Snippet 2:**
```cpp
for (int i = 1; i <= n; i++)
    for (int j = 1; j <= i; j++)
        for (int k = 1; k <= j; k++)
            sum++;
```
**Answer**: O(n³ / 6) = O(n³)

**Snippet 3:**
```cpp
int f(int n) {
    if (n <= 1) return 1;
    return f(n - 1) + f(n - 2);
}
```
**Answer**: O(2ⁿ)

**Snippet 4 (recurrence):**
```cpp
int g(int n) {
    if (n <= 1) return 1;
    return g(n / 2) + g(n / 2);
}
```
**Answer**: T(n) = 2T(n/2) + O(1) = O(n) (Master Theorem)

---

### Module 1.12 — Practice Marathon (12 hours)

Solve these specific LeetCode problems (in order):

**Easy (do all 30):**
- 1, 9, 13, 14, 20, 21, 26, 27, 28, 35, 53, 66, 70, 88, 100, 101, 104, 108, 121, 125, 136, 141, 169, 198, 217, 226, 234, 242, 283, 412

**Medium (do 15):**
- 2, 3, 5, 11, 15, 19, 22, 33, 39, 46, 49, 55, 56, 73, 75

---

## 📊 PROBLEM VOLUME

- ~120 structured problems above
- **Goal**: 200 LeetCode Easy + 50 LeetCode Medium by end of Level 1

---

## ⏱️ ESTIMATED TIME

- 80 hours of focused practice
- ~8-10 weeks at 8-10 hours/week
- ~3-4 weeks at 25 hours/week

---

## ✅ EXIT TEST

In 90 minutes, no references:

1. Implement binary search.
2. Solve [LeetCode 53: Maximum Subarray](https://leetcode.com/problems/maximum-subarray) (Kadane's).
3. Solve [LeetCode 141: Linked List Cycle](https://leetcode.com/problems/linked-list-cycle) (Floyd's).
4. Solve [LeetCode 20: Valid Parentheses](https://leetcode.com/problems/valid-parentheses).
5. Explain in 5 sentences: how does a hash table achieve O(1) lookup?
6. State the Big-O for: linear search, binary search, bubble sort, accessing an element in a hash map.

**Pass**: 5/6 correct.

---

## 📌 RESOURCES

### Books
- **Cracking the Coding Interview** — Gayle McDowell (Chapters 1-3)
- **Grokking Algorithms** — Aditya Bhargava (visual, beginner-friendly)

### YouTube
- **[NeetCode](https://neetcode.io)** — neetcode.io has the BLIND 75 list — gold for this level
- **Take U Forward** (Striver) — A2Z DSA Sheet
- **[Abdul Bari](https://www.youtube.com/@abdul_bari)** — Algorithm fundamentals

### Practice Sheets
- **NeetCode 150** ([neetcode.io](https://neetcode.io))
- **Striver's A2Z Sheet** ([takeuforward.org](https://takeuforward.org))
- **LeetCode Top 100 Liked**

### Cheat Sheets
- Big-O cheat sheet: [bigocheatsheet.com](https://www.bigocheatsheet.com)
- C++ STL cheat sheet (in this codex: `19-TEMPLATES-AND-IMPLEMENTATIONS/`)

---

## 🚀 ON COMPLETION

You are now a "junior" problem solver. You can solve simple problems with confidence.

**→ Proceed to:** [`Level-02-Academic-DSA.md`](./Level-02-Academic-DSA.md)
