"""
To run tests:
python -B ./testMain.py [suite1 ]...

To run test and coverage tool:
python -B -m coverage run ./testMain.py

To see coverage report on terminal:
python -m coverage report

To generate coverage lcov file:
python -m coverage lcov
"""

import sys
import unittest
from typing import Dict, List, Set

import tests.logic.board as tlb
import tests.test_suites as ts

_suites: Dict[ts.TestSuites, Set[unittest.TestCase]] = {}
# NOTE - gather tests from modules
_suites_list: List[Dict[ts.TestSuites, List[unittest.TestCase]]] = []
# NOTE - extend _suites with _suites_list
for d in _suites_list:
    for suite, tests in d.items():
        if suite not in _suites:
            _suites[suite] = set()
        _suites[suite].update(tests)


def main(argv):
    runner = unittest.TextTestRunner(verbosity=2)
    tests = unittest.TestSuite()
    desired_test_suites: Set[ts.TestSuites] = set()
    not_found_test_suites: Set[str] = set()
    # -----   -----
    for suite_name in argv:
        upper_name = suite_name.upper()
        try:
            desired_test_suites.add(ts.TestSuites[upper_name])
        except KeyError:
            not_found_test_suites.add(suite_name)
    # -----   -----
    if len(desired_test_suites) == 0:
        for s in _suites:
            desired_test_suites.add(s)
    # -----   -----
    for dts in desired_test_suites:
        tests.addTests(_suites[dts])
    runner.run(tests)
    # -----   -----
    if len(not_found_test_suites) > 0:
        print(
            f"""\n{'+'*70}\nSUITE(S) NOT FOUND:\n{not_found_test_suites}\n""")


if __name__ == "__main__":
    main(sys.argv[1:])
