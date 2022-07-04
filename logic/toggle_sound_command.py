from logic.game_overall_context import GameOverallContext
from logic.generic_command import GenericCommand
from ui.widgets.button_widget import Button


class ToggleSoundCommand(GenericCommand):
    def __init__(self, toggle: Button):
        self.toggle = toggle

    def execute(self):
        """
        Initiate a new game injecting all the selected options on it.
        """
        GameOverallContext().set_sound_option(self.toggle.selected)
        print(f"Sound set to {self.toggle.selected}")
