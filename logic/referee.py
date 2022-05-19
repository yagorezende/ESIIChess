from typing import Dict
from logic.const import DELTAS
from ui.piece import ChessPiece

class Referee():

    def __init__(self, board_matrix:list, pieces:dict) -> None:
        self.board_matrix = board_matrix
        self.pieces:Dict[str, ChessPiece] = pieces

    def check_status(self): # TODO: implement
        pass

    def check_bounds(self, pos) -> bool: # checks whether position exists in the board
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7

    def check_void(self, pos) -> bool: # checks whether a slot is empty
        return self.check_bounds(pos) and not self.board_matrix[pos[0]][pos[1]]

    def probe(self, pos:tuple, factor:tuple, enemy_color:str) -> list: # returns possible moves in one direction
        space = []
        new_row, new_col = pos[0] + factor[0], pos[1] + factor[1]
        while self.check_void((new_row, new_col)): # while void spaces exist...
            space.append((new_row, new_col))
            new_row, new_col = new_row + factor[0], new_col + factor[1]
        if self.check_enemy_presence((new_row, new_col), enemy_color): # is last space occupied by enemy?
            space.append((new_row, new_col))
        return space
    
    def get_possible_diagonal_moves(self, pos:tuple) -> list:
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        return self.probe(pos, (-1, 1), enemy_color) + \
            self.probe(pos, (-1, -1), enemy_color) + \
            self.probe(pos, (1, 1), enemy_color) + \
            self.probe(pos, (1, -1), enemy_color)

    def get_possible_cross_moves(self, pos:tuple) -> list:
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        return self.probe(pos, (-1, 0), enemy_color) + \
            self.probe(pos, (1, 0), enemy_color) + \
            self.probe(pos, (0, 1), enemy_color) + \
            self.probe(pos, (0, -1), enemy_color)

    def get_delta_moves(self, pos:tuple, key:str):
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        space = []
        for (i, j) in DELTAS[key]:
            new_pos = (pos[0] + i, pos[1] + j)
            if self.check_enemy_presence(new_pos, enemy_color) or self.check_void(new_pos): # free space
                space.append(new_pos)
        return space

    def check_enemy_presence(self, pos:tuple, enemy_color:str) -> bool:
        return self.check_bounds(pos) and self.board_matrix[pos[0]][pos[1]] and self.board_matrix[pos[0]][pos[1]][0] == enemy_color

    def check_en_passant(self, pawn_pos:tuple, enemy_pawn_pos:tuple, factor:int, enemy_color:str) -> bool:
        if self.check_enemy_presence(enemy_pawn_pos, enemy_color):
            aux = self.board_matrix[enemy_pawn_pos[0]][enemy_pawn_pos[1]]
            if aux[1] == 'p' and self.pieces[aux].has_jumped:
                return self.check_void((pawn_pos[0] + factor, enemy_pawn_pos[1] + factor))
        return False

    def get_pawn_moves(self, piece:str, bottomup_orientation:bool) -> list:
        space = []
        r, c = self.pieces[piece].get_board_pos()
        if not r % 7: # is the pawn on top/bottom?
            return space
        enemy_color = 'b' if self.board_matrix[r][c][0] == 'w' else 'w'
        factor = -1 if bottomup_orientation else 1

        if not self.board_matrix[r + factor][c]: # no one ahead? normal step
            space.append((r + factor, c))
            if r == int(3.5 - factor*2.5) and not self.board_matrix[r + 2*factor][c]: # no one way ahead? double step
                space.append((r + 2*factor, c))

        aux = (r + factor, c + factor)
        if self.check_enemy_presence(aux, enemy_color):
            space.append(aux)

        aux = (r + factor, c - factor)
        if self.check_enemy_presence(aux, enemy_color):
            space.append(aux)

        aux = (r, c + factor)
        if self.check_en_passant((r, c), aux, factor, enemy_color):
            space.append((r + factor, c + factor))

        aux = (r, c - factor)
        if self.check_en_passant((r, c), aux, factor, enemy_color):
            space.append((r + factor, c - factor))

        return space
    
    def get_rook_moves(self, pos:tuple) -> list:
        return self.get_possible_cross_moves(pos)
    
    def get_knight_moves(self, pos:tuple) -> list:
        return self.get_delta_moves(pos, 'knight')
    
    def get_bishop_moves(self, pos:tuple) -> list:
        return self.get_possible_diagonal_moves(pos)

    def get_queen_moves(self, pos:tuple) -> list:
        return self.get_possible_cross_moves(pos) + self.get_possible_diagonal_moves(pos)

    def get_king_moves(self, pos:tuple) -> list: # TODO
        space = self.get_delta_moves(pos, 'king')
        # TODO: include castling
        return space

    def get_possible_moves(self, piece:str, bottomup_orientation:bool = True) -> list: # inform the possible moves for a single piece
        pos = self.pieces[piece].get_board_pos()
        if not self.board_matrix[pos[0]][pos[1]]:
            return []
        type = self.pieces[piece].get_type()
        if type == 'p': # it's a pawn
            return self.get_pawn_moves(piece, bottomup_orientation)
        if type == 'r': # it's a rook
            return self.get_rook_moves(pos)
        if type == 'n': # it's a knight
            return self.get_knight_moves(pos)
        if type == 'b': # it's a bishop
            return self.get_bishop_moves(pos)
        if type == 'q': # it's the queen
            return self.get_queen_moves(pos)
        if type == 'k': # it's the king
            return self.get_king_moves(piece)
        return None