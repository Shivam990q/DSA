"""
COMPETITIVE PROGRAMMING TEMPLATE — Python 3
Uses fast I/O. Run with PyPy3 for CP whenever available (~5-10× faster).
"""

import sys
from sys import stdin, stdout
from collections import defaultdict, Counter, deque
from heapq import heappush, heappop, heapify, heappushpop, heapreplace
from bisect import bisect_left, bisect_right, insort
from itertools import accumulate, combinations, permutations, product
from math import gcd, lcm, sqrt, ceil, floor, log, log2, isqrt, factorial, comb, perm
from functools import lru_cache, reduce
import math

# Increase recursion limit
sys.setrecursionlimit(10**6)

# Fast input
input = stdin.readline

# Constants
MOD = 10**9 + 7
INF = float('inf')

def ints(): return list(map(int, input().split()))
def integer(): return int(input())
def words(): return input().split()
def word(): return input().strip()

def solve():
    n = integer()
    arr = ints()
    # ... your code here
    print(n)

def main():
    t = 1
    # t = integer()  # uncomment for multiple test cases
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
