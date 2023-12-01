# Mainly used for testing, will be changed later based on the database's API
from ship import Ship
import manifest
import lualgorithm
import balancingAlg

def main():
    test_filename = "ShipCase4.txt"
    # test_filename = "Voyager_Capt_King.txt"


    testManifest = manifest.Manifest()
    new_ship = testManifest.read_manifest(test_filename)
    new_ship.print_bay()

    # new_ship.set_value(5, 4, (100, "Test"))
    
    # testManifest.write_manifest(new_ship, test_filename)

    # neighbors = lualgorithm.neighbors((1,2), new_ship)
    
    print()
    print()
    
    print(new_ship.colHeight)
    
    # print("Neighbors:", neighbors)

    res = balancingAlg.ucs(new_ship)

    res.print_bay()

if __name__ == "__main__":
    main()