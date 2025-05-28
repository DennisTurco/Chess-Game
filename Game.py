import pygame
import logging
import sys
import pygame_menu.font as font_module

from Board import Board
from Move import Move
from Widgets.ButtonImage import ButtonImage
from Entities.Pos import Pos
from Entities.PosMove import PosMove
from Enums.Piece import PieceName

import GameManager

class Game:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.IMAGES = {}

        font_path = font_module.FONT_MUNRO
        self.normal_text = pygame.font.Font(font_path, 20)
        self.bold_text = pygame.font.SysFont(font_path, 35, bold=True)

        self.game()


    def game(self) -> None:
        screen = self.init_and_get_window()

        playerClicks = PosMove()
        board = Board()
        move = Move(playerClicks, board, screen)
        move_history = []
        possiblePositions = move.reset_posssible_positions()

        self.loadImages()
        running = True
        self.buttons = self.draw_buttons(screen)

        while running:
            screen.fill(pygame.Color('white'))

            self.refresh(screen, board, possiblePositions, move_history)
            self.buttons = self.draw_buttons(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    if self.buttons["reset"].is_clicked(pos):
                        (board, move, move_history, playerClicks, possiblePositions) = self.restart_game(screen, move_history)
                        continue

                    if self.buttons["menu"].is_clicked(pos):
                        running = False
                        return

                    if pos[0] < GameManager.SIDEBAR_WIDTH:
                        continue

                    board_x = (pos[0] - GameManager.SIDEBAR_WIDTH) // GameManager.SQ_SIZE
                    board_y = pos[1] // GameManager.SQ_SIZE
                    posxy: Pos = Pos(board_x, board_y)

                    # check if is a piece
                    if board.board[posxy.x][posxy.y] != PieceName.EMPTY:

                        if playerClicks.initial_position is None or (move.isPlayerWhiteTurn() and move.isWhitePiece(posxy.x, posxy.y)) or (not move.isPlayerWhiteTurn() and not move.isWhitePiece(posxy.x, posxy.y)):
                            playerClicks.initial_position = posxy
                            move.setPossibleMovements(posxy)
                            possiblePositions = move.getPossiblePositions()

                        elif playerClicks.initial_position == posxy:
                            playerClicks.initial_position = None

                        # check if the second position is a piece
                        elif playerClicks.initial_position is not None:
                            playerClicks.final_position = posxy
                            if move.captureRequest(playerClicks):
                                move_notation = f"{chr(65 + playerClicks.initial_position.x)}{8 - playerClicks.initial_position.y} -> {chr(65 + playerClicks.final_position.x)}{8 - playerClicks.final_position.y}"
                                move_history.append(move_notation)
                                self.logger.info(f"Moving piece from {playerClicks.initial_position} to {playerClicks.final_position}")
                            # reset possiblePositions
                            playerClicks = PosMove()
                            possiblePositions = move.reset_posssible_positions()

                    # check if first position is selected and the second not
                    elif playerClicks.initial_position is not None and playerClicks.final_position is None:
                        playerClicks.final_position = posxy
                        if move.moveRequest(playerClicks):
                            move_notation = f"{chr(65 + playerClicks.initial_position.x)}{8 - playerClicks.initial_position.y} -> {chr(65 + playerClicks.final_position.x)}{8 - playerClicks.final_position.y}"
                            move_history.append(move_notation)
                            self.logger.info(f"Moving piece from {playerClicks.initial_position} to {playerClicks.final_position}")
                        # reset possiblePositions
                        playerClicks = PosMove()
                        possiblePositions = move.reset_posssible_positions()

                if move.restart():
                    (board, move, move_history, playerClicks, possiblePositions) = self.restart_game(screen, move_history)
                    continue
                elif move.isFinished():
                    running = False
                    return

                self.refresh(screen, board, possiblePositions, move_history)


    def restart_game(self, screen: pygame.Surface, move_history: list):
        board = Board()
        move = Move(PosMove(), board, screen)
        move_history.clear()
        playerClicks = PosMove()
        possiblePositions = move.reset_posssible_positions()
        return (board, move, move_history, playerClicks, possiblePositions)

    def loadImages(self):
        pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']

        for piece in pieces:
            image = f"images/{piece}.png"
            try:
                self.IMAGES[piece] = pygame.transform.scale(pygame.image.load(image), (GameManager.SQ_SIZE, GameManager.SQ_SIZE))
            except:
                self.logger.error(f"{sys.argv[0]} -> error on loading image")


    def init_and_get_window(self) -> pygame.Surface:
        pygame.init()    # initialize pygame
        pygame.display.set_caption(GameManager.APP_NAME)
        programIcon = pygame.image.load('images/wK.png')
        pygame.display.set_icon(programIcon)
        screen = pygame.display.set_mode((GameManager.WINDOW_WIDTH, GameManager.HEIGHT))
        screen.fill(pygame.Color('white'))
        return screen


    def refresh(self, screen: pygame.Surface, board: Board, possiblePositions: list[list[int]], move_history: list) -> None:
        self.drawGameState(screen, board, possiblePositions, move_history)
        pygame.display.flip()


    def drawGameState(self, screen: pygame.Surface, board: Board, possiblePositions: list[list[int]], move_history: list) -> None:
        self.drawSidebar(screen, move_history)
        self.drawBoard(screen)
        self.drawHighlight(screen, possiblePositions)
        self.drawPieces(screen, board)


    def drawBoard(self, screen: pygame.Surface) -> None:
        colors = [pygame.Color('white'), pygame.Color('gray')]

        for i in range(GameManager.DIMENSION):
            for j in range(GameManager.DIMENSION):
                x = i * GameManager.SQ_SIZE + GameManager.SIDEBAR_WIDTH
                y = j * GameManager.SQ_SIZE
                color = colors[(i + j) % 2]
                pygame.draw.rect(screen, color, pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))

                # numbers to the left
                if i == 0:
                    text = self.normal_text.render(str(8 - j), False, pygame.Color('black'))
                    screen.blit(text, (GameManager.SIDEBAR_WIDTH - 18, y + 4))

                # letters down
                if j == 7:
                    text = self.normal_text.render(chr(65 + i), False, pygame.Color('black'))
                    screen.blit(text, (x + GameManager.SQ_SIZE // 2 - 6, GameManager.HEIGHT - 20))


    def draw_buttons(self, screen: pygame.Surface) -> dict[str, ButtonImage]:
        if not hasattr(self, "buttons"):
            image_restart = pygame.image.load("images/reset.png").convert_alpha()
            image_menu = pygame.image.load("images/reset.png").convert_alpha()
            reset_button = ButtonImage(screen, 10, 400, image_restart, 0.08, 180, 255)
            menu_button = ButtonImage(screen, 10, 450, image_menu, 0.08, 180, 255)
            self.buttons = {"reset": reset_button, "menu": menu_button}

        self.buttons["reset"].update()
        self.buttons["reset"].draw()
        self.buttons["menu"].update()
        self.buttons["menu"].draw()

        return self.buttons


    def drawSidebar(self, screen: pygame.Surface, move_history: list) -> None:
        pygame.draw.rect(screen, pygame.Color("lightgray"), pygame.Rect(0, 0, GameManager.SIDEBAR_WIDTH, GameManager.HEIGHT))

        # app name
        title = self.bold_text.render(GameManager.APP_NAME, False, pygame.Color("black"))
        screen.blit(title, (10, 10))

        # history moves
        label = self.normal_text.render("Moves:", False, pygame.Color("black"))
        screen.blit(label, (10, 40))

        y_offset = 70
        for i, move in enumerate(move_history[-15:]):  # show only the last 15 moves
            text = self.normal_text.render(move, False, pygame.Color("black"))
            screen.blit(text, (10, y_offset + i * 18))

        if "reset" in self.buttons:
            self.buttons["reset"].update()
            self.buttons["reset"].draw()
        if "menu" in self.buttons:
            self.buttons["menu"].update()
            self.buttons["menu"].draw()


    def drawHighlight(self, screen: pygame.Surface, possiblePositions: list[list[int]]) -> None:
        if possiblePositions == [[],[]]: return
        image_dot = pygame.transform.scale(pygame.image.load("images/black_dot.png"), (GameManager.SQ_SIZE, GameManager.SQ_SIZE))
        image_circle = pygame.transform.scale(pygame.image.load("images/black_circle.png"), (GameManager.SQ_SIZE, GameManager.SQ_SIZE))

        for i in range(GameManager.DIMENSION):
            for j in range(GameManager.DIMENSION):
                x = i * GameManager.SQ_SIZE + GameManager.SIDEBAR_WIDTH
                y = j * GameManager.SQ_SIZE

                if possiblePositions[i][j] == 1:
                    screen.blit(image_dot, pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))
                elif possiblePositions[i][j] == 2:
                    screen.blit(image_circle, pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))


    def drawPieces(self, screen: pygame.Surface, board: Board) -> None:
        for i in range(GameManager.DIMENSION):
            for j in range(GameManager.DIMENSION):
                if board.board[i][j] != PieceName.EMPTY:
                    piece = str(board.board[i][j])
                    try:
                        x = i * GameManager.SQ_SIZE + GameManager.SIDEBAR_WIDTH
                        y = j * GameManager.SQ_SIZE
                        screen.blit(self.IMAGES[piece], pygame.Rect(x, y, GameManager.SQ_SIZE, GameManager.SQ_SIZE))
                    except:
                        self.logger.error(f"{sys.argv[0]} -> cannot load piece '{piece}' into the board")