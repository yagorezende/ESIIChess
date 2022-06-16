from typing import Dict, List, Tuple
from logic.const import Status
from logic.tools import count_material_advantage, show_board_matrix
from logic.referee import Referee
from ui.board import ChessPiece
from random import uniform, choice

class Node():

    def __init__(self, referee_info, g, f=None, origin=None):
        self.board_matrix = referee_info['board']
        self.bottom_color = referee_info['bottom_color']
        self.pieces_counter = referee_info['pieces_counter']
        self.king_info = referee_info['king']
        self.left_rook = referee_info['l_rook']
        self.right_rook = referee_info['r_rook']
        self.rushed_pawn = referee_info['rushed_pawn']
        self.turn_color = referee_info['turn_color']
        self.g = g
        self.f = f
        self.origin = origin
        return

    def transform(self, origin: tuple, move: tuple):
        r, c = origin
        i, j = move
        code = self.board_matrix[r][c]
        if code[1] == 'k':
            self.king_info = True
            displacement = c - j
            if displacement == 2:  # small castle
                self.board_matrix[r][c - 1] = self.board_matrix[r][c + 1]
                self.board_matrix[r][c + 1] = None
                self.left_rook = True
            elif displacement == -2:  # big castle
                self.board_matrix[r][c + 1] = self.board_matrix[r][c - 2]
                self.board_matrix[r][c - 2] = None
                self.right_rook = True
        elif code[1] == 'r':
            if code[2] == '1':
                self.left_rook = True
            elif code[2] == '8':
                self.right_rook = True
        elif code[1] == 'p':
            if abs(r - i) == 2: # double step
                self.rushed_pawn = move
            else:
                self.rushed_pawn = None
                if c != j and not self.board_matrix[r][c]:  # en passant
                    self.board_matrix[i][c] = None
        self.board_matrix[i][j] = self.board_matrix[r][c] # transform
        self.board_matrix[r][c] = None # same
        return

    def get_info(self):
        return {
            'board' : [row.copy() for row in self.board_matrix],
            'bottom_color' : self.bottom_color,
            'pieces_counter' : self.pieces_counter,
            'king' : self.king_info,
            'l_rook' : self.left_rook,
            'r_rook' : self.right_rook,
            'rushed_pawn' : self.rushed_pawn,
            'turn_color' : self.turn_color
        }

    def copy(self):
        return Node(
            self.get_info(),
            self.g, self.f, self.origin
        )

class Bot():

    def __init__(self, level: int, referee: Referee, board_matrix: list, pieces: dict, color: str, bottomup_orientation: bool) -> None:
        self.level = level
        self.referee = referee
        self.board_matrix = board_matrix
        self.pieces: Dict[str, ChessPiece] = pieces
        self.color = color
        self.bottomup_orientation = bottomup_orientation

    def get_action(self):
        """
        Finds a move to proceed with the game.
        """
        if self.level == 0: # random move
            return self.random_action()
        if self.level == 1: # blind killer (it never wins)
            return self.material_advantage_search() # for tests only
        return self.search() # may have some action here

    def evaluate_state(self, state: Node) -> float:
        """
        Function to assess a particular state.
        It returns a number that is smaller the more the state
        is favorable to the color of the turn. Return 0 means checkmate.
        """
        bonus = 0
        backup = self.get_referee_info()
        self.set_referee_info(state.get_info())
        bottomup_orientation = state.turn_color == state.bottom_color
        for r in range(8):
            for c in range(8):
                key = state.board_matrix[r][c]
                if key:
                    if key[1] == 'k':
                        if key[0] == state.turn_color:
                            if self.referee.check_threat((r, c)):
                                if not self.referee.check_mobility():
                                    return 1000 # the worst state
                                bonus -= 0.2
                        else:
                            if self.referee.check_threat((r, c)):
                                if not self.referee.check_mobility():
                                    return 0 # the perfect state
                            bonus += 0.2
                    elif key[1] == 'p':
                        if key[0] == state.turn_color:
                            if bottomup_orientation and r > 4:
                                bonus += 0.1 * (r - 4)
                        elif not bottomup_orientation and r < 4:
                            bonus -= 0.1 * (4 - r)
        self.set_referee_info(backup)
        self.referee.board_matrix = self.board_matrix
        return 1000 - count_material_advantage(state.board_matrix, state.turn_color) * (1 + bonus)

    def material_advantage_search(self):
        """
        Returns the move that gives the greatest material advantage.
        """
        best_action = None
        best_advantage = -1
        canvas = [row.copy() for row in self.board_matrix]
        for key, value in self.pieces.items():
            if key[0] == self.color and value.active: # for each peace...
                for move in self.referee.get_possible_moves(key): # for each possible move...
                    pos = value.get_board_pos()
                    b1, b2 = canvas[move[0]][move[1]], canvas[pos[0]][pos[1]] # backups
                    canvas[move[0]][move[1]] = canvas[pos[0]][pos[1]] # transform
                    canvas[pos[0]][pos[1]] = None # still tranforming...
                    h = count_material_advantage(canvas, self.color) # evaluate board
                    if h > best_advantage: # if its better...
                        best_advantage = h
                        best_action = (pos, move)
                    elif h == best_advantage: # if its equally good...
                        if uniform(0, 1) > 0.5: # randomly choose between them
                            best_advantage = h
                            best_action = (pos, move)
                    canvas[move[0]][move[1]] = b1 # reconstitute matrix, so we don't have to build another one
                    canvas[pos[0]][pos[1]] = b2 # and here
        return best_action

    def random_action(self) -> tuple:
        """
        Returns a random move for a random piece.
        """
        alive = []
        for key, value in self.pieces.items():
            if key[0] == self.color and value.active:
                space = self.referee.get_possible_moves(key)
                if space: alive.append((value, space))
        if not alive: return None
        r_selection = choice(alive)
        move = choice(r_selection[1])
        pos = r_selection[0].get_board_pos()
        return pos, move

    def search(self) -> Tuple[tuple, tuple]:
        # initial = Node(self.get_referee_info(), g=0)
        # initial.f = self.evaluate_state(initial)
        # result = self.RBFS(initial, 10**9, 0)
        # state = result[0][1]
        # return state.origin
        return self.random_action() # NOTE: provisional

    def generate_successors(self, node: Node) -> List[Node]:
        """
        Generates all possible neighbors of a node.
        """
        backup = self.get_referee_info()
        self.set_referee_info(node.get_info())
        successors = []
        for r in range(8):
            for c in range(8):
                code = node.board_matrix[r][c]
                if code and code[0] == node.turn_color:
                    for move in self.referee.get_possible_moves(piece=code, pos=(r, c)):
                        neighbor = node.copy()
                        neighbor.turn_color = 'w' if node.turn_color == 'b' else 'b'
                        neighbor.transform((r, c), move)
                        neighbor.g += 1
                        neighbor.f = neighbor.g + self.evaluate_state(neighbor)
                        neighbor.origin = ((r, c), move)
                        successors.append(neighbor)
        self.set_referee_info(backup)
        self.referee.board_matrix = self.board_matrix
        return successors

    def select_nodes(self, nodes: List[Node]) -> tuple:
        """
        Chooses the two best nodes in a list.
        """
        best = choice(nodes)
        alternative = None
        for node in nodes:
            if node.f < best.f:
                alternative = best
                best = node
            elif node.f == best.f:
                if uniform(0, 1) > 0.5:
                    alternative = best
                    best = node
            if alternative and node.f < alternative.f:
                alternative = node
            elif alternative is None:
                alternative = node
        return best, alternative

    def RBFS(self, node: Node, f_limit: int, depth: int) -> Tuple[List[Node], float]: # Recursive Best-First Search
        if depth >= self.level * 1.5:
            return [node], node.f
        successors = self.generate_successors(node)
        if not successors:
            return [node], node.f
        limit = 50
        while limit:
            limit -= 1
            selected = self.select_nodes(successors)
            if selected[0].f > f_limit:
                return [], selected[0].f
            if selected[1]:
                aux = self.RBFS(selected[0], min(f_limit, selected[1].f), depth + 1)
            else:
                aux = self.RBFS(selected[0], f_limit, depth + 1)
                # return [selected[0]], selected[0].f
                # aux = [selected[0]], selected[0].f
            if aux[0]:
                aux[0].insert(0, node)
                return aux
            else:
                selected[0].f = aux[1] # failure, update the heuristic and try again.
        return ([], 0)

    def get_referee_info(self) -> dict:
        """
        Returns some information about the referee object.
        """
        return {
            'board' : self.referee.board_shot(),
            'bottom_color' : self.referee.bottom_color,
            'pieces_counter' : self.referee.pieces_counter,
            'king' : self.referee.pieces[self.referee.turn_color + 'k5'].has_moved,
            'l_rook' : self.pieces[self.referee.turn_color + 'r1'].has_moved,
            'r_rook' : self.pieces[self.referee.turn_color + 'r8'].has_moved,
            'rushed_pawn' : self.referee.rushed_pawn,
            'turn_color' : self.referee.turn_color
        }
    
    def set_referee_info(self, info: dict) -> None:
        """
        Set some information about the referee object.
        """
        self.referee.board_matrix = info['board']
        self.referee.bottom_color = info['bottom_color']
        self.referee.pieces_counter = info['pieces_counter']
        self.referee.pieces[self.referee.turn_color + 'k5'].has_moved = info['king']
        self.referee.pieces[self.referee.turn_color + 'r1'].has_moved = info['l_rook']
        self.referee.pieces[self.referee.turn_color + 'r8'].has_moved = info['r_rook']
        self.referee.rushed_pawn = info['rushed_pawn']
        self.referee.turn_color = info['turn_color']
        return

    def get_state(self) -> dict:
        return {
            'level' : self.level,
            'color' : self.color,
            'bottomup_orientation' : self.bottomup_orientation
            }
    
    def set_state(self, state: dict) -> None:
        self.level = state['level']
        self.color = state['color']
        self.bottomup_orientation = state['bottomup_orientation']
        return None

