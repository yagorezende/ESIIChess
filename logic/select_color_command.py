import random

from logic.game_overall_context import GameOverallContext
from logic.generic_command import GenericCommand


class SelectColorCommand(GenericCommand):
    def __init__(self, color: str):
        """abc"""
        self.color = color

    def execute(self):
        """
        Initiate a new game injecting all the selected options on it.
        """
        choice = self.color
        if self.color == "random":
            choice = random.choice(["w", "b"])
            GameOverallContext().set_color(choice)
        else:
            GameOverallContext().set_color(self.color)
        print(f"Playing with {choice} ")
