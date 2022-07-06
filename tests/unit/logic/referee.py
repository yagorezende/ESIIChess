import unittest
import unittest.mock as mock
from typing import Callable, Dict, List, NamedTuple, Tuple, Union

import tests.test_suites as ts
import ui.board

import logic.referee


class TestTurnConfig(NamedTuple):
    turn_color: str
    turn_counter: int
    rushed_pawn: Union[Tuple[int, int], None]
    board: List[List[Union[str, None]]]


class TestTurnResult(NamedTuple):
    turn_color: str
    turn_counter: int
    rushed_pawn: Union[Tuple[int, int], None]


class TestMatInsufInput(NamedTuple):
    id: int
    type: str
    color: str
    active: bool
    row: int
    column: int


class TestCheckThreatInput(NamedTuple):
    pos: Tuple[int, int]
    turn_color: str
    # NOTE - bool(turn_color == bottom_color)
    bottomup_orientation: Callable[[], bool]
    board_matrix: List[List[Union[str, None]]]


class TestGetKingMovesInput(NamedTuple):
    pos: Tuple[int, int]
    turn_color: str
    enemy_color: str
    king_moved: bool
    king_threatened: List[bool]
    get_delta_moves: List[Tuple[int, int]]
    board: List[List[Union[str, None]]]


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

    def _check_enemy_presence(self, pos: Tuple[int, int]) -> bool:
        enemy_color = 'w'
        if self.referee.turn_color == 'w':
            enemy_color = 'b'
        # NOTE - pos[0] is inside rows
        cond = (0 <= pos[0] < 8)
        # NOTE - pos[0] is inside colums
        cond = cond and (0 <= pos[1] < 8)
        # NOTE - pos is not empty
        cond = cond and self.referee.board_matrix[pos[0]][pos[1]] is not None
        # NOTE - piece on pos have the enemy color
        cond = cond and \
            self.referee.board_matrix[pos[0]][pos[1]][0] == enemy_color
        return cond

    def _check_void(self, pos) -> bool:
        cond = 0 <= pos[0] < 8
        cond = cond and 0 <= pos[1] < 8
        cond = cond and not self.referee.board_matrix[pos[0]][pos[1]]
        return cond

    def _add_tuples(self, t0, t1) -> Tuple[int, int]:
        return (t0[0]+t1[0], t0[1]+t1[1])

    def test_turn(self) -> None:
        # NOTE - Change turn to oponent and also prevent en passants out of the right turn.
        # --- SECTION - CONFIGURE TEST
        runs: List[Tuple[TestTurnResult, TestTurnConfig]] = []
        # NOTE (0): - b -> w; without rushed pawn
        runs.append((
            # NOTE - expected
            TestTurnResult(
                turn_color='w',
                turn_counter=1,
                rushed_pawn=None),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='b',
                turn_counter=0,
                rushed_pawn=None,
                board=[[None]*8]*8)
        ))
        # NOTE (1): - w -> b; without rushed pawn
        runs.append((
            # NOTE - expected
            TestTurnResult(
                turn_color='b',
                turn_counter=1,
                rushed_pawn=None),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='w',
                turn_counter=0,
                rushed_pawn=None,
                board=[[None]*8]*8)
        ))
        # NOTE (2): - w -> b; with rushed_pawn, board[*rushed_pawn]==None
        runs.append((
            # NOTE - expected
            TestTurnResult(
                turn_color='b',
                turn_counter=1,
                rushed_pawn=None),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='w',
                turn_counter=0,
                rushed_pawn=(0, 1),
                board=[[None]*8]*8)
        ))
        # NOTE (3): - w -> b; with rushed_pawn, board[*rushed_pawn]=='bp2'
        runs.append((
            # NOTE - expected
            TestTurnResult(
                turn_color='b',
                turn_counter=1,
                rushed_pawn=None),
            # NOTE - "params"
            TestTurnConfig(
                turn_color='w',
                turn_counter=0,
                rushed_pawn=(3, 1),
                board=[
                    [None]*8, [None]*8, [None]*8,
                    [None, 'bp2', None, None, None, None, None, None],
                    [None]*8, [None]*8, [None]*8, [None]*8])
        ))
    # --- !SECTION - CONFIGURE TEST
    # --- SECTION - TEST
        # STUB - self.referee.update_status
        with mock.patch.multiple(
                self.referee, spec=True,
                update_status=lambda: None,
                enemy_color=lambda: 'b'if self.referee.turn_color == 'w' else 'w'):
            for i in range(len(runs)):
                with self.subTest(i=i):
                    self._configure_test_turn(runs[i][1])
                # --- SECTION - beeing tested
                    self.referee.turn()
                # --- !SECTION
                    result = TestTurnResult(
                        turn_color=self.referee.turn_color,
                        turn_counter=self.referee.turn_counter,
                        rushed_pawn=self.referee.rushed_pawn)
                    self.assertEqual(result, runs[i][0])  # NOTE - compare
    # --- !SECTION - TEST
        return None

    def _configure_test_turn(self, config: TestTurnConfig) -> None:
        self.referee.turn_color = config.turn_color
        self.referee.turn_counter = config.turn_counter
        self.referee.rushed_pawn = config.rushed_pawn
        self.referee.board_matrix = config.board

    def test_check_material_insufficiency(self) -> None:
        # --- SECTION - CONFIGURATIONS
        runs: List[Tuple[bool, List[TestMatInsufInput]]] = []
        # NOTE (0): empty board
        runs.append((False, []))
        # NOTE (1): exists a pawn
        runs.append((
            False,
            [TestMatInsufInput(
                id=8, color='w', type='p', active=True, row=1, column=7),
             TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2)]))
        # NOTE (2): exists a rook
        runs.append((
            False,
            [TestMatInsufInput(
                id=1, color='w', type='r', active=True, row=3, column=0),
             TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2)]))
        # NOTE (3): exists a queen
        runs.append((
            False,
            [TestMatInsufInput(
                id=4, color='w', type='q', active=True, row=7, column=7),
             TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2)]))
        # NOTE (4): wk vs bk
        runs.append((
            True,
            [TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2)]))
        # NOTE (5): wk vs bk, bb
        runs.append((
            True,
            [TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2),
             TestMatInsufInput(
                id=0, color='b', type='b', active=True, row=7, column=7)]))
        # NOTE (6): wk, wb vs bk
        runs.append((
            True,
            [TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=0, color='w', type='b', active=True, row=0, column=7),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2)
             ]))
        # NOTE (7): wk vs bk, bn
        runs.append((
            True,
            [TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2),
             TestMatInsufInput(
                id=0, color='b', type='n', active=True, row=7, column=7)]))
        # NOTE (8): wk, wn vs bk
        runs.append((
            True,
            [TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=0, color='w', type='n', active=True, row=0, column=7),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2)
             ]))
        # NOTE (9): wk, wb vs bk, bb
        runs.append((
            True,
            [TestMatInsufInput(
                id=5, color='w', type='k', active=True, row=2, column=2),
             TestMatInsufInput(
                id=0, color='w', type='b', active=True, row=0, column=7),
             TestMatInsufInput(
                id=5, color='b', type='k', active=True, row=5, column=2),
             TestMatInsufInput(
                id=0, color='b', type='b', active=True, row=7, column=0)]))
        # --- !SECTION - CONFIGURATIONS
        # --- SECTION - TEST
        for i, (expected, input_pieces) in enumerate(runs):
            # NOTE - test material insuficiency in multiple runs
            # NOTE - patch referee method that is not beeing tested with a stub
            with self.subTest(i=i), mock.patch.object(logic.referee.Referee, 'get_square_color') as get_square_color:
                get_square_color.side_effect = \
                    lambda p: 'b' if (p[0] % 2+p[0]*8+p[1]) % 2 else 'w'
                self.referee.pieces = self._mat_insuf_load_pieces(input_pieces)
                self.referee.board_matrix = self._mat_insuf_load_board(
                    self.referee.pieces)
            # --- SECTION - beeing tested
                result = self.referee.check_material_insufficiency()
            # --- !SECTION - beeing tested
                self.assertEqual(result, expected)
        # --- !SECTION - TEST
        return None

    def _mat_insuf_load_pieces(self, pieces: List[TestMatInsufInput]) -> Dict[str, ui.board.ChessPiece]:
        d: Dict[str, ui.board.ChessPiece] = {}
        for p in pieces:
            # STUB - ui.board.ChessPiece
            piece_mock = mock.create_autospec(
                spec=ui.board.ChessPiece, color=p.color, type=p.type)
            piece_mock.active = True
            piece_mock.type = p.type
            piece_mock.get_board_pos.return_value = (p.row, p.column)
            d[f'{p.color}{p.type}{str(p.id)}'] = piece_mock
        return d

    def _mat_insuf_load_board(self, pieces: Dict[str, ui.board.ChessPiece]):
        board = []
        for _ in range(8):
            board.append([None]*8)
        for k_piece, piece in pieces.items():
            r, c = piece.get_board_pos()
            board[r][c] = k_piece
        return board

    def test_check_threat(self) -> None:
        # --- SECTION - CONFIGURATION
        runs: List[Tuple[bool, TestCheckThreatInput]] = []
        # NOTE (0) - test not beeing threatened
        runs.append((
            False,
            TestCheckThreatInput(
                pos=(3, 1),
                turn_color='b',
                bottomup_orientation=lambda: False,
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
                bottomup_orientation=lambda: True,
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
                bottomup_orientation=lambda: False,
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
                bottomup_orientation=lambda: False,
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
                bottomup_orientation=lambda: False,
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
                bottomup_orientation=lambda: False,
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
                bottomup_orientation=lambda: False,
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
                bottomup_orientation=lambda: False,
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
            with self.subTest(i=i), \
                    mock.patch(
                        'logic.referee.add_tuples',
                        spec=logic.referee.add_tuples) as add_tuples, \
                    mock.patch.multiple(
                        self.referee,
                        spec=True,
                        # SECTION - patch referee methods
                        bottomup_orientation=input_config.bottomup_orientation,
                        check_enemy_presence=self._check_enemy_presence,
                        check_void=self._check_void):
                # --- !SECTION
                self.referee.board_matrix = input_config.board_matrix
                self.referee.turn_color = input_config.turn_color
                add_tuples.side_effect = self._add_tuples
                # --- SECTION - beeing tested
                result = self.referee.check_threat(
                    pos=input_config.pos)  # ,
                # enemy_color=input_config.enemy_color)
                # --- !SECTION - beeing tested
                self.assertEqual(expected, result)
        # --- !SECTION - TEST
        return None

    def test_get_king_moves(self) -> None:
        # --- SECTION - CONFIGURATIONS
        runs: List[Tuple[List[Tuple[int, int]], TestGetKingMovesInput]] = []
        # NOTE () - king threatened
        board = [[]]
        moves = [(7, 3), (6, 3), (6, 4), (6, 5), (7, 5)]
        runs.append((
            moves,
            TestGetKingMovesInput(
                pos=(7, 4),
                turn_color='w',
                enemy_color='b',
                king_moved=True,
                king_threatened=[True],
                get_delta_moves=moves,
                board=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None, None, None, None, 'wk5', None, None, None]
                ])))
        # NOTE () - king not threatened, but moved
        moves = [(7, 3), (6, 3), (6, 4), (6, 5), (7, 5)]
        runs.append((
            moves,
            TestGetKingMovesInput(
                pos=(7, 4),
                turn_color='w',
                enemy_color='b',
                king_moved=True,
                king_threatened=[False, False, False,
                    True, False, False, False, True],
                get_delta_moves=moves,
                board=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    ['wr1', None, None, None, 'wk5', None, None, 'wr8']
                ])))
        # NOTE () - king not threatened, but moved
        moves = [(7, 3), (6, 3), (6, 4), (6, 5), (7, 5)]
        runs.append((
            moves,
            TestGetKingMovesInput(
                pos=(7, 4),
                turn_color='w',
                enemy_color='b',
                king_moved=False,
                king_threatened=[False, False, False, False, False, False],
                get_delta_moves=moves,
                board=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    ['wr1', None, None, None, 'wk5', None, None, 'wr8']
                ])))
        # --- !SECTION - CONFIGURATIONS
        # --- SECTION - TEST
        for i, (expected, input_config) in enumerate(runs):
            with self.subTest(i=i), \
                mock.patch.multiple(
                    self.referee, spec=True,
                    get_delta_moves=lambda pos, full_type: input_config.get_delta_moves,
                    enemy_color=lambda: input_config.enemy_color,
                    check_threat=mock.DEFAULT,
                    check_void=self._check_void) as mocks:
                mocks['check_threat'].side_effect = input_config.king_threatened
                self.referee.turn_color = input_config.turn_color
                self.referee.board_matrix = input_config.board
                self.referee.pieces = self._test_get_king_moves_load_pieces(
                    input_config)
                # --- SECTION - beeing tested
                result = self.referee.get_king_moves(input_config.pos)
                # --- !SECTION - beeing tested
                self.assertEqual(set(expected), set(result))
        # --- !SECTION - TEST
        return None

    def _test_get_king_moves_load_pieces(self, input_config: TestGetKingMovesInput) -> Dict[str, ui.board.ChessPiece]:
        pieces = {}
        for row in input_config.board:
            for k_piece in row:
                if k_piece:
                    # STUB - ui.board.ChessPiece
                    piece_mock = mock.create_autospec(
                        ui.board.ChessPiece, color=k_piece[0], type=k_piece[1])
                    # NOTE - default values for piece
                    if k_piece[0] == input_config.turn_color:
                        piece_mock.has_moved = input_config.king_moved
                    else:
                        piece_mock.has_moved = False
                        piece_mock.color = k_piece[0]
                        piece_mock.type = k_piece[1]
                    pieces[k_piece] = piece_mock
        return pieces


def suites() -> Dict[ts.TestSuites, List[unittest.TestCase]]:
    return {
        ts.TestSuites.GAME_LOGIC: [
            TestReferee('test_check_threat'),
            TestReferee('test_get_king_moves')],
        ts.TestSuites.GAME_TIES: [
            TestReferee('test_check_material_insufficiency')],
        ts.TestSuites.SMOKE_TESTING: [
            TestReferee('test_turn')]
    }
