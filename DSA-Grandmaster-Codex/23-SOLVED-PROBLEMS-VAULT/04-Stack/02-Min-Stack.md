# Min Stack

**Platform**: LeetCode 155 · **Difficulty**: Medium · **Topics**: Stack, Design · **Pattern**: Auxiliary state tracking

---

## 📜 Problem Statement

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:
- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element `val` onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with **O(1) time complexity** for each function.

### Examples

**Example 1:**
```
Input:
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

Output:
[null,null,null,null,-3,null,0,-2]

Explanation:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2
```

**Example 2:**
```
Input:
["MinStack","push","push","getMin","pop","getMin"]
[[],[1],[0],[],[],[]]

Output:
[null,null,null,0,null,1]

Explanation:
MinStack minStack = new MinStack();
minStack.push(1);
minStack.push(0);
minStack.getMin(); // return 0
minStack.pop();
minStack.getMin(); // return 1
```

### Constraints
```
-2^31 <= val <= 2^31 - 1
Methods pop, top and getMin operations will always be called on non-empty stacks.
At most 3 * 10^4 calls will be made to push, pop, top, and getMin.
```

---

## 🧠 Understanding the problem

A normal stack gives O(1) push/pop/top. The challenge is `getMin()` in O(1). The naive approach (scan the stack) is O(n). We need to **remember** what the minimum is at every point in the stack's history, because when we pop, the minimum might change.

Key insight: the minimum can only change when we push or pop. If we store the running minimum alongside each element, popping automatically restores the previous minimum.

---

## Approach 1 — Two stacks (auxiliary min-stack)

### Intuition
Keep a second stack that mirrors the main stack but only tracks the running minimum. The top of the min-stack is always the current minimum.

### Algorithm
1. `push(val)`: push `val` onto main stack. Push `min(val, minStack.top())` onto min-stack.
2. `pop()`: pop from both stacks.
3. `top()`: return main stack's top.
4. `getMin()`: return min-stack's top.

### Dry run
```
push(-2): main=[-2], mins=[-2]
push(0):  main=[-2,0], mins=[-2,-2]
push(-3): main=[-2,0,-3], mins=[-2,-2,-3]
getMin(): mins.top() = -3
pop():    main=[-2,0], mins=[-2,-2]
top():    main.top() = 0
getMin(): mins.top() = -2
```

### Code
```cpp
class MinStack {
    stack<int> data;
    stack<int> mins;
public:
    MinStack() {}
    
    void push(int val) {
        data.push(val);
        if (mins.empty() || val <= mins.top())
            mins.push(val);
        else
            mins.push(mins.top());
    }
    
    void pop() {
        data.pop();
        mins.pop();
    }
    
    int top() {
        return data.top();
    }
    
    int getMin() {
        return mins.top();
    }
};
```
```java
class MinStack {
    private Deque<Integer> data = new ArrayDeque<>();
    private Deque<Integer> mins = new ArrayDeque<>();

    public MinStack() {}

    public void push(int val) {
        data.push(val);
        if (mins.isEmpty() || val <= mins.peek())
            mins.push(val);
        else
            mins.push(mins.peek());
    }

    public void pop() {
        data.pop();
        mins.pop();
    }

    public int top() {
        return data.peek();
    }

    public int getMin() {
        return mins.peek();
    }
}
```
```python
class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []

    def push(self, val: int) -> None:
        self.data.append(val)
        if not self.mins or val <= self.mins[-1]:
            self.mins.append(val)
        else:
            self.mins.append(self.mins[-1])

    def pop(self) -> None:
        self.data.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return self.mins[-1]
```

### Complexity
- **Time**: O(1) for all operations.
- **Space**: O(n) — two stacks of size n.

---

## Approach 2 — Single stack of pairs (optimal) ⭐

### Intuition
Instead of two separate stacks, store `(value, current_min)` pairs in a single stack. Same idea, less bookkeeping.

### Algorithm
1. `push(val)`: compute `new_min = min(val, current top's min)`. Push `(val, new_min)`.
2. `pop()`: pop the pair.
3. `top()`: return pair's first element.
4. `getMin()`: return pair's second element.

### Code
```cpp
class MinStack {
    stack<pair<int,int>> st; // {value, min_so_far}
public:
    MinStack() {}
    
    void push(int val) {
        int curMin = st.empty() ? val : min(val, st.top().second);
        st.push({val, curMin});
    }
    
    void pop() {
        st.pop();
    }
    
    int top() {
        return st.top().first;
    }
    
    int getMin() {
        return st.top().second;
    }
};
```
```java
class MinStack {
    private Deque<int[]> st = new ArrayDeque<>(); // {value, min_so_far}

    public MinStack() {}

    public void push(int val) {
        int curMin = st.isEmpty() ? val : Math.min(val, st.peek()[1]);
        st.push(new int[]{val, curMin});
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return st.peek()[0];
    }

    public int getMin() {
        return st.peek()[1];
    }
}
```
```python
class MinStack:
    def __init__(self):
        self.stack = []  # each entry: (val, current_min)

    def push(self, val: int) -> None:
        cur_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, cur_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

### Complexity
- **Time**: O(1) for all operations.
- **Space**: O(n) — one stack, but each entry is a pair (2n integers total).

---

## Approach 3 — Space-optimized min-stack (push to min-stack only when min changes)

### Intuition
The min-stack in Approach 1 has many repeated values. We can push to the min-stack only when the new value is `<=` the current minimum, and pop from it only when the popped value equals the current minimum.

### Code
```cpp
class MinStack {
    stack<int> data;
    stack<int> mins;
public:
    MinStack() {}
    
    void push(int val) {
        data.push(val);
        if (mins.empty() || val <= mins.top())
            mins.push(val);
    }
    
    void pop() {
        if (data.top() == mins.top())
            mins.pop();
        data.pop();
    }
    
    int top() {
        return data.top();
    }
    
    int getMin() {
        return mins.top();
    }
};
```
```java
class MinStack {
    private Deque<Integer> data = new ArrayDeque<>();
    private Deque<Integer> mins = new ArrayDeque<>();

    public MinStack() {}

    public void push(int val) {
        data.push(val);
        if (mins.isEmpty() || val <= mins.peek())
            mins.push(val);
    }

    public void pop() {
        if (data.peek().intValue() == mins.peek().intValue())
            mins.pop();
        data.pop();
    }

    public int top() {
        return data.peek();
    }

    public int getMin() {
        return mins.peek();
    }
}
```
```python
class MinStack:
    def __init__(self):
        self.data = []
        self.mins = []

    def push(self, val: int) -> None:
        self.data.append(val)
        if not self.mins or val <= self.mins[-1]:
            self.mins.append(val)

    def pop(self) -> None:
        if self.data[-1] == self.mins[-1]:
            self.mins.pop()
        self.data.pop()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return self.mins[-1]
```

### Complexity
- **Time**: O(1) for all operations.
- **Space**: O(n) worst case (all elements decreasing), but typically less than 2n.

### Verdict
Slightly more space-efficient in practice. The `<=` in the push condition is critical — using `<` would break when duplicates of the minimum are pushed.

---

## ⚖️ Approach comparison

| Approach | Time (all ops) | Space | Simplicity |
|----------|---------------|-------|------------|
| Two full stacks | O(1) | 2n | Simple |
| Single stack of pairs | O(1) | 2n | Cleanest ⭐ |
| Lazy min-stack | O(1) | n to 2n | Slightly tricky |

All three are valid interview answers. The pairs approach is the cleanest to explain.

---

## 🧪 Edge cases & pitfalls
- **Duplicate minimums**: pushing `[0, 1, 0]` — when we pop the second `0`, the min must still be `0`. The `<=` condition handles this.
- **Single element**: push then getMin → must return that element.
- **All same values**: `[5, 5, 5]` — min is always 5, pop doesn't change it.
- **INT_MIN values**: the problem allows `-2^31`; no special handling needed since we use `min()`.
- **Pitfall**: using `<` instead of `<=` in the lazy approach causes bugs with duplicate minimums.

---

## 🔗 Related problems
- **Max Stack** (LC 716) — similar but with max + popMax (needs more complex structure).
- **Min Stack with O(1) space** — encode difference from min (interview follow-up).
- **Stack with Increment Operation** (LC 1381) — lazy increment trick.
- **Implement Queue using Stacks** (LC 232) — another design problem.

---

**→ Prev:** [`01-Valid-Parentheses.md`](./01-Valid-Parentheses.md) · **→ Next:** [`03-Evaluate-RPN.md`](./03-Evaluate-RPN.md) | [Problem set index](./00-Index.md)
