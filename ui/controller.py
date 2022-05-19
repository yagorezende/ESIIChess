from typing import Dict, List
from logic.const import TILE_SIZE
import pygame
from logic.referee import Referee
from logic.tools import show_board_matrix

from ui.piece import ChessPiece

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


class Controller:
    def __init__(self):
        self.grid: List[BoardTile] = []
        self.pieces:Dict[str, ChessPiece] = {}
        self.board_matrix = [
            ['br1', 'bn2', 'bb3', 'bq4', 'bk5', 'bb6', 'bn7', 'br8'],
            ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],		
			[None] * 8,
			[None] * 8,
			[None] * 8,
			[None] * 8,
            ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
            ['wr1', 'wn2', 'wb3', 'wq4', 'wk5', 'wb6', 'wn7', 'wr8']			
		]
        self.referee = Referee(self.board_matrix, self.pieces)
        self.selected:ChessPiece = None
        self.player_color = 'w'
        self.offset = 0

    def init_board(self):
        # add tiles
        white = False
        for i in range(8):
            for j in range(8):
                self.grid.append(BoardTile(white, TILE_SIZE * j, TILE_SIZE * i, self.offset))
                white = not white
            white = not white
        # add pieces
        order = ["r", "n", "b", "q", "k", "b", "n", "r"]
        for i in range(8):
            # white
            self.pieces['wp' + str(i+1)] = ChessPiece(self, x=i * TILE_SIZE, y=6 * TILE_SIZE, offset=self.offset)
            try:
                self.pieces['w' + order[i] + str(i+1)] = ChessPiece(self, _type=order[i], x=i * TILE_SIZE, y=7 * TILE_SIZE, offset=self.offset)
            except Exception as e:
                print(f"Could not import w{order[i]}.png")

            # black
            self.pieces['bp' + str(i+1)] = ChessPiece(self, color='b', x=i * TILE_SIZE, y=1 * TILE_SIZE, offset=self.offset)
            try:
                self.pieces['b' + order[i] + str(i+1)] = ChessPiece(self, color='b', _type=order[i], x=i * TILE_SIZE, y=0 * TILE_SIZE, offset=self.offset)
            except Exception as e:
                print(f"Could not import b{order[i]}.png")

    def transform(self, x, y):
        self.board_matrix[x][y] = self.selected
        aux = self.pieces[self.selected].get_board_pos()
        self.board_matrix[aux[0]][aux[1]] = None
        self.pieces[self.selected].move((y * TILE_SIZE, x * TILE_SIZE))
        self.selected = None
        print('\nBoard Matrix:\n')
        show_board_matrix(self.board_matrix)
        print()
        
    def on_click(self):  # TODO: callings to referee

        y, x = pygame.mouse.get_pos()
        x //= TILE_SIZE
        y //= TILE_SIZE
        target = self.board_matrix[x][y]
        print(f"Click on {(x, y)}")

        if target:  # click on piece
            if target[0] == self.player_color:  # if it's a player's piece
                self.selected = target
                print(f"Selected piece: {target}\nPossible moves: {self.referee.get_possible_moves(self.selected)}")
            elif self.selected:  # player wants to kill an enemie's piece
                piece = self.pieces[self.board_matrix[x][y]]
                if ((x, y) in self.referee.get_possible_moves(self.selected)):
                    piece.active = False
                    self.transform(x, y)
                    return
        elif self.selected:  # click on empty slot, a piece was previously selected
            if ((x, y) in self.referee.get_possible_moves(self.selected)):
                self.transform(x, y)
                return

    def on_render(self, surface):
        for tile in self.grid:
            surface.blit(*tile.render())

        for piece in self.pieces.values():
            if piece.active:
                surface.blit(*piece.render())