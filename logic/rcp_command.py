import ui.screens.piece_selection
from logic.generic_command import GenericCommand

class RetrieveChosenPiece(GenericCommand):
    """
    Set up a callback function who receive a string representing the selected
    piece on the piece selection screen.
    """

    def __init__(self, pawn_k: str, scr: ui.screens.piece_selection.PieceSelection, controller) -> None:
        self._pawn_k = pawn_k
        self._screen = scr
        self._controller = controller
        return None

    def execute(self) -> None:
        self._controller.promote_pawn(self._pawn_k, self._screen.selected_piece)
        return None
