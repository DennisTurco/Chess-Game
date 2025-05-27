import logging
import sys

import pygame

from Board import Board
from Entities.Pos import Pos
from Entities.PosMove import PosMove
from Menus.MessageBox import MessageBox
from Enums.Piece import Color, PieceName, PieceType
from Pieces.PieceClassMap import PieceClassMap

class Move():

    def __init__(self, playerClicks: PosMove, board: Board, screen: pygame.Surface):
        self.__playerClicks = playerClicks
        self.__board = board
        self.__screen = screen
        self.__whiteMove = True
        self.__finished = False
        self.__restart = False
        self.__blackKingCastling = True
        self.__whiteKingCastling = True
        self.__possibleMovements = self.reset_posssible_positions()

        self.__sound_move = pygame.mixer.Sound("sounds/move.wav")
        self.__sound_capture = pygame.mixer.Sound("sounds/capture.wav")

        self.__initPossiblePositions()

        self.logger = logging.getLogger(self.__class__.__name__)

    def __initPossiblePositions(self) -> None:
        self.__possibleMovements = [[0 for x in range(len(self.__board))] for y in range(len(self.__board))] # create a matrix 8 x 8 full with '0'

    def getPossiblePositions(self) -> list[list[int]]:
        return self.__possibleMovements

    def reset_posssible_positions(self) -> list[list[int]]:
        self.__possibleMovements = [[0 for _ in range(8)] for _ in range(8)]
        return self.getPossiblePositions()

    def isWhitePiece(self, x: int, y: int) -> bool:
        piece = self.__board[x][y]
        return piece != PieceName.EMPTY and piece.color == Color.WHITE

    def isPlayerWhiteTurn(self) -> bool:
        return self.__whiteMove

    def __modifyPosition(self) -> None:
        self.__playSound()

        self.__initPossiblePositions()

        self.__board[self.__playerClicks.final_position.x][self.__playerClicks.final_position.y] = self.getCurrentPieceName()
        self.__board[self.__playerClicks.initial_position.x][self.__playerClicks.initial_position.y] = PieceName.EMPTY

        # change turn
        self.__whiteMove = not self.__whiteMove

        self.__printMatrix(self.__board)


    # check if it is a simple move or someone is capturing a piece to play the correct sound
    def __playSound(self) -> None:
        try:
            self.__sound_move.play() if self.getTargetPieceName() == PieceName.EMPTY else self.__sound_capture.play()
        except:
            self.logger.error(f"{sys.argv[0]} -> error on playing sound")


    # return True if the piace has been moved correctly
    def captureRequest(self, playerClicks: PosMove) -> bool:
        if self.__finished: return False

        # set __pos_start and __pos_final
        self.__setPlayerClicks(playerClicks)

        # the white piace cannot eat another white piece (same for black)
        piece = self.getTargetPieceName()
        if (self.__whiteMove and piece != PieceName.EMPTY and piece.color == Color.WHITE) or \
            (not self.__whiteMove and piece != PieceName.EMPTY and piece.color == Color.BLACK):
            return False
        else:
            move_request = self.moveRequest(playerClicks)
            check_mate = self.isCheckMate()
            return move_request or check_mate


    def setPossibleMovements(self, posxy: Pos) -> None:
        if not self.__canMove(posxy):
            return
        self.__initPossiblePositions()
        piece = self.getCurrentPieceName(posxy.x, posxy.y)
        self.__checkPossibleMoveByPieceType(piece.type, posxy)


    # return True if the piace hab been moved correctly
    def moveRequest(self, playerClicks: PosMove) -> bool:
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


    def __canMove(self, posxy: Pos) -> bool:
        if (self.isWhitePiece(posxy.x, posxy.y) and not self.__whiteMove) or \
            (not self.isWhitePiece(posxy.x, posxy.y) and self.__whiteMove):
            return False
        return True


    def __checkPossibleMoveByPieceType(self, type: PieceType, posxy: Pos) -> None:
        try:
            piece_class = PieceClassMap.MAP[type]
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

    def getCurrentPieceName(self, posx = None, posy = None) -> PieceName:
        if posx is None or posy is None:
            return self.__board[self.__playerClicks.initial_position.x][self.__playerClicks.initial_position.y]
        else:
            return self.__board[posx][posy]

    def getTargetPieceName(self) -> PieceName:
        return self.__board[self.__playerClicks.final_position.x][self.__playerClicks.final_position.y]

    def getPossibleTargetPieceName(self, posx: Pos, posy: Pos) -> PieceName:
        return self.__board[posx][posy]

    def __printMatrix(self, matrix: list[list[PieceName]]) -> None:
        print("\n###############################")
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                print(f"{str(matrix[i][j])} ", end="")
            print()

    def isFinished(self) -> bool:
        return self.__finished

    def restart(self) -> bool:
        return self.isFinished() and self.__restart

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
            if not whiteKing:
                self.__restart = messageBox.ask_restart(False, self.__screen) # white is winner
            else:
                self.__restart = messageBox.ask_restart(True, self.__screen) # black is winner

        return self.__finished

    def __setPlayerClicks(self, playerClicks: PosMove) -> None:
        self.__playerClicks = playerClicks