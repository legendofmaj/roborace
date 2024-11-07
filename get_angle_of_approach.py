#!/usr/bin/env python3

import math

def getAngleOfApproach(a, b, alpha, beta):
    anOfAprch = a - b * math.sin(90-(alpha-beta)) / math.sqrt(a** + b** - 2*a*b * math.cos(alpha-beta))
    return anOfAprch

#Debugging Notes: a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle

#Example usage
def main():
    res = getAngleOfApproach(1, 1, 1, 1)
    print(res)

if __name__ == "__main__":
    main()