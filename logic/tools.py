def show_board_matrix(matrix):
    for row in matrix:
        for cell in row:
            if cell:
                print(f'''{cell : ^5}''', end='')
            else:
                print(f'''{'-' : ^5}''', end='')
        print()
    return