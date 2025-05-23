import pygame_menu
from pygame_menu import themes
import GameManager

class MessageBox:
    def __init__(self):
        self.__whiteWin = "White has won the game!"
        self.__blackWin = "Black has won the game!"
        self.__question = "Would you like to restart the game?"
        self.__titleMessage = "Game Over"

    def ask_restart(self, isWhite, screen):
        import pygame
        if not pygame.get_init():
            pygame.init()

        message = f"{(self.__whiteWin if isWhite else self.__blackWin)}\n{self.__question}"

        restart = None

        def on_yes():
            nonlocal restart
            restart = True
            menu.disable()

        def on_no():
            nonlocal restart
            restart = False
            menu.disable()

        menu = pygame_menu.Menu(self.__titleMessage, GameManager.WINDOW_WIDTH, GameManager.HEIGHT, theme=themes.THEME_SOLARIZED)
        menu.add.label(message, max_char=-1, font_size=20)
        menu.add.button('Yes', on_yes)
        menu.add.button('No', on_no)

        clock = pygame.time.Clock()

        while menu.is_enabled():
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return None
            menu.update(events)
            screen.fill((0, 0, 0))

            if menu.is_enabled():
                menu.draw(screen)
                pygame.display.flip()

            clock.tick(60)

        return restart
