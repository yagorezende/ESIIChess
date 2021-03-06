import json
import os
from typing import Dict, List

import pygame

from logic.bot import Bot
from logic.const import BOARD_MATRIX_1, BOARD_MATRIX_2, SAVE_FOLDER, TILE_SIZE, Status
from logic.game_overall_context import GameOverallContext
from logic.rcp_command import RetrieveChosenPiece
from logic.referee import Referee
from logic.tools import count_material_advantage, letter_to_color
from logic.tools import show_board_matrix
from ui.board import BoardTile, ChessPiece
from ui.screens.endgame_screen import EndGameScreen
from ui.screens.navigator import Navigator
from ui.screens.piece_selection import PieceSelection
from logic.turn_conditions import TurnCondition


class Controller:

    def __init__(self):
        self.grid: List[BoardTile] = []
        self.pieces: Dict[str, ChessPiece] = {}
        if GameOverallContext().is_white_bottom():
            self.board_matrix = [row.copy() for row in BOARD_MATRIX_1]
        else:
            self.board_matrix = [row.copy() for row in BOARD_MATRIX_2]

        self.referee = Referee(self.board_matrix, self.pieces)
        self.bot = Bot(
            level=2,
            referee=self.referee,
            board_matrix=self.board_matrix,
            pieces=self.pieces,
            color=GameOverallContext().get_opponent_color(),
            bottomup_orientation=False)
        self.multiplayer = GameOverallContext().is_multiplayer()
        self.selected = None
        self.offset = 0
        self.highlight = []
        self._wait_to_open_selection_screen = True
        self.board_edge = TILE_SIZE * 8
        self.infos = pygame.image.load("assets/images/Commands.png").convert_alpha()
        self.turn_condition = TurnCondition(self.turn)

    def init_board(self):
        # add tiles
        white = False
        for i in range(8):
            for j in range(8):
                self.grid.append(BoardTile(white, TILE_SIZE * j, TILE_SIZE * i, self.offset))
                white = not white
            white = not white
        # add pieces
        self.load_pieces()
        return None

    def transform(self, r, c):
        piece = self.pieces[self.selected]
        piece_pos = piece.get_board_pos()
        piece.has_moved = True  # update instance
        white_bottom = GameOverallContext().get_color() == 'w'
        factor = 1 if white_bottom else - 1

        if piece.type == 'k':
            rook = None
            displacement = c - piece_pos[1]
            if displacement == 2 and white_bottom or displacement == -2 and not white_bottom:  # the player is trying a small castle
                # if white_bottom:
                self.board_matrix[r][c - factor] = self.board_matrix[r][c + factor]  # update matrix
                self.board_matrix[r][c + factor] = None  # update matrix
                rook = self.pieces[self.board_matrix[r][c - factor]]
                rook.move(((c - factor) * TILE_SIZE, r * TILE_SIZE))
                rook.has_moved = True
            elif displacement == -2 and GameOverallContext().get_color() == 'w' \
                    or displacement == 2 and GameOverallContext().get_color() == 'b':  # the player is trying a big castle
                self.board_matrix[r][c + factor] = self.board_matrix[r][c - 2 * factor]  # update matrix
                self.board_matrix[r][c - 2 * factor] = None  # update matrix
                rook = self.pieces[self.board_matrix[r][c + factor]]
                rook.move(((c + factor) * TILE_SIZE, r * TILE_SIZE))
                rook.has_moved = True
        elif piece.type == 'p':  # update instance
            if abs(r - piece_pos[0]) == 2:  # double step
                self.referee.rushed_pawn = (r, c)
            else:
                if c != piece_pos[1] and not self.board_matrix[r][c]:  # en passant
                    self.pieces[self.board_matrix[piece_pos[0]][c]].active = False
                    self.board_matrix[piece_pos[0]][c] = None
                    self.referee.no_progression_counter = 0
                    self.referee.pieces_counter -= 1
        self.board_matrix[r][c] = self.selected  # update matrix
        self.board_matrix[piece_pos[0]][piece_pos[1]] = None  # update matrix

        piece.move((c * TILE_SIZE, r * TILE_SIZE))  # move sprite
        return

    def on_click(self, pos):
        if not self.multiplayer and self.referee.turn_color == self.bot.color:
            return
        r = pos[1] // TILE_SIZE
        c = pos[0] // TILE_SIZE
        print('-' * 50)
        print(f"Click on {(r, c)}")

        # Evitando erro, caso o click seja fora do board
        if pos[0] > TILE_SIZE * 8 or pos[1] > TILE_SIZE * 8:
            return

        target = self.board_matrix[r][c]
        if target:  # click on piece
            if target[0] == self.referee.turn_color:  # if it's a player's piece
                self.handle_highlight_hint(target)
                self.grid[c * 8 + r].turn_light(True)
                self.selected = target
            elif self.selected:  # the player wants to kill an enemy piece
                move = (r, c)
                if move in self.referee.get_possible_moves(self.selected):
                    self.manage_kill(move)
                    self.handle_highlight_hint(None, turnoff=True, pos=(r, c))
                    self.turn_condition.piece_captured = True
                    # self.turn()
        elif self.selected:  # click on empty slot, a piece was previously selected
            move = (r, c)
            if move in self.referee.get_possible_moves(self.selected):
                self.manage_move(move)
                self.handle_highlight_hint(None, turnoff=True)
                self.turn_condition.piece_moved = True
                # self.turn()
        self.handle_red_light()
        return None

    def turn(self):
        self.selected = None
        # NOTE - check if king with current turn_color still in danger
        self.referee.update_status()
        # NOTE - update the tile under the king with current turn_color
        self.handle_red_light()
        # NOTE - pass turn
        self.referee.turn()
        # NOTE - check if king with current turn_color is in danger (already done inside referee.turn)
        # #self.referee.update_status()#
        # NOTE - update the tile under the king with current turn_color
        self.handle_red_light()
        return None

    def handle_endgame(self):
        if self.referee.status == Status.CHECKMATE:
            Navigator().show(EndGameScreen(Navigator().get_surface(), self.referee.turn_color))
        elif self.referee.status in [Status.DRAW_MATERIAL, Status.DRAW_REPETITION,
                                     Status.DRAW_PROGRESSION, Status.DRAW_STALEMATE]:
            Navigator().show(EndGameScreen(Navigator().get_surface(), 'draw'))

    def on_pressing(self, key):
        print('-' * 50)
        print('Key pressed:', key)
        if key == 'r':
            self.restart()
        elif key == 's':
            self.save_game()
        elif key == 'l':
            self.load_game()
        elif key == 'i':
            self.show_info()
        elif key == 'q':
            Navigator().close_actual_screen()
        return None

    def manage_move(self, move) -> None:
        self.transform(move[0], move[1])
        self._pp_look_promotion = True
        if self.selected[1] == 'p':
            self.referee.no_progression_counter = 0
        else:
            self.referee.no_progression_counter += 1
        return None

    def manage_kill(self, move) -> None:
        self.pieces[self.board_matrix[move[0]][move[1]]].active = False
        self.transform(move[0], move[1])
        self._pp_look_promotion = True
        self.referee.no_progression_counter = 0
        self.referee.pieces_counter -= 1
        return None

    def show_info(self) -> None:
        print('\nBoard Matrix:\n')
        show_board_matrix(self.board_matrix)
        print(f'''
            Turn color: {self.referee.turn_color}
            Material Score: {count_material_advantage(self.board_matrix, self.referee.turn_color)}
            Turn counter: {self.referee.turn_counter}
            Status: {self.referee.status.name}
        ''')
        print()

    def handle_red_light(self):
        kings_place = {'b': 4, 'w': 5}[GameOverallContext().get_color()]

        x, y = self.pieces[f"{self.referee.turn_color}k{kings_place}"].get_board_pos()
        tile = self.grid[y * 8 + x]
        if self.referee.status == Status.CHECK or self.referee.status == Status.CHECKMATE:
            tile.turn_red()
        elif tile.sprite is tile.danger_sprite:
            tile.turn_light(False)
        return None

    def on_loop(self) -> None:
        self.handle_endgame()
        if self.referee.check_termination():
            return None
        if self.is_bot_turn() and not self.turn_condition.ia_played:
            action = self.bot.get_action()
            self.selected = self.board_matrix[action[0][0]][action[0][1]]
            if self.board_matrix[action[1][0]][action[1][1]]:
                self.manage_kill(action[1])
            else:
                self.manage_move(action[1])
            self.handle_highlight_hint(None, turnoff=True)
            self.turn_condition.ia_played = True
            # self.turn()
            self.handle_red_light()
        if self.turn_condition.board_change():
            self.manage_pawn_promotion()
        # NOTE - should exist only one local to pass the turn
        self.turn_condition.activate_action()
        return None

    def on_render(self) -> None:
        dead_offset = {'b': 0, 'w': 0}
        Navigator().get_surface().fill((29, 30, 42))
        for tile in self.grid:
            Navigator().get_surface().blit(*tile.render())
        for piece in self.pieces.values():
            if piece.active:
                Navigator().get_surface().blit(*piece.render())
            else:
                Navigator().get_surface().blit(*self.render_dead_piece(piece, dead_offset[piece.color]))
                dead_offset[piece.color] += 1
        Navigator().get_surface().blit(self.infos,
                                       (self.board_edge + 12, self.board_edge / 2 - self.infos.get_height() / 2 - 50))
        return

    def _process_dead_piece_place(self, sprite: pygame.Surface, index: int):
        edge = TILE_SIZE * 8
        padding_x = 22  # 22 of padding on x-axis
        padding_y = 5
        row_capacity = 4
        # index = x+y
        x = index % row_capacity
        y = index // row_capacity
        return padding_x + edge + (x * sprite.get_width()), padding_y + y * sprite.get_height()

    def render_dead_piece(self, piece: ChessPiece, index=0):
        rectx = piece.sprite.get_width() * .5
        recty = piece.sprite.get_height() * .5
        sprite = pygame.transform.scale(piece.sprite, (rectx, recty))
        x, y = self._process_dead_piece_place(sprite, index)

        if GameOverallContext().is_white_bottom():
            if piece.color != "w":
                y += TILE_SIZE * 5
        else:
            if piece.color != "b":
                y += TILE_SIZE * 5

        return sprite, (x, y)

    def handle_highlight_hint(self, target: str, turnoff: bool = False, pos: tuple = None) -> None:
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
        return

    def manage_pawn_promotion(self) -> None:
        """
        Test if there is a pawn to be promoted, and if there is promote it.
        """
        # NOTE - run only between frames after a change and the change of turn
        pawn_k = self.referee.get_pawn_promote()
        self.turn_condition.has_pawn_to_promote = pawn_k != ''
        if (pawn_k):
            # NOTE - promote to a new type
            if self.is_bot_turn():
                self.promote_pawn(pawn_k, 'q')
            else:
                if self._wait_to_open_selection_screen:
                    self._wait_to_open_selection_screen = False
                else:
                    self.open_piece_selection_screen(pawn_k)
                    self._wait_to_open_selection_screen = True
        return None

    def promote_pawn(self, pawn_k: str, new_type: str) -> None:
        """
        Promote the pawn specified by pawn_k to the specified type.
        """
        piece = self.pieces.pop(pawn_k)
        piece.type = new_type
        piece.reload_sprite()
        # NOTE - +8 to solve colisions ex. wp1 -> wr1 replacing the existing wr1
        new_key = f"{pawn_k[0]}{new_type}{int(pawn_k[2:]) + 8}"
        r, c = piece.get_board_pos()
        self.pieces[new_key] = piece
        self.board_matrix[r][c] = new_key
        return

    def open_piece_selection_screen(self, pawn_k: str) -> None:
        scr = PieceSelection(Navigator().get_surface())
        scr.show_color = pawn_k[0]
        scr.command_on_leave = RetrieveChosenPiece(pawn_k, scr, self)
        Navigator().show(scr)
        return

    def is_bot_turn(self):
        return not self.multiplayer and self.referee.turn_color == self.bot.color

    def check_status(self) -> None:
        """
        Call the referee to check the game status.
        """
        return self.referee.update_status()

    def clear(self) -> None:
        self.selected = None
        self.offset = 0
        self.highlight = []
        self._PP_COUNTER_VALUE = 1
        self._pp_counter_until_piece_selection = self._PP_COUNTER_VALUE
        self._pp_look_promotion = False

        for piece in self.grid:
            piece.turn_light(False)

        return None

    def get_state(self) -> dict:
        """
        Returns the state of the controller object.
        """
        aux = {}
        for key, value in self.pieces.items():
            aux[key] = {
                'position': value.get_board_pos(),
                'has_moved': value.has_moved,
                'active': value.active
            }
        return {
            'board_matrix': self.board_matrix,
            'pieces': aux,
            'multiplayer': self.multiplayer,
            'referee': self.referee.get_state(),
            'bot': self.bot.get_state(),
            'color': GameOverallContext().get_color()
        }

    def set_state(self, state) -> None:
        """
        Loads state.
        """
        aux: Dict[ChessPiece] = state['pieces']
        GameOverallContext().set_color(state['color'])
        if state['multiplayer']:
            GameOverallContext().set_opponent_as_multiplayer()
        else:
            GameOverallContext().set_opponent_as_IA()
        removable = list(self.pieces.keys())
        for key in removable:
            if not key in aux.keys():
                self.pieces.pop(key)
        for key, value in aux.items():
            if not key in self.pieces.keys():
                self.pieces[key] = ChessPiece(
                    type=key[1],
                    color=key[0]
                )
            self.pieces[key].y = value['position'][0] * TILE_SIZE
            self.pieces[key].x = value['position'][1] * TILE_SIZE
            self.pieces[key].has_moved = value['has_moved']
            self.pieces[key].active = value['active']
        self.board_matrix = state['board_matrix']
        self.multiplayer = state['multiplayer']
        self.referee.board_matrix = self.board_matrix
        self.referee.set_state(state['referee'])
        self.bot.board_matrix = self.board_matrix
        self.bot.set_state(state['bot'])
        return None

    def save_game(self, filename: str = 'save') -> None:
        if not os.path.isdir(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)
        with open(SAVE_FOLDER + filename + '.json', 'w') as file:
            json.dump(self.get_state(), file, indent=4)
        print('Game state saved.')
        return None

    def load_game(self, filename: str = 'save') -> None:
        if os.path.exists(SAVE_FOLDER + filename + '.json'):
            with open(SAVE_FOLDER + filename + '.json') as file:
                self.set_state(json.load(file))
            print(f'''Game state loaded. {letter_to_color(self.referee.turn_color).capitalize()} plays next.''')
        else:
            print('There is no game state to be loaded.')
        self.clear()
        return None

    def restart(self) -> None:
        self.pieces.clear()
        self.load_pieces()
        if GameOverallContext().is_white_bottom():
            self.board_matrix = [row.copy() for row in BOARD_MATRIX_1]
        else:
            self.board_matrix = [row.copy() for row in BOARD_MATRIX_2]
        self.referee = Referee(self.board_matrix, self.pieces)
        self.bot = Bot(
            level=self.bot.level,
            referee=self.referee,
            board_matrix=self.board_matrix,
            pieces=self.pieces,
            color=GameOverallContext().get_opponent_color(),
            bottomup_orientation=False)
        self.clear()
        print('#' * 50 + '\nNew Game')
        return None

    def load_pieces(self):
        order = ["r", "n", "b", "q", "k", "b", "n", "r"]
        player = GameOverallContext().get_color()
        opponent = GameOverallContext().get_opponent_color()
        if player == "b":
            order.reverse()
        for i in range(8):
            # white
            self.pieces[player + 'p' + str(i + 1)] = ChessPiece(x=i * TILE_SIZE, y=6 * TILE_SIZE, offset=self.offset,
                                                                color=player)
            try:
                self.pieces[player + order[i] + str(i + 1)] = ChessPiece(type=order[i], x=i * TILE_SIZE,
                                                                         y=7 * TILE_SIZE,
                                                                         offset=self.offset, color=player)
            except Exception as e:
                print(f"Could not import w{order[i]}.png")
            # black
            self.pieces[opponent + 'p' + str(i + 1)] = ChessPiece(color=opponent, x=i * TILE_SIZE, y=1 * TILE_SIZE,
                                                                  offset=self.offset)
            try:
                self.pieces[opponent + order[i] + str(i + 1)] = ChessPiece(color=opponent, type=order[i],
                                                                           x=i * TILE_SIZE,
                                                                           y=0 * TILE_SIZE, offset=self.offset)
            except Exception as e:
                print(f"Could not import b{order[i]}.png")
        return None
