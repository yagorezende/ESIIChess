from typing import Dict
from logic.const import DELTAS
from ui.board import ChessPiece

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

    def check_enemy_presence(self, pos:tuple, enemy_color:str) -> bool:
        return self.check_bounds(pos) and self.board_matrix[pos[0]][pos[1]] and self.board_matrix[pos[0]][pos[1]][0] == enemy_color

    def check_en_passant(self, pawn_pos:tuple, enemy_pawn_pos:tuple, factor:int, enemy_color:str) -> bool:
        if self.check_enemy_presence(enemy_pawn_pos, enemy_color):
            aux = self.board_matrix[enemy_pawn_pos[0]][enemy_pawn_pos[1]]
            if aux[1] == 'p' and self.pieces[aux].has_jumped:
                return self.check_void((pawn_pos[0] + factor, enemy_pawn_pos[1]))
        return False

    def check_threat(self, pos, enemy_color, bottomup_orientation = True):
        # look for enemy pawns
        factors = [(-1, 1), (-1, -1)] if bottomup_orientation else [(1, 1), (1, -1)]
        for factor in factors:
            new_pos = (pos[0] + factor[0], pos[1] + factor[1])
            if self.check_enemy_presence(new_pos, enemy_color): # is last space occupied by enemy?
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'p':
                    print('threatened by pawn')
                    return True
        # print('pawns checked')
        # look for enemy knights
        for factor in DELTAS['knight']:
            new_pos = (pos[0] + factor[0], pos[1] + factor[1])
            if self.check_enemy_presence(new_pos, enemy_color):
                if self.board_matrix[new_pos[0]][new_pos[1]][1] == 'n':
                    print('threatened by knight')
                    return True
        # print('knights checked')
        # look for enemy rooks or queens
        factors = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for factor in factors:
            new_pos = (pos[0] + factor[0], pos[1] + factor[1])
            while self.check_void(new_pos): # while void spaces exist...
                new_pos = (new_pos[0] + factor[0], new_pos[1] + factor[1])
            if self.check_enemy_presence(new_pos, enemy_color): # is last space occupied by enemy?
                type = self.board_matrix[new_pos[0]][new_pos[1]][1]
                if type == 'r' or type == 'q':
                    print('threatened by queen/rook')
                    return True
        # print('queen/rooks checked')
        # look for enemy bishops or queens
        factors = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for factor in factors:
            new_pos = (pos[0] + factor[0], pos[1] + factor[1])
            while self.check_void(new_pos): # while void spaces exist...
                new_pos = (new_pos[0] + factor[0], new_pos[1] + factor[1])
            if self.check_enemy_presence(new_pos, enemy_color): # is last space occupied by enemy?
                type = self.board_matrix[new_pos[0]][new_pos[1]][1]
                if type == 'b' or type == 'q':
                    print('threatened by queen/bishop')
                    return True
        # print('queen/bishops checked')
        return False

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

    def get_king_moves(self, pos:tuple) -> list:
        space = self.get_delta_moves(pos, 'king')
        enemy_color = 'b' if self.board_matrix[pos[0]][pos[1]][0] == 'w' else 'w'
        if self.check_threat(pos, enemy_color): # king is currently threatened, he can't castle
            return space

        king = self.pieces[self.board_matrix[pos[0]][pos[1]]]
        if not king.has_moved:
            # small castle
            new_pos = (pos[0], pos[1] + 1)
            while self.check_void(new_pos) and not self.check_threat(new_pos, enemy_color):
                new_pos = (new_pos[0], new_pos[1] + 1)
            if not self.check_void(new_pos):
                piece = self.pieces[self.board_matrix[new_pos[0]][new_pos[1]]]
                if piece.color != enemy_color and piece.type == 'r' and not piece.has_moved:
                    space.append((new_pos[0], new_pos[1] - 1))
            # big castle
            new_pos = (pos[0], pos[1] - 1)
            while self.check_void(new_pos) and not self.check_threat(new_pos, enemy_color):
                new_pos = (new_pos[0], new_pos[1] - 1)
            if not self.check_void(new_pos):
                piece = self.pieces[self.board_matrix[new_pos[0]][new_pos[1]]]
                if piece.color != enemy_color and piece.type == 'r' and not piece.has_moved:
                    space.append((new_pos[0], new_pos[1] + 2))        
            
        return space

    def get_possible_moves(self, piece:str, bottomup_orientation:bool = True) -> list: # inform the possible moves for a single piece
        pos = self.pieces[piece].get_board_pos()
        if not self.board_matrix[pos[0]][pos[1]]:
            return []
        type = self.pieces[piece].type
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
            return self.get_king_moves(pos)
        return None