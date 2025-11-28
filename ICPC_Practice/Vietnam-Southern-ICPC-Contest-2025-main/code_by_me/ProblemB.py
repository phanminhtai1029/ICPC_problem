import sys
from collections import defaultdict, deque

n, m = list(map(int, sys.stdin.readline().split()))
adj = defaultdict(list)

for _ in range(m):
    u, v = list(map(int, sys.stdin.readline().split()))
    adj[u].append(v)

q = int(sys.stdin.readline())

max_station = n + q + 5
parent = list(range(max_station))

def find_set(v):
    if v == parent[v]:
        return v
    parent[v] = find_set(parent[v])
    return parent[v]

current_station = n

for _ in range(q):
    query = list(map(int, sys.stdin.readline().split()))

    if query[0] == 1:
        current_station += 1
        if query[2] == 0:
            adj[query[1]].append(current_station)
        else:
            parent[current_station] = find_set(query[1])

    else:
        if query[1] == query[2]:
            print("Yes")
            continue
        queue = deque([query[1]])
        visited = {query[1]}
        found = False
        while queue:
            node = queue.popleft()
            for neighbor in adj[node]:
                if neighbor not in visited:
                    if neighbor == query[2]:
                        found = True
                        break
                    queue.append(neighbor)
                    visited.add(neighbor)
            
            if found == True:
                break

            node_parent = find_set(node)
            if node_parent != node and node_parent not in visited:
                if node_parent == query[2]:
                    found = True
                    break
                visited.add(node_parent)
                queue.append(node_parent)

        if found == True:
            print("Yes")
        else:
            print("No")