from Enums.Piece import PieceType
from Pieces.Bishop import Bishop
from Pieces.King import King
from Pieces.Pawn import Pawn
from Pieces.Queen import Queen
from Pieces.Rook import Rook
from Pieces.Knight import Knight

class PieceClassMap():

    MAP = {
            PieceType.PAWN: Pawn,
            PieceType.ROOK: Rook,
            PieceType.BISHOP: Bishop,
            PieceType.KNIGHT: Knight,
            PieceType.QUEEN: Queen,
            PieceType.KING: King
        }