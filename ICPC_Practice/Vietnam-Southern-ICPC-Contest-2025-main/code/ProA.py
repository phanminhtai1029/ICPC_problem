import sys

def solve():
    """
    Hàm giải quyết cho một test case.
    """
    try:
        # Đọc dữ liệu đầu vào
        line1 = sys.stdin.readline()
        if not line1: return
        n, C, D = map(int, line1.split())
        a = list(map(int, sys.stdin.readline().split()))
        b = list(map(int, sys.stdin.readline().split()))
    except (IOError, ValueError):
        return

    # --- Bước 1: Tính các đại lượng cần thiết ---
    
    # Tính mảng hiệu d[i] = a[i] - b[i], đây là đại lượng bất biến
    d = [a[i] - b[i] for i in range(n)]

    # Tìm các giá trị max/min ban đầu
    max_a = max(a)
    max_b = max(b)
    min_d = min(d)
    max_d = max(d)

    # --- Bước 2: Kiểm tra điều kiện tồn tại nghiệm ---
    
    # Nếu chênh lệch lớn nhất của hiệu (max_d - min_d) lớn hơn
    # tổng các khoảng cho phép (C + D), thì không thể tìm ra lời giải.
    if max_d - min_d > C + D:
        print(-1)
        return

    # --- Bước 3: Xác định không gian tìm kiếm và các điểm ứng cử viên ---
    
    # Gọi min_a' và min_b' là min của mảng a và b sau khi biến đổi.
    # Ta cần tìm cặp (min_a', min_b') tối ưu.
    # Các điều kiện ràng buộc tạo thành một vùng đa giác lồi.
    # Chi phí là hàm lồi, nên giá trị tối ưu sẽ nằm ở các đỉnh của vùng này.
    
    # Ràng buộc dưới cho min_a' và min_b'
    x_bound = max_a - C  # min_a' >= max_a - C
    y_bound = max_b - D  # min_b' >= max_b - D

    # Ràng buộc cho hiệu min_a' - min_b'
    # z_lower <= min_a' - min_b' <= z_upper
    z_lower = max_d - C
    z_upper = min_d + D

    # Tìm các đỉnh của vùng khả thi làm ứng cử viên
    candidates = []
    
    # Điểm giao của các đường biên. Chúng ta chỉ quan tâm các điểm
    # nằm trên biên "dưới-trái" của vùng khả thi.
    
    # Ứng cử viên 1: giao của x = x_bound và y = y_bound
    if z_lower <= x_bound - y_bound <= z_upper:
        candidates.append((x_bound, y_bound))
    
    # Ứng cử viên 2 & 3: giao của x = x_bound và các đường chéo
    y2 = x_bound - z_upper
    if y2 >= y_bound:
        candidates.append((x_bound, y2))
        
    y3 = x_bound - z_lower
    if y3 >= y_bound:
        candidates.append((x_bound, y3))

    # Ứng cử viên 4 & 5: giao của y = y_bound và các đường chéo
    x4 = y_bound + z_upper
    if x4 >= x_bound:
        candidates.append((x4, y_bound))
        
    x5 = y_bound + z_lower
    if x5 >= x_bound:
        candidates.append((x5, y_bound))
        
    # --- Bước 4: Tính chi phí và tìm kết quả nhỏ nhất ---
    
    min_ops = float('inf')

    # Nếu không có ứng cử viên nào, có thể có lỗi logic hoặc trường hợp đặc biệt.
    # Tuy nhiên, với logic trên, danh sách ứng cử viên sẽ không rỗng nếu có nghiệm.
    if not candidates:
        print(-1) # Trường hợp dự phòng
        return

    # Duyệt qua các điểm ứng cử viên để tìm chi phí nhỏ nhất
    for x, y in candidates:
        current_ops = 0
        for i in range(n):
            # Số phép toán tại chỉ số i là max(0, min_a' - a[i], min_b' - b[i])
            ops_i = max(0, x - a[i], y - b[i])
            current_ops += ops_i
        min_ops = min(min_ops, current_ops)

    print(min_ops)


def main():
    """
    Hàm chính để đọc số lượng test case và gọi hàm giải.
    """
    try:
        # Đọc số lượng test case
        T_str = sys.stdin.readline()
        if not T_str: return
        T = int(T_str)
        for _ in range(T):
            solve()
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()