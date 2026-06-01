# Evaluate Reverse Polish Notation

**Platform**: LeetCode 150 · **Difficulty**: Medium · **Topics**: Array, Math, Stack · **Pattern**: Operand stack evaluation

---

## 📜 Problem Statement

You are given an array of strings `tokens` that represents an arithmetic expression in **Reverse Polish Notation** (postfix notation).

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:
- The valid operators are `'+'`, `'-'`, `'*'`, and `'/'`.
- Each operand may be an integer or another expression.
- The division between two integers always **truncates toward zero**.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in reverse polish notation.
- The answer and all the intermediate calculations can be represented in a **32-bit** integer.

### Examples

**Example 1:**
```
Input:  tokens = ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
```

**Example 2:**
```
Input:  tokens = ["4","13","5","/","+"]
Output: 6
Explanation: (4 + (13 / 5)) = 4 + 2 = 6
```

**Example 3:**
```
Input:  tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
Output: 22
Explanation:
  ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 22
```

### Constraints
```
1 <= tokens.length <= 10^4
tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200].
```

---

## 🧠 Understanding the problem

RPN (postfix) eliminates the need for parentheses and operator precedence rules. The evaluation rule is simple:
- Numbers → push onto a stack.
- Operator → pop two operands, apply the operator, push the result back.

The final value on the stack is the answer. This is literally how stack-based calculators and many compilers work internally.

**Division note**: truncation toward zero means `int(a/b)` in Python 3 won't work directly (it floors). We need `int(a / b)` using `trunc` or `int(float(a)/b)`.

---

## Approach 1 — Brute force (find and reduce)

### Intuition
Scan the array for the first operator, apply it to the two preceding numbers, replace those three tokens with the result, and repeat until one token remains.

### Algorithm
1. While `tokens` has more than 1 element:
   - Find the first operator token.
   - Get the two operands before it.
   - Compute the result.
   - Replace the three tokens (operand, operand, operator) with the result.
2. Return the remaining token as an integer.

### Code
```cpp
class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        while (tokens.size() > 1) {
            for (int i = 0; i < tokens.size(); i++) {
                if (tokens[i] == "+" || tokens[i] == "-" || 
                    tokens[i] == "*" || tokens[i] == "/") {
                    int a = stoi(tokens[i-2]);
                    int b = stoi(tokens[i-1]);
                    int res = 0;
                    if (tokens[i] == "+") res = a + b;
                    else if (tokens[i] == "-") res = a - b;
                    else if (tokens[i] == "*") res = a * b;
                    else res = a / b; // C++ truncates toward zero
                    tokens.erase(tokens.begin() + i - 2, tokens.begin() + i + 1);
                    tokens.insert(tokens.begin() + i - 2, to_string(res));
                    break;
                }
            }
        }
        return stoi(tokens[0]);
    }
};
```
```java
class Solution {
    public int evalRPN(String[] tokens) {
        List<String> list = new ArrayList<>(Arrays.asList(tokens));
        while (list.size() > 1) {
            for (int i = 0; i < list.size(); i++) {
                String t = list.get(i);
                if (t.equals("+") || t.equals("-") ||
                    t.equals("*") || t.equals("/")) {
                    int a = Integer.parseInt(list.get(i - 2));
                    int b = Integer.parseInt(list.get(i - 1));
                    int res = 0;
                    if (t.equals("+")) res = a + b;
                    else if (t.equals("-")) res = a - b;
                    else if (t.equals("*")) res = a * b;
                    else res = a / b; // Java truncates toward zero
                    list.subList(i - 2, i + 1).clear();
                    list.add(i - 2, Integer.toString(res));
                    break;
                }
            }
        }
        return Integer.parseInt(list.get(0));
    }
}
```
```python
class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        ops = {'+', '-', '*', '/'}
        while len(tokens) > 1:
            for i, t in enumerate(tokens):
                if t in ops:
                    a, b = int(tokens[i-2]), int(tokens[i-1])
                    if t == '+': res = a + b
                    elif t == '-': res = a - b
                    elif t == '*': res = a * b
                    else: res = int(a / b)  # truncate toward zero
                    tokens = tokens[:i-2] + [str(res)] + tokens[i+1:]
                    break
        return int(tokens[0])
```

### Complexity
- **Time**: O(n²) — each reduction scans and shifts the array.
- **Space**: O(n) for the modified array.

### Verdict
Correct but inefficient. Demonstrates understanding of RPN semantics.

---

## Approach 2 — Stack evaluation (optimal) ⭐

### Intuition
The textbook RPN evaluation: push numbers, pop two on operator, push result. One pass, O(n).

### Algorithm
1. Create an empty stack.
2. For each token:
   - If it's a number → push it.
   - If it's an operator → pop `b` (top), pop `a` (second), compute `a op b`, push result.
3. Return the single remaining element on the stack.

### Dry run on `["4","13","5","/","+"]`
```
"4"  → push 4    → stack: [4]
"13" → push 13   → stack: [4, 13]
"5"  → push 5    → stack: [4, 13, 5]
"/"  → pop 5, 13 → 13/5 = 2 → push 2 → stack: [4, 2]
"+"  → pop 2, 4  → 4+2 = 6  → push 6 → stack: [6]
Return 6
```

### Code
```cpp
class Solution {
public:
    int evalRPN(vector<string>& tokens) {
        stack<int> st;
        for (const string& t : tokens) {
            if (t == "+" || t == "-" || t == "*" || t == "/") {
                int b = st.top(); st.pop();
                int a = st.top(); st.pop();
                if (t == "+") st.push(a + b);
                else if (t == "-") st.push(a - b);
                else if (t == "*") st.push(a * b);
                else st.push(a / b); // C++ truncates toward zero
            } else {
                st.push(stoi(t));
            }
        }
        return st.top();
    }
};
```
```java
class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> st = new ArrayDeque<>();
        for (String t : tokens) {
            if (t.equals("+") || t.equals("-") || t.equals("*") || t.equals("/")) {
                int b = st.pop();
                int a = st.pop();
                if (t.equals("+")) st.push(a + b);
                else if (t.equals("-")) st.push(a - b);
                else if (t.equals("*")) st.push(a * b);
                else st.push(a / b); // Java truncates toward zero
            } else {
                st.push(Integer.parseInt(t));
            }
        }
        return st.peek();
    }
}
```
```python
class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for t in tokens:
            if t in ('+', '-', '*', '/'):
                b = stack.pop()
                a = stack.pop()
                if t == '+': stack.append(a + b)
                elif t == '-': stack.append(a - b)
                elif t == '*': stack.append(a * b)
                else: stack.append(int(a / b))  # truncate toward zero
            else:
                stack.append(int(t))
        return stack[0]
```

### Complexity
- **Time**: O(n) — single pass through tokens.
- **Space**: O(n) — stack holds at most n/2 + 1 elements (all operands before any operator).

### Verdict
**The optimal and standard answer.** This is the canonical RPN evaluation algorithm.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Find-and-reduce | O(n²) | O(n) | Simulates by array manipulation |
| Stack evaluation | **O(n)** | O(n) | Textbook optimal ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Single number** (`["42"]`) → no operators, stack has one element → return 42.
- **Negative numbers** (`["-3", "2", "+"]`) → token `"-3"` is a number, not operator. `stoi` / `int()` handles the sign.
- **Division truncation toward zero**: `6 / (-132) = 0` (not -1). In Python, `//` floors (gives -1), so use `int(a / b)` instead.
- **Operand order**: when popping, the first pop is `b` (right operand), second pop is `a` (left operand). `a - b` and `a / b` are NOT commutative — order matters!
- **Pitfall**: confusing `a` and `b` order → `3 - 5` becomes `5 - 3` if you swap them.

---

## 🔗 Related problems
- **Basic Calculator** (LC 224) — infix with `+`, `-`, parentheses (harder).
- **Basic Calculator II** (LC 227) — infix with `+`, `-`, `*`, `/` (no parens).
- **Valid Parentheses** (LC 20) — stack matching.
- **Design a Stack With Increment Operation** (LC 1381) — stack design.

---

**→ Prev:** [`02-Min-Stack.md`](./02-Min-Stack.md) · **→ Next:** [`04-Generate-Parentheses.md`](./04-Generate-Parentheses.md) | [Problem set index](./00-Index.md)
