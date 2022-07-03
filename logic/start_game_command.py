import enum

from ui.screens.game_screen import GameScreen
from ui.screens.navigator import Navigator

import logic.selected_options as sp
from logic.generic_command import GenericCommand


class StartGameCommand(GenericCommand):
    def __init__(self, game_options_screen) -> None:
        self._screen = game_options_screen
        return None

    def execute(self) -> None:
        """
        Initiate a new game injecting all the selected options on it.
        """
        Navigator().close_actual_screen()
        _, color = self._screen.color.selected_option
        _, oponent = self._screen.oponent.selected_option
        _, difficulty = self._screen.difficulty.selected_option
        oponent_enum_member = self._find_enum_member(
            oponent, sp.Oponent)
        color_enum_member = self._find_enum_member(
            color, sp.Color)
        difficulty_enum_member = self._find_enum_member(
            difficulty, sp.Difficulty)
        Navigator().show(GameScreen(
            oponent=oponent_enum_member,  # type: ignore
            p1_color=color_enum_member,  # type: ignore
            difficulty=difficulty_enum_member))  # type: ignore
        return None

    def _find_enum_member(self, name: str, enumeration: enum.Enum) -> enum.Enum:
        for member in list(enumeration):  # type: ignore
            if member.name.lower() == name.lower():
                return member
        raise LookupError(f'could not find {name} in {enumeration}')
