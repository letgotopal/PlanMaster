import copy
# returns the minimum cost in a vector( if
# there are multiple goal states)
# Goal: empty list
# Start: List with containers to be unloaded
# Ship: Manifest, and Goal Containers


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

''''
@function:Unload operations functions for our ucs algorithm
@param ship: the Ship object
@return: a list of tuples of the form (score, ship)
'''
def operations(ship):
    
    result = []
    
    # 12 columns = 144 possible new ship states
    for column in range(ship.c):
        value = 'UNUSED'
        r,c = 0,0
        top, bottom = ship.colHeight[column]
        if top != bottom:
            # If so, set the value var to the value of the cell
            value = ship.get_value(top, column)
            r, c = top, column
        else:
            continue
        
        for col in range(ship.c):
            # Check if the cell is not empty
            if col == column:
                continue

            top, bottom = ship.colHeight[col]
            if bottom != ship.r:
                if top != ship.r:
                    
                    # Make a copy of the ship
                    new_ship = copy.deepcopy(ship)

                    # set the final location of the container with it's weight and value
                    new_ship.set_value(top+1, col, value)

                    # Reset the original location to UNUSED
                    new_ship.set_value(r, c, (0, "UNUSED"))

                    # Update the gn score of the ship with move's score
                    new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col)

                    # Recalculate the colHeights of the ship
                    new_ship.calculateColHeight()

                    # Re-setting the crane's intital location to the new container's location
                    new_ship.craneLocation = (top+2,col)

                    # Setting the balance score of the ship
                    score = balanceScore(new_ship)

                    # Appending the balance score and the new ship to the result list
                    result.append((score, new_ship))

    return result


# Tests whether the ship is balanced
def goalTest(score):
    if score > 0.9:
        return True
    return False


def ucs(ship):

    # Creating a frontier array to store the nodes
    queue = []
    visited = []

    # Initialize the frontier with the initial state's operations
    queue = operations(ship)    

    queue = sorted(queue, key=lambda x: x[1].gn)
    
    while(len(queue) != 0):
        node = queue.pop(0)

        print("Len of queue: ", len(queue), '\n')

        print("The current bay with score: ", node[1].gn)
        node[1].print_bay()
        print('\n')

        goalRes = goalTest(node[0])
    
        if goalRes is True:
            return node[1]

        newOperations = operations(node[1])
        visited.append(node)
        appendFlag = False  
        for newOp in newOperations:
            if newOp not in visited:
                inQueue = any(newOp[1] == ships for vals, ships in queue)
                if inQueue:
                    continue
                queue.append(newOp)
                appendFlag = True
                
        if appendFlag:
            queue = sorted(queue, key=lambda x: x[1].gn)

    # Supposed to call SIFT
    return "TESTING: Can't be balanced" 
        
