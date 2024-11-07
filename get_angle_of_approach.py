#!/usr/bin/env python3

import math

def getAngleOfApproach(a, b, beta, gamma):
    anOfAprch = a - b * math.sin(90-(gamma-beta)) / math.sqrt(a** + b** - 2*a*b * math.cos(gamma-beta))
    return anOfAprch

#Example usage
def main():
    res = getAngleOfApproach(1, 1, 1)
    print(res)

if __name__ == "__main__":
    main()