# # Contains the load/unload algorithm for Part 1 of the problem
# # For less than 3 moves, we're going to be using Uniform Cost Search as our algorithm
# # For more than 3 moves, we're going to be using the same with a different heuristic (TBD)

# # Importing the necessary libraries
# import heapq
# import math
# import copy
# from ship import Ship
# from manifest import Manifest
# from collections import deque

# # Identify all the columns of the goal containers
# # Identify all the columns of the UNUSED containers
# # To unload the containers, we need to move the containers above it
# # on top of the UNUSED stack to make room for unloading it
# # Hence our start becomes everything that is stacked above the goal containers
# # Our end becomes every valid position nearest to the start
# # Some pitfalls of this algorithm include:
# #   - Every column has a goal container
# #   - There could be multiple goal containers in a column
# #  - Stacking it on top of a goal container column with prove to be more efficient
# #    than stacking it on top of the closest UNUSED container column 
  
# # Pseudocode for the algorithm:
# # unload_algorithm(ship=Ship, goalContainers=List, heuristic=ManhattanDistance)
#     # colWithGoals = set(col for col in ship.bay if col in goalContainers)

#     # for each item in goalContainers:
#         # itemRow, itemCol = item

#         # for each container in range(1, itemRow):
#             # if container != "UNUSED":
#                 # possibleEnds = findEndPos(container, colsWithGoals)
#                 # costList = []
                
#                 # for each end in possibleEnds:
#                 #    costList = uniform_cost_search(start=container, end=end, heuristic=ManhattanDistance)
                
#                 # min(costList)
#                 # break

# # Pseudocode for finding the end position:
# # findEndPos(container, colsWithGoals, ship)
#     # endPos = []
#     # numCols = ship.c i.e. all the columns in the ship

#     # for each col in numCols:
#         # for each item in col:
#             # openPos = the first UNUSED position in the column
#             # cost = uniform_cost_search(start=container, end=openPos, heuristic=ManhattanDistance)
#             # if col is in colsWithGoals:
#                 # cost *= 2 Since we'd have to move the container back to the original position at the worst case
#             # endPos.append((cost, openPos))
#     # return min(endPos)

# # Pseudocode for Uniform Cost Search:
# def uniform_cost_search(start, end, heuristic):
#     frontier = heapq.heapify([]) # Priority queue
#     frontier.put(start, 0)
#     came_from = {}
#     cost_so_far = {}
#     came_from[start] = None
#     cost_so_far[start] = 0

#     while not frontier.empty():
#         current = frontier.get()

#         if current == end:
#             break

#         # for next in graph.neighbors(current):
#         for next in neighbors(current):
#             # new_cost = cost_so_far[current] + graph.cost(current, next) 
#             new_cost = cost_so_far[current] + 1 # Where the cost is always 1 (minute)
#             if next not in cost_so_far or new_cost < cost_so_far[next]:
#                 cost_so_far[next] = new_cost
#                 priority = new_cost + heuristic(end, next)
#                 frontier.put(next, priority)
#                 came_from[next] = current

#     return came_from, cost_so_far

# '''
# @function neighbors: finds the neighbors of a given cell
# it works by finding the list of immediately adjacent cells that are empty
# @param current: the current cell/position
# @param ship: the ship object
# @return: a list of the neighbors of the current cell
# '''
# def neighbors(current, ship):
#     neighbors = []
#     r, c = current
#     # Up
#     if current[0] > 0 and ship.get_value(r-1, c)[1] == "UNUSED":
#         neighbors.append((current[0]-1, current[1]))
    
#     # Left
#     if current[1] > 0 and ship.get_value(r, c-1)[1] == "UNUSED":
#         neighbors.append((current[0], current[1]-1))
    
#     # Right
#     if current[1] < ship.c-1 and ship.get_value(r, c+1)[1] == "UNUSED":
#         neighbors.append((current[0], current[1]+1))
    
#     # Down
#     if current[0] < ship.r-1 and ship.get_value(r+1, c)[1] == "UNUSED":
#         neighbors.append((current[0]+1, current[1]))
    
#     return neighbors



# Python3 implementation of above approach
 
# returns the minimum cost in a vector( if
# there are multiple goal states)
# Goal: empty list
# Start: List with containers to be unloaded
# Ship: Manifest, and Goal Containers
def  uniform_cost_search(goal, start):
     
    # minimum cost upto
    # goal state from starting
    global graph,cost
    answer = []
 
    # create a priority queue
    queue = []
 
    # set the answer vector to max value
    for i in range(len(goal)):
        answer.append(10**8)
 
    # insert the starting index
    queue.append([0, start])
 
    # map to store visited node
    visited = {}
 
    # count
    count = 0
 
    # while the queue is not empty
    while (len(queue) > 0):
 
        # get the top element of the
        queue = sorted(queue)
        p = queue[-1]
 
        # pop the element
        del queue[-1]
 
        # get the original value
        p[0] *= -1
 
        # check if the element is part of
        # the goal list
        if (p[1] in goal):
 
            # get the position
            index = goal.index(p[1])
 
            # if a new goal is reached
            if (answer[index] == 10**8):
                count += 1
 
            # if the cost is less
            if (answer[index] > p[0]):
                answer[index] = p[0]
 
            # pop the element
            del queue[-1]
 
            queue = sorted(queue)
            if (count == len(goal)):
                return answer
 
        # check for the non visited nodes
        # which are adjacent to present node
        if (p[1] not in visited):
            for i in range(len(graph[p[1]])):
 
                # value is multiplied by -1 so that
                # least priority is at the top
                queue.append( [(p[0] + cost[(p[1], graph[p[1]][i])])* -1, graph[p[1]][i]])
 
        # mark as visited
        visited[p[1]] = 1
 
    return answer
 
# main function
if __name__ == '__main__':
     
    # create the graph
    graph,cost = [[] for i in range(8)],{}
 
    # add edge
    graph[0].append(1)
    graph[0].append(3)
    graph[3].append(1)
    graph[3].append(6)
    graph[3].append(4)
    graph[1].append(6)
    graph[4].append(2)
    graph[4].append(5)
    graph[2].append(1)
    graph[5].append(2)
    graph[5].append(6)
    graph[6].append(4)
 
    # add the cost
    cost[(0, 1)] = 2
    cost[(0, 3)] = 5
    cost[(1, 6)] = 1
    cost[(3, 1)] = 5
    cost[(3, 6)] = 6
    cost[(3, 4)] = 2
    cost[(2, 1)] = 4
    cost[(4, 2)] = 4
    cost[(4, 5)] = 3
    cost[(5, 2)] = 6
    cost[(5, 6)] = 3
    cost[(6, 4)] = 7
 
    # goal state
    goal = []
 
    # set the goal
    # there can be multiple goal states
    goal.append(6)
 
    # get the answer
    answer = uniform_cost_search(goal, 0)
 
    # print the answer
    print("Minimum cost from 0 to 6 is = ",answer[0])
 
