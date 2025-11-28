#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, Q;
    cin >> N >> Q;

    unordered_map<string, int> dict1;
    for (int i = 0; i < N; ++i) {
        string s;
        int c;
        cin >> s >> c;
        dict1[s] = c;
    }

    string T;
    cin >> T;

    vector<pair<int, int>> queries(Q);
    for (int i = 0; i < Q; ++i) {
        int L, R;
        cin >> L >> R;
        queries[i] = {L, R};
    }

    for (auto &[L, R] : queries) {
        string substring = T.substr(L - 1, R - L + 1);
        long long total_value = 0;

        for (auto &[pattern, weight] : dict1) {
            size_t pos = substring.find(pattern);
            while (pos != string::npos) {
                total_value += weight;
                pos = substring.find(pattern, pos + 1);
            }
        }

        cout << total_value << "\n";
    }

    return 0;
}
