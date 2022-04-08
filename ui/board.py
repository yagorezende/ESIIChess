from typing import List

import pygame

PIECES_ORDER = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]


class ChessPiece:
    def __init__(self, _type="pawn", color="white", x=0, y=0, offset=0):
        self.sprite = pygame.image.load(f"assets/images/{_type}-{color}.png").convert_alpha()
        self.x = x
        self.y = y
        self.offset = offset

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
        return self.sprite, (self.x + self.offset, self.y + self.offset)


class Board:
    def __init__(self):
        self.grid: List[BoardTile] = []
        self.pieces: List[ChessPiece] = []
        self.offset = 0

    def init_board(self):
        white = False
        for i in range(8):
            for j in range(8):
                self.grid.append(BoardTile(white, 80 * j, 80 * i, self.offset))
                white = not white
            white = not white

        # add pieces
        for i in range(8):
            # white
            self.pieces.append(ChessPiece(x=i * 80, y=6 * 80, offset=self.offset))

            try:
                self.pieces.append(ChessPiece(_type=PIECES_ORDER[i], x=i * 80, y=7*80, offset=self.offset))
            except Exception as e:
                print(f"Could not import {PIECES_ORDER[i]}-white-png")

            # black
            self.pieces.append(ChessPiece(color="dark", x=i * 80, y=1 * 80, offset=self.offset))
            try:
                self.pieces.append(
                    ChessPiece(_type=PIECES_ORDER[i], x=i * 80, y=0, color="dark", offset=self.offset))
            except Exception as e:
                print(f"Could not import {PIECES_ORDER[i]}-white-png")

    def on_render(self, surface):
        for tile in self.grid:
            surface.blit(*tile.render())

        for piece in self.pieces:
            surface.blit(*piece.render())
