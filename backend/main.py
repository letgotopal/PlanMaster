# Mainly used for testing, will be changed later based on the database's API
import manifest

def main():
    test_filename = "Voyager_Capt_King.txt"

    testManifest = manifest.Manifest()
    new_ship = testManifest.read_manifest(test_filename)
    new_ship.print_bay()

    new_ship.set_value(5, 4, (100, "Test"))
    
    testManifest.write_manifest(new_ship, test_filename)

if __name__ == "__main__":
    main()