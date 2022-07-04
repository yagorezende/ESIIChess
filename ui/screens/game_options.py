from typing import Tuple

import pygame

import logic.selected_options as sp
import ui.screens.generic_screen as gs
from logic.start_game_command import StartGameCommand
from ui.widgets.radial_selection import RadialSelection
from ui.widgets.settings_container import SettingsContainer
from ui.widgets.settings_navigator import SettingsNavigator
from ui.widgets.text_button import TextButton


class GameOptions(gs.GenericScreen):
    def __init__(self, surface):
        super().__init__(surface)
        self.screen_size = [0, 0]
        self._WIDGETS_PADDING: int = 10
        self.background_sprite = pygame.image.load("assets/images/BackgroundBlur.png").convert()
        self.background_sprite = pygame.transform.scale(self.background_sprite, size=surface.get_size())

        # Navigator
        self.navigator = SettingsNavigator(self.surface)
        self.container = SettingsContainer(self.surface)

        self.widgets = [self.navigator, self.container]

        self.oponent = RadialSelection(
            0, 0,
            title='Play against:',
            options=[names.name.capitalize() for names in sp.Oponent],
            default=0)
        self.color = RadialSelection(
            0, 0,
            title='Choose your color',
            options=[names.name.capitalize() for names in sp.Color],
            default=0)
        self.difficulty = RadialSelection(
            0, 0,
            title='Choose the game difficulty',
            options=[names.name.capitalize() for names in sp.Difficulty],
            default=0)
        self.difficulty.active = not self.oponent.selected_option[0] == 0
        # self.button_continue = TextButton(
        #     0, 0,
        #     text='Play',
        #     bg_color_normal=(30, 127, 30),
        #     bg_color_hover=(30, 117, 30),
        #     bg_color_click=(30, 107, 30),
        #     trbl_padding=(5, 20, 5, 20),
        #     click_command=StartGameCommand(game_options_screen=self))

    def on_enter(self) -> None:
        return None

    def on_event(self, event) -> None:
        for widget in self.widgets:
            widget.on_event(event)

        self.oponent.on_event(event)
        self.color.on_event(event)
        self.difficulty.active = not self.oponent.selected_option[0] == 0
        if self.difficulty.active:
            self.difficulty.on_event(event)
        # self.button_continue.on_event(event)
        return None

    def on_loop(self) -> None:
        return None

    def on_render(self) -> None:
        self.draw_background()
        # NOTE - update widgets position if they aren't correct
        self._update_widgets_position(self.surface.get_size())
        self.navigator.on_render()
        self.container.on_render()
        return None

    def _update_widgets_position(self, screen_size: Tuple[int, int]) -> None:
        if screen_size[0] != self.screen_size[0] or screen_size[1] != self.screen_size[1]:
            self.screen_size = list(screen_size)
            # -----   -----
            width_diff = self.screen_size[0] - self.oponent.rect.width
            self.oponent.rect.left = int(0.35 * width_diff)
            height_diff = self.screen_size[1] - self.oponent.rect.height
            self.oponent.rect.top = int(0.15 * height_diff)
            # -----   -----
            self.color.rect.topleft = self.oponent.rect.bottomleft
            self.color.rect.top += self._WIDGETS_PADDING
            # -----   -----
            self.difficulty.rect.topleft = self.color.rect.bottomleft
            self.difficulty.rect.top += self._WIDGETS_PADDING
        return None

    def on_leave(self) -> None:
        return None
