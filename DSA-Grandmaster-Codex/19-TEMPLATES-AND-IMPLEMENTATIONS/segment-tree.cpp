// Segment Tree (recursive + iterative) — point update + range query
// Replace `+` (and identity 0) with any associative op (min, max, gcd, etc.)

// ===== RECURSIVE VERSION =====
struct SegTreeRec {
    int n;
    vector<long long> tree;
    
    SegTreeRec(int n_) : n(n_), tree(4 * n_, 0) {}
    
    void build(vector<int>& a, int node, int l, int r) {
        if (l == r) { tree[node] = a[l]; return; }
        int m = (l + r) / 2;
        build(a, 2*node, l, m);
        build(a, 2*node+1, m+1, r);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    void update(int node, int l, int r, int idx, int val) {
        if (l == r) { tree[node] = val; return; }
        int m = (l + r) / 2;
        if (idx <= m) update(2*node, l, m, idx, val);
        else update(2*node+1, m+1, r, idx, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    long long query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[node];
        int m = (l + r) / 2;
        return query(2*node, l, m, ql, qr) + query(2*node+1, m+1, r, ql, qr);
    }
    
    void update(int idx, int val) { update(1, 0, n-1, idx, val); }
    long long query(int l, int r) { return query(1, 0, n-1, l, r); }
};

// ===== ITERATIVE VERSION (faster, no recursion overhead) =====
template<typename T>
struct SegTreeIter {
    int n;
    vector<T> t;
    T identity;
    function<T(T, T)> combine;
    
    SegTreeIter(int n_, T id, function<T(T, T)> op)
        : n(n_), t(2 * n_, id), identity(id), combine(op) {}
    
    void build(vector<T>& a) {
        for (int i = 0; i < n; i++) t[n + i] = a[i];
        for (int i = n - 1; i > 0; --i) t[i] = combine(t[2*i], t[2*i + 1]);
    }
    
    void update(int p, T val) {
        for (t[p += n] = val; p >>= 1; )
            t[p] = combine(t[2*p], t[2*p + 1]);
    }
    
    T query(int l, int r) {  // [l, r), exclusive r
        T resL = identity, resR = identity;
        for (l += n, r += n; l < r; l >>= 1, r >>= 1) {
            if (l & 1) resL = combine(resL, t[l++]);
            if (r & 1) resR = combine(t[--r], resR);
        }
        return combine(resL, resR);
    }
};

// Usage:
// SegTreeIter<long long> st(n, 0, [](long long a, long long b) { return a + b; });
// st.build(arr);
// st.update(3, 10);
// long long s = st.query(0, n);  // sum [0, n)
