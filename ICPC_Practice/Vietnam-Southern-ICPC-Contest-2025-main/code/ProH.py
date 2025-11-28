import sys

def solve():
    """
    Hàm giải quyết bài toán "Removing noisy data".
    """
    try:
        n_str = sys.stdin.readline()
        if not n_str: return
        n = int(n_str)
        a = list(map(int, sys.stdin.readline().split()))
    except (IOError, ValueError):
        return

    zeros = []
    positives = []
    negatives = []
    for x in a:
        if x == 0:
            zeros.append(x)
        elif x > 0:
            positives.append(x)
        else:
            negatives.append(x)
    positives.sort()
    negatives.sort()

    luna_removes = 0
    thana_removes = 0

    if len(zeros) > 1:
        luna_removes = max(a)
        thana_removes = min(a)

    elif len(zeros) == 1:
        if len(negatives) % 2 != 0:
            non_zeros = positives + negatives
            luna_removes = max(non_zeros)
            thana_removes = min(non_zeros)
        else:
            luna_removes = 0
            thana_removes = 0

    else:
        if len(negatives) % 2 != 0:
            luna_removes = negatives[-1] 
            thana_removes = negatives[-1]
        else:
            if positives:
                luna_removes = positives[0] 
                thana_removes = positives[0]
            else:
                luna_removes = negatives[0] 
                thana_removes = negatives[0]

    print(luna_removes, thana_removes)

if __name__ == "__main__":
    solve()