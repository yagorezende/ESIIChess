from typing import List

import pygame


class BoardTile:
    def __init__(self, dark=True, x=0, y=0):
        if dark:
            self.sprite = pygame.image.load("assets/images/tile-dark.png").convert()
        else:
            self.sprite = pygame.image.load("assets/images/tile-light.png").convert()
        self.x = x
        self.y = y

    def render(self):
        return self.sprite, (self.x, self.y)


class Board:
    def __init__(self):
        self.grid: List[BoardTile] = []

    def init_board(self):
        white = True
        for i in range(8):
            for j in range(8):
                self.grid.append(BoardTile(white, 80*j, 80*i))
                white = not white
            white = not white

    def on_render(self, surface):
        for tile in self.grid:
            surface.blit(*tile.render())
