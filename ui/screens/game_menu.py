import pygame
import pygame.freetype as ft
from ui.screens.game_screen import GameScreen
from ui.screens.generic_screen import GenericScreen
from ui.screens.navigator import Navigator


class GameMenu(GenericScreen):
    def __init__(self) -> None:
        super().__init__()
        self.defaut_font = ft.SysFont("", 20)

    # ----------

    def on_enter(self) -> None:
        return super().on_enter()

    def on_event(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONUP:
            Navigator().show(GameScreen())
        return None

    def on_loop(self) -> None:
        return super().on_loop()

    def on_render(self, scr_surf: pygame.Surface) -> None:
        title_surf, title_rect = self.defaut_font.render(
            "ESIIChess",
            fgcolor=(255, 255, 255),
            size=scr_surf.get_height()/8)
        press_any_surf, press_any_rect = self.defaut_font.render(
            "[ CLICK TO START ]",
            fgcolor=(255, 255, 255),
            size=scr_surf.get_height()/32)
        # ----------
        scr_surf.fill((0, 0, 0))
        scr_surf.blit(
            title_surf, (
                (scr_surf.get_width()-title_rect.width)*0.5,
                (scr_surf.get_height()-title_rect.height)*0.1,
                title_rect.width, title_rect.height))
        scr_surf.blit(
            press_any_surf, (
                (scr_surf.get_width() - press_any_rect.width)*0.5,
                (scr_surf.get_height()-press_any_rect.height)*0.9,
                press_any_rect.width, press_any_rect.height))
        return None

    def on_leave(self) -> None:
        return super().on_leave()
