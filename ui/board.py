from typing import List, Tuple
from logic.rule_machine import RuleMachine
import pygame

TILE_SIZE = 80  # px
PIECES_ORDER = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]


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

    def get_board_pos(self) -> Tuple[int, int]:
        return int(self.x / TILE_SIZE - self.offset), int(self.y / TILE_SIZE - self.offset)

    def on_event(self, event):
        if self.catch_click(event) and self._is_over():
            print(f"Click on {self._type} {self.color} on position {self.get_board_pos()}")
            board_state = self.board.get_board_matrix()  # this call gets the board state

            positions = self.board.rule_machine.get_valid_moves(self, self.board.get_board_matrix())
            print(f'''piece: {self._type} {self.color}\n\t{len(positions)} new position{'s' if len(positions) else ''}\n\t{positions}''')

            self._event_keeper = None  # release the event keeper

    def get_type(self) -> str:
        return self._type

    def catch_click(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONUP:
            self._event_keeper = event
            return False
        elif self._event_keeper is not None and self._event_keeper.type == pygame.MOUSEBUTTONUP:
            return True
        return False

    def _is_over(self) -> bool:
        return self._event_keeper is not None and self.x < self._event_keeper.pos[0] < self.x + TILE_SIZE and self.y < \
               self._event_keeper.pos[1] < self.y + TILE_SIZE

    def render(self):
        return self.sprite, (self.x + self.offset, self.y + self.offset)


class BoardTile:
    def __init__(self, dark=True, x=0, y=0, offset=0):
        if dark:
            self.sprite = pygame.image.load("assets/images/tile-dark.png").convert()
        else:
            self.sprite = pygame.image.load("assets/images/tile-light.png").convert()
        self.x = x
        self.y = y
        self.offset = offset

    def render(self):
        return self.sprite, (self.y + self.offset, self.x + self.offset)


class Board:
    def __init__(self):
        self.grid: List[BoardTile] = []
        self.pieces: List[ChessPiece] = []
        self.rule_machine = RuleMachine()
        self.offset = 0

    def init_board(self):
        white = False
        for i in range(8):
            for j in range(8):
                self.grid.append(BoardTile(white, TILE_SIZE * j, TILE_SIZE * i, self.offset))
                white = not white
            white = not white

        # add pieces
        for i in range(8):
            # white
            self.pieces.append(ChessPiece(self, x=i * TILE_SIZE, y=6 * TILE_SIZE, offset=self.offset))

            try:
                self.pieces.append(
                    ChessPiece(self, _type=PIECES_ORDER[i], x=i * TILE_SIZE, y=7 * TILE_SIZE, offset=self.offset))
            except Exception as e:
                print(f"Could not import {PIECES_ORDER[i]}-white-png")

            # black
            self.pieces.append(ChessPiece(self, color="dark", x=i * TILE_SIZE, y=1 * TILE_SIZE, offset=self.offset))
            try:
                self.pieces.append(
                    ChessPiece(self, _type=PIECES_ORDER[i], x=i * TILE_SIZE, y=0, color="dark", offset=self.offset))
            except Exception as e:
                print(f"Could not import {PIECES_ORDER[i]}-white-png")

    def on_event(self, event):
        for piece in self.pieces:
            piece.on_event(event)

    def get_board_matrix(self) -> List[List[ChessPiece]]:
        matrix = [[None] * 8 for i in range(8)]  # matrix 8X8
        for piece in self.pieces:
            x, y = piece.get_board_pos()
            matrix[x][y] = piece
        return matrix

    def on_render(self, surface):
        for tile in self.grid:
            surface.blit(*tile.render())

        for piece in self.pieces:
            surface.blit(*piece.render())
