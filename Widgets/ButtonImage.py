import pygame
import logging

import pygame
import logging

class ButtonImage:
    def __init__(self, screen, x: int, y: int, image: pygame.Surface, scale: float = 1, initial_opacity: int = 255, over_opacity: int = 255) -> None:
        self.screen = screen
        self.original_image = image.convert_alpha()
        width = self.original_image.get_width()
        height = self.original_image.get_height()
        self.scaled_size = (int(width * scale), int(height * scale))

        self.image = pygame.transform.smoothscale(self.original_image, self.scaled_size)
        self.initial_opacity = initial_opacity
        self.over_opacity = over_opacity
        self.opacity = initial_opacity
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hovered = False
        self.logger = logging.getLogger(self.__class__.__name__)
        self.draw()  # draw initially

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            self.logger.info("Button image clicked")
            return True
        return False

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        hovered_now = self.rect.collidepoint(mouse_pos)

        if hovered_now != self.hovered:
            self.hovered = hovered_now
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if self.hovered else pygame.SYSTEM_CURSOR_ARROW)
            self.opacity = self.over_opacity if self.hovered else self.initial_opacity
            self.draw()

    def draw(self):
        temp_image = pygame.transform.smoothscale(self.original_image, self.scaled_size).copy()
        temp_image.set_alpha(self.opacity)
        self.image = temp_image
        self.screen.blit(self.image, self.rect.topleft)
