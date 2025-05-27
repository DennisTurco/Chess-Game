from Board import Board
from Entities.Pos import Pos
from Pieces.Piece import Piece

class King(Piece):
    def __init__(self, board: Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy: Pos) -> None:
        moves = [(-1, -1), (-1, +1), (+1, -1), (+1, +1),
                 (+1, 0), (0, +1), (-1, 0), (0, -1)]
        for dx, dy in moves:
            self.specific_scan_check(posxy, dx, dy)

