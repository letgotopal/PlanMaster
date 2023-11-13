class Ship:
    '''
    @function: constructor for the Ship class
    @param self: the Ship object
    @param r: the number of rows on the ship
    @param c: the number of columns on the ship
    @param bay: the 2D array representing the ship's bay. MUST BE SUPPLIED BY THE MANIFEST ORDER TO SUCCESSFULLY DISPLAY THE ORDER
    @return: a Ship object
    '''
    def __init__(self, r=8, c=12, bay=None):
        self.r = r
        self.c = c
        self.bay = bay or [["NAN" for j in range(c)] for i in range(r)]

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
    @param i: the row of the cell
    @param j: the column of the cell
    @param value: the value to set the cell to
    @return: None
    '''
    def set_value(self, i, j, value):
        self.bay[i][j] = value

    '''
    @function: gets the value of a cell in the ship's bay
    @param self: the Ship object
    @param i: the row of the cell
    @param j: the column of the cell
    @return: the value of the cell
    '''
    def get_value(self, i, j):
        return self.bay[i][j]