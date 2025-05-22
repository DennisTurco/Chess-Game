import pygame
import logging
import sys

from Board import Board
from Move import Move
from Widgets.ButtonImage import ButtonImage
from Entities.Pos import Pos
from Entities.PosMove import PosMove
from Enums.Piece import Piece

SIDEBAR_WIDTH = 220
WIDTH = 512
HEIGHT = 512
WINDOW_WIDTH = WIDTH + SIDEBAR_WIDTH
DIMENSION = 8   # dimension for chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION   # square size
IMAGES = {}

def loadImages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']

    for piece in pieces:
        image = "images/" + piece + ".png"
        try:
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(image), (SQ_SIZE, SQ_SIZE))
        except:
            logging.error(f"{sys.argv[0]} -> error on loading image")

def main():
    pygame.init()    # initialize pygame

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
    )

    pygame.display.set_caption('Chess')
    programIcon = pygame.image.load('images/wK.png')
    pygame.display.set_icon(programIcon)
    screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
    screen.fill(pygame.Color('white'))

    playerClicks: PosMove = PosMove()

    board = Board()
    move = Move(playerClicks, board.board)
    move_history = []
    possiblePositions = move.getPossiblePositions()

    loadImages()
    running = True

    while running:
        buttons = drawGameState(screen, board.board, possiblePositions, move_history)

        for event in pygame.event.get():
            # check for Quit
            if event.type == pygame.QUIT:
                running = False

            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if buttons["reset"].is_clicked(pos):
                    board = Board()
                    move = Move(PosMove(), board.board)
                    move_history.clear()
                    playerClicks = PosMove()
                    possiblePositions = move.reset_posssible_positions()
                    refresh(screen, board, possiblePositions, move_history)
                    continue

                # Se il click è nella sidebar, ignoralo
                if pos[0] < SIDEBAR_WIDTH:
                    continue

                board_x = (pos[0] - SIDEBAR_WIDTH) // SQ_SIZE
                board_y = pos[1] // SQ_SIZE
                posxy: Pos = Pos(board_x, board_y)

                logging.debug(f"position clicked = {posxy}")

                # check if is a piece
                if board.board[posxy.x][posxy.y] != Piece.EMPTY:

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
                            logging.info(f"Moving piece from {playerClicks.initial_position} to {playerClicks.final_position}")
                        # reset possiblePositions
                        playerClicks = PosMove()
                        possiblePositions = move.reset_posssible_positions()

                # check if first position is selected and the second not
                elif playerClicks.initial_position is not None and playerClicks.final_position is None:
                    playerClicks.final_position = posxy
                    if move.moveRequest(playerClicks):
                        move_notation = f"{chr(65 + playerClicks.initial_position.x)}{8 - playerClicks.initial_position.y} -> {chr(65 + playerClicks.final_position.x)}{8 - playerClicks.final_position.y}"
                        move_history.append(move_notation)
                        logging.info(f"Moving piece from {playerClicks.initial_position} to {playerClicks.final_position}")
                    # reset possiblePositions
                    playerClicks = PosMove()
                    possiblePositions = move.reset_posssible_positions()

            refresh(screen, board, possiblePositions, move_history)

def refresh(screen, board, possiblePositions, move_history):
    drawGameState(screen, board.board, possiblePositions, move_history)
    pygame.display.flip()

def drawGameState(screen, board, possiblePositions, move_history):
    drawSidebar(screen, move_history)
    buttons = draw_buttons(screen)
    drawBoard(screen)
    drawHighlight(screen, possiblePositions)
    drawPieces(screen, board)
    return buttons

def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    font = pygame.font.SysFont("Arial", 16)

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            x = i * SQ_SIZE + SIDEBAR_WIDTH
            y = j * SQ_SIZE
            color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))

            # Numeri a sinistra (1–8)
            if i == 0:
                text = font.render(str(8 - j), True, pygame.Color('black'))
                screen.blit(text, (SIDEBAR_WIDTH - 18, y + 4))

            # Lettere sotto (A–H)
            if j == 7:
                text = font.render(chr(65 + i), True, pygame.Color('black'))
                screen.blit(text, (x + SQ_SIZE // 2 - 6, HEIGHT - 20))


def draw_buttons(screen):
    image_restart = pygame.image.load("images/reset.png").convert_alpha()
    reset_button = ButtonImage(screen, 10, 50, image_restart, 0.08)
    return {"reset": reset_button}


def drawSidebar(screen, move_history):
    pygame.draw.rect(screen, pygame.Color("lightgray"), pygame.Rect(0, 0, SIDEBAR_WIDTH, HEIGHT))

    font = pygame.font.SysFont("Arial", 20, bold=True)
    small_font = pygame.font.SysFont("Arial", 16)

    # app name
    title = font.render("Chess App", True, pygame.Color("black"))
    screen.blit(title, (10, 10))

    # history moves
    label = small_font.render("Moves:", True, pygame.Color("black"))
    screen.blit(label, (10, 100))

    y_offset = 130
    for i, move in enumerate(move_history[-20:]):  # Mostra solo le ultime 20 mosse
        text = small_font.render(move, True, pygame.Color("black"))
        screen.blit(text, (10, y_offset + i * 18))


def drawHighlight(screen, possiblePositions):
    if possiblePositions == [[],[]]: return
    image_dot = pygame.transform.scale(pygame.image.load("images/black_dot.png"), (SQ_SIZE, SQ_SIZE))
    image_circle = pygame.transform.scale(pygame.image.load("images/black_circle.png"), (SQ_SIZE, SQ_SIZE))

    for i in range(DIMENSION):
        for j in range(DIMENSION):
            x = i * SQ_SIZE + SIDEBAR_WIDTH
            y = j * SQ_SIZE

            if possiblePositions[i][j] == 1:
                screen.blit(image_dot, pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))
            elif possiblePositions[i][j] == 2:
                screen.blit(image_circle, pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if board[i][j] != Piece.EMPTY:
                piece = str(board[i][j])
                try:
                    x = i * SQ_SIZE + SIDEBAR_WIDTH
                    y = j * SQ_SIZE
                    screen.blit(IMAGES[piece], pygame.Rect(x, y, SQ_SIZE, SQ_SIZE))
                except:
                    logging.error(f"{sys.argv[0]} -> cannot load piece '{piece}' into the board")

if __name__ == "__main__":
    try: main()
    except: logging.exception(f"{sys.argv[0]}")