"""
aznt - From A to Z Number Theory
Author: Adrian Zapała, Msc, adrian.zapala@outlook.com, All rights reserved
Licence: MIT
"""


def is_prime_naive1(n):
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


def is_prime_naive2(n):
    if n <= 1:
        return False
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True


def is_prime_sqrt(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def is_prime_sqrt_odd(n):
    if n == 2:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def eratosthenes_sieve(n):
    nums = [True if i >= 2 else False for i in range(n + 1)]

    for i in range(2, int(n ** 0.5) + 1):
        j = i
        while j <= n:
            if j > i:
                nums[j] = False
            j += i

    return [i for i in range(len(nums)) if nums[i]]
