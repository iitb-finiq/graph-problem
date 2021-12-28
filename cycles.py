import numpy as np

'''
detect_cycles() function returns the length (cost) of 
all the cycles that are found in a path
'''
def detect_cycles(path, edges):
    dict = {}
    length = 0
    dict[path[0]] = 0
    cost = []

    for i in range(1, len(path)):
        length += edges[path[i-1]][path[i]]
        
        if path[i] in dict.keys():
            keyss = list(dict.keys())
            
            for k in keyss:
                if dict[k] > dict[path[i]]:
                    del dict[k]
            
            cost.append(length - dict[path[i]])
        
        dict[path[i]] = length
    
    return cost



path = [0, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 1]

edges = np.ones((6, 6))*float('inf')
edges[0][1] = 2
edges[1][2] = 3
edges[2][3] = 4
edges[3][4] = 5
edges[4][1] = 6
edges[5][0] = 1
edges[3][1] = 2

# print(detect_cycles(path, edges))