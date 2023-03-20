# SELF represents the instance of class. This handy keyword allows you to access variables, attributes, and methods of a defined class in Python.
# the Python equivalent of the C++ constructor in an object-oriented approach.

import logging
import sys

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
        
    def getPieceName(self, playerClicks):
        return self.board[playerClicks[0][0]][playerClicks[0][1]]


# -----------------------------------------------------------------

class Move():

    def __init__(self, playerClicks, board):
        self.playerClicks = playerClicks
        self.board = board
        self.whiteMove = True
        self.finished = False

    def modifyPosition(self, playerClicks):
        piece_name = Board.getPieceName(playerClicks)
        self.board[playerClicks[1][0]][playerClicks[1][1]] = piece_name
        self.board[playerClicks[0][0]][playerClicks[0][1]] = '--'


    def moveRequest(self, playerClicks):
        
        if self.finished: return
        
        piece_name = Board.getPieceName(playerClicks)
        
        # errors check
        if piece_name[0] == "w" and self.whiteMove == False:
            logging.error("{} -> 'piece_name[0] == \"w\" and self.whiteMove == False' ", format(sys.argv[0]))
            return
        elif piece_name[0] == "b" and self.whiteMove == True:
            logging.error("{} -> 'piece_name[0] == \"b\" and self.whiteMove == True' ", format(sys.argv[0]))
            return
        
        # pawns
        if piece_name[1] == 'p':
            self.pawnMove(playerClicks)
        
        # rocks
        elif piece_name[1] == 'R':
            self.rockMove(playerClicks)
        
        # bishops
        elif piece_name[1] == 'B':
            self.rockMove(playerClicks)
        
        # knights
        elif piece_name[1] == 'K':
            self.rockMove(playerClicks)
            
        # queen
        elif piece_name[1] == 'Q':
            self.rockMove(playerClicks)
            
        # king
        elif piece_name[1] == 'K':
            self.rockMove(playerClicks)
            
        else:
            logging.error("{} -> piece: '{}' doesn't exist", format(sys.argv[0], piece_name[1]))
            return
            
    def pawnMove(self, playerClicks):
        # white turn
        if self.whiteMove:
            if (playerClicks[0][1] == playerClicks[1][1]+1) or (playerClicks[0][1] == playerClicks[1][1]+2 and playerClicks[0][1] == 6):
                self.modifyPosition(playerClicks)
                self.whiteMove = False
            else: return
        # black turn
        else:
            if (playerClicks[0][1] == playerClicks[1][1]+1) or (playerClicks[0][1] == playerClicks[1][1]-2 and playerClicks[0][1] == 2):
                self.modifyPosition(playerClicks)
                self.whiteMove = True
            else: return
    
    def rockMove(self, playerClicks):
        # white turn
        if self.whiteMove:
            if True:
                self.modifyPosition(playerClicks)
                self.whiteMove = False
            else: return
        # black turn
        else:
            if True:
                self.modifyPosition(playerClicks)
                self.whiteMove = True
            else: return