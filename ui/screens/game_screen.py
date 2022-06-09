import pygame
from ui.controller import Controller
from ui.screens.generic_screen import GenericScreen


class GameScreen(GenericScreen):
    def __init__(self) -> None:
        super().__init__()
        self.controller = Controller()
        return None

    # ----------

    def on_enter(self) -> None:
        self.controller.init_board()
        return None

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.controller.on_click()

    def on_loop(self) -> None:
        self.controller.on_loop()
        return None

    def on_render(self, scr_surf: pygame.Surface) -> None:
        self.controller.on_render(scr_surf)
        return None

    def on_leave(self) -> None:
        return None