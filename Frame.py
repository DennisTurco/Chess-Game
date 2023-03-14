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
            logging.info("image '" + image + "' loaded")
        except:
            logging.error( sys.argv[0] + " -> error on loading image '" + image + "'")
    

def main():
    pygame.init()    # initialize pygame
    
    pygame.display.set_caption('Chess')
    programIcon = pygame.image.load('images/wK.png')
    pygame.display.set_icon(programIcon)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color('white'))
        
    board = Board.GameState()
    loadImages()
    running = True
    
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        drawGameState(screen, board.board)
        pygame.display.flip()

def drawGameState(screen, board):
    drawBoard(screen) # draw squares on the board
    drawPieces(screen, board)

def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if ((i + j) % 2) == 0:
                color = colors[0]
            else:
                color = colors[1] 
            pygame.draw.rect(screen, color, pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    
def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                try:
                    screen.blit(IMAGES[piece], pygame.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
                    logging.info("piece '" + piece + "' loaded into the board")
                except:
                    logging.error( sys.argv[0] + " -> cannot load piece '" + piece + "' into the board")

if __name__ == "__main__":
    main()