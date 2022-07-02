from typing import List

from logic.const import Status

# Visual

def show_dic(dic: dict):
    for key, value in dic.items():
        print(key, value)
    return None

def show_board_matrix(matrix: List[List[str]]):
    for row in matrix:
        for cell in row:
            if cell:
                print(f'''{cell : ^5}''', end='')
            else:
                print(f'''{'-' : ^5}''', end='')
        print()
    return

def board_to_str(matrix: List[List[str]]):
    matrix_str = ""
    for row in matrix:
        for cell in row:
            if cell:
                matrix_str += f'''{cell : ^5}'''
            else:
                matrix_str += f'''{'-' : ^5}'''
        matrix_str += '\n'
    return matrix_str

def letter_to_color(l: str):
    if l == 'b': return 'black'
    if l == 'w': return 'white'
    return None

# Math

def add_tuples(a: int, b: int) -> tuple:
	return a[0] + b[0], a[1] + b[1]

def count_material_advantage(board_matrix: List[List[str]], color: str) -> int:
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

# Others

def str_to_status(name: str) -> Status:
    if name == 'NORMAL':
        return Status.NORMAL
    elif name == 'CHECK':
        return Status.CHECK
    elif name == 'CHECKMATE':
        return Status.CHECKMATE
    elif name == 'DRAW_REPETITION':
        return Status.DRAW_REPETITION
    elif name == 'DRAW_STALEMATE':
        return Status.DRAW_STALEMATE
    elif name == 'DRAW_MATERIAL':
        return Status.DRAW_MATERIAL
    elif name == 'DRAW_PROGRESSION':
        return Status.DRAW_PROGRESSION
    return None