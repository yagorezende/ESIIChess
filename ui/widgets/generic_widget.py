from typing import Tuple, List

import pygame


class GenericWidget:
    def __init__(self) -> None:
        self.active: bool = True
        self.surface: pygame.Surface = pygame.Surface((10, 10))
        self.rect: pygame.Rect = pygame.Rect(self.surface.get_rect())
        self.rect.top = 0
        self.rect.left = 0
        self.widgets: List[GenericWidget] = []

    def on_event(self, event) -> None:
        for widget in self.widgets:
            widget.on_event(event)
        return None

    def on_update(self) -> None:
        return None

    def on_render(self) -> Tuple[pygame.Surface, pygame.Rect]:
        return self.surface, self.rect

    def align_center(self, widget2: pygame.Surface) -> tuple:
        wcenterX = widget2.get_rect().x + widget2.get_width() / 2
        wcenterY = widget2.get_rect().y + widget2.get_width() / 2

        centerX = self.rect.x + self.surface.get_width() / 2
        centerY = self.rect.y + self.surface.get_height() / 2

        return abs(wcenterX - centerX), abs(wcenterY - centerY)
