import logging
import pygame
import pygame_menu
from pygame_menu import events

from Enums.Mode import Mode
from Enums.Piece import Color
from Menus.Menu import Menu
import GameManager

class MainMenu(Menu):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        super().__init__()
        self.mode = None
        self.elo = 1200
        self.color_side = Color.WHITE

        programIcon = pygame.image.load('assets/images/wK.png')
        pygame.display.set_icon(programIcon)

        self.main_menu = pygame_menu.Menu(
            title=f'Welcome to {GameManager.APP_NAME}',
            width=self.WIDTH,
            height=self.HEIGHT,
            theme=self.custom_theme
        )
        self.mode_menu = pygame_menu.Menu(
            title='Modes',
            width=self.WIDTH,
            height=self.HEIGHT,
            theme=self.custom_theme
        )

        self.mode_menu.add.button('Player vs Player', self.select_pvp)
        self.mode_menu.add.button('Player vs AI', self.elo_menu)
        self.mode_menu.add.button('Back', events.BACK)

        self.elo_select_menu = pygame_menu.Menu(
            title='Select AI Difficulty (ELO)',
            width=self.WIDTH,
            height=self.HEIGHT,
            theme=self.custom_theme
        )
        self.elo_select_menu.add.selector('ELO level:', [
            ('400', 400), ('600', 600), ('800', 800), ('1000', 1000), ('1200', 1200), ('1500', 1500),
            ('1800', 1800), ('2000', 2000), ('2200', 2200), ('2500', 2500),
            ('2800', 2800), ('3000', 3000)
            ], default=4, onchange=self.set_elo)
        self.elo_select_menu.add.selector('Color:', [
            ('White', Color.WHITE), ('Black', Color.BLACK)
            ], default=0, onchange=self.set_color_side)
        self.elo_select_menu.add.button('Start AI Game', self.select_ai)
        self.elo_select_menu.add.button('Back', lambda: self.main_menu.mainloop(self.surface))

        self.main_menu.add.button('Play / Modes', self.mode_menu)
        self.main_menu.add.button('Quit', events.EXIT)

        self.surface = None

    def set_elo(self, selected, value: int) -> None:
        self.elo = value

    def set_color_side(self, selected, value: Color) -> None:
        self.color_side = value

    def elo_menu(self) -> None:
        self.elo_select_menu.mainloop(self.surface)

    def select_pvp(self) -> None:
        self.logger.info("Mode selected: Player vs Player")
        self.mode = Mode.PVP
        self.main_menu.disable()

    def select_ai(self) -> None:
        self.logger.info("Mode selected: Player vs AI")
        self.mode = Mode.PVE
        self.elo_select_menu.disable()
        self.main_menu.disable()

    def mainloop(self, surface: pygame.Surface) -> tuple[Mode | None, int, Color]:
        self.surface = surface
        self.main_menu.mainloop(surface)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return self.mode, self.elo, self.color_side