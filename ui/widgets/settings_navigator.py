import pygame

from logic.start_game_command import StartGameCommand
from logic.toggle_sound_command import ToggleSoundCommand
from ui.widgets.button_widget import Button
from ui.widgets.generic_widget import GenericWidget

NAV_COLOR = pygame.Color(255, 255, 255, 35)
SPACE_PERCENT = .3


class SettingsNavigator(GenericWidget):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.surface = surface
        self.brand_sprite = pygame.image.load("assets/images/NavigatorBrand.png")
        self.x = self.surface.get_width() - self.get_width()
        self.centerX = self.surface.get_width() - self.get_width() / 2

        start_btn = pygame.image.load("assets/images/NavigatorStartMatch.png")
        start_btn_hover = pygame.image.load("assets/images/NavigatorStartMatch_hover.png")

        self.start_match_btn = Button(start_btn,
                                      (self.centerX - start_btn.get_width() / 2,
                                       self.surface.get_height() - start_btn.get_height() - 90),
                                      alpha=True, action=StartGameCommand(), hover_sprite=start_btn_hover)

        checkbox_sprite_off = pygame.image.load("assets/images/Checkbox_off.png")
        checkbox_sprite_on = pygame.image.load("assets/images/Checkbox_on.png").convert_alpha()
        checkbox_sprite_hover = pygame.image.load("assets/images/Checkbox_hover.png").convert_alpha()
        self.sound_checkbox = Button(checkbox_sprite_off,
                                     (self.x + 50, self.surface.get_height() * .7),
                                     alpha=True,
                                     hover_sprite=checkbox_sprite_hover,
                                     selected_sprite=checkbox_sprite_on,
                                     selectable=True,
                                     checkable=True,
                                     trigger=True)
        self.sound_checkbox.action = ToggleSoundCommand(self.sound_checkbox)

        # Sound selected as default
        self.sound_checkbox.selected = True
        self.sound_checkbox.surface = self.sound_checkbox.selected_sprite

        # Labels
        self.sound_checkbox_label = pygame.image.load("assets/images/SoundLabel.png")

        self.widgets = [self.start_match_btn, self.sound_checkbox]

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
        checkbox_center = self.sound_checkbox.align_center(self.sound_checkbox_label)
        self.surface.blit(self.brand_sprite, (nav_center[0] - self.brand_sprite.get_width() / 2, 0))
        self.surface.blit(self.sound_checkbox_label,
                          (checkbox_center[0] + self.sound_checkbox_label.get_width() / 2 + 28,
                           checkbox_center[1] + self.sound_checkbox.surface.get_height()/2 + self.sound_checkbox_label.get_height()/2))
        self.surface.blit(*self.start_match_btn.on_render())
        self.surface.blit(*self.sound_checkbox.on_render())
