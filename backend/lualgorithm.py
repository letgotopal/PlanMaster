# Contains the load/unload algorithm for Part 1 of the problem
# For less than 3 moves, we're going to be using Uniform Cost Search as our algorithm
# For more than 3 moves, we're going to be using the same with a different heuristic (TBD)

# Importing the necessary libraries
import heapq
import math
import copy
from ship import Ship
from manifest import Manifest
from collections import deque

# Identify all the columns of the goal containers
# Identify all the columns of the UNUSED containers
# To unload the containers, we need to move the containers above it
# on top of the UNUSED stack to make room for unloading it
# Hence our start becomes everything that is stacked above the goal containers
# Our end becomes every valid position nearest to the start
# Some pitfalls of this algorithm include:
#   - Every column has a goal container
#   - There could be multiple goal containers in a column
#  - Stacking it on top of a goal container column with prove to be more efficient
#    than stacking it on top of the closest UNUSED container column 
  
# Pseudocode for the algorithm:
# unload_algorithm(ship=Ship, goalContainers=List, heuristic=ManhattanDistance)
    # colWithGoals = set(col for col in ship.bay if col in goalContainers)

    # for each item in goalContainers:
        # itemRow, itemCol = item

        # for each container in range(1, itemRow):
            # if container != "UNUSED":
                # possibleEnds = findEndPos(container, colsWithGoals)
                # costList = []
                
                # for each end in possibleEnds:
                #    costList = uniform_cost_search(start=container, end=end, heuristic=ManhattanDistance)
                
                # min(costList)
                # break

# Pseudocode for finding the end position:
# findEndPos(container, colsWithGoals, ship)
    # endPos = []
    # numCols = ship.c i.e. all the columns in the ship

    # for each col in numCols:
        # for each item in col:
            # openPos = the first UNUSED position in the column
            # cost = uniform_cost_search(start=container, end=openPos, heuristic=ManhattanDistance)
            # if col is in colsWithGoals:
                # cost *= 2 Since we'd have to move the container back to the original position at the worst case
            # endPos.append((cost, openPos))
    # return min(endPos)

# Pseudocode for Uniform Cost Search:
def uniform_cost_search(start, end, heuristic):
    frontier = heapq.heapify([]) # Priority queue
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == end:
            break

        # for next in graph.neighbors(current):
        for next in neighbors(current):
            # new_cost = cost_so_far[current] + graph.cost(current, next) 
            new_cost = cost_so_far[current] + 1 # Where the cost is always 1 (minute)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far

'''
@function neighbors: finds the neighbors of a given cell
it works by finding the list of immediately adjacent cells that are empty
@param current: the current cell/position
@param ship: the ship object
@return: a list of the neighbors of the current cell
'''
def neighbors(current, ship):
    neighbors = []
    r, c = current
    # Up
    if current[0] > 0 and ship.get_value(r-1, c)[1] == "UNUSED":
        neighbors.append((current[0]-1, current[1]))
    
    # Left
    if current[1] > 0 and ship.get_value(r, c-1)[1] == "UNUSED":
        neighbors.append((current[0], current[1]-1))
    
    # Right
    if current[1] < ship.c-1 and ship.get_value(r, c+1)[1] == "UNUSED":
        neighbors.append((current[0], current[1]+1))
    
    # Down
    if current[0] < ship.r-1 and ship.get_value(r+1, c)[1] == "UNUSED":
        neighbors.append((current[0]+1, current[1]))
    
    return neighbors