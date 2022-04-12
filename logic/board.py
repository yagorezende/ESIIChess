from typing import List, Tuple

# NOTE - indexes are (column, row)

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
