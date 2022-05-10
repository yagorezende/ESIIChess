from typing import Tuple
import pygame

from logic.const import TILE_SIZE

class ChessPiece:
    def __init__(self, board, _type="p", color="w", x=0, y=0, offset=0):
        self.sprite = pygame.image.load(f"assets/images/{color}{_type}.png").convert_alpha()
        self.board = board
        self._type = _type
        self.color = color
        self.x = x
        self.y = y
        self.active = True
        self.offset = offset
        self._event_keeper = None
    
    def move(self, pos:tuple):
        self.x, self.y = pos

    def get_board_pos(self) -> Tuple[int, int]:
        return int(self.x / TILE_SIZE - self.offset), int(self.y / TILE_SIZE - self.offset)

    def get_type(self) -> str:
        return self._type

    def render(self):
        return self.sprite, (self.x + self.offset, self.y + self.offset)