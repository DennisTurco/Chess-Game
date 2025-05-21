import logging
import sys
import copy
import simpleaudio
from Enums.Piece import Color, Piece, PieceType
import MessageBox as mb

class Board():

    def __init__(self):
        self.board = [
            [Piece.BLACK_ROOK, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_ROOK],
            [Piece.BLACK_KNIGHT, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_KNIGHT],
            [Piece.BLACK_BISHOP, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_BISHOP],
            [Piece.BLACK_QUEEN, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_QUEEN],
            [Piece.BLACK_KING, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_KING],
            [Piece.BLACK_BISHOP, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_BISHOP],
            [Piece.BLACK_KNIGHT, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_KNIGHT],
            [Piece.BLACK_ROOK, Piece.BLACK_PAWN, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.EMPTY, Piece.WHITE_PAWN, Piece.WHITE_ROOK],
        ]
        self.startBoard = self.board

    def restartBoard(self):
        self.board = copy.deepcopy(self.startBoard) # to reset competly the board

# -----------------------------------------------------------------

class Move():

    def __init__(self, playerClicks, board):
        self.__pos_start = playerClicks[0]
        self.__pos_final = playerClicks[1]
        self.__board = board
        self.__whiteMove = True
        self.__finished = False
        self.__blackKingCastling = True
        self.__whiteKingCastling = True
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
        piece = self.__board[x][y]
        return piece != Piece.EMPTY and piece.color == Color.WHITE

    def isPlayerWhiteTurn(self):
        return self.__whiteMove

    def __modifyPosition(self):
        # check if it is a simple move or someone is capturing a piece to play the correct sound
        if self.getTargetPieceName() == Piece.EMPTY:
            try: self.__sound_move.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")
        else:
            try: self.__sound_capture.play()
            except: logging.error(sys.argv[0] + " -> error on playing sound")

        self.__initPossiblePositions()

        self.__board[self.__pos_final[0]][self.__pos_final[1]] = self.getCurrentPieceName()
        self.__board[self.__pos_start[0]][self.__pos_start[1]] = Piece.EMPTY

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
        piece = self.getTargetPieceName()
        if  (self.__whiteMove == True and piece == Color.WHITE) or (self.__whiteMove == False and piece == Color.BLACK):
            return
        else:
            self.moveRequest(playerClicks)
            self.isCheckMate()

    def setPossibleMovements(self, posxy):

        self.__initPossiblePositions()

        piece = self.getCurrentPieceName2(posxy[0], posxy[1])

        if self.isWhitePiece(posxy[0], posxy[1]) and not self.__whiteMove: return
        if not self.isWhitePiece(posxy[0], posxy[1]) and self.__whiteMove: return

        if piece.type == PieceType.PAWN:
           self.__pawnPossiblesMove(posxy, piece)

        elif piece.type == PieceType.ROOK:
            self.__rockPossiblesMove(posxy)

        elif piece.type == PieceType.BISHOP:
            self.__bishopPossiblesMove(posxy)

        elif piece.type == PieceType.KNIGHT:
            self.__knightPossiblesMove(posxy)

        elif piece.type == PieceType.QUEEN:
            self.__rockPossiblesMove(posxy)
            self.__bishopPossiblesMove(posxy)

        elif piece.type == PieceType.KING:
            self.__kingPossiblesMove(posxy)

    def moveRequest(self, playerClicks):
        if self.__finished: return

        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)

        piece = self.getCurrentPieceName()

        # errors check
        if piece == Color.WHITE and self.__whiteMove == False:
            logging.error(sys.argv[0] + " -> 'piece[0] == \"w\" and self.__whiteMove == False'")
            return
        elif piece == Color.BLACK and self.__whiteMove == True:
            logging.error(sys.argv[0] + " -> 'piece[0] == \"b\" and self.__whiteMove == True'")
            return

        # movement
        self.__pieceMove()


    def __pawnPossiblesMove(self, posxy, piece):
        # white turn
        if self.__whiteMove:
            # movement
            if self.__board[posxy[0]][posxy[1]-1] == Piece.EMPTY: self.__possibleMovements[posxy[0]][posxy[1]-1] = 1
            if posxy[1] == 6 and self.__board[posxy[0]][posxy[1]-2] == Piece.EMPTY: self.__possibleMovements[posxy[0]][posxy[1]-2] = 1
            # capture
            if piece == Color.WHITE:
                if posxy[0] != len(self.__board)-1 and posxy[1] != len(self.__board)-1: # i need this check for avoid "list index out of range"
                    if (not self.isWhitePiece(posxy[0]-1, posxy[1]-1)) and (self.getPossibleTargetPieceName(posxy[0]-1, posxy[1]-1) != Piece.EMPTY): 
                        self.__possibleMovements[posxy[0]-1][posxy[1]-1] = 2
                    if (not self.isWhitePiece(posxy[0]+1, posxy[1]-1)) and (self.getPossibleTargetPieceName(posxy[0]+1, posxy[1]-1) != Piece.EMPTY): 
                        self.__possibleMovements[posxy[0]+1][posxy[1]-1] = 2
        # black turn
        else:
            # movement
            if self.__board[posxy[0]][posxy[1]+1] == Piece.EMPTY: self.__possibleMovements[posxy[0]][posxy[1]+1] = 1
            if posxy[1] == 1 and self.__board[posxy[0]][posxy[1]+2] == Piece.EMPTY: self.__possibleMovements[posxy[0]][posxy[1]+2] = 1
            # capture
            if piece == Color.BLACK:
                if posxy[0] != len(self.__board)-1 and posxy[1] != len(self.__board)-1:  # i need this check for avoid "list index out of range"
                    if (self.isWhitePiece(posxy[0]+1, posxy[1]+1)) and (self.getPossibleTargetPieceName(posxy[0]+1, posxy[1]+1) != Piece.EMPTY):
                        self.__possibleMovements[posxy[0]+1][posxy[1]+1] = 2
                    if (self.isWhitePiece(posxy[0]-1, posxy[1]+1)) and (self.getPossibleTargetPieceName(posxy[0]-1, posxy[1]+1) != Piece.EMPTY):
                        self.__possibleMovements[posxy[0]-1][posxy[1]+1] = 2

    def __rockPossiblesMove(self, posxy):
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, 0, +1)     # the movement is from top to down
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, 0, -1)     # the movement is from down to top
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, -1, 0)     # the movement is from right to left
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, +1, 0)     # the movement is from left to right

    def __bishopPossiblesMove(self, posxy):
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, -1, -1)      # the movement is from bottom to top-left
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, +1, +1)      # the movement is from top to bottom-right
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, -1, +1)      # the movement is from top to bommon-left
        self.__rockAndBishopPossiblesMoveAlgorithm(posxy, +1, -1)      # the movement is from bottom to top-right

    def __knightPossiblesMove(self, posxy):
        # check if final position is correct for the night
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -1, -2)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -1, +2)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +1, +2)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +2, +1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +1, -2)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -2, +1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +2, -1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -2, -1)

    def __kingPossiblesMove(self, posxy):
        # check if final position is correct for the king
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -1, -1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -1, +1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +1, -1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +1, +1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, +1, 0)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, 0, +1)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, -1, 0)
        self.__knightAndKingPossiblesMoveAlgorithm(posxy, 0, -1)

    def __rockAndBishopPossiblesMoveAlgorithm(self, posxy, incrementer1, incrementer2):
        i = incrementer1
        j = incrementer2

        condition = True

        # check if there is a piece in the middle
        while condition:

            condition = posxy[0]+i <= len(self.__board)-1 and posxy[1]+j <= len(self.__board)-1 and posxy[0]+i >= 0 and posxy[1]+j >= 0

            if (not condition): return

            if self.__board[posxy[0]+i][posxy[1]+j] != Piece.EMPTY:
                if (self.isWhitePiece(posxy[0]+i, posxy[1]+j) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]+j) and self.__whiteMove): # check if there is a possible capture
                    self.__possibleMovements[posxy[0]+i][posxy[1]+j] = 2
                break
            self.__possibleMovements[posxy[0]+i][posxy[1]+j] = 1
            i = i + incrementer1
            j = j + incrementer2

    def __knightAndKingPossiblesMoveAlgorithm(self, posxy, i, j):
        condition = posxy[1]+j <= len(self.__board)-1 and posxy[0]+i <= len(self.__board)-1 and posxy[1]+j >= 0 and posxy[0]+i >= 0

        if (not condition): return

        if self.__board[posxy[0]+i][posxy[1]+j] == Piece.EMPTY:
            self.__possibleMovements[posxy[0]+i][posxy[1]+j] = 1
        elif self.__board[posxy[0]+i][posxy[1]+j] != Piece.EMPTY and (self.isWhitePiece(posxy[0]+i, posxy[1]+j) and not self.__whiteMove) or (not self.isWhitePiece(posxy[0]+i, posxy[1]+j) and self.__whiteMove): # check if there is a possible capture:
            self.__possibleMovements[posxy[0]+i][posxy[1]+j] = 2

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
                piece = self.getCurrentPieceName2(i, j)
                if piece == Piece.BLACK_KING: blackKing = True
                elif piece == Piece.WHITE_KING: whiteKing = True

        if not blackKing or not whiteKing:
            self.__finished = True
            messageBox = mb.MessageBox()
            if not whiteKing: messageBox.setWinner(False) # white is winner
            else: messageBox.setWinner(True) # black is winner

            # check for restart
            if messageBox.getRestartResponse() == True:
                self.__finished = False
                self.__board

    def __setPlayerClicks(self, playerClicks):
        self.__pos_start = playerClicks[0]
        self.__pos_final = playerClicks[1]