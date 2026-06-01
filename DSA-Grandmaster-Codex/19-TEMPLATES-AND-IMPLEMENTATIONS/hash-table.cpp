// Custom hash for unordered_map (anti-hack against adversarial CF inputs)

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct CustomHash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t FIXED_RANDOM = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + FIXED_RANDOM);
    }
};

// Usage:
// unordered_map<long long, int, CustomHash> safe_map;
// unordered_set<long long, CustomHash> safe_set;

// For pair<int, int> keys, combine into uint64_t:
struct PairHash {
    size_t operator()(const pair<int,int>& p) const {
        return CustomHash{}((uint64_t)p.first * 1000000007ULL + p.second);
    }
};
