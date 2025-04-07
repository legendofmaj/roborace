#!/usr/bin/env python3

import math

def getAngleOfApproach(a, b, alpha, beta):
    anOfAprch = (((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha
    return anOfAprch

#Debugging Notes: a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle

#Example usage
def main():
    res = getAngleOfApproach(84.10000000000001, 83.30000000000001, 104, 185)
    print(res)

if __name__ == "__main__":
    main()