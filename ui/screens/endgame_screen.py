import pygame

from ui.screens.generic_screen import GenericScreen
from ui.screens.navigator import Navigator


class EndGameScreen(GenericScreen):
    def __init__(self, surface: pygame.Surface, result: str) -> None:
        """
        Use this screen to show the final result of a match
        :param surface: pygame Surface as reference
        :param result: str containing the result: w|b|draw
        """
        super().__init__(surface)
        print(f"------>", result, type(result))
        if result == 'b':
            self.banner = pygame.image.load("assets/images/WhiteWins.png").convert_alpha()
        elif result == 'w':
            self.banner = pygame.image.load("assets/images/BlackWins.png").convert_alpha()
        else:
            self.banner = pygame.image.load("assets/images/Draw.png").convert_alpha()

        self.x = (self.surface.get_width() * .7) / 2 - self.banner.get_width() / 2
        self.y = self.surface.get_height() / 2 - self.banner.get_height() / 2
        self.rect = (self.x, self.y)
        self._transparency = 255
        self._initial_surface = surface.copy()

    def on_enter(self) -> None:
        return super().on_enter()

    def on_event(self, event) -> None:
        super(EndGameScreen, self).on_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self._transparency = 140 if self._transparency == 255 else 255
        if event.type == pygame.KEYUP and event.unicode == '\r':
            print("Done")
            Navigator().close_actual_screen()
            Navigator().close_actual_screen()
        return None

    def on_loop(self) -> None:
        return super().on_loop()

    def on_render(self) -> None:
        self.surface.blit(self._initial_surface, (0,0))
        self.banner.set_alpha(self._transparency)
        self.surface.blit(self.banner, self.rect)

    def on_leave(self) -> None:
        return super().on_leave()
