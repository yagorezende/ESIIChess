from typing import Dict
from logic.const import DELTAS, NO_PROGRESSION_LIMIT, REPETITIONS_FOR_DRAW, Status
from logic.tools import add_tuples, letter_to_color
from ui.board import ChessPiece

class Referee():

    def __init__(self, board_matrix: list, pieces: dict, bottom_color: str = 'w') -> None:
        self.board_matrix = board_matrix
        self.states_counter: Dict[str, int] = {}
        self.pieces: Dict[str, ChessPiece] = pieces
        self.turn_color = 'w'
        self.bottom_color = bottom_color
        self.no_progression_counter = 0
        self.kill_flag = False
        self.status = Status.NORMAL

    def enemy_color(self) -> str:
        return 'b' if self.turn_color == 'w' else 'w'

    def bottomup_orientation(self) -> bool:
        return self.turn_color == self.bottom_color

    def board_shot(self):
        return [row.copy() for row in self.board_matrix]

    def turn(self) -> None:
        self.turn_color = 'b' if self.turn_color == 'w' else 'w' # change turns
        for i in range(1, 9): # update pawns to avoid second chances in en passants
            pawn = self.pieces[self.turn_color + 'p' + str(i)]
            if pawn.active and pawn.has_jumped:
                pawn.has_jumped = False
        self.update_status()

    def update_status(self) -> None:
        print('status checking: ', end='')
        # check progression
        if self.no_progression_counter == NO_PROGRESSION_LIMIT:
            print('LACK OF PROGRESSION')
            self.status = Status.DRAW_PROGRESSION
            return
        # check king
        if self.check_threat(self.pieces[self.turn_color + 'k5'].get_board_pos(), self.enemy_color()):
            for key, value in self.pieces.items():
                if key[0] == self.turn_color:
                    if value.active and self.get_possible_moves(key):
                        print('CHECK - ' + letter_to_color(self.turn_color) + ' king is in check.')
                        self.status = Status.CHECK
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
        # check material
        if self.kill_flag:
            if self.check_material_insufficiency():
                print('MATERIAL INSUFFICIENCY')
                self.status = Status.DRAW_MATERIAL
            self.kill_flag = False
            self.no_progression_counter = 0
            return
        # normal status
        print('NORMAL - its ' + letter_to_color(self.turn_color) + ' turn.')
        self.status = Status.NORMAL
        return

    def check_repetition(self) -> bool:
        key = ''
        for i in range(8):
            for j in range(8):
                if self.board_matrix[i][j]:
                    key += self.board_matrix[i][j][0] + self.board_matrix[i][j][1]
                else:
                    key += '0'
        self.states_counter[key] = self.states_counter.get(key, 0) + 1
        if self.states_counter[key] == REPETITIONS_FOR_DRAW:
            return True
        return False

    def check_mobility(self) -> bool:
        for key, value in self.pieces.items():
            if key[0] == self.turn_color:
                if value.active and self.get_possible_moves(key):
                    return True
        return False

    def check_material_insufficiency(self) -> bool:

        w_sum = {}
        b_sum = {}
        for key, value in self.pieces.items():
            if not value.active:
                continue
            if value.type == 'p' or value.type == 'r' or value.type == 'q':
                return False
            d = w_sum if key[0] == 'w' else b_sum
            p_type = key[1]
            d[p_type] = d.get(p_type, 0) + 1

        w_count = set(w_sum.items())
        b_count = set(b_sum.items())

        # 1 king vs 1 king
        condition = w_count == b_count == {('k', 1)}
        # 1 king vs 1 king and 1 bishop
        condition |= \
            (w_count == {('k', 1)} and b_count == {('k', 1),('b', 1)}) or \
            (b_count == {('k', 1)} and w_count == {('k', 1),('b', 1)})
        # 1 king vs 1 king and 1 knight
        condition |= \
            (w_count == {('k', 1)} and b_count == {('k', 1),('n', 1)}) or \
            (b_count == {('k', 1)} and w_count == {('k', 1),('n', 1)})
        # 1 king and 1 bishop vs 1 king and 1 bishop (bishops of similar squares)
        if w_count == {('k', 1), ('b', 1)} and b_count == {('k', 1), ('b', 1)}:
            wbcode = 'wb3' if self.pieces['wb3'].active else 'wb6'
            bbcode = 'bb3' if self.pieces['bb3'].active else 'bb6'
            condition = wbcode[2] != bbcode[2]
        return condition
    
    def check_bounds(self, pos) -> bool:  # checks whether position exists in the board
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7

    def check_void(self, pos) -> bool:  # checks whether a slot is empty
        return self.check_bounds(pos) and not self.board_matrix[pos[0]][pos[1]]

    def check_enemy_presence(self, pos: tuple, enemy_color: str) -> bool:
        return self.check_bounds(pos) and self.board_matrix[pos[0]][pos[1]] and self.board_matrix[pos[0]][pos[1]][
            0] == enemy_color

    def check_en_passant(self, pawn_pos: tuple, enemy_pawn_pos: tuple) -> bool: # self-explanatory
        factor = -1 if self.bottomup_orientation() else 1
        enemy_color = 'b' if self.board_matrix[pawn_pos[0]][pawn_pos[1]][0] == 'w' else 'w'
        if self.check_enemy_presence(enemy_pawn_pos, enemy_color):
            aux = self.board_matrix[enemy_pawn_pos[0]][enemy_pawn_pos[1]]
            if aux[1] == 'p' and self.pieces[aux].has_jumped:
                return self.check_void((pawn_pos[0] + factor, enemy_pawn_pos[1]))
        return False

    def check_threat(self, pos: tuple, enemy_color: str) -> bool: # checks the existence of a threat in a particular position
        # look for enemy pawns
        factors = [(-1, 1), (-1, -1)] if self.bottomup_orientation() else [(1, 1), (1, -1)]
        for factor in factors:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos, enemy_color):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'p':
                    return True
        # look for enemy king
        for factor in DELTAS['king']:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos, enemy_color):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'k':
                    return True
        # look for enemy knights
        for factor in DELTAS['knight']:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos, enemy_color):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'n':
                    return True
        # look for enemy rooks or queens
        factors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for factor in factors:
            new_pos = add_tuples(pos, factor)
            while self.check_void(new_pos):
                new_pos = (new_pos[0] + factor[0], new_pos[1] + factor[1])
            if self.check_enemy_presence(new_pos, enemy_color):
                name = self.board_matrix[new_pos[0]][new_pos[1]]
                if name[1] == 'r' or name[1] == 'q':
                    return True
        # look for enemy bishops or queens
        factors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for factor in factors:
            new_pos = add_tuples(pos, factor)
            while self.check_void(new_pos):
                new_pos = (new_pos[0] + factor[0], new_pos[1] + factor[1])
            if self.check_enemy_presence(new_pos, enemy_color):
                name = self.board_matrix[new_pos[0]][new_pos[1]]
                if name[1] == 'b' or name[1] == 'q':
                    return True
        return None

    def probe(self, pos: tuple, factor: tuple, enemy_color: str) -> list:  # returns possible moves in one direction
        space = []
        new_pos = add_tuples(pos, factor)
        while self.check_void(new_pos):  # while void spaces exist...
            space.append(new_pos)
            new_pos = add_tuples(new_pos, factor)
        if self.check_enemy_presence(new_pos, enemy_color):  # is last space occupied by enemy?
            space.append(new_pos)
        return space

    def prune(self, pos: tuple, moves: list) -> None: 
        pruned = []
        king_pos = self.pieces[self.turn_color + 'k5'].get_board_pos()
        for move in moves:

            if self.board_matrix[pos[0]][pos[1]][1] == 'k':
                king_pos = move

            b1, b2 = self.board_matrix[move[0]][move[1]], self.board_matrix[pos[0]][pos[1]]

            self.board_matrix[move[0]][move[1]] = self.board_matrix[pos[0]][pos[1]]
            self.board_matrix[pos[0]][pos[1]] = None

            if not self.check_threat(king_pos, self.enemy_color()):
                pruned.append(move)

            self.board_matrix[move[0]][move[1]] = b1
            self.board_matrix[pos[0]][pos[1]] = b2

        return pruned

    def get_possible_diagonal_moves(self, pos: tuple) -> list:
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        return self.probe(pos, (-1, 1), enemy_color) + \
               self.probe(pos, (-1, -1), enemy_color) + \
               self.probe(pos, (1, 1), enemy_color) + \
               self.probe(pos, (1, -1), enemy_color)

    def get_possible_cross_moves(self, pos: tuple) -> list:
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        return self.probe(pos, (-1, 0), enemy_color) + \
               self.probe(pos, (1, 0), enemy_color) + \
               self.probe(pos, (0, 1), enemy_color) + \
               self.probe(pos, (0, -1), enemy_color)

    def get_delta_moves(self, pos: tuple, key: str) -> list:
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        space = []
        for factor in DELTAS[key]:
            new_pos = add_tuples(pos, factor)
            if self.check_enemy_presence(new_pos, enemy_color) or self.check_void(new_pos):
                space.append(new_pos)
        return space

    def get_pawn_moves(self, pos: tuple) -> list:
        space = []
        if pos[0] == 0 or pos[0] == 7:  # is the pawn on top/bottom?
            return space
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        factor = -1 if self.bottomup_orientation() else 1

        if not self.board_matrix[pos[0] + factor][pos[1]]:  # no one ahead? normal step
            space.append((pos[0] + factor, pos[1]))
            if pos[0] == int(3.5 - factor * 2.5) and not self.board_matrix[pos[0] + 2 * factor][
                pos[1]]:  # no one way ahead? double step
                space.append((pos[0] + 2 * factor, pos[1]))

        aux = (pos[0] + factor, pos[1] + factor)
        if self.check_enemy_presence(aux, enemy_color):
            space.append(aux)

        aux = (pos[0] + factor, pos[1] - factor)
        if self.check_enemy_presence(aux, enemy_color):
            space.append(aux)

        aux = (pos[0], pos[1] + factor)
        if self.check_en_passant((pos[0], pos[1]), aux):
            space.append((pos[0] + factor, pos[1] + factor))

        aux = (pos[0], pos[1] - factor)
        if self.check_en_passant((pos[0], pos[1]), aux):
            space.append((pos[0] + factor, pos[1] - factor))

        return space

    def get_rook_moves(self, pos: tuple) -> list:
        return self.get_possible_cross_moves(pos)

    def get_knight_moves(self, pos: tuple) -> list:
        return self.get_delta_moves(pos, 'knight')

    def get_bishop_moves(self, pos: tuple) -> list:
        return self.get_possible_diagonal_moves(pos)

    def get_queen_moves(self, pos: tuple) -> list:
        return self.get_possible_cross_moves(pos) + self.get_possible_diagonal_moves(pos)

    def get_king_moves(self, pos: tuple) -> list:
        space = self.get_delta_moves(pos, 'king')
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        if self.check_threat(pos, enemy_color):  # king is currently threatened, he can't castle
            return space

        king = self.pieces[self.board_matrix[pos[0]][pos[1]]]
        if not king.has_moved:
            # small castle
            new_pos, steps = (pos[0], pos[1] + 1), 0
            while self.check_void(new_pos) and not self.check_threat(new_pos, enemy_color):
                new_pos = (new_pos[0], new_pos[1] + 1)
                steps += 1
            if steps == 2 and not self.check_void(new_pos):
                piece = self.pieces[self.board_matrix[new_pos[0]][new_pos[1]]]
                if piece.color != enemy_color and piece.type == 'r' and not piece.has_moved:
                    space.append((new_pos[0], new_pos[1] - 1))
            # big castle
            new_pos, steps = (pos[0], pos[1] - 1), 0
            while self.check_void(new_pos) and not self.check_threat(new_pos, enemy_color):
                new_pos = (new_pos[0], new_pos[1] - 1)
                steps += 1
            if steps == 3 and not self.check_void(new_pos):
                piece = self.pieces[self.board_matrix[new_pos[0]][new_pos[1]]]
                if piece.color != enemy_color and piece.type == 'r' and not piece.has_moved:
                    space.append((new_pos[0], new_pos[1] + 2))

        return space

    def get_possible_moves(self, piece: str) -> list:
        """
        inform the possible moves for a single piece
        :param piece: the str piece code
        :param bottom_up_orientation: checks if the orientation of piece is bottom-up
        :return: list of possible moves
        """

        pos = self.pieces[piece].get_board_pos()
        if not self.board_matrix[pos[0]][pos[1]]:
            return []
        piece_type = self.pieces[piece].type
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