from typing import Dict, List, Tuple
from logic.const import INFINITE
from logic.referee import Referee
from ui.board import ChessPiece
from random import uniform, choice

class Node():

    def __init__(self, referee_info, evaluation=None, origin=None):
        self.board_matrix = referee_info['board']
        self.bottom_color = referee_info['bottom_color']
        self.pieces_counter = referee_info['pieces_counter']
        self.castle_info = {
            "wk5" : referee_info['castle_info']['wk5'],
            "bk5" : referee_info['castle_info']['bk5'],
            "wr1" : referee_info['castle_info']['wr1'],
            "wr8" : referee_info['castle_info']['wr8'],
            "br1" : referee_info['castle_info']['br1'],
            "br8" : referee_info['castle_info']['br8']
        }
        self.rushed_pawn = referee_info['rushed_pawn']
        self.turn_color = referee_info['turn_color']
        self.evaluation = evaluation
        self.origin = origin
        return

    def transform(self, origin: tuple, move: tuple):
        r, c = origin
        i, j = move
        code = self.board_matrix[r][c]
        if code[1] == 'k':
            self.castle_info[code[0] + 'k5'] = True
            displacement = c - j
            if displacement == 2:  # small castle
                self.board_matrix[r][c - 1] = self.board_matrix[r][c + 1]
                self.board_matrix[r][c + 1] = None
                self.castle_info[code[0] + 'r1'] = True
            elif displacement == -2:  # big castle
                self.board_matrix[r][c + 1] = self.board_matrix[r][c - 2]
                self.board_matrix[r][c - 2] = None
                self.castle_info[code[0] + 'r8'] = True
        elif code[1] == 'r':
            self.castle_info[code] = True
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
            'castle_info' : self.castle_info,
            'rushed_pawn' : self.rushed_pawn,
            'turn_color' : self.turn_color
        }

    def copy(self):
        return Node(
            self.get_info(),
            self.evaluation, self.origin
        )

class Bot():

    def __init__(self, level: int, referee: Referee, board_matrix: list, pieces: dict, color: str, bottomup_orientation: bool) -> None:
        self.level = level
        self.referee = referee
        self.board_matrix = board_matrix
        self.pieces: Dict[str, ChessPiece] = pieces
        self.color = color
        self.bottomup_orientation = bottomup_orientation

    def get_action(self) -> Tuple[tuple, tuple]:
        """
        Finds a move to proceed with the game.
        """
        if self.level == 0 or self.referee.turn_counter < 3:
            return self.random_action()
        return self.search(max_depth=self.level)

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

    def evaluate_node(self, node: Node) -> float:
        """
        Function to evaluate a particular state.
        It returns a number that is greater the more the state
        is favorable to the color of the turn.
        """
        advantage = 0
        backup = self.get_referee_info()
        self.set_referee_info(node.get_info())
        for r in range(8):
            for c in range(8):
                key = node.board_matrix[r][c]
                if key:
                    factor = 1 if key[0] == node.turn_color else -1
                    if key[1] == 'k': # 100 for kings
                        advantage += factor * 100
                    elif key[1] == 'p': # 1 for pawns
                        advantage += factor
                    elif key[1] == 'r': # 5 for rooks
                        advantage += factor * 5
                    elif key[1] == 'q': # 9 for queens
                        advantage += factor * 9
                    else: # 3 for knights and bishops
                        advantage += factor * 3
        self.set_referee_info(backup)
        self.referee.board_matrix = self.board_matrix
        return advantage
    
    def search(self, max_depth: int = 0) -> Tuple[tuple, tuple]:
        """
        Starts a search for a good move using a tree with a maximum allowed depth.
        """
        initial = Node(self.get_referee_info())
        result = self.minimax(initial, max_depth=max_depth)
        return result[0].origin

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
                        neighbor.origin = ((r, c), move)
                        successors.append(neighbor)
        self.set_referee_info(backup)
        self.referee.board_matrix = self.board_matrix
        return successors

    def get_min_node(self, nodes: List[Node]) -> Node:
        """
        Returns the node with the smallest evaluation.
        If two nodes are equally valued, one of them is randomly selected.
        """
        if not nodes:
            return None
        min_node = None
        min_adv = 10 ** 6
        for node in nodes:
            node.evaluation = self.evaluate_node(node)
            if node.evaluation < min_adv or node.evaluation == min_adv and uniform(0, 1) > 0.5:
                min_node = node
                min_adv = node.evaluation
        return min_node
    
    def minimize(self, successors: List[Node], depth: int = 0, max_depth: int = 1):
        best = []
        best_eval = INFINITE
        for successor in successors:
            aux = self.minimax(successor, depth=depth, max_depth=max_depth)
            if aux[1] == best_eval:
                best.append(successor)
            elif aux[1] < best_eval:
                successor.evaluation = aux[1]
                best_eval = aux[1]
                best = [successor]
        return choice(best), best_eval

    def maximize(self, successors: List[Node], depth: int = 0, max_depth: int = 1):
        best = []
        best_eval = -INFINITE
        for successor in successors:
            aux = self.minimax(successor, depth=depth, max_depth=max_depth)
            if aux[1] == best_eval:
                best.append(successor)
            elif aux[1] > best_eval:
                successor.evaluation = aux[1]
                best_eval = aux[1]
                best = [successor]
        return choice(best), best_eval
    
    def minimax(self, node: Node, depth: int = 0, max_depth: int = 1) -> Tuple[Node, int]:
        successors = self.generate_successors(node)
        if not successors:
            backup = self.get_referee_info()
            self.set_referee_info(node.get_info())
            if self.referee.check_threat(self.referee.find(node.turn_color + 'k5')):
                node.evaluation = INFINITE
            else:
                node.evaluation = -INFINITE
            self.set_referee_info(backup)
            self.referee.board_matrix = self.board_matrix
            return node, node.evaluation
        next_level = depth + 1
        if next_level >= max_depth: # next level is the leaf level, so we just get the minimum nodes from there.
            best = self.get_min_node(successors)
            return best, best.evaluation
        if max_depth % 2: # leaf level is odd, so we minimize on odd depths.
            if next_level % 2:
                return self.minimize(successors, next_level, max_depth)
            return self.maximize(successors, next_level, max_depth)
        if next_level % 2: # leaf level is even, so we maximize on odd depths.
            return self.maximize(successors, next_level, max_depth)
        return self.minimize(successors, next_level, max_depth)

    def get_referee_info(self) -> dict:
        """
        Returns some information about the referee object.
        """
        return {
            'board' : self.referee.board_shot(),
            'bottom_color' : self.referee.bottom_color,
            'pieces_counter' : self.referee.pieces_counter,
            'castle_info' : {
                'wk5' : self.referee.pieces['wk5'].has_moved,
                'bk5' : self.referee.pieces['bk5'].has_moved,
                'wr1' : self.referee.pieces['wr1'].has_moved,
                'wr8' : self.referee.pieces['wr8'].has_moved,
                'br1' : self.referee.pieces['br1'].has_moved,
                'br8' : self.referee.pieces['br8'].has_moved
            },
            'rushed_pawn' : self.referee.rushed_pawn,
            'turn_color' : self.referee.turn_color
        }
    
    def set_referee_info(self, info: dict) -> None:
        """
        Set some information about the referee object.
        """
        self.referee.board_matrix = info['board']
        self.referee.bottom_color = info['bottom_color']
        self.referee.turn_color = info['turn_color']
        self.referee.pieces_counter = info['pieces_counter']
        self.referee.pieces['wk5'].has_moved = info['castle_info']['wk5']
        self.referee.pieces['bk5'].has_moved = info['castle_info']['bk5']
        self.referee.pieces['wr1'].has_moved = info['castle_info']['wr1']
        self.referee.pieces['wr8'].has_moved = info['castle_info']['wr8']
        self.referee.pieces['br1'].has_moved = info['castle_info']['br1']
        self.referee.pieces['br8'].has_moved = info['castle_info']['br8']
        self.referee.rushed_pawn = info['rushed_pawn']
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
