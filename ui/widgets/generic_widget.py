from typing import Tuple

import pygame


class GenericWidget:
    def __init__(self) -> None:
        self.active: bool = True
        self.surface: pygame.Surface = pygame.Surface((10, 10))
        self.rect: pygame.Rect = pygame.Rect(self.surface.get_rect())
        self.rect.top = 0
        self.rect.left = 0
        return None

    def on_event(self, event) -> None:
        return None

    def on_update(self) -> None:
        return None

    def on_render(self) -> Tuple[pygame.Surface, pygame.Rect]:
        return (self.surface, self.rect)
