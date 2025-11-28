n = int(input())
a = list(map(int, input().split()))

pos_nums = []
neg_nums = []
zero_count = 0

for x in a:
    if x > 0:
        pos_nums.append(x)
    elif x < 0:
        neg_nums.append(x)
    else:
        zero_count += 1
        
candidates_to_remove = []

if zero_count > 0:
    if len(neg_nums) % 2 != 0:
        candidates_to_remove = a
    else:
        candidates_to_remove.append(0)
        
else:
    if len(neg_nums) % 2 != 0:
        candidates_to_remove.append(max(neg_nums))
    else:
        if pos_nums:
            candidates_to_remove.append(min(pos_nums))
        else:
            candidates_to_remove.append(min(neg_nums))

luna_removes = max(candidates_to_remove)
thana_removes = min(candidates_to_remove)

print(luna_removes, thana_removes)