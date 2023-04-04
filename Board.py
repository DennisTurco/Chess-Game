# SELF represents the instance of class. This handy keyword allows you to access variables, attributes, and methods of a defined class in Python.
# the Python equivalent of the C++ constructor in an object-oriented approach.

import logging
import sys
import simpleaudio
from tkinter import messagebox


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

class MessageBox():
    
    def __init__(self, board):
        self.whiteWin = "White has won the game!"
        self.blackWin = "Black has won the game!"
        self.titleMessage = "Good Job"
        
    def setWinner(self, isWhite):
        # check the winner        
        if isWhite: messagebox.showinfo(self.titleMessage, self.whiteWin)
        else: messagebox.showinfo(self.titleMessage, self.blackWin)
        

# -----------------------------------------------------------------

class Move():

    def __init__(self, playerClicks, board):     
        self.pos_start = playerClicks[0]
        self.pos_final = playerClicks[1]
        self.board = board
        self.whiteMove = True
        self.finished = False
        self.possibleMovements = [[],[]]
        self.initPossiblePositions()
        
        try:
            self.sound_move = simpleaudio.WaveObject.from_wave_file("sounds/move.wav")
            self.sound_capture = simpleaudio.WaveObject.from_wave_file("sounds/capture.wav")
        except:
            logging.error(sys.argv[0] + " -> error on loading sounds")        

    def initPossiblePositions(self):
        # create a matrix 8 x 8 full with '0'
        self.possibleMovements = [[0 for x in range(len(self.board))] for y in range(len(self.board))]    
    
    def getPossiblePositions(self):
        return self.possibleMovements
    
    def isWhitePiece(self, x, y):
        piece_name = self.board[x][y]
        return piece_name[0] == 'w'
    
    def isPlayerWhiteTurn(self):
        return self.whiteMove
    
    def modifyPosition(self):
        # check if it is a simple move or someone is capturing a piece to play the correct sound
        if self.getTargetPieceName() == '--':
            try: self.sound_move.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
        else:
            try: self.sound_capture.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
            
        self.initPossiblePositions()
            
        self.board[self.pos_final[0]][self.pos_final[1]] = self.getCurrentPieceName()
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
        piece_name = self.getTargetPieceName()
        if  (self.whiteMove == True and piece_name[0] == 'w') or (self.whiteMove == False and piece_name[0] == 'b'):
            return
        else:
            self.moveRequest(playerClicks) 
            self.finished = self.isFinished()  
        
    def checkPossibleMovements(self, posxy):
        
        self.initPossiblePositions()
        
        piece_name = self.getCurrentPieceName2(posxy[0], posxy[1])
        
        if piece_name[0] == 'w' and not self.whiteMove: return
        if piece_name[0] == 'b' and self.whiteMove: return
        
        if piece_name[1] == 'p':
           self.pawnPossiblesMove(posxy, piece_name)
                                
        elif piece_name[1] == 'R':
            self.rockPossiblesMove(posxy)       
            
        elif  piece_name[1] == 'B':
            self.bishopPossiblesMove(posxy)       
            
        elif piece_name[1] == 'N':
            self.knightPossiblesMove(posxy)
            
        elif piece_name[1] == 'Q':
            self.rockPossiblesMove(posxy)
            self.bishopPossiblesMove(posxy)
            
        elif piece_name[1] == 'K':
            self.kingPossiblesMove(posxy)
            
            
    
    def moveRequest(self, playerClicks):
        if self.finished: return
        
        # set pos_start and pos_final
        self.setPlayerClicks(playerClicks)
    
        piece_name = self.getCurrentPieceName()
        
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
        
    
    def pawnPossiblesMove(self, posxy, piece_name):
         # white turn
            if self.whiteMove:
                # movement 
                if self.board[posxy[0]][posxy[1]-1] == '--': self.possibleMovements[posxy[0]][posxy[1]-1] = 1
                if posxy[1] == 6 and self.board[posxy[0]][posxy[1]-1] == '--': self.possibleMovements[posxy[0]][posxy[1]-2] = 1
                # capture
                if piece_name[0] == 'w':   
                    if posxy[0] != len(self.board)-1 and posxy[1] != len(self.board)-1: # i need this check for avoid "list index out of range" 
                        if (not self.isWhitePiece(posxy[0]-1, posxy[1]-1)) and (self.getPossibleTargetPieceName(posxy[0]-1, posxy[1]-1) != '--'): 
                            self.possibleMovements[posxy[0]-1][posxy[1]-1] = 2
                        if (not self.isWhitePiece(posxy[0]+1, posxy[1]-1)) and (self.getPossibleTargetPieceName(posxy[0]+1, posxy[1]-1) != '--'): 
                            self.possibleMovements[posxy[0]+1][posxy[1]-1] = 2
                                       
            # black turn
            else:
                # movement 
                if self.board[posxy[0]][posxy[1]+1] == '--': self.possibleMovements[posxy[0]][posxy[1]+1] = 1
                if posxy[1] == 1 and self.board[posxy[0]][posxy[1]+1] == '--': self.possibleMovements[posxy[0]][posxy[1]+2] = 1
                # capture
                if piece_name[0] == 'b':  
                    if posxy[0] != len(self.board)-1 and posxy[1] != len(self.board)-1:  # i need this check for avoid "list index out of range" 
                        if (self.isWhitePiece(posxy[0]+1, posxy[1]+1)) and (self.getPossibleTargetPieceName(posxy[0]+1, posxy[1]+1) != '--'): 
                            self.possibleMovements[posxy[0]+1][posxy[1]+1] = 2
                        if (self.isWhitePiece(posxy[0]-1, posxy[1]+1)) and (self.getPossibleTargetPieceName(posxy[0]-1, posxy[1]+1) != '--'):  
                            self.possibleMovements[posxy[0]-1][posxy[1]+1] = 2
                            
    def rockPossiblesMove(self, posxy):
        # check if there is a piece in the middle
        i = 1
        while posxy[1]-i != len(self.board):    # the movement is from top to down
            if self.board[posxy[0]][posxy[1]-i] != '--': 
                if (self.isWhitePiece(posxy[0], posxy[1]-i) and not self.whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]-i) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]][posxy[1]-i] = 2
                break
            self.possibleMovements[posxy[0]][posxy[1]-i] = 1
            i = i + 1
        i = 1
        while posxy[1]+i != len(self.board):    # the movement is from down to top
            if self.board[posxy[0]][posxy[1]+i] != '--': 
                if (self.isWhitePiece(posxy[0], posxy[1]+i) and not self.whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]+i) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]][posxy[1]+i] = 2
                break
            self.possibleMovements[posxy[0]][posxy[1]+i] = 1
            i = i + 1
        i = 1
        while posxy[0]-i != len(self.board):    # the movement is from right to left
            if self.board[posxy[0]-i][posxy[1]] != '--': 
                if (self.isWhitePiece(posxy[0]-i, posxy[1]) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-i, posxy[1]) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]-i][posxy[1]] = 2
                break
            self.possibleMovements[posxy[0]-i][posxy[1]] = 1
            i = i + 1
        i = 1
        while posxy[0]+i != len(self.board):    # the movement is from right to left
            if self.board[posxy[0]+i][posxy[1]] != '--': 
                if (self.isWhitePiece(posxy[0]+i, posxy[1]) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]+i][posxy[1]] = 2
                break
            self.possibleMovements[posxy[0]+i][posxy[1]] = 1
            i = i + 1
                
    def bishopPossiblesMove(self, posxy):
        # check if there is a piece in the middle
        i = 1
        while posxy[1]-i != len(self.board):    # the movement is from top to down
            if self.board[posxy[0]][posxy[1]-i] != '--': 
                if (self.isWhitePiece(posxy[0], posxy[1]-i) and not self.whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]-i) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]][posxy[1]-i] = 2
                break
            self.possibleMovements[posxy[0]][posxy[1]-i] = 1
            i = i + 1
        i = 1
        while posxy[1]+i != len(self.board):    # the movement is from down to top
            if self.board[posxy[0]][posxy[1]+i] != '--': 
                if (self.isWhitePiece(posxy[0], posxy[1]+i) and not self.whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]+i) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]][posxy[1]+i] = 2
                break
            self.possibleMovements[posxy[0]][posxy[1]+i] = 1
            i = i + 1
        i = 1
        while posxy[0]-i != len(self.board):    # the movement is from right to left
            if self.board[posxy[0]-i][posxy[1]] != '--': 
                if (self.isWhitePiece(posxy[0]-i, posxy[1]) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-i, posxy[1]) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]-i][posxy[1]] = 2
                break
            self.possibleMovements[posxy[0]-i][posxy[1]] = 1
            i = i + 1
        i = 1
        while posxy[0]+i != len(self.board):    # the movement is from right to left
            if self.board[posxy[0]+i][posxy[1]] != '--': 
                if (self.isWhitePiece(posxy[0]+i, posxy[1]) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]) and self.whiteMove): # check if there is a possible capture
                    self.possibleMovements[posxy[0]+i][posxy[1]] = 2
                break
            self.possibleMovements[posxy[0]+i][posxy[1]] = 1
            i = i + 1
            
    def knightPossiblesMove(self, posxy):
        # check if final position is correct for the night              
        if posxy[0]-1 >= 0 and posxy[1]-2 >= 0:                     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]-1][posxy[1]-2] == '--':
                self.possibleMovements[posxy[0]-1][posxy[1]-2] = 1
            elif self.board[posxy[0]-1][posxy[1]-2] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]-2) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]-2) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-1][posxy[1]-2] = 2
                
        if posxy[0]-1 >= 0 and posxy[1]+2 <= len(self.board)-1:     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]-1][posxy[1]+2] == '--':
                self.possibleMovements[posxy[0]-1][posxy[1]+2] = 1
            elif self.board[posxy[0]-1][posxy[1]+2] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]+2) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]+2) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-1][posxy[1]+2] = 2
                
        if posxy[0]+1 <= len(self.board)-1 and posxy[1]+2 <= len(self.board)-1:     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]+1][posxy[1]+2] == '--':
                self.possibleMovements[posxy[0]+1][posxy[1]+2] = 1
            elif self.board[posxy[0]+1][posxy[1]+2] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]+2) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]+2) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+1][posxy[1]+2] = 2
                
        if posxy[0]+2 <= len(self.board)-1 and posxy[1]+1 <= len(self.board)-1:     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]+2][posxy[1]+1] == '--':
                self.possibleMovements[posxy[0]+2][posxy[1]+1] = 1
            elif self.board[posxy[0]+2][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]+2, posxy[1]+1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+2, posxy[1]+1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+2][posxy[1]+1] = 2
        
        if posxy[0]+1 <= len(self.board)-1 and posxy[1]-2 >= 0:     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]+1][posxy[1]-2] == '--':
                self.possibleMovements[posxy[0]+1][posxy[1]-2] = 1
            elif self.board[posxy[0]+1][posxy[1]-2] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]-2) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]-2) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+1][posxy[1]-2] = 2
                
        if posxy[0]-2 >= 0 and posxy[1]+1 <= len(self.board)-1:     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]-2][posxy[1]+1] == '--':
                self.possibleMovements[posxy[0]-2][posxy[1]+1] = 1
            elif self.board[posxy[0]-2][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]-2, posxy[1]+1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-2, posxy[1]+1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-2][posxy[1]+1] = 2     
        
        if posxy[0]+2 <= len(self.board)-1 and posxy[1]-1 >= 0:     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]+2][posxy[1]-1] == '--':
                self.possibleMovements[posxy[0]+2][posxy[1]-1] = 1
            elif self.board[posxy[0]+2][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]+2, posxy[1]-1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+2, posxy[1]-1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+2][posxy[1]-1] = 2
                
        if posxy[0]-2 >= 0 and posxy[1]-1 >= 0:                     # i need this check for avoid "list index out of range"    
            if self.board[posxy[0]-2][posxy[1]-1] == '--':
                self.possibleMovements[posxy[0]-2][posxy[1]-1] = 1
            elif self.board[posxy[0]-2][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]-2, posxy[1]-1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-2, posxy[1]-1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-2][posxy[1]-1] = 2
        
    def kingPossiblesMove(self, posxy):
        # check if final position is correct for the king    
        if posxy[0]-1 >= 0 and posxy[1]-1 >= 0:                     # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]-1][posxy[1]-1] == '--':
                self.possibleMovements[posxy[0]-1][posxy[1]-1] = 1
            elif self.board[posxy[0]-1][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]-1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]-1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-1][posxy[1]-1] = 2
        
        if posxy[0]-1 >= 0 and posxy[1]+1 <= len(self.board)-1:                     # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]-1][posxy[1]+1] == '--':
                self.possibleMovements[posxy[0]-1][posxy[1]+1] = 1
            elif self.board[posxy[0]-1][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]+1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]+1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-1][posxy[1]+1] = 2
                
        if posxy[0]+1 <= len(self.board)-1 and posxy[1]-1 >= 0:                     # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]+1][posxy[1]-1] == '--':
                self.possibleMovements[posxy[0]+1][posxy[1]-1] = 1
            elif self.board[posxy[0]+1][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]-1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]-1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+1][posxy[1]-1] = 2
        
        if posxy[0]+1 <= len(self.board)-1 and posxy[1]+1 <= len(self.board)-1:     # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]+1][posxy[1]+1] == '--':
                self.possibleMovements[posxy[0]+1][posxy[1]+1] = 1
            elif self.board[posxy[0]+1][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]+1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]+1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+1][posxy[1]+1] = 2
        
        if posxy[0]+1 <= len(self.board)-1:         # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]+1][posxy[1]] == '--':
                self.possibleMovements[posxy[0]+1][posxy[1]] = 1
            elif self.board[posxy[0]+1][posxy[1]] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]+1][posxy[1]] = 2
                
        if posxy[1]+1 <= len(self.board)-1:         # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]][posxy[1]+1] == '--':
                self.possibleMovements[posxy[0]][posxy[1]+1] = 1
            elif self.board[posxy[0]][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0], posxy[1]+1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]+1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]][posxy[1]+1] = 2
                
        if posxy[0]-1 >= 0:                         # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]-1][posxy[1]] == '--':
                self.possibleMovements[posxy[0]-1][posxy[1]] = 1
            elif self.board[posxy[0]-1][posxy[1]] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]) and not self.whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]-1][posxy[1]] = 2
        
        if posxy[1]-1 >= 0:                         # i need this check for avoid "list index out of range" 
            if self.board[posxy[0]][posxy[1]-1] == '--':
                self.possibleMovements[posxy[0]][posxy[1]-1] = 1
            elif self.board[posxy[0]][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0], posxy[1]-1) and not self.whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]-1) and self.whiteMove): # check if there is a possible capture:
                self.possibleMovements[posxy[0]][posxy[1]-1] = 2
    
    def pawnMove(self):        
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)
        if self.possibleMovements[self.pos_final[0]][self.pos_final[1]] != 0:
            self.modifyPosition()
        else: return  
    
    def rockMove(self):
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)        
        if self.possibleMovements[self.pos_final[0]][self.pos_final[1]] != 0:
            self.modifyPosition()
        else: return
        
    def bishopMove(self):                
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)        
        if self.possibleMovements[self.pos_final[0]][self.pos_final[1]] != 0:
            self.modifyPosition()
        else: return  
        
    def knightMove(self):
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)        
        if self.possibleMovements[self.pos_final[0]][self.pos_final[1]] != 0:
            self.modifyPosition()
        else: return
    
    def queenMove(self):
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)        
        if self.possibleMovements[self.pos_final[0]][self.pos_final[1]] != 0:
            self.modifyPosition()
        else: return
    
    def kingMove(self):
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)        
        if self.possibleMovements[self.pos_final[0]][self.pos_final[1]] != 0:
            self.modifyPosition()
        else: return
    
    def getCurrentPieceName(self):
        return self.board[self.pos_start[0]][self.pos_start[1]]
    
    # FIXME: why is not possible overloading?? python is shit (i want java.....)
    def getCurrentPieceName2(self, posx, posy):
        return self.board[posx][posy]


    def getTargetPieceName(self):
        return self.board[self.pos_final[0]][self.pos_final[1]]
    
    
    def getPossibleTargetPieceName(self, posx, posy):
        return self.board[posx][posy]
    
    
    def getPositionDifference(self):
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
        
        return pos_diff

    
    def printMatrix(self):
        for i in range(len(self.possibleMovements)):
            print(self.possibleMovements[i])
    
    
    def isFinished(self):
        if self.finished: MessageBox(self.board)
        else: return

    
    def setPlayerClicks(self, playerClicks):
        self.pos_start = playerClicks[0]
        self.pos_final = playerClicks[1]