from Board import Board
from Pieces.Piece import Piece

class King(Piece):
    def __init__(self, board: Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy, can_castling_left: bool, can_castling_right: bool):
        moves = [(-1, -1), (-1, +1), (+1, -1), (+1, +1),
                 (+1, 0), (0, +1), (-1, 0), (0, -1)]

        if can_castling_left:
            moves.append((-2, 0))

        if can_castling_right:
            moves.append((+2, 0))

        for dx, dy in moves:
            self.specific_scan_check(posxy, dx, dy)

