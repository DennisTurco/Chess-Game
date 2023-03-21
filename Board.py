# SELF represents the instance of class. This handy keyword allows you to access variables, attributes, and methods of a defined class in Python.
# the Python equivalent of the C++ constructor in an object-oriented approach.

import logging
import sys
from playsound import playsound

class Board():

    def __init__(self):
        self.board = [
            ["bR", "bp", "--", "--", "--", "--", "wp", "wR"],
            ["bN", "bp", "--", "--", "--", "--", "wp", "wN"],
            ["bB", "bp", "--", "--", "--", "--", "wp", "wB"],
            ["bQ", "bp", "--", "--", "--", "--", "wp", "wQ"],
            ["bK", "bp", "--", "--", "--", "--", "wp", "wK"],
            ["bB", "bp", "--", "--", "--", "--", "wp", "wB"],
            ["bN", "bp", "--", "--", "--", "--", "wp", "wN"],
            ["bR", "bp", "--", "--", "--", "--", "wp", "wR"],]

# -----------------------------------------------------------------

class Move():

    def __init__(self, playerClicks, board):
        self.pos_start = playerClicks[0]
        self.pos_final = playerClicks[1]
        self.board = board
        self.whiteMove = True
        self.finished = False

    def modifyPosition(self):
        piece_name = self.getPieceName()
        
        # check if it is a simple move or someone is capturing a piece to play the correct sound
        if self.board[self.pos_final[0]][self.pos_final[1]] == '--':
            sound = "sounds/move.mp3"
            #try: playsound(sound)
            #except: logging.error(sys.argv[0] + " -> error on loading sound '" + sound + "'")
        else:
            sound = "sounds/capture.mp3"
            #try: playsound(sound)
            #except: logging.error(sys.argv[0] + " -> error on loading sound '" + sound + "'")
            
            
        self.board[self.pos_final[0]][self.pos_final[1]] = piece_name
        self.board[self.pos_start[0]][self.pos_start[1]] = '--'
        
        if self.whiteMove == True: 
            self.whiteMove = False
        else:
            self.whiteMove = True
        
    
    def captureRequest(self, playerClicks):
        if self.finished: return
        
        # set pos_start and pos_final
        self.setPlayerClicks(playerClicks)
        
        self.modifyPosition()   
        

    def moveRequest(self, playerClicks):
        if self.finished: return
        
        # set pos_start and pos_final
        self.setPlayerClicks(playerClicks)
        
        piece_name = self.getPieceName()
        
        # errors check
        if piece_name[0] == "w" and self.whiteMove == False:
            logging.error(sys.argv[0] + " -> 'piece_name[0] == \"w\" and self.whiteMove == False' ")
            return
        elif piece_name[0] == "b" and self.whiteMove == True:
            logging.error(sys.argv[0] + " -> 'piece_name[0] == \"b\" and self.whiteMove == True' ")
            return
        
        # pawns
        if piece_name[1] == 'p':
            self.pawnMove()
        
        # rocks
        elif piece_name[1] == 'R':
            self.rockMove()
        
        # bishops
        elif piece_name[1] == 'B':
            self.rockMove()
        
        # knights
        elif piece_name[1] == 'K':
            self.rockMove()
            
        # queen
        elif piece_name[1] == 'Q':
            self.rockMove()
            
        # king
        elif piece_name[1] == 'K':
            self.rockMove()
            
        else:
            logging.error(sys.argv[0] + " -> piece: '" + piece_name + "' doesn't exist")
            return
            
    def pawnMove(self):
        # white turn
        if self.whiteMove:            
            if (self.pos_start[1] == self.pos_final[1]+1 and self.pos_start[0] == self.pos_final[0]) or (self.pos_start[1] == self.pos_final[1]+2 and self.pos_start[0] == self.pos_final[0] and self.pos_final[1] == 4):
                self.modifyPosition()
            else: return
        # black turn
        else:
            if (self.pos_start[1] == self.pos_final[1]-1 and self.pos_start[0] == self.pos_final[0]) or (self.pos_start[1] == self.pos_final[1]-2 and self.pos_start[0] == self.pos_final[0] and self.pos_final[1] == 3):
                self.modifyPosition()
            else: return
    
    def rockMove(self):
        # check if final position is correct for rock
        if (self.pos_final[0] == self.pos_final[0]) or (self.pos_final[1] == self.pos_final[1]):
            
            i = j = 1
            
            # check if there is a piece in the middle
            if self.pos_start[1] > self.pos_final[1]:           # the movement is from top to down
                while self.pos_start[1]-i != self.pos_final[1]:
                    if self.board[self.pos_start[0]][self.pos_start[1]-i] != '--': 
                        return
                    i = i + 1
            elif self.pos_start[1] < self.pos_final[1]:         # the movement is from down to top
                while self.pos_start[1]+i != self.pos_final[1]:
                    if self.board[self.pos_start[0]][self.pos_start[1]+i] != '--': 
                        return
                    i = i + 1
            if self.pos_start[0] > self.pos_final[0]:           # the movement is from right to left
                while self.pos_start[0]-j != self.pos_final[0]:
                    if self.board[self.pos_start[0]-j][self.pos_start[1]] != '--': 
                        return
                    j = j + 1
            elif self.pos_start[0] < self.pos_final[0]:         # the movement is from right to left
                while self.pos_start[0]+j != self.pos_final[0]:
                    if self.board[self.pos_start[0]+j][self.pos_start[1]] != '--': 
                        return
                    j = j + 1
            
            # let the movement
            self.modifyPosition()
        
        else: return
     
    def getPieceName(self):
        return self.board[self.pos_start[0]][self.pos_start[1]]
    
    def setPlayerClicks(self, playerClicks):
        self.pos_start = playerClicks[0]
        self.pos_final = playerClicks[1]