
# trace path from start ship to end ship
def trace(ship):
    path = []
    while not ship is None:
        path.append(ship)
        ship = ship.parent
    return reversed(path)