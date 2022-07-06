from typing import Dict, List
from logic.const import DELTAS, NO_PROGRESSION_LIMIT, REPETITIONS_FOR_DRAW, INITIAL_STATE_1, INITIAL_STATE_2, Status
from logic.game_overall_context import GameOverallContext
from logic.tools import add_tuples, letter_to_color, str_to_status
from ui.board import ChessPiece


class Referee():

    def __init__(self, board_matrix: list, pieces: dict, bottom_color: str = 'w') -> None:
        self.board_matrix: List[List[str]] = board_matrix
        self.pieces: Dict[str, ChessPiece] = pieces
        self.rushed_pawn: tuple = None
        self.turn_counter = 1
        self.turn_color = 'w'
        self.bottom_color = GameOverallContext().get_color()
        self.no_progression_counter = 0
        self.pieces_counter = 32
        self.status = Status.NORMAL
        self.kings_place = {'b': 4, 'w': 5}[GameOverallContext().get_color()]
        if self.bottom_color == 'w':
            self.states_counter: Dict[str, int] = {INITIAL_STATE_1: 1}
        else:
            self.states_counter: Dict[str, int] = {INITIAL_STATE_2: 1}

    def board_shot(self) -> List[List[str]]:
        """
        Returns a copy of the board matrix.
        """
        return [row.copy() for row in self.board_matrix]

    def get_state(self) -> dict:
        """
        Returns the state of the referee object.
        """
        return {
            'bottom_color': self.bottom_color,
            'no_progression_counter': self.no_progression_counter,
            'pieces_counter': self.pieces_counter,
            'rushed_pawn': self.rushed_pawn,
            'states_counter': self.states_counter,
            'status': self.status.name,
            'turn_color': self.turn_color,
            'turn_counter': self.turn_counter
        }

    def set_state(self, state) -> None:
        """
        Loads state.
        """
        self.bottom_color = state['bottom_color']
        self.no_progression_counter = state['no_progression_counter']
        self.pieces_counter = state['pieces_counter']
        self.rushed_pawn = state['rushed_pawn']
        self.states_counter = state['states_counter']
        self.turn_color = state['turn_color']
        self.turn_counter = state['turn_counter']
        self.status = str_to_status(state['status'])
        self.kings_place = {'b': 4, 'w': 5}[GameOverallContext().get_color()]
        if self.bottom_color == 'w':
            self.states_counter: Dict[str, int] = {INITIAL_STATE_1: 1}
        else:
            self.states_counter: Dict[str, int] = {INITIAL_STATE_2: 1}
        return

    def bottomup_orientation(self) -> bool:
        """
        Checks whether current player started at the bottom.
        """
        return self.turn_color == self.bottom_color

    def enemy_color(self) -> str:
        """
        Returns enemy pieces' color.
        """
        return 'b' if self.turn_color == 'w' else 'w'

    def turn(self) -> None:
        """
        Turn changing.
        """
        if self.rushed_pawn:
            hp = self.board_matrix[self.rushed_pawn[0]][self.rushed_pawn[1]]
            if hp is None or hp[0] == self.enemy_color():
                self.rushed_pawn = None
        self.turn_color = 'b' if self.turn_color == 'w' else 'w'  # change turns
        self.turn_counter += 1
        self.update_status()

    def update_status(self) -> None:  # self-explanatory
        print('status checking: ', end='')
        # check progression
        if self.no_progression_counter == NO_PROGRESSION_LIMIT:
            print('LACK OF PROGRESSION')
            self.status = Status.DRAW_PROGRESSION
            return
        # check material
        if self.pieces_counter < 5:
            if self.check_material_insufficiency():
                print('MATERIAL INSUFFICIENCY')
                self.status = Status.DRAW_MATERIAL
                return
        # check king
        if self.check_threat(self.find(self.turn_color + f'k{self.kings_place}')):
            if self.check_mobility():
                print('CHECK - ' + letter_to_color(self.turn_color, ) + ' king is in check.')
                self.status = Status.CHECK
                return
            print('CHECKMATE - ' + letter_to_color(self.enemy_color()).upper() + ' WINS!')
            self.status = Status.CHECKMATE
            return
        # check stalemate
        if not self.check_mobility():
            print('STALEMATE - No ' + letter_to_color(self.turn_color) + ' piece can move.')
            self.status = Status.DRAW_STALEMATE
            return
        # check repetition
        if self.check_repetition():
            print('REPETITION')
            self.status = Status.DRAW_REPETITION
            return
            # normal status
        print('NORMAL - its ' + letter_to_color(self.turn_color) + ' turn.')
        self.status = Status.NORMAL
        return

    def check_termination(self) -> bool:
        """
        Checks whether the game has ended.
        """
        return not (self.status == Status.NORMAL or self.status == Status.CHECK)

    def check_repetition(self) -> bool:
        '''
        Checks whether the current state has already happened a pre-defined number of times.
        '''
        key = ''
        for i in range(8):
            for j in range(8):
                if self.board_matrix[i][j]:
                    key += self.board_matrix[i][j][:2]
                else:
                    key += '0'
        if not key:
            return False
        self.states_counter[key] = self.states_counter.get(key, 0) + 1
        return self.states_counter[key] == REPETITIONS_FOR_DRAW

    def check_mobility(self) -> bool:
        '''
        Checks whether there's at least one valid move.
        '''
        for row in self.board_matrix:
            for key in row:
                if key and key[0] == self.turn_color and self.get_possible_moves(key):
                    return True
        return False

    def check_material_insufficiency(self) -> bool:  # self-explanatory
        w_sum = {}
        b_sum = {}
        wbishop_pos = bbishop_pos = None
        for r in range(8):
            for c in range(8):
                key = self.board_matrix[r][c]
                if not key: continue
                if key[1] == 'p' or key[1] == 'r' or key[1] == 'q':
                    return False
                if key[1] == 'b':
                    if key[0] == 'w':
                        wbishop_pos = (r, c)
                    else:
                        bbishop_pos = (r, c)
                d = w_sum if key[0] == 'w' else b_sum
                d[key[1]] = d.get(key[1], 0) + 1

        w_count = set(w_sum.items())
        b_count = set(b_sum.items())

        # 1 king vs 1 king
        condition = w_count == b_count == {('k', 1)}
        # 1 king vs 1 king and 1 bishop
        condition |= \
            (w_count == {('k', 1)} and b_count == {('k', 1), ('b', 1)}) or \
            (b_count == {('k', 1)} and w_count == {('k', 1), ('b', 1)})
        # 1 king vs 1 king and 1 knight
        condition |= \
            (w_count == {('k', 1)} and b_count == {('k', 1), ('n', 1)}) or \
            (b_count == {('k', 1)} and w_count == {('k', 1), ('n', 1)})
        # 1 king and 1 bishop vs 1 king and 1 bishop (bishops of similar squares)
        if w_count == {('k', 1), ('b', 1)} and b_count == {('k', 1), ('b', 1)}:
            condition = self.get_square_color(wbishop_pos) == self.get_square_color(bbishop_pos)
        return condition

    def check_bounds(self, pos) -> bool:
        """
        Checks whether a position exists in the board.
        """
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7

    def check_void(self, pos) -> bool:
        """
        Checks whether a square is empty.
        """
        return self.check_bounds(pos) and not self.board_matrix[pos[0]][pos[1]]

    def check_enemy_presence(self, pos: tuple) -> bool:
        """
        Checks enemy presence in a particular position.
        """
        return self.check_bounds(pos) and self.board_matrix[pos[0]][pos[1]] and self.board_matrix[pos[0]][pos[1]][
            0] == self.enemy_color()

    def check_threat(self, pos: tuple) -> bool:
        """
        Checks the existence of a threat in a particular position.
        """
        # look for enemy pawns
        factors = [(-1, 1), (-1, -1)] if self.bottomup_orientation() else [(1, 1), (1, -1)]
        for factor in factors:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'p':
                    return True
        # look for enemy king
        for factor in DELTAS['king']:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'k':
                    return True
        # look for enemy knights
        for factor in DELTAS['knight']:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'n':
                    return True
        # look for enemy rooks or queens
        factors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for factor in factors:
            new_pos = add_tuples(pos, factor)
            while self.check_void(new_pos):
                new_pos = add_tuples(new_pos, factor)
            if self.check_enemy_presence(new_pos):
                name = self.board_matrix[new_pos[0]][new_pos[1]]
                if name[1] == 'r' or name[1] == 'q':
                    return True
        # look for enemy bishops or queens
        factors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for factor in factors:
            new_pos = add_tuples(pos, factor)
            while self.check_void(new_pos):
                new_pos = add_tuples(new_pos, factor)
            if self.check_enemy_presence(new_pos):
                name = self.board_matrix[new_pos[0]][new_pos[1]]
                if name[1] == 'b' or name[1] == 'q':
                    return True
        return False

    def get_square_color(self, pos: tuple) -> str:
        """
        Returns the color of a square in a certain position.
        """
        if pos[0] % 2 and pos[1] % 2 or not pos[0] % 2 and not pos[1] % 2:
            return 'w'
        return 'b'

    def probe(self, pos: tuple, factor: tuple) -> List[tuple]:
        """
        Returns all possible moves in one direction for a piece in a particular position.
        """
        space = []
        new_pos = add_tuples(pos, factor)
        while self.check_void(new_pos):  # while void spaces exist...
            space.append(new_pos)
            new_pos = add_tuples(new_pos, factor)
        if self.check_enemy_presence(new_pos):  # is last space occupied by enemy?
            space.append(new_pos)
        return space

    def find(self, piece: str) -> tuple:
        """
        Finds the position of a piece by it's key.
        """

        r, c = self.pieces[self.turn_color + f'k{self.kings_place}'].get_board_pos()
        if self.board_matrix[r][c] == piece:
            return r, c
        for r in range(8):
            for c in range(8):
                if self.board_matrix[r][c] == piece:
                    return r, c
        return

    def prune(self, pos: tuple, moves: list) -> List[tuple]:
        """
        Removes from a list the moves that leave the king in a check position.
        """
        king_pos = self.find(self.turn_color + f'k{self.kings_place}')
        if not king_pos:
            return moves
        pruned = []
        for move in moves:

            if self.board_matrix[pos[0]][pos[1]][1] == 'k':
                king_pos = move

            b1, b2 = self.board_matrix[move[0]][move[1]], self.board_matrix[pos[0]][pos[1]]

            self.board_matrix[move[0]][move[1]] = self.board_matrix[pos[0]][pos[1]]
            self.board_matrix[pos[0]][pos[1]] = None

            if not self.check_threat(king_pos):
                pruned.append(move)

            self.board_matrix[move[0]][move[1]] = b1
            self.board_matrix[pos[0]][pos[1]] = b2

        return pruned

    def get_possible_diagonal_moves(self, pos: tuple) -> List[tuple]:
        return self.probe(pos, (-1, 1)) + \
               self.probe(pos, (-1, -1)) + \
               self.probe(pos, (1, 1)) + \
               self.probe(pos, (1, -1))

    def get_possible_cross_moves(self, pos: tuple) -> List[tuple]:
        return self.probe(pos, (-1, 0)) + \
               self.probe(pos, (1, 0)) + \
               self.probe(pos, (0, 1)) + \
               self.probe(pos, (0, -1))

    def get_delta_moves(self, pos: tuple, key: str) -> List[tuple]:
        space = []
        for factor in DELTAS[key]:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos) or self.check_void(new_pos):
                space.append(new_pos)
        return space

    def get_pawn_moves(self, pos: tuple) -> List[tuple]:
        space = []
        if pos[0] == 0 or pos[0] == 7:  # is the pawn on top/bottom?
            return space
        factor = -1 if self.bottomup_orientation() else 1

        if not self.board_matrix[pos[0] + factor][pos[1]]:  # no one ahead? normal step
            space.append((pos[0] + factor, pos[1]))
            if pos[0] == int(3.5 - factor * 2.5) and not self.board_matrix[pos[0] + 2 * factor][
                pos[1]]:  # no one way ahead? double step
                space.append((pos[0] + 2 * factor, pos[1]))

        aux = (pos[0] + factor, pos[1] + factor)
        if self.check_enemy_presence(aux):
            space.append(aux)

        aux = (pos[0] + factor, pos[1] - factor)
        if self.check_enemy_presence(aux):
            space.append(aux)

        if self.rushed_pawn:
            if self.rushed_pawn == (pos[0], pos[1] + 1):  # en passant on the right
                space.append((pos[0] + factor, self.rushed_pawn[1]))
            elif self.rushed_pawn == (pos[0], pos[1] - 1):  # en passant on the left
                space.append((pos[0] + factor, self.rushed_pawn[1]))

        return space

    def get_rook_moves(self, pos: tuple) -> List[tuple]:
        return self.get_possible_cross_moves(pos)

    def get_knight_moves(self, pos: tuple) -> List[tuple]:
        return self.get_delta_moves(pos, 'knight')

    def get_bishop_moves(self, pos: tuple) -> List[tuple]:
        return self.get_possible_diagonal_moves(pos)

    def get_queen_moves(self, pos: tuple) -> List[tuple]:
        return self.get_possible_cross_moves(pos) + self.get_possible_diagonal_moves(pos)

    def get_king_moves(self, pos: tuple) -> List[tuple]:
        space = self.get_delta_moves(pos, 'king')
        if self.check_threat(pos):  # king is currently threatened, he can't castle
            return space

        king = self.pieces[self.board_matrix[pos[0]][pos[1]]]
        if not king.has_moved:
            factor = 1 if GameOverallContext().get_color() == 'w' else -1
            # small castle
            new_pos, steps = (pos[0], pos[1] + factor), 0
            while self.check_void(new_pos) and not self.check_threat(new_pos):
                new_pos = (new_pos[0], new_pos[1] + factor)
                steps += 1
            if steps == 2 and not self.check_void(new_pos):
                piece = self.pieces[self.board_matrix[new_pos[0]][new_pos[1]]]
                if piece.color == self.turn_color and piece.type == 'r' and not piece.has_moved:
                    space.append((new_pos[0], new_pos[1] - factor))
            # big castle
            new_pos, steps = (pos[0], pos[1] - factor), 0
            while self.check_void(new_pos) and not self.check_threat(new_pos):
                new_pos = (new_pos[0], new_pos[1] - factor)
                steps += 1
            if steps == 3 and not self.check_void(new_pos):
                piece = self.pieces[self.board_matrix[new_pos[0]][new_pos[1]]]
                if piece.color == self.turn_color and piece.type == 'r' and not piece.has_moved:
                    space.append((new_pos[0], new_pos[1] + factor*2))

        return space

    def get_possible_moves(self, piece: str = None, pos: tuple = None) -> List[tuple]:
        """
        Returns all the possible moves for a single piece.
        """
        if not pos:
            if not piece:
                return []
            pos = self.find(piece)
        if not self.board_matrix[pos[0]][pos[1]]:
            return []
        piece_type = self.board_matrix[pos[0]][pos[1]][1]
        if piece_type == 'p':  # it's a pawn
            return self.prune(pos, self.get_pawn_moves(pos))
        if piece_type == 'r':  # it's a rook
            return self.prune(pos, self.get_rook_moves(pos))
        if piece_type == 'n':  # it's a knight
            return self.prune(pos, self.get_knight_moves(pos))
        if piece_type == 'b':  # it's a bishop
            return self.prune(pos, self.get_bishop_moves(pos))
        if piece_type == 'q':  # it's the queen
            return self.prune(pos, self.get_queen_moves(pos))
        if piece_type == 'k':  # it's the king
            return self.prune(pos, self.get_king_moves(pos))
        return None

    def get_pawn_promote(self) -> str:
        """
        Returns the pawn key of the pawn ready to be promoted.
        """
        bottom_color = self.bottom_color
        top_color = 'w' if bottom_color=='b' else 'b'
        for k, cp in self.pieces.items():
            # NOTE - if piece is pawn
            is_pawn = cp.type == 'p'
            # NOTE - pawn on top row
            c2 = is_pawn and cp.get_board_pos()[0] == 0
            pawn_top_row = c2 and cp.color != top_color
            # NOTE - pawn on bottom row
            c4 = is_pawn and cp.get_board_pos()[0] == 7
            pawn_bottom_row = c4 and cp.color != bottom_color
            # NOTE - white pawn on 'black row' or black pwan on 'white row'
            c6 = pawn_top_row or pawn_bottom_row
            if c6:
                return k
        return ''
