from typing import Tuple, Callable

import pygame

from ui.widgets.generic_widget import GenericWidget


class Button(GenericWidget):
    def __init__(self, sprite: pygame.Surface, axis: tuple, alpha=False, action=None):
        super(Button, self).__init__()
        self.surface = sprite
        self.axis = axis
        self.rect = sprite.get_rect()
        self.rect[0] += axis[0]
        self.rect[1] += axis[1]
        self.action: Callable = action

        if alpha:
            self.sprite = sprite.convert_alpha()
        else:
            self.sprite = sprite.convert()

    def on_event(self, event) -> None:
        super(Button, self).on_event(event)
        if self._is_hover(event):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONUP:
                print("Click no btn")
                if self.action:
                    self.action()
        else:
            pass

    def _is_hover(self, event: pygame.event) -> bool:
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.sprite.get_width() \
                    and self.rect.y <= event.pos[1] <= self.rect.y + self.sprite.get_height():
                return True
        return False

    def on_render(self) -> Tuple[pygame.Surface, pygame.Rect]:
        return self.sprite, self.rect
