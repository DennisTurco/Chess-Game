import pygame
import pygame_menu
from pygame_menu import themes, events

import GameManager

class Menu:
    def __init__(self):
        self.mode = None
        self.elo = 1200

        custom_theme = themes.THEME_SOLARIZED.copy()
        custom_theme.title_font = pygame_menu.font.FONT_MUNRO
        custom_theme.widget_font = pygame_menu.font.FONT_MUNRO
        custom_theme.title_font_size = 60
        custom_theme.widget_font_size = 35

        programIcon = pygame.image.load('images/wK.png')
        pygame.display.set_icon(programIcon)

        self.main_menu = pygame_menu.Menu(
            title=f'Welcome to {GameManager.APP_NAME}',
            width=GameManager.WINDOW_WIDTH,
            height=GameManager.HEIGHT,
            theme=custom_theme
        )
        self.mode_menu = pygame_menu.Menu(
            title='Modes',
            width=GameManager.WINDOW_WIDTH,
            height=GameManager.HEIGHT,
            theme=custom_theme
        )

        self.mode_menu.add.button('Player vs Player', self.select_pvp)
        self.mode_menu.add.button('Player vs AI', self.elo_menu)
        self.mode_menu.add.button('Back', events.BACK)

        self.elo_select_menu = pygame_menu.Menu(
            title='Select AI Difficulty (ELO)',
            width=GameManager.WINDOW_WIDTH,
            height=GameManager.HEIGHT,
            theme=custom_theme
        )
        self.elo_select_menu.add.selector('ELO level:', [
            ('400', 400), ('600', 600), ('800', 800), ('1000', 1000), ('1200', 1200), ('1500', 1500),
            ('1800', 1800), ('2000', 2000), ('2200', 2200), ('2500', 2500),
            ('2800', 2800), ('3000', 3000)
            ], onchange=self.set_elo)
        self.elo_select_menu.add.button('Start AI Game', self.select_ai)
        self.elo_select_menu.add.button('Back', lambda: self.main_menu.mainloop(self.surface))

        self.main_menu.add.button('Play / Modes', self.mode_menu)
        self.main_menu.add.button('Quit', events.EXIT)

        self.surface = None

    def set_elo(self, selected, value: int) -> None:
        self.elo = value

    def elo_menu(self) -> None:
        self.elo_select_menu.mainloop(self.surface)

    def select_pvp(self) -> None:
        self.mode = "pvp"
        self.main_menu.disable()

    def select_ai(self) -> None:
        self.mode = "ai"
        self.elo_select_menu.disable()

    def mainloop(self, surface: pygame.Surface) -> tuple[str | None, int]:
        self.surface = surface
        self.main_menu.mainloop(surface)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return self.mode, self.elo