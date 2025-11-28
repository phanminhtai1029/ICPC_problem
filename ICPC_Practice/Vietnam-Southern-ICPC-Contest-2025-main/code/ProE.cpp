#include <iostream>
#include <vector>
#include <numeric> // For std::gcd
#include <stack>
#include <deque>
#include <algorithm>

// Hàm kiểm tra điều kiện xóa trực tiếp
// Trả về true nếu hai số là nguyên tố cùng nhau hoặc một số là bội của số kia
bool can_delete_directly(long long a, long long b)
{
    if (a == 0 || b == 0)
        return false; // Theo đề bài a_i >= 2
    long long common_divisor = std::gcd(a, b);
    return common_divisor == 1 || a % b == 0 || b % a == 0;
}

void solve()
{
    int n;
    std::cin >> n;
    std::vector<long long> a(n);
    for (int i = 0; i < n; ++i)
    {
        std::cin >> a[i];
    }

    long long ops = 0;
    std::stack<long long> s;

    // --- Giai đoạn 1: Xử lý dãy ban đầu bằng stack ---
    for (long long val : a)
    {
        if (s.empty())
        {
            s.push(val);
        }
        else
        {
            if (can_delete_directly(s.top(), val))
            {
                s.pop();
                ops++; // Chi phí 1 cho việc xóa trực tiếp
            }
            else
            {
                s.push(val);
            }
        }
    }

    // --- Giai đoạn 2: Xử lý các phần tử còn lại ---
    // Chuyển từ stack sang deque để xử lý theo thứ tự từ trái sang phải
    std::deque<long long> q;
    while (!s.empty())
    {
        q.push_front(s.top());
        s.pop();
    }

    while (!q.empty())
    {
        if (q.size() == 1)
        {
            // Còn 1 phần tử, bắt buộc phải dùng 2 thao tác:
            // 1. Thêm một số x vào cuối
            // 2. Xóa cặp (a_1+x, a_2)
            ops += 2;
            q.pop_front();
        }
        else
        {
            long long u = q.front();
            q.pop_front();
            long long v = q.front();
            q.pop_front();

            // Trường hợp đặc biệt: Nếu hai phần tử còn lại là (2, 2)
            // chúng có thể xóa trực tiếp vì 2 là bội của 2.
            if (u == 2 && v == 2)
            {
                ops++; // Chi phí 1
            }
            else
            {
                // Trường hợp chung: Phải thực hiện "Xóa bắt buộc"
                // 1. Thao tác 2: biến đổi u và thêm x=2 vào cuối -> chi phí 1
                // 2. Thao tác 1: xóa cặp đã biến đổi -> chi phí 1
                ops += 2;
                q.push_back(2); // Thêm số 2 mới vào cuối dãy
            }
        }
    }

    std::cout << ops << "\n";
}

int main()
{
    // Tăng tốc độ nhập xuất
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    int t;
    std::cin >> t;
    while (t--)
    {
        solve();
    }

    return 0;
}