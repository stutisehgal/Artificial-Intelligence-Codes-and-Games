# -*- coding: utf-8 -*-

from queue import PriorityQueue
from ast import literal_eval

v = int(input("Enter total no. of nodes: "))
graph = [[] for i in range(v)]



def best_first_search(source, target, n):
    visited = [0] * n
    visited[0] = True
    pq = PriorityQueue()
    pq.put((0, source))
    while pq.empty() == False:
            
        u = pq.get()[1]
        print(u, end=" ")
        if u == target:
            break
        
        for v, c in graph[u]:
            if visited[v] == False:
                visited[v] = True
                pq.put((c, v))
    print()


def addedge(x, y, cost):
    graph[x].append((y, cost))
    graph[y].append((x, cost))

flag = False
print("==========")
print("Write 0,1,5 to denote edge from 0 to 1 with cost 5 | 'X' to finish")
strs = input("Input: ")
while flag is False:
    literal_eval(strs.replace(' ',','))
    i = int(strs[0])
    j = int(strs[2])
    k = int(strs[4])
    addedge(i, j, k)
    strs = input("Input: ")
    if strs == 'X':
        flag = True

source = int(input("Enter source node: "))
target = int(input("Enter target node: "))
best_first_search(source, target, v)