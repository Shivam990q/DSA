# 🧪 Stress Testing — The Bug Murderer

> *"Stress testing finds the bug you swear isn't there."*

---

## I. THE CONCEPT
Compare your solution against a slow-but-correct brute force on thousands of random inputs. Any mismatch reveals a bug.

---

## II. THE 4-FILE SETUP
1. **gen.cpp** — random valid input generator (seeded)
2. **brute.cpp** — obviously-correct, slow solution
3. **sol.cpp** — your optimized solution
4. **runner** — script that loops, compares, reports mismatches

See [`../19-TEMPLATES-AND-IMPLEMENTATIONS/stress-test-runner.sh`](../19-TEMPLATES-AND-IMPLEMENTATIONS/stress-test-runner.sh).

---

## III. THE GENERATOR
```cpp
#include <bits/stdc++.h>
using namespace std;
int main(int argc, char* argv[]) {
    srand(atoi(argv[1]));        // seed from command line
    int n = rand() % 10 + 1;     // SMALL inputs (brute must be fast)
    cout << n << "\n";
    for (int i = 0; i < n; i++)
        cout << rand() % 20 << " \n"[i == n-1];
    return 0;
}
```

Key: keep inputs SMALL so brute force runs fast and bugs surface on simple cases.

---

## IV. THE RUNNER (Linux/Mac)
```bash
for i in {1..10000}; do
    ./gen $i > in.txt
    ./brute < in.txt > b.txt
    ./sol < in.txt > s.txt
    if ! diff -q b.txt s.txt > /dev/null; then
        echo "MISMATCH seed $i"; cat in.txt; break
    fi
done
echo "ALL PASSED"
```

---

## V. WHEN TO STRESS TEST
- Whenever you get WA on a problem you "thought was right"
- For ALL greedy solutions (greedy is often subtly wrong)
- For complex DP / data structure code
- Before final submit on hard problems

---

## VI. WHAT STRESS TESTING CATCHES
- Off-by-one errors
- Edge cases (n=1, all same)
- Wrong greedy choices
- Integer overflow (if brute uses bigger types)
- Incorrect algorithm logic

---

## VII. WHAT IT DOESN'T CATCH
- TLE (it tests correctness, not speed) — test large inputs separately
- Bugs only on huge inputs that brute can't handle — use targeted large tests
- Bugs that both brute and sol share (write brute independently!)

---

## VIII. THE DISCIPLINE
A grandmaster stress-tests by REFLEX. The 5 minutes setting it up saves hours of blind debugging. Make it a habit.

---

**→ Next:** [`11-Template-Engineering.md`](./11-Template-Engineering.md)
