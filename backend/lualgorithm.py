from ship import Ship
import copy

# Writing the G(n) approach of calculating the time taken to unload all the requested containers off the ship
'''
@function: Identifying the list of containers to be unloaded
@param ship: the Ship object
@param userInput: (row, column) of the container to be unloaded
@return: a list of container names to be unloaded
# '''
# def unloadList(ship, userInput):
#     res = []
#     for container in userInput:
#         res.append((ship.get_value(container[0], container[1])[1]))
    
#     pass

'''
@function: Unload operations functions for our algorithm
@param ship: the Ship object
@return: a list of tuples of the form (score, ship)
'''
def operations(ship, unloadList):
    
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

            # Change the colHeight to remove the goal container
            new_ship.colHeight[column] = (top-1, bottom)
            
            # New score of the ship that has been unloaded
            new_ship.gn = ship.gn + ship.unloadTimeFunction(row, column)

            # Update the bay to reflect the unloaded container
            new_ship.set_value(row, column, (0, "UNUSED"))
            
            # A flag in the goalTest list that it has been unloaded
            unloadList[i] = (-1, -1)

            # Re-setting the crane's intital location to (0,0)
            new_ship.craneLocation = (9,0)

            # Appending the current gn score to sort based on the order
            result.append((new_ship.gn, new_ship))
            
            continue
        
        if top != row:
            # If so, set the value var to the value of the cell
            value = ship.get_value(top, column)
            r, c = top, column
        else:
            continue

    return result

