import chess

from Entities.Pos import Pos
from Pieces.Piece import Piece

class Rook(Piece):
    def __init__(self, board: chess.Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy: Pos) -> None:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # vertical and horizontal
        for dx, dy in directions:
            self.linear_or_diagonal_scan(posxy, dx, dy)
