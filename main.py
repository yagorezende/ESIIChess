import pygame
from pygame.locals import *

from ui.board import Board


class App:
    def __init__(self):
        self._running = True
        self.fps_clock = None
        self._display_surf = None
        self._FPS_LIMIT = 60
        self.size = self.width, self.height = 640, 640
        self.board = Board()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(
            self.size, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._running = True
        self.fps_clock = pygame.time.Clock()

        # init gameobjects
        self.board.init_board()

        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            self.board.on_click()
        
    def on_loop(self):
        """
        Use this method to process the next step of the game
        :return: None
        """
        pass

    def on_render(self):
        """
        Use this method to render all objects in the game
        :return: None
        """
        # display the board first
        self.board.on_render(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        """
        Use this method to exit the game cleaning everything
        :return: None
        """
        pygame.quit()

    def on_execute(self):
        if not self.on_init():
            print("quiting")
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.fps_clock.tick(self._FPS_LIMIT)
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
