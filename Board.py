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
        
        self.startBoard = self.board
        
    def restartBoard(self):
        self.board = self.startBoard
        

# -----------------------------------------------------------------

class MessageBox():
    
    def __init__(self):
        self.__whiteWin = "White has won the game!"
        self.__blackWin = "Black has won the game!"
        self.__question = "Would you like to restart the game?"
        self.__titleMessage = "Good Job"
        self.__restart = False
        
    def setWinner(self, isWhite):
        # check the winner   
        if isWhite: self.__restart = messagebox.askyesno(self.__titleMessage, self.__whiteWin + "\n" + self.__question)
        else: self.__restart = messagebox.askyesno(self.__titleMessage, self.__blackWin + "\n" + self.__question)
        
    def getRestartResponse(self):
        return self.__restart
        

# -----------------------------------------------------------------

class Move():

    def __init__(self, playerClicks, board):  
        self.__pos_start = playerClicks[0]
        self.__pos_final = playerClicks[1]
        self.__board = board
        self.__whiteMove = True
        self.__finished = False
        self.__possibleMovements = [[],[]]
        
        self.__initPossiblePositions()
        
        try:
            self.__sound_move = simpleaudio.WaveObject.from_wave_file("sounds/move.wav")
            self.__sound_capture = simpleaudio.WaveObject.from_wave_file("sounds/capture.wav")
        except:
            logging.error(sys.argv[0] + " -> error on loading sounds")        

    def __initPossiblePositions(self):
        # create a matrix 8 x 8 full with '0'
        self.__possibleMovements = [[0 for x in range(len(self.__board))] for y in range(len(self.__board))]    
    
    def getPossiblePositions(self):
        return self.__possibleMovements
    
    def isWhitePiece(self, x, y):
        piece_name = self.__board[x][y]
        return piece_name[0] == 'w'
    
    def isPlayerWhiteTurn(self):
        return self.__whiteMove
    
    def __modifyPosition(self):
        # check if it is a simple move or someone is capturing a piece to play the correct sound
        if self.getTargetPieceName() == '--':
            try: self.__sound_move.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
        else:
            try: self.__sound_capture.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
            
        self.__initPossiblePositions()
            
        self.__board[self.__pos_final[0]][self.__pos_final[1]] = self.getCurrentPieceName()
        self.__board[self.__pos_start[0]][self.__pos_start[1]] = '--'
            
        if self.__whiteMove == True: 
            self.__whiteMove = False
        else:
            self.__whiteMove = True
        
        self.__printMatrix(self.__board)  
    
    def captureRequest(self, playerClicks):        
        if self.__finished: return
        
        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)
        
        # the white piace cannot eat another white piece (same for black)
        piece_name = self.getTargetPieceName()
        if  (self.__whiteMove == True and piece_name[0] == 'w') or (self.__whiteMove == False and piece_name[0] == 'b'):
            return
        else:
            self.moveRequest(playerClicks) 
            self.isCheckMate()  
        
    def setPossibleMovements(self, posxy):
        
        self.__initPossiblePositions()
        
        piece_name = self.getCurrentPieceName2(posxy[0], posxy[1])
        
        if piece_name[0] == 'w' and not self.__whiteMove: return
        if piece_name[0] == 'b' and self.__whiteMove: return
        
        if piece_name[1] == 'p':
           self.__pawnPossiblesMove(posxy, piece_name)
                                
        elif piece_name[1] == 'R':
            self.__rockPossiblesMove(posxy)       
            
        elif  piece_name[1] == 'B':
            self.__bishopPossiblesMove(posxy)       
            
        elif piece_name[1] == 'N':
            self.__knightPossiblesMove(posxy)
            
        elif piece_name[1] == 'Q':
            self.__rockPossiblesMove(posxy)
            self.__bishopPossiblesMove(posxy)
            
        elif piece_name[1] == 'K':
            self.__kingPossiblesMove(posxy)
                  
    def moveRequest(self, playerClicks):
        if self.__finished: return
        
        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)
    
        piece_name = self.getCurrentPieceName()
        
        # errors check
        if piece_name[0] == "w" and self.__whiteMove == False:
            logging.error(sys.argv[0] + " -> 'piece_name[0] == \"w\" and self.__whiteMove == False' ")
            return
        elif piece_name[0] == "b" and self.__whiteMove == True:
            logging.error(sys.argv[0] + " -> 'piece_name[0] == \"b\" and self.__whiteMove == True' ")
            return
        
        # movement
        self.__pieceMove()
        
        
    def __pawnPossiblesMove(self, posxy, piece_name):
         # white turn
            if self.__whiteMove:
                # movement 
                if self.__board[posxy[0]][posxy[1]-1] == '--': self.__possibleMovements[posxy[0]][posxy[1]-1] = 1
                if posxy[1] == 6 and self.__board[posxy[0]][posxy[1]-2] == '--': self.__possibleMovements[posxy[0]][posxy[1]-2] = 1
                # capture
                if piece_name[0] == 'w':   
                    if posxy[0] != len(self.__board)-1 and posxy[1] != len(self.__board)-1: # i need this check for avoid "list index out of range" 
                        if (not self.isWhitePiece(posxy[0]-1, posxy[1]-1)) and (self.getPossibleTargetPieceName(posxy[0]-1, posxy[1]-1) != '--'): 
                            self.__possibleMovements[posxy[0]-1][posxy[1]-1] = 2
                        if (not self.isWhitePiece(posxy[0]+1, posxy[1]-1)) and (self.getPossibleTargetPieceName(posxy[0]+1, posxy[1]-1) != '--'): 
                            self.__possibleMovements[posxy[0]+1][posxy[1]-1] = 2
                                       
            # black turn
            else:
                # movement 
                if self.__board[posxy[0]][posxy[1]+1] == '--': self.__possibleMovements[posxy[0]][posxy[1]+1] = 1
                if posxy[1] == 1 and self.__board[posxy[0]][posxy[1]+2] == '--': self.__possibleMovements[posxy[0]][posxy[1]+2] = 1
                # capture
                if piece_name[0] == 'b':  
                    if posxy[0] != len(self.__board)-1 and posxy[1] != len(self.__board)-1:  # i need this check for avoid "list index out of range" 
                        if (self.isWhitePiece(posxy[0]+1, posxy[1]+1)) and (self.getPossibleTargetPieceName(posxy[0]+1, posxy[1]+1) != '--'): 
                            self.__possibleMovements[posxy[0]+1][posxy[1]+1] = 2
                        if (self.isWhitePiece(posxy[0]-1, posxy[1]+1)) and (self.getPossibleTargetPieceName(posxy[0]-1, posxy[1]+1) != '--'):  
                            self.__possibleMovements[posxy[0]-1][posxy[1]+1] = 2
    
    #FIXME: fix black rock move                         
    def __rockPossiblesMove(self, posxy):
        # check if there is a piece in the middle
        i = 1
        while posxy[1]-i != len(self.__board):    # the movement is from top to down
            if self.__board[posxy[0]][posxy[1]-i] != '--': 
                if (self.isWhitePiece(posxy[0], posxy[1]-i) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]-i) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]][posxy[1]-i] = 2
                break
            self.__possibleMovements[posxy[0]][posxy[1]-i] = 1
            i = i + 1
        i = 1
        while posxy[1]+i != len(self.__board):    # the movement is from down to top
            if self.__board[posxy[0]][posxy[1]+i] != '--': 
                if (self.isWhitePiece(posxy[0], posxy[1]+i) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]+i) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]][posxy[1]+i] = 2
                break
            self.__possibleMovements[posxy[0]][posxy[1]+i] = 1
            i = i + 1
        i = 1
        while posxy[0]-i != len(self.__board):    # the movement is from right to left
            if self.__board[posxy[0]-i][posxy[1]] != '--': 
                if (self.isWhitePiece(posxy[0]-i, posxy[1]) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-i, posxy[1]) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]-i][posxy[1]] = 2
                break
            self.__possibleMovements[posxy[0]-i][posxy[1]] = 1
            i = i + 1
        i = 1
        while posxy[0]+i != len(self.__board):    # the movement is from right to left
            if self.__board[posxy[0]+i][posxy[1]] != '--': 
                if (self.isWhitePiece(posxy[0]+i, posxy[1]) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]+i][posxy[1]] = 2
                break
            self.__possibleMovements[posxy[0]+i][posxy[1]] = 1
            i = i + 1
                
    def __bishopPossiblesMove(self, posxy):
        # check if there is a piece in the middle
        i = 1
        while posxy[0]-i >= 0 and posxy[1]-i >= 0:    # the movement is from bottom to top-left
            if self.__board[posxy[0]-i][posxy[1]-i] != '--': 
                if (self.isWhitePiece(posxy[0]-i, posxy[1]-i) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-i, posxy[1]-i) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]-i][posxy[1]-i] = 2
                break
            self.__possibleMovements[posxy[0]-i][posxy[1]-i] = 1
            i = i + 1
        i = 1
        while posxy[0]+i <= len(self.__board)-1 and posxy[1]+i <= len(self.__board)-1:    # the movement is from top to bottom-right
            if self.__board[posxy[0]+i][posxy[1]+i] != '--': 
                if (self.isWhitePiece(posxy[0]+i, posxy[1]+i) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]+i) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]+i][posxy[1]+i] = 2
                break
            self.__possibleMovements[posxy[0]+i][posxy[1]+i] = 1
            i = i + 1
        i = 1   
        while posxy[0]-i >= 0 and posxy[1]+i <= len(self.__board)-1:    # the movement is from top to bommon-left
            if self.__board[posxy[0]-i][posxy[1]+i] != '--': 
                if (self.isWhitePiece(posxy[0]-i, posxy[1]+i) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-i, posxy[1]+i) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]-i][posxy[1]+i] = 2
                break
            self.__possibleMovements[posxy[0]-i][posxy[1]+i] = 1
            i = i + 1
        i = 1
        while posxy[0]+i <= len(self.__board)-1 and posxy[1]-i >= 0:    # the movement is from bottom to top-right
            if self.__board[posxy[0]+i][posxy[1]-i] != '--': 
                if (self.isWhitePiece(posxy[0]+i, posxy[1]-i) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]-i) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]+i][posxy[1]-i] = 2
                break
            self.__possibleMovements[posxy[0]+i][posxy[1]-i] = 1
            i = i + 1
        i = 1
                  
    def __knightPossiblesMove(self, posxy):
        # check if final position is correct for the night              
        if posxy[0]-1 >= 0 and posxy[1]-2 >= 0:                     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]-1][posxy[1]-2] == '--':
                self.__possibleMovements[posxy[0]-1][posxy[1]-2] = 1
            elif self.__board[posxy[0]-1][posxy[1]-2] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]-2) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]-2) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-1][posxy[1]-2] = 2
                
        if posxy[0]-1 >= 0 and posxy[1]+2 <= len(self.__board)-1:     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]-1][posxy[1]+2] == '--':
                self.__possibleMovements[posxy[0]-1][posxy[1]+2] = 1
            elif self.__board[posxy[0]-1][posxy[1]+2] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]+2) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]+2) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-1][posxy[1]+2] = 2
                
        if posxy[0]+1 <= len(self.__board)-1 and posxy[1]+2 <= len(self.__board)-1:     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]+1][posxy[1]+2] == '--':
                self.__possibleMovements[posxy[0]+1][posxy[1]+2] = 1
            elif self.__board[posxy[0]+1][posxy[1]+2] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]+2) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]+2) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+1][posxy[1]+2] = 2
                
        if posxy[0]+2 <= len(self.__board)-1 and posxy[1]+1 <= len(self.__board)-1:     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]+2][posxy[1]+1] == '--':
                self.__possibleMovements[posxy[0]+2][posxy[1]+1] = 1
            elif self.__board[posxy[0]+2][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]+2, posxy[1]+1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+2, posxy[1]+1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+2][posxy[1]+1] = 2
        
        if posxy[0]+1 <= len(self.__board)-1 and posxy[1]-2 >= 0:     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]+1][posxy[1]-2] == '--':
                self.__possibleMovements[posxy[0]+1][posxy[1]-2] = 1
            elif self.__board[posxy[0]+1][posxy[1]-2] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]-2) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]-2) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+1][posxy[1]-2] = 2
                
        if posxy[0]-2 >= 0 and posxy[1]+1 <= len(self.__board)-1:     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]-2][posxy[1]+1] == '--':
                self.__possibleMovements[posxy[0]-2][posxy[1]+1] = 1
            elif self.__board[posxy[0]-2][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]-2, posxy[1]+1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-2, posxy[1]+1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-2][posxy[1]+1] = 2     
        
        if posxy[0]+2 <= len(self.__board)-1 and posxy[1]-1 >= 0:     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]+2][posxy[1]-1] == '--':
                self.__possibleMovements[posxy[0]+2][posxy[1]-1] = 1
            elif self.__board[posxy[0]+2][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]+2, posxy[1]-1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+2, posxy[1]-1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+2][posxy[1]-1] = 2
                
        if posxy[0]-2 >= 0 and posxy[1]-1 >= 0:                     # i need this check for avoid "list index out of range"    
            if self.__board[posxy[0]-2][posxy[1]-1] == '--':
                self.__possibleMovements[posxy[0]-2][posxy[1]-1] = 1
            elif self.__board[posxy[0]-2][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]-2, posxy[1]-1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-2, posxy[1]-1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-2][posxy[1]-1] = 2
        
    def __kingPossiblesMove(self, posxy):
        # check if final position is correct for the king    
        if posxy[0]-1 >= 0 and posxy[1]-1 >= 0:                     # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]-1][posxy[1]-1] == '--':
                self.__possibleMovements[posxy[0]-1][posxy[1]-1] = 1
            elif self.__board[posxy[0]-1][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]-1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]-1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-1][posxy[1]-1] = 2
        
        if posxy[0]-1 >= 0 and posxy[1]+1 <= len(self.__board)-1:                     # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]-1][posxy[1]+1] == '--':
                self.__possibleMovements[posxy[0]-1][posxy[1]+1] = 1
            elif self.__board[posxy[0]-1][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]+1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]+1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-1][posxy[1]+1] = 2
                
        if posxy[0]+1 <= len(self.__board)-1 and posxy[1]-1 >= 0:                     # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]+1][posxy[1]-1] == '--':
                self.__possibleMovements[posxy[0]+1][posxy[1]-1] = 1
            elif self.__board[posxy[0]+1][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]-1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]-1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+1][posxy[1]-1] = 2
        
        if posxy[0]+1 <= len(self.__board)-1 and posxy[1]+1 <= len(self.__board)-1:     # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]+1][posxy[1]+1] == '--':
                self.__possibleMovements[posxy[0]+1][posxy[1]+1] = 1
            elif self.__board[posxy[0]+1][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]+1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]+1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+1][posxy[1]+1] = 2
        
        if posxy[0]+1 <= len(self.__board)-1:         # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]+1][posxy[1]] == '--':
                self.__possibleMovements[posxy[0]+1][posxy[1]] = 1
            elif self.__board[posxy[0]+1][posxy[1]] != '--' and (self.isWhitePiece(posxy[0]+1, posxy[1]) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+1, posxy[1]) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]+1][posxy[1]] = 2
                
        if posxy[1]+1 <= len(self.__board)-1:         # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]][posxy[1]+1] == '--':
                self.__possibleMovements[posxy[0]][posxy[1]+1] = 1
            elif self.__board[posxy[0]][posxy[1]+1] != '--' and (self.isWhitePiece(posxy[0], posxy[1]+1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]+1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]][posxy[1]+1] = 2
                
        if posxy[0]-1 >= 0:                         # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]-1][posxy[1]] == '--':
                self.__possibleMovements[posxy[0]-1][posxy[1]] = 1
            elif self.__board[posxy[0]-1][posxy[1]] != '--' and (self.isWhitePiece(posxy[0]-1, posxy[1]) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]-1, posxy[1]) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]-1][posxy[1]] = 2
        
        if posxy[1]-1 >= 0:                         # i need this check for avoid "list index out of range" 
            if self.__board[posxy[0]][posxy[1]-1] == '--':
                self.__possibleMovements[posxy[0]][posxy[1]-1] = 1
            elif self.__board[posxy[0]][posxy[1]-1] != '--' and (self.isWhitePiece(posxy[0], posxy[1]-1) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0], posxy[1]-1) and self.__whiteMove): # check if there is a possible capture:
                self.__possibleMovements[posxy[0]][posxy[1]-1] = 2
    
    def __pieceMove(self):  
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)
        if self.__possibleMovements[self.__pos_final[0]][self.__pos_final[1]] != 0:
            self.__modifyPosition()
        else: return      
    
    def getCurrentPieceName(self):
        return self.__board[self.__pos_start[0]][self.__pos_start[1]]
    
    # FIXME: why is not possible overloading?? python is shit (i want java.....)
    def getCurrentPieceName2(self, posx, posy):
        return self.__board[posx][posy]


    def getTargetPieceName(self):
        return self.__board[self.__pos_final[0]][self.__pos_final[1]]
    
    
    def getPossibleTargetPieceName(self, posx, posy):
        return self.__board[posx][posy]

    
    def __printMatrix(self, matrix):
        for i in range(len(matrix)):
            print(matrix[i])
    
    
    def isFinished(self):
        return self.__finished
        
    def isCheckMate(self):
        # check possible check mate, i'm serching king piece. assign to true if they are on the __board
        blackKing = False
        whiteKing = False
        for i in range(len(self.__board)):
            for j in range(len(self.__board)):
                piece_name = self.getCurrentPieceName2(i, j)
                if piece_name == 'bK': blackKing = True
                elif piece_name == 'wK': whiteKing = True
        
        if not blackKing or not whiteKing:
            self.__finished = True
            messageBox = MessageBox()
            if not whiteKing: messageBox.setWinner(False) # white is winner
            else: messageBox.setWinner(True) # black is winner
            
            # check for restart
            if messageBox.getRestartResponse() == True:
                self.__finished = False
                self.__board

    def __setPlayerClicks(self, playerClicks):
        self.__pos_start = playerClicks[0]
        self.__pos_final = playerClicks[1]