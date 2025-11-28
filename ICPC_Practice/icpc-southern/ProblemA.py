import math

def solve():
    """
    Hàm giải quyết cho mỗi test case.
    """
    try:
        # Đọc dữ liệu đầu vào
        n_str, c_str, d_str = input().split()
        n = int(n_str)
        C = int(c_str)
        D = int(d_str)
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
    except (IOError, ValueError):
        return

    # *** PHẦN SỬA LỖI ***
    # Tính toán khoảng tìm kiếm cho Z dựa trên hiệu b[i] - a[i]
    b_minus_a = [b[i] - a[i] for i in range(n)]
    
    min_b_minus_a = float('inf')
    max_b_minus_a = -float('inf')
    for val in b_minus_a:
        if val < min_b_minus_a:
            min_b_minus_a = val
        if val > max_b_minus_a:
            max_b_minus_a = val

    lower_z = max_b_minus_a - D  # Sửa từ C thành D
    upper_z = min_b_minus_a + C  # Sửa từ D thành C
    
    # Oops, kiểm tra lại đại số
    # Z >= b_i - a_i - C => Z >= max(b-a) - C
    # Z <= b_i - a_i + D => Z <= min(b-a) + D
    # Vậy nên phải là:
    lower_z = max_b_minus_a - C
    upper_z = min_b_minus_a + D
    
    # Tìm các giá trị max của a và b để tính X_lower_bound sau này
    max_a = max(a)
    max_b = max(b)

    # Nếu khoảng tìm kiếm không hợp lệ, không có lời giải
    if lower_z > upper_z:
        print(-1)
        return

    def calculate_cost(z):
        """
        Tính chi phí tối thiểu cho một giá trị Z = X - Y cố định.
        Hàm này không thay đổi so với logic ban đầu.
        """
        # X phải đủ lớn để tất cả các k_i đều không âm.
        # X_lower_bound là giá trị X nhỏ nhất có thể.
        x_lower_bound = max(max_a - C, max_b + z - D)
        
        total_cost = 0
        for i in range(n):
            # Tính số phép toán cần thiết cho cặp (a_i, b_i)
            # k_i = max(0, X - a_i, Y - b_i) = max(0, X - min(a_i, b_i + z))
            m_i = min(a[i], b[i] + z)
            cost_i = max(0, x_lower_bound - m_i)
            total_cost += cost_i
            
        return total_cost

    # Sử dụng tìm kiếm tam phân để tìm Z tối ưu trong khoảng [lower_z, upper_z]
    l, r = lower_z, upper_z
    
    # Lặp 100 lần là đủ để hội tụ cho các ràng buộc của bài toán
    for _ in range(100):
        if r - l < 3:
            break
        m1 = l + (r - l) // 3
        m2 = r - (r - l) // 3
        
        cost1 = calculate_cost(m1)
        cost2 = calculate_cost(m2)
        
        if cost1 < cost2:
            r = m2
        else:
            l = m1

    # Vì Z là số nguyên, ta cần kiểm tra các giá trị trong khoảng hẹp cuối cùng
    min_cost = float('inf')
    for z_final in range(int(l), int(r) + 2):
        min_cost = min(min_cost, calculate_cost(z_final))

    print(min_cost)


def main():
    """
    Hàm main để xử lý nhiều test cases.
    """
    try:
        num_test_cases_str = input()
        if not num_test_cases_str:
            return
        num_test_cases = int(num_test_cases_str.strip())
        for _ in range(num_test_cases):
            solve()
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()