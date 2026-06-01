# 🔢 Game Theory (Combinatorial Games)

> *"Two players, perfect information, no luck. Who wins? Math knows."*

---

## I. COMBINATORIAL GAMES
- Two players alternate moves; perfect information; no chance.
- **Normal play**: the player who cannot move LOSES.
- **Misère play**: the player who cannot move WINS (trickier).
- **Impartial game**: both players have the same moves available (depends only on position, not whose turn). Nim is impartial.
- **Partisan game**: players have different moves (e.g., chess).

---

## II. WINNING & LOSING POSITIONS (P/N)
- **P-position** (Previous player wins): a LOSING position for the player to move.
- **N-position** (Next player wins): a WINNING position.
- Rules:
  - A position is **P** if ALL moves lead to N-positions.
  - A position is **N** if SOME move leads to a P-position.
- Terminal (no moves) = P-position (in normal play).

DP over positions computes P/N for finite games.

---

## III. NIM ⭐
Several piles of stones; a move removes ≥1 stone from one pile. Normal play.
- **Theorem (Bouton)**: the position is a LOSS for the player to move iff the **XOR of all pile sizes = 0**.
- Strategy: move to make XOR become 0.

```cpp
bool firstPlayerWins(vector<int>& piles) {
    int x = 0; for (int p : piles) x ^= p;
    return x != 0;  // nonzero XOR => first player (mover) wins
}
```

---

## IV. SPRAGUE-GRUNDY THEOREM ⭐⭐
**Every impartial game position is equivalent to a Nim pile of some size — its Grundy number (nimber).**

- **Grundy(position)** = mex{ Grundy(next positions) }
  where **mex**(S) = smallest non-negative integer NOT in S.
- A position is losing (P) iff Grundy = 0.

```cpp
int grundy(state) {
    if (terminal) return 0;
    set<int> s;
    for (next : moves(state)) s.insert(grundy(next));
    int m = 0; while (s.count(m)) m++;  // mex
    return m;
}
```

---

## V. SUM OF GAMES ⭐
If a game splits into independent sub-games played simultaneously (a move is made in exactly one), the Grundy number of the whole = **XOR of the sub-games' Grundy numbers**.

- This is why Nim works: each pile is an independent game with Grundy = pile size; whole-game Grundy = XOR.

---

## VI. CLASSIC GAMES & THEIR GRUNDY
- **Nim**: Grundy(pile of n) = n
- **Subtraction game** (remove from a fixed set S): Grundy via mex, often periodic
- **Staircase Nim**, **Misère Nim** (special-case analysis), **Green Hackenbush** (impartial)
- **Wythoff's game**: losing positions relate to the golden ratio

---

## VII. GAME DP (for non-impartial / scoring games)
For games where players maximize a score (not just win/lose):
- **Minimax DP**: dp[state] = best achievable score difference for the mover.
- Stone Game series (LC 877, 1140, 1406, ...): dp[i][j] = max score difference on segment [i, j].

```cpp
// Stone Game style:
// dp[i][j] = max(a[i] - dp[i+1][j], a[j] - dp[i][j-1])
```

---

## VIII. PROBLEMS
- Nim Game (LC 292), Stone Game I-IX (LC 877, 1140, 1406, 1510, ...)
- Predict the Winner (LC 486)
- Flip Game II (LC 294)
- Can I Win (LC 464) — bitmask game DP
- [CSES](https://cses.fi/problemset/) "Nim Game I/II", "Stair Game", "Grundy's Game"
- CF problems tagged "games" / "dp" + "games"

---

## IX. THE DECISION TREE
```
Impartial game, win/lose only?  → Sprague-Grundy (Grundy numbers + XOR)
Single Nim-like?                → XOR of piles
Scoring game (maximize points)? → Minimax DP
Misère play?                    → special analysis (often Nim with a twist)
```

---

**→ Next:** [`10-Generating-Functions.md`](./10-Generating-Functions.md)
