from typing import Callable


class TurnCondition:
    def __init__(self, action: Callable[[],None]) -> None:
        """
        Define conditions that influence wether or not the turn should be passed
        and the `action` to be done in an affirmtive case.
        """
        self._action = action
        self.has_pawn_to_promote: bool = False
        self.piece_captured: bool = False
        self.piece_moved: bool = False
        self.ia_played: bool = False
        self._reset_conditions()
        return None

    def _reset_conditions(self) -> None:
        """
        Prepare to the next turn.
        """
        # NOTE - True to prevent turn to pass
        self.has_pawn_to_promote = True
        self.piece_captured = False
        self.piece_moved = False
        self.ia_played = False

    def board_change(self) -> bool:
        """
        Return if a piece was moved or captured by the player or IA.
        """
        return self.piece_moved or self.piece_captured or self.ia_played

    def _condition_fullfiled(self) -> bool:
        """
        Check if the conditions to pass a turn were fullfiled.
        """
        # NOTE - rule 1 (some action took place)
        r1 = self.board_change()
        # NOTE - rule 2 (there is not a pawn to promote)
        r2 = not self.has_pawn_to_promote
        # NOTE - rule 3 (some action and there no pawn to promote)
        r3 = r1 and r2
        return r3

    def activate_action(self) -> None:
        """
        Do `action` after the conditions to pass turn be fullfiled.
        """
        if self._condition_fullfiled():
            self._action()
            self._reset_conditions()
        return None
