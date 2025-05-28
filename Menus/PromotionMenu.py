import logging
import pygame
import pygame_menu
from Enums.Piece import PieceType
from Menus.Menu import Menu

class PromotionMenu(Menu):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Opening promotion menu")
        super().__init__()
        self.selection = None

        self.menu = pygame_menu.Menu(
            title='Choose Promotion',
            width=self.WIDTH,
            height=self.HEIGHT,
            theme=self.custom_theme
        )

        self.menu.add.label("Promote to:")
        self.menu.add.button(PieceType.QUEEN.name, lambda: self.set_choice(PieceType.QUEEN.value))
        self.menu.add.button(PieceType.ROOK.name, lambda: self.set_choice(PieceType.ROOK.value))
        self.menu.add.button(PieceType.BISHOP.name, lambda: self.set_choice(PieceType.BISHOP.value))
        self.menu.add.button(PieceType.KNIGHT.name, lambda: self.set_choice(PieceType.KNIGHT.value))

        self.surface = None

    def set_choice(self, piece: str) -> None:
        self.selection = piece
        self.menu.disable()

    def show(self, surface: pygame.Surface) -> str:
        self.selection = None
        self.surface = surface
        self.menu.mainloop(surface)
        self.logger.info(f"Promotion to {self.selection}")
        return str(self.selection)