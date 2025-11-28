import sys

# Tăng giới hạn đệ quy cho cây
sys.setrecursionlimit(2 * 10**5)

# Đọc input nhanh hơn
def fast_input():
    return sys.stdin.readline().strip()

# Lớp Node cho Cây Phân Đoạn Bền Vững
class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.count = 0
        self.power_sum = 0

# Cấu trúc Cây Phân Đoạn Bền Vững
class PersistentSegmentTree:
    def __init__(self, size):
        self.size = size
        self.roots = [self._build(0, size - 1)]

    def _build(self, l, r):
        # Hàm nội bộ để xây dựng cây rỗng ban đầu
        node = Node()
        if l == r:
            return node
        mid = (l + r) // 2
        node.left = self._build(l, mid)
        node.right = self._build(mid + 1, r)
        return node

    def update(self, prev_node, l, r, idx, val):
        # Tạo một phiên bản cây mới dựa trên phiên bản cũ (prev_node)
        new_node = Node()
        if l == r:
            new_node.count = prev_node.count + val
            new_node.power_sum = new_node.count * (power_map_rev[idx])
            return new_node

        mid = (l + r) // 2
        new_node.left = prev_node.left
        new_node.right = prev_node.right

        if idx <= mid:
            new_node.left = self.update(prev_node.left, l, mid, idx, val)
        else:
            new_node.right = self.update(prev_node.right, mid + 1, r, idx, val)
        
        new_node.count = new_node.left.count + new_node.right.count
        new_node.power_sum = new_node.left.power_sum + new_node.right.power_sum
        return new_node

    def query(self, node, l, r, k):
        # Tìm tổng sức mạnh của k quái vật yếu nhất
        if l == r:
            # Nếu cần k con mà chỉ có node.count con, lấy hết
            # và nhân với sức mạnh của nó
            return min(k, node.count) * (power_map_rev[l])
        
        if k == 0:
            return 0
            
        mid = (l + r) // 2
        left_count = node.left.count

        if k <= left_count:
            # Nếu k nhỏ hơn số quái vật ở nhánh trái, chỉ cần tìm ở nhánh trái
            return self.query(node.left, l, mid, k)
        else:
            # Ngược lại, lấy toàn bộ nhánh trái và tìm (k - left_count) con nữa ở nhánh phải
            return node.left.power_sum + self.query(node.right, mid + 1, r, k - left_count)

# --- Chương trình chính ---

# Đọc n, m
n, m = map(int, fast_input().split())

monsters = []
moves = []
all_powers = set()
max_time = 0

# Đọc thông tin quái vật
for _ in range(n):
    l, r, p = map(int, fast_input().split())
    monsters.append((l, r, p))
    all_powers.add(p)
    max_time = max(max_time, r)

# Đọc thông tin các lượt đi
for _ in range(m):
    t, d, a, f = map(int, fast_input().split())
    moves.append((t, d, a, f))
    max_time = max(max_time, t)

# Rời rạc hóa sức mạnh
sorted_powers = sorted(list(all_powers))
power_map = {p: i for i, p in enumerate(sorted_powers)}
power_map_rev = {i: p for i, p in enumerate(sorted_powers)}
power_cnt = len(all_powers)

# Tạo các sự kiện
events = [[] for _ in range(max_time + 2)]
for l, r, p in monsters:
    p_idx = power_map[p]
    events[l].append((p_idx, 1))
    if r + 1 <= max_time + 1:
        events[r + 1].append((p_idx, -1))

# Xây dựng PST
pst = PersistentSegmentTree(power_cnt)
for t in range(1, max_time + 1):
    current_root = pst.roots[-1]
    for p_idx, val in events[t]:
        current_root = pst.update(current_root, 0, power_cnt - 1, p_idx, val)
    pst.roots.append(current_root)

# Xử lý các lượt đi
prev_power = 1
for t_j, d, a, f in moves:
    e_j = 1 + (d * prev_power + a) % f
    
    root_at_tj = pst.roots[t_j]
    
    total_monsters_at_tj = root_at_tj.count
    if total_monsters_at_tj == 0:
        absorbed_power = 0
    else:
        # Hấp thụ min(e_j, tổng số quái) con
        k = min(e_j, total_monsters_at_tj)
        absorbed_power = pst.query(root_at_tj, 0, power_cnt - 1, k)
        
    print(absorbed_power)
    prev_power = absorbed_power