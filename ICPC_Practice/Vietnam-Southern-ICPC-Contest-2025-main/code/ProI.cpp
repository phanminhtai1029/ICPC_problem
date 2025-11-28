#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

// Định nghĩa một điểm
struct Point {
    long long x, y;
};

int main() {
    // Tăng tốc độ nhập xuất
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(NULL);

    long long n, k;
    std::cin >> n >> k;

    // Tính số đường chéo tối thiểu và tối đa
    long long k_min = n - 3;
    long long k_max = n * (n - 3) / 2;

    // Trường hợp k nằm ngoài khoảng cho phép
    if (k < k_min) {
        std::cout << "No\n";
        return 0;
    }

    // Tìm số đỉnh bên trong 'd'
    int d = -1;
    for (int current_d = 0; current_d <= n - 3; ++current_d) {
        if (k_max - (long long)current_d * (current_d + 1) / 2 == k) {
            d = current_d;
            break;
        }
    }

    // Nếu không tìm thấy giá trị 'd' phù hợp
    if (d == -1) {
        std::cout << "No\n";
        return 0;
    }

    std::cout << "Yes\n";

    // Số đỉnh trên bao lồi
    int m = n - d;
    std::vector<Point> polygon_vertices;

    // 1. Tạo m-1 đỉnh của bao lồi theo hình ziczac để tránh thẳng hàng
    // P_i = (2*i, i % 2)
    long long last_convex_x = 0;
    long long last_convex_y = 0;
    for (int i = 0; i < m - 1; ++i) {
        last_convex_x = 2LL * i;
        last_convex_y = i % 2;
        polygon_vertices.push_back({last_convex_x, last_convex_y});
    }

    // 2. Tạo 'd' đỉnh bên trong, tạo thành một túi lõm
    // Chúng ta gắn chúng vào sau đỉnh P_{m-2}
    std::vector<Point> internal_vertices;
    for (int i = 0; i < d; ++i) {
        long long new_x = last_convex_x + 2LL * (i + 1);
        long long new_y = last_convex_y - 2LL - (i % 2); // Đặt Y thấp hơn hẳn để tạo túi lõm rõ ràng
        internal_vertices.push_back({new_x, new_y});
    }
    
    // Đảo ngược thứ tự các đỉnh bên trong để thêm vào đa giác
    std::reverse(internal_vertices.begin(), internal_vertices.end());
    for(const auto& p : internal_vertices) {
        polygon_vertices.push_back(p);
    }


    // 3. Đỉnh cuối cùng của bao lồi
    // Đặt ở vị trí xa để "khép" đa giác và đảm bảo tính lồi tổng thể (trừ túi lõm)
    polygon_vertices.push_back({-1, 3LL * n});

    // In ra các đỉnh theo đúng thứ tự
    for (const auto& p : polygon_vertices) {
        std::cout << p.x << " " << p.y << "\n";
    }

    return 0;
}