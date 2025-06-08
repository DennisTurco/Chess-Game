import chess
from Entities.Pos import Pos

class Piece:
    def __init__(self, board: chess.Board, is_white_turn: bool) -> None:
        self.board = board
        self.is_white_turn = is_white_turn
        self.possible_moves = [[0 for _ in range(8)] for _ in range(8)]

    def is_white_piece(self, x: int, y: int) -> bool:
        square = chess.square(x, 7 - y)  # converti coordinate (x,y) in square (python-chess)
        piece = self.board.piece_at(square)
        return piece is not None and piece.color == chess.WHITE

    def get_possible_moves(self) -> list[list[int]]:
        return self.possible_moves

    def is_valid_capture(self, x: int, y: int) -> bool:
        square = chess.square(x, 7 - y)
        piece = self.board.piece_at(square)
        if piece is None:
            return False
        # controllo che il pezzo appartenga al colore opposto rispetto al turno corrente
        if (piece.color == chess.WHITE and not self.is_white_turn) or (piece.color == chess.BLACK and self.is_white_turn):
            return True
        return False

    def linear_or_diagonal_scan(self, posxy: Pos, dx: int, dy: int) -> None:
        x, y = posxy.x, posxy.y
        i, j = x + dx, y + dy
        while 0 <= i < 8 and 0 <= j < 8:
            square = chess.square(i, 7 - j)
            target_piece = self.board.piece_at(square)
            if target_piece is None:
                self.possible_moves[j][i] = 1
            else:
                if self.is_valid_capture(i, j):
                    self.possible_moves[j][i] = 2
                break
            i += dx
            j += dy

    def specific_scan_check(self, posxy: Pos, dx: int, dy: int) -> None:
        x, y = posxy.x, posxy.y
        i, j = x + dx, y + dy
        if 0 <= i < 8 and 0 <= j < 8:
            square = chess.square(i, 7 - j)
            target_piece = self.board.piece_at(square)
            if target_piece is None:
                self.possible_moves[j][i] = 1
            elif self.is_valid_capture(i, j):
                self.possible_moves[j][i] = 2
