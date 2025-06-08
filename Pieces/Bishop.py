import chess
from Entities.Pos import Pos
from Pieces.Piece import Piece

class Bishop(Piece):
    def __init__(self, board: chess.Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy: Pos) -> None:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals
        for dx, dy in directions:
            self.linear_or_diagonal_scan(posxy, dx, dy)
