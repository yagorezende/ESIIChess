from logic.singleton_meta import SingletonMeta

IA = "IA"
MULTIPLAYER = "Multiplayer"


class GameOverallContext(metaclass=SingletonMeta):
    def __init__(self):
        self._against = "IA"
        self._color = "w"
        self._sound = False

    def set_color(self, color: str):
        self._color = color

    def get_color(self):
        return self._color

    def get_against(self):
        return self._against

    def is_multiplayer(self):
        return self._against != "IA"

    def set_opponent(self, opponent: str):
        self._against = opponent
