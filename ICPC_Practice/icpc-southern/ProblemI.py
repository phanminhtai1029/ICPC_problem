import sys

input = sys.stdin.readline

class AhoCorasick:
    def __init__(self):
        self.trie = [{}]
        self.fail = [0]
        self.output = [[]]

    def add_word(self, word, value):
        node = 0
        for char in word:
            if char not in self.trie[node]:
                self.trie[node][char] = len(self.trie)
                self.trie.append({})
                self.fail.append(0)
                self.output.append([])
            node = self.trie[node][char]
        self.output[node].append((len(word), value))

    def build(self):
        q = []
        head = 0
        
        for char, next_node in self.trie[0].items():
            q.append(next_node)
        
        while head < len(q):
            node = q[head]
            head += 1
            
            for char, next_node in self.trie[node].items():
                f = self.fail[node]
                while f and char not in self.trie[f]:
                    f = self.fail[f]
                self.fail[next_node] = self.trie[f].get(char, 0)
                self.output[next_node].extend(self.output[self.fail[next_node]])
                q.append(next_node)

class FenwickTree:
    def __init__(self, size):
        self.tree = [0] * (size + 1)

    def add(self, index, delta):
        while index < len(self.tree):
            self.tree[index] += delta
            index += index & -index

    def query(self, index):
        s = 0
        while index > 0:
            s += self.tree[index]
            index -= index & -index
        return s

def solve():
    try:
        line = input()
        if not line: return
        N, Q = map(int, line.split())
    except (IOError, ValueError):
        return

    AC = AhoCorasick()
    for _ in range(N):
        s, c = input().split()
        AC.add_word(s, int(c))
    
    T = input().strip()
    text_len = len(T)

    queries_by_R = [[] for _ in range(text_len + 1)]
    for i in range(Q):
        L, R = map(int, input().split())
        queries_by_R[R].append((L, i))

    AC.build()

    occurrences_by_end = [[] for _ in range(text_len + 1)]
    node = 0
    for i, char in enumerate(T, 1):
        while node and char not in AC.trie[node]:
            node = AC.fail[node]
        node = AC.trie[node].get(char, 0)
        
        for length, value in AC.output[node]:
            start_pos = i - length + 1
            occurrences_by_end[i].append((start_pos, value))

    BIT = FenwickTree(text_len)
    answers = [0] * Q

    for i in range(1, text_len + 1):
        for start_pos, value in occurrences_by_end[i]:
            BIT.add(start_pos, value)
        
        for L, query_index in queries_by_R[i]:
            total_sum_up_to_i = BIT.query(i)
            sum_before_L = BIT.query(L - 1)
            answers[query_index] = total_sum_up_to_i - sum_before_L
            
    for ans in answers:
        print(ans)

if __name__ == "__main__":
    solve()