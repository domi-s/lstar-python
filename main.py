import argparse
import unittest

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--large", action="store_true",
                        help="also learn and check the large DFA cases")
    args = parser.parse_args()

    suite = unittest.defaultTestLoader.discover("tests")
    if args.large:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(
            "tests.large_dfas"
        ))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(not result.wasSuccessful())
