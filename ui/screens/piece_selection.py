from typing import Dict, Tuple

import pygame
from logic.generic_command import GenericCommand
from ui.screens.generic_screen import GenericScreen
from ui.screens.navigator import Navigator


class PieceSelection(GenericScreen):
    def __init__(self) -> None:
        self.command_on_leave: GenericCommand = GenericCommand()
        self.command_on_enter: GenericCommand = GenericCommand()
        self.show_color = ''
        self.selected_piece = ''
        self.position: Tuple[float, float] = (0.5, 0.5)
        # ----------
        self._pieces_image: Dict[Tuple[str, str],
                                 Tuple[pygame.surface.Surface, pygame.rect.Rect]] = {}
        self._bg: Tuple[pygame.surface.Surface, pygame.rect.Rect] = (
            pygame.Surface((0, 0)), pygame.Rect(0, 0, 0, 0))
        return None

    def on_enter(self) -> None:
        self.command_on_enter.execute() # REVIEW - set the color to show
        bg_rect = pygame.Rect(0, 0, 0, 0)
        # NOTE - load the images
        c = self.show_color
        sum_width = 0
        for t in ('q', 'b', 'r', 'n'):
            img = pygame.image.load(
                f'assets/images/{c}{t}.png').convert_alpha()
            rect = img.get_rect()
            # NOTE - positioning images
            rect.x = sum_width
            self._pieces_image[(c, t)] = (img, rect)
            sum_width += rect.width
        # SECTION - update the bg
            # NOTE - as high as the higher image
            if rect.height > bg_rect.height:
                bg_rect.height = rect.height
        # NOTE - as wide as the wider set of images
        if sum_width > bg_rect.width:
            bg_rect.width = sum_width
        self._bg = (pygame.Surface((bg_rect.width, bg_rect.height)), bg_rect)
        self._bg[0].fill((255, 255, 255))
        # !SECTION
        return None

    def on_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            self.selected_piece = self._handle_selection(event.pos)
            if self.selected_piece:
                Navigator().close_actual_screen()
        return None

    def on_loop(self) -> None:
        return None

    def on_render(self) -> None:
        self._change_base_pos(self.surface.get_size())
        self.surface.blit(*self._bg)
        for (c, _), (i, r) in self._pieces_image.items():
            if c == self.show_color:
                self.surface.blit(i, r)
        return None

    def on_leave(self) -> None:
        self.command_on_leave.execute()
        return None

    # ----------

    def _change_base_pos(self, scr_size) -> None:
        """
        Change the position of all screen rects for the images if necessary.
        """
        # NOTE - to use relative position is needed the screen size which is
        # only known when rendering
        desired_x = (scr_size[0]-self._bg[1].width)*self.position[0]
        desired_y = (scr_size[1]-self._bg[1].height)*self.position[1]
        if self._bg[1].x == desired_x and self._bg[1].y == desired_y:
            return None
        acc_width = 0
        self._bg[1].topleft = (desired_x, desired_y)
        for (c, _), (_, r) in self._pieces_image.items():
            if c == self.show_color:
                r.x = desired_x + acc_width
                r.y = desired_y
                acc_width += r.width

    def _handle_selection(self, pos) -> str:
        """
        Returns the piece type selected by the player
        """
        if not self._bg[1].collidepoint(*pos):
            return ''
        for (c, t), (_, r) in self._pieces_image.items():
            if c == self.show_color:
                if r.collidepoint(*pos):
                    return t
        return ''
