import copy
from typing import Optional
from Enums.Piece import Color, PieceName

class Board():

    def __init__(self, color_side: Optional[Color] = None):
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

        if color_side is not None and color_side == Color.BLACK:
            self.board = [list(reversed(row)) for row in reversed(self.board)]

        self.startBoard = copy.deepcopy(self.board)

    def restartBoard(self) -> None:
        self.board = copy.deepcopy(self.startBoard) # to reset competly the board

    # to convert the board to the standard fen
    def board_to_fen(self) -> str:
        fen_rows = []
        for row in self.board:
            empty = 0
            fen_row = ""
            for piece in row:
                symbol = piece.value  # e.g., 'p', 'K', '.'
                if symbol == ".":
                    empty += 1
                else:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += symbol
            if empty > 0:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        fen = "/".join(fen_rows)
        fen += " w KQkq - 0 1"  # Add default metadata
        return fen