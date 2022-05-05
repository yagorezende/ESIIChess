from logic.const import DELTAS


class Referee():

    @staticmethod
    def check_bounds(pos) -> bool: # checks whether position exists in the board
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7

    @staticmethod
    def probe(board_matrix:list, pos:tuple, factor:tuple, enemy_color:str) -> list: # returns possible moves in one direction
        space = []
        new_row, new_col = pos[0] + factor[0], pos[1] + factor[1]
        while Referee.check_bounds((new_row, new_col)) and not board_matrix[new_row][new_col]: # while void spaces exist...
            space.append((new_row, new_col))
            new_row, new_col = new_row + factor[0], new_col + factor[1]
        if Referee.check_bounds((new_row, new_col)):
            if board_matrix[new_row][new_col][0] == enemy_color: # is last space occupied by enemy?
                space.append((new_row, new_col))
        return space
    
    @staticmethod
    def get_possible_diagonal_moves(board_matrix:list, pos:tuple) -> list:
        piece = board_matrix[pos[0]][pos[1]]
        if piece[0] == 'w':
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        diag_space = Referee.probe(board_matrix, pos, (-1, 1), enemy_color) # up-right
        diag_space += Referee.probe(board_matrix, pos, (-1, -1), enemy_color) # up-left
        diag_space += Referee.probe(board_matrix, pos, (1, 1), enemy_color) # down-right
        diag_space += Referee.probe(board_matrix, pos, (1, -1), enemy_color) # down-left
        return diag_space

    @staticmethod
    def get_possible_cross_moves(board_matrix:list, pos:tuple) -> list:
        if board_matrix[pos[0]][pos[1]][0] == 'w':
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        cross_space = Referee.probe(board_matrix, pos, (-1, 0), enemy_color) # up
        cross_space += Referee.probe(board_matrix, pos, (1, 0), enemy_color) # down
        cross_space += Referee.probe(board_matrix, pos, (0, 1), enemy_color) # right
        cross_space += Referee.probe(board_matrix, pos, (0, -1), enemy_color) # left
        return cross_space
    
    @staticmethod
    def get_pawn_moves(board_matrix:list, pos:tuple, bottomup_orientation:bool) -> list:
        space = []
        if bottomup_orientation:
            key = 'pawnUp'
        else:
            key = 'pawnDown'
        for (i, j) in DELTAS[key]:
            new_pos = (pos[0] + i, pos[1] + j)
            # TODO: implement pawn movement assessment
        return space
    
    @staticmethod
    def get_rook_moves(board_matrix:list, pos:tuple) -> list:
        return Referee.get_possible_cross_moves(board_matrix, pos)
    
    @staticmethod
    def get_knight_moves(board_matrix:list, pos:tuple) -> list:
        space = []
        if board_matrix[pos[0]][pos[1]][0] == 'w':
            enemy_color = 'b'
        else:
            enemy_color = 'w'
        for (i, j) in DELTAS['knight']:
            new_pos = (pos[0] + i, pos[1] + j)
            if Referee.check_bounds(new_pos):
                if board_matrix[new_pos[0]][new_pos[1]]:
                    if board_matrix[new_pos[0]][new_pos[1]][0] == enemy_color:
                        space.append(new_pos)
                else: # free space
                    space.append(new_pos)
        return space
    
    @staticmethod
    def get_bishop_moves(board_matrix:list, pos:tuple) -> list:
        return Referee.get_possible_diagonal_moves(board_matrix, pos)

    @staticmethod
    def get_queen_moves(board_matrix:list, pos:tuple) -> list:
        return Referee.get_possible_cross_moves(board_matrix, pos) + Referee.get_possible_diagonal_moves(board_matrix, pos)

    @staticmethod
    def get_king_moves(board_matrix:list, pos:tuple) -> list: # TODO
        return []

    @staticmethod
    def get_possible_moves(board_matrix:list, pos:tuple, bottomup_orientation:bool = True) -> list: # inform the possible moves for a single piece
        piece = board_matrix[pos[0]][pos[1]]
        if not piece:
            return []
        if piece[1] == 'p': # it's a pawn
            return Referee.get_pawn_moves(board_matrix, pos, bottomup_orientation)
        if piece[1] == 'r': # it's a rook
            return Referee.get_rook_moves(board_matrix, pos)
        if piece[1] == 'n': # it's a knight
            return Referee.get_knight_moves(board_matrix, pos)
        if piece[1] == 'b': # it's a bishop
            return Referee.get_bishop_moves(board_matrix, pos)
        if piece[1] == 'q': # it's the queen
            return Referee.get_queen_moves(board_matrix, pos)
        if piece[1] == 'k': # it's the king
            return Referee.get_king_moves(board_matrix, pos)
        return None