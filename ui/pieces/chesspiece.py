import pygame

from typing import List, Tuple
import ui.board


class ChessPiece:
    def __init__(self, board, _type="pawn", color="white", x=0, y=0, offset=0):
        self.sprite = pygame.image.load(f"assets/images/{_type}-{color}.png").convert_alpha()
        self.board = board
        self._type = _type
        self.color = color
        self.x = x
        self.y = y
        self.offset = offset
        self._event_keeper = None
        self.value = 0  # pawn1, bishop3, knight3, rook5, queen9

    def get_board_pos(self) -> Tuple[int, int]:
        return int(self.x / ui.board.TILE_SIZE - self.offset), int(self.y / ui.board.TILE_SIZE - self.offset)

    def on_event(self, event):
        if self.catch_click(event) and self._is_over():
            print(f"Click on {self._type} {self.color} on position {self.get_board_pos()}")
            board_state = self.board.get_board_matrix()  # this call gets the board state
            self._event_keeper = None  # release the event keeper

    def catch_click(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP:
            self._event_keeper = event
            return False
        elif self._event_keeper is not None and self._event_keeper.type == pygame.MOUSEBUTTONUP:
            return True
        return False

    def _is_over(self) -> bool:
        return self._event_keeper is not None and self.x < self._event_keeper.pos[0] < self.x + ui.board.TILE_SIZE and self.y < self._event_keeper.pos[1] < self.y + ui.board.TILE_SIZE

    def render(self):
        return self.sprite, (self.x + self.offset, self.y + self.offset)
