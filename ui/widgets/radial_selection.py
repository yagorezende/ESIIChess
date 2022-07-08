from typing import List, NamedTuple, Tuple, Dict, Sequence

import pygame
import pygame.freetype as ft
import ui.widgets.generic_widget as gw


class TSR(NamedTuple):
    """
    Wrap the text, surface and rect together.
    """
    text: str
    surface: pygame.surface.Surface
    rect: pygame.rect.Rect


class RadialSelection(gw.GenericWidget):
    def __init__(self, x, y, title: str, options: Sequence[str], default: int = 0, highlight_color: Tuple[int,int,int] = (30,127,30)) -> None:
        super().__init__()
        self.selected_option: Tuple[int, str] = (default, options[default])
        # -----   -----
        TEXT_COLOR: Tuple[int, int, int] = (255, 255, 255)
        self._LEFT_PADDING: int = 10
        self._BOTTOM_PADDING: int = 2
        # NOTE - default font
        DF = ft.SysFont("", 20)
        self._title: TSR = TSR(title, *DF.render(title, TEXT_COLOR))
        self._title.rect.y = 0
        self._options: List[TSR] = [
            TSR(o, *DF.render(o, TEXT_COLOR)) for o in options]
        # -----   -----
        self._indicators: Dict[str, TSR] = {}
        indicator = '# '
        self._indicators['hover'] = TSR(
            indicator, *DF.render(indicator, highlight_color))
        self._indicators['selected'] = TSR(
            indicator, *DF.render(indicator, TEXT_COLOR))
        widest_indicator = max(
            [o.rect.width for o in self._indicators.values()])
        # -----   -----
        # NOTE - update position for each option
        self._LINE_HIGHT = DF.render('0123456789abcdefghijklmnopqrstuwxyz')[0].get_height()
        for i in range(len(self._options)):
            opt = self._options[i]
            opt.rect.left = self._LEFT_PADDING + widest_indicator
            opt.rect.top = (i+1)*(self._LINE_HIGHT+self._BOTTOM_PADDING)
        # -----   -----
        self.rect = pygame.Rect((x, y), self._find_size())
        self.surface = pygame.Surface(self.rect.size)
        # -----   -----
        # NOTE - Generate the base surface that is going to be updated later
        self.surface.blit(self._title.surface, self._title.rect)
        for opt in self._options:
            self.surface.blit(opt.surface, opt.rect)
        # -----   -----
        self._update_indicators()
        return None

    def _find_size(self) -> Tuple[int, int]:
        """
        Calculate this widget width and height.
        """
        w = self._title.rect.width
        h = (len(self._options)+1)*(self._LINE_HIGHT + self._BOTTOM_PADDING)
        # NOTE - find the widest element
        for opt in self._options:
            if self._LEFT_PADDING+opt.rect.width > w:
                w = self._LEFT_PADDING+opt.rect.width
        return w, h

    def _update_indicators(self, i_hover=-1) -> None:
        """
        Update the surface to show the current selected option and highlight
        that under the mouse.

        `value` is the option being hovered.
        """
        # NOTE - clear the indicators
        clear_area = pygame.Rect(
            0, self._title.rect.bottom,
            self._options[0].rect.left, self.rect.height-self._title.rect.height)
        self.surface.fill((0, 0, 0, 0), clear_area)
        # NOTE - show the selected option
        indicator = self._indicators['selected']
        indicator.rect.right = self._options[self.selected_option[0]].rect.left
        indicator.rect.top = self._options[self.selected_option[0]].rect.top
        self.surface.blit(indicator.surface, indicator.rect)
        # NOTE - exit if no option being hovered
        if i_hover == -1 or i_hover > len(self._options):
            return None
        # NOTE - show the hovered option
        indicator = self._indicators['hover']
        indicator.rect.right = self._options[i_hover].rect.left
        indicator.rect.top = self._options[i_hover].rect.top
        self.surface.blit(indicator.surface, indicator.rect)
        return None

    def on_event(self, event) -> None:
        if not self.active:
            return
        self._update_indicators()
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            if not self.rect.collidepoint(event.pos):
                return None
            hovered = -1
            for i, (t, _, r) in enumerate(self._options):
                pos = list(event.pos[:])
                # NOTE - check if the event.pos is inside the widget
                pos[0] -= self.rect.left
                pos[1] -= self.rect.top
                if r.collidepoint(pos):
                    hovered = i
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.selected_option = (i, t)
                    break
            self._update_indicators(hovered)
        return None

    def on_update(self) -> None:
        if not self.active:
            return None
        return None

    def on_render(self) -> Tuple[pygame.Surface, pygame.Rect]:
        return self.surface, self.rect
