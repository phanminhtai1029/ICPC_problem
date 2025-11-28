import sys

n_str = sys.stdin.readline()
n = int(n_str)
a = list(map(int, sys.stdin.readline().split()))

zeros = []
positives = []
negatives = []

for i in a:
    if i == 0:
        zeros.append(i)
    elif i > 0:
        positives.append(i)
    else:
        negatives.append(i)

positives.sort()
negatives.sort()

luna_remove = 0
thana_remove = 0

if len(zeros) > 1:
    luna_remove = max(a)
    thana_remove = min(a)

elif len(zeros) == 1:
    if len(negatives) % 2 == 0:
        luna_remove = thana_remove = 0
    else:
        non_zeros = negatives + positives
        luna_remove, thana_remove = non_zeros[-1], non_zeros[0]

else:
    if len(negatives) %2 == 0:
        if positives:
            luna_remove = thana_remove = positives[0]
        else:
            luna_remove = thana_remove = negatives[0]
    else:
        luna_remove, thana_remove = negatives[-1], negatives[-1]

print(luna_remove, thana_remove)