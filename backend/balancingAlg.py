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

'''
@function: constructor for the Ship class
@param self: the Ship object
@param r: the number of rows on the ship
@param c: the number of columns on the ship
@param bay: the 2D array representing the ship's bay. MUST BE SUPPLIED BY THE MANIFEST ORDER TO SUCCESSFULLY DISPLAY THE ORDER
@return: a Ship object
The value of the ship is stored as: value = (int(weight), message)
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
            
            top, bottom = ship.colHeight[col]
            if bottom != ship.r:
                if top != ship.r:
                    ship.set_value(top+1, col, value)
                    score = balanceScore(ship)
                    result.append((score, ship))
                    ship.set_value(top+1, col, (0, "UNUSED"))
    
    return result


# Tests whether the ship is balanced
def goalTest(score):
    if score > 0.9:
        return True
    return False
'''
@function
'''

 
def ucs(ship):
    
    queue = set(operations(ship))

    while(len(queue) != 0):
        node = queue.pop()
        
        if goalTest(node[0]):
            return node[1]

        newOperations = operations(node[1])
        queue.update(newOperations)
    
    # Supposed to call SIFT
    return "TESTING: Can't be balanced" 
        
