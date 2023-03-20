import pygame
import logging
import sys

import Board

WIDTH = 512
HEIGHT = 512    
DIMENSION = 8   # dimension for chess board is 8x8
SQ_SIZE = HEIGHT // DIMENSION   # square size
MAX_FPS = 15    # for animations
IMAGES = {}

def loadImages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']

    for piece in pieces:
        try:
            image = "images/" + piece + ".png"
            IMAGES[piece] = pygame.transform.scale(pygame.image.load(image), (SQ_SIZE, SQ_SIZE))
            logging.info("image '{}' loaded", format(image))
        except:
            logging.error("{} -> error on loading image '{}'", format(sys.argv[0], image))
    

def main():
    pygame.init()    # initialize pygame
    
    pygame.display.set_caption('Chess')
    programIcon = pygame.image.load('images/wK.png')
    pygame.display.set_icon(programIcon)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color('white'))
    
    playerClicks = [[], []]
      
    board = Board.Board()
    move = Board.Move(playerClicks, board.board)
    
    loadImages()
    running = True
    
    while running == True:
        for event in pygame.event.get():
            
            # check for Quit
            if event.type == pygame.QUIT:
                running = False
            
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                posxy = [pos[0] // SQ_SIZE, pos[1] // SQ_SIZE]  # i want to se the board like a matrix
                logging.info("position selected: {}",  format(posxy))
            
                # check if is a piece
                if board.board[posxy[0]][posxy[1]] != '--':
                    print('piece selected -> {}', format(board.board[posxy[0]][posxy[1]]))
                    logging.info("piece selected: {}", format(board.board[posxy[0]][posxy[1]]))   
                    
                    if playerClicks[0] == []:
                        playerClicks[0] = posxy
                    
                    elif playerClicks[0] == posxy:
                        playerClicks[0] = []

                # check if first position is selected
                elif playerClicks[0] != []:
                    if playerClicks[1] == []:
                        playerClicks[1] = posxy
                        move.moveRequest(playerClicks)
                        playerClicks = [[], []]
                        
                print(playerClicks)

            # draw
            drawGameState(screen, board.board)
            pygame.display.flip()


def drawGameState(screen, board):
    # draw squares on the board
    drawBoard(screen) 
    # draw pieces on the board
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if ((i + j) % 2) == 0:
                color = colors[0]
            else:
                color = colors[1] 
            pygame.draw.rect(screen, color, pygame.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                try:
                    screen.blit(IMAGES[piece], pygame.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
                    logging.info("piece '{}' loaded into the board", format(piece))
                except:
                    logging.error("{} -> cannot load piece '{}' into the board", format(sys.argv[0], piece))

if __name__ == "__main__":
    main()