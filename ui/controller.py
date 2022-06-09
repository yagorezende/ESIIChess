from typing import Dict, List
from logic.const import TILE_SIZE
from logic.referee import Referee
from logic.tools import show_board_matrix
import pygame

from ui.board import BoardTile, ChessPiece
from ui.screens.navigator import Navigator
from ui.screens.piece_selection import PieceSelection
from logic.rcp_command import RetrieveChosenPiece

class Controller:

    def __init__(self):
        self.grid: List[BoardTile] = []
        self.pieces: Dict[str, ChessPiece] = {}
        self.board_matrix: List[List[str]] = [
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
        self.selected = None
        self.offset = 0
        self.highlight = []
        self._PP_COUNTER_VALUE = 1
        self._pp_counter_until_piece_selection = self._PP_COUNTER_VALUE
        self._pp_look_promotion = False

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
            self.pieces['wp' + str(i + 1)] = ChessPiece(x=i * TILE_SIZE, y=6 * TILE_SIZE, offset=self.offset)
            try:
                self.pieces['w' + order[i] + str(i + 1)] = ChessPiece(type=order[i], x=i * TILE_SIZE, y=7 * TILE_SIZE,
                                                                      offset=self.offset)
            except Exception as e:
                print(f"Could not import w{order[i]}.png")

            # black
            self.pieces['bp' + str(i + 1)] = ChessPiece(color='b', x=i * TILE_SIZE, y=1 * TILE_SIZE, offset=self.offset)
            try:
                self.pieces['b' + order[i] + str(i + 1)] = ChessPiece(color='b', type=order[i], x=i * TILE_SIZE,
                                                                      y=0 * TILE_SIZE, offset=self.offset)
            except Exception as e:
                print(f"Could not import b{order[i]}.png")

    def transform(self, r, c):

        piece = self.pieces[self.selected]
        piece_pos = piece.get_board_pos()

        if piece.type == 'k':
            rook = None
            displacement = c - piece_pos[1]
            if displacement == 2:  # the player is trying a small castle
                self.board_matrix[r][c - 1] = self.board_matrix[r][c + 1]  # update matrix
                self.board_matrix[r][c + 1] = None  # update matrix
                rook = self.pieces[self.board_matrix[r][c - 1]]
                rook.move(((c - 1) * TILE_SIZE, r * TILE_SIZE))
            elif displacement == -2:  # the player is trying a big castle
                self.board_matrix[r][c + 1] = self.board_matrix[r][c - 2]  # update matrix
                self.board_matrix[r][c - 2] = None  # update matrix
                rook = self.pieces[self.board_matrix[r][c + 1]]
                rook.move(((c + 1) * TILE_SIZE, r * TILE_SIZE))
            if rook:
                rook.has_moved = True
            piece.has_moved = True  # update instance
        elif piece.type == 'r':  # update instance
            piece.has_moved = True
        elif piece.type == 'p':  # update instance
            if abs(r - piece_pos[0]) == 2: # double step
                piece.has_jumped = True
            else:
                piece.has_jumped = False
                if c != piece_pos[1] and not self.board_matrix[r][c]:  # en passant
                    self.pieces[self.board_matrix[piece_pos[0]][c]].active = False
                    self.board_matrix[piece_pos[0]][c] = None
                    self.referee.no_progression_counter = 0
                    self.referee.pieces_counter -= 1

        self.board_matrix[r][c] = self.selected  # update matrix
        self.board_matrix[piece_pos[0]][piece_pos[1]] = None  # update matrix

        piece.move((c * TILE_SIZE, r * TILE_SIZE))  # move sprite

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
            if target[0] == self.referee.turn_color:  # if it's a player's piece
                self.handle_highlight_hint(target)
                self.grid[c * 8 + r].turn_light(True)
                self.selected = target
            elif self.selected:  # the player wants to kill an enemy piece
                if (r, c) in self.referee.get_possible_moves(self.selected):
                    self.pieces[self.board_matrix[r][c]].active = False
                    self.transform(r, c)
                    self.referee.no_progression_counter = 0
                    self.referee.pieces_counter -= 1
                    self.referee.turn()
                self.handle_highlight_hint(None, turnoff = True, pos=(r, c))
                self.selected = None

        elif self.selected:  # click on empty slot, a piece was previously selected
            if (r, c) in self.referee.get_possible_moves(self.selected):
                self.transform(r, c)
                if self.selected[1] == 'p':
                    self.referee.no_progression_counter = 0
                else:
                    self.referee.no_progression_counter += 1
                self.referee.turn()
            self.handle_highlight_hint(None, turnoff = True)
            self.selected = None

        self._pp_look_promotion = True

    def on_loop(self) -> None:
        self.manage_pawns_promotion()
        return None

    def on_render(self, surface):
        for tile in self.grid:
            surface.blit(*tile.render())

        for piece in self.pieces.values():
            if piece.active:
                surface.blit(*piece.render())

    def handle_highlight_hint(self, target: str, turnoff = False, pos: tuple = None):
        if target == self.selected:
            return

        # turn off old path
        if self.selected or turnoff:
            for tile in self.grid:
                tile.turn_light()

        if not turnoff:
            # turn on path
            for pos in self.referee.get_possible_moves(target):
                x, y = pos
                # print(f"hightlight {y * 8 + x} for pos = {pos}")
                self.grid[y * 8 + x].turn_light(True)

    def manage_pawns_promotion(self) -> None:
        """
        Test if there is a pawn to be promoted, and if there is promote it.
        """
        # NOTE - look for promotions only after an click event; saving frames;
        if not self._pp_look_promotion:
            return
        # NOTE - handle promotion when counter is on 0
        if self._pp_counter_until_piece_selection == 0:
            # NOTE - reset counter
            self._pp_counter_until_piece_selection = self._PP_COUNTER_VALUE
            self._pp_look_promotion = False

            pawn_k = self.referee.get_pawn_promote()
            if (pawn_k):
                # NOTE - promote to a new type
                self.open_piece_selection_screen(pawn_k)
        elif self._pp_counter_until_piece_selection > 0:
            self._pp_counter_until_piece_selection -= 1

    def promote_pawn(self, pawn_k: str, new_type: str):
        """
        Promote the pawn specified by pawn_k to the specified type.
        """
        piece = self.pieces.pop(pawn_k)
        new_piece = ChessPiece(
            type=new_type,
            color=piece.color,
            x=piece.x, y=piece.y,
            offset=piece.offset)
        # NOTE - +8 to solve colisions ex. wp1 -> wr1 replacing the existing wr1
        new_key = f"{pawn_k[0]}{new_type}{int(pawn_k[2:])+8}"
        r, c = piece.get_board_pos()
        self.pieces[new_key] = new_piece
        self.board_matrix[r][c] = new_key

    def open_piece_selection_screen(self, pawn_k: str):
        scr = PieceSelection()
        scr.show_color = pawn_k[0]
        scr.command_on_leave = RetrieveChosenPiece(pawn_k, scr, self)
        Navigator().show(scr)

    def check_status(self) -> None:
        """
        Call the referee to check the game status.
        """
        return self.referee.update_status()