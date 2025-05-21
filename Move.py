import logging
import sys
import simpleaudio
import MessageBox as mb
from Enums.Piece import Color, Piece, PieceType
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.Pawn import Pawn

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

        #self.__printMatrix(self.__board)

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
            self.__rookPossiblesMove(posxy)

        elif piece.type == PieceType.BISHOP:
            self.__bishopPossiblesMove(posxy)

        elif piece.type == PieceType.KNIGHT:
            self.__knightPossiblesMove(posxy)

        elif piece.type == PieceType.QUEEN:
            self.__queenPossiblesMove(posxy)

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
        pawn = Pawn(self.__board, self.__whiteMove)
        pawn.generate_moves(posxy, piece.color)
        self.__possibleMovements = pawn.get_possible_moves()

    def __rookPossiblesMove(self, posxy):
        rock = Rook(self.__board, self.__whiteMove)
        rock.generate_moves(posxy)
        self.__possibleMovements = rock.get_possible_moves()

    def __bishopPossiblesMove(self, posxy):
        bishop = Bishop(self.__board, self.__whiteMove)
        bishop.generate_moves(posxy)
        self.__possibleMovements = bishop.get_possible_moves()

    def __knightPossiblesMove(self, posxy):
        knight = Knight(self.__board, self.__whiteMove)
        knight.generate_moves(posxy)
        self.__possibleMovements = knight.get_possible_moves()

    def __queenPossiblesMove(self, posxy):
        queen = Queen(self.__board, self.__whiteMove)
        queen.generate_moves(posxy)
        self.__possibleMovements = queen.get_possible_moves()

    def __kingPossiblesMove(self, posxy):
        king = King(self.__board, self.__whiteMove)
        king.generate_moves(posxy)
        self.__possibleMovements = king.get_possible_moves()

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