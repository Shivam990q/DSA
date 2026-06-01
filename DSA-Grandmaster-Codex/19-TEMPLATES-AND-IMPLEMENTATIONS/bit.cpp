// Binary Indexed Tree (Fenwick Tree)
// Point update, prefix/range sum query — both O(log n)

struct BIT {
    int n;
    vector<long long> t;
    BIT(int n) : n(n), t(n + 1, 0) {}
    
    void update(int i, long long v) {  // 0-indexed
        for (++i; i <= n; i += i & -i) t[i] += v;
    }
    
    long long query(int i) {  // sum [0..i]
        long long s = 0;
        for (++i; i > 0; i -= i & -i) s += t[i];
        return s;
    }
    
    long long range(int l, int r) {
        return query(r) - (l > 0 ? query(l - 1) : 0);
    }
};
