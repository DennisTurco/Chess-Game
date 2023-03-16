# SELF represents the instance of class. This handy keyword allows you to access variables, attributes, and methods of a defined class in Python.
# the Python equivalent of the C++ constructor in an object-oriented approach.

class Board():

    def __init__(self):
        '''self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],]'''

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
        self.playerClicks = playerClicks
        self.board = board
        self.whiteMove = True
        self.finished = True 

    def modifyPosition(self, playerClicks):
        self.board[playerClicks[1][0]][playerClicks[1][1]] = self.board[playerClicks[0][0]][playerClicks[0][1]]
        self.board[playerClicks[0][0]][playerClicks[0][1]] = '--'
        
        playerClicks = [[], []]
        return playerClicks

    def pawnMove(self):
        if self.finished:
            return
        
        if self.whiteMove:
            self.whiteMove = False