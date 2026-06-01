// Disjoint Set Union (Union-Find) with path compression + union by rank
// Time: nearly O(1) amortized per operation (inverse Ackermann)

struct DSU {
    vector<int> parent, rank_;
    int components;
    
    DSU(int n) : parent(n), rank_(n, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }
    
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    
    bool unite(int x, int y) {
        x = find(x); y = find(y);
        if (x == y) return false;
        if (rank_[x] < rank_[y]) swap(x, y);
        parent[y] = x;
        if (rank_[x] == rank_[y]) rank_[x]++;
        --components;
        return true;
    }
    
    bool connected(int x, int y) { return find(x) == find(y); }
};
