from enum import Enum

class Color(Enum):
    WHITE = 'w'
    BLACK = 'b'
    NONE = '--'  # empty cell

class PieceType(Enum):
    PAWN = 'p'
    ROOK = 'r'
    KNIGHT = 'n'
    BISHOP = 'b'
    QUEEN = 'q'
    KING = 'k'
    EMPTY = '--'  # empty cell
