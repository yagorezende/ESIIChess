from typing import Dict, List, Tuple
from enum import Enum

class Status(Enum):

    NORMAL = 0
    CHECK = 1
    CHECKMATE = 2
    DRAW_REPETITION = 3
    DRAW_STALEMATE = 4
    DRAW_MATERIAL = 5
    DRAW_PROGRESSION = 6

# NOTE - mapping the movements for each chess piece
DELTAS: Dict[str, List[Tuple[int, int]]] = {
    "king": [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1)
    ],
    "knight": [
        (-1, -2), (-2, -1),
        (1, -2), (2, -1),
        (1, 2), (2, 1),
        (-1, 2), (-2, 1)
    ]
}

TILE_SIZE = 80
REPETITIONS_FOR_DRAW = 3
NO_PROGRESSION_LIMIT = 50
INITIAL_STATE_1 = 'brbnbbbqbkbbbnbrbpbpbpbpbpbpbpbp00000000000000000000000000000000wpwpwpwpwpwpwpwpwrwnwbwqwkwbwnwr'
INITIAL_STATE_2 = 'wrwnwbwqwkwbwnwrwpwpwpwpwpwpwpwp00000000000000000000000000000000bpbpbpbpbpbpbpbpbrbnbbbqbkbbbnbr'
