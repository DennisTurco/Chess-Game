from Board import Board
from Entities.Pos import Pos
from Enums.Piece import Color, PieceName
from Pieces.Piece import Piece

class Knight(Piece):
    def __init__(self, board: Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy: Board) -> None:
        moves = [(-1, -2), (-1, +2), (+1, +2), (+2, +1),
                 (+1, -2), (-2, +1), (+2, -1), (-2, -1)]
        for dx, dy in moves:
            self.specific_scan_check(posxy, dx, dy)
