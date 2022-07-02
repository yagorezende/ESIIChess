import unittest

from typing import Dict, List
from logic.referee import Referee
from ui.board import ChessPiece

pieces: Dict[str, ChessPiece] = {}
board_matrix: List[List[str]] = [
            ['br1', 'bn2', 'bb3', 'bq4', 'bk5', 'bb6', 'bn7', 'br8'],
            ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
            ['wr1', 'wn2', 'wb3', 'wq4', 'wk5', 'wb6', 'wn7', 'wr8']
        ]

obj = Referee(board_matrix, pieces)

