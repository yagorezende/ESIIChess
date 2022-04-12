from typing import Dict, List, Tuple

# NOTE - indexes are (column, row)

# NOTE - mapping the movements for each chess piece
_pieces_movements_deltas: Dict[str, List[Tuple[int, int]]] = {
    "king": [
        (-1,-1),( 0,-1),( 1,-1),
        (-1, 0),        ( 1, 0),
        (-1, 1),( 0, 1),( 1, 1),
        (-2, 0),        ( 2, 0)  # NOTE - occur when castling
    ],
    "queen":
        _v_direction_deltas  + _h_direction_deltas + \
        _d1_direction_deltas + _d2_direction_deltas,
    "rook":
        _v_direction_deltas  + _h_direction_deltas,
    "bishop":
        _d1_direction_deltas + _d2_direction_deltas,
    "knight": [
        (-1,-2),(-2,-1),
        ( 1,-2),( 2,-1),
        ( 1, 2),( 2, 1),
        (-1, 2),(-2, 1)
    ],
    "pawn": [
        ( 0,-1),( 0,-2),
        ( 0, 1),( 0, 2),
        (-1,-1),( 1,-1),  # NOTE - when capturing
        (-1, 1),( 1, 1)   # NOTE - when capturing
    ]
}


def gen_piece_positions(_type: str, cur_col: int, cur_row: int) -> List[Tuple[int, int]]:
    """
    Generate a list of positions inside the board that the piece may go (further
    rules must be applied).
    `return:` list of pairs (column, row)
    """
    try:
        mv_deltas =  _pieces_movements_deltas[_type.lower()]
    except KeyError:
        raise ValueError('Got unexpected value for _type')
    res = []
    for (i, j) in mv_deltas:
        new_col = cur_col + i
        new_row = cur_row + j
        # REVIEW - hardcoded boardsize
        if ( 0 <= new_col < 8 and 0 <= new_row < 8 ) and \
           ( new_col != cur_col or new_row != cur_row ):
            res.append( (new_col, new_row) )
    return res
