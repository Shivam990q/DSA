// =============================================================
// NUMBER THEORY — REFERENCE IMPLEMENTATIONS
// =============================================================

#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 1'000'000'007LL;

// -------- GCD / LCM --------
ll gcd(ll a, ll b) { return b == 0 ? a : gcd(b, a % b); }
ll lcm(ll a, ll b) { return a / gcd(a, b) * b; }

// -------- Extended Euclidean: returns gcd; sets x, y s.t. a*x + b*y = gcd --------
ll extGcd(ll a, ll b, ll& x, ll& y) {
    if (b == 0) { x = 1; y = 0; return a; }
    ll x1, y1, d = extGcd(b, a % b, x1, y1);
    x = y1; y = x1 - (a / b) * y1;
    return d;
}

// -------- Fast modular exponentiation --------
ll modPow(ll b, ll e, ll m = MOD) {
    ll r = 1 % m; b %= m;
    while (e > 0) {
        if (e & 1) r = r * b % m;
        b = b * b % m;
        e >>= 1;
    }
    return r;
}

// -------- Modular inverse (m prime via Fermat) --------
ll modInv(ll a, ll m = MOD) { return modPow(a, m - 2, m); }

// -------- Sieve of Eratosthenes --------
vector<bool> sieve(int n) {
    vector<bool> is(n + 1, true);
    is[0] = is[1] = false;
    for (int i = 2; (ll)i * i <= n; i++)
        if (is[i])
            for (int j = i * i; j <= n; j += i) is[j] = false;
    return is;
}

// -------- Linear sieve with smallest prime factor --------
pair<vector<int>, vector<int>> linearSieve(int n) {
    vector<int> spf(n + 1, 0);
    vector<int> primes;
    for (int i = 2; i <= n; i++) {
        if (spf[i] == 0) { spf[i] = i; primes.push_back(i); }
        for (int p : primes) {
            if (p > spf[i] || (ll)i * p > n) break;
            spf[i * p] = p;
        }
    }
    return {spf, primes};
}

// -------- Euler's totient (single n) --------
ll phi(ll n) {
    ll result = n;
    for (ll p = 2; p * p <= n; p++)
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            result -= result / p;
        }
    if (n > 1) result -= result / n;
    return result;
}

// -------- Miller-Rabin primality (deterministic for 64-bit) --------
bool millerRabin(ll n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0) return false;
    ll d = n - 1; int r = 0;
    while (d % 2 == 0) { d /= 2; r++; }
    auto check = [&](ll a) -> bool {
        if (a % n == 0) return true;
        ll x = modPow(a, d, n);
        if (x == 1 || x == n - 1) return true;
        for (int i = 0; i < r - 1; i++) {
            x = (__int128)x * x % n;
            if (x == n - 1) return true;
        }
        return false;
    };
    for (ll a : {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37})
        if (!check(a)) return false;
    return true;
}

// -------- Combinatorics precomputation (nCr mod MOD) --------
struct Combinatorics {
    int n;
    vector<ll> fact, inv_fact;
    Combinatorics(int n) : n(n), fact(n + 1, 1), inv_fact(n + 1, 1) {
        for (int i = 1; i <= n; i++) fact[i] = fact[i-1] * i % MOD;
        inv_fact[n] = modInv(fact[n]);
        for (int i = n - 1; i >= 0; i--) inv_fact[i] = inv_fact[i+1] * (i+1) % MOD;
    }
    ll C(int n_, int r) {
        if (r < 0 || r > n_) return 0;
        return fact[n_] * inv_fact[r] % MOD * inv_fact[n_ - r] % MOD;
    }
};
