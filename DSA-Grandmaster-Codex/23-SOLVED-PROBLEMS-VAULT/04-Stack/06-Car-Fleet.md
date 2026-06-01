# Car Fleet

**Platform**: LeetCode 853 · **Difficulty**: Medium · **Topics**: Array, Stack, Sorting, Monotonic Stack · **Pattern**: Sort by position descending, compare arrival times

---

## 📜 Problem Statement

There are `n` cars going to the same destination along a one-lane road. The destination is `target` miles away.

You are given two integer arrays `position` and `speed`, both of length `n`, where `position[i]` is the position of the `i`th car and `speed[i]` is the speed of the `i`th car (in miles per hour).

A car can never pass another car ahead of it, but it can catch up to it and drive bumper to bumper **at the same speed**. The faster car will slow down to match the slower car's speed. The distance between these two cars is ignored (i.e., they are assumed to be at the same position).

A **car fleet** is some non-empty set of cars driving at the same position and same speed. Note that a single car is also a car fleet.

If a car catches up to a car fleet right at the destination point, it still counts as one fleet.

Return the number of car fleets that will arrive at the destination.

### Examples

**Example 1:**
```
Input:  target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
Output: 3
Explanation:
  Car at pos 10, speed 2: arrives at time (12-10)/2 = 1.0
  Car at pos 8, speed 4:  arrives at time (12-8)/4 = 1.0  → catches car at 10, forms fleet
  Car at pos 0, speed 1:  arrives at time (12-0)/1 = 12.0
  Car at pos 5, speed 1:  arrives at time (12-5)/1 = 7.0
  Car at pos 3, speed 3:  arrives at time (12-3)/3 = 3.0  → catches car at 5? No, 3.0 < 7.0 means it arrives earlier if alone, but car at 5 is ahead and slower → car at 3 is blocked by car at 5 → they form a fleet at speed 1
  
  Fleets: {10,8}, {5,3}, {0} → 3 fleets
```

**Example 2:**
```
Input:  target = 10, position = [3], speed = [3]
Output: 1
```

**Example 3:**
```
Input:  target = 100, position = [0,2,4], speed = [4,2,1]
Output: 1
Explanation: 
  Car at 4, speed 1: time = 96
  Car at 2, speed 2: time = 49 < 96 → blocked by car at 4, joins fleet
  Car at 0, speed 4: time = 25 < 96 → blocked by the fleet ahead, joins fleet
  All merge into 1 fleet.
```

### Constraints
```
n == position.length == speed.length
1 <= n <= 10^5
0 < target <= 10^6
0 <= position[i] < target
All the values of position are unique.
0 < speed[i] <= 10^6
```

---

## 🧠 Understanding the problem

Key insight: a car behind another car can only merge into it (forming a fleet), never pass it. So we process cars from **closest to target** to **farthest**. Each car's "arrival time" (if it were alone) is `(target - position) / speed`.

If a car behind has a shorter or equal arrival time than the car/fleet ahead, it will catch up → they merge (the fleet's arrival time stays the slower one's). If it has a longer arrival time, it can never catch up → it starts a new fleet.

---

## Approach 1 — Brute force (simulation)

### Intuition
Simulate the cars moving second by second until all reach the target. Track which cars merge. This is conceptually correct but impractical for the given constraints.

### Verdict
O(target × n) time — far too slow. We skip the implementation and go to the analytical approach.

---

## Approach 2 — Sort + stack of arrival times (optimal) ⭐

### Intuition
Sort cars by position descending (closest to target first). Compute each car's arrival time. Use a stack: if the current car's time is greater than the stack's top, it forms a new fleet (push). Otherwise, it merges into the fleet ahead (don't push).

### Algorithm
1. Pair up `(position[i], speed[i])` and sort by position **descending**.
2. Initialize an empty stack (stores arrival times of fleet leaders).
3. For each car in sorted order:
   - Compute `time = (target - position) / speed`.
   - If stack is empty OR `time > stack.top()` → new fleet, push `time`.
   - Else → this car merges into the fleet ahead (do nothing).
4. Return `stack.size()`.

### Dry run on target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]
```
Sort by position desc: [(10,2), (8,4), (5,1), (3,3), (0,1)]
Times: [1.0, 1.0, 7.0, 3.0, 12.0]

Car (10,2): time=1.0, stack empty → push. Stack: [1.0]
Car (8,4):  time=1.0, 1.0 <= 1.0 → merges. Stack: [1.0]
Car (5,1):  time=7.0, 7.0 > 1.0 → new fleet. Stack: [1.0, 7.0]
Car (3,3):  time=3.0, 3.0 <= 7.0 → merges. Stack: [1.0, 7.0]
Car (0,1):  time=12.0, 12.0 > 7.0 → new fleet. Stack: [1.0, 7.0, 12.0]

Answer: 3 ✓
```

### Code
```cpp
class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        vector<pair<int,int>> cars(n);
        for (int i = 0; i < n; i++)
            cars[i] = {position[i], speed[i]};
        
        // Sort by position descending (closest to target first)
        sort(cars.begin(), cars.end(), [](auto& a, auto& b) {
            return a.first > b.first;
        });
        
        stack<double> st; // arrival times of fleet leaders
        for (auto& [pos, spd] : cars) {
            double time = (double)(target - pos) / spd;
            if (st.empty() || time > st.top()) {
                st.push(time); // new fleet
            }
            // else: merges into fleet ahead, do nothing
        }
        return st.size();
    }
};
```
```java
class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        int[][] cars = new int[n][2];
        for (int i = 0; i < n; i++) {
            cars[i][0] = position[i];
            cars[i][1] = speed[i];
        }

        // Sort by position descending (closest to target first)
        Arrays.sort(cars, (a, b) -> b[0] - a[0]);

        Deque<Double> st = new ArrayDeque<>(); // arrival times of fleet leaders
        for (int[] car : cars) {
            double time = (double)(target - car[0]) / car[1];
            if (st.isEmpty() || time > st.peek()) {
                st.push(time); // new fleet
            }
            // else: merges into fleet ahead, do nothing
        }
        return st.size();
    }
}
```
```python
class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        # Sort by position descending
        cars = sorted(zip(position, speed), key=lambda x: -x[0])
        
        stack = []  # arrival times of fleet leaders
        for pos, spd in cars:
            time = (target - pos) / spd
            if not stack or time > stack[-1]:
                stack.append(time)  # new fleet
            # else: merges into fleet ahead
        
        return len(stack)
```

### Complexity
- **Time**: O(n log n) — dominated by the sort.
- **Space**: O(n) — for the sorted array and stack.

### Verdict
**The optimal answer.** The sort is unavoidable (we need position order), and the stack pass is O(n).

---

## Approach 3 — Sort + counter (no explicit stack)

### Intuition
We don't actually need a stack — just a counter and the last fleet's arrival time. If the current car's time exceeds the last fleet's time, increment the counter and update the last time.

### Code
```cpp
class Solution {
public:
    int carFleet(int target, vector<int>& position, vector<int>& speed) {
        int n = position.size();
        vector<pair<int,int>> cars(n);
        for (int i = 0; i < n; i++)
            cars[i] = {position[i], speed[i]};
        
        sort(cars.begin(), cars.end(), [](auto& a, auto& b) {
            return a.first > b.first;
        });
        
        int fleets = 0;
        double lastTime = 0;
        for (auto& [pos, spd] : cars) {
            double time = (double)(target - pos) / spd;
            if (time > lastTime) {
                fleets++;
                lastTime = time;
            }
        }
        return fleets;
    }
};
```
```java
class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        int[][] cars = new int[n][2];
        for (int i = 0; i < n; i++) {
            cars[i][0] = position[i];
            cars[i][1] = speed[i];
        }

        Arrays.sort(cars, (a, b) -> b[0] - a[0]);

        int fleets = 0;
        double lastTime = 0;
        for (int[] car : cars) {
            double time = (double)(target - car[0]) / car[1];
            if (time > lastTime) {
                fleets++;
                lastTime = time;
            }
        }
        return fleets;
    }
}
```
```python
class Solution:
    def carFleet(self, target: int, position: list[int], speed: list[int]) -> int:
        cars = sorted(zip(position, speed), key=lambda x: -x[0])
        
        fleets = 0
        last_time = 0.0
        for pos, spd in cars:
            time = (target - pos) / spd
            if time > last_time:
                fleets += 1
                last_time = time
        
        return fleets
```

### Complexity
- **Time**: O(n log n) — sort dominates.
- **Space**: O(n) for sorted array, O(1) extra.

### Verdict
Slightly cleaner — same logic without the explicit stack data structure. Both are equally valid interview answers.

---

## ⚖️ Approach comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Simulation | O(target × n) | O(n) | Impractical |
| Sort + stack | **O(n log n)** | O(n) | Clear stack-based ⭐ |
| Sort + counter | **O(n log n)** | O(n) | Simplified variant |

---

## 🧪 Edge cases & pitfalls
- **Single car** → always 1 fleet.
- **All cars same speed** → no merging possible (unless same position, which constraints forbid) → n fleets.
- **All cars merge** (Example 3) → 1 fleet.
- **Cars at position 0** → valid, time = target / speed.
- **Floating point**: use `double` for time calculations. Integer division would lose precision.
- **Pitfall**: sorting ascending instead of descending — you'd compare against the wrong fleet.
- **Pitfall**: using `>=` instead of `>` for the merge condition — equal arrival times DO merge (they meet exactly at the destination).

---

## 🔗 Related problems
- **Car Fleet II** (LC 1776) — harder variant with collision times.
- **Boats to Save People** (LC 881) — greedy pairing.
- **Meeting Rooms II** (LC 253) — interval scheduling with sorting.
- **Daily Temperatures** (LC 739) — monotonic stack pattern.

---

**→ Prev:** [`05-Daily-Temperatures.md`](./05-Daily-Temperatures.md) · **→ Next:** [`07-Largest-Rectangle-Histogram.md`](./07-Largest-Rectangle-Histogram.md) | [Problem set index](./00-Index.md)
