#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>

long long max_of_three(long long a, long long b, long long c)
{
    return std::max({a, b, c});
}

void solve()
{
    int n;
    long long C, D;
    std::cin >> n >> C >> D;

    std::vector<long long> a(n), b(n);
    long long max_a = LLONG_MIN;
    long long max_b = LLONG_MIN;

    for (int i = 0; i < n; ++i)
    {
        std::cin >> a[i];
        if (a[i] > max_a)
        {
            max_a = a[i];
        }
    }
    for (int i = 0; i < n; ++i)
    {
        std::cin >> b[i];
        if (b[i] > max_b)
        {
            max_b = b[i];
        }
    }

    std::vector<long long> d(n);
    long long min_d = LLONG_MAX;
    long long max_d = LLONG_MIN;
    for (int i = 0; i < n; ++i)
    {
        d[i] = a[i] - b[i];
        if (d[i] < min_d)
        {
            min_d = d[i];
        }
        if (d[i] > max_d)
        {
            max_d = d[i];
        }
    }

    if (max_d - min_d > C + D)
    {
        std::cout << -1 << std::endl;
        return;
    }

    long long x_bound = max_a - C;
    long long y_bound = max_b - D;
    long long z_lower = max_d - C;
    long long z_upper = min_d + D;

    std::vector<std::pair<long long, long long>> candidates;

    if (z_lower <= x_bound - y_bound && x_bound - y_bound <= z_upper)
    {
        candidates.push_back({x_bound, y_bound});
    }

    long long y2 = x_bound - z_upper;
    if (y2 >= y_bound)
    {
        candidates.push_back({x_bound, y2});
    }
    long long y3 = x_bound - z_lower;
    if (y3 >= y_bound)
    {
        candidates.push_back({x_bound, y3});
    }

    long long x4 = y_bound + z_upper;
    if (x4 >= x_bound)
    {
        candidates.push_back({x4, y_bound});
    }
    long long x5 = y_bound + z_lower;
    if (x5 >= x_bound)
    {
        candidates.push_back({x5, y_bound});
    }

    long long min_ops = LLONG_MAX;

    if (candidates.empty())
    {
        std::cout << -1 << std::endl;
        return;
    }

    for (const auto &p : candidates)
    {
        long long x = p.first;
        long long y = p.second;
        long long current_ops = 0;
        for (int i = 0; i < n; ++i)
        {
            current_ops += max_of_three(0LL, x - a[i], y - b[i]);
        }
        min_ops = std::min(min_ops, current_ops);
    }

    std::cout << min_ops << std::endl;
}

int main()
{
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    int T;
    std::cin >> T;
    while (T--)
    {
        solve();
    }

    return 0;
}