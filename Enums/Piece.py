from enum import Enum

class Color(Enum):
    WHITE = 'w'
    BLACK = 'b'
    NONE = '--'  # empty cell

class PieceType(Enum):
    PAWN = 'p'
    ROOK = 'R'
    KNIGHT = 'N'
    BISHOP = 'B'
    QUEEN = 'Q'
    KING = 'K'
    EMPTY = '--'  # empty cell

class PieceName(Enum):
    EMPTY = (Color.NONE, PieceType.EMPTY)
    WHITE_PAWN = (Color.WHITE, PieceType.PAWN)
    WHITE_ROOK = (Color.WHITE, PieceType.ROOK)
    WHITE_KNIGHT = (Color.WHITE, PieceType.KNIGHT)
    WHITE_BISHOP = (Color.WHITE, PieceType.BISHOP)
    WHITE_QUEEN = (Color.WHITE, PieceType.QUEEN)
    WHITE_KING = (Color.WHITE, PieceType.KING)
    BLACK_PAWN = (Color.BLACK, PieceType.PAWN)
    BLACK_ROOK = (Color.BLACK, PieceType.ROOK)
    BLACK_KNIGHT = (Color.BLACK, PieceType.KNIGHT)
    BLACK_BISHOP = (Color.BLACK, PieceType.BISHOP)
    BLACK_QUEEN = (Color.BLACK, PieceType.QUEEN)
    BLACK_KING = (Color.BLACK, PieceType.KING)

    def __init__(self, color, type_):
        self.color = color
        self.type = type_

    def __str__(self):
        if self == PieceName.EMPTY:
            return '--'
        return self.color.value + self.type.value

    @staticmethod
    def from_string(s):
        if s == '--':
            return PieceName.EMPTY
        color = Color(s[0])
        type_ = PieceType(s[1])
        for piece in PieceName:
            if piece.color == color and piece.type == type_:
                return piece
        raise ValueError(f"Invalid piece string: {s}")
