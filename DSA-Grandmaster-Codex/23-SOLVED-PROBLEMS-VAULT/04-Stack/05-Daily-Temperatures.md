# Daily Temperatures

**Platform**: LeetCode 739 · **Difficulty**: Medium · **Topics**: Array, Stack, Monotonic Stack · **Pattern**: Monotonic decreasing stack of indices

---

## 📜 Problem Statement

Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`th day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0`.

### Examples

**Example 1:**
```
Input:  temperatures = [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
Explanation:
  Day 0 (73): next warmer is day 1 (74) → wait 1 day
  Day 1 (74): next warmer is day 2 (75) → wait 1 day
  Day 2 (75): next warmer is day 6 (76) → wait 4 days
  Day 3 (71): next warmer is day 5 (72) → wait 2 days
  Day 4 (69): next warmer is day 5 (72) → wait 1 day
  Day 5 (72): next warmer is day 6 (76) → wait 1 day
  Day 6 (76): no warmer day → 0
  Day 7 (73): no warmer day → 0
```

**Example 2:**
```
Input:  temperatures = [30,40,50,60]
Output: [1,1,1,0]
```

**Example 3:**
```
Input:  temperatures = [30,60,90]
Output: [1,1,0]
```

### Constraints
```
1 <= temperatures.length <= 10^5
30 <= temperatures[i] <= 100
```

---

## 🧠 Understanding the problem

For each day, find the **next greater element** to the right and compute the distance. This is the classic "Next Greater Element" pattern, solved optimally with a **monotonic stack**.

The brute force checks every future day for each position — O(n²). The monotonic stack processes each element at most twice (push + pop) for O(n) total.

---

## Approach 1 — Brute force (scan right for each day)

### Intuition
For each day `i`, scan forward until we find a temperature strictly greater than `temperatures[i]`.

### Algorithm
1. For each `i` from 0 to n-1:
   - For each `j` from i+1 to n-1:
     - If `temperatures[j] > temperatures[i]` → `answer[i] = j - i`, break.
2. Return answer (unset entries remain 0).

### Code
```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> answer(n, 0);
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (temperatures[j] > temperatures[i]) {
                    answer[i] = j - i;
                    break;
                }
            }
        }
        return answer;
    }
};
```
```java
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] answer = new int[n];
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (temperatures[j] > temperatures[i]) {
                    answer[i] = j - i;
                    break;
                }
            }
        }
        return answer;
    }
}
```
```python
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        answer = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if temperatures[j] > temperatures[i]:
                    answer[i] = j - i
                    break
        return answer
```

### Complexity
- **Time**: O(n²) — worst case when temperatures are decreasing.
- **Space**: O(1) extra (besides the output array).

### Verdict
Correct but TLEs on n = 10^5 with decreasing input.

---

## Approach 2 — Monotonic decreasing stack (optimal) ⭐

### Intuition
Maintain a stack of **indices** whose temperatures haven't found their "next warmer" yet. The stack is monotonically decreasing in temperature (top is the coldest unresolved day).

When we encounter a new temperature that's warmer than the stack's top, we've found the answer for that top element. Pop it and record the distance. Keep popping while the new temperature is still warmer.

### Algorithm
1. Initialize `answer` array of zeros, empty stack.
2. For each index `i`:
   - While stack is non-empty AND `temperatures[i] > temperatures[stack.top()]`:
     - Pop `j` from stack.
     - `answer[j] = i - j`.
   - Push `i` onto stack.
3. Return answer (indices remaining on stack have no warmer day → stay 0).

### Dry run on `[73, 74, 75, 71, 69, 72, 76, 73]`
```
i=0 (73): stack empty → push 0. Stack: [0]
i=1 (74): 74 > 73 → pop 0, answer[0]=1-0=1. Push 1. Stack: [1]
i=2 (75): 75 > 74 → pop 1, answer[1]=2-1=1. Push 2. Stack: [2]
i=3 (71): 71 < 75 → push 3. Stack: [2,3]
i=4 (69): 69 < 71 → push 4. Stack: [2,3,4]
i=5 (72): 72 > 69 → pop 4, answer[4]=5-4=1.
          72 > 71 → pop 3, answer[3]=5-3=2.
          72 < 75 → push 5. Stack: [2,5]
i=6 (76): 76 > 72 → pop 5, answer[5]=6-5=1.
          76 > 75 → pop 2, answer[2]=6-2=4.
          Push 6. Stack: [6]
i=7 (73): 73 < 76 → push 7. Stack: [6,7]
End: indices 6,7 remain → answer[6]=0, answer[7]=0
Result: [1,1,4,2,1,1,0,0] ✓
```

### Code
```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> answer(n, 0);
        stack<int> st; // indices with decreasing temperatures
        
        for (int i = 0; i < n; i++) {
            while (!st.empty() && temperatures[i] > temperatures[st.top()]) {
                int j = st.top(); st.pop();
                answer[j] = i - j;
            }
            st.push(i);
        }
        return answer;
    }
};
```
```java
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] answer = new int[n];
        Deque<Integer> st = new ArrayDeque<>(); // indices with decreasing temperatures

        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && temperatures[i] > temperatures[st.peek()]) {
                int j = st.pop();
                answer[j] = i - j;
            }
            st.push(i);
        }
        return answer;
    }
}
```
```python
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []  # indices, monotonically decreasing temps
        
        for i in range(n):
            while stack and temperatures[i] > temperatures[stack[-1]]:
                j = stack.pop()
                answer[j] = i - j
            stack.append(i)
        
        return answer
```

### Complexity
- **Time**: O(n) — each index is pushed and popped at most once.
- **Space**: O(n) — stack can hold all indices in worst case (strictly decreasing input).

### Verdict
**The optimal answer.** Classic monotonic stack application. Each element is processed exactly twice (one push, one pop), giving amortized O(1) per element.

---

## Approach 3 — Backward traversal (space optimization)

### Intuition
Process from right to left. For each day `i`, use the already-computed `answer` array to "jump" forward: if `temperatures[i+1]` isn't warmer, jump by `answer[i+1]` to skip days we know aren't the answer.

### Algorithm
1. Start from `i = n-2` down to 0 (last day's answer is always 0).
2. For each `i`, set `j = i + 1`:
   - If `temperatures[j] > temperatures[i]` → `answer[i] = j - i`.
   - Else if `answer[j] == 0` → no warmer day exists → `answer[i] = 0`.
   - Else → jump: `j += answer[j]`, repeat.

### Code
```cpp
class Solution {
public:
    vector<int> dailyTemperatures(vector<int>& temperatures) {
        int n = temperatures.size();
        vector<int> answer(n, 0);
        
        for (int i = n - 2; i >= 0; i--) {
            int j = i + 1;
            while (j < n) {
                if (temperatures[j] > temperatures[i]) {
                    answer[i] = j - i;
                    break;
                } else if (answer[j] == 0) {
                    // no warmer day after j either
                    break;
                }
                j += answer[j]; // jump forward
            }
        }
        return answer;
    }
};
```
```java
class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] answer = new int[n];

        for (int i = n - 2; i >= 0; i--) {
            int j = i + 1;
            while (j < n) {
                if (temperatures[j] > temperatures[i]) {
                    answer[i] = j - i;
                    break;
                } else if (answer[j] == 0) {
                    // no warmer day after j either
                    break;
                }
                j += answer[j]; // jump forward
            }
        }
        return answer;
    }
}
```
```python
class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        n = len(temperatures)
        answer = [0] * n
        
        for i in range(n - 2, -1, -1):
            j = i + 1
            while j < n:
                if temperatures[j] > temperatures[i]:
                    answer[i] = j - i
                    break
                elif answer[j] == 0:
                    break  # no warmer day exists
                j += answer[j]  # jump
        
        return answer
```

### Complexity
- **Time**: O(n) amortized — each jump skips already-resolved days.
- **Space**: O(1) extra (only the output array, no stack).

### Verdict
Same time complexity, avoids the explicit stack. Slightly harder to reason about but saves space.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute force | O(n²) | O(1) | TLE on large inputs |
| Monotonic stack | **O(n)** | O(n) | Clearest optimal ⭐ |
| Backward jump | O(n) | O(1) | Space-optimized variant |

---

## 🧪 Edge cases & pitfalls
- **All same temperature** (`[70,70,70]`) → all answers are 0 (no *strictly* warmer day).
- **Strictly increasing** (`[30,40,50,60]`) → each answer is 1 (next day is always warmer).
- **Strictly decreasing** (`[60,50,40,30]`) → all answers are 0; stack fills completely.
- **Single element** → answer is `[0]`.
- **Pitfall**: using `>=` instead of `>` in the comparison — the problem asks for *strictly* warmer.
- **Pitfall**: storing temperatures on the stack instead of indices — we need indices to compute distances.

---

## 🔗 Related problems
- **Next Greater Element I** (LC 496) — same pattern, different setup.
- **Next Greater Element II** (LC 503) — circular array variant.
- **Online Stock Span** (LC 901) — monotonic stack for "days since last higher price."
- **Largest Rectangle in Histogram** (LC 84) — monotonic increasing stack.
- **Trapping Rain Water** (LC 42) — can be solved with monotonic stack.

---

**→ Prev:** [`04-Generate-Parentheses.md`](./04-Generate-Parentheses.md) · **→ Next:** [`06-Car-Fleet.md`](./06-Car-Fleet.md) | [Problem set index](./00-Index.md)
