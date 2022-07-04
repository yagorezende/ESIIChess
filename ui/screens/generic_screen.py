import pygame


class GenericScreen:

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.background_sprite: pygame.sprite = None

    def on_enter(self) -> None:
        return None

    def on_event(self, event) -> None:
        return None

    def on_loop(self) -> None:
        return None

    def on_render(self) -> None:
        return None

    def on_leave(self) -> None:
        return None

    def get_center(self):
        return self.surface.get_width() // 2, self.surface.get_height() // 2

    def draw_background(self):
        rect = self.background_sprite.get_rect()
        rect.center = self.surface.get_width() // 2, self.surface.get_height() // 2
        self.surface.blit(self.background_sprite, rect)
