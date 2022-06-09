import pygame


class GenericScreen():

    def on_enter(self) -> None:
        return None

    def on_event(self, event) -> None:
        return None

    def on_loop(self) -> None:
        return None

    def on_render(self, scr_surf: pygame.Surface) -> None:
        return None

    def on_leave(self) -> None:
        return None
