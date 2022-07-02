import unittest
import unittest.mock as mock
from typing import Callable, Dict, List, NamedTuple, Tuple, Union

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


class TestMatInsufInput(NamedTuple):
    id: int
    type: str
    color: str
    active: bool
    row: int
    column: int


class TestCheckThreatInput(NamedTuple):  # TODO
    pos: Tuple[int, int]
    enemy_color: str
    # NOTE - bool(turn_color == bottom_color)
    bottomup_orientation: Callable[[], bool]
    board_matrix: List[List[Union[str, None]]]


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

    def _check_enemy_presence(self, pos, enemy_color) -> bool:
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8 and self.referee.board_matrix[pos[0]][pos[1]] and self.referee.board_matrix[pos[0]][pos[1]][0] == enemy_color

    def _check_void(self, pos) -> bool:
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8 and not self.referee.board_matrix[pos[0]][pos[1]]

    def _add_tuples(self, t0, t1) -> Tuple[int, int]:
        return (t0[0]+t1[0], t0[1]+t1[1])

    def test_turn(self) -> None:
        # NOTE - Change turn to oponent and also prevent en passants out of the right turn.
        # --- SECTION - CONFIGURE TEST
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

    # --- !SECTION - CONFIGURE TEST
    # --- SECTION - TEST
        # STUB - self.referee.update_status
        with mock.patch.object(self.referee, 'update_status') as update_status_mock:
            update_status_mock.return_value = None
            for i in range(len(runs)):
                with self.subTest(i=i):
                    self._configure_test_turn(runs[i][1])
                # --- SECTION - beeing tested
                    self.referee.turn()
                # --- !SECTION
                    result = self._get_test_turn_result(
                        runs[i][1].k_pawn1, runs[i][1].k_pawn2)
                    self.assertEqual(result, runs[i][0])  # NOTE - compare
    # --- !SECTION - TEST
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

    def test_check_threat(self) -> None:
        '''
        Test if a position is beeing threatened
        '''
        # --- SECTION - CONFIGURATION
        runs: List[Tuple[bool, TestCheckThreatInput]] = []
        # NOTE (0) - test not beeing threatened
        runs.append((
            False,
            TestCheckThreatInput(
                pos=(3, 1),
                enemy_color='w',
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
                enemy_color='b',
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
                enemy_color='w',
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
                enemy_color='w',
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
                enemy_color='w',
                bottomup_orientation=lambda: False,
                board_matrix=[
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [None, 'bp2', *[None]*6],
                    [None]*8,
                    [None]*8,
                    [None]*8,
                    [*[None]*5, 'wb6', *[None]*2]])))        # # NOTE () - test not beeing threatened by a ...
        # NOTE (5) - test beeing threatened by a white knight
        runs.append((
            True,
            TestCheckThreatInput(
                pos=(3, 1),
                enemy_color='w',
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
                enemy_color='w',
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
                enemy_color='w',
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
                add_tuples.side_effect = self._add_tuples
                # --- SECTION - beeing tested
                result = self.referee.check_threat(
                    pos=input_config.pos,
                    enemy_color=input_config.enemy_color)
                # --- !SECTION - beeing tested
                self.assertEqual(expected, result)
        # --- !SECTION - TEST
        return None


def suites() -> Dict[ts.TestSuites, List[unittest.TestCase]]:
    return {
        ts.TestSuites.GAME_LOGIC: [TestReferee('test_turn')],
        ts.TestSuites.GAME_TIES: [TestReferee('test_material_insufficiency')],
        ts.TestSuites.SMOKE_TESTING: [TestReferee('test_check_threat')]
    }
