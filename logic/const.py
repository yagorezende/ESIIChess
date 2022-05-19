from typing import Dict, List, Tuple

# NOTE - mapping the movements for each chess piece
DELTAS: Dict[str, List[Tuple[int, int]]] = {
    "king": [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1),
        (-2, 0), (2, 0)  # NOTE - occur when castling
    ],
    "knight": [
        (-1, -2), (-2, -1),
        (1, -2), (2, -1),
        (1, 2), (2, 1),
        (-1, 2), (-2, 1)
    ],
    "pawnUp": [
        (-1, 0), (-2, 0),
        (-1, -1), (-1, 1),  # NOTE - when capturing
    ],
    "pawnDown": [
        (1, 0), (2, 0),
        (1, -1), (1, 1)  # NOTE - when capturing
    ]
}

TILE_SIZE = 80