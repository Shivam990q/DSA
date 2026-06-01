// =============================================================
// GRAPH ALGORITHMS — REFERENCE IMPLEMENTATIONS
// =============================================================
// Includes: BFS, DFS, Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal, Prim, TopSort

#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 1e18;

// -------- BFS --------
vector<int> bfs(int src, int n, vector<vector<int>>& adj) {
    vector<int> dist(n, -1);
    queue<int> q; q.push(src); dist[src] = 0;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u])
            if (dist[v] == -1) { dist[v] = dist[u] + 1; q.push(v); }
    }
    return dist;
}

// -------- DFS (iterative) --------
void dfs(int src, int n, vector<vector<int>>& adj, vector<bool>& visited) {
    stack<int> stk; stk.push(src);
    while (!stk.empty()) {
        int u = stk.top(); stk.pop();
        if (visited[u]) continue;
        visited[u] = true;
        for (int v : adj[u]) if (!visited[v]) stk.push(v);
    }
}

// -------- Dijkstra (non-negative weights) --------
vector<ll> dijkstra(int src, int n, vector<vector<pair<int,int>>>& adj) {
    vector<ll> dist(n, INF); dist[src] = 0;
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    pq.push({0, src});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u])
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
    }
    return dist;
}

// -------- Bellman-Ford (handles negative; detects negative cycle) --------
vector<ll> bellmanFord(int src, int n, vector<tuple<int,int,int>>& edges, bool& negCycle) {
    vector<ll> dist(n, INF); dist[src] = 0;
    for (int i = 0; i < n - 1; i++)
        for (auto& [u, v, w] : edges)
            if (dist[u] != INF && dist[u] + w < dist[v]) dist[v] = dist[u] + w;
    negCycle = false;
    for (auto& [u, v, w] : edges)
        if (dist[u] != INF && dist[u] + w < dist[v]) { negCycle = true; break; }
    return dist;
}

// -------- Floyd-Warshall (all-pairs) --------
vector<vector<ll>> floydWarshall(int n, vector<vector<ll>> mat) {
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (mat[i][k] != INF && mat[k][j] != INF && mat[i][k] + mat[k][j] < mat[i][j])
                    mat[i][j] = mat[i][k] + mat[k][j];
    return mat;
}

// -------- Topological Sort (Kahn's BFS) --------
vector<int> topoSort(int n, vector<vector<int>>& adj) {
    vector<int> indeg(n, 0);
    for (int u = 0; u < n; u++) for (int v : adj[u]) indeg[v]++;
    queue<int> q;
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.push(i);
    vector<int> order;
    while (!q.empty()) {
        int u = q.front(); q.pop(); order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) q.push(v);
    }
    return order.size() == (size_t)n ? order : vector<int>{};
}

// -------- Kruskal's MST --------
struct DSU {  // (use earlier dsu.cpp template)
    vector<int> p, r; DSU(int n) : p(n), r(n, 0) { iota(p.begin(), p.end(), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int x, int y) { x = find(x); y = find(y); if (x == y) return false;
        if (r[x] < r[y]) swap(x, y); p[y] = x; if (r[x] == r[y]) r[x]++; return true; }
};

ll kruskal(int n, vector<tuple<int,int,int>>& edges) {
    sort(edges.begin(), edges.end());
    DSU dsu(n);
    ll total = 0;
    for (auto& [w, u, v] : edges)
        if (dsu.unite(u, v)) total += w;
    return total;
}

// -------- Prim's MST --------
ll prim(int n, vector<vector<pair<int,int>>>& adj) {
    vector<bool> inMST(n, false);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    pq.push({0, 0});
    ll total = 0;
    while (!pq.empty()) {
        auto [w, u] = pq.top(); pq.pop();
        if (inMST[u]) continue;
        inMST[u] = true; total += w;
        for (auto [v, ww] : adj[u]) if (!inMST[v]) pq.push({ww, v});
    }
    return total;
}
