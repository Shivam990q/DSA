# 🎚️ State Modeling — The Bookkeeping of Reality

> *"A program is a state machine pretending to be prose."*

---

## I. WHAT IS STATE?

**State** = the complete description of a system at a given moment, sufficient to determine its future behavior given inputs.

For a simple counter: `state = current_count`.
For a chess game: `state = (board configuration, whose turn, castling rights, en passant target, half-move clock, full-move number)`.

---

## II. STATE IN DSA

Every algorithm maintains state. Identifying state is the first step to:

1. **DP** — what's the *minimal* state representing a subproblem?
2. **Search/BFS** — what defines a "node" in the state graph?
3. **Simulation** — what variables capture "where I am"?
4. **Invariants** — what properties of state never change?

---

## III. THE STATE-DESIGN TEMPLATE

For any DP/search problem:

1. **What's the answer's signature?** (output)
2. **What's varying as I make decisions?** (state variables)
3. **What's the smallest state that captures all decision-relevant info?**
4. **What are the transitions?**
5. **What's the base?**

> Example: Coin change — given coins, target T, find min coins.
> - Output: integer (min count)
> - Varying: amount remaining
> - State: `dp[i]` = min coins to make i
> - Transition: `dp[i] = min(dp[i-c] + 1)` for c in coins
> - Base: `dp[0] = 0`

---

## IV. STATE EXPLOSION & COMPRESSION

A state can have too many dimensions:
- "Stocks held" + "transactions used" + "cooldown active" + "current day" → 4D state
- TSP: "cities visited" + "current city" → 2D where the first is a *bitmask*

**Compression techniques**:
- Drop redundant dimensions (if derivable)
- Use bitmask for set membership (n ≤ 20)
- Coordinate compression (huge values → small indices)
- Hash encoding (state → int)

---

## V. INVARIANTS

An **invariant** is a property of state that holds throughout an algorithm's execution.

> Example: in BFS, "the queue contains exactly the nodes at distance d or d+1 from source, never further."

> Example: in quicksort partition, "elements ≤ pivot are in [low, i], elements > pivot are in (i, j)."

Invariants are **proof tools**. Identifying them is how you prove correctness.

### Loop invariant
A statement true at the start of each iteration:
```
INVARIANT: After iteration i, dp[0..i] contains correct min-coin-count for amounts 0..i.
```

If invariant holds:
- Initially (base case)
- After each step (preserved)
- At termination (gives final answer)

→ Algorithm is correct (induction).

---

## VI. MUTATION VS IMMUTABILITY

### Mutable state
```python
nums = [1, 2, 3]
nums.append(4)         # nums is now [1, 2, 3, 4]
```
- Easier to update
- Hard to reason about (who modified what?)
- Concurrency hazard

### Immutable state
```python
nums = (1, 2, 3)
new_nums = nums + (4,)  # new tuple; original unchanged
```
- Easier to reason about (no aliasing surprises)
- Slower (allocation overhead)
- Safer concurrent

**Rule of thumb**: prefer immutability for clarity. Switch to mutation only when performance demands.

---

## VII. STATE MACHINES

A formal model: nodes = states, edges = transitions on input.

> Example: regex `a*b` as a state machine:
> - State 0: start
> - On 'a': stay in state 0
> - On 'b': go to state 1 (accept)

State machines underpin:
- Lexers/parsers
- Network protocols (TCP)
- Game AI
- Regular expressions
- Many DP problems (state machine DP — paint house, stock with cooldown)

---

## VIII. STATE IN GRAPH SEARCH

When you do BFS/DFS, the **state space graph** has nodes = states, edges = legal transitions.

> Example: 8-puzzle. State = board configuration. ~9!/2 = 181,440 states. Find path from initial to goal.

Often the state graph is **implicit** (computed on the fly), not built ahead.

---

## IX. EXERCISE: IDENTIFY THE STATE

For each problem, identify the minimal state for DP/search:

1. **Best time to buy/sell stock with cooldown**  
   *State*: `(day, holding?)` (2D, where holding is 0/1)

2. **Coin change (number of ways)**  
   *State*: `(amount, coin_index)` or `(amount)` if iterated outer

3. **Edit distance**  
   *State*: `(i, j)` — index in word1, index in word2

4. **Travelling Salesman Problem**  
   *State*: `(visited_set_bitmask, current_city)`

5. **Knight's shortest path**  
   *State*: `(x, y)`

6. **Sudoku**  
   *State*: full board (all 81 cells)

---

## X. THE FIVE STATE-DESIGN PRINCIPLES

1. **Minimality**: smallest state that determines transitions and answer
2. **Completeness**: state must capture all decision-relevant info
3. **Markov property**: future depends only on state, not history
4. **Identifiability**: equal states should produce equal answers
5. **Computability**: transitions efficient to compute

---

## XI. THE FINAL TRUTH

> **"You don't solve a DP problem.  
>  You discover its state.  
>  Once the state is right, the transitions are forced.  
>  The hard part is *seeing the state*."**

---

**→ Next:** [`06-Complexity-Thinking.md`](./06-Complexity-Thinking.md)
