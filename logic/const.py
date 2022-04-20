from typing import Dict, List, Tuple

# NOTE - indexes are (column, row)
RANGE_ALL_BOARD = range(-7, 8)

# NOTE - deltas for all possible vertical positions
V_DIRECTION_DELTAS: List[Tuple[int, int]] = [(int(0), i) for i in RANGE_ALL_BOARD]

# NOTE - deltas for all possible horizontal positions
H_DIRECTION_DELTAS: List[Tuple[int, int]] = [(i, int(0)) for i in RANGE_ALL_BOARD]

# NOTE - deltas for all possible positions on the main diagonal
D1_DIRECTION_DELTAS: List[Tuple[int, int]] = [(i, i) for i in RANGE_ALL_BOARD]

# NOTE - deltas for all possible positions on the secondary diagonal
D2_DIRECTION_DELTAS: List[Tuple[int, int]] = [(-i, i) for i in RANGE_ALL_BOARD]

# NOTE - mapping the movements for each chess piece
PIECES_MOVEMENTS_DELTAS: Dict[str, List[Tuple[int, int]]] = {
    "king": [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1),
        (-2, 0), (2, 0)  # NOTE - occur when castling
    ],
    "queen":
        V_DIRECTION_DELTAS + H_DIRECTION_DELTAS + D1_DIRECTION_DELTAS + D2_DIRECTION_DELTAS,
    "rook":
        V_DIRECTION_DELTAS + H_DIRECTION_DELTAS,
    "bishop":
        D1_DIRECTION_DELTAS + D2_DIRECTION_DELTAS,
    "knight": [
        (-1, -2), (-2, -1),
        (1, -2), (2, -1),
        (1, 2), (2, 1),
        (-1, 2), (-2, 1)
    ],
    "pawn": [
        (0, -1), (0, -2),
        (0, 1), (0, 2),
        (-1, -1), (1, -1),  # NOTE - when capturing
        (-1, 1), (1, 1)  # NOTE - when capturing
    ]
}


def gen_piece_positions(_type: str, cur_col: int, cur_row: int) -> List[Tuple[int, int]]:
    """
    Generate a list of positions inside the board that the piece may go (further
    rules must be applied).
    `return:` list of pairs (column, row)
    """
    try:
        mv_deltas = PIECES_MOVEMENTS_DELTAS[_type.lower()]
    except KeyError:
        raise ValueError('Got unexpected value for _type')
    res = []
    for (i, j) in mv_deltas:
        new_col = cur_col + i
        new_row = cur_row + j
        # REVIEW - hardcoded boardsize
        if (0 <= new_col < 8 and 0 <= new_row < 8) and \
                (new_col != cur_col or new_row != cur_row):
            res.append((new_col, new_row))
    return res


if __name__ == '__main__':
    for piece in PIECES_MOVEMENTS_DELTAS.keys():
        positions = gen_piece_positions(piece, 4, 4)
        print(f'''piece: {piece}\n\t{len(positions)} new position{'s' if len(positions) else ''}\n\t{positions}''')
