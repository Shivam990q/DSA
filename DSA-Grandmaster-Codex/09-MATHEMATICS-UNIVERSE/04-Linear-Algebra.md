# 🔢 Linear Algebra for CP

> *"Matrix exponentiation turns linear recurrences from O(n) into O(log n)."*

---

## I. MATRICES
- An n×m matrix; multiplication: (n×m)·(m×p) = n×p, cost O(nmp).
- Identity matrix I; A·I = A.

```cpp
typedef vector<vector<long long>> Mat;
Mat mul(const Mat& A, const Mat& B, long long mod) {
    int n = A.size(), m = B[0].size(), k = B.size();
    Mat C(n, vector<long long>(m, 0));
    for (int i = 0; i < n; i++)
        for (int x = 0; x < k; x++) if (A[i][x])
            for (int j = 0; j < m; j++)
                C[i][j] = (C[i][j] + A[i][x]*B[x][j]) % mod;
    return C;
}
```

---

## II. MATRIX EXPONENTIATION ⭐
To compute A^k: binary exponentiation on matrices, O(d³ log k) for d×d matrix.
```cpp
Mat matpow(Mat A, long long k, long long mod) {
    int d = A.size();
    Mat R(d, vector<long long>(d, 0));
    for (int i = 0; i < d; i++) R[i][i] = 1;  // identity
    while (k) { if (k&1) R = mul(R,A,mod); A = mul(A,A,mod); k >>= 1; }
    return R;
}
```

### Use: Fibonacci in O(log n)
[[F(n+1)],[F(n)]] = [[1,1],[1,0]]^n · [[1],[0]]
So F(n) is read from the matrix power.

### General linear recurrence
For a_n = c1·a_{n-1} + c2·a_{n-2} + ... + ck·a_{n-k}, build a k×k companion matrix; matrix power gives the nth term in O(k³ log n).

---

## III. OTHER MATRIX-EXP USES
- **Counting paths of length k** in a graph: (adjacency matrix)^k gives path counts.
- **DP with fixed transitions** repeated many times → encode transition as a matrix.
- **Probability transitions** (Markov chains over many steps).

---

## IV. GAUSSIAN ELIMINATION
Solve a system Ax = b in O(n³):
- Forward elimination to row echelon form, then back-substitution.
- Also computes: determinant, rank, matrix inverse.
- **Over GF(2)** (XOR): solve linear systems mod 2 with bitsets — fast; used for "XOR basis" problems.

---

## V. XOR BASIS (linear algebra over GF(2)) ⭐
A set of numbers under XOR forms a vector space over GF(2). Maintain a basis to:
- Check if a value is representable as XOR of a subset
- Count distinct XOR values (2^(basis size))
- Find max XOR subset
```cpp
int basis[30]; // for 30-bit numbers
void insert(int x) {
    for (int b = 29; b >= 0; b--) {
        if (!((x>>b)&1)) continue;
        if (!basis[b]) { basis[b] = x; return; }
        x ^= basis[b];
    }
}
```

---

## VI. DETERMINANT, RANK, INVERSE
- Determinant via Gaussian elimination (track row swaps for sign).
- Rank = number of nonzero pivot rows.
- Inverse: augment with identity, reduce.

---

## VII. PROBLEMS
- Fibonacci / linear recurrences with huge n (matrix exp)
- Count paths of length k in a graph
- [CSES](https://cses.fi/problemset/) "Throwing Dice" (matrix exp), "Graph Paths"
- Maximum XOR subset (XOR basis)
- CF problems tagged "matrices" / "math"

---

## VIII. TEMPLATE
Matrix multiply + power in [`../19-TEMPLATES-AND-IMPLEMENTATIONS/number-theory.cpp`](../19-TEMPLATES-AND-IMPLEMENTATIONS/number-theory.cpp) (and Math Toolkit §04).

---

**→ Next:** [`05-FFT-NTT.md`](./05-FFT-NTT.md)
