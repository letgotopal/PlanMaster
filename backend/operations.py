import copy

''''
@function:Unload operations functions for our balancing/basic algorithm
@param ship: the Ship object
@return: a list of tuples of the form (score, ship)
'''
def baseOperations(ship):
    
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

                    # Update the gn score of the ship with move's score
                    new_ship.gn = ship.gn + ship.balanceTimeFunction(column, col)

                    # Setting the containers previous (from the old ship) and new location on the new ship
                    new_ship.lastMove = ((origRow, origCol), (top+1, col))

                    # Recalculate the colHeights of the ship
                    new_ship.calculateColHeight()

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
        
        if unloadList[i] == (-1, -1):
            continue
        
        if top == row:
            # Make a copy of the ship
            new_ship = copy.deepcopy(ship)

            # Setting the parent of the new ship to the current ship
            new_ship.parent = ship

            # Change the colHeight to remove the goal container
            new_ship.colHeight[column] = (top-1, bottom)

            # Setting the old container location, and the new location (-1,-1) since it has been moved to a truck
            new_ship.lastMove = ((top, column), (-1,-1))
            
            # New score of the ship that has been unloaded
            new_gn = ship.unloadTimeFunction(row, column)
            new_ship.gn = ship.gn + new_gn
            print("The old ship.gn is: ", ship.gn, "+ the new addition of: ", new_gn, " = ", new_ship.gn)

            # Update the bay to reflect the unloaded container
            new_ship.set_value(row, column, (0, "UNUSED"))

            # A flag in the goalTest list that it has been unloaded
            newUnloadList = copy.deepcopy(unloadList)
            newUnloadList[i] = (-1, -1)

            # Re-setting the crane's intital location to (8,0)
            new_ship.craneLocation = (8,0)

            # Appending the current gn score to sort based on the order
            result.append((newUnloadList, new_ship))
        elif top != row:
            # If so, set the value var to the value of the cell
            value = ship.get_value(top, column)
            r, c = top, column
            for ops in baseOperations(ship):
                result.append((unloadList, ops))
        else:
            print("WHY ARE YOU HERE!!")

    return result

