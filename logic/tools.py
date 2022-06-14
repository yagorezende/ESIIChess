from typing import List, Tuple


def show_board_matrix(matrix):
    for row in matrix:
        for cell in row:
            if cell:
                print(f'''{cell : ^5}''', end='')
            else:
                print(f'''{'-' : ^5}''', end='')
        print()
    return

def letter_to_color(l):
    if l == 'b': return 'black'
    if l == 'w': return 'white'
    return None

def add_tuples(a, b):
	return a[0] + b[0], a[1] + b[1]

def count_material_advantage(board_matrix, color) -> int:
    advantage = 0
    for row in board_matrix:
        for code in row:
            if code and code[1] != 'k':
                factor = 1 if code[0] == color else -1
                if code[1] == 'p': # 1 for pawns
                    advantage += factor
                elif code[1] == 'r': # 5 for rooks
                    advantage += factor * 5
                elif code[1] == 'q': # 9 for queens
                    advantage += factor * 9
                else: # 3 for knights and bishops
                    advantage += factor * 3
    return advantage

def transform(board_matrix, p1, p2) -> List[Tuple[tuple, bool]]:
    r, c = p2[0], p2[1]
    piece_code = board_matrix[p1[0]][p1[1]]
    special = []
    if piece_code[1] == 'k':
        displacement = c - p1[1]
        special.append((p1, True))
        if displacement == 2:  # the player is trying a small castle
            board_matrix[r][c - 1] = board_matrix[r][c + 1]  # update matrix
            board_matrix[r][c + 1] = None  # update matrix
            special.append(((r, c-1), True))
        elif displacement == -2:  # the player is trying a big castle
            board_matrix[r][c + 1] = board_matrix[r][c - 2]  # update matrix
            board_matrix[r][c - 2] = None  # update matrix
            special.append(((r, c+1), True))
    elif piece_code[1] == 'r':
        special.append((p1, True))
    elif piece_code[1] == 'p':  # update instance
        if abs(r - p1[0]) == 2: # double step
            special.append((p1, True))
        else:
            special.append((p1, False))
            if c != p1[1] and not board_matrix[r][c]:  # en passant
                board_matrix[p1[0]][c] = None  
        board_matrix[r][c] = piece_code  # update matrix
        board_matrix[p1[0]][p1[1]] = None  # update matrix
        return