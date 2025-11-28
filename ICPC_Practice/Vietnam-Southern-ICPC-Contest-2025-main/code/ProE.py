# delete_sequence_greedy.py
# Greedy simulator for "Delete sequence" problem (practical solver)

from collections import deque
import math
import sys

def is_good(x, y):
    return math.gcd(x, y) == 1 or x % y == 0 or y % x == 0

def find_small_x_make_good(a1, a2, max_try=200):
    """
    Try small x from 2..max_try to make (a1 + x) and a2 'good'.
    Returns x if found, otherwise returns a larger constructive x:
    choose x = ((a1//a2) + 1) * a2 - a1  (this makes a1+x a multiple of a2).
    Ensure returned x >= 2.
    """
    for x in range(2, max_try + 1):
        if is_good(a1 + x, a2):
            return x
    # fallback: make a1+x be a multiple of a2
    t = a1 // a2 + 1
    x = t * a2 - a1
    if x <= 1:
        # pick next multiple
        x += a2
    if x <= 1:
        x = 2
    return x

def solve_one_case(arr):
    dq = deque(arr)
    ops = 0
    # safety limit to avoid infinite loops on pathological inputs
    safety = 10**7
    steps = 0
    while dq:
        steps += 1
        if steps > safety:
            raise RuntimeError("Exceeded safety step limit")
        if len(dq) == 1:
            # single element: must do op2 then op1 (2 ops)
            a = dq.popleft()
            # choose x to pair with new a: try small x making (a+x, x) good
            x = find_small_x_make_good(a, 2, max_try=200)  # second param dummy; but (a+x, x) will be checked next iteration
            # apply op2
            a += x
            dq.append(x)
            ops += 1
            # now a and the next element (which is x we just appended) will be handled next loop
            # loop continues
            continue

        a1 = dq[0]
        a2 = dq[1]
        if is_good(a1, a2):
            # operation 1: delete first two
            dq.popleft()
            dq.popleft()
            ops += 1
        else:
            # operation 2: choose small x so (a1+x, a2) is good
            x = find_small_x_make_good(a1, a2, max_try=200)
            # apply op2: a1 += x, append x
            dq[0] = a1 + x
            dq.append(x)
            ops += 1
            # next cycle we will delete a1 (modified) and a2 with op1
    return ops

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    t = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        arr = [int(next(it)) for __ in range(n)]
        res = solve_one_case(arr)
        out_lines.append(str(res))
    print("\n".join(out_lines))

if __name__ == "__main__":
    main()
