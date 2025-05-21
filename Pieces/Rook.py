from Enums.Piece import Color, Piece

class Rook:
    def __init__(self, board, is_white_turn):
        self.board = board
        self.is_white_turn = is_white_turn
        self.possible_moves = [[0 for _ in range(8)] for _ in range(8)]

    def is_white_piece(self, x, y):
        piece = self.board[x][y]
        return piece != Piece.EMPTY and piece.color == Color.WHITE

    def generate_moves(self, posxy):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # vertical and horizontal
        for dx, dy in directions:
            self._scan_line(posxy, dx, dy)

    def _scan_line(self, posxy, dx, dy):
        x = posxy.x
        y = posxy.y
        i, j = x + dx, y + dy

        while 0 <= i < 8 and 0 <= j < 8:
            target_piece = self.board[i][j]

            if target_piece == Piece.EMPTY:
                self.possible_moves[i][j] = 1
            else:
                if (self.is_white_piece(i, j) and not self.is_white_turn) or \
                   (not self.is_white_piece(i, j) and self.is_white_turn):
                    self.possible_moves[i][j] = 2
                break
            i += dx
            j += dy

    def get_possible_moves(self):
        return self.possible_moves
