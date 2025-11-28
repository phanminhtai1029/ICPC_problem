#include <iostream>
#include <vector>
#include <algorithm>
#include <map>

void fast_io()
{
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);
}

struct Node
{
    int left = 0, right = 0;
    long long count = 0;
    long long power_sum = 0;
};

const int MAX_NODES = 4500000;
Node tree[MAX_NODES];
int node_cnt = 0;

std::vector<int> roots;
std::map<int, int> power_map;
std::vector<int> power_map_rev;

int build(int l, int r)
{
    int curr_node_idx = ++node_cnt;
    if (l == r)
        return curr_node_idx;
    int mid = l + (r - l) / 2;
    tree[curr_node_idx].left = build(l, mid);
    tree[curr_node_idx].right = build(mid + 1, r);
    return curr_node_idx;
}

int update(int prev_node_idx, int l, int r, int target_idx, int val)
{
    int new_node_idx = ++node_cnt;
    tree[new_node_idx] = tree[prev_node_idx];

    if (l == r)
    {
        tree[new_node_idx].count += val;
        tree[new_node_idx].power_sum = tree[new_node_idx].count * power_map_rev[target_idx];
        return new_node_idx;
    }

    int mid = l + (r - l) / 2;
    if (target_idx <= mid)
    {
        tree[new_node_idx].left = update(tree[prev_node_idx].left, l, mid, target_idx, val);
    }
    else
    {
        tree[new_node_idx].right = update(tree[prev_node_idx].right, mid + 1, r, target_idx, val);
    }

    tree[new_node_idx].count = tree[tree[new_node_idx].left].count + tree[tree[new_node_idx].right].count;
    tree[new_node_idx].power_sum = tree[tree[new_node_idx].left].power_sum + tree[tree[new_node_idx].right].power_sum;
    return new_node_idx;
}

long long query(int node_idx, int l, int r, int k)
{
    if (k <= 0)
        return 0;
    if (l == r)
    {
        return std::min((long long)k, tree[node_idx].count) * power_map_rev[l];
    }

    int mid = l + (r - l) / 2;
    long long left_count = tree[tree[node_idx].left].count;

    if (k <= left_count)
    {
        return query(tree[node_idx].left, l, mid, k);
    }
    else
    {
        return tree[tree[node_idx].left].power_sum + query(tree[node_idx].right, mid + 1, r, k - left_count);
    }
}

struct Monster
{
    int l, r, p;
};

struct Move
{
    int t, d, a, f;
};

struct Event
{
    int p_idx, val;
};

int main()
{
    fast_io();

    int n, m;
    std::cin >> n >> m;

    std::vector<Monster> monsters(n);
    std::vector<int> all_powers;
    int max_time = 0;

    for (int i = 0; i < n; ++i)
    {
        std::cin >> monsters[i].l >> monsters[i].r >> monsters[i].p;
        all_powers.push_back(monsters[i].p);
        max_time = std::max(max_time, monsters[i].r);
    }

    std::vector<Move> moves(m);
    for (int i = 0; i < m; ++i)
    {
        std::cin >> moves[i].t >> moves[i].d >> moves[i].a >> moves[i].f;
        max_time = std::max(max_time, moves[i].t);
    }

    std::sort(all_powers.begin(), all_powers.end());
    all_powers.erase(std::unique(all_powers.begin(), all_powers.end()), all_powers.end());

    power_map_rev.push_back(0);
    for (int p : all_powers)
    {
        power_map[p] = power_map_rev.size();
        power_map_rev.push_back(p);
    }
    int power_cnt = power_map_rev.size() - 1;
    if (power_cnt == 0)
        power_cnt = 1;

    std::vector<std::vector<Event>> events(max_time + 2);
    for (const auto &mon : monsters)
    {
        int p_idx = power_map[mon.p];
        events[mon.l].push_back({p_idx, 1});
        if (mon.r + 1 <= max_time + 1)
        {
            events[mon.r + 1].push_back({p_idx, -1});
        }
    }

    roots.resize(max_time + 1);
    roots[0] = build(1, power_cnt);
    for (int t = 1; t <= max_time; ++t)
    {
        roots[t] = roots[t - 1];
        for (const auto &ev : events[t])
        {
            roots[t] = update(roots[t], 1, power_cnt, ev.p_idx, ev.val);
        }
    }

    long long prev_power = 1;
    for (const auto &move : moves)
    {
        long long e_j = 1 + (1LL * move.d * prev_power + move.a) % move.f;

        int root_at_tj = roots[move.t];
        long long total_monsters_at_tj = tree[root_at_tj].count;
        long long absorbed_power = 0;

        if (total_monsters_at_tj > 0)
        {
            long long k = std::min(e_j, total_monsters_at_tj);
            absorbed_power = query(root_at_tj, 1, power_cnt, k);
        }

        std::cout << absorbed_power << "\n";
        prev_power = absorbed_power;
    }

    return 0;
}