from Enums.Piece import Color, PieceName
from Pieces.Piece import Piece

class Rook(Piece):
    def __init__(self, board, is_white_turn):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # vertical and horizontal
        for dx, dy in directions:
            self.linear_or_diagonal_scan(posxy, dx, dy)
