import unittest
from typing import Dict, List, NamedTuple, Tuple, Union

import tests.test_suites as ts

import logic.referee


class TestCheckThreatInput(NamedTuple):  # TODO
    pos: Tuple[int, int]
    turn_color: str
    board_matrix: List[List[Union[str, None]]]


class TestReferee(unittest.TestCase):
    def setUp(self) -> None:
        self.referee = logic.referee.Referee([], {}, 'w')
        return None

    def tearDown(self) -> None:
        self.referee = None
        return None

    def test_check_threat(self) -> None:
        # --- SECTION - CONFIGURATION
        runs: List[Tuple[bool, TestCheckThreatInput]] = []
        # NOTE (0) - test not beeing threatened
        runs.append((
            False,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None]*8,
                    ['bp1', *[None]*7],
                    [None]*8,
                    [None, 'wp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8])))
        # # NOTE (1) - test beeing threatened by a black pawn
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='w',
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    ['bp1', *[None]*7],
                    [None, 'wp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8])))
        # # NOTE (2) - test beeing threatened by a white pawn
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None, 'bp2', *[None]*6],
                    ['wp1', *[None]*7],
                    [None]*8,
                    [None]*8,
                    [None]*8])))
        # NOTE (3) - test beeing threatened by a white rook
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None, 'wr1', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None, 'bp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8])))
        # NOTE (4) - test beeing threatened by a white bishop
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None, 'bp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [*[None]*5, 'wb6', *[None]*2]])))
        # NOTE (5) - test beeing threatened by a white knight
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None, 'bp2', *[None]*6],
                    [None]*8,
                    ['wn2', *[None]*7],
                    [None]*8,
                    [None]*8])))
        # NOTE (6) - test beeing threatened by a white queen
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None, 'bp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None, 'wq', *[None]*6],
                    [None]*8])))
        # NOTE (7) - test beeing threatened by a white king
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    ['wk4', 'bp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8])))
        # --- !SECTION - CONFIGURATION
        # --- SECTION - TEST
        for i, (expected, input_config) in enumerate(runs):
            with self.subTest(i=i):
                self.referee.board_matrix = input_config.board_matrix
                self.referee.turn_color = input_config.turn_color
                # --- SECTION - beeing tested
                result = self.referee.check_threat(pos=input_config.pos)
                # --- !SECTION - beeing tested
                self.assertEqual(expected, result)
        # --- !SECTION - TEST
        return None


def suites() -> Dict[ts.TestSuites, List[unittest.TestCase]]:
    return {
        ts.TestSuites.GAME_LOGIC: [
            TestReferee('test_check_threat')],
    }
