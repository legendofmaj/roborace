#!/usr/bin/env python3

import math

def getAngleOfApproach(a, b, c):
    anOfAprch = a - b * math.sin(90-(c-b)) / math.sqrt(a** + b** - 2*a*b * math.cos(c-b))
    return anOfAprch

def main():
    res = getAngleOfApproach(1, 1, 1)
    print(res)

if __name__ == "__main__":
    main()