import pygame
import pygame.freetype as ft
from ui.screens.game_options import GameOptions
from ui.screens.generic_screen import GenericScreen
from ui.screens.navigator import Navigator


class GameMenu(GenericScreen):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface)
        self.default_font = ft.SysFont("", 20)
        self.background_sprite = pygame.image.load("assets/images/menu-bg.jpg").convert()
        self.background_sprite = pygame.transform.scale(self.background_sprite, size=surface.get_size())
        self.logo_sprite = pygame.image.load("assets/images/Brand.png").convert_alpha()
        self.click_start_sprite = pygame.image.load("assets/images/ClickStart.png").convert_alpha()

        self.game_settings = GameOptions(self.surface)
        self.widgets = [self.game_settings]

    def on_enter(self) -> None:
        return super().on_enter()

    def on_event(self, event) -> None:
        super(GameMenu, self).on_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            # NOTE - mantain this screen on stack
            Navigator().show(self.game_settings)
        return None

    def on_loop(self) -> None:
        return super().on_loop()

    def on_render(self) -> None:
        # background
        logo_rect = self.logo_sprite.get_rect()
        logo_rect.center = self.get_center()
        self.draw_background()
        self.surface.blit(self.logo_sprite, (logo_rect[0], 75))
        click_rect = self.click_start_sprite.get_rect()
        click_rect.center = self.get_center()
        self.surface.blit(self.click_start_sprite, (click_rect[0], click_rect[1]*1.85))

    def on_leave(self) -> None:
        return super().on_leave()
