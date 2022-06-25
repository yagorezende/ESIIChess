from typing import Dict, NamedTuple, Tuple

import logic.generic_command as gc
import pygame
import pygame.freetype as ft
import ui.widgets.generic_widget as gw


class ButtonPalete(NamedTuple):
    bg_normal: Tuple[int, int, int]
    fg_normal: Tuple[int, int, int]
    bg_click: Tuple[int, int, int]
    fg_click: Tuple[int, int, int]
    bg_hover: Tuple[int, int, int]
    fg_hover: Tuple[int, int, int]


class ButtonSurfaces(NamedTuple):
    normal: pygame.Surface
    click: pygame.Surface
    hover: pygame.Surface


class TextButton(gw.GenericWidget):
    def __init__(
            self,
            x=0, y=0,
            text: str = "",
            bg_color_normal: Tuple[int, int, int] = (0, 0, 0),
            fg_color_normal: Tuple[int, int, int] = (255, 255, 255),
            bg_color_click: Tuple[int, int, int] = (0, 0, 0),
            fg_color_click: Tuple[int, int, int] = (255, 255, 255),
            bg_color_hover: Tuple[int, int, int] = (0, 0, 0),
            fg_color_hover: Tuple[int, int, int] = (255, 255, 255),
            trbl_padding: Tuple[int, int, int, int] = (2, 2, 2, 2),
            click_command: gc.GenericCommand = gc.GenericCommand()) -> None:
        super().__init__()
        self.text: str = text
        self.colors: ButtonPalete = ButtonPalete(
            bg_normal=bg_color_normal,
            fg_normal=fg_color_normal,
            bg_click=bg_color_click,
            fg_click=fg_color_click,
            bg_hover=bg_color_hover,
            fg_hover=fg_color_hover)
        self.trbl_padding: Tuple[int, int, int, int] = trbl_padding
        self.click_command = click_command
        # -----   -----
        # NOTE - default font
        DF = ft.SysFont('', 20)
        line_height = DF.render('0123456789abcdefghijklmnopqrstwuxyz')[
            0].get_height()
        temp_surfaces = []
        for i, (fg, bg) in enumerate((
                (self.colors.fg_normal, self.colors.bg_normal),
                (self.colors.fg_click, self.colors.bg_click),
                (self.colors.fg_hover, self.colors.bg_hover))):
            # NOTE - generate button text surface
            temp1 = DF.render(
                text, fg, bg)[0]
            # NOTE - generate surfaces
            text_size = temp1.get_size()
            bg_width = text_size[0] + \
                self.trbl_padding[1] + self.trbl_padding[3]
            bg_height = line_height + \
                self.trbl_padding[0] + self.trbl_padding[2]
            s = pygame.Surface((bg_width, bg_height))
            s.fill(bg)
            s.blit(temp1, (self.trbl_padding[3], self.trbl_padding[0]))
            temp_surfaces.append(s)
        self._surfaces: ButtonSurfaces = ButtonSurfaces(*temp_surfaces)
        # -----   -----
        self.surface = self._surfaces.normal
        self.rect = pygame.Rect(self.surface.get_rect())
        self.rect.top = y
        self.rect.left = x
        # -----   ------
        return None

    def on_event(self, event) -> None:
        self.surface = self._surfaces.normal
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            self.surface = self._surfaces.normal
            if not self.rect.collidepoint(event.pos):
                return
            # NOTE - hovered
            if event.type == pygame.MOUSEMOTION:
                self.surface = self._surfaces.hover
            # NOTE - released
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click_command.execute()
                self.surface = self._surfaces.hover
            # NOTE - pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.surface = self._surfaces.click

        return None

    def on_update(self) -> None:
        return None

    def on_render(self) -> Tuple[pygame.Surface, pygame.Rect]:
        return self.surface, self.rect
