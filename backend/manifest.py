# For Frontend:
from .ship import Ship

# For backend:
# from ship import Ship

import re

class Manifest:
    def __init__(self, positions=[], weights=[], msgs=[]):
        self.positions = positions
        self.weights = weights
        self.msgs = msgs

    def read_manifest(self, filename):
        
        ship = Ship()
        
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:

                # Regex used to extract the different aspects of information from a line, here's a breakdown:
                    # \[([^\]]+)\] matches the row and column values in the bay
                    # \{([^}]+)\} matches the weight
                    # (.*) matches the message
                pattern = re.compile(r'\[([^\]]+)\],\s*\{([^}]+)\},\s*(.*)')

                # Find the matches in the line
                matches = re.match(pattern, line)

                # Check if there is a match
                if matches:
                    # Extract the row, column, weight, and message
                    row_column_content = matches.group(1)
                    weight_content = matches.group(2)
                    message_content = matches.group(3)

                    # Process row and column content
                    row_column_parts = [part.strip() for part in row_column_content.split(',')]
                    row, column = row_column_parts

                    # Process weight content
                    weight = weight_content.strip()

                    # Process message content
                    message = message_content.strip()

                    # Setting the final variables to the appropriate format
                    row = int(row)
                    column = int(column)
                    value = (int(weight), message)
                    
                    # (Testing) Now you have separate variables for row, column, weight, and message
                    # print("Row:", int(row))
                    # print("Column:", int(column))
                    # print("Weight:", int(weight))
                    # print("Message:", message)
                else:
                    # Error clause for mistakes in the manifest
                    print("No match found in the line.")

                # Assigning manifest values to the ship's bay
                # Rows and columns are offset to have the first row and column be 0
                ship.set_value(row-1, column-1, value=value)

        # Set all the column heights of the newly created ship
        ship.calculateColHeight()
        
        # Returning the newly assigned Ship object
        return ship

    def write_manifest(self, ship, filename):
        if ship is None:
            print("Wrong variable passed in or empty manifest!!")
        
        filename = filename[:-4]

        filename = filename + "_OUTBOUND.txt"

        with open(filename, 'w') as f:
            
            # The extra row is eliminated since it is not part of the ship's bay
            for i in range(ship.r - 1):
                for j in range(ship.c):
                    value = ship.get_value(i,j)

                    # Rows and columns must be changed back to their original offset
                    f.write("[" + "{:02d}".format(i+1) + "," + "{:02d}".format(j+1) + "], "
                            + "{" + "{:05d}".format(value[0]) + "}, " + value[1] + "\n")

                
    def print_manifest(self):
        for i in range(len(self.positions)):
            print(self.positions[i], self.weights[i], self.msgs[i])