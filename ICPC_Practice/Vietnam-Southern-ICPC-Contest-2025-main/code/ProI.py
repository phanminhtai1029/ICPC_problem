import sys

def solve():
    """
    Hàm giải quyết bài toán "Draw a Polygon".
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return
        n, k = map(int, line.split())
    except (IOError, ValueError):
        return

    # 1. Kiểm tra điều kiện tồn tại
    total_diagonals_in_convex = n * (n - 3) // 2
    min_diagonals = n - 3
    
    if k < min_diagonals:
        print("No")
        return

    print("Yes")

    # Trường hợp đặc biệt: Đa giác lồi có k tối đa
    if k == total_diagonals_in_convex:
        for i in range(n):
            # Các điểm trên một parabol tạo thành đa giác lồi
            print(i, i * i)
        return

    # --- Cấu trúc chung: P1 và một chuỗi P2..Pn ---
    # Số đường chéo cần tạo trong chuỗi P2..Pn
    k_chain = k - min_diagonals

    # 2. Tìm m: số đỉnh của phần chuỗi lồi
    # Chuỗi lồi m đỉnh có (m-1)(m-2)/2 đường chéo
    m = 2
    while (m - 1) * (m - 2) // 2 <= k_chain:
        m += 1
    m -= 1
    
    # Số đường chéo còn lại cần tạo bởi đỉnh chuyển tiếp
    rem_diagonals = k_chain - (m - 2) * (m - 1) // 2
    
    coords = []
    
    # 3. Dựng các đỉnh
    # P1 (sẽ là điểm cuối cùng trong danh sách)
    # Phần chuỗi lồi P2..Pm
    for i in range(1, m):
        coords.append((i, i * i))

    # Đỉnh chuyển tiếp P_{m+1}
    # Điểm cuối của chuỗi lồi: P_m
    last_convex_x, last_convex_y = m - 1, (m - 1)**2
    # Điểm xác định đường thẳng chặn tầm nhìn
    blocking_point_x, blocking_point_y = rem_diagonals, rem_diagonals**2
    
    # Chọn tọa độ x cho điểm chuyển tiếp
    next_x = m
    # Tính tọa độ y tương ứng trên đường thẳng nối P_m và P_{rem+2}
    # y - y1 = slope * (x - x1)
    # slope = (y2-y1)/(x2-x1)
    # Chú ý: P_i có tọa độ (i-1, (i-1)^2), nên P_{rem+2} có x = rem+1
    slope = (last_convex_y - blocking_point_y) / (last_convex_x - blocking_point_x) if last_convex_x != blocking_point_x else 10**18
    next_y = int(slope * (next_x - last_convex_x) + last_convex_y) - 1 # Đặt ngay bên dưới đường thẳng
    
    coords.append((next_x, next_y))

    # Chuỗi zig-zag P_{m+2}..Pn
    base_x, base_y = next_x, next_y
    for i in range(n - 1 - m):
        base_x += 1
        base_y += 1
        coords.append((base_x, base_y))

    # Đỉnh gốc P1, đặt ở xa để đảm bảo tầm nhìn
    coords.append((-30000, 30000))
    
    # In kết quả
    for x, y in coords:
        print(x, y)

if __name__ == "__main__":
    solve()