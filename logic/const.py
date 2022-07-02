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

INFINITE = 2**31-1
TILE_SIZE = 80
REPETITIONS_FOR_DRAW = 3
NO_PROGRESSION_LIMIT = 50
INITIAL_STATE_1 = 'brbnbbbqbkbbbnbrbpbpbpbpbpbpbpbp00000000000000000000000000000000wpwpwpwpwpwpwpwpwrwnwbwqwkwbwnwr'
INITIAL_STATE_2 = 'wrwnwbwqwkwbwnwrwpwpwpwpwpwpwpwp00000000000000000000000000000000bpbpbpbpbpbpbpbpbrbnbbbqbkbbbnbr'
SAVE_FOLDER = 'logic\\gamestate\\'
BOARD_MATRIX_1 = [
    ['br1', 'bn2', 'bb3', 'bq4', 'bk5', 'bb6', 'bn7', 'br8'],
    ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
    ['wr1', 'wn2', 'wb3', 'wq4', 'wk5', 'wb6', 'wn7', 'wr8']
]
BOARD_MATRIX_2 = [
    ['wr1', 'wn2', 'wb3', 'wq4', 'wk5', 'wb6', 'wn7', 'wr8'],
    ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
    ['br1', 'bn2', 'bb3', 'bq4', 'bk5', 'bb6', 'bn7', 'br8']
]
