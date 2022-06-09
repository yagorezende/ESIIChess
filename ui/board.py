from typing import Tuple
import pygame

from logic.const import TILE_SIZE

class BoardTile:
    def __init__(self, dark=True, x=0, y=0, offset=0):
        if dark:
            self.normal_sprite = pygame.image.load("assets/images/tile-dark.png").convert()
            self.highlight_sprite = pygame.image.load("assets/images/tile-dark-highlight.png").convert()
            self.danger_sprite = pygame.image.load("assets/images/tile-dark-danger.png").convert()
        else:
            self.normal_sprite = pygame.image.load("assets/images/tile-light.png").convert()
            self.highlight_sprite = pygame.image.load("assets/images/tile-light-highlight.png").convert()
            self.danger_sprite = pygame.image.load("assets/images/tile-light-danger.png").convert()
        self.x = x
        self.y = y
        self.offset = offset
        self.sprite = self.normal_sprite

    def turn_light(self, on=False):
        if on:
            self.sprite = self.highlight_sprite
        else:
            self.sprite = self.normal_sprite

    def render(self):
        return self.sprite, (self.y + self.offset, self.x + self.offset)

    def turn_red(self):
        self.sprite = self.danger_sprite


class ChessPiece:
    def __init__(self, type="p", color="w", x=0, y=0, offset=0):
        self.sprite = pygame.image.load(f"assets/images/{color}{type}.png").convert_alpha()
        self.type = type
        self.color = color
        self.x = x
        self.y = y
        self.active = True
        self.offset = offset
        self._event_keeper = None

        if type == 'p':
            self.has_jumped = False

        elif type == 'k' or type == 'r':
            self.has_moved = False

    def move(self, pos:tuple):
        self.x, self.y = pos

    def get_board_pos(self) -> Tuple[int, int]:
        return int(self.y / TILE_SIZE - self.offset), int(self.x / TILE_SIZE - self.offset)

    def render(self):
        return self.sprite, (self.x + self.offset, self.y + self.offset)

    def reload_sprite(self):
        self.sprite = self._load_sprite()

    def _load_sprite(self):
        return pygame.image.load(f"assets/images/{self.color}{self.type}.png").convert_alpha()