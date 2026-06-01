# 🎭 Programming Paradigms

> *"A language that doesn't change the way you think isn't worth learning."* — Alan Perlis

---

## I. WHAT IS A PARADIGM?

A paradigm is a **fundamental style of structuring computation**. Most languages support multiple, but lean toward one or two.

---

## II. THE FIVE MAJOR PARADIGMS

### 1. **Imperative**
*"Do this, then this, then this."*

Code is a sequence of statements that change state.
- Examples: C, Pascal, Bash
- Mental model: machine instructions

```c
int sum = 0;
for (int i = 1; i <= n; i++) sum += i;
```

### 2. **Procedural** (subset of imperative)
Imperative + functions/procedures.
- Examples: C, Pascal

### 3. **Object-Oriented (OOP)**
*"Things have data and behavior."*

Code organized around objects (instances of classes).
- Pillars: encapsulation, inheritance, polymorphism, abstraction
- Examples: Java, C#, C++ (multi-paradigm), Smalltalk

```java
class Stack<T> {
    private List<T> items = new ArrayList<>();
    public void push(T x) { items.add(x); }
    public T pop() { return items.remove(items.size() - 1); }
}
```

### 4. **Functional**
*"Compute by evaluating expressions, not by mutating state."*

Functions are first-class. Avoid mutation. Use recursion + higher-order functions.
- Examples: Haskell, OCaml, Lisp, Erlang, F#
- Modern multi-paradigm: Scala, Kotlin, Python, JavaScript

```haskell
sum [] = 0
sum (x:xs) = x + sum xs

-- or:
sum = foldr (+) 0
```

### 5. **Declarative** (umbrella for functional, logical, query)
*"Describe WHAT, not HOW."*

- SQL: declarative database queries
- Prolog: declarative logic programming
- HTML/CSS: declarative UI

```sql
SELECT name, max(salary) FROM employees GROUP BY department;
```

---

## III. KEY DIFFERENCES

| Aspect           | Imperative              | Functional             | OOP                       |
|------------------|-------------------------|------------------------|---------------------------|
| Primary unit     | Statement               | Function (expression)  | Object                    |
| State            | Mutable, central        | Immutable              | Encapsulated, mutable     |
| Iteration        | Loops                   | Recursion / map/fold   | Loops or iterators        |
| Composition      | Sequence + procedures   | Function composition   | Inheritance + composition |
| Concurrency      | Hard (shared mutable)   | Easy (no mutation)     | Medium                    |

---

## IV. WHY PARADIGM MATTERS FOR DSA

Different paradigms lead to different algorithm expressions:

### Imperative DP
```cpp
int[] dp = new int[n+1];
dp[0] = 0;
for (int i = 1; i <= n; i++) dp[i] = dp[i-1] + a[i];
```

### Functional DP
```haskell
prefix = scanl (+) 0 a
-- Same result, no mutation
```

### OOP DP (overengineered for tiny task!)
```java
class PrefixSum {
    private int[] sums;
    public PrefixSum(int[] a) { /* compute */ }
    public int range(int l, int r) { return sums[r] - sums[l-1]; }
}
```

---

## V. RECURSION: THE FUNCTIONAL BRIDGE

Recursion is **the natural way** to think functionally. Many DSA problems are naturally recursive (trees, divide-and-conquer, DP).

**Example**: tree traversal in functional style:
```haskell
inorder :: Tree a -> [a]
inorder Empty = []
inorder (Node l x r) = inorder l ++ [x] ++ inorder r
```

vs imperative (with stack):
```cpp
vector<int> inorder(TreeNode* root) {
    vector<int> result;
    stack<TreeNode*> stk;
    while (root || !stk.empty()) {
        while (root) { stk.push(root); root = root->left; }
        root = stk.top(); stk.pop();
        result.push_back(root->val);
        root = root->right;
    }
    return result;
}
```

---

## VI. PARADIGM POLYGLOT — WHAT TO LEARN

For the journey from beginner to grandmaster:

1. **Master one imperative/OOP language** (C++, Java, or Python) — for raw productivity
2. **Learn one functional language** (Haskell, Scheme, OCaml) — to rewire your thinking
3. **Be familiar with one declarative** (SQL is essential anyway)

> *"You don't need to be fluent in 5 languages. You need to be fluent in 1, conversational in 2, and aware of 3."*

---

## VII. PARADIGM IN CP

- **C++**: imperative-OOP-template-functional hybrid; the king of CP for speed
- **Python**: imperative + functional; great for prototyping; slow at scale
- **Haskell**: rare in CP, but elegant for some problems

In contests, paradigm choice matters less than **algorithm choice**. But the paradigm you internalize shapes how easily you see the algorithm.

---

## VIII. THE GRANDMASTER'S MULTI-PARADIGM MIND

A great problem solver:
- Thinks recursively (functional) about subproblems
- Manages state crisply (imperative) for performance
- Designs APIs cleanly (OOP) for libraries
- Queries declaratively (SQL/Pandas) for data

You don't pick one. You **switch** based on the problem.

---

## IX. RECOMMENDED READING

- **SICP (Structure and Interpretation of Computer Programs)** ⭐⭐⭐ — paradigm-shifting
- **The Pragmatic Programmer** — practical paradigm awareness
- **Land of Lisp** — functional / logic
- **Real World OCaml** — typed functional + imperative

---

**→ Next:** [`04-Recursion-Thinking.md`](./04-Recursion-Thinking.md)
