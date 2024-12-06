import math
dist_at_oneOFive = 85
edges = {150: [85, 1]}
edges[270] = [95, 2]
edges[280] = [64, 1]
edges[340] = [50, 2]
anglesAndDists = {1000000 : 100000}

def find_angles():
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)
    leftest_edge = edges[edges_keys[0]]
    if leftest_edge[1] == 2:
        edges[150] = [dist_at_oneOFive, 1]
    edges_keys = edges.keys()
    edges_keys = [int(x) for x in edges_keys]
    edges_keys = sorted(edges_keys)

    for x in range(len(edges)):
        if x % 2 != 0:
            continue
        right = edges[edges_keys[x]]
        left = edges[edges_keys[(x+1)]]
        a = int(right[0])#rightCornerDist 
        b = int(left[0])#leftCornerDist 
        alpha = int(edges_keys[x])#rightCornerAngle
        beta = int(edges_keys[(x+1)])#leftCornerAngle
        anOfAprch = getAngleOfApproach(a, b, alpha, beta)
        distToNextHouse = getDistToNextHouse(a, alpha, anOfAprch)
        anglesAndDists[int(distToNextHouse)] = int(anOfAprch)
        print(left)
        print(right)
        print(alpha)
        print(beta)
        print(anglesAndDists)
        print(x)


def getAngleOfApproach(a, b, alpha, beta):
    #global anOfAprch
    #try:
    anOfAprch = ((((a - b * math.sin(math.radians(90-(beta-alpha)))) / math.sqrt(((a*a) + (b*b)) - (2*a*b * math.cos(math.radians((beta-alpha)))))) * 180 / math.pi) + alpha) - 90
    #except ZeroDivisionError:
    #    anOfAprch = 90
    #    print("fuck fuck fuck fuck FUUUUCK")
    #except:
    #    print("wtf is wrong now?")
    return anOfAprch

def getDistToNextHouse(a, alpha, anOfAprch):
    distToNextHouse = abs(math.cos(anOfAprch - alpha)) * a
    return distToNextHouse

find_angles()