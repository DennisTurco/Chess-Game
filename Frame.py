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
        except:
            logging.error(sys.argv[0] + " -> error on loading image '" + image + "'")
    

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
    possiblePositions = move.getPossiblePositions()                
    
    
    loadImages()
    running = True
    
    while running:
        for event in pygame.event.get():
            
            # check for Quit
            if event.type == pygame.QUIT:
                running = False
            
            # handle MOUSEBUTTONUP
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                posxy = [pos[0] // SQ_SIZE, pos[1] // SQ_SIZE]  # i want to se the board like a matrix
            
                # check if is a piece
                if board.board[posxy[0]][posxy[1]] != '--':
                    
                    if playerClicks[0] == [] or (move.isPlayerWhiteTurn() and move.isWhitePiece(posxy[0], posxy[1])) or (not move.isPlayerWhiteTurn() and not move.isWhitePiece(posxy[0], posxy[1])):
                        playerClicks[0] = posxy
                        move.checkPossibleMovements(posxy)
                        possiblePositions = move.getPossiblePositions()                
                    
                    elif playerClicks[0] == posxy:
                        playerClicks[0] = []
                    
                    # check if the second position is a piece
                    elif playerClicks[0] != []:
                        playerClicks[1] = posxy
                        move.captureRequest(playerClicks)
                        playerClicks = [[], []]

                # check if first position is selected and the second not
                elif playerClicks[0] != [] and playerClicks[1] == []:   
                    playerClicks[1] = posxy
                    move.moveRequest(playerClicks)
                    print(playerClicks)
                    playerClicks = [[], []]
                    move.initPossiblePositions()               

            # draw
            drawGameState(screen, board.board, possiblePositions)
            pygame.display.flip()


def drawGameState(screen, board, possiblePositins):
    # draw squares on the board
    drawBoard(screen)   
    
    # draw pieces on the board
    drawPieces(screen, board)
    
    # draw Highlight
    drawHighlight(screen, possiblePositins)  
    

def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if ((i + j) % 2) == 0:
                color = colors[0]
            else:
                color = colors[1] 
            pygame.draw.rect(screen, color, pygame.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawHighlight(screen, possiblePositins):
    image_dot = "images/black_dot.png"
    image_dot = pygame.transform.scale(pygame.image.load(image_dot), (SQ_SIZE, SQ_SIZE))
    
    image_circle = "images/black_circle.png"
    image_circle = pygame.transform.scale(pygame.image.load(image_circle), (SQ_SIZE, SQ_SIZE))
    
    for i in range(DIMENSION):
        for j in range(DIMENSION): 
            if possiblePositins[i][j] == 1:      
                screen.blit(image_dot, pygame.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif possiblePositins[i][j] == 2:
                screen.blit(image_circle, pygame.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                try:
                    screen.blit(IMAGES[piece], pygame.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
                except:
                    logging.error(sys.argv[0] + " -> cannot load piece '" + piece + "' into the board")

if __name__ == "__main__":
    main()