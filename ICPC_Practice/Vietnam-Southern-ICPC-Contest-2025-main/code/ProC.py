import sys
from collections import deque

# Tăng giới hạn đệ quy nếu cần cho Aho-Corasick
sys.setrecursionlimit(2 * 10**5)

# Cài đặt cây Fenwick (Binary Indexed Tree)
class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def add(self, i, delta):
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

# Cài đặt Aho-Corasick
class AhoCorasick:
    def __init__(self):
        # Mỗi node trong trie là một dictionary
        self.trie = [{'children': {}, 'fail': 0, 'output': []}]
        self.nodes_count = 1

    def add_string(self, s, weight):
        node_idx = 0
        for char in s:
            if char not in self.trie[node_idx]['children']:
                self.trie[node_idx]['children'][char] = self.nodes_count
                self.trie.append({'children': {}, 'fail': 0, 'output': []})
                self.nodes_count += 1
            node_idx = self.trie[node_idx]['children'][char]
        self.trie[node_idx]['output'].append((len(s), weight))

    def build_failure_links(self):
        queue = deque()
        for char, next_node_idx in self.trie[0]['children'].items():
            queue.append(next_node_idx)

        while queue:
            current_idx = queue.popleft()
            for char, next_idx in self.trie[current_idx]['children'].items():
                fail_idx = self.trie[current_idx]['fail']
                while char not in self.trie[fail_idx]['children'] and fail_idx != 0:
                    fail_idx = self.trie[fail_idx]['fail']
                
                if char in self.trie[fail_idx]['children']:
                    self.trie[next_idx]['fail'] = self.trie[fail_idx]['children'][char]
                else:
                    self.trie[next_idx]['fail'] = 0
                
                # Nối output từ failure link
                fail_output_idx = self.trie[next_idx]['fail']
                self.trie[next_idx]['output'].extend(self.trie[fail_output_idx]['output'])
                queue.append(next_idx)

    def find_all_occurrences(self, text):
        text_len = len(text)
        occurrences_by_end = [[] for _ in range(text_len + 1)]
        current_node_idx = 0

        for i, char in enumerate(text):
            while char not in self.trie[current_node_idx]['children'] and current_node_idx != 0:
                current_node_idx = self.trie[current_node_idx]['fail']
            
            if char in self.trie[current_node_idx]['children']:
                current_node_idx = self.trie[current_node_idx]['children'][char]
            else:
                current_node_idx = 0

            # Thu thập tất cả các kết quả tại node hiện tại
            if self.trie[current_node_idx]['output']:
                end_pos = i + 1  # 1-indexed
                for length, weight in self.trie[current_node_idx]['output']:
                    start_pos = end_pos - length + 1
                    occurrences_by_end[end_pos].append((start_pos, weight))
        
        return occurrences_by_end

def solve():
    """
    Hàm chính giải quyết bài toán
    """
    # Đọc input nhanh hơn
    input = sys.stdin.readline

    try:
        n_str, q_str = input().split()
        n = int(n_str)
        q = int(q_str)
    except (IOError, ValueError):
        return

    ac = AhoCorasick()
    for _ in range(n):
        s, c = input().split()
        ac.add_string(s, int(c))
    
    ac.build_failure_links()

    text = input().strip()
    text_len = len(text)

    # 1. Tìm tất cả các lần xuất hiện
    occurrences_by_end = ac.find_all_occurrences(text)

    # 2. Nhóm các truy vấn theo R
    queries_by_r = [[] for _ in range(text_len + 1)]
    for i in range(q):
        l, r = map(int, input().split())
        queries_by_r[r].append((l, i))

    # 3. Xử lý offline với cây Fenwick
    bit = FenwickTree(text_len + 1)
    results = [0] * q

    for r in range(1, text_len + 1):
        # Cập nhật BIT với các chuỗi kết thúc tại r
        if occurrences_by_end[r]:
            for start, weight in occurrences_by_end[r]:
                bit.add(start, weight)
        
        # Trả lời các truy vấn có R = r
        if queries_by_r[r]:
            for l, query_idx in queries_by_r[r]:
                ans = bit.query(r) - bit.query(l - 1)
                results[query_idx] = ans
    
    # In kết quả theo thứ tự ban đầu
    for res in results:
        print(res)

if __name__ == "__main__":
    solve()