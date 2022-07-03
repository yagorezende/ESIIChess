import pygame

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
        padding = (self.surface.get_width() - (self.surface.get_width() * .3 + white_card_sprite.get_width() * 3)) / 4
        top_padding = self.surface.get_height() / 2 - white_card_sprite.get_height() / 2
        self.white_card_button = Button(white_card_sprite, (padding, top_padding), alpha=True)
        self.black_card_button = Button(black_card_sprite, (2 * padding + white_card_sprite.get_width(), top_padding),
                                        alpha=True)
        self.random_card_button = Button(random_card_sprite,
                                         (3 * padding + 2 * white_card_sprite.get_width(), top_padding), alpha=True)
        # Labels
        self.white_card_button_label = pygame.image.load("assets/images/WhitesLabel.png")
        self.blacks_card_button_label = pygame.image.load("assets/images/BlacksLabel.png")
        self.random_card_button_label = pygame.image.load("assets/images/RandomLabel.png")
        # [END OF CARDS WIDGET]

        # Title
        self.title = pygame.image.load("assets/images/MatchSettingsTitle.png").convert_alpha()

        self.widgets = [self.white_card_button, self.black_card_button, self.random_card_button]

    def on_render(self):
        # blit cards buttons
        self.surface.blit(*self.white_card_button.on_render())
        self.surface.blit(*self.black_card_button.on_render())
        self.surface.blit(*self.random_card_button.on_render())

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
