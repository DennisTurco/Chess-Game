# SELF represents the instance of class. This handy keyword allows you to access variables, attributes, and methods of a defined class in Python.
# the Python equivalent of the C++ constructor in an object-oriented approach.

import logging
import sys
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio


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
        
        try:
            self.sound_move = simpleaudio.WaveObject.from_wave_file("sounds/move.wav")
            self.sound_capture = simpleaudio.WaveObject.from_wave_file("sounds/capture.wav")
        except:
            logging.error(sys.argv[0] + " -> error on loading sounds")

    def modifyPosition(self):
        piece_name = self.getPieceName()
        
        # check if it is a simple move or someone is capturing a piece to play the correct sound
        if self.board[self.pos_final[0]][self.pos_final[1]] == '--':
            try: self.sound_move.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
        else:
            try: self.sound_capture.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
            
            
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
        
        # the white piace cannot eat another white piece (same for black)
        piece_name = self.board[self.pos_final[0]][self.pos_final[1]]
        if  (self.whiteMove == True and piece_name[0] == 'w') or (self.whiteMove == False and piece_name[0] == 'b'):
            return
        else:
            self.moveRequest(playerClicks)   
        

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
            self.bishopMove()
        
        # knights
        elif piece_name[1] == 'N':
            self.knightMove()
            
        # queen
        elif piece_name[1] == 'Q':
            self.queenMove()
            
        # king
        elif piece_name[1] == 'K':
            self.kingMove()
            
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
        if (self.pos_start[0] == self.pos_final[0]) or (self.pos_start[1] == self.pos_final[1]):
            
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
            elif self.pos_start[0] > self.pos_final[0]:           # the movement is from right to left
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
        
    def bishopMove(self):                
        # check if final position is correct for the king    
        pos_diff = [0, 0]
        
        # find x diff
        if self.pos_start[0] <= self.pos_final[0]:
            pos_diff[0] =  self.pos_final[0] - self.pos_start[0]
        elif self.pos_start[0] > self.pos_final[0]:
            pos_diff[0] =  self.pos_start[0] - self.pos_final[0]
        
        # find the y diff
        if self.pos_start[1] <= self.pos_final[1]:
            pos_diff[1] =  self.pos_final[1] - self.pos_start[1]
        elif self.pos_start[1] > self.pos_final[1]:
            pos_diff[1] =  self.pos_start[1] - self.pos_final[1]
                    
        # allow the movement only if the of pos_diff x and y is equal  
        if pos_diff[0] == pos_diff[1]:
            # check if there is a piece in the middle
            i = 1
            if self.pos_start[0] < self.pos_final[0] and self.pos_start[1] > self.pos_final[1]:     # the movement is to left-down
                    while self.pos_start[0]+i != self.pos_final[0]:
                        if self.board[self.pos_start[0]+i][self.pos_start[1]-i] != '--': 
                            return
                        i = i + 1
            elif self.pos_start[0] < self.pos_final[0] and self.pos_start[1] < self.pos_final[1]:   # the movement is to left-top
                while self.pos_start[1]+i != self.pos_final[1]:
                    if self.board[self.pos_start[0]+i][self.pos_start[1]+i] != '--': 
                        return
                    i = i + 1
            elif self.pos_start[0] > self.pos_final[0] and self.pos_start[1] > self.pos_final[1]:   # the movement is to right-down
                while self.pos_start[0]-i != self.pos_final[0]:
                    if self.board[self.pos_start[0]-i][self.pos_start[1]-i] != '--': 
                        return
                    i = i + 1
            elif self.pos_start[0] > self.pos_final[0] and self.pos_start[1] < self.pos_final[1]:   # the movement is to right-top
                while self.pos_start[0]-i != self.pos_final[0]:
                    if self.board[self.pos_start[0]-i][self.pos_start[1]+i] != '--': 
                        return
                    i = i + 1
            self.modifyPosition()
        
        
    def knightMove(self):
        
        # check if final position is correct for the king    
        pos_diff = [0, 0]
        
        # find x diff
        if self.pos_start[0] <= self.pos_final[0]:
            pos_diff[0] =  self.pos_final[0] - self.pos_start[0]
        elif self.pos_start[0] > self.pos_final[0]:
            pos_diff[0] =  self.pos_start[0] - self.pos_final[0]
        
        # find the y diff
        if self.pos_start[1] <= self.pos_final[1]:
            pos_diff[1] =  self.pos_final[1] - self.pos_start[1]
        elif self.pos_start[1] > self.pos_final[1]:
            pos_diff[1] =  self.pos_start[1] - self.pos_final[1] 
        
        
        # allow the movement only if the sum of pos_diff x and y is == 3  
        if pos_diff[0] + pos_diff[1] == 3:
            self.modifyPosition()
    
    def queenMove(self):
        
        self.modifyPosition()
    
    def kingMove(self):
        
        # check if final position is correct for the king    
        pos_diff = [0, 0]
        
        # find x diff
        if self.pos_start[0] <= self.pos_final[0]:
            pos_diff[0] =  self.pos_final[0] - self.pos_start[0]
        elif self.pos_start[0] > self.pos_final[0]:
            pos_diff[0] =  self.pos_start[0] - self.pos_final[0]
        
        # find the y diff
        if self.pos_start[1] <= self.pos_final[1]:
            pos_diff[1] =  self.pos_final[1] - self.pos_start[1]
        elif self.pos_start[1] > self.pos_final[1]:
            pos_diff[1] =  self.pos_start[1] - self.pos_final[1]
        
        # allow the movement only if the pos_diff x and y is <= 1  
        if (pos_diff[0] == 1 or pos_diff[0] == 0 or pos_diff[0] == -1) and (pos_diff[1] == 1 or pos_diff[1] == 0 or pos_diff[1] == -1):
            self.modifyPosition()
        
     
    def getPieceName(self):
        return self.board[self.pos_start[0]][self.pos_start[1]]
    
    def setPlayerClicks(self, playerClicks):
        self.pos_start = playerClicks[0]
        self.pos_final = playerClicks[1]