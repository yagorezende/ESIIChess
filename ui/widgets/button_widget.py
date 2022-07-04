from typing import Tuple

import pygame

from logic.generic_command import GenericCommand
from ui.widgets.generic_widget import GenericWidget


class Button(GenericWidget):
    def __init__(self, sprite: pygame.Surface, axis: tuple, alpha=False, action=None,
                 hover_sprite: pygame.Surface = None, selectable=False):
        super(Button, self).__init__()
        self.axis = axis
        self.rect = sprite.get_rect()
        self.rect[0] += axis[0]
        self.rect[1] += axis[1]
        self.action: GenericCommand = action
        self.hover_sprite = hover_sprite
        self.selected = False
        self.selectable = selectable

        if alpha:
            self.sprite = sprite.convert_alpha()
        else:
            self.sprite = sprite.convert()
        self.surface = self.sprite

    def on_event(self, event) -> None:
        super(Button, self).on_event(event)
        if self._is_hover(event):
            if self.hover_sprite:
                self.surface = self.hover_sprite
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONUP:
                if self.selectable:
                    self.selected = True
                print("Click no btn")
                if self.action:
                    self.action.execute()
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                self.selected = False
            if not self.selected:
                self.surface = self.sprite

    def _is_hover(self, event: pygame.event) -> bool:
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
            if self.rect.x <= event.pos[0] <= self.rect.x + self.surface.get_width() \
                    and self.rect.y <= event.pos[1] <= self.rect.y + self.surface.get_height():
                return True
        return False

    def on_render(self) -> Tuple[pygame.Surface, pygame.Rect]:
        return self.surface, self.rect
