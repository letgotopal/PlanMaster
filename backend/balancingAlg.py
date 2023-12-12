from operations import baseOperations
from sortedcontainers import SortedSet

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
    # queue = []
    # visited = []

    # Initialize the frontier with the initial state's operations
    queue = baseOperations(ship)    

    # Initializing the visited set
    # visited = set(node for node in queue)
    visited = set()

    # Set up the frontier as a sortedset based on the gn score
    queue = SortedSet(queue, key=lambda x: x.gn)

    # Sort the frontier based on the gn score
    # queue = sorted(queue, key=lambda x: x.gn)
    
    while(len(queue) != 0):
        # node = queue.pop(0)
        node = queue[0]
        queue.discard(node)

        # print("Len of queue: ", len(queue), '\n')

        print("The current bay with score: ", node.gn)
        node.print_bay()
        print('\n')

        goalRes = goalTest(node)
    
        if goalRes is True:
            return node


        if node not in visited:
            newOperations = baseOperations(node)
            visited.add(node)
            visited = set(visited)
            for newOp in newOperations:
                if newOp not in visited:
                    queue.add(newOp)
            queue = SortedSet(queue, key=lambda x: x.gn)


        # newOperations = baseOperations(node)
        # # visited.append(node)
        # # appendFlag = False  
        # for newOp in newOperations:
        #     # if newOp not in visited:
        #     if newOp not in visited:

        #     #     inQueue = any(newOp == ships for ships in queue)
        #     #     if inQueue:
        #     #         continue
        #     #     queue.append(newOp)
        #     #     appendFlag = True
        #         visited.add(newOp)    
        #         queue.add(newOp)
        # if appendFlag:
        #     queue = sorted(queue, key=lambda x: x.gn)

    # NEVER CALLING SIFT!!!!!!!!!!!(No sift)
    return "Can't be balanced" 