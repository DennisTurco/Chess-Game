import copy
from typing import Optional
from Entities.Pos import Pos
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

        self.turn = Color.WHITE

        self.__is_flipped = False
        if color_side is not None and color_side == Color.BLACK:
            self.board = [list(reversed(row)) for row in reversed(self.board)]
            self.__is_flipped = True

        self.startBoard = copy.deepcopy(self.board)

    def restartBoard(self) -> None:
        self.board = copy.deepcopy(self.startBoard) # to reset competly the board

    def move_piece(self, initial_pos: Pos, final_pos: Pos, initial_piece: PieceName, final_piece: PieceName, switch_turn: bool = True):
        self.board[initial_pos.x][initial_pos.y] = final_piece
        self.board[final_pos.x][final_pos.y] = initial_piece

        if switch_turn:
            self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK

    # to convert the board to the standard fen
    def board_to_fen(self) -> str:
        fen_rows = []
        for row in self.board:
            empty = 0
            fen_row = ""
            for piece in row:
                if piece == PieceName.EMPTY:
                    empty += 1
                else:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    symbol = piece.type.value
                    if piece.color == Color.BLACK:
                        symbol = symbol.lower()
                    else:
                        symbol = symbol.upper()
                    fen_row += symbol
            if empty > 0:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        fen = "/".join(fen_rows)
        fen += f" {"w" if self.turn is Color.WHITE else "b"} KQkq - 0 1"
        return fen

    def is_flipped(self):
        return self.__is_flipped