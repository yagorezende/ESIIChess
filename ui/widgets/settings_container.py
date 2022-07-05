import pygame

from logic.game_overall_context import GameOverallContext, IA, MULTIPLAYER
from logic.select_color_command import SelectColorCommand
from logic.select_opponent_command import SelectOpponentCommand
from ui.widgets.button_widget import Button
from ui.widgets.generic_widget import GenericWidget


class SettingsContainer(GenericWidget):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.surface = surface

        # [CARDS WIDGET]
        white_card_sprite = pygame.image.load("assets/images/WhitesCard.png")
        black_card_sprite = pygame.image.load("assets/images/BlacksCard.png")
        random_card_sprite = pygame.image.load("assets/images/RandomCard.png")
        # [CARDS WIDGET Hover]
        white_card_sprite_hover = pygame.image.load("assets/images/WhitesCard_hover.png")
        black_card_sprite_hover = pygame.image.load("assets/images/BlacksCard_hover.png")
        random_card_sprite_hover = pygame.image.load("assets/images/RandomCard_hover.png")

        padding = (self.surface.get_width() - (self.surface.get_width() * .3 + white_card_sprite.get_width() * 3)) / 4
        top_padding = self.surface.get_height() / 2 - white_card_sprite.get_height() / 2
        self.card_group = []
        self.white_card_button = Button(white_card_sprite, (padding, top_padding),
                                        action=SelectColorCommand("w"), drop=False, group=self.card_group,
                                        selected_sprite=white_card_sprite_hover,
                                        alpha=True, hover_sprite=white_card_sprite_hover, selectable=True,
                                        checkable=True)
        self.black_card_button = Button(black_card_sprite, (2 * padding + white_card_sprite.get_width(), top_padding),
                                        selected_sprite=black_card_sprite_hover,
                                        action=SelectColorCommand("b"), drop=False, group=self.card_group,
                                        alpha=True, hover_sprite=black_card_sprite_hover, selectable=True,
                                        checkable=True)
        self.random_card_button = Button(random_card_sprite,
                                         (3 * padding + 2 * white_card_sprite.get_width(), top_padding),
                                         selected_sprite=random_card_sprite_hover,
                                         action=SelectColorCommand("random"), drop=False, checkable=True,
                                         group=self.card_group,
                                         alpha=True, hover_sprite=random_card_sprite_hover, selectable=True)
        self.card_group.append(self.white_card_button)
        self.card_group.append(self.black_card_button)
        self.card_group.append(self.random_card_button)

        self.white_card_button.selected = True
        self.white_card_button.surface = self.white_card_button.hover_sprite
        # Labels
        self.white_card_button_label = pygame.image.load("assets/images/WhitesLabel.png")
        self.blacks_card_button_label = pygame.image.load("assets/images/BlacksLabel.png")
        self.random_card_button_label = pygame.image.load("assets/images/RandomLabel.png")
        # [END OF CARDS WIDGET]

        # Title
        self.title = pygame.image.load("assets/images/MatchSettingsTitle.png").convert_alpha()

        # Sound checkbox
        checkbox_sprite_off = pygame.image.load("assets/images/Checkbox_off.png")
        checkbox_sprite_on = pygame.image.load("assets/images/Checkbox_on.png").convert_alpha()
        checkbox_sprite_hover = pygame.image.load("assets/images/Checkbox_hover.png").convert_alpha()
        self.checkbox_group = []
        self.IA_checkbox = Button(checkbox_sprite_off,
                                  (self.surface.get_width() * .15, self.surface.get_height() - 80),
                                  action=SelectOpponentCommand(IA),
                                  alpha=True,
                                  hover_sprite=checkbox_sprite_hover,
                                  selected_sprite=checkbox_sprite_on,
                                  selectable=True,
                                  checkable=True, group=self.checkbox_group)

        self.multiplayer_checkbox = Button(checkbox_sprite_off,
                                           (self.surface.get_width() * .40, self.surface.get_height() - 80),
                                           action=SelectOpponentCommand(MULTIPLAYER),
                                           alpha=True,
                                           hover_sprite=checkbox_sprite_hover,
                                           selected_sprite=checkbox_sprite_on,
                                           selectable=True,
                                           checkable=True, group=self.checkbox_group)

        self.checkbox_group.append(self.IA_checkbox)
        self.checkbox_group.append(self.multiplayer_checkbox)
        # Checkbox Labels
        self.IA_checkbox_label = pygame.image.load("assets/images/IALabel.png").convert_alpha()
        self.multiplayer_checkbox_label = pygame.image.load("assets/images/MultiplayerLabel.png").convert_alpha()

        # IA selected as default
        self.IA_checkbox.selected = True
        self.IA_checkbox.surface = self.IA_checkbox.selected_sprite

        self.widgets = [self.white_card_button, self.black_card_button, self.random_card_button, self.IA_checkbox,
                        self.multiplayer_checkbox]
        self._mark_selected()

    def _mark_selected(self):
        if GameOverallContext().get_color() == "w":
            self.white_card_button.selected = True
        else:
            self.black_card_button.selected = True

    def on_render(self):
        # blit widgets
        for widget in self.widgets:
            self.surface.blit(*widget.on_render())

        # blit cards labels
        rect = self.white_card_button.align_center(self.white_card_button_label)
        self.surface.blit(self.white_card_button_label,
                          (rect[0], rect[1] + self.white_card_button.surface.get_height() * .75))
        rect = self.black_card_button.align_center(self.blacks_card_button_label)
        self.surface.blit(self.blacks_card_button_label,
                          (rect[0], rect[1] + self.white_card_button.surface.get_height() * .75))
        rect = self.random_card_button.align_center(self.random_card_button_label)
        self.surface.blit(self.random_card_button_label,
                          (rect[0], rect[1] + self.white_card_button.surface.get_height() * .78))

        rect = self.black_card_button.align_center(self.title)
        self.surface.blit(self.title, (rect[0], self.surface.get_height() * .10))

        # blit checkbox labels
        rect = self.IA_checkbox.align_center(self.IA_checkbox_label)
        self.surface.blit(self.IA_checkbox_label,
                          (rect[0] + self.IA_checkbox_label.get_width() / 2 + 28, rect[1]))

        rect = self.multiplayer_checkbox.align_center(self.multiplayer_checkbox_label)
        self.surface.blit(self.multiplayer_checkbox_label,
                          (rect[0] + self.multiplayer_checkbox_label.get_width() / 2 + 28, rect[1] + 44))
