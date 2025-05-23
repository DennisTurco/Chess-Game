import logging
import sys
import simpleaudio

from MessageBox import MessageBox
from Enums.Piece import Color, PieceName, PieceType
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.Pawn import Pawn

PIECE_CLASS_MAP = {
    PieceType.PAWN: Pawn,
    PieceType.ROOK: Rook,
    PieceType.BISHOP: Bishop,
    PieceType.KNIGHT: Knight,
    PieceType.QUEEN: Queen,
    PieceType.KING: King
}

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
        except Exception as e:
            self.logger.error(f"{sys.argv[0]} -> error on loading sounds: {e}")

    def __initPossiblePositions(self):
        # create a matrix 8 x 8 full with '0'
        self.__possibleMovements = [[0 for x in range(len(self.__board))] for y in range(len(self.__board))]    

    def getPossiblePositions(self):
        return self.__possibleMovements

    def reset_posssible_positions(self):
        self.__possibleMovements = [[0 for _ in range(8)] for _ in range(8)]
        return self.getPossiblePositions()

    def isWhitePiece(self, x, y):
        piece = self.__board[x][y]
        return piece != PieceName.EMPTY and piece.color == Color.WHITE

    def isPlayerWhiteTurn(self):
        return self.__whiteMove

    def __modifyPosition(self):
        self.__playSound()

        self.__initPossiblePositions()

        self.__board[self.__playerClicks.final_position.x][self.__playerClicks.final_position.y] = self.getCurrentPieceName()
        self.__board[self.__playerClicks.initial_position.x][self.__playerClicks.initial_position.y] = PieceName.EMPTY

        # change turn
        self.__whiteMove = not self.__whiteMove

        print("\n###############################")
        self.__printMatrix(self.__board)


    # check if it is a simple move or someone is capturing a piece to play the correct sound
    def __playSound(self):
        try:
            self.__sound_move.play() if self.getTargetPieceName() == PieceName.EMPTY else self.__sound_capture.play()
        except:
            self.logger.error(f"{sys.argv[0]} -> error on playing sound")


    # return True if the piace has been moved correctly
    def captureRequest(self, playerClicks):
        if self.__finished: return False

        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)

        # the white piace cannot eat another white piece (same for black)
        piece = self.getTargetPieceName()
        if (self.__whiteMove and piece != PieceName.EMPTY and piece.color == Color.WHITE) or \
            (not self.__whiteMove and piece != PieceName.EMPTY and piece.color == Color.BLACK):
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
        self.__checkPossibleMoveByPieceType(piece.type, posxy)


    # return True if the piace hab been moved correctly
    def moveRequest(self, playerClicks) -> bool:
        if self.__finished: return False

        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)

        piece = self.getCurrentPieceName()

        # errors check
        if piece.color == Color.WHITE and self.__whiteMove == False:
            self.logger.error(f"{sys.argv[0]} -> 'piece == Color.WHITE and self.__whiteMove == False'")
            return False
        elif piece.color == Color.BLACK and self.__whiteMove == True:
            self.logger.error(f"{sys.argv[0]} -> 'piece == Color.BLACK and self.__whiteMove == True'")
            return False

        # movement
        return self.__pieceMove()


    def __canMove(self, posxy) -> bool:
        if (self.isWhitePiece(posxy.x, posxy.y) and not self.__whiteMove) or \
            (not self.isWhitePiece(posxy.x, posxy.y) and self.__whiteMove):
            return False
        return True


    def __checkPossibleMoveByPieceType(self, type, posxy):
        try:
            piece_class = PIECE_CLASS_MAP[type]
            piece = piece_class(self.__board, self.__whiteMove)
            piece.generate_moves(posxy)
            self.__possibleMovements = piece.get_possible_moves()
        except KeyError:
            raise Exception(f"PieceName type '{type}' does not exist")

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
            for j in range(len(matrix)):
                print(f"{str(matrix[i][j])} ", end="")
            print()

    def isFinished(self):
        return self.__finished

    def isCheckMate(self) -> bool:
        # check possible check mate, i'm serching king piece. assign to true if they are on the __board
        blackKing = False
        whiteKing = False
        for i in range(len(self.__board)):
            for j in range(len(self.__board)):
                piece = self.getCurrentPieceName(i, j)
                if piece == PieceName.BLACK_KING: blackKing = True
                elif piece == PieceName.WHITE_KING: whiteKing = True

        if not blackKing or not whiteKing:
            self.__finished = True
            messageBox = MessageBox()
            if not whiteKing: messageBox.setWinner(False) # white is winner
            else: messageBox.setWinner(True) # black is winner

            # check for restart
            if messageBox.getRestartResponse():
                self.resetGame()

        return self.__finished

    def __setPlayerClicks(self, playerClicks):
        self.__playerClicks = playerClicks

    def resetGame(self):
        self.__board.restartBoard()
        self.__whiteMove = True
        self.__finished = False
        self.__whiteKingCastling = True
        self.__blackKingCastling = True
        self.__initPossiblePositions()