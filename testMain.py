import unittest
from tests.logic.board import TestBoardLogic

_app_tests_suites = {
    'board_logic_tests_positions':[
        TestBoardLogic('test_king_positions'),
        TestBoardLogic('test_queen_positions'),
        TestBoardLogic('test_rook_positions'),
        TestBoardLogic('test_bishop_positions'),
        TestBoardLogic('test_knight_positions'),
        TestBoardLogic('test_pawn_positions')
    ]
}

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    suite  = unittest.TestSuite()
    tests  = []
    desired_test = ''
    try:
        tests = _app_tests_suites[desired_test]
    except KeyError:
        for tests_list in _app_tests_suites.values():
            tests.extend(tests_list)
    suite.addTests(tests)
    runner.run(suite)
