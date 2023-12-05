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
    def __init__(self, r=9, c=12, bay=None, gn=0):
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
        self.craneLocation = (9,0)

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
        if initCol < finalCol:
            for col in range(initCol+1, finalCol+1):
                if maxHeight <= colHeights[col][0]:
                    maxHeight = colHeights[col][0] + 1
        else:
            for col in range(finalCol, initCol):
                if maxHeight <= colHeights[col][0]:
                    maxHeight = colHeights[col][0] + 1
        
        # The final height of the container
        finalHeight = colHeights[finalCol][0] + 1

        # The time taken to move the container from start to end
        result = (maxHeight - initialHeight) + abs(finalCol - initCol) + (maxHeight - finalHeight)

        # Updating the result to include the crane's time taken to move to the container
        result += self.craneTimeFunction(initCol)
        
        return result
    
    '''
    @function: Calculating the G(n) i.e. time taken to move the crane from origin to the goal container's pos
    @param self: The ship with the initial position of the container
    @param finalRow: Row of the goal container
    @param finalCol: Col of the goal container
    @return: Same as description of the function
    '''
    def craneTimeFunction(self, finalCol):

        # colHeights[0] is the heights of all the columns in the ship
        colHeights = self.colHeight
        
        # Initializing the base val of maxHeight
        maxHeight = self.craneLocation[0]
        
        # The top of the initial container
        initialHeight = maxHeight
        
        # Setting the initCol to the crane's current column
        initCol = self.craneLocation[1]

        # For the heights between the initial and final container columns
        if initCol < finalCol:
            for col in range(initCol+1, finalCol+1):
                if maxHeight <= colHeights[col][0]:
                    maxHeight = colHeights[col][0] + 1
        else:
            for col in range(finalCol, initCol):
                if maxHeight <= colHeights[col][0]:
                    maxHeight = colHeights[col][0] + 1
        
        # The final height of the container
        finalHeight = colHeights[finalCol][0] + 1

        # The time taken to move the container from start to end
        result = (maxHeight - initialHeight) + abs(finalCol - initCol) + (maxHeight - finalHeight)
        
        return result

    '''
    @function: Calculating the G(n) i.e. total time taken to unload a container off the ship
    @param self: The ship with the initial position of the container
    @param row: The row of the goal container
    @param column: The column of the goal container
    @return: An int value of the G(n) score
    '''
    def unloadTimeFunction(self, row, column):
        # Check the crane's prev location
        if self.craneLocation != (0,0):
            # If the crane's prev location is (0,0), then the crane is at the ship's location
            craneTime = self.craneTimeFunction(column)

            res += craneTime

        # Calculaing the time take to move from the initial position onto the truck
        # Calculating the time to get to 9 high
        rowTot =  8 - row

        # Calculatin ghte time to get to the 0th col
        colTot = column

        # The time taken to got from the ship to the truck is 2 units/minutes
        shipToTruck = 2


        # Final result
        res = rowTot + colTot + shipToTruck

        if self.craneLocation == (0,0):
            # Double the result to add the time taken by the crane
            res *= 2
        
        return res




