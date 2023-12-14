from .ship import Ship
from .operations import loadOperation

# Here, our goal test is to check if the all the containers have been loaded
# i.e. if the loadList is empty


'''
@function: Interative load algorithm
@param ship: the Ship object
@param loadList: the list of containers to load
@return: the ship object with the containers loaded
'''

def load(ship, loadList):
    while len(loadList) != 0:
        container = loadList.pop(0)
        ship = loadOperation(ship, container)
        if isinstance(ship, int):
            return "ERROR: Loading failed/interrupted"
    return ship