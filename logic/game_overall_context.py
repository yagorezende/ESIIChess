from logic.singleton_meta import SingletonMeta

IA = "IA"
MULTIPLAYER = "Multiplayer"


class GameOverallContext(metaclass=SingletonMeta):
    def __init__(self):
        self._against = "IA"
        self._color = "w"
        self._sound = True

    def set_color(self, color: str):
        self._color = color

    def get_color(self):
        return self._color

    def get_opponent_color(self):
        return {"b": "w", "w": "b"}[self._color]

    def is_white_bottom(self):
        """
        Get the board orientation
        :return: bool: if white is bottom oriented
        """
        return self._color == 'w'

    def get_against(self):
        return self._against

    def should_play(self):
        return self._sound

    def is_multiplayer(self):
        return self._against != "IA"

    def set_opponent(self, opponent: str):
        self._against = opponent

    def set_opponent_as_IA(self):
        self.set_opponent(IA)

    def set_opponent_as_multiplayer(self):
        self.set_opponent(MULTIPLAYER)

    def set_sound_option(self, selected):
        self._sound = selected
