import pygame_menu
from pygame_menu import themes

import GameManager

class Menu:
    def __init__(self):
        self.custom_theme = themes.THEME_SOLARIZED.copy()
        self.custom_theme.title_font = pygame_menu.font.FONT_MUNRO
        self.custom_theme.widget_font = pygame_menu.font.FONT_MUNRO
        self.custom_theme.title_font_size = 60
        self.custom_theme.widget_font_size = 35
        self.WIDTH = GameManager.WINDOW_WIDTH
        self.HEIGHT = GameManager.HEIGHT