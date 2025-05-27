from Board import Board
from Entities.Pos import Pos
from Enums.Piece import PieceName, Color
class Piece():

    def __init__(self, board: Board, is_white_turn: bool) -> None:
        self.board = board
        self.is_white_turn = is_white_turn
        self.possible_moves = [[0 for _ in range(8)] for _ in range(8)]

    def is_white_piece(self, x: int, y: int) -> bool:
        piece = self.board[x][y]
        return piece != PieceName.EMPTY and piece.color == Color.WHITE

    def get_possible_moves(self) -> list[list[int]]:
        return self.possible_moves

    def is_valid_capture(self, i: int, j: int) -> bool:
        return (self.is_white_piece(i, j) and not self.is_white_turn) or \
            (not self.is_white_piece(i, j) and self.is_white_turn)

    def linear_or_diagonal_scan(self, posxy: Pos, dx: int, dy: int) -> None:
        x = posxy.x
        y = posxy.y
        i, j = x + dx, y + dy

        while 0 <= i < 8 and 0 <= j < 8:
            target_piece = self.board[i][j]

            if target_piece == PieceName.EMPTY:
                self.possible_moves[i][j] = 1  # valid move
            else:
                if self.is_valid_capture(i, j):
                    self.possible_moves[i][j] = 2  # valid capture
                break  # stop after finding a piece (own or enemy)
            i += dx
            j += dy

    def specific_scan_check(self,  posxy: Pos, dx: int, dy: int) -> None:
        x = posxy.x
        y = posxy.y
        i, j = x + dx, y + dy

        if 0 <= i < 8 and 0 <= j < 8:
            target = self.board[i][j]
            if target == PieceName.EMPTY:
                self.possible_moves[i][j] = 1
            elif self.is_valid_capture(i, j):
                self.possible_moves[i][j] = 2

    