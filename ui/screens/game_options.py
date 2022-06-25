from typing import List, Tuple
import pygame
import ui.screens.generic_screen as gs
import ui.widgets.generic_widget as gw
from ui.widgets.radial_selection import RadialSelection
from ui.widgets.text_button import TextButton


class GameOptions(gs.GenericScreen):
    def __init__(self) -> None:
        self.screen_size = [0,0]
        self._WIDGETS_PADDING: int = 10
        self.oponent = RadialSelection(
            0, 0,
            title='Play against:',
            options=('Human', 'AI'),
            default=0)
        self.color = RadialSelection(
            0, 0,
            title='Choose your color',
            options=('White', 'Black', 'Random'),
            default=0)
        self.dificulty = RadialSelection(
            0, 0,
            title='Choose the game dificulty',
            options=('Easy', 'Normal', 'Hard'),
            default=0)
        self.button_continue = TextButton(
            0, 0,
            text='Play',
            bg_color_normal=(30,127,30),
            bg_color_hover=(30,117,30),
            bg_color_click=(30,107,30),
            trbl_padding=(5,20,5,20))
        return None

    def on_enter(self) -> None:
        return None

    def on_event(self, event) -> None:
        # for w in self._widgets:
        #     w.on_event(event)
        self.oponent.on_event(event)
        self.color.on_event(event)
        self.dificulty.active = not self.oponent.selected_option[0] == 0
        if self.dificulty.active:
            self.dificulty.on_event(event)
        self.button_continue.on_event(event)
        return None

    def on_loop(self) -> None:
        return None

    def on_render(self, scr_surf: pygame.Surface) -> None:
        # NOTE - update widgets position if they aren't correct
        self._update_widgets_position(scr_surf.get_size())
        # NOTE - clear the screen surface
        scr_surf.fill((0, 0, 0))
        scr_surf.blit(*self.oponent.on_render())
        scr_surf.blit(*self.color.on_render())
        if self.dificulty.active:
            scr_surf.blit(*self.dificulty.on_render())
        scr_surf.blit(*self.button_continue.on_render())
        return None

    def _update_widgets_position(self,screen_size: Tuple[int,int]) -> None:
        if screen_size[0] != self.screen_size[0] or screen_size[1] != self.screen_size[1]:
            self.screen_size = list(screen_size)
            # -----   -----
            width_diff = self.screen_size[0]-self.oponent.rect.width
            self.oponent.rect.left = int(0.35*width_diff)
            height_diff = self.screen_size[1]-self.oponent.rect.height
            self.oponent.rect.top = int(0.15*height_diff)
            # -----   -----
            self.color.rect.topleft = self.oponent.rect.bottomleft
            self.color.rect.top += self._WIDGETS_PADDING
            # -----   -----
            self.dificulty.rect.topleft = self.color.rect.bottomleft
            self.dificulty.rect.top += self._WIDGETS_PADDING
            # -----   -----
            width_diff = self.screen_size[0]-self.button_continue.rect.width
            self.button_continue.rect.left = int(0.5*width_diff)
            height_diff = self.screen_size[1]-self.button_continue.rect.height
            self.button_continue.rect.top = int(0.9*height_diff)
        return None

    def on_leave(self) -> None:
        return None
