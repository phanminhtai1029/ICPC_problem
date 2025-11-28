import sys
import random

n, k = list(map(int, sys.stdin.readline().split()))

MOD = 10**9 + 7

def power(base, exp):
    res = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return res

def modInverse(n):
    return power(n, MOD - 2)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def miller_rabin(n, k=10):
    if n < 2: return False
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True