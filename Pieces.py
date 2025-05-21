class Piece:
    def __init__(self, color):
        self.color = color

    def is_white(self):
        return self.color == "w"

    def get_possible_moves(self, board, x, y):
        return []

class Rook(Piece):
    def get_possible_moves(self, board, x, y):
        moves = []
        return moves