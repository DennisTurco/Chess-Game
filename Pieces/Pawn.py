from Enums.Piece import Color, Piece

class Pawn:
    def __init__(self, board, is_white_turn):
        self.board = board
        self.is_white_turn = is_white_turn
        self.possible_moves = [[0 for _ in range(8)] for _ in range(8)]

    def is_white_piece(self, x, y):
        piece = self.board[x][y]
        return piece != Piece.EMPTY and piece.color == Color.WHITE

    def get_piece_at(self, x, y):
        return self.board[x][y] if 0 <= x < 8 and 0 <= y < 8 else None

    def generate_moves(self, posxy, piece_color):
        x, y = posxy

        if self.is_white_turn:
            self._forward_move_white(x, y)
            if piece_color == Color.WHITE:
                self._capture_white(x, y)
        else:
            self._forward_move_black(x, y)
            if piece_color == Color.BLACK:
                self._capture_black(x, y)

    def _forward_move_white(self, x, y):
        if self.get_piece_at(x, y - 1) == Piece.EMPTY:
            self.possible_moves[x][y - 1] = 1
            if y == 6 and self.get_piece_at(x, y - 2) == Piece.EMPTY:
                self.possible_moves[x][y - 2] = 1

    def _forward_move_black(self, x, y):
        if self.get_piece_at(x, y + 1) == Piece.EMPTY:
            self.possible_moves[x][y + 1] = 1
            if y == 1 and self.get_piece_at(x, y + 2) == Piece.EMPTY:
                self.possible_moves[x][y + 2] = 1

    def _capture_white(self, x, y):
        for dx in [-1, 1]:
            i, j = x + dx, y - 1
            if 0 <= i < 8 and 0 <= j < 8:
                target = self.get_piece_at(i, j)
                if target != Piece.EMPTY and not self.is_white_piece(i, j):
                    self.possible_moves[i][j] = 2

    def _capture_black(self, x, y):
        for dx in [-1, 1]:
            i, j = x + dx, y + 1
            if 0 <= i < 8 and 0 <= j < 8:
                target = self.get_piece_at(i, j)
                if target != Piece.EMPTY and self.is_white_piece(i, j):
                    self.possible_moves[i][j] = 2

    def get_possible_moves(self):
        return self.possible_moves
