import pygame
import logic.selected_options as sp

from ui.screens.game_screen import GameScreen
from ui.screens.navigator import Navigator
from ui.widgets.button_widget import Button
from ui.widgets.generic_widget import GenericWidget

NAV_COLOR = pygame.Color(255, 255, 255, 35)
SPACE_PERCENT = .3


class SettingsNavigator(GenericWidget):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.surface = surface
        self.brand_sprite = pygame.image.load("assets/images/NavigatorBrand.png")
        self.centerX = self.surface.get_width() - self.get_width() / 2

        start_btn = pygame.image.load("assets/images/NavigatorStartMatch.png")

        self.start_match_btn = Button(start_btn,
                                      (self.centerX - start_btn.get_width() / 2,
                                       self.surface.get_height() - start_btn.get_height() - 90),
                                      alpha=True, action=self.transition_to_game)

        self.widgets = [self.start_match_btn]

    def transition_to_game(self):
        opponent_enum_member = "IA"
        color_enum_member = "w"
        Navigator().show(GameScreen(
            Navigator().get_surface(),
            oponent=opponent_enum_member,  # type: ignore
            p1_color=color_enum_member,  # type: ignore
            difficulty=sp.Difficulty.EASY))

    def get_width(self):
        return self.surface.get_width() * SPACE_PERCENT

    def on_render(self):
        # RENDER BG
        rect = pygame.Rect(self.surface.get_width() - (self.get_width()), 0,
                           self.get_width(),
                           self.surface.get_height())
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, NAV_COLOR, shape_surf.get_rect())
        self.surface.blit(shape_surf, rect)
        # ENDOF RENDER BG

        # RENDER WIDGETS
        nav_center = rect.center
        self.surface.blit(self.brand_sprite, (nav_center[0] - self.brand_sprite.get_width() / 2, 0))
        self.surface.blit(*self.start_match_btn.on_render())
