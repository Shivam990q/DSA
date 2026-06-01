// =============================================================
// STRING ALGORITHMS — REFERENCE IMPLEMENTATIONS
// =============================================================
// Includes: KMP, Z-algorithm, polynomial hashing, Manacher

#include <bits/stdc++.h>
using namespace std;

// -------- KMP failure function --------
vector<int> computeFail(const string& p) {
    int m = p.size();
    vector<int> fail(m, 0);
    for (int i = 1, j = 0; i < m; ) {
        if (p[i] == p[j]) fail[i++] = ++j;
        else if (j > 0) j = fail[j-1];
        else fail[i++] = 0;
    }
    return fail;
}

vector<int> kmpSearch(const string& t, const string& p) {
    int n = t.size(), m = p.size();
    auto fail = computeFail(p);
    vector<int> matches;
    for (int i = 0, j = 0; i < n; ) {
        if (t[i] == p[j]) {
            i++; j++;
            if (j == m) { matches.push_back(i - m); j = fail[j-1]; }
        } else if (j > 0) j = fail[j-1];
        else i++;
    }
    return matches;
}

// -------- Z-function --------
vector<int> zFunction(const string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) { l = i; r = i + z[i]; }
    }
    return z;
}

// -------- Polynomial hash --------
struct StringHash {
    static const long long B = 131, P = 1'000'000'007LL;
    vector<long long> h, pw;
    StringHash(const string& s) {
        int n = s.size();
        h.assign(n + 1, 0); pw.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            h[i+1] = (h[i] * B + s[i]) % P;
            pw[i+1] = (pw[i] * B) % P;
        }
    }
    long long get(int l, int r) {  // s[l..r] (inclusive, 0-indexed)
        return (h[r+1] - h[l] * pw[r - l + 1] % P + P * P) % P;
    }
};

// -------- Manacher's (longest palindromic substring) --------
string longestPalindrome(const string& s) {
    string t = "^";
    for (char c : s) { t += '#'; t += c; }
    t += "#$";
    int n = t.size();
    vector<int> p(n, 0);
    int c = 0, r = 0;
    for (int i = 1; i < n - 1; i++) {
        int mirror = 2 * c - i;
        if (i < r) p[i] = min(r - i, p[mirror]);
        while (t[i + (1 + p[i])] == t[i - (1 + p[i])]) p[i]++;
        if (i + p[i] > r) { c = i; r = i + p[i]; }
    }
    int max_len = 0, center = 0;
    for (int i = 1; i < n - 1; i++)
        if (p[i] > max_len) { max_len = p[i]; center = i; }
    return s.substr((center - max_len) / 2, max_len);
}
