# Mainly used for testing, will be changed later based on the database's API
from ship import Ship
import manifest
import luAlg
import balancingAlg
import loadAlg
import siftAlg

def main():
    test_filename = "ShipCase4.txt"


    testManifest = manifest.Manifest()
    new_ship = testManifest.read_manifest(test_filename)
    new_ship.print_bay()

    # new_ship.set_value(5, 4, (100, "Test"))
    
    # testManifest.write_manifest(new_ship, test_filename)

    # neighbors = lualgorithm.neighbors((1,2), new_ship)
    
    print()
    print()

    # Testing the sift's goal builder algorithm
    # new_ship = siftAlg.ucs(new_ship)
    new_ship.print_bay()        
    # print("Neighbors:", neighbors)

    # res = balancingAlg.ucs(new_ship)

    res = loadAlg.load(new_ship, [(100, 'test1'), (100, 'test2'), (100, 'test3'), (100, 'test4'), (100, 'test5'), (100, 'test6'), (100, 'test7'), (100, 'test8'),
                                  (100, 'test11'), (100, 'test12'), (100, 'test13'), (100, 'test14'), (100, 'test15'), (100, 'test16'), (100, 'test17'), (100, 'test18'),
                                  (100, 'test21'), (100, 'test22'), (100, 'test23'), (100, 'test24'), (100, 'test25'), (100, 'test26'), (100, 'test27'), (100, 'test28')])
    
    # res = luAlg.ucs(new_ship, [(6,4), (5,4)])

    print(res)
    print("The final ship's G(n) is: ", res.gn, "and it's crane values are: ", res.craneLocation)
    print("The ship's col heights are: ", res.colHeight)
    print("The final move was: ", res.lastMove)
    res.print_bay()
    
    while(type(res.parent) != type(None)):
        res = res.parent
        print("The parent's G(n) is: ", res.gn, "and it's crane values are: ", res.craneLocation)
        print("The parent's col heights are: ", res.colHeight)
        print("The move was: ", res.lastMove)
        res.print_bay()
    
if __name__ == "__main__":
    main()