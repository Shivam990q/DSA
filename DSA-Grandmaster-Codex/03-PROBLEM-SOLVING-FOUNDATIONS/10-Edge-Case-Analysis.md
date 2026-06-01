# 🛡️ Edge Case Analysis — Where Lazy Minds Die

> *"The careless engineer dies at edges. The grandmaster lives there."*

---

## I. THE EDGE CASE TAXONOMY

Every problem has predictable edge cases. Memorize this list:

### Size edges
- **n = 0** (empty input)
- **n = 1** (single element)
- **n = 2** (smallest non-trivial)
- **n = MAX** (largest allowed by constraints)

### Value edges
- **All same** (e.g., array of identical values)
- **All distinct**
- **All zero / one**
- **Negative numbers** (if allowed)
- **Very large** (overflow potential)
- **Very small / minimum int**

### Order edges
- **Already sorted**
- **Reverse sorted**
- **Random**
- **Sorted but with one out of place**

### Boundary edges
- **First element / last element** is the answer / problematic
- **Off-by-one** in indices
- **Inclusive vs exclusive** ranges

### Structure edges (for graphs/trees)
- **Empty graph**
- **Single node**
- **Disconnected components**
- **Cycle of one node** (self-loop, if allowed)
- **Linear chain** (vs balanced)
- **Bipartite vs not**

### Algorithm-specific edges
- **Hash collisions** (adversarial input)
- **Integer overflow** in sums
- **Recursion depth** (for n=10⁵, recursion limit?)
- **Negative weights** (for shortest path)
- **Negative cycle** (for Bellman-Ford)
- **Empty intervals**, **zero-length strings**

---

## II. THE SYSTEMATIC EDGE CASE CHECKLIST

Before submitting, verify your solution handles:

### Input edges
- [ ] n = 0?
- [ ] n = 1?
- [ ] All elements equal?
- [ ] Empty string / array?
- [ ] Single-character string?
- [ ] Negative numbers?
- [ ] Zero?
- [ ] Maximum constraint values?

### Output edges
- [ ] Output type correct? (int vs long long for sum)
- [ ] Output format? (newline, spaces, "Yes/No" vs "YES/NO")
- [ ] Empty output if no answer?
- [ ] Modulo applied at every step (not just final)?

### Logic edges
- [ ] Off-by-one (n vs n-1, 0-indexed vs 1-indexed)?
- [ ] Inclusive / exclusive ranges?
- [ ] First iteration correct?
- [ ] Last iteration correct?
- [ ] Single iteration (n=1 case)?

### Algorithm-specific
- [ ] Sorted input handles correctly?
- [ ] Reverse-sorted?
- [ ] All same?
- [ ] Maximum constraint (overflow, TLE)?

---

## III. INTEGER OVERFLOW — THE SILENT KILLER

C++:
- `int`: ~ ±2.1×10⁹
- `long long`: ~ ±9.2×10¹⁸
- `unsigned int`: 0 to ~4.3×10⁹
- `unsigned long long`: 0 to ~1.8×10¹⁹

### Common overflow triggers
- Sum of n elements where each ≤ 10⁹ and n = 10⁵ → 10¹⁴, **overflow if int**
- Product of two ints ≤ 10⁹ → 10¹⁸, fits in long long
- nCr without modular: factorial overflows fast (20! > 10¹⁸)

### Safe practices
- Use `long long` for sums by default in CP
- For C++: `#define int long long` at top (and `int32_t main()`)
- For Python: built-in big integers; no overflow worry (but slow)
- For Java: use `long` instead of `int` for sums; `BigInteger` for arbitrary

---

## IV. NULL / EMPTY CHECKS

### Lists/arrays
```python
if not arr: return  # or whatever
```

### Trees
```python
def height(root):
    if not root: return 0
    return 1 + max(height(root.left), height(root.right))
```

### Strings
```python
if not s: return 0
```

**Always** check empty input before accessing `arr[0]` or `root.left`.

---

## V. THE OFF-BY-ONE BANE

The most common bug.

### Common patterns
```python
# Wrong: off-by-one
for i in range(n+1):  # one too many?
for i in range(0, n-1):  # one too few?

# Inclusive vs exclusive
arr[l:r]    # Python: [l, r) — right exclusive
arr[l..r]   # Math: [l, r] — both inclusive
```

### Defense
- **Be explicit** in your head: "I want indices 0 through n-1 inclusive."
- **Trace n=1, n=2** by hand.
- **Use named functions** with clear semantics: `range_sum(l, r)` (inclusive both? assert).

---

## VI. RECURSION DEPTH

Default Python recursion limit: 1000. C++: ~50K-100K (stack size dependent).

For n = 10⁵, naive recursion may stack overflow.

### Defenses
- Increase limit: `sys.setrecursionlimit(10**6)` (Python)
- Convert to iteration with explicit stack
- For trees: ensure balanced or use iterative DFS

---

## VII. MODULO PITFALLS

When the problem says "answer mod p":

### Apply mod at every step
```python
ans = (ans + a) % MOD
ans = (ans * b) % MOD
```

### Modular subtraction can give negative
```python
diff = (a - b + MOD) % MOD  # always positive
```

### Modular division requires inverse
```python
# a / b mod p (p prime, gcd(b, p) = 1)
inv_b = pow(b, p-2, p)
ans = (a * inv_b) % p
```

### Don't forget to mod the output
Even if your computation is mod throughout, the final print step should ensure non-negative.

---

## VIII. EDGE CASE EXAMPLES

### Example 1: Two-sum — what if duplicates?
> arr = [3, 3], target = 6 → indices [0, 1].
> 
> If you build hash: `{3: 0}` first. Then check `target - 3 = 3` in hash — yes, return [0, 1]. ✓
>
> But if you write `seen[a[i]] = i` *before* the check, you'd find the same index. → check before insert.

### Example 2: Binary search — empty array
> If `n = 0`, the loop never enters; correctly returns -1. ✓

### Example 3: Linked list reverse — single node
> Iterative: `prev = None, curr = head`. Loop: `next_node = curr.next; curr.next = prev; prev = curr; curr = next_node`. For single node, one iteration; returns the node correctly with `next = None`. ✓

### Example 4: Tree max path sum — single node, all negative
> Some implementations return 0 (path of nothing). Problem may require including at least one node. → Read problem carefully.

### Example 5: GCD — gcd(a, 0) = a
> Don't forget the base case in Euclidean algorithm.

---

## IX. STRESS-TEST FOR EDGES

After coding, run on:
- [ ] All examples from problem statement
- [ ] Edge: n=1
- [ ] Edge: n at max
- [ ] Edge: all same value
- [ ] Random small cases (validated against brute)

For random testing, random inputs of small size + brute reference = bug detector.

---

## X. THE FINAL TRUTH

> **"The 5 minutes you spend on edge cases save 5 hours of debugging.  
>  The grandmaster doesn't 'find' edge cases — they generate them by reflex."**

---

**→ Next:** [`11-The-Polya-Method.md`](./11-The-Polya-Method.md)
