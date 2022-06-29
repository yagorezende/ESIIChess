#! python
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
from enum import Enum, auto
from typing import Dict, List, Set

import tests.logic.board as tlb


class TestSuites(Enum):
    SMOKE_TESTING = auto()
    BOARD_POSITIONS = auto()


_suites: Dict[TestSuites, List[unittest.TestCase]] = {
    TestSuites.SMOKE_TESTING: [],
    TestSuites.BOARD_POSITIONS: [
        tlb.TestBoardLogic('test_king_positions'),
        tlb.TestBoardLogic('test_queen_positions'),
        tlb.TestBoardLogic('test_rook_positions'),
        tlb.TestBoardLogic('test_bishop_positions'),
        tlb.TestBoardLogic('test_knight_positions'),
        tlb.TestBoardLogic('test_pawn_positions')
    ]
}

def main(argv):
    runner = unittest.TextTestRunner()
    tests = unittest.TestSuite()
    desired_test_suites: Set[TestSuites] = set()
    not_found_test_suites: Set[str] = set()
    # -----   -----
    for suite_name in argv:
        upper_name = suite_name.upper()
        try:
            desired_test_suites.add(TestSuites[upper_name])
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
