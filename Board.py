import copy
from Enums.Piece import Piece

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