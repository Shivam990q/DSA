# Valid Palindrome

**Platform**: LeetCode 125 · **Difficulty**: Easy · **Topics**: String, Two Pointers · **Pattern**: Converging pointers

---

## 📜 Problem Statement

A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and digits.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

### Examples

**Example 1:**
```
Input:  s = "A man, a plan, a canal: Panama"
Output: true
Explanation: After cleanup → "amanaplanacanalpanama", which is a palindrome.
```

**Example 2:**
```
Input:  s = "race a car"
Output: false
Explanation: After cleanup → "raceacar", not a palindrome.
```

**Example 3:**
```
Input:  s = " "
Output: true
Explanation: After cleanup → "" (empty string), which is a palindrome by definition.
```

### Constraints
```
1 <= s.length <= 2 * 10^5
s consists only of printable ASCII characters.
```

---

## 🧠 Understanding the problem

Two tasks: (1) ignore non-alphanumeric characters, (2) compare case-insensitively. The naive approach creates a cleaned string and checks if it equals its reverse. The optimal approach skips the extra string entirely — use two pointers from both ends, skipping non-alnum chars in place.

---

## Approach 1 — Clean + reverse compare

### Intuition
Build a new string with only lowercase alphanumeric chars. Check if it equals its reverse.

### Code
```cpp
bool isPalindrome(string s) {
    string clean;
    for (char c : s)
        if (isalnum(c)) clean += tolower(c);
    string rev = clean;
    reverse(rev.begin(), rev.end());
    return clean == rev;
}
```
```java
public boolean isPalindrome(String s) {
    StringBuilder clean = new StringBuilder();
    for (char c : s.toCharArray())
        if (Character.isLetterOrDigit(c)) clean.append(Character.toLowerCase(c));
    String cleanStr = clean.toString();
    String rev = clean.reverse().toString();
    return cleanStr.equals(rev);
}
```
```python
def isPalindrome(s):
    clean = ''.join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) for the cleaned string.

### Verdict
Correct and simple. But uses O(n) extra space — can we do O(1)?

---

## Approach 2 — Two pointers in-place (optimal) ⭐

### Intuition
Two pointers `l` and `r` start at both ends. Skip non-alnum chars. Compare lowercased chars. If mismatch → false. If pointers cross → true.

### Algorithm
1. `l = 0, r = len-1`.
2. While `l < r`:
   - Advance `l` past non-alnum.
   - Retreat `r` past non-alnum.
   - If `lower(s[l]) != lower(s[r])` → return false.
   - `l++, r--`.
3. Return true.

### Dry run on `"A man, a plan, a canal: Panama"`
```
l→'A', r→'a' (skip non-alnum from right: 'a' at index 29)
'a' == 'a' ✓ → l++, r--
l→'m' (skip space), r→'m' (skip ':' etc.)
'm' == 'm' ✓ → ...
... all match → true
```

### Code
```cpp
bool isPalindrome(string s) {
    int l = 0, r = s.size() - 1;
    while (l < r) {
        while (l < r && !isalnum(s[l])) l++;
        while (l < r && !isalnum(s[r])) r--;
        if (tolower(s[l]) != tolower(s[r])) return false;
        l++; r--;
    }
    return true;
}
```
```java
public boolean isPalindrome(String s) {
    int l = 0, r = s.length() - 1;
    while (l < r) {
        while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++;
        while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--;
        if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r))) return false;
        l++; r--;
    }
    return true;
}
```
```python
def isPalindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1; r -= 1
    return True
```

### Complexity
- **Time**: O(n) — each pointer traverses at most n positions total.
- **Space**: O(1) — no extra string.

### Verdict
**The optimal answer.** O(n) time, O(1) space, single pass, no extra allocation.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Clean + reverse | O(n) | O(n) | simple, Pythonic |
| Two pointers | **O(n)** | **O(1)** | optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **All non-alnum** (`",.!@#"`) → cleaned is empty → palindrome (true).
- **Single character** → always true.
- **Digits count as alnum** (`"0P"` → "0p" → not palindrome).
- **Pitfall**: forgetting to skip non-alnum on BOTH sides before comparing.

---

## 🔗 Related problems
- **Valid Palindrome II** (LC 680) — can delete at most one char.
- **Palindrome Linked List** (LC 234) — two pointers on a linked list.
- **Longest Palindromic Substring** (LC 5) — expand around center.

---

**→ Next:** [`02-Two-Sum-II-Sorted.md`](./02-Two-Sum-II-Sorted.md) | [Index](./00-Index.md)
