from random import choice

import ui.screens.game_options
from ui.screens.game_screen import GameScreen
from ui.screens.navigator import Navigator

from logic.generic_command import GenericCommand
from logic.selected_options import SelectedOptions


class StartGameCommand(GenericCommand):
    def __init__(self, game_options_screen) -> None:
        self._screen = game_options_screen
        return None

    def execute(self) -> None:
        """
        Initiate a new game injecting all the selected options on it.
        """
        newScreen = GameScreen()
        # NOTE - if random was choosed select a color
        i, color = self._screen.color.selected_option
        if color.lower() == 'random':
            options = [c for ic, c in enumerate(
                self._screen.color._options) if i != ic]
            color, _, _ = choice(options)
        newScreen.selected_options = SelectedOptions(
            self._screen.oponent.selected_option[1].lower(),
            color.lower(),
            self._screen.difficulty.selected_option[1].lower())
        Navigator().close_actual_screen()
        Navigator().show(newScreen)
        return None
