import enum

from logic.generic_command import GenericCommand
from ui.screens.game_screen import GameScreen
from ui.screens.navigator import Navigator


class StartGameCommand(GenericCommand):
    def __init__(self):
        """abc"""

    def execute(self) -> None:
        """
        Initiate a new game injecting all the selected options on it.
        """
        Navigator().close_actual_screen()
        Navigator().get_surface().fill((29, 30, 42))
        Navigator().show(GameScreen(
            Navigator().get_surface()))
        return None

    def _find_enum_member(self, name: str, enumeration: enum.Enum) -> enum.Enum:
        for member in list(enumeration):  # type: ignore
            if member.name.lower() == name.lower():
                return member
        raise LookupError(f'could not find {name} in {enumeration}')
