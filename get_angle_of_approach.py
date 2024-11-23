#!/usr/bin/env python3

import math

def getAngleOfApproach(a, b, alpha, beta):
    anOfAprch = (((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha
    return anOfAprch
#Notes: a = right house distance, b = left house distance, alpha = right house angle, beta = left house angle

#Example usage
def main():
    res = getAngleOfApproach(69, 65, 169, 247)
    resDeg = res * 180 / math.pi
    print(res)
    print(resDeg)

if __name__ == "__main__":
    main()