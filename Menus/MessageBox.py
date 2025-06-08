import logging
from typing import Optional
import pygame
import pygame_menu
from Menus.Menu import Menu

class MessageBox(Menu):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Opening game over message")
        super().__init__()
        self._whiteWin = "White has won the game!"
        self._blackWin = "Black has won the game!"
        self._stalmate = "The match finished in stalmate"
        self._question = "Would you like to restart the game?"
        self._titleMessage = "Game Over"

    def ask_restart(self, is_white: Optional[bool], screen: pygame.Surface) -> bool | None:
        if not pygame.get_init():
            pygame.init()

        if is_white is None:
            message = f"{self._stalmate}\n{self._question}"
        else:
            message = f"{(self._whiteWin if is_white else self._blackWin)}\n{self._question}"

        restart = None

        def on_yes():
            nonlocal restart
            restart = True
            menu.disable()

        def on_no():
            nonlocal restart
            restart = False
            menu.disable()

        menu = pygame_menu.Menu(
            title=self._titleMessage,
            width=self.WIDTH,
            height=self.HEIGHT,
            theme=self.custom_theme
        )
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

        self.logger.info(f"Restart setted to {restart}")
        return restart
