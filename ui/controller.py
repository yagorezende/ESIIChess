from typing import Dict, List
from logic.const import TILE_SIZE
import pygame
from logic.referee import Referee
from logic.tools import show_board_matrix

from ui.board import BoardTile, ChessPiece

class Controller:
    def __init__(self):
        self.grid:List[BoardTile] = []
        self.pieces:Dict[str, ChessPiece] = {}
        self.board_matrix:List[List[str]] = [
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
        self.player_color:str = 'w'
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
            self.pieces['wp' + str(i+1)] = ChessPiece(x=i * TILE_SIZE, y=6 * TILE_SIZE, offset=self.offset)
            try:
                self.pieces['w' + order[i] + str(i+1)] = ChessPiece(type=order[i], x=i * TILE_SIZE, y=7 * TILE_SIZE, offset=self.offset)
            except Exception as e:
                print(f"Could not import w{order[i]}.png")

            # black
            self.pieces['bp' + str(i+1)] = ChessPiece(color='b', x=i * TILE_SIZE, y=1 * TILE_SIZE, offset=self.offset)
            try:
                self.pieces['b' + order[i] + str(i+1)] = ChessPiece(color='b', type=order[i], x=i * TILE_SIZE, y=0 * TILE_SIZE, offset=self.offset)
            except Exception as e:
                print(f"Could not import b{order[i]}.png")

    def transform(self, r, c):
        piece = self.pieces[self.selected]
        piece_pos = piece.get_board_pos()

        self.board_matrix[r][c] = self.selected # update matrix
        self.board_matrix[piece_pos[0]][piece_pos[1]] = None # update matrix

        if piece.type == 'k':
            rook = None
            displacement = c - piece_pos[1]
            if displacement == 2: # the player is trying small castle
                print('small castle')
                self.board_matrix[r][c-1] = self.board_matrix[r][c+1] # update matrix
                self.board_matrix[r][c+1] = None # update matrix
                rook = self.pieces[self.board_matrix[r][c-1]]
                rook.move(((c-1) * TILE_SIZE, r * TILE_SIZE))
            if displacement == -2: # the player is trying big castle
                print('big castle')
                self.board_matrix[r][c+1] = self.board_matrix[r][c-2] # update matrix
                self.board_matrix[r][c-2] = None # update matrix
                rook = self.pieces[self.board_matrix[r][c+1]]
                rook.move(((c+1) * TILE_SIZE, r * TILE_SIZE))
            if rook:
                rook.has_moved = True
            piece.has_moved = True # update instance
            print('a king has moved')
        elif piece.type == 'r': # update instance
            piece.has_moved = True
            print('a rook has moved')
        elif piece.type == 'p': # update instance
            if abs(c - piece_pos[0]) == 2:
                piece.has_jumped = True
                print('double step pawn')

        piece.move((c * TILE_SIZE, r * TILE_SIZE)) # move sprite

        print('\nBoard Matrix:\n')
        show_board_matrix(self.board_matrix)
        print()
        
    def on_click(self):
        print('-' * 50)
        c, r = pygame.mouse.get_pos()
        r //= TILE_SIZE
        c //= TILE_SIZE
        target = self.board_matrix[r][c]
        print(f"Click on {(r, c)}")

        if target:  # click on piece
            if target[0] == self.player_color:  # if it's a player's piece
                self.selected = target
                print(f"Selected piece: {target}\nPossible moves: {self.referee.get_possible_moves(self.selected)}")
            elif self.selected:  # player wants to kill an enemie's piece
                if ((r, c) in self.referee.get_possible_moves(self.selected)):
                    self.pieces[self.board_matrix[r][c]].active = False
                    self.transform(r, c)
                self.selected = None
        elif self.selected:  # click on empty slot, a piece was previously selected
            if ((r, c) in self.referee.get_possible_moves(self.selected)):
                self.transform(r, c)
            self.selected = None

    def on_render(self, surface):
        for tile in self.grid:
            surface.blit(*tile.render())

        for piece in self.pieces.values():
            if piece.active:
                surface.blit(*piece.render())