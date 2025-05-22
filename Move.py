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
        self.__playerClicks = playerClicks
        self.__board = board
        self.__whiteMove = True
        self.__finished = False
        self.__blackKingCastling = True
        self.__whiteKingCastling = True
        self.__possibleMovements = self.reset_posssible_positions()

        self.__initPossiblePositions()

        self.logger = logging.getLogger(self.__class__.__name__)

        try:
            self.__sound_move = simpleaudio.WaveObject.from_wave_file("sounds/move.wav")
            self.__sound_capture = simpleaudio.WaveObject.from_wave_file("sounds/capture.wav")
        except:
            self.logger.error(f"{sys.argv[0]} -> error on loading sounds")

    def __initPossiblePositions(self):
        # create a matrix 8 x 8 full with '0'
        self.__possibleMovements = [[0 for x in range(len(self.__board))] for y in range(len(self.__board))]    

    def getPossiblePositions(self):
        return self.__possibleMovements

    def reset_posssible_positions(self):
        self.__possibleMovements = [[],[]]
        return self.getPossiblePositions()

    def isWhitePiece(self, x, y):
        piece = self.__board[x][y]
        return piece != Piece.EMPTY and piece.color == Color.WHITE

    def isPlayerWhiteTurn(self):
        return self.__whiteMove

    def __modifyPosition(self):
        self.__playSound()

        self.__initPossiblePositions()

        self.__board[self.__playerClicks.final_position.x][self.__playerClicks.final_position.y] = self.getCurrentPieceName()
        self.__board[self.__playerClicks.initial_position.x][self.__playerClicks.initial_position.y] = Piece.EMPTY

        if self.__whiteMove == True:
            self.__whiteMove = False
        else:
            self.__whiteMove = True

        self.__printMatrix(self.__board)


    # check if it is a simple move or someone is capturing a piece to play the correct sound
    def __playSound(self):
        try:
            if self.getTargetPieceName() == Piece.EMPTY:
                self.__sound_move.play()
            else:
                self.__sound_capture.play()
        except:
            self.logger.error(f"{sys.argv[0]} -> error on playing sound")


    # return True if the piace has been moved correctly
    def captureRequest(self, playerClicks):
        if self.__finished: return False

        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)

        # the white piace cannot eat another white piece (same for black)
        piece = self.getTargetPieceName()
        if  (self.__whiteMove == True and piece == Color.WHITE) or (self.__whiteMove == False and piece == Color.BLACK):
            return False
        else:
            return (
                self.moveRequest(playerClicks) or
                self.isCheckMate()
            )


    def setPossibleMovements(self, posxy):
        if not self.__canMove(posxy):
            return
        self.__initPossiblePositions()
        piece = self.getCurrentPieceName(posxy.x, posxy.y)
        self.__checkPossibleMoveByPieceType(piece.type, posxy, piece)


    # return True if the piace hab been moved correctly
    def moveRequest(self, playerClicks) -> bool:
        if self.__finished: return False

        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)

        piece = self.getCurrentPieceName()

        # errors check
        if piece == Color.WHITE and self.__whiteMove == False:
            self.logger.error(f"{sys.argv[0]} -> 'piece == Color.WHITE and self.__whiteMove == False'")
            return False
        elif piece == Color.BLACK and self.__whiteMove == True:
            self.logger.error(f"{sys.argv[0]} -> 'piece == Color.BLACK and self.__whiteMove == True'")
            return False

        # movement
        return self.__pieceMove()


    def __canMove(self, posxy) -> bool:
        if self.isWhitePiece(posxy.x, posxy.y) and not self.__whiteMove: return False
        if not self.isWhitePiece(posxy.x, posxy.y) and self.__whiteMove: return False
        return True


    def __checkPossibleMoveByPieceType(self, type, posxy, piece):
        match type:
            case PieceType.PAWN:
                self.__pawnPossiblesMove(posxy, piece)
            case PieceType.ROOK:
                self.__rookPossiblesMove(posxy)
            case PieceType.BISHOP:
                self.__bishopPossiblesMove(posxy)
            case PieceType.KNIGHT:
                self.__knightPossiblesMove(posxy)
            case PieceType.QUEEN:
                self.__queenPossiblesMove(posxy)
            case PieceType.KING:
                self.__kingPossiblesMove(posxy)
            case _:
                raise Exception(f"Piece type '{piece.type} does\'t exist'")


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

    # return True if the piace hab been moved correctly
    def __pieceMove(self) -> bool:
        # check if it is a correct movement or a capture (if the result is: 1 -> movement; 2 -> capture)
        if self.__possibleMovements[self.__playerClicks.final_position.x][self.__playerClicks.final_position.y] != 0:
            self.__modifyPosition()
            return True
        else: return False

    def getCurrentPieceName(self, posx = None, posy = None):
        if posx is None or posy is None:
            return self.__board[self.__playerClicks.initial_position.x][self.__playerClicks.initial_position.y]
        else:
            return self.__board[posx][posy]

    def getTargetPieceName(self):
        return self.__board[self.__playerClicks.final_position.x][self.__playerClicks.final_position.y]

    def getPossibleTargetPieceName(self, posx, posy):
        return self.__board[posx][posy]

    def __printMatrix(self, matrix):
        for i in range(len(matrix)):
            print(matrix[i])

    def isFinished(self):
        return self.__finished

    def isCheckMate(self) -> bool:
        # check possible check mate, i'm serching king piece. assign to true if they are on the __board
        blackKing = False
        whiteKing = False
        for i in range(len(self.__board)):
            for j in range(len(self.__board)):
                piece = self.getCurrentPieceName(i, j)
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

        return False

    def __setPlayerClicks(self, playerClicks):
        self.__playerClicks = playerClicks