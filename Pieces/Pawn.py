from Board import Board
from Entities.Pos import Pos
from Enums.Piece import PieceName
from Pieces.Piece import Piece

class Pawn(Piece):
    def __init__(self, board: Board, is_white_turn: bool):
        super().__init__(board, is_white_turn)

    def generate_moves(self, posxy: Pos) -> None:
        x, y = posxy.x, posxy.y
        direction = -1 if self.is_white_turn else 1
        start_row = 6 if self.is_white_turn else 1

        # forward movement (1 cell)
        if self.board[x][y + direction] == PieceName.EMPTY:
            self.possible_moves[x][y + direction] = 1

            # initial movement (2 cells)
            if y == start_row and self.board[x][y + 2 * direction] == PieceName.EMPTY:
                self.possible_moves[x][y + 2 * direction] = 1

        # diagonal capture
        for dx in [-1, 1]:
            i = x + dx
            j = y + direction
            if 0 <= i < 8 and 0 <= j < 8:
                if self.board[i][j] != PieceName.EMPTY and self.is_valid_capture(i, j):
                    self.possible_moves[i][j] = 2
