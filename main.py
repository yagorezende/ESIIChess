import sys
import pygame

from logic.game_overall_context import GameOverallContext
from ui.screens.game_menu import GameMenu
from ui.screens.navigator import Navigator

GAME_TITLE = 'ESII Chess'

class App:
    def __init__(self):
        self._running = True
        self.fps_clock = None
        self._display_surf = None
        self._display_flags = pygame.HWSURFACE | pygame.DOUBLEBUF
        self._is_fullscreen: bool = False
        self._FPS_LIMIT = 60
        self.size = self.width, self.height = 850, 640
        self.navigator = Navigator()
        GameOverallContext().set_color('w')  # essa linha faz nada, é só pra inicializar o Singleton

    def on_init(self):
        pygame.init()
        self._create_display_window(self.size, self._display_flags, GAME_TITLE)
        self._running = True
        self.fps_clock = pygame.time.Clock()

        # init gameobjects
        self.navigator.show(GameMenu(self._display_surf))

        return True

    def _create_display_window(self, size, flags, title: str = '') -> None:
        self._display_surf = pygame.display.set_mode(size, flags)
        if title:
            pygame.display.set_caption(title)

    def on_event(self, event):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_F11:
            if self._is_fullscreen:
                self._display_flags &= ~pygame.FULLSCREEN
                self._display_flags &= ~pygame.SCALED
            else:
                self._display_flags |= pygame.FULLSCREEN
                self._display_flags |= pygame.SCALED
            self._create_display_window(self.size, self._display_flags, GAME_TITLE)
            self._is_fullscreen = not self._is_fullscreen

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
                self.navigator.on_event(event)
            self.on_loop()
            self.navigator.on_loop()
            self.navigator.on_render()
            self.on_render()
            self.fps_clock.tick(self._FPS_LIMIT)
        self.on_cleanup()


def main(argv):
    theApp = App()
    theApp.on_execute()


if __name__ == "__main__":
    main(sys.argv[1:])
