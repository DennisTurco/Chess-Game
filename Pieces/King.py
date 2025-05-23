from Enums.Piece import Color, PieceName
from Pieces.Piece import Piece

class King(Piece):
    def __init__(self, board, is_white_turn):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy):
        moves = [(-1, -1), (-1, +1), (+1, -1), (+1, +1),
                 (+1, 0), (0, +1), (-1, 0), (0, -1)]
        for dx, dy in moves:
            self.specific_scan_check(posxy, dx, dy)

