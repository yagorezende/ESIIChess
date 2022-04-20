from typing import List, Tuple
from . import const


class RuleMachine:
    def get_valid_moves(self, piece, board: List[List]) -> List[Tuple[int, int]]:
        """
            Generate a list of positions inside the board that the piece may go (further
            rules must be applied).
            `return:` list of pairs (column, row)
            """
        try:
            mv_deltas = const.PIECES_MOVEMENTS_DELTAS[piece._type]
        except KeyError:
            raise ValueError('Got unexpected value for _type')
        res = []
        cur_col, cur_row = piece.get_board_pos()
        for (i, j) in mv_deltas:
            new_col = cur_col + i
            new_row = cur_row + j
            # REVIEW - hardcoded boardsize
            if (0 <= new_col < 8 and 0 <= new_row < 8) and (new_col != cur_col or new_row != cur_row):
                res.append((new_col, new_row))
        return res
