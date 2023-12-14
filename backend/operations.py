import copy

''''
@function:this is the operations for balancing a ship
@param ship: the Ship object
@return: a list of expanded ships
'''
def balancingOperations(ship, mode):
    
    result = []
    
    # 12 columns = 144 possible new ship states
    for column in range(ship.c):
        value = 'UNUSED'
        r,c = 0,0
        top, bottom = ship.colHeight[column]
        origRow = top
        origCol = column
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

                    # Setting the parent of the new ship to the current ship
                    new_ship.parent = ship

                    # set the final location of the container with it's weight and value
                    new_ship.set_value(top+1, col, value)

                    # Reset the original location to UNUSED
                    new_ship.set_value(r, c, (0, "UNUSED"))

###TESTING
                    #new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col)
###TESTING
                    # Setting the containers previous (from the old ship) and new location on the new ship
                    new_ship.lastMove = ((origRow, origCol), (top+1, col))

                    # Recalculate the colHeights of the ship
                    new_ship.calculateColHeight()

                    # Update the gn score of the ship with move's score
                    if mode == 0: #mode == 0 means that we want to use the balancing heuristic
                        new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col) + new_ship.balanceHeuristic()
                    else: #mode != 0 means that we want to use the unloading heuristic 
                        new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col) 

                    # Re-setting the crane's intital location to the new container's location
                    new_ship.craneLocation = (top+1,col)
                    # print("The crane's location is: ", new_ship.craneLocation)
                    
                    # Appending the balance score and the new ship to the result list
                    # result.append((score, new_ship))
                    result.append(new_ship)

    return result


''''
@function:Base unload operations functions for our basic algorithm for unloading
@param ship: the Ship object
@param uList: the list of containers to be unloaded
@return: a list of tuples of the form (score, ship)
'''
def baseUnloadOperations(ship, unloadList):
    
    result = []
    
    # 12 columns = 144 possible new ship states
    for column in range(ship.c):
        value = 'UNUSED'
        r,c = 0,0
        top, bottom = ship.colHeight[column]
        origRow = top
        origCol = column
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

                    # Setting the parent of the new ship to the current ship
                    new_ship.parent = ship

                    # set the final location of the container with it's weight and value
                    new_ship.set_value(top+1, col, value)

                    # Reset the original location to UNUSED
                    new_ship.set_value(r, c, (0, "UNUSED"))

###TESTING
                    #new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col)
###TESTING
                    # Setting the containers previous (from the old ship) and new location on the new ship
                    new_ship.lastMove = ((origRow, origCol), (top+1, col))

                    # Recalculate the colHeights of the ship
                    new_ship.calculateColHeight()

                    # Update the gn score of the ship with move's score
                    #new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col)
                    new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col) + new_ship.unloadHeuristic(unloadList)

                    # Re-setting the crane's intital location to the new container's location
                    new_ship.craneLocation = (top+1,col)
                    # print("The crane's location is: ", new_ship.craneLocation)
                    
                    # Appending the balance score and the new ship to the result list
                    # result.append((score, new_ship))
                    result.append(new_ship)

    return result


'''
@function: Unload operations functions for our unload algorithm
@param ship: the Ship object
@return: a list of tuples of the form (score, ship)
'''
def unloadOperations(ship, unloadList):
    
    result = []
    
    for i in range(len(unloadList)):
        # value = 'UNUSED'
        row, column = unloadList[i]
        r,c = 0,0
        top, bottom = ship.colHeight[column]

        print("Unload col was: ", column, ", unload row was: ", row)
        print("Top was: ", top)

        if unloadList[i] == (-1, -1):
            continue
        
        if top == row:
            print("TOP WAS ROW")
            # Make a copy of the ship
            new_ship = copy.deepcopy(ship)

            # Setting the parent of the new ship to the current ship
            new_ship.parent = ship

            # Change the colHeight to remove the goal container
            new_ship.colHeight[column] = (top-1, bottom)

            # Setting the old container location, and the new location (-1,-1) since it has been moved to a truck
            new_ship.lastMove = ((top, column), (-1,-1))
            
            #new_gn = ship.unloadTimeFunction(row, column)

            # Update the bay to reflect the unloaded container
            new_ship.set_value(row, column, (0, "UNUSED"))

            # A flag in the goalTest list that it has been unloaded
            newUnloadList = copy.deepcopy(unloadList)
            newUnloadList[i] = (-1, -1)

            # New score of the ship that has been unloaded
            #new_gn = ship.unloadTimeFunction(row, column)
            new_gn = ship.unloadTimeFunction(row, column) + new_ship.unloadHeuristic(newUnloadList)
            new_ship.gn = ship.gn + new_gn
            print("The old ship.gn is: ", ship.gn, "+ the new addition of: ", new_gn, " = ", new_ship.gn)

            # Re-setting the crane's intital location to (8,0)
            new_ship.craneLocation = (8,0)

            # Appending the current gn score to sort based on the order
            result.append((newUnloadList, new_ship))
            return result #TESTING TESTING
        #elif top != row:
    print("NOT ROW")
    # If so, set the value var to the value of the cell
    value = ship.get_value(top, column)
    r, c = top, column
    for ops in baseUnloadOperations(ship, unloadList):
        result.append((unloadList, ops))
    #else:
        #print("WHY ARE YOU HERE!!")

    return result

'''
@function: Generates the most efficient load operation for the ship
@param ship: the Ship object
@param container: the container to be loaded
@return: The ship which has the container loaded in the most optimal position
'''

def loadOperation(ship, loadContainer):
    
    # Calculating the time taken for the crane to get back to the edge of the ship
    # Adds zero if the crane is already at the edge of the ship
    ship.gn += ((ship.r - 1) - ship.craneLocation[0]) + (0 - ship.craneLocation[1])
    
    # Resetting the crane's location to the edge of the ship for loads
    ship.craneLocation = (8,0)

    # Calculate the first one before going through the loop
    # Setting minTime an arbitrarily large value
    minTime = 10000
    minCol = 0 

    for col in range(ship.c):
        curTime = ship.craneTimeFunction(col)
        if minTime >= curTime and ship.colHeight[col][0] < 7:
            minTime = curTime
            minCol = col
    
    # Checking if the ship is full
    if minTime == 10000:
        print("The ship is full, cannot load anymore containers")
        return -1

    # Getting a deep copy of the ship
    new_ship = copy.deepcopy(ship)

    # Update the gn score of the ship with move's score
    new_ship.gn = ship.gn + minTime

    # Updating the colHeights of the ship
    new_ship.colHeight[minCol] = (new_ship.colHeight[minCol][0] + 1, new_ship.colHeight[minCol][1])
    
    # Setting the value of the cell to the container
    row = new_ship.colHeight[minCol][0]
    new_ship.set_value(row, minCol, loadContainer)
    
    new_ship.lastMove((-1,-1),(row, minCol))
    # Setting the crane to the new final location as the container
    new_ship.craneLocation = (row, minCol)

    # Returning the new ship
    return new_ship


''''
@function: SIFT algorithm operations
@param ship: the Ship object
@param goal: the goal state of the ship
@return: a list of ships that could possibly be the goal state
'''
def siftOperations(ship, goal):
    
    result = []
    
    # 12 columns = 144 possible new ship states
    for column in range(ship.c):
        value = 'UNUSED'
        r,c = 0,0
        top, bottom = ship.colHeight[column]
        origRow = top
        origCol = column
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

                    # Setting the parent of the new ship to the current ship
                    new_ship.parent = ship

                    # set the final location of the container with it's weight and value
                    new_ship.set_value(top+1, col, value)

                    # Reset the original location to UNUSED
                    new_ship.set_value(r, c, (0, "UNUSED"))

                    # Setting the containers previous (from the old ship) and new location on the new ship
                    new_ship.lastMove = ((origRow, origCol), (top+1, col))

                    # Recalculate the colHeights of the ship
                    new_ship.calculateColHeight()

                    new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col) + new_ship.siftHeuristic(goal)

                    # Re-setting the crane's intital location to the new container's location
                    new_ship.craneLocation = (top+1,col)
                    
                    # Appending the balance score and the new ship to the result list
                    result.append(new_ship)

    return result