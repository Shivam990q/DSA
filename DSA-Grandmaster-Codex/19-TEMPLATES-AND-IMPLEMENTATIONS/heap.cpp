// Indexed Priority Queue (with decrease-key support)
// Useful for Dijkstra with decrease-key, or when you need to update priorities

template<typename T>
class IndexedPQ {
    int n;
    vector<int> pq;       // pq[i] = item at heap position i
    vector<int> qp;       // qp[item] = position in pq, or -1
    vector<T> keys;
    
    void up(int i) {
        while (i > 1 && keys[pq[i/2]] > keys[pq[i]]) {
            swap(pq[i], pq[i/2]);
            qp[pq[i]] = i; qp[pq[i/2]] = i/2;
            i /= 2;
        }
    }
    
    void down(int i) {
        while (2*i <= sz) {
            int j = 2*i;
            if (j < sz && keys[pq[j]] > keys[pq[j+1]]) j++;
            if (keys[pq[i]] <= keys[pq[j]]) break;
            swap(pq[i], pq[j]);
            qp[pq[i]] = i; qp[pq[j]] = j;
            i = j;
        }
    }
    
public:
    int sz;
    IndexedPQ(int n_) : n(n_), pq(n_+1), qp(n_, -1), keys(n_), sz(0) {}
    
    bool contains(int item) { return qp[item] != -1; }
    
    void insert(int item, T key) {
        sz++;
        pq[sz] = item;
        qp[item] = sz;
        keys[item] = key;
        up(sz);
    }
    
    int extractMin() {
        int item = pq[1];
        swap(pq[1], pq[sz]);
        qp[pq[1]] = 1; qp[item] = -1;
        sz--;
        down(1);
        return item;
    }
    
    void decreaseKey(int item, T newKey) {
        keys[item] = newKey;
        up(qp[item]);
    }
    
    T keyOf(int item) { return keys[item]; }
    bool empty() { return sz == 0; }
};
