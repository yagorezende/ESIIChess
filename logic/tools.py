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
