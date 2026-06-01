// =============================================================
// COMPETITIVE PROGRAMMING TEMPLATE — C++17
// Author: DSA-Grandmaster-Codex
// Compile: g++ -std=c++17 -O2 -Wall solve.cpp -o solve
// =============================================================

#include <bits/stdc++.h>
using namespace std;

// -------- Type aliases --------
using ll  = long long;
using ull = unsigned long long;
using ld  = long double;
using vi  = vector<int>;
using vll = vector<long long>;
using pii = pair<int, int>;
using pll = pair<long long, long long>;
using vvi = vector<vector<int>>;
using vvll = vector<vector<long long>>;

// -------- Macros --------
#define rep(i, a, b) for (int i = (a); i < (b); ++i)
#define per(i, a, b) for (int i = (b) - 1; i >= (a); --i)
#define all(x) (x).begin(), (x).end()
#define rall(x) (x).rbegin(), (x).rend()
#define sz(x) (int)(x).size()
#define pb push_back
#define eb emplace_back
#define mp make_pair
#define fi first
#define se second

// -------- Constants --------
const int  INF  = 0x3f3f3f3f;
const ll   LINF = 0x3f3f3f3f3f3f3f3fLL;
const ll   MOD  = 1'000'000'007;
const ld   PI   = acosl(-1.0L);
const int  dx[] = {0, 0, 1, -1};
const int  dy[] = {1, -1, 0, 0};

// -------- Debug macros (use with -DLOCAL flag locally) --------
#ifdef LOCAL
template<class T> void _print(const T& x) { cerr << x; }
template<class T, class U> void _print(const pair<T, U>& p) { cerr << "(" << p.fi << "," << p.se << ")"; }
template<class T> void _print(const vector<T>& v) { cerr << "["; for (auto& x : v) { _print(x); cerr << ","; } cerr << "]"; }
#define dbg(x) cerr << #x << "=", _print(x), cerr << endl
#else
#define dbg(x)
#endif

// -------- Modular utilities --------
ll modPow(ll b, ll e, ll m = MOD) {
    ll r = 1 % m; b %= m;
    while (e > 0) {
        if (e & 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}
ll modInv(ll a, ll m = MOD) { return modPow(a, m - 2, m); }

// -------- Custom hash (anti-hack) --------
struct CustomHash {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t SEED = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + SEED);
    }
};

// -------- Solve function --------
void solve() {
    int n;
    cin >> n;
    // ... your code here
}

// -------- Main --------
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    int t = 1;
    // cin >> t;  // uncomment if multiple test cases
    while (t--) solve();
    return 0;
}
