import pygame
import logging

class ButtonImage():
    def __init__(self, screen, x: int, y: int, image: pygame.Surface, scale: float) -> None:
        self.screen = screen
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.logger = logging.getLogger(self.__class__.__name__)
        self.__draw()


    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.logger.info("Resetting the game")
            return True
        return False


    # draw button on screen
    def __draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def __get_mouse_position(self):
        pos = pygame.mouse.get_pos()
        return pos