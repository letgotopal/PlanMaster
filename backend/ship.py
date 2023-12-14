from copy import copy

class Ship:
    '''
    @function: constructor for the Ship class
    @param self: the Ship object
    @param r: the number of rows on the ship
    @param c: the number of columns on the ship
    @ param gn: the time taken to move the container from start to end
    @param bay: the 2D array representing the ship's bay. MUST BE SUPPLIED BY THE MANIFEST ORDER TO SUCCESSFULLY DISPLAY THE ORDER
    @return: a Ship object
    '''
    def __init__(self, r=9, c=12, bay=None, gn=0, parent=None):
        self.r = r
        self.c = c

        # Initialize bay with "UNUSED" for all elements
        self.bay = [[(0, "UNUSED") for _ in range(c)] for _ in range(r)]

        # Stores a tuple of the form (top, bottom) for each column
        # The top is the first instance of a container in the column
        # The bottom is the last instance of a container in the column
        self.colHeight = [(0,0)]*c

        self.gn = gn

        # Override with the provided bay if available
        if bay:
            self.bay = bay

        # Adding a crane location (row, column) to the ship
        self.craneLocation = (8,0)

        # Adding a parent variable to each ship
        self.parent = parent

        # Adding variable to show what the specific move from the parent ship to the current ship was
        # Initialized to ((-1,-1),(-1,-1)) because no container has been moved on the initial ship.
        # ((startRow,startCol), (endRow,endCol))
        self.lastMove = ((-1,-1),(-1,-1))

    '''
    @function: prints the ship's bay
    @param self: the Ship object
    @return: None
    '''
    def print_bay(self):
        for i in range(self.r):
            for j in range(self.c):
                print(self.bay[i][j], end=' ')
            print() # newline

    '''
    @function: sets the value of a cell in the ship's bay
    @param self: the Ship object
    @param int(i): the row of the cell
    @param int(j): the column of the cell
    @param tuple(value): the value to set the cell of type (int(weight), str(message))
    @return: None
    '''
    def set_value(self, i, j, value):
        self.bay[i][j] = value

    '''
    @function: gets the value of a cell in the ship's bay
    @param self: the Ship object
    @param int(i): the row of the cell
    @param int(j): the column of the cell
    @return: the value of the cell
    '''
    def get_value(self, i, j):
        return self.bay[i][j]
    
    '''
    @function: gets the value of a cell in the ship's bay
    @param self: the Ship object
    @return: None
    updates the colHeights of the ship
    '''
    def calculateColHeight(self):
        for col in range(self.c):
            top = -1
            bottom = -1
            for row in range(self.r):
                if self.bay[row][col][1] != "UNUSED" and self.bay[row][col][1] != "NAN":
                    top += 1
                elif self.bay[row][col][1] == "NAN":
                    bottom += 1
                    top += 1

            self.colHeight[col] = (top, bottom)

    '''
    @function: Re-defining the equality operator for the Ship class
    @param self: the Ship object
    @param other: the other Ship object to compare to
    @return: True if the two ships are equal, False otherwise
    '''
    def __eq__(self, other):
        if self.r != other.r or self.c != other.c:
            return False

        if self.bay != other.bay:
            return False

        return True
    
    '''
    @function: Calculating the G(n) i.e. time taken to move container from one position to another
    @param self: The ship with the initial position of the container
    @param initCol: The initial position of the container
    @param finalCol: The final position of the container
    @return: The time taken to move the container from start to end
    '''
    def balanceTimeFunction(self, initCol, finalCol):

        # colHeights[0] is the heights of all the columns in the ship
        colHeights = self.colHeight
        
        # Initializing the base val of maxHeight
        maxHeight = colHeights[initCol][0]
        
        # The top of the initial container
        initialHeight = maxHeight
        
        # For the heights between the initial and final container columns
        # Makes sure to go a level above the max height container unless it's already at 8 (0-indexed)
        if initCol < finalCol:
            for col in range(initCol+1, finalCol+1):
                if maxHeight <= colHeights[col][0] and maxHeight < 8:
                    maxHeight = colHeights[col][0] + 1
        else:
            for col in range(finalCol, initCol):
                if maxHeight <= colHeights[col][0] and maxHeight < 8:
                    maxHeight = colHeights[col][0] + 1
        
        # The final height of the container
        finalHeight = colHeights[finalCol][0] + 1

        # The time taken to move the container from start to end
        result = abs(maxHeight - initialHeight) + abs(finalCol - initCol) + abs(maxHeight - finalHeight)

        # Updating the result to include the crane's time taken to move to the container
        result += self.craneTimeFunction(initCol)

        # Printing the entire g(n) score breakdown
        # print('(', maxHeight, '-', initialHeight, ') + ', 'abs (', finalCol, ' - ', initCol, ')', ' + (', maxHeight, '-', finalHeight, ') + ', self.craneTimeFunction(initCol), ' = ', result, sep='')
        
        return result
    

    '''
    @function: Calculating the H(n) i.e. the estimated time to move to a balanced ship from the current
    @param self: The ship with the final position of the container
    @return: H(n) value
    '''
    def balanceHeuristic(self):
        leftMass = 0
        rightMass = 0
        balanceMass = 0
        deficit = 0
        leftContainers = []
        rightContainers = []
        closestLeftAvailableCol = 0
        closestRightAvailableCol = 6
        colHeights = self.colHeight
        hn = 0

        left = self.c//2
        right = self.c - left

        
        for col in range(left):
            for row in range(self.r):
                if self.get_value(row, col)[1] != "UNUSED":
                    containerMass = self.get_value(row, col)[0]
                    leftMass += containerMass
                    leftContainers.append((col, containerMass))
            if colHeights[col][0] < 7:
                closestLeftAvailableCol = col
        
        colSetFlag = 0 #making sure we only set the first available column since we are starting next to the centerline
        for col in range(right, self.c):
            for row in range(self.r):
                if self.get_value(row, col)[1] != "UNUSED":
                    containerMass = self.get_value(row, col)[0]
                    rightMass += containerMass
                    rightContainers.append((col, containerMass))
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
            hn = 1
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
    

    '''
    @function: Calculating the H(n) i.e. the estimated time to move to an unloaded ship from the current
    @param self: The ship with the final position of the container
    @return: H(n) value
    '''
    def unloadHeuristic(self, unloadList):
        hn = 0
        colHeights = self.colHeight

        for i in range(len(unloadList)):
            (unloadRow,unloadCol) = unloadList[i]
            top = colHeights[unloadCol][0]
            hn = hn + top-unloadRow
        
        return hn


    '''
    @function: Calculating the G(n) i.e. time taken to move the crane from origin to the goal container's pos
    @param self: The ship with the initial position of the container
    @param finalRow: Row of the goal container
    @param finalCol: Col of the goal container
    @return: Same as description of the function
    '''
    def craneTimeFunction(self, finalColumn):
        colHeights = self.colHeight
        finalRow = colHeights[finalColumn][0]
        initCraneRow = self.craneLocation[0]
        initCraneCol = self.craneLocation[1]

        # Initializing the base val of maxHeight
        maxHeight = initCraneRow

        if initCraneCol < finalColumn:
            for col in range(initCraneCol+1, finalColumn):
                if maxHeight <= colHeights[col][0] and maxHeight < 8:
                    maxHeight = colHeights[col][0] + 1
        else:
            for col in range(finalColumn+1, initCraneCol):
                if maxHeight <= colHeights[col][0] and maxHeight < 8:
                    maxHeight = colHeights[col][0] + 1

        if maxHeight <= colHeights[finalColumn][0] and maxHeight < 8:
            maxHeight = colHeights[finalColumn][0]

        result = abs(maxHeight- min(initCraneRow, finalRow)) + abs(initCraneCol-finalColumn)

        # Printing the entire g(n) score breakdown
        # print('abs (', maxHeight, '-', finalRow, ') + ', 'abs (', initCraneCol, ' - ', finalColumn, ')', ' = ', result, sep='')

        
        return result


    '''
    @function: Calculating the G(n) i.e. total time taken to unload a container off the ship
    @param self: The ship with the initial position of the container
    @param row: The row of the goal container
    @param column: The column of the goal container
    @return: An int value of the G(n) score
    '''
    def unloadTimeFunction(self, row, column):
        
        # The result to be returned
        res = 0
        
        # Initializing the Crane time variable
        craneTime = 0
        
        # The time taken to got from the ship to the truck is 2 units/minutes
        shipToTruck = 2

        # Check the crane's prev location
        if self.craneLocation[0] != 8 or self.craneLocation[1] != 0:
            # If the crane's prev location is (0,0), then the crane is at the ship's location
            print("In here")
            craneTime = self.craneTimeFunction(column)
            print("Crane time is: ", craneTime)
            
            # Updating the result to include the crane's time taken to move to the container
            res += craneTime + shipToTruck

        # Calculaing the time take to move from the initial position onto the truck
        # Calculating the time to get to 9 high
        rowTot =  8 - row

        # Calculatin ghte time to get to the 0th col
        colTot = column


        # Final result
        # rowTot + colTot is the time to get to the top left of the ship (also accounting for the additional ship to truck time here)
        res = res + rowTot + colTot + shipToTruck

        if self.craneLocation == (8,0):
            # Double the result to add the time taken by the crane
            res *= 2
        
            # Printing the entire g(n) score breakdown
            # print('(', rowTot, '+', colTot, '+', shipToTruck, ') * 2 = ', res, sep='')
        
        # Printing the entire g(n) score breakdown outside the if statement
        # print('(', rowTot, '+', colTot, '+', shipToTruck, ') + (', craneTime,') = ', res, sep='')

        return res


    # Not a perfect heuristic, but it's a start
    '''
    @function: SIFTING heuristic function
    @param self: The ship with the initial position of the container
    @param goal: The goal state of the ship
    @return: An int value of the H(n) score
    '''
    def siftHeuristic(self, goal):
        hn = 0
        for col in range(self.c):
            for row in range(self.r):
                if self.get_value(row, col)[1] != goal.get_value(row, col)[1]:
                    hn += 1
        return hn


