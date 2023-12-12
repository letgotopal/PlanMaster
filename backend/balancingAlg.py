from operations import baseOperations

def balanceScore(ship):
    # Formula: BalanceScore = min(left, right)/max(left, right) > 0.9
    # left = sum of weights of containers on the left side of the ship i.e. columns 0-5
    # right = sum of weights of containers on the right side of the ship i.e. columns 6-11
    left = ship.c//2
    right = ship.c - left

    leftSum = 0
    for col in range(left):
        for row in range(ship.r):
            if ship.get_value(row, col)[1] != "UNUSED":
                leftSum += ship.get_value(row, col)[0]

    rightSum = 0
    for col in range(right, ship.c):
        for row in range(ship.r):
            if ship.get_value(row, col)[1] != "UNUSED":
                rightSum += ship.get_value(row, col)[0]

    # If the ship is empty
    if leftSum == 0 and rightSum == 0:
        return 1

    # If one side is empty
    if leftSum == 0 or rightSum == 0:
        return 0

    result = min(leftSum, rightSum)/max(leftSum, rightSum)

    return result

# Tests whether the ship is balanced
def goalTest(ship):
    score = balanceScore(ship)
    if score > 0.9:
        return True
    return False

# def closetAvailCol(ship, side):
#     colHeights = ship.colHeight
#     left = ship.c//2
#     right = ship.c - left
#     closestCol = 0
#     if side == "Left":
#         for col in range(left):
#             if colHeights[col][0] < 7:
#                 closestCol = col
#     elif side == "Right":
#         colFound = False
#         for col in range(right, ship.c):
#             if colHeights[col][0] < 7 and colFound == False:
#                 closestCol = col
#                 colFound = True
    



#return hn for a heuristic
def heuristic(ship):
    leftMass = 0
    rightMass = 0
    balanceMass = 0
    deficit = 0
    leftContainers = []
    rightContainers = []
    closestLeftAvailableCol = 0
    closestRightAvailableCol = 6
    colHeights = ship.colHeight
    hn = 0

    left = ship.c//2
    right = ship.c - left

    
    for col in range(left):
        for row in range(ship.r):
            if ship.get_value(row, col)[1] != "UNUSED":
                containerMass = ship.get_value(row, col)[0]
                leftMass += containerMass
                leftContainers.append(col, containerMass)
        if colHeights[col][0] < 7:
            closestLeftAvailableCol = col
    
    colSetFlag = 0 #making sure we only set the first available column since we are starting next to the centerline
    for col in range(right, ship.c):
        for row in range(ship.r):
            if ship.get_value(row, col)[1] != "UNUSED":
                containerMass = ship.get_value(row, col)[0]
                rightMass += containerMass
                rightContainers.append(col, containerMass)
        if colHeights[col][0] < 7 and colSetFlag == 0:
            closestRightAvailableCol = col
            colSetFlag = 1

    balanceMass = (leftMass + rightMass)/2
    balScore = min(leftMass, rightMass)/max(leftMass, rightMass)

    if balScore > 0.9:
        hn = 0
        return hn
    else:
        #if deficit is left side

        if balanceMass - leftMass > 0:
            deficit = balanceMass - leftMass
            rightContainers.sort(key=lambda x: x[1], reverse=True)
            for container in rightContainers:
                if container[1] <= deficit:
                    hn = hn + abs(closestLeftAvailableCol - container[0]) #need closest available cols function to make better
                    deficit = deficit - container[0]

        #if deficit is right side

        elif balanceMass - rightMass > 0:
            deficit = balanceMass - rightMass
            leftContainers.sort(key=lambda x: x[1], reverse=True)
            for container in leftContainers:
                if container[1] <= deficit:
                    hn = hn + abs(closestRightAvailableCol - container[0]) #need closest available cols function to make better
                    deficit = deficit - container[0]
              ######What to do when surplus side does not have a container <= the deficit???? Maybe we need to look at deficit side and 
              # see if there is a container where we can get the deficit by swapping one from deficit side for a heavier one on surplus side
              # (where the difference between the swapped is = to deficit)      
    return hn




def ucs(ship):

    # Creating a frontier array to store the nodes
    queue = []
    visited = []

    # Initialize the frontier with the initial state's operations
    queue = baseOperations(ship)    

    # Sort the frontier based on the gn score
    queue = sorted(queue, key=lambda x: x.gn)
    
    while(len(queue) != 0):
        node = queue.pop(0)

        # print("Len of queue: ", len(queue), '\n')

        print("The current bay with score: ", node.gn)
        # node.print_bay()
        print('\n')

        goalRes = goalTest(node)
    
        if goalRes is True:
            return node

        newOperations = baseOperations(node)
        visited.append(node)
        appendFlag = False  
        for newOp in newOperations:
            if newOp not in visited:
                inQueue = any(newOp == ships for ships in queue)
                if inQueue:
                    continue
                queue.append(newOp)
                appendFlag = True
                
        if appendFlag:
            queue = sorted(queue, key=lambda x: x.gn)

    # NEVER CALLING SIFT!!!!!!!!!!!(No sift)
    return "Can't be balanced" 
        
