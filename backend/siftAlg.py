from ship import Ship
from operations import siftOperations
import copy

def goalBuilder(ship):
    # Get all the containers of the ship
    containers = []
    for col in range(ship.c):
        for row in range(ship.r):
            val = ship.get_value(row, col)
            if val[1] != 'UNUSED' and val[1] != 'NAN':
                print("The val is: ", val)
                containers.append(val)

    # Sort the containers based on their weight
    containers = sorted(containers, key=lambda x: x[0])

    # Create a new ship instance
    newShip = copy.deepcopy(ship)

    # Preserving only the NANs for the new ship
    for col in range(newShip.c):
        for row in range(newShip.r):
            val = newShip.get_value(row, col)
            if val[1] != 'NAN':
                newShip.set_value(row, col, (0, 'UNUSED'))

    # Building the traversal order lists
    # Left
    leftTraversal = ['start']
    leftTraversal.extend(i for i in reversed(range(ship.c // 2)))
    leftTraversal.append('end')
    # Right
    rightTraversal = ['start']
    rightTraversal.extend(j for j in range(ship.c // 2, ship.c))
    rightTraversal.append('end')

    incL = True
    incR = True

    rightRow, rightCol = 0, 1
    leftRow, leftCol = 0, 1


    # Load the containers into the new ship
    for count, container in enumerate(containers):
        # Even counts of the loop will load the containers to the left of the ship
        if count % 2 == 0:
            # Load the container to the left of the ship
            placedL = False

            while not placedL:
                # print("Left Row: ", leftRow, "Left Col: ", leftCol)
                # Maintaining the bounds of traversalList
                if leftTraversal[leftCol] == 'end':
                    leftRow += 1
                    incL = False
                    leftCol -= 1
                elif leftTraversal[leftCol] == 'start':
                    leftRow += 1
                    incL = True
                    leftCol += 1

                # Places the element in question
                if newShip.get_value(leftRow, leftTraversal[leftCol])[1] != "NAN":
                        newShip.set_value(leftRow, leftTraversal[leftCol], container)
                        print("Placed container: ", container)
                        placedL = True

                # Traverses the list based on the incL flag
                if incL:
                    leftCol += 1
                else:
                    leftCol -= 1

                # Ensures that the row doesn't go out of bounds
                if leftRow > ship.r:
                    print("ERROR: Left side of the ship too full performing SIFTING")
                    # breaks the program
                    return -1

        else:

            placedR = False

            while not placedR:
                print("Right Row: ", rightRow, "Right Col: ", rightCol)
                # Maintaining the bounds of traversalList
                if rightTraversal[rightCol] == 'end':
                    rightRow += 1
                    incR = False
                    rightCol -= 1
                elif rightTraversal[rightCol] == 'start':
                    rightRow += 1
                    incR = True
                    rightCol += 1

                # Places the element in question
                if newShip.get_value(rightRow, rightTraversal[rightCol])[1] != "NAN":
                        newShip.set_value(rightRow, rightTraversal[rightCol], container)
                        print("Placed container: ", container)
                        placedR = True

                # Traverses the list based on the incL flag
                if incR:
                    rightCol += 1
                else:
                    rightCol -= 1

                # Ensures that the row doesn't go out of bounds
                if rightRow > ship.r:
                    print("ERROR: Right side of the ship too full performing SIFTING")
                    # breaks the program
                    return -1
            
    # Return the ship with all the containers in order
    return newShip

# Goal test to see if the ship is in the right order for SIFT
def goalTest(ship, goalShip):

    if ship == goalShip:
        return True
    else:
        return False   
    


def ucs(ship):

    # Creating a frontier array to store the nodes
    queue = []
    visited = []

    # Setting up the goal ship
    goalShip = goalBuilder(ship)

    # Initialize the frontier with the initial state's operations
    queue = siftOperations(ship, goalShip) #mode is 0 because we are balancing    

    # Sort the frontier based on the gn score
    queue = sorted(queue, key=lambda x: x.gn)
    
    while(len(queue) != 0):
        node = queue.pop(0)

        # print("Len of queue: ", len(queue), '\n')

        print("The current bay with score: ", node.gn)
        # node.print_bay()
        print('\n')

        goalRes = goalTest(node, goalShip)
    
        if goalRes is True:
            return node

        newOperations = siftOperations(node, goalShip) # mode is 0 because we are balancing
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

    return "ERROR: SIFTING wasn't performed correctly" 
        
