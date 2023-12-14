from .ship import Ship
from .operations import unloadOperations


'''
@function: Goal test for the unload algorithm
@param ship: the Ship object
@return: True if the ship is empty, False otherwise
'''
def goalTest(unloadList):
    for container in unloadList:
        if container != (-1, -1):
            return False
    return True

def ucs(ship, uList):

    # Creating a frontier array to store the nodes
    queue = []
    visited = []

    # Initialize the frontier with the initial state's operations
    queue = unloadOperations(ship, uList)    

    # Sort the frontier based on the gn score
    queue = sorted(queue, key=lambda x: x[1].gn)
    
    while(len(queue) != 0):
        node = queue.pop(0)

        # print("The current bay with list: ", node[0])
        # print("The Crane's current location is: ", node[1].craneLocation)
        # node[1].print_bay()
        # print('\n')

        goalRes = goalTest(node[0])
    
        if goalRes is True:
            return node[1]

        newOperations = unloadOperations(node[1], node[0])
        visited.append(node[1])
        appendFlag = False  
        for newOp in newOperations:           
            if newOp[1] not in visited:
                inQueue = any(newOp[1] == ships for lists, ships in queue)
                if inQueue:
                    continue
                queue.append(newOp)
                appendFlag = True
                
        if appendFlag:
            queue = sorted(queue, key=lambda x: x[1].gn)

    # It should never print this string
    return "Big OOF" 
        

    


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

