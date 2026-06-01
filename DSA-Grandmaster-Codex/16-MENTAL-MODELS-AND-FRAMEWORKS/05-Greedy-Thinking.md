# 💎 Greedy Thinking

> *"Make the locally optimal choice. Pray (or prove) it's globally optimal."*

---

## THE WORLDVIEW
At each step, pick the choice that looks best right now. Works ONLY when the greedy choice property + optimal substructure hold.

## THE TRIGGERS
- "Sort by ..."
- "Pick the smallest/largest/earliest first"
- "Minimize/maximize with a single sweep"

## THE CRITICAL RULE
**Greedy requires proof.** Without proof, it's a guess. Most wrong greedy solutions LOOK right.

## THE TWO PROOF TECHNIQUES
1. **Exchange argument**: any optimal solution can be transformed into the greedy one without getting worse.
2. **Greedy stays ahead**: greedy's partial solution is always ≥ any other's.

## MANIFESTATIONS
- Activity selection (sort by end time)
- Huffman coding (merge smallest)
- Kruskal/Prim MST
- Dijkstra (closest unvisited)
- Fractional knapsack (best ratio first)
- Job scheduling (earliest deadline)

## WHEN GREEDY FAILS
- 0/1 knapsack (use DP)
- Coin change with arbitrary denominations (use DP)
- Whenever a "later" cost depends on "earlier" choices non-trivially

## THE GREEDY CHECKLIST
1. State the greedy choice precisely.
2. Try counterexamples (small cases).
3. Prove (or sketch) correctness.
4. If unsure, write DP as backup.

## EXERCISE
Decide greedy or DP:
1. Maximum non-overlapping intervals → greedy (sort by end)
2. Coin change [1,3,4], target 6 → DP (greedy fails!)
3. Minimum platforms for trains → greedy (sweep)
4. 0/1 knapsack → DP

---

**→ Next:** [`06-Mathematical-Thinking.md`](./06-Mathematical-Thinking.md) | Deep dive: [`../05-ALGORITHMS-UNIVERSE/04-Greedy-Algorithms.md`](../05-ALGORITHMS-UNIVERSE/04-Greedy-Algorithms.md)
