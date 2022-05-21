from typing import Dict, List, Tuple

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