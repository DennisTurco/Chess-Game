from Enums.Piece import Color, Piece

class Knight:
    def __init__(self, board, is_white_turn):
        self.board = board
        self.is_white_turn = is_white_turn
        self.possible_moves = [[0 for _ in range(8)] for _ in range(8)]

    def is_white_piece(self, x, y):
        piece = self.board[x][y]
        return piece != Piece.EMPTY and piece.color == Color.WHITE

    def generate_moves(self, posxy):
        moves = [(-1, -2), (-1, +2), (+1, +2), (+2, +1),
                 (+1, -2), (-2, +1), (+2, -1), (-2, -1)]
        for dx, dy in moves:
            self._check(posxy, dx, dy)

    def _check(self, posxy, dx, dy):
        x, y = posxy
        i, j = x + dx, y + dy

        if 0 <= i < 8 and 0 <= j < 8:
            target = self.board[i][j]
            if target == Piece.EMPTY:
                self.possible_moves[i][j] = 1
            elif (self.is_white_piece(i, j) and not self.is_white_turn) or \
                 (not self.is_white_piece(i, j) and self.is_white_turn):
                self.possible_moves[i][j] = 2

    def get_possible_moves(self):
        return self.possible_moves
