from logic.game_overall_context import GameOverallContext
from logic.generic_command import GenericCommand


class SelectOpponentCommand(GenericCommand):
    def __init__(self, opponent: str):
        self.opponent = opponent

    def execute(self):
        """
        Initiate a new game injecting all the selected options on it.
        """
        GameOverallContext().set_opponent(self.opponent)
        print(f"Playing against {self.opponent}")
