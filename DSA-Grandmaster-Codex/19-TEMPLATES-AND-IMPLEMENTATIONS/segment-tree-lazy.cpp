// Segment Tree with Lazy Propagation (range add, range sum)
// Build: O(n), Update/Query: O(log n)

struct LazySegTree {
    int n;
    vector<long long> tree, lazy;
    
    LazySegTree(int n_) : n(n_), tree(4 * n_, 0), lazy(4 * n_, 0) {}
    
    void build(vector<long long>& a, int node, int l, int r) {
        if (l == r) { tree[node] = a[l]; return; }
        int m = (l + r) / 2;
        build(a, 2*node, l, m);
        build(a, 2*node+1, m+1, r);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    void push(int node, int l, int r) {
        if (lazy[node]) {
            tree[node] += lazy[node] * (r - l + 1);
            if (l != r) {
                lazy[2*node] += lazy[node];
                lazy[2*node+1] += lazy[node];
            }
            lazy[node] = 0;
        }
    }
    
    void update(int node, int l, int r, int ql, int qr, long long val) {
        push(node, l, r);
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            lazy[node] += val;
            push(node, l, r);
            return;
        }
        int m = (l + r) / 2;
        update(2*node, l, m, ql, qr, val);
        update(2*node+1, m+1, r, ql, qr, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    long long query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        push(node, l, r);
        if (ql <= l && r <= qr) return tree[node];
        int m = (l + r) / 2;
        return query(2*node, l, m, ql, qr) + query(2*node+1, m+1, r, ql, qr);
    }
    
    void update(int l, int r, long long val) { update(1, 0, n-1, l, r, val); }
    long long query(int l, int r) { return query(1, 0, n-1, l, r); }
};
