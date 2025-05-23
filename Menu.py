import pygame
import pygame_menu
from pygame_menu import themes, events

class Menu:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((600, 400))
        pygame.display.set_caption("Chess Game")

        self.mode = None
        self.elo = 1200

        self.main_menu = pygame_menu.Menu('Welcome on Chess Game', 600, 400, theme=themes.THEME_SOLARIZED)
        self.mode_menu = pygame_menu.Menu('Modes', 600, 400, theme=themes.THEME_SOLARIZED)

        self.mode_menu.add.button('Player vs Player', lambda: self.start_game(mode="pvp"))
        self.mode_menu.add.button('Player vs AI', action=self.elo_menu)
        self.mode_menu.add.button('Back', events.BACK)

        self.elo_select_menu = pygame_menu.Menu('Select AI Difficulty (ELO)', 600, 400, theme=themes.THEME_SOLARIZED)
        self.elo_select_menu.add.selector('ELO level:', [
            ('400', 400), ('600', 600), ('800', 800), ('1000', 1000), ('1200', 1200), ('1500', 1500),
            ('1800', 1800), ('2000', 2000), ('2200', 2200), ('2500', 2500),
            ('2800', 2800), ('3000', 3000)
            ], onchange=self.set_elo)
        self.elo_select_menu.add.button('Start AI Game', lambda: self.start_game(mode="ai"))
        self.elo_select_menu.add.button('Back', events.BACK)

        self.main_menu.add.button('Play / Modes', self.mode_menu)
        self.main_menu.add.button('Quit', events.EXIT)

    def set_elo(self, selected, value):
        self.elo = value
        print(f"ELO selected: {self.elo}")

    def elo_menu(self):
        # Passa al menu di selezione ELO
        self.elo_select_menu.mainloop(self.surface)

    def start_game(self, mode):
        self.mode = mode
        print(f"Avvio gioco in modalità: {mode}")
        if mode == "ai":
            print(f"Livello AI (ELO): {self.elo}")

    def run(self):
        self.main_menu.mainloop(self.surface)

    def load_images(self):
        self.exit_icon_surface = pygame.image.load('images/menu/logout.png')
        self.exit_icon_surface = pygame.transform.scale(self.exit_icon_surface, (40, 40))
        self.ai_icon = pygame.image.load('images/menu/ai.png')
        self.ai_icon = pygame.transform.scale(self.ai_icon, (40, 40))
        self.people_icon = pygame.image.load('images/menu/people.png')
        self.people_icon = pygame.transform.scale(self.people_icon, (40, 40))
        self.joystick_icon = pygame.image.load('images/menu/joystick.png')
        self.joystick_icon = pygame.transform.scale(self.joystick_icon, (40, 40))