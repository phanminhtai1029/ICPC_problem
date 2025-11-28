import sys
import random

def fast_input():
    return sys.stdin.readline().strip()

MOD = 10**9 + 7

def power(base, exp):
    """Tính (base^exp) % MOD một cách hiệu quả."""
    res = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return res

def modInverse(n):
    """Tính nghịch đảo modulo của n."""
    return power(n, MOD - 2)

def gcd(a, b):
    """Tính ước chung lớn nhất."""
    while b:
        a, b = b, a % b
    return a

def miller_rabin(n, k=10):
    """Kiểm tra số nguyên tố Miller-Rabin."""
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

def pollards_rho(n):
    """Thuật toán Pollard's Rho để tìm một ước số không tầm thường."""
    if n % 2 == 0: return 2
    x = random.randint(1, n-2)
    y = x
    c = random.randint(1, n-1)
    d = 1
    
    f = lambda val: (pow(val, 2, n) + c) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
    
    if d == n:
        return pollards_rho(n)
    return d

def factorize(n):
    """Phân tích n ra thừa số nguyên tố."""
    factors = {}
    
    def get_factors(num):
        if num == 1:
            return
        if miller_rabin(num):
            factors[num] = factors.get(num, 0) + 1
            return
        
        factor = pollards_rho(num)
        get_factors(factor)
        get_factors(num // factor)

    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
    
    if n > 1:
        get_factors(n)
    return factors

def solve_for_prime_power(p, a, k):
    """Tính E(p^a, k) bằng Quy hoạch động."""
    dp = [[0] * (k + 1) for _ in range(a + 1)]
    inverses = [modInverse(i) for i in range(1, a + 2)]

    current_p_power = 1
    for i in range(a + 1):
        dp[i][0] = current_p_power
        current_p_power = (current_p_power * p) % MOD

    for j in range(1, k + 1):  
        prefix_sum = 0
        for i in range(a + 1):  
            prefix_sum = (prefix_sum + dp[i][j - 1]) % MOD
            dp[i][j] = (prefix_sum * inverses[i]) % MOD
    
    return dp[a][k]

def solve():
    """Hàm chính để đọc input và chạy giải thuật."""
    try:
        n, k = map(int, fast_input().split())
    except (IOError, ValueError):
        return

    factors = factorize(n)

    total_expected_value = 1
    for p, a in factors.items():
        res_for_p = solve_for_prime_power(p, a, k)
        total_expected_value = (total_expected_value * res_for_p) % MOD
    
    print(total_expected_value)

if __name__ == "__main__":
    solve()