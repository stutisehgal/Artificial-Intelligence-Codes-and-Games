# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 12:15:36 2021

@author: LEGION
"""

from sys import maxsize
from itertools import permutations

V = 4


# implementation of travelling Salesman Problem
def travellingSalesmanProblem(graph, s):
    print("State Space:\n")
    # store all vertex apart from source vertex
    vertex = []
    for i in range(V):
        if i != s:
            vertex.append(i)

            # store minimum weight Hamiltonian Cycle
    min_path = maxsize
    next_permutation = permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # For Display
        print(s + 1, "->", end="")
        # compute current path weight
        k = s
        for j in i:
            current_pathweight += graph[k][j]
            print(j + 1, "->", end="")
            k = j
        print(s + 1)
        current_pathweight += graph[k][s]
        print("Current Cost:", current_pathweight)
        print("\n")

        # update minimum
        min_path = min(min_path, current_pathweight)

    return min_path


if __name__=='__main__':

#    graph = [[0, 5, 3, 2], [10, 0, 30, 25],
#             [15, 35, 0, 30], [1, 4, 10, 0]]
    
    graph = [[0, 10, 15, 20], [10, 0, 35, 25],
             [15, 35, 0, 30], [20, 25, 30, 0]]
    
    s = 0
    print("Minimum Cost:", travellingSalesmanProblem(graph, s))
    
    
    
    
    
    
    print("Optimal path: 1 ->3 ->4 ->2 ->1")