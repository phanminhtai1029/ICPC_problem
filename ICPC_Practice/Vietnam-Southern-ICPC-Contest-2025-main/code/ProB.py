import sys
from collections import deque, defaultdict

sys.setrecursionlimit(200005)

def fast_input():
    return sys.stdin.readline().strip()

def solve():
    """
    Hàm chính giải quyết bài toán
    """
    try:
        n_str, m_str = fast_input().split()
        n = int(n_str)
        m = int(m_str)
    except (IOError, ValueError):

        return

    adj = defaultdict(list)
    for _ in range(m):
        u, v = map(int, fast_input().split())
        adj[u].append(v)

    q = int(fast_input())

    max_stations = n + q + 5 # +5 đề phòng
    parent = list(range(max_stations))

    def find_set(v):
        """
        Hàm find trong DSU với kỹ thuật nén đường đi (path compression)
        """
        if v == parent[v]:
            return v
        parent[v] = find_set(parent[v])
        return parent[v]

    
    current_n = n

    for _ in range(q):
        query = list(map(int, fast_input().split()))
        op_type = query[0]

        if op_type == 1:
         
            x, d = query[1], query[2]
            current_n += 1
            
            if d == 0:
              
                adj[x].append(current_n)
            else: 
                parent[current_n] = find_set(x)
        
        else: 
            x, y = query[1], query[2]

            if x == y:
                print("Yes")
                continue

            queue = deque([x])
            visited = {x}
            found = False

            while queue:
                u = queue.popleft()

                for v in adj[u]:
                    if v not in visited:
                        if v == y:
                            found = True
                            break
                        visited.add(v)
                        queue.append(v)
                
                if found:
                    break

                p = find_set(u)
                if p != u and p not in visited:
                    if p == y:
                        found = True
                        break
                    visited.add(p)
                    queue.append(p)
            
            if found:
                print("Yes")
            else:
                print("No")


if __name__ == "__main__":
    solve()