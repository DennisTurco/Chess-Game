import pygame
import pygame_menu
from pygame_menu import themes, events

import GameManager

class Menu:
    def __init__(self):
        self.mode = None
        self.elo = 1200

        programIcon = pygame.image.load('images/wK.png')
        pygame.display.set_icon(programIcon)

        self.main_menu = pygame_menu.Menu(f'Welcome to {GameManager.APP_NAME}', GameManager.WINDOW_WIDTH, GameManager.HEIGHT, theme=themes.THEME_SOLARIZED)
        self.mode_menu = pygame_menu.Menu('Modes', GameManager.WINDOW_WIDTH, GameManager.HEIGHT, theme=themes.THEME_SOLARIZED)

        self.mode_menu.add.button('Player vs Player', self.select_pvp)
        self.mode_menu.add.button('Player vs AI', self.elo_menu)
        self.mode_menu.add.button('Back', events.BACK)

        self.elo_select_menu = pygame_menu.Menu('Select AI Difficulty (ELO)', GameManager.WINDOW_WIDTH, GameManager.HEIGHT, theme=themes.THEME_SOLARIZED)
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

    def set_elo(self, selected, value):
        self.elo = value

    def elo_menu(self):
        self.elo_select_menu.mainloop(self.surface)

    def select_pvp(self):
        self.mode = "pvp"
        self.main_menu.disable()

    def select_ai(self):
        self.mode = "ai"
        self.elo_select_menu.disable()

    def mainloop(self, surface):
        self.surface = surface
        self.main_menu.mainloop(surface)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return self.mode, self.elo

    def load_images(self):
        self.exit_icon_surface = pygame.image.load('images/menu/logout.png')
        self.exit_icon_surface = pygame.transform.scale(self.exit_icon_surface, (40, 40))
        self.ai_icon = pygame.image.load('images/menu/ai.png')
        self.ai_icon = pygame.transform.scale(self.ai_icon, (40, 40))
        self.people_icon = pygame.image.load('images/menu/people.png')
        self.people_icon = pygame.transform.scale(self.people_icon, (40, 40))
        self.joystick_icon = pygame.image.load('images/menu/joystick.png')
        self.joystick_icon = pygame.transform.scale(self.joystick_icon, (40, 40))