# Find the Duplicate Number

**Platform**: LeetCode 287 · **Difficulty**: Medium · **Topics**: Array, Two Pointers, Binary Search, Bit Manipulation · **Pattern**: Array as implicit linked list + Floyd's cycle detection

---

## 📜 Problem Statement

Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive.

There is only **one repeated number** in `nums`, return *this repeated number*.

You must solve the problem **without** modifying the array `nums` and uses only constant extra space.

### Examples

**Example 1:**
```
Input:  nums = [1, 3, 4, 2, 2]
Output: 2
```

**Example 2:**
```
Input:  nums = [3, 1, 3, 4, 2]
Output: 3
```

**Example 3:**
```
Input:  nums = [3, 3, 3, 3, 3]
Output: 3
```

### Constraints
```
1 <= n <= 10^5
nums.length == n + 1
1 <= nums[i] <= n
All the integers in nums appear only once except for precisely one integer which appears two or more times.
```

**Follow-up:** How can we prove that at least one duplicate number must exist? Can you solve the problem in linear runtime complexity?

---

## 🧠 Understanding the problem

We have `n + 1` values, each in `[1, n]`. By the pigeonhole principle there *must* be a repeat — that answers the first follow-up. The hard constraints are the kicker: **don't modify the array** and use **O(1) space**. That rules out sorting (modifies) and a hash set (O(n) space).

The clever reframe: because every value is in `[1, n]` and indices run `0..n`, we can treat each value as a **pointer to another index**. Define the sequence `x → nums[x] → nums[nums[x]] → …` starting at index 0. Since values point into `[1, n]`, we never jump to index 0 again as a *value* — but two different indices map to the same value (the duplicate), which means two arrows point **into the same node**. That's precisely a linked list with a cycle, and the **entrance of the cycle is the duplicate value**.

So the problem becomes Linked List Cycle II (LC 142) on an array. Floyd's algorithm finds the cycle entrance in O(n) time and O(1) space — satisfying every constraint.

---

## Approach 1 — Sort or hash set (violates constraints, but instructive)

### Intuition
The obvious solutions: sort and look for adjacent equals, or scan with a seen-set. Both find the duplicate immediately. They're disqualified here (sorting mutates; the set uses O(n) space) but worth stating to show you understand the constraints you're being pushed past.

### Algorithm (hash set)
1. Create empty set `seen`.
2. For each `x` in `nums`: if `x` in `seen` → return `x`; else add `x`.

### Dry run on `[1, 3, 4, 2, 2]`
```
1 → add {1}
3 → add {1,3}
4 → add {1,3,4}
2 → add {1,3,4,2}
2 → already present → return 2 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        unordered_set<int> seen;
        for (int x : nums) {
            if (seen.count(x)) return x;
            seen.insert(x);
        }
        return -1;  // unreachable per constraints
    }
};
```

**Java**
```java
class Solution {
    public int findDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) {
            if (!seen.add(x)) return x;  // add returns false if already present
        }
        return -1;  // unreachable per constraints
    }
}
```

**Python**
```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        seen = set()
        for x in nums:
            if x in seen:
                return x
            seen.add(x)
        return -1  # unreachable per constraints
```

### Complexity
- **Time**: O(n).
- **Space**: O(n) — violates the constraint. (Sorting would be O(n log n) time, O(1) space but mutates the array — also disallowed.)

### Verdict
Correct but breaks the rules. Use it only to frame the discussion before delivering the constant-space answer.

---

## Approach 2 — Floyd's cycle detection (optimal) ⭐

### Intuition
Interpret `i → nums[i]` as a "next" pointer. Start at index 0 and follow the chain. Because some value is duplicated, two indices point to the same place — a cycle forms — and the node where the cycle begins is the duplicated value.

Phase 1: run a slow pointer (1 step) and a fast pointer (2 steps) until they meet inside the cycle. Phase 2: reset one pointer to the start; advance both one step at a time; where they meet is the cycle entrance = the duplicate.

### Why does the entrance equal the duplicate?
A node is a cycle entrance iff two different predecessors point to it. In our mapping, index `i` points to value `nums[i]`. Two distinct indices `i ≠ j` with `nums[i] == nums[j]` both point to the same value `v` — so `v` is the node with two incoming arrows, i.e., the cycle entrance. Floyd's second phase mathematically lands exactly there.

### Algorithm
1. **Phase 1 (find meeting point)**: `slow = fast = nums[0]`. Repeat `slow = nums[slow]`, `fast = nums[nums[fast]]` until `slow == fast`.
2. **Phase 2 (find entrance)**: set `slow = nums[0]`. While `slow != fast`: `slow = nums[slow]`, `fast = nums[fast]`.
3. Return `slow`.

### Dry run on `[1, 3, 4, 2, 2]`
```
Mapping (index → value):
  0→1, 1→3, 2→4, 3→2, 4→2
Chain from 0:  0→1→3→2→4→2→4→2…   (cycle: 2→4→2)

Phase 1:
  slow=nums[0]=1  fast=nums[0]=1
  s=nums[1]=3      f=nums[nums[1]]=nums[3]=2
  s=nums[3]=2      f=nums[nums[2]]=nums[4]=2   → meet at 2

Phase 2:
  slow=nums[0]=1   fast=2
  s=nums[1]=3      f=nums[2]=4   (3 != 4)
  s=nums[3]=2      f=nums[4]=2   → meet at 2
return 2 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int slow = nums[0], fast = nums[0];
        // Phase 1: find the meeting point inside the cycle
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        // Phase 2: find the cycle entrance = duplicate
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
};
```

**Java**
```java
class Solution {
    public int findDuplicate(int[] nums) {
        int slow = nums[0], fast = nums[0];
        // Phase 1: find the meeting point inside the cycle
        do {
            slow = nums[slow];
            fast = nums[nums[fast]];
        } while (slow != fast);
        // Phase 2: find the cycle entrance = duplicate
        slow = nums[0];
        while (slow != fast) {
            slow = nums[slow];
            fast = nums[fast];
        }
        return slow;
    }
}
```

**Python**
```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow = fast = nums[0]
        # Phase 1: find the meeting point inside the cycle
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        # Phase 2: find the cycle entrance = duplicate
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```

### Complexity
- **Time**: O(n) — both phases are linear in the chain length.
- **Space**: O(1) — two integer indices, no modification of `nums`.

### Verdict
The intended optimal answer. It satisfies every constraint at once: linear time, constant space, read-only array. The leap "array → implicit linked list → Floyd" is the entire trick and a classic interview reveal.

---

## Approach 3 — Binary search on the value range

### Intuition
Binary-search the *answer value*, not an index. For a candidate `mid`, count how many array elements are `<= mid`. If the count exceeds `mid`, the duplicate lies in `[low, mid]` (pigeonhole: too many small values); otherwise it's in `[mid+1, high]`. This also respects the read-only and O(1)-space constraints, at the cost of an extra log factor.

### Algorithm
1. `low = 1`, `high = n`.
2. While `low < high`:
   - `mid = (low + high) / 2`.
   - `count = number of nums[i] <= mid`.
   - If `count > mid` → `high = mid`; else `low = mid + 1`.
3. Return `low`.

### Dry run on `[1, 3, 4, 2, 2]` (n = 4)
```
low=1 high=4
mid=2: count(≤2) = {1,2,2} = 3 > 2 → high=2
low=1 high=2
mid=1: count(≤1) = {1} = 1, not > 1 → low=2
low==high=2 → return 2 ✅
```

### Code

**C++**
```cpp
class Solution {
public:
    int findDuplicate(vector<int>& nums) {
        int low = 1, high = (int)nums.size() - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            int count = 0;
            for (int x : nums) if (x <= mid) count++;
            if (count > mid) high = mid;
            else low = mid + 1;
        }
        return low;
    }
};
```

**Java**
```java
class Solution {
    public int findDuplicate(int[] nums) {
        int low = 1, high = nums.length - 1;
        while (low < high) {
            int mid = low + (high - low) / 2;
            int count = 0;
            for (int x : nums) if (x <= mid) count++;
            if (count > mid) high = mid;
            else low = mid + 1;
        }
        return low;
    }
}
```

**Python**
```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        low, high = 1, len(nums) - 1
        while low < high:
            mid = (low + high) // 2
            count = sum(1 for x in nums if x <= mid)
            if count > mid:
                high = mid
            else:
                low = mid + 1
        return low
```

### Complexity
- **Time**: O(n log n) — log n binary-search steps, each an O(n) count.
- **Space**: O(1).

### Verdict
A strong alternative if you don't recall the Floyd reframing. It's read-only and constant-space, just a log factor slower. Good to mention as a backup.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Modifies array | Notes |
|----------|------|-------|----------------|-------|
| Hash set | O(n) | O(n) | no | violates space constraint |
| Sort + scan | O(n log n) | O(1) | **yes** | violates no-modify constraint |
| Binary search on value | O(n log n) | **O(1)** | no | satisfies constraints; log factor |
| Floyd cycle detection | **O(n)** | **O(1)** | no | optimal; the intended answer ⭐ |

---

## 🧪 Edge cases & pitfalls
- **Duplicate appears more than twice** (`[3,3,3,3,3]`) → Floyd still works; the cycle simply has the repeated value as its entrance.
- **Why start at index 0?** Values are in `[1, n]`, so no value ever points to index 0; therefore index 0 is never inside the cycle, guaranteeing the chain *enters* a cycle from outside (a valid "ρ shape" for Floyd).
- **Pitfall — `do/while` vs `while`**: Phase 1 must step *before* comparing (both start equal at `nums[0]`); a plain `while (slow != fast)` would exit immediately. Use `do/while` (C++/Java) or `while True` with a break (Python).
- **Pitfall — modifying the array (negation/marking)**: there's a popular O(n)/O(1) trick that negates `nums[abs(x)]`, but it **mutates the array**, violating the constraint. Don't use it here.
- **Pitfall (binary search) — counting `< mid` vs `<= mid`**: must count `<= mid`. The invariant is "if more than `mid` values are ≤ `mid`, a duplicate is in the lower half."

---

## 🔗 Related problems
- **Linked List Cycle II** (LC 142) — the pure linked-list version of Floyd's entrance-finding.
- **Linked List Cycle** (LC 141) — cycle existence. See [`03-Linked-List-Cycle.md`](./03-Linked-List-Cycle.md).
- **Contains Duplicate** (LC 217) — duplicate existence with no special constraints (hash set).
- **Missing Number** (LC 268) / **Set Mismatch** (LC 645) — related index-as-value array tricks.

---

**→ Next:** [`09-LRU-Cache.md`](./09-LRU-Cache.md) | **← Prev:** [`07-Add-Two-Numbers.md`](./07-Add-Two-Numbers.md) | Back to [`00-Index.md`](./00-Index.md)
