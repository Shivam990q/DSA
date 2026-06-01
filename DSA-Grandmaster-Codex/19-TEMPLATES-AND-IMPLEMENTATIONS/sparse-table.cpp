// Sparse Table — O(1) RMQ (or other idempotent ops) on static arrays
// Build: O(n log n), Query: O(1)

template<typename T, typename F = function<T(const T&, const T&)>>
class SparseTable {
    vector<vector<T>> sp;
    F op;
public:
    SparseTable(const vector<T>& a, F op_) : op(op_) {
        int n = a.size();
        int LOG = __lg(n) + 1;
        sp.assign(LOG, vector<T>(n));
        sp[0] = a;
        for (int k = 1; k < LOG; k++) {
            for (int i = 0; i + (1 << k) <= n; i++) {
                sp[k][i] = op(sp[k-1][i], sp[k-1][i + (1 << (k-1))]);
            }
        }
    }
    
    T query(int l, int r) {  // [l, r] inclusive
        int k = __lg(r - l + 1);
        return op(sp[k][l], sp[k][r - (1 << k) + 1]);
    }
};

// Usage:
// SparseTable<int> st(arr, [](int a, int b) { return min(a, b); });
// int result = st.query(2, 7);  // min in [2, 7]
