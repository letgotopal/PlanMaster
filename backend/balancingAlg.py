# For Frontend:
from .operations import balancingOperations
from .siftAlg import ucs as siftAlg

# For backend:
# from operations import balancingOperations

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

    


def ucs(ship):

    # Creating a frontier array to store the nodes
    queue = []
    visited = []

    # Initialize the frontier with the initial state's operations
    queue = balancingOperations(ship, 0) #mode is 0 because we are balancing    

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

        newOperations = balancingOperations(node, 0) # mode is 0 because we are balancing
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

    # if couldn't balance, call sift
    newShip = siftAlg(ship)
    return newShip
    # NEVER CALLING SIFT!!!!!!!!!!!(No sift)
    # return "Can't be balanced" 
