from typing import List

from ui.screens.generic_screen import GenericScreen
from logic.singleton_meta import SingletonMeta


class Navigator(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._stack: List[GenericScreen] = []
        self._cur_scr: GenericScreen = GenericScreen()

    def show(self, screen: GenericScreen) -> None:
        """
        Navigate to a screen showing it on top of the others.
        """
        self._stack.append(screen)
        self._cur_scr = screen
        screen.on_enter()

    def close_actual_screen(self) -> None:
        """
        Navigate to the last screen closing the screen on top of the others.
        """
        screen: GenericScreen = self._stack.pop()
        screen.on_leave()
        if self._stack:
            self._cur_scr = self._stack[-1]

    def on_event(self, event) -> None:
        """
        Pass the event for the current screen on top of the stack.
        """
        self._cur_scr.on_event(event)
        return None

    def on_loop(self) -> None:
        """
        Let the screen on top of the stack run its code.
        """
        self._cur_scr.on_loop()
        return None

    def on_render(self, scr_surf) -> None:
        """
        Renders the current screen on top of the stack.
        """
        self._cur_scr.on_render(scr_surf)
        return None
