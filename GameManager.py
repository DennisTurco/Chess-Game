import logging
import pygame
from Enums.Mode import Mode
from Menus.MainMenu import MainMenu
from Game import Game

APP_NAME = "Chess Game"
SIDEBAR_WIDTH = 220
WIDTH = 512
HEIGHT = 512
WINDOW_WIDTH = WIDTH + SIDEBAR_WIDTH
DIMENSION = 8   # dimension for chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION   # square size

class GameManager():
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
        pygame.display.set_caption(APP_NAME)

    def run(self) -> None:
        running = True
        while running:
            menu = MainMenu()
            mode, elo, color_side = menu.mainloop(self.surface)

            if mode is None:
                running = False
                continue

            if mode == Mode.PVP:
                self.logger.info("Running game in Player vs Player mode")
                Game()
            elif mode == Mode.PVE:
                self.logger.info("Running game in Player vs AI mode")
                Game(color_side, elo)
            else:
                raise Exception("Mode selected is not valid")

        pygame.quit()
