import copy
from Enums.Piece import PieceName

class Board():

    def __init__(self):
        self.board = [
            [PieceName.BLACK_ROOK, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_ROOK],
            [PieceName.BLACK_KNIGHT, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_KNIGHT],
            [PieceName.BLACK_BISHOP, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_BISHOP],
            [PieceName.BLACK_QUEEN, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_QUEEN],
            [PieceName.BLACK_KING, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_KING],
            [PieceName.BLACK_BISHOP, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_BISHOP],
            [PieceName.BLACK_KNIGHT, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_KNIGHT],
            [PieceName.BLACK_ROOK, PieceName.BLACK_PAWN, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.EMPTY, PieceName.WHITE_PAWN, PieceName.WHITE_ROOK],
        ]
        self.startBoard = copy.deepcopy(self.board)

    def restartBoard(self) -> None:
        self.board = copy.deepcopy(self.startBoard) # to reset competly the board