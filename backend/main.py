# Mainly used for testing, could be changed later
from ship import Ship

def main():
    testShip = Ship()
    testShip.print_bay()

    testShip.set_value(0, 0, "Walmart - Adult bicycles (Call Sue from office)")

    testShip.print_bay()

if __name__ == "__main__":
    main()