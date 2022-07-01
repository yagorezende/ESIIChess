import unittest
import unittest.mock as mock
from typing import Dict, List, Literal, NamedTuple, Tuple, Union

import tests.test_suites as ts
import ui.board

import logic.referee


class TestTurnConfig(NamedTuple):
    turn_color: str
    k_pawn1: str
    pawn1_exist: bool
    pawn1_active: bool
    pawn1_has_jumped: bool
    k_pawn2: str
    pawn2_exist: bool
    pawn2_active: bool
    pawn2_has_jumped: bool
    pieces: Dict[str, ui.board.ChessPiece]


class TestTurnResult(NamedTuple):
    turn_color: str
    pawn1_exist: bool
    pawn1_active: Union[bool, None]
    pawn1_has_jumped: Union[bool, None]
    pawn2_exist: bool
    pawn2_active: Union[bool, None]
    pawn2_has_jumped: Union[bool, None]


class MatInsufPieceInput(NamedTuple):
    id: int
    type: str
    color: str
    active: bool
    row: int
    column: int


class TestReferee(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.referee = None

    def setUp(self) -> None:
        """
        Called before each test method to set up something
        """
        # mock = unittest.mock.create_autospec()
        self.referee = logic.referee.Referee([], {}, 'w')
        return None

    def tearDown(self) -> None:
        """
        Called to do something after each test method
        """
        self.referee = None
        return None

    def test_turn(self) -> None:
        # NOTE - Change turn to oponent and also prevent en passants out of the right turn.
        # SECTION - CONFIGURE TEST
        runs: List[Tuple[TestTurnResult, TestTurnConfig]] = []
        # NOTE (0): - w -> b; without a b pawn;
        runs.append((
            # NOTE - expected
            TestTurnResult(
                'b',
                pawn1_exist=False, pawn1_active=None, pawn1_has_jumped=None,
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='w',
                k_pawn1='bp1',
                pawn1_exist=False, pawn1_active=False, pawn1_has_jumped=False,
                k_pawn2='wp1',
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True,
                pieces=self._test_turn_load_pieces([
                    [None] * 8,
                    [None] * 8,
                    [None] * 8,
                    [None, 'bp1', *[None]*6],
                    [None] * 8,
                    [None] * 8,
                    ['wp1', *[None] * 7],
                    [None] * 8]))
        ))
        # NOTE (1): w -> b; with a b pawn active;
        runs.append((
            # NOTE - expected
            TestTurnResult(
                'b',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=False,
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='w',
                k_pawn1='bp1',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=False,
                k_pawn2='wp1',
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True,
                pieces=self._test_turn_load_pieces([
                    [None] * 8,
                    [None] * 8,
                    [None] * 8,
                    [None, 'bp1', *[None]*6],
                    [None] * 8,
                    [None] * 8,
                    ['wp1', *[None] * 7],
                    [None] * 8]))
        ))
        # NOTE (2): w -> b; with a b pawn active and has jumped;
        runs.append((
            # NOTE - expected
            TestTurnResult(
                'b',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=False,
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='w',
                k_pawn1='bp1',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                k_pawn2='wp1',
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True,
                pieces=self._test_turn_load_pieces([
                    [None] * 8,
                    [None] * 8,
                    [None] * 8,
                    [None, 'bp1', *[None]*6],
                    [None] * 8,
                    [None] * 8,
                    ['wp1', *[None] * 7],
                    [None] * 8]))
        ))
        # NOTE (3): b -> w; without a w pawn
        runs.append((
            # NOTE - expected
            TestTurnResult(
                'w',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                pawn2_exist=False, pawn2_active=None, pawn2_has_jumped=None),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='b',
                k_pawn1='bp1',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                k_pawn2='wp1',
                pawn2_exist=False, pawn2_active=False, pawn2_has_jumped=False,
                pieces=self._test_turn_load_pieces([
                    [None] * 8,
                    [None] * 8,
                    [None] * 8,
                    [None, 'bp1', *[None]*6],
                    [None] * 8,
                    [None] * 8,
                    ['wp1', *[None] * 7],
                    [None] * 8]))
        ))
        # NOTE (4): b -> w; with a w pawn active
        runs.append((
            # NOTE - expected
            TestTurnResult(
                'w',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=False),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='b',
                k_pawn1='bp1',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                k_pawn2='wp1',
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=False,
                pieces=self._test_turn_load_pieces([
                    [None] * 8,
                    [None] * 8,
                    [None] * 8,
                    [None, 'bp1', *[None]*6],
                    [None] * 8,
                    [None] * 8,
                    ['wp1', *[None] * 7],
                    [None] * 8]))
        ))
        # NOTE (5): b -> w; with a w pawn active and has jumped
        runs.append((
            # NOTE - expected
            TestTurnResult(
                'w',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=False),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='b',
                k_pawn1='bp1',
                pawn1_exist=True, pawn1_active=True, pawn1_has_jumped=True,
                k_pawn2='wp1',
                pawn2_exist=True, pawn2_active=True, pawn2_has_jumped=True,
                pieces=self._test_turn_load_pieces([
                    [None] * 8,
                    [None] * 8,
                    [None] * 8,
                    [None, 'bp1', *[None]*6],
                    [None] * 8,
                    [None] * 8,
                    ['wp1', *[None] * 7],
                    [None] * 8]))
        ))

    # !SECTION - CONFIGURE TEST
    # SECTION - TEST
        # STUB - self.referee.update_status
        with mock.patch.object(self.referee, 'update_status') as update_status_mock:
            update_status_mock.return_value = None
            for i in range(len(runs)):
                with self.subTest(i=i):
                    self._configure_test_turn(runs[i][1])
                # SECTION - beeing tested
                    self.referee.turn()
                # !SECTION
                    result = self._get_test_turn_result(
                        runs[i][1].k_pawn1, runs[i][1].k_pawn2)
                    self.assertEqual(result, runs[i][0])  # NOTE - compare
    # !SECTION - TEST
        return None

    def _test_turn_load_pieces(self, board: List[List[Union[str, None]]]) -> Dict[str, ui.board.ChessPiece]:
        """
        Load stubs to replace ChessPieces.
        """
        pieces = {}
        for row in board:
            for piece in row:
                if piece:
                    # STUB - ui.board.ChessPiece
                    piece_mock = mock.create_autospec(
                        ui.board.ChessPiece, color=piece[0], type=piece[1])
                    # NOTE - default values for piece
                    piece_mock.active = True
                    piece_mock.has_jumped = False
                    pieces[piece] = piece_mock
        return pieces

    def _configure_test_turn(self, config: TestTurnConfig) -> None:
        """
        Change referee attributes that influence which independent path is taken
        when running `turn` method.
        """
        self.referee.turn_color = config.turn_color
        self.referee.pieces = config.pieces

        pawn1 = self.referee.pieces[config.k_pawn1]
        pawn1.active = config.pawn1_active
        pawn1.has_jumped = config.pawn1_has_jumped
        if not config.pawn1_exist:
            self.referee.pieces.pop(config.k_pawn1, None)

        pawn2 = self.referee.pieces[config.k_pawn2]
        pawn2.active = config.pawn2_active
        pawn2.has_jumped = config.pawn2_has_jumped
        if not config.pawn2_exist:
            self.referee.pieces.pop(config.k_pawn2, None)

    def _get_test_turn_result(self, k_pawn1: str, k_pawn2: str) -> TestTurnResult:
        """
        Aggregate the atributes that `turn` method touch.
        """
        result_pawn1 = self.referee.pieces.get(k_pawn1)
        result_pawn2 = self.referee.pieces.get(k_pawn2)
        return TestTurnResult(
            turn_color=self.referee.turn_color,
            pawn1_exist=True if result_pawn1 else False,
            pawn1_active=result_pawn1.active if result_pawn1 else None,
            pawn1_has_jumped=result_pawn1.has_jumped if result_pawn1 else None,
            pawn2_exist=True if result_pawn2 else False,
            pawn2_active=result_pawn2.active if result_pawn2 else None,
            pawn2_has_jumped=result_pawn2.has_jumped if result_pawn2 else None)

    def test_material_insufficiency(self) -> None:
        # SECTION - CONFIGURE TEST
        runs: List[Tuple[bool, List[MatInsufPieceInput]]] = []
        # NOTE (0): empty board
        runs.append((False, []))
        # NOTE (1): exists a pawn
        runs.append((
            False,
            [MatInsufPieceInput(
                id=8, type='p', color='w', active=True, row=1, column=8),
             MatInsufPieceInput(
                id=5, type='k', color='w', active=True, row=2, column=2),
             MatInsufPieceInput(
                id=5, type='k', color='b', active=True, row=5, column=2)]))
        # NOTE (2): exists a rook
        runs.append((
            False,
            [MatInsufPieceInput(
                id=1, type='r', color='w', active=True, row=3, column=0),
             MatInsufPieceInput(
                id=5, type='k', color='w', active=True, row=2, column=2),
             MatInsufPieceInput(
                id=5, type='k', color='b', active=True, row=5, column=2)]))
        # NOTE (3): exists a queen
        runs.append((
            False,
            [MatInsufPieceInput(
                id=4, type='q', color='w', active=True, row=7, column=8),
             MatInsufPieceInput(
                id=5, type='k', color='w', active=True, row=2, column=2),
             MatInsufPieceInput(
                id=5, type='k', color='b', active=True, row=5, column=2)]))
        # NOTE (4): wk vs bk
        runs.append((
            True,
            [MatInsufPieceInput(
                id=5, type='k', color='w', active=True, row=2, column=2),
             MatInsufPieceInput(
                id=5, type='k', color='b', active=True, row=5, column=2)]))
        # NOTE (5): wk vs bk, bb  TODO
        runs.append((
            False,
            [MatInsufPieceInput(
                id=5, type='k', color='w', active=True, row=2, column=2),
             MatInsufPieceInput(
                id=5, type='k', color='b', active=True, row=5, column=2),
             MatInsufPieceInput(
                id=4, type='q', color='w', active=True, row=7, column=8)]))
        # NOTE (6): wk, wb vs bk  TODO
        runs.append((
            False,
            [MatInsufPieceInput(
                id=5, type='k', color='w', active=True, row=2, column=2),
             MatInsufPieceInput(
                id=5, type='k', color='b', active=True, row=5, column=2),
             MatInsufPieceInput(
                id=4, type='q', color='w', active=True, row=7, column=8)]))

    # !SECTION - CONFIGURE TEST
    # SECTION - TEST
        for i in range(len(runs)):
            with self.subTest(i=i):
                expected = runs[i][0]
                self.referee.pieces = self._mat_insuf_load_pieces(runs[i][1])
                self.referee.board_matrix = runs[i][1]
                result = self.referee.check_material_insufficiency()
                self.assertEqual(result, expected)
    # !SECTION - TEST
        return None

    def _mat_insuf_load_piece(self, pieces: List[MatInsufPieceInput]) -> Dict[str, ui.board.ChessPiece]:
        d: Dict[str, ui.board.ChessPiece] = {}
        for p in pieces:
            # STUB - ui.board.ChessPiece
            piece_mock = mock.create_autospec(
                ui.board.ChessPiece, color=p.color, type=p.type)
            piece_mock.active = True
            piece_mock.type = p.type
            piece_mock.get_board_pos = (p.row, p.column)
            piece_mock.get_square_color = 'w' if (
                p.row*8+p.column) % 2 else 'b'
            d[f'{p.color}{p.type}{p.id}'] = piece_mock
        return d


def suites() -> Dict[ts.TestSuites, List[unittest.TestCase]]:
    return {
        ts.TestSuites.GAME_LOGIC: [TestReferee('test_turn')],
        ts.TestSuites.GAME_TIES: [TestReferee('test_material_insufficiency')]
    }
