n = int(input())

arr = list(map(int, input().split()))

n1 = sum(i for i in arr[:len(arr)//2])
n2 = sum(i for i in arr[len(arr)//2:])

print(abs(n2 - n1))