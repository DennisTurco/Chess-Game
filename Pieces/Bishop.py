from Enums.Piece import Color, PieceName
from Pieces.Piece import Piece

class Bishop(Piece):
    def __init__(self, board, is_white_turn):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
        for dx, dy in directions:
            self.linear_or_diagonal_scan(posxy, dx, dy)
